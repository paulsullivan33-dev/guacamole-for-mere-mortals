# The Moving Parts

By the end of this chapter you can name
the four pieces of a Guacamole system
and say which one you are looking at
when something breaks. Almost every
Guacamole problem belongs to exactly
one of them.

## 1. The browser client

The part you touch. Guacamole's client
is a **web page** — HTML and JavaScript
served by the gateway itself. It draws
the remote screen on a canvas, sends
your keystrokes and mouse movements
back, and handles the clipboard and
file transfers of chapter 10. There is
deliberately nothing to install: the
"client software" is whatever browser
you already have. When a session looks
wrong — a keyboard layout mismatch, a
stuck modifier key — the browser end
is one of the suspects.

## 2. The web application

The part that answers your browser.
The web application (packaged as a
Java **WAR file** — a web application
archive) runs inside a **servlet
container**, normally **Apache
Tomcat**. It serves the client pages,
checks your login, keeps the lists of
users and connections, and brokers
every session. Its home is a directory
called **GUACAMOLE_HOME**, holding:

- `guacamole.properties` — the main
  settings, above all where to find
  the third piece (below).
- `user-mapping.xml` — **only** if the
  simple file-based login is used
  (chapter 4).
- An `extensions/` folder — the
  add-ons (database login, LDAP,
  two-factor) of chapter 7.

The lab ran this half exactly so:
Tomcat serving the official
`guacamole-1.6.0.war`, verified against
the project's published SHA-256
checksum before it was trusted
(`guacamole-lab/transcripts/t00-downloads.txt`).

## 3. guacd — the proxy daemon

The part that does the remote-access
work. **guacd** is a small native
program (written in C) that listens on
**port 4822**. When the web application
asks it to open a session, guacd loads
a **protocol plugin** — one shared
library per protocol:

- `libguac-client-rdp` for RDP,
- `libguac-client-ssh` for SSH,
- `libguac-client-vnc` for VNC,
- `libguac-client-telnet` for telnet,

— and makes the real connection to the
target machine: the SSH login, the VNC
handshake, the RDP session. The remote
screen comes back to guacd, which
re-encodes it as Guacamole's own
protocol and hands it to the web
application for delivery to your tab.

Two facts about guacd matter more than
any other in this guide:

- **guacd performs no authentication.**
  The manual says it plainly: guacd is
  "a passive proxy". Anyone who can
  reach port 4822 can ask it to connect
  to anything it can reach. Chapter 11
  builds the defence; the lab simply
  bound guacd to the loopback address
  of its own machine, where only the
  web application could reach it.
- **guacd is where protocol support
  lives.** If a protocol is missing
  from the connection form, or a
  session fails in a protocol-specific
  way, this is the half to rebuild or
  inspect. The lab compiled guacd from
  source and got all four plugins into
  the build (chapter 3 tells how, and
  what refused to cooperate).

Two companion tools ship with guacd:
**guacenc**, which turns session
recordings into ordinary video files
(chapter 9, run for real in the lab),
and **guaclog**, which turns the input
log of a recorded terminal session
into readable text.

## 4. The target machines

The computers being reached. They run
whatever they already run — an SSH
server, a desktop sharing its screen,
a Windows box with Remote Desktop
enabled. Guacamole never installs
anything on them. When a session fails
at the far side — refused connection,
rejected password — the answer is in
the target's own logs, and the lab's
fixture targets demonstrate: its SSH
server's log line `Accepted password
for labguest` is one of the three
independent proofs that the lab's
first session really happened.

## The Guacamole protocol — the seam

Between guacd and the web application
(and onward, wrapped in a WebSocket,
to your browser) runs the **Guacamole
protocol**: a simple text stream of
**instructions**. Each instruction is a
list of length-prefixed pieces ending
in a semicolon, like:

```
5.ready,37.$725f3c86-3277-4c1a-834a-a7fa9003848f;
```

(`ready`, followed by the session's
identifier — a real one, captured in
the lab.) Drawing is instructions too:
`rect` and `cfill` paint rectangles,
`img` and `blob` deliver image tiles,
`sync` marks a finished frame. Your
input travels the other way as `key`
and `mouse` instructions. You never
need to write this protocol by hand —
but knowing it exists explains the
whole architecture: it is why the
browser client can be so thin, why
guacd can be shared by other programs,
and why session recordings (chapter 9)
are small files of instructions rather
than video until you ask guacenc to
render them.

The handshake at the start of every
session is also instructions, and
chapter 5 shows it happening: the web
application sends `select`, guacd
answers `args` with the list of
parameters the protocol understands
(forty-one of them for SSH, from
`hostname` and `port` to `color-scheme`
and `recording-path`), and the web
application replies with `size`,
`audio`, `video`, `image` and finally
`connect` carrying the values from the
connection's configuration.

## Check your understanding

Something is wrong and you must choose
where to look: logins rejected → the
web application and its authentication
(chapter 7). A protocol missing or a
session dying mid-handshake → guacd
and its plugins. A password refused by
the far machine → the target's logs.
A screen that draws garbage → the
browser end, or guacd's encoding.
That map is this chapter.
