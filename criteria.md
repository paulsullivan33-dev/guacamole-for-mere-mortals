# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's machines, accounts and passwords are invented
   fixtures on loopback addresses.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** The Limits chapter names what the
   tool cannot do: no agent-side management, targets must
   already speak a protocol, motion and audio are weak, the
   browser is both ceiling and floor, and the file-based login
   is a rung rather than a home.
8. **The security rule is in the text, early.** Guacamole is a
   door into other machines, so its line is drawn in chapter 1
   and the README before any procedure depends on it, and
   chapter 11 is devoted to it: guacd performs no
   authentication and must be isolated, the file-based login
   is not for production (the manual's own words), and the
   gateway goes behind HTTPS and a real second factor before
   it faces an untrusted network.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, ~8 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran (timings are
therefore ranges, and the guide says so). Guacamole **1.6.0**
was used throughout: the web application from the official
`guacamole-1.6.0.war` (15,641,879 bytes) and guacd from the
official `guacamole-server-1.6.0.tar.gz`, both downloaded
from downloads.apache.org and both verified against the
project's published SHA-256 files (`sha256sum -c` → OK for
each, transcript t00). All transcripts live in
`guacamole-lab/transcripts/`; the lab's session client is
`guacamole-lab/guac_session.py`; its configuration files are
kept redacted alongside. Everything the lab ran was bound to
loopback; all services were stopped and the lab tree deleted
when the work finished (t12).

Run for real, with transcripts as evidence:

- The WAR's deployment failure on Tomcat 10.1.55 (Ubuntu
  packages, extracted .deb tree), verbatim
  `ClassNotFoundException: javax.servlet.ServletContextListener`,
  and the cause proven from the WAR's own classes (javax, not
  jakarta). Ubuntu 24.04 has no Tomcat 9 package (checked), so
  Tomcat **9.0.99** came from Apache's official archive,
  SHA-512 verified (t01, t02).
- The login page served (HTTP 200), login through the real
  REST API: wrong password → 403 `INVALID_CREDENTIALS`;
  fixture credentials → an auth token (printed redacted);
  the connections endpoint listing both connections defined
  in the lab's user-mapping.xml (t03–t05).
- guacamole-server **compiled from source**: configure found
  every offered library and enabled **all four protocols**
  (RDP, SSH, telnet, VNC) plus guacenc and guaclog. Libraries
  were the distribution's .deb files downloaded and extracted
  to a local tree, never installed system-wide; 27 dangling
  symlinks in that tree had to be repointed at host copies,
  and configure needed
  `--enable-allow-freerdp-snapshots` for Ubuntu's FreeRDP
  2.11.5 — both disclosed in chapter 3 (t06).
- A complete **SSH session** through web application → guacd
  → a fixture sshd (its own instance on a loopback high
  port): websocket tunnel upgraded (HTTP 101), 21 sync
  frames counted at the client, a typed command sent as
  `key` instructions, guacd's log line "SSH connection
  successful.", the target sshd's own "Accepted password"
  line, and — in a repeat run — a decoded PNG instruction
  tile (240×19, 720 distinct colours) proving rendered
  terminal text (t07).
- A complete **VNC session** the same way, to a fixture
  desktop (Xvfb + x11vnc): guacd reported "Screen is now
  initialized", x11vnc logged the connection, and the
  client received img/blob/copy frames (t09).
- **Session recording**: a raw-protocol SSH session with
  recording parameters produced a 12,133-byte recording;
  guacenc refused it as in-progress (the disconnect was
  abrupt), then with `-f` encoded it to an MPEG-4 video
  measured by ffprobe at 1024×768, 10.04 s (t11).
- The webapp-to-guacd **timeout diagnosis** (t08): native
  clients reached guacd instantly while the JVM's
  dual-stack sockets were routed by the sandbox into its
  network fabric and black-holed (proven with a minimal
  Java test program, before and after
  `-Djava.net.preferIPv4Stack=true`). A first Tomcat
  restart that silently did not happen (old JVM still
  serving; BindException in the new instance's log) is
  recorded in chapter 14 as part of the same entry.

Documented only — described from the project's manual
(guacamole.apache.org/doc/gug, 1.6.0), read for this guide,
not run, and the text does not claim otherwise:

- The Docker installation route (three containers,
  environment-variable configuration, manual database
  initialisation), including the manual's verbatim warning
  about exposing guacd, quoted in chapter 11.
- Database authentication (MySQL/MariaDB, PostgreSQL, SQL
  Server), the shipped schema scripts, the default
  `guacadmin` account and its required password change;
  LDAP/Active Directory; TOTP; RADIUS, CAS, OpenID Connect
  and SAML; HTTP header authentication.
- Users, user groups, connection groups (organisational and
  balancing), per-object permissions, session sharing,
  active-session administration and connection history.
- RDP and telnet **sessions** (both protocol plugins were
  compiled, installed and listed — t10 — but the lab had
  no RDP or telnet target to connect to), including RDP
  drive redirection, printing, gateways and NLA choices.
- SFTP file transfer within SSH sessions (the plugin and
  parameters were present and are quoted from the live
  handshake; no transfer was performed), the RDP shared
  drive, VNC audio, and the browser client's on-screen
  keyboard, touch modes and session menu as interactions
  (the lab's client was a protocol-level program, not a
  browser; drawing instructions it received are quoted as
  measurements, and no claim is made about how a session
  *feels*).
- Kubernetes protocol support: configure reported it
  unavailable (no libwebsockets) and the guide does not
  teach it.

Fixtures are this guide's own and deliberately generic: one
web user (`labreader`), one SSH account (`labguest`) on a
throwaway sshd, one VNC desktop showing a clock, all on
loopback, all deleted when the lab closed. Passwords and
the session token appear in transcripts only in redacted
form.
