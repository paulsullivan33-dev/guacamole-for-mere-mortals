# First Login

By the end of this chapter you have
logged in to Guacamole for real, and
created the two connections the next
chapter will open. The method used
here — a single XML file — is the
project's built-in starter mechanism,
and this chapter follows the manual in
being blunt about it: **it is for
verifying an installation, not for
production.** Chapter 7 replaces it
with database authentication. But as
a first rung it is perfect: one file,
no database, and every part of it can
be inspected with your own eyes.

## The file: user-mapping.xml

Guacamole's built-in authentication
reads `GUACAMOLE_HOME/user-mapping.xml`.
The lab's file (kept, with its fixture
passwords redacted, as
`guacamole-lab/user-mapping.xml`)
defines one user and two connections:

```xml
<user-mapping>
  <authorize username="labreader"
             password="[md5 of the password]"
             encoding="md5">
    <connection name="Lab SSH shell">
      <protocol>ssh</protocol>
      <param name="hostname">127.0.0.1</param>
      <param name="port">18222</param>
      <param name="username">labguest</param>
      <param name="password">[fixture]</param>
    </connection>
    <connection name="Lab VNC desktop">
      <protocol>vnc</protocol>
      <param name="hostname">127.0.0.1</param>
      <param name="port">5901</param>
      <param name="password">[fixture]</param>
    </connection>
  </authorize>
</user-mapping>
```

Read it slowly; it teaches the whole
model:

- A **user** is an `<authorize>` block.
  The password is stored as an **MD5
  hash** (`echo -n 'your-password' |
  md5sum`), never as plain text in
  this file. (MD5 is weak by modern
  standards — one more reason this
  method is a starter, not a home.)
- A **connection** is a name, a
  protocol, and a list of **parameters
  ** — the same parameters guacd
  listed in its `args` reply in
  chapter 2. Hostname and port say
  where the target lives; the rest
  tell the protocol plugin how to
  behave when it gets there.
- Connections belong to the user who
  may use them. Two users, two
  different lists — that is the whole
  access-control model of the file
  method.

The lab's targets are deliberately
small: an SSH server on a high
loopback port with a single fixture
account, and a VNC server sharing a
test desktop (a virtual screen with
one clock drawn on it — the lab's
fixture targets, not real machines).
Yours will be real addresses; nothing
about the file changes.

## Telling the web application where guacd is

One more file in GUACAMOLE_HOME,
`guacamole.properties`, needs two
lines in the lab's layout (kept as
`guacamole-lab/guacamole.properties`):

```
guacd-hostname: 127.0.0.1
guacd-port: 4822
```

These are also the defaults, but
writing them down is how you remember
the seam exists. Restart Tomcat after
changing either file; the
user-mapping is read at login time,
but the properties belong to startup.

## Proving the login — without a browser

The web client's login form talks to
a **REST API**, and anything the form
can do, a command line can do. That
gives this chapter its check, run for
real in the lab (transcript
`t04-rest-login.txt`). First, a wrong
password, to watch the door stay shut:

```
POST /guacamole/api/tokens
  username=labreader&password=wrong-password

-> HTTP 403
{"message":"Permission Denied.", ...
 "type":"INVALID_CREDENTIALS"}
```

Then the real credentials:

```
POST /guacamole/api/tokens
  username=labreader&password=[the lab password]

{
  "authToken": "95030EBA...[redacted]",
  "username": "labreader",
  "dataSource": "default",
  "availableDataSources": ["default"]
}
```

The **auth token** is the session
key: the browser holds one exactly
like it and presents it with every
request. (The token above is printed
as the lab printed it — first eight
characters only. Treat real tokens
like passwords; they are bearer
credentials.)

With the token, the API shows what
the login bought (transcript
`t05-connections-api.txt`): a request
to `/api/session/data/default/connections`
returns both connections from the
file, each with its protocol and a
count of active connections —
`"Lab SSH shell"`, protocol `ssh`,
and `"Lab VNC desktop"`, protocol
`vnc`. If your connections do not
appear here, the file has a syntax
error or sits in the wrong
GUACAMOLE_HOME; Tomcat's log says
which, and chapter 14 collects the
symptoms.

## Check your login

You have this chapter if the wrong
password earns a 403, the right one
earns a token, and the connections
endpoint lists what your file
defines. Chapter 5 spends the token:
it opens the SSH connection and
follows the session all the way to
the fixture server's own logbook.
