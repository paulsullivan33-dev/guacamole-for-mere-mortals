# Troubleshooting

Every entry here happened — most of
them to this guide's own lab, whose
failures were kept as carefully as
its successes. Entries are in the
order you will meet the layers: page,
login, tunnel, guacd, target.

## The login page is a 404, or Tomcat starts and Guacamole does not

Read the container log before anything
else. The lab's first deployment
(Tomcat 10) failed with:

```
SEVERE ... Context [/guacamole]
  startup failed due to previous errors
Caused by:
java.lang.ClassNotFoundException:
  javax.servlet.ServletContextListener
```

Cause: Guacamole 1.6.0 needs a
**javax**-generation servlet
container — **Tomcat 9**, not 10.
The WAR did not change; the container
did. (Check any "listener failed to
start" error the same way: the
missing class names the mismatch.)

## Login fails with the right password

- Wrong file, right contents:
  `user-mapping.xml` is read from
  the **GUACAMOLE_HOME of the running
  web application**. If the API
  answers but your connections never
  appear (chapter 4's check), that
  is the cause until proven
  otherwise.
- The password hash must be the MD5
  of exactly the password,
  `echo -n` — a trailing newline
  hashes a different password.
- A wrong password on purpose should
  give `403 INVALID_CREDENTIALS`
  through the API. If it gives a
  token, you are not testing the
  account you think you are.

## "Creation of WebSocket tunnel to guacd failed"

The web application's log names the
reason; the lab met three:

- `Parameter "GUAC_ID" is required`
  (and `GUAC_TYPE`, `GUAC_DATA_SOURCE`
  after it) — a hand-rolled client
  missing its destination parameters.
  Real browsers send them; scripted
  clients must too (chapter 5).
- `Requested tunnel destination does
  not exist` — the ID does not match
  any connection or group the user
  may see. Check spelling and data
  source before checking guacd.
- `Connection to guacd timed out` —
  the deep one. Work it in layers:
  1. Is guacd listening (`ss -tln`,
     port 4822)?
  2. Can a **local, native** client
     speak to it? Send the raw
     instruction `6.select,3.ssh;`
     to 4822 (a three-line socket
     program suffices) — guacd should
     answer with its `args` list
     instantly. If it does, guacd and
     its plugins are innocent.
  3. Can the **web application's own
     runtime** reach it? In the lab
     the answer was no, for a reason
     specific to its sandbox: the
     JVM's default dual-stack sockets
     were routed by the sandbox into
     its network fabric, where
     loopback services do not exist —
     while plain IPv4 sockets reached
     guacd instantly. The tell was a
     test program whose local address
     was a fabric address instead of
     127.0.0.1. The fix, in Tomcat's
     `setenv.sh`:
     `CATALINA_OPTS="-Djava.net.preferIPv4Stack=true"`.
     On an ordinary machine this entry
     should never fire — keep it as a
     diagnostic pattern: *prove each
     leg separately before blaming
     the next one.*
  4. And the lab's own confession: its
     first "restart" after applying
     that fix did not restart — the
     old JVM never stopped (its start
     had needed a kill, which the log
     showed as a `BindException` from
     the new instance), so the flag
     was verified in a file and absent
     from the running process. Check
     the **running** process's
     arguments (`ps`), not the file
     you edited.

## guacd says: Handshake failed, "connect" instruction was not received

guacd got a `select`, sent its
`args`, and the other side went quiet.
Seen when a client connects to guacd
and stops mid-handshake (the lab's
own raw probe did this deliberately
once). Through the web application
it means the tunnel died between
args and connect — read the web
application's log for the same
minute.

## A protocol is missing from the connection form

It was missing at **configure time**
(chapter 3). Run configure again and
read its summary like a contract;
install the missing development
library; rebuild. The Docker images
do not have this failure — all
plugins are built in.

## configure refuses FreeRDP as a "development version"

The lab's message, verbatim in
spirit: FreeRDP's API check failed
against a perfectly ordinary 2.11.5
distribution release, and configure
demanded
`--enable-allow-freerdp-snapshots`.
If your FreeRDP came from your
distribution as a release, the flag
is the way through — the plugin then
built and linked cleanly. If it came
from a nightly build, believe the
warning instead.

## The SSH session connects but warns about host identity

`No known host keys provided, host
identity will not be verified` is
guacd telling you the connection has
no `host-key` parameter. Set it
(chapter 6) on anything real; the
warning is the sound of trust-on-
first-use, which for a gateway means
trusting whoever answers first.

## guacenc refuses: "Refusing to encode in-progress recording"

The recording lacks its finish
marker — the session ended uncleanly
or is genuinely still running. If
you are sure it is finished, `-f`
overrides (chapter 9). Do not make
`-f` a habit on a live gateway; a
recording that is still being
written will encode truncated.

## Sessions are slow or the picture lags

Count what is actually moving:
full-screen motion is the known weak
suit (chapter 12). For RDP, the
performance switches (wallpaper,
theming, font smoothing off) are the
first lever; for VNC, colour depth
and a smaller target screen. If a
*terminal* session lags, suspect the
network leg between browser and
gateway, not guacd — the lab's SSH
session needed only twenty-one small
frames in sixteen seconds.

## Where to look, summarised

| Symptom | First log |
|---|---|
| Page missing / app won't start | Tomcat's `catalina.out` and the per-app `localhost` log |
| Login rejected | Web application log; then the mapping file |
| Tunnel creation failed | Web application log (it names the reason) |
| Handshake stalls | guacd log at debug level |
| Target refuses | The target's own service log |

Run guacd with `-L debug` while
diagnosing — its parameter-by-parameter
account of a session (chapter 5) is
the most informative log in the
system — and turn it back down when
done.
