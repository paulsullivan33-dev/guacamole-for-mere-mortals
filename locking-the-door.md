# Locking the Door

By the end of this chapter your
gateway's threat model fits on an
index card and each item on it has a
named defence. Read this before
Guacamole faces any network beyond
your own desk — including, especially,
a home network with other people's
devices on it.

## The threat model, plainly

Guacamole concentrates access. One
login stands in front of every
connected machine, with the
credentials for those machines often
stored behind it. An attacker who
gets in does not need to attack your
machines — they inherit your own
access to them. Everything below
follows from that single paragraph.

## Defence 1: guacd is not a door

The most important sentence in the
manual is in its Docker chapter, and
it is about guacd:

> "Take great care when doing this —
> guacd is a passive proxy and does
> not perform any kind of
> authentication. If you do not
> properly isolate guacd from
> untrusted parts of your network,
> malicious users may be able to use
> guacd as a jumping point to other
> systems."

guacd checks nothing. Anyone who can
open a TCP connection to port 4822
can ask it to connect anywhere it can
reach, using protocols it speaks. So:

- Bind guacd to **loopback** (the
  lab's choice: `-b 127.0.0.1`) or to
  a private container network (the
  Docker route's default), and never
  publish 4822 on a shared network,
  let alone the internet.
- Firewall it from everything except
  the web application, even on a LAN.
- Do not be reassured that "4822 is
  an obscure port". Obscurity is not
  authentication.

## Defence 2: HTTPS in front

The web application should be reached
over **HTTPS** only — a reverse proxy
(Nginx, Apache, Caddy) terminating
TLS in front of Tomcat is the usual
shape, with Tomcat itself bound to
loopback or a private address. The
manual's proxy notes matter here:
the proxy must pass WebSocket
upgrades (without them, sessions
silently fall back or fail) and
Tomcat's `RemoteIpValve` or the
proxy's headers must be configured
so logged addresses are the real
clients, not the proxy. Plain HTTP
on a LAN is a credential broadcast to
anyone listening.

## Defence 3: authentication worth the name

From chapters 4 and 7, in order of
increasing seriousness:

- **Never** run `user-mapping.xml` in
  production — the manual says so,
  and MD5 is why.
- Database accounts with strong
  passwords; change `guacadmin` the
  minute it exists.
- Add **TOTP** (or SSO with its own
  MFA) before any internet exposure.
- If you use header authentication
  behind a proxy, ensure the gateway
  **cannot be reached except through
  that proxy** — header auth trusts
  a header, and anyone who can talk
  to Tomcat directly can write it.

## Defence 4: least reach

- Connections grant the minimum: a
  user who needs one server does not
  get the folder of servers.
- Switch off what a connection does
  not need: clipboard, drive, SFTP,
  printing (chapter 6). Every enabled
  transfer path is a way for data to
  leave the target across your nice
  audited gateway, unaudited.
- Target credentials stored in
  connections are a convenience with
  a price; prefer per-user logins
  (tokens, chapter 6) where the
  estate allows.
- Verify targets: SSH `host-key`,
  RDP certificates not ignored. A
  gateway that trusts first contact
  can be fed a false machine.

## Defence 5: upkeep

- Sessions are observable: use the
  active-sessions and history views
  (chapter 8); a gateway nobody
  watches is a door nobody watches.
- Keep Guacamole, Tomcat, the JDK
  and the host patched; Guacamole's
  releases include security fixes
  like everyone else's.
- Back up `GUACAMOLE_HOME` and the
  database — they are the gateway's
  whole memory — and guard the
  backups as credentials, because
  that is what they contain.
- Recordings (chapter 9) are
  credentials-grade data too: they
  show screens, sometimes secrets.
  Store and rotate them like it.

## Check your defences

You have this chapter if you can
answer, for your own gateway: who
can reach 4822 (nobody but the web
application); how a browser reaches
the login (HTTPS, through a proxy);
what a stolen password alone buys an
attacker (ideally not enough — a
second factor stands behind it); and
what each connection is forbidden to
carry out.
