# Guacamole for Mere Mortals

You have computers you need to reach —
a server in a rack, a desktop at the
office, a small machine at home — and
reaching them usually means a different
tool for each one: an SSH client for
the servers, a VNC viewer for the
desktops, an RDP client for the Windows
boxes, and a VPN before any of it works
from away. **Apache Guacamole** replaces
that drawer of tools with one web page.
You open your browser, log in once, and
the desktops and terminals of your other
machines appear inside the tab. The
machines themselves need nothing
installed or changed: Guacamole speaks
their own languages — **RDP**, **VNC**
and **SSH** — on their behalf.

This guide explains how that trick
works, how to install Guacamole, and
how to connect it to real machines.
Then it does the part most gateway
guides rush: proving the sessions are
real, recording one to a video file,
and locking the door properly — because
a program that puts every machine you
own behind one login is a door worth
locking well.

The lab behind this guide ran the real
thing: **Guacamole 1.6.0**, the official
release, on a small Linux machine. The
web application ran in Tomcat and was
logged into through its real API. The
native half, **guacd**, was compiled
from the project's own source with all
four of its protocol plugins — RDP,
SSH, VNC and telnet — and driven
through two complete sessions: an SSH
login to a fixture server and a VNC
session to a fixture desktop, with the
picture decoded and counted pixel by
pixel at the receiving end. A third
session was recorded and turned into a
real video file. Where the lab reached
a boundary — and it reached a few,
including one memorable networking
quirk — the guide says so, and the
troubleshooting chapter tells those
stories in full. Nothing here depends
on taking the author's word: the lab's
transcripts are in `guacamole-lab/`,
and every claim in these chapters
points at one.

Chapters 3 and 4 get you a running
Guacamole and a first login; chapter 5
opens the first live session. Chapter
11 is the one to read before Guacamole
faces any network you do not fully
control: it explains, in the project's
own words, which half of Guacamole
performs no authentication at all, and
what to do about that.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [SSH for Mere Mortals](https://paulsullivan33-dev.github.io/ssh-for-mere-mortals/)
- [RustDesk for Mere Mortals](https://paulsullivan33-dev.github.io/rustdesk-for-mere-mortals/)
- [MeshCentral for Mere Mortals](https://paulsullivan33-dev.github.io/meshcentral-for-mere-mortals/)
- [Tailscale for Mere Mortals](https://paulsullivan33-dev.github.io/tailscale-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/guacamole-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/guacamole-for-mere-mortals/blob/main/LICENSE-CODE).
