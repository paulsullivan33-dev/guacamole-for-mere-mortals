# Glossary

**Balancing group** — A connection
group whose members are equivalent
machines; connecting to the group
connects you to one member, chosen
by load.

**Connection** — A named definition:
one protocol, one target, and the
parameters for reaching it. What a
user clicks.

**Connection group** — A folder of
connections (organisational) or a
pool of them (balancing).

**Data source** — Where a login was
authenticated and its connections
came from: the built-in file,
a database, a directory. Named in
the login token and in tunnel
requests (`GUAC_DATA_SOURCE`).

**Extension** — A JAR in
`GUACAMOLE_HOME/extensions/` that
adds an authentication method or a
feature (database, LDAP, TOTP,
recording playback).

**Gateway** — A program that stands
between users and machines, speaking
to each side in its own terms.
Guacamole is one.

**guacd** — The native proxy daemon.
Listens on port 4822, loads protocol
plugins, makes the real connections.
Performs no authentication.

**guacenc** — The tool that renders
a graphical session recording into
an MPEG-4 video file.

**guaclog** — The tool that renders
a terminal typescript recording into
readable text.

**Guacamole protocol** — The text
instruction stream between guacd,
the web application and the client:
`ready`, `img`, `sync`, `key`, and
their kin.

**GUACAMOLE_HOME** — The web
application's configuration
directory: `guacamole.properties`,
`user-mapping.xml`, `extensions/`.

**Instruction** — One message of the
Guacamole protocol: length-prefixed
elements, comma-separated, ended by
a semicolon.

**NLA (Network Level Authentication)**
— RDP's modern mode, authenticating
before a session is created. Prefer
it.

**Parameter token** — A placeholder
in a connection parameter
(`${GUAC_USERNAME}` and friends),
filled from the logged-in user's
details at connect time. Needs
database or directory auth.

**Plugin (protocol plugin)** — One
shared library per protocol that
guacd loads per session:
`libguac-client-ssh`, `-vnc`,
`-rdp`, `-telnet`.

**Servlet container** — The program
that runs Java web applications.
For Guacamole 1.6.0: Tomcat 9
(javax generation, not jakarta).

**Typescript** — A timed text
recording of a terminal (SSH or
telnet) session, in two files: text
and timing.

**User mapping** — The file method:
`user-mapping.xml`, users and their
connections in one XML file. For
verifying an installation, not for
production.

**WAR** — Web application archive:
the packaged web application
(`guacamole-1.6.0.war`), deployed
into the servlet container.

**WebSocket tunnel** — The browser's
connection to the web application's
tunnel endpoint, carrying the
Guacamole protocol for one session.
