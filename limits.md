# Limits

What Guacamole cannot do, stated as
plainly as the rest of the guide.
Several of these are the same facts
as its strengths, from the other
side.

- **It is a gateway, not an agent.**
  No power control, no inventory, no
  reaching a machine whose remote
  protocols are all off, no help for
  a machine that cannot be reached on
  the network at all — a dead target
  stays dead. MeshCentral (chapter
  13) exists for that world.
- **The target must already speak.**
  RDP, VNC, SSH or telnet must be
  running on the far side. Guacamole
  adds no protocol to a machine that
  has none.
- **Video and games are out of
  scope.** The protocol is built from
  screen updates, not a video codec
  pipeline; full-screen motion,
  video playback inside a session,
  and anything latency-sensitive
  will feel like what it is — a
  gateway re-drawing your screen.
  Audio is uneven: SSH has none, VNC
  audio needs a cooperating target
  server (documented only here), RDP
  audio exists but shares the motion
  limits.
- **The browser is the ceiling and
  the floor.** No client install is
  the great convenience — and the
  browser sandbox bounds the rest:
  clipboard is plain text through a
  panel, local drives and printers
  arrive only through the gateway's
  own redirection features, and a
  browser that cannot do WebSocket
  cannot play.
- **One screen, mostly.** Multi-
  monitor estates are handled within
  protocol limits; the comfortable
  case is one display.
- **The file login is a rung, not a
  home** — MD5 hashes, no groups, no
  history, no sharing (chapters 4,
  7). The features that make
  Guacamole an organisational tool
  all live behind database or
  directory authentication.
- **Recordings show the screen, not
  the truth** — and can capture the
  secrets they audit (chapter 9).
- **guacd trusts its network.**
  The design assumes 4822 is
  reachable only by the web
  application; deployments that
  violate that assumption are not
  limited Guacamole, they are broken
  Guacamole (chapter 11).
- **Performance is per-session
  work.** guacd renders and encodes
  on the gateway; a small gateway
  serves a handful of graphical
  sessions well and a crowd poorly.
  The lab's guacd used two worker
  threads for one VNC screen on a
  2-CPU box — extrapolate honestly.
- **This guide's own limits** belong
  here too: RDP and telnet sessions,
  database authentication, Docker,
  sharing, and VNC audio were not
  run in the lab. They are described
  from the project's manual and
  labelled wherever they appear;
  the lab-verified core is the web
  application, the REST login, the
  file authentication, guacd with all
  four plugins built, complete SSH
  and VNC sessions, and session
  recording to video. The ledger in
  `criteria.md` is the exact list.
