# Users, Groups and Sharing

By the end of this chapter you know
what Guacamole's organisation tools
are and which of them the file-based
starter cannot do. Everything beyond
the file method in this chapter is
**documented from the manual**, as
chapter 7's note explained: the lab
proved the small case; this is the
large one, described faithfully and
labelled.

## Users and permissions

With database authentication, a user
is an account with **permissions**:
which connections and groups it may
use, and whether it may administer —
create users, edit connections, see
history. **System permissions** are
the coarse switches (administer the
system, create users, create
connections); **object permissions**
are per item (use this connection,
read that user's history). The
routine shape of a deployment: one or
two administrators, everyone else
 holding only the connections their
work needs — least privilege, in the
product's own vocabulary.

## User groups

Groups collect users so a connection
can be granted to a *team* once.
Groups can themselves be members of
groups and can hold permissions of
their own. This is the feature that
makes a fifty-person deployment
sane — and it belongs entirely to the
database and LDAP world. The file
method has no groups: each
`<authorize>` block is an island,
which is fine for one reader in a lab
and unworkable for a department.

## Connection groups

Connections organise too, and in two
flavours worth distinguishing:

- **Organisational groups** — folders.
  "Servers", "Office desktops", "Lab".
  Pure tidiness.
- **Balancing groups** — a connection
  that is really several machines:
  the user connects to the *group*,
  and Guacamole picks a member by
  load (fewest current users, or
  round-robin weights). The classic
  use is a pool of identical desktops
  or terminal servers.

Remember the tunnel parameters of
chapter 5: `GUAC_TYPE=c` named a
connection. A balancing group is what
the other value is for.

## Sharing a live session

Guacamole's most distinctive trick:
a session in progress can be
**shared**. The connection's owner
opens the session menu and gets a
sharing link (or invites specific
users); a second person joins the
*same* session — same screen, same
shell. The join can be **read-only**
(watch over a shoulder, from another
continent) or full (two drivers, one
keyboard apiece — take turns). The
manual's administration chapter
covers the share profiles that decide
which. For support work and teaching
this is the feature the alternatives
in chapter 13 mostly lack.

## Keeping an eye on things

Administrators get the other half of
the story:

- **Active sessions** — who is
  connected to what, right now, with
  the ability to end a session.
- **History** — the database's record
  of past connections: user,
  connection, start, end. (The lab
  saw the file method's shadow of
  this: its connections API reported
  `activeConnections: 0` for each
  connection — the counter exists;
  the file method simply has no
  history behind it.)
- **Settings** — the web interface's
  own page of the same
  `guacamole.properties` world:
  connection limits per user and in
  total live here as connection
  attributes too (`max-connections`,
  `max-connections-per-user`).

## Check your understanding

You have this chapter if you can
separate the three kinds of grouping
(user groups grant, organisational
groups tidy, balancing groups pool),
say what session sharing adds, and
name the price: all of it needs the
database or directory of chapter 7.
