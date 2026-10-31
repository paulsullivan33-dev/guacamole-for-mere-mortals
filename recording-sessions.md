# Recording Sessions

By the end of this chapter a real
session has been recorded and turned
into a real video file — in the lab,
not in theory. The evidence is
transcript `t11-recording.txt`, and
the artefact is honest about its
size: ten seconds of a terminal
session became a ten-second MPEG-4
video at 1024×768.

## Two kinds of recording

Guacamole can record a session in two
forms, set per connection:

- **Graphical recording** — the
  protocol instruction stream itself,
  saved by guacd to a file. Play it
  back in the browser (with the
  session-recording player extension)
  or render it to video with
  **guacenc**. Set with
  `recording-path` and
  `recording-name`; add
  `create-recording-path` if the
  directory may not exist yet, and
  `recording-include-keys` if typed
  keys (which graphical recordings
  otherwise leave out) must be in the
  picture. The SSH parameter list from
  the lab's handshake shows the whole
  family: `recording-exclude-output`,
  `recording-exclude-mouse`,
  `recording-write-existing` are
  there beside them.
- **Typescript** — for SSH and telnet
  only: the terminal's text, timed,
  saved as a pair of files (the text
  and its timing). `guaclog` turns a
  typescript into plain readable text.
  Set with `typescript-path` and
  `typescript-name`.

Recordings are written **by guacd, on
the gateway machine** — the user in
the session gets no say and no copy.
That is what makes them evidence
rather than souvenirs.

## The lab's recording, step by step

The lab drove one short SSH session
(the raw-protocol route of chapter 2,
this time by hand rather than through
the web application) with the
recording parameters set. guacd
wrote:

```
recordings/lab-ssh-session   12,133 bytes
```

Twelve kilobytes for ten seconds —
the instruction stream is compact,
which is the practical reason
recordings can be kept for every
session rather than sampled.

Then guacenc, twice. The first try
refused, and its refusal is worth
learning:

```
guacenc: WARNING: Refusing to encode
in-progress recording
"recordings/lab-ssh-session"
(specify the -f option to override
this behavior).
```

A recording whose session ended
cleanly carries a proper finish;
this one had been cut off by hand,
so guacenc treated it as possibly
still being written. With `-f`:

```
guacenc: INFO: Encoding
"recordings/lab-ssh-session" to
"recordings/lab-ssh-session.m4v" ...
guacenc: INFO: All files encoded
successfully.
```

And the result, measured rather than
described:

```
codec_name=mpeg4, width=1024,
height=768, duration=10.04 s,
649,554 bytes
```

A video you can hand to someone who
has never heard of Guacamole — an
auditor, a manager, your future self
— and they can simply watch what the
session did. Encoding is a rendering
job (it ran through the FFmpeg
libraries the lab's configure found),
so batch it off-hours for long
recordings.

## Honest limits of a recording

- A graphical recording shows the
  **screen**, not the truth behind
  it. A user who opens a file sees
  its contents drawn; a user who
  reads a secret sees it too. Review
  recordings before sharing them —
  they can contain exactly the
  credentials they were meant to
  audit.
- `recording-include-keys` is off by
  default for a reason: with it on,
  everything typed — passwords
  included — is in the file.
- Storage is small per session and
  unbounded in total; a busy gateway
  needs a rotation habit (chapter 12
  has one).

## Check your recording

You have this chapter if you can set
the two recording parameters, say
where the file lands and whose
program writes it, and turn a
finished recording into a video with
one command — and if you remember
that guacenc's refusal to touch an
unfinished recording is a safety
feature, not an error.
