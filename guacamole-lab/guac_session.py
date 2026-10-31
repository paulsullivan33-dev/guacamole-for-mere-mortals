#!/usr/bin/env python3
"""Drive one real Guacamole session through the webapp websocket tunnel.

Minimal RFC 6455 client + Guacamole instruction parser, stdlib only.
Logs in via the REST API, opens the tunnel for one connection, records
the instruction stream, optionally types a command, and disconnects.
The auth token value is never printed.
"""
import base64, hashlib, json, os, socket, struct, sys, time
import urllib.request, urllib.parse

BASE = "http://127.0.0.1:18103/guacamole"
WS_HOST, WS_PORT = "127.0.0.1", 18103

def get_token(user, password):
    data = urllib.parse.urlencode({"username": user, "password": password}).encode()
    req = urllib.request.Request(BASE + "/api/tokens", data=data)
    with urllib.request.urlopen(req) as r:
        return json.load(r)["authToken"]

class WS:
    def __init__(self, path):
        self.sock = socket.create_connection((WS_HOST, WS_PORT), timeout=15)
        key = base64.b64encode(os.urandom(16)).decode()
        self.buf = b""
        req = (f"GET {path} HTTP/1.1\r\nHost: {WS_HOST}:{WS_PORT}\r\n"
               "Upgrade: websocket\r\nConnection: Upgrade\r\n"
               f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
               "Sec-WebSocket-Protocol: guacamole\r\n\r\n")
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise RuntimeError("no handshake response")
            resp += chunk
        head, _, rest = resp.partition(b"\r\n\r\n")
        self.buf = rest
        status = head.split(b"\r\n")[0].decode()
        print("websocket handshake:", status)
        if b"101" not in head.split(b"\r\n")[0]:
            raise RuntimeError("handshake failed: " + head.decode(errors="replace")[:200])

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise EOFError
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def recv_text(self, timeout=10):
        self.sock.settimeout(timeout)
        while True:
            b1, b2 = self._read(2)
            fin, op = b1 & 0x80, b1 & 0x0F
            ln = b2 & 0x7F
            if ln == 126: ln = struct.unpack(">H", self._read(2))[0]
            elif ln == 127: ln = struct.unpack(">Q", self._read(8))[0]
            if b2 & 0x80:
                mask = self._read(4)
                payload = bytes(x ^ mask[i % 4] for i, x in enumerate(self._read(ln)))
            else:
                payload = self._read(ln)
            if op == 9:  # ping -> pong
                self.send_frame(0xA, payload); continue
            if op == 8:
                raise EOFError("close frame")
            if op in (1, 2, 0):
                return payload

    def send_frame(self, op, payload):
        mask = os.urandom(4)
        ln = len(payload)
        if ln < 126: head = struct.pack("BB", 0x80 | op, 0x80 | ln)
        elif ln < 65536: head = struct.pack(">BBH", 0x80 | op, 0x80 | 126, ln)
        else: head = struct.pack(">BBQ", 0x80 | op, 0x80 | 127, ln)
        masked = bytes(x ^ mask[i % 4] for i, x in enumerate(payload))
        self.sock.sendall(head + mask + masked)

    def send_text(self, s):
        self.send_frame(1, s.encode())

def parse_instructions(text, state):
    """Feed text into Guacamole instruction parser; returns list of (op, args)."""
    out = []
    state["buf"] += text
    buf = state["buf"]
    while True:
        # one instruction: elements 'len.value' joined by ',' ended by ';'
        pos, elements, ok = 0, [], True
        while True:
            dot = buf.find(".", pos)
            if dot == -1: ok = False; break
            try: ln = int(buf[pos:dot])
            except ValueError: ok = False; break
            if len(buf) < dot + 1 + ln + 1: ok = False; break
            elements.append(buf[dot + 1: dot + 1 + ln])
            sep = buf[dot + 1 + ln]
            pos = dot + 1 + ln + 1
            if sep == ";": break
            if sep != ",": ok = False; break
        if not ok: break
        out.append(elements)
        buf = buf[pos:]
    state["buf"] = buf
    return out

def fmt_instr(elements):
    parts = []
    for e in elements:
        parts.append(e if len(e) <= 44 else e[:41] + "...")
    return ",".join(parts)

def main():
    conn_name = sys.argv[1]           # e.g. "Lab SSH shell"
    type_text = sys.argv[2] if len(sys.argv) > 2 else ""
    token = get_token("labreader", os.environ.get("GUAC_LAB_PASSWORD", ""))
    print("REST login OK (token value not printed)")
    q = urllib.parse.urlencode({
        "token": token, "GUAC_ID": conn_name,
        "GUAC_TYPE": "c", "GUAC_DATA_SOURCE": "default",
        "GUAC_WIDTH": "1024", "GUAC_HEIGHT": "768", "GUAC_DPI": "96"})
    ws = WS(f"/guacamole/websocket-tunnel?{q}")
    # Per ConfiguredGuacamoleSocket in guacamole-client 1.6.0, the webapp
    # performs the whole guacd handshake itself (select/args/size/connect);
    # the client just receives the resulting instruction stream.
    state = {"buf": ""}
    seen, frames, blobs = {}, 0, 0
    started = time.time()
    typed = False

    def pump(seconds):
        nonlocal frames, blobs
        end = time.time() + seconds
        while time.time() < end:
            try:
                payload = ws.recv_text(timeout=max(1, end - time.time()))
            except (socket.timeout, TimeoutError):
                break
            if payload:
                print(f"  [frame {len(payload)} bytes]")
            for el in parse_instructions(payload.decode("utf-8", "replace"), state):
                op = el[0]
                seen[op] = seen.get(op, 0) + 1
                if op == "blob": blobs += 1
                if op in ("ready", "name", "error", "disconnect", "args"):
                    print("  instr:", fmt_instr(el))
                if op == "sync": frames += 1

    pump(10)  # connect, plugin loads, remote login happens
    if type_text:
        instr = []
        for ch in type_text:
            instr.append(f"3.key,{len(str(ord(ch)))}.{ord(ch)},1.1;")
            instr.append(f"3.key,{len(str(ord(ch)))}.{ord(ch)},1.0;")
        instr.append("3.key,5.65293,1.1;3.key,5.65293,1.0;")
        ws.send_text("".join(instr))
        print("sent keystrokes:", repr(type_text), "+ Enter")
        typed = True
        pump(6)
    try:
        ws.send_text("10.disconnect;")
    except Exception:
        pass
    print("instruction counts:", dict(sorted(seen.items())))
    print(f"frames (sync): {frames}, blobs: {blobs}, elapsed: {time.time()-started:.1f}s, typed: {typed}")

if __name__ == "__main__":
    main()
