# Connections in Depth

By the end of this chapter you can
read a connection definition the way
guacd does, and you know the handful
of parameters per protocol that change
a deployment's character. The full
parameter lists are long — the SSH
plugin alone answered the lab's
handshake with forty-one names — so
this chapter teaches the load-bearing
ones and shows you where the rest
live: in guacd's `args` reply, and in
the manual's chapter per protocol.

## The shape of every connection

Whatever the protocol, a connection's
parameters answer four questions:

- **Where?** `hostname`, `port`. The
  defaults are the protocol's own
  (SSH 22, VNC 5900, RDP 3389, telnet
  23); the lab's connections set both,
  because its targets lived on
  nonstandard ports — as yours may,
  behind port forwarding or on
  multi-service machines.
- **As whom?** `username`, `password`,
  or key material. Storing a target's
  password in the connection lets a
  user open it without knowing the
  password — convenient, and a real
  decision: you are concentrating that
  credential in Guacamole (chapter
  11). Leaving them blank makes the
  user type them at connect time.
- **How should it look and behave?**
  The display and session parameters.
- **What is it allowed to do?** The
  permission parameters — clipboard,
  file transfer, printing. These are
  security settings wearing a UI
  costume.

## SSH

The terminal protocol, and the one
the lab exercised most:

- `color-scheme` and `font-name` /
  `font-size` — the terminal's look;
  guacd renders the text itself, so
  these are real rendering choices,
  not hints. The lab's session ran
  on the logged defaults
  (`monospace`, 12).
- `host-key` — the expected SSH host
  key of the target, in the usual
  OpenSSH format. Set it, and guacd
  verifies the server's identity
  instead of trusting first contact
  (the warning in chapter 5 is what
  happens when you do not).
- `private-key` and `passphrase` —
  key-based login in place of a
  password.
- `enable-sftp` — turns on file
  transfer over the same connection
  (chapter 10). The lab's parameter
  list shows its companions:
  `sftp-root-directory`,
  `sftp-disable-download`,
  `sftp-disable-upload` — the shape of
  a permission system in miniature.
- `command` — run this instead of a
  shell: the way to hand someone one
  program (a menu, a log tailer)
  instead of a machine.
- `typescript-path` / `typescript-name`
  — a text recording of the terminal
  session, the terminal counterpart of
  chapter 9's graphical recordings,
  readable afterwards through
  `guaclog`.

## VNC

The desktop protocol at its simplest:

- `password` — the VNC server's
  password (VNC's own authentication
  is famously thin; eight characters
  is its historical limit — one reason
  VNC targets should live on trusted
  networks, with Guacamole as the
  strong door in front of them).
- `read-only` — view without touching:
  the support-desk and classroom mode.
- `swap-red-blue`, `cursor`,
  `color-depth` — the pragmatic
  fixes for odd servers and slow
  links, in the manual's VNC chapter.
- Clipboard and **audio** parameters
  exist too (`enable-audio` with a
  PulseAudio server on the target) —
  the lab's build included the Pulse
  library, but its fixture desktop
  had no audio to give, so this guide
  labels VNC audio **documented
  only**.

## RDP

The richest parameter set, and the
one where Guacamole changes a Windows
machine's life most:

- `domain`, `username`, `password` —
  and `ignore-cert`, which you should
  meet with suspicion: it silences
  the target's certificate check.
- `security` — the negotiation mode
  (`any`, `nla`, `tls`, `rdp`).
  Network Level Authentication (NLA)
  is the modern default to prefer.
- `resize-method` — how the remote
  desktop follows your browser
  window's size (`display-update`
  asks the server to resize for real).
- **Drive redirection** — `enable-drive`,
  `drive-path`, `create-drive-path`:
  a folder on the Guacamole machine
  appears inside the RDP session as a
  shared drive. File transfer in both
  directions, and therefore a chapter
  11 topic as much as a convenience.
- `enable-printing` (print to a PDF
  that downloads to your browser),
  `enable-audio`, `disable-audio`,
  and the **performance** switches —
  `enable-wallpaper`, `enable-theming`,
  `enable-font-smoothing` — the
  standard trade of beauty for
  bandwidth on slow links.
- `gateway-*` parameters — reaching
  targets through an RDP gateway, for
  estates that have one.

The lab's RDP plugin was **built and
loaded** (it sits in guacd's plugin
directory alongside the others,
transcript `t10-tools.txt`), but the
lab had **no Windows or xrdp target**
to connect it to — so everything
about RDP *sessions* in this guide is
documented from the manual, and is
labelled as such wherever it matters.
The same honesty applies to **telnet**:
the plugin built, no legacy target
was available, and its chapter of the
manual is the source.

## Where parameters can live

In the file method (chapter 4) every
parameter sits in the open, per user.
Database authentication (chapter 7)
changes the game in two ways: values
can contain **parameter tokens** —
`${GUAC_USERNAME}` and friends, filled
in from the logged-in user's own
details at connect time — and the
manual documents attributes that let
an LDAP directory supply hostnames
per user. The single most useful
pattern this enables: **one connection
definition, many users**, each landing
on their own machine or account
without anyone's password being
stored at all.

## Check your understanding

You have this chapter if, shown any
connection, you can sort its
parameters into *where*, *as whom*,
*how it behaves* and *what it may
do* — and if you can name the one
parameter (`host-key`, or RDP's
certificate handling) that decides
whether the gateway checks it is
talking to the machine it thinks it
is.
