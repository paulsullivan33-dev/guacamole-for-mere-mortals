# The Neighbours

Guacamole is one shape of remote
access. These are the others, named
fairly, with the honest rule for
choosing. All four have guides of
their own in this series.

## RustDesk — the direct answer

[RustDesk for Mere Mortals](https://paulsullivan33-dev.github.io/rustdesk-for-mere-mortals/)
is remote desktop without a gateway:
install it on both ends (or run your
own relay), and one machine shows
another's screen. For helping a
relative or reaching your own desktop
from your own laptop, it is less
machinery than Guacamole and the
right choice. What it does not have:
the browser-only client, the
multi-protocol reach (it is desktops,
not SSH terminals), per-user
connection lists, and session
recordings. Choose it when the
relationship is one-to-one and both
ends can run software.

## MeshCentral — the management fleet

[MeshCentral for Mere Mortals](https://paulsullivan33-dev.github.io/meshcentral-for-mere-mortals/)
is also a web interface to many
machines — the closest neighbour in
this chapter — but it reaches them
through an **agent installed on each
machine**. The agent buys what
Guacamole cannot do: power control,
hardware inventory, terminal and file
access even where no remote protocol
is enabled, machines phoning home
from behind NAT. The price is the
agent itself — software to install,
update and trust on every target.
Choose MeshCentral when you *manage*
the machines; choose Guacamole when
you merely *visit* them, or when the
machines cannot take an agent.

## SSH, plain — the terminal itself

[SSH for Mere Mortals](https://paulsullivan33-dev.github.io/ssh-for-mere-mortals/)
is what Guacamole's SSH plugin speaks
to. A terminal and an SSH client
remain the fastest, lightest way to
run a server you alone use. Guacamole
adds value when the client machine
cannot have an SSH client, when the
login must be brokered and recorded,
or when terminals and desktops need
one front door. It does not make SSH
itself better — and its SSH is a
terminal in a browser, slightly
heavier than the real thing.

## Tailscale and WireGuard — move the network instead

[Tailscale for Mere Mortals](https://paulsullivan33-dev.github.io/tailscale-for-mere-mortals/)
(and its WireGuard foundation) take
the opposite approach to the whole
problem: instead of a gateway that
speaks every protocol, build a
private network on which your devices
simply *are* together — then use each
machine's own native clients. It is
the strongest answer when every end
is yours to enrol. It cannot help a
borrowed browser, gives no central
session recording, and expects the
target machines to join the network.
Many real setups combine the two: a
gateway for people, a mesh for
machines.

## The rule

- One person, their own machines, any
  client software allowed: **direct
  tools** (SSH, RustDesk) or a **mesh**
  (Tailscale).
- Machines you manage end to end,
  agents welcome: **MeshCentral**.
- Many machines, many people, browser
  the only common client, sessions
  worth recording: **Guacamole**.
