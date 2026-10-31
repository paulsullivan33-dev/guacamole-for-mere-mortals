# Recipes

Small, complete jobs. Each names the
chapters it stands on. Recipes marked
*(lab)* were run, in substance, by the
guide's own lab.

## 1. The five-minute home gateway *(lab)*

Docker route (chapter 3), database
initialised with the shipped schema
(chapter 7), one admin, one SSH
connection per machine. Change the
default admin password before adding
the second machine. You now have the
deployment most homes actually need.

## 2. Verify a new installation without a browser *(lab)*

Chapters 4 and 5, as commands: POST
to `/api/tokens` with a deliberately
wrong password (expect 403), then
with the right one (expect a token),
then GET
`/api/session/data/<source>/connections`
with the token and confirm your
connections are listed. Three answers
prove the web application, its
authentication and its configuration
in one pass — the same pass the lab's
transcripts `t04` and `t05` record.

## 3. A read-only window onto a family PC

VNC connection (chapter 6) with
`read-only` set, granted to a
helper's account. They can see the
screen and talk the owner through a
fix; they cannot click anything
themselves. Remove the grant when
the fix is done.

## 4. One program, not one machine

SSH connection with `command` set
(chapter 6) — a menu script, a log
viewer, a backup-status page. The
user logs in through Guacamole and
lands in exactly that program; when
it exits, the session ends. The
smallest possible door.

## 5. Record everything, watch selectively

Set `recording-path` on the
connections that matter (chapter 9),
leave `recording-include-keys` **off**,
and run guacenc only when a session
needs reviewing. A cron line that
encodes yesterday's recordings and
deletes originals older than your
retention completes the habit —
recordings are small, but forever is
a long time.

## 6. A pool of identical desktops

Several same-image machines inside a
**balancing group** (chapter 8); one
link on every user's home screen,
nobody cares which machine they got.
The recipe for classroom and
call-centre desktops.

## 7. Support session with a witness

Open the session, share it read-only
(chapter 8) to a colleague, fix the
problem while they watch and take
notes. The recording recipe above
makes the same session reviewable
afterwards.

## 8. Retire a machine completely

Delete (do not merely disable) its
connection, remove any stored
credentials for it, and check
history for its last uses. A decommissioned
machine that remains a Guacamole
connection is a door to whatever its
address is reused by.
