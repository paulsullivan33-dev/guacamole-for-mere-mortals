# Installing Guacamole

By the end of this chapter you have
chosen an installation route and can
say what each route puts on the
machine. The lab's evidence covers the
native route in full — every step of
it ran — while the Docker route is
described from the project's manual,
and the chapter marks which is which.

## The two supported routes

The manual offers exactly two:

1. **Docker containers.** Three
   containers: `guacamole/guacd`,
   `guacamole/guacamole` (the web
   application, on Tomcat 9, configured
   by environment variables), and a
   database container (MySQL or
   PostgreSQL) holding users and
   connections. This is the route most
   readers should take: the images are
   built by the project, the awkward
   dependency work is done inside
   them, and upgrades are image swaps.
   **Documented only in this guide** —
   the lab machine has no container
   runtime — and described here from
   the manual's Docker chapter, read
   in full.
2. **Native installation.** A servlet
   container running the WAR, plus
   guacd compiled from source against
   your system's libraries. More moving
   parts, and the route this guide's
   lab took — because only the native
   route lets a guide *prove* each
   piece separately, and because it is
   still the route on machines where
   containers are not welcome.

Whichever route you choose, the shape
is the same (chapter 2): browser →
web application → guacd → targets.

## Before anything: checksums

The lab downloaded two artefacts from
`downloads.apache.org` — the web
application (`guacamole-1.6.0.war`,
about 15 MB) and the guacd source
(`guacamole-server-1.6.0.tar.gz`) —
each with its published `.sha256`
file, and verified both before use:

```
guacamole-1.6.0.war: OK
guacamole-server-1.6.0.tar.gz: OK
```

(transcript `t00-downloads.txt`).
Make this a habit for anything that
will one day hold the keys to all your
machines: check the checksum, and
prefer the project's own download
pages over mirrors.

## The web application: Tomcat 9, not 10

Deploying the WAR is the easy half —
and it contains this chapter's sharpest
lesson. The lab first tried **Tomcat
10** (the only Tomcat in Ubuntu
24.04's packages) and the web
application failed to start:

```
java.lang.ClassNotFoundException:
  javax.servlet.ServletContextListener
```

The cause, verified by inspecting the
WAR's own classes: Guacamole 1.6.0 is
built against the older **javax**
servlet API, while Tomcat 10 speaks
only **jakarta**. (The project's own
Docker image, the manual confirms,
runs Tomcat 9.x for the same reason.)
So: use **Tomcat 9** for Guacamole
1.6.0. Ubuntu no longer packages it,
so the lab used Apache's official
Tomcat 9.0.99 archive, checksum-verified
(`t02-tomcat9.txt`), with its connector
moved from the default 8080 to the
lab's assigned port. On a machine with
Tomcat 9 packaged (Debian, for
example), the distribution package is
the better choice.

With the WAR placed in Tomcat's
`webapps/` folder as `guacamole.war`
and Tomcat started, the login page
should answer:

```
GET /guacamole/ -> HTTP 200
```

(transcript `t03-login-page.txt`).
The page itself is a small HTML shell
— the client is a JavaScript program,
so the title and forms appear only
when a browser runs it. Chapter 4
proves the login itself through the
API, which needs no browser.

## guacd: building the native half

guacd is C, built the classic way —
`./configure`, `make`, `make install` —
and its one real demand is **libraries**:
each protocol plugin exists only if
its development libraries were present
at configure time. The lab's configure
run (transcript `t06-configure.txt`)
found everything it was offered and
reported the full set:

```
Protocol support:
   RDP ........... yes
   SSH ........... yes
   Telnet ........ yes
   VNC ........... yes
```

Three honest footnotes from that
build, each of which is a real-world
lesson in miniature:

- **FreeRDP needed a flag.** Configure
  at first refused Ubuntu's FreeRDP
  2.11.5, calling it a "development
  version" (its check for one function
  fails against that release) and
  demanding `--enable-allow-freerdp-snapshots`.
  Knowing the library was in fact a
  normal distribution release, the lab
  used the flag — and the RDP plugin
  then compiled and linked cleanly.
  Read configure's summary before
  believing its warnings, and after.
- **Extracted packages need care.**
  The lab did not install libraries
  system-wide; it downloaded the
  distribution's `.deb` files and
  extracted them into a local tree.
  Twenty-seven library symlinks in
  that tree dangled (their targets
  already lived on the host) and had
  to be repointed before the linker
  would use them. Installing the
  `-dev` packages properly, as a
  reader on their own machine should,
  skips this entirely.
- **The summary is the contract.**
  Whatever configure lists as "no" is
  what your guacd cannot do. The lab's
  only "no" that mattered was
  Kubernetes support (it needs
  libwebsockets), which this guide
  therefore does not teach.

The build also produced `guacenc` and
`guaclog` (transcript `t10-tools.txt`).
Started with its bind address pinned
to loopback, guacd announced itself:

```
Guacamole proxy daemon (guacd) version 1.6.0 started
Listening on host 127.0.0.1, port 4822
```

## The Docker route, in outline

From the manual's Docker chapter
(documented-only here):

```bash
docker run --network=some-network \
  --name some-guacd -d guacamole/guacd

docker run --network=some-network \
  --name some-guacamole \
  -e GUACD_HOSTNAME=some-guacd \
  ... database settings ... \
  -d -p 8080:8080 guacamole/guacamole
```

Three things the manual insists on,
worth knowing before you start: the
database must be **initialised by
hand** with the SQL scripts the
project ships (the web application
will not create its own tables);
configuration arrives as **environment
variables** (each `guacamole.properties`
entry upper-cased, dashes turned to
underscores — `GUACD_HOSTNAME`,
`GUACD_PORT`); and guacd in its
container listens on 4822 inside the
Docker network, **not** published to
the host — which is exactly the
isolation chapter 11 asks for.

## Check your installation

You have this chapter if: the WAR
answers on its port with HTTP 200;
`guacd -v` reports its version; and
you can name which route you took and
which protocols your configure
summary promised. Chapter 4 puts a
user and two connections into the
running system.
