# What Guacamole Is

You are away from your desk, on a
 borrowed laptop or a tablet, and you
need the machine back home — the file
on its desktop, the terminal on the
server under the stairs. The usual
answers each cover one case.
**Apache Guacamole** covers all of
them with a single web page.

**Guacamole is a remote access
gateway.** A gateway is a program that
sits between you and a set of machines,
speaks to each machine in its own
language, and presents the result in
one place. Guacamole's languages are
the three standard remote-access
protocols — **RDP** (the Windows
remote desktop protocol), **VNC** (the
long-standing graphical desktop
protocol) and **SSH** (the secure
shell used by servers everywhere) —
plus **telnet**, kept for old equipment
that speaks nothing newer. Its
presentation is your **browser**: no
client program to install, nothing to
keep updated on the machine in your
hands. If a device can open a modern
web page, it can be your window onto
every machine behind the gateway.

This is worth pausing on, because it
is the reason the tool exists. The
target machines need **no agent, no
account and no changes**. A Windows
box that already allows Remote Desktop,
a Linux server that already runs SSH,
a desktop already sharing its screen
by VNC — Guacamole can reach all three
today, as they are. The gateway learns
a new machine when you type its
address and credentials into a form.

## Who it is for

Guacamole earns its place when one or
more of these is true:

- You look after **several machines**
  and want one door and one login
  instead of a drawer of client tools.
- You need to reach machines from
  **devices you cannot install
  software on** — a borrowed laptop, a
  tablet, a locked-down work machine.
- You help **other people** reach
  machines — family desktops, a small
  team's servers — and want to hand
  them a web address, not a
  configuration file.
- You want **records**: who connected,
  to what, and (chapter 9) even a
  video of the session.

It is the wrong tool for reaching one
machine from one other machine, both
yours: a direct SSH client or a mesh
tool like RustDesk is less machinery
for that job. Chapter 13 compares the
neighbours honestly.

## The one warning, up front

A gateway concentrates risk exactly as
much as it concentrates convenience.
Whoever gets through Guacamole's login
stands in front of every machine you
connected to it. That is manageable —
chapter 11 is devoted to it — but it
shapes the whole design of this guide:
strong authentication is not an
optional extra at the end, and the
simplest login method, the one the lab
uses to prove everything works, is one
the project's own manual tells you
**not** to run in production. You will
meet that warning again, in context,
in chapters 4 and 7.

## A first taste

After installing (chapter 3) and
configuring one connection (chapter
4), using Guacamole is unremarkable —
which is the point:

1. Open `https://your-gateway/guacamole/`
   in any browser.
2. Log in. You see a list of the
   machines you may reach.
3. Click one. Its desktop — or its
   terminal — fills the tab, live.

The lab's transcripts show the machine
room view of step 3: the browser
receiving drawing instructions —
rectangles, image tiles, cursor moves
— twenty-one screen updates for one
short SSH session, whose pixels the
lab decoded and verified rather than
admired (`guacamole-lab/transcripts/t07-ssh-session.txt`).

## Check your understanding

You have this chapter if you can say:
Guacamole is a gateway, not a client;
the machines it reaches need nothing
installed; its protocols are RDP, VNC,
SSH and telnet; and its convenience
and its risk are the same fact seen
from two sides.
