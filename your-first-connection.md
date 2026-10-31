# Your First Connection

By the end of this chapter an SSH
session has run end to end — browser
side, web application, guacd, target —
and been proven at three independent
points. This is the chapter the whole
lab was built for, and every number in
it comes from transcript
`t07-ssh-session.txt` and the logs of
the three programs involved.

## What the browser actually does

Clicking a connection in the web
client opens a **WebSocket** to a
tunnel endpoint on the web
application:

```
GET /guacamole/websocket-tunnel?...
-> HTTP/1.1 101 (connection upgraded)
```

The address carries the auth token
and three parameters that name the
destination — `GUAC_ID` (the
connection's identifier),
`GUAC_TYPE=c` (a connection, as
opposed to a group) and
`GUAC_DATA_SOURCE` (which login
database it came from). The lab's
client was a small Python program
rather than a browser (kept as
`guacamole-lab/guac_session.py`), and
finding those parameters took it three
failed attempts, each answered by the
server naming the next missing one:

```
Parameter "GUAC_ID" is required.
Parameter "GUAC_TYPE" is required.
Parameter "GUAC_DATA_SOURCE" is required.
```

That is a fine way to learn an API:
the error messages are the manual.

## The handshake, server side

With the tunnel open, the web
application does the guacd handshake
itself (chapter 2): `select` for the
SSH plugin, the plugin's `args` list
in reply, then `size`, `audio`,
`video`, `image`, and `connect`
carrying the parameters from the
connection's definition. guacd's debug
log shows its side of the exchange:

```
Creating new client for protocol "ssh"
Parameter "font-size" omitted.
  Using default value of 12.
WARNING: No known host keys provided,
  host identity will not be verified.
Supported authentication methods:
  publickey,password,keyboard-interactive
SSH connection successful.
```

Two lines deserve a pause. The
**defaults**: any parameter the
connection leaves out is filled from
the plugin's own defaults, and guacd
logs each one — reading a guacd log
is how you learn what a session
actually used. And the **host key
warning**: with no expected host key
configured, guacd accepts the SSH
server's key on trust. For a fixture
on loopback that is fine; for a real
server it is a hole — the `host-key`
parameter exists to close it, and
chapter 6 returns to it.

## The session, measured

Once connected, the remote terminal
arrives as protocol instructions. The
lab counted what its client received
over about sixteen seconds, including
typing one command
(`echo GUAC-LAB-MARKER-$((6*7))`) into
the shell:

```
instruction counts: {
  'sync': 21,      (finished frames)
  'rect': 10, 'cfill': 10, (painting)
  'img': 6, 'blob': 8,     (image tiles)
  'size': 7, 'move': 4, 'cursor': 1,
  'argv': 3, 'end': 9 }
```

Twenty-one finished frames for a
short session: the login banner, the
shell prompt, the typed command
echoing character by character, and
its answer. The client did not have
to believe any of it — in a second
run it **decoded the image stream**:
a PNG tile 240×19 pixels (one line of
terminal text) containing **720
distinct colours**. A blank or broken
pipeline does not produce anti-aliased
text pixels; something on the far side
really rendered a terminal, and the
far side's own log is the third proof:

```
Accepted password for labguest
  from 127.0.0.1 port 56924 ssh2
```

— the fixture SSH server recording
guacd's login in its own book. Three
programs, three logs, one session.

## The VNC session, briefly

The second connection — the fixture
desktop — ran the same path with the
VNC plugin (transcript
`t09-vnc-session.txt`): guacd created
a client for protocol `vnc`, reported
`Screen is now initialized`, and the
client received `img`, `blob` and
`copy` instructions carrying the
little test desktop (a virtual screen
running one clock). The VNC server's
log shows the connection arriving from
127.0.0.1 — guacd again, knocking on
the correct door. Graphical sessions
are chattier than terminal ones but
made of the same instructions.

## Reading a session's health

You now own a checklist for any real
session that misbehaves:

1. **Web application log** — did the
   login and tunnel creation succeed,
   or is there a named parameter or
   destination error?
2. **guacd log** — was a client
   created for the right protocol, and
   how far did its handshake get?
3. **Target log** — did anything knock
   at all, and what did the target
   refuse, if it refused?

Chapter 14 turns each failure the lab
actually met into an entry in that
form. Chapter 6 first takes the
connection parameters seriously —
there are forty-one of them for SSH
alone, and a handful decide whether a
real deployment is pleasant or
dangerous.
