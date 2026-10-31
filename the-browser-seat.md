# The Browser Seat

By the end of this chapter you know
what it is like to sit in front of a
Guacamole session — what the browser
end does well, what it cannot do, and
which of its features are really
gateway decisions. The stream-level
facts are from the lab; the
interaction details are the manual's
client chapter, labelled as before.

## The screen

The remote display draws on a canvas,
repainted frame by frame as `sync`
instructions arrive — the lab's SSH
session produced twenty-one frames in
sixteen seconds, the VNC session
fewer, larger ones. On a healthy link
the result feels local for terminals
and office desktops. It is not a
video stream: static parts of the
screen are sent once and copied
client-side (the `copy` instructions
in the VNC transcript are exactly
that), which is why Guacamole sips
bandwidth compared with streaming a
movie of your desktop — and why fast
motion is its weak suit (chapter 12).

The session menu — the client's own
drawer, summoned with a key
combination or a swipe — holds the
controls below, plus zoom, window
size behaviour, and the on-screen
keyboard.

## The clipboard

Copy in the remote session, paste on
your machine, and the reverse: the
menu's clipboard panel is the bridge.
It works, with a plain-text honesty
(resized or rich content does not
cross). **The important part is
administrative**: clipboard access
can be switched off per connection
(`disable-copy`, `disable-paste` in
the SSH list; equivalents elsewhere)
— because a clipboard is a file
transfer that nobody logs, and on a
sensitive target it should be off on
purpose, not by accident.

## Files in and out

Two roads, depending on protocol:

- **SFTP over SSH connections** —
  with `enable-sftp` set (chapter 6),
  the session's file browser uploads
  and downloads through the same SSH
  connection. The lab's build has the
  SSH plugin and the parameter is in
  its `args` list; the lab did not
  exercise a transfer, so the
  workflow is documented from the
  manual.
- **The RDP drive** — `enable-drive`
  makes a gateway folder appear
  inside the session as a shared
  drive; files placed there download
  to the browser from the menu. PDFs
  from `enable-printing` arrive down
  the same road.

Either road is a door in the wall a
gateway is supposed to be. Enable
per connection, on purpose.

## Keyboard, mouse, touch

The client sends your keyboard as
**keysyms** — the lab's client
literally typed `key` instructions,
character by character, and read the
shell's answer in the frames — so
layout mismatches are a known
species of problem (the target's
layout, set per connection for RDP,
matters more than your physical
keyboard's). The mouse is fully
supported including the wheel; on
touch devices the client offers both
absolute (tap = click there) and
relative (trackpad-style) modes, and
the on-screen keyboard covers the
no-keyboard case. None of it needs
configuration to be usable; all of
it is in the manual's client chapter.

## Multiple monitors, reality-checked

RDP and the client both understand
multi-monitor targets within limits
set by the protocol and the gateway's
own display size; the pragmatic
summary is that one good monitor's
worth of desktop is the comfortable
case, and chapter 12 lists display
size among the honest limits.

## Check your understanding

You have this chapter if you can say
where the clipboard bridge lives and
how to close it, name the two file
roads and their protocols, and
explain why a still screen costs
almost no bandwidth while a video
playing inside the session costs
plenty.
