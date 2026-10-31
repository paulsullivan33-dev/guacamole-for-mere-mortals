# Real Authentication

By the end of this chapter you know
what replaces the starter file, how
the pieces fit, and which option
matches which kind of deployment.
This chapter is **documented from the
manual** — the lab proved the file
method end to end and did not run a
database or a directory — and it says
so wherever a procedure appears, so
nothing here borrows the lab's
authority.

## Why the file has to go

The manual's own words about
`user-mapping.xml`: it is "not
intended for production use", exists
to verify an installation, and "we do
not recommend using user-mapping.xml
for production or anything
public-facing." The reasons are
concrete: passwords hashed with MD5,
no web interface for managing users,
no connection groups or sharing or
history, and every change is a file
edit and a restart. Fine for a lab.
Not a door to leave on a house.

## The model: extensions

Guacamole's web application loads
**authentication extensions** — JAR
files placed in
`GUACAMOLE_HOME/extensions/` — and
each extension can vouch for users
and supply their connections. Several
can run at once, layered: a database
for local accounts, LDAP for the
company directory, each appearing as
a **data source** (the login token in
chapter 4 named its source:
`"default"`, the file). The rest of
this chapter is the catalogue.

## Database authentication — the standard route

The manual calls database storage "a
typical, standard installation", and
it is what most deployments use. The
project ships extensions for **MySQL
(and MariaDB), PostgreSQL and SQL
Server**. What the database buys:

- **Users and connections managed in
  the web interface** — an
  administrator logs in and creates
  accounts, connections, groups,
  without touching a file.
- **Passwords hashed properly**
  (salted SHA-512 in the schema the
  project ships), not MD5.
- **History** — every connection
  attempt and session is recorded,
  which chapter 8 uses.
- **Parameter tokens** (chapter 6)
  and per-user attributes.

The setup shape (manual, database
chapter): create an empty database;
load the schema with the project's
own SQL scripts (`schema/*.sql` in
the extension's release archive) —
the application **will not create its
own tables**, and forgetting this
step is the classic first failure;
drop the extension JAR into
`extensions/`; add the connection
settings (`mysql-hostname`,
`mysql-database`, `mysql-username`,
`mysql-password`, or the `postgresql-*`
equivalents) to `guacamole.properties`;
restart. On first start the database
contains one administrator,
`guacadmin` with password `guacadmin`
— the manual and this guide agree on
the first instruction: **log in and
change it immediately**, before the
gateway faces anyone else.

In the Docker route this is the third
container of chapter 3, and the same
manual warning applies: you
initialise the database by hand, with
the shipped scripts.

## LDAP — when a directory already exists

The LDAP extension authenticates
against an existing directory —
notably **Active Directory** — so
people log in with the accounts they
already have. Its honest shape: it
adds configuration for the directory
server, a search/bind account, and
the attributes that find users. Two
patterns matter:

- **LDAP for logins, database for
  connections.** The most common real
  deployment: the directory says who
  you are; the database holds what
  you may reach.
- **LDAP for both.** Connection
  definitions can live in the
  directory itself, keyed per user.

## Second factors and single sign-on

Also extensions, all documented in
the manual's extension chapters and
none of them run in the lab:

- **TOTP** — time-based one-time
  codes (the authenticator-app kind),
  layered over another method.
- **RADIUS**, **CAS**, **OpenID
  Connect** and **SAML** — the
  single-sign-on family, for estates
  that already have an identity
  provider.
- **HTTP header** authentication —
  trusting a reverse proxy that has
  already authenticated the user
  (chapter 11 shows where that fits;
  it is exactly as dangerous as it
  sounds if the gateway can also be
  reached directly).

## Choosing

- A home or tiny team: the **database**
  extension, one strong admin password,
  done. Do not stay on the file.
- An organisation with accounts
  already: **LDAP plus database**, and
  **TOTP** if the gateway is reachable
  from the internet.
- An organisation with an identity
  provider: **SSO** in front, database
  behind.

## Check your understanding

You have this chapter if you can say
why the file must go (MD5, no
management, the manual's own warning),
what an extension and a data source
are, and which single step —
initialising the schema by hand —
every database deployment depends on.
