---
title: How Secrets Leak
---

Before you fix anything, it's worth being precise about *how* a credential actually escapes.
Leaks are rarely dramatic — almost always the token was simply written somewhere convenient,
and "somewhere convenient" turned out to be somewhere readable.

## The three leak paths

Nearly every plaintext-credential incident is one of these three:

- **Baked into the image.** A `Dockerfile` `ENV` or `ARG`, or a config file copied into the
  layers, carries the token. Now the secret ships with the image: anyone who can pull the
  image — or run `skopeo inspect` on it — can read it, and it's the same for every deployment
  of that image, forever, until the image is rebuilt.
- **Printed to logs.** The app logs its own config at startup ("connecting with token
  abc123…"), or an error dumps the environment. Logs are aggregated, searchable, and retained
  — a token in stdout is a token in the logging backend, visible to anyone with log access.
- **Inline in a manifest / env dump.** The credential is a literal `env` value in a Deployment.
  Anyone who can `oc get deploy` or run `oc set env deploy/... --list` sees it in clear text —
  and if that manifest is committed, it's now in git history too, which is effectively forever.

This lab focuses on the third path — the inline literal — because it's the one a tenant
controls directly and the one a Secret cleanly solves. The first two follow from the same
discipline: never write the value where it will be copied.

## The fix, in one sentence

Store the credential in a dedicated **Secret** object, and have the workload reference it —
so the value lives in exactly one place and never appears in the manifest, the image, or
(if the app behaves) the logs.

## base64 is NOT encryption

Here is the misconception that trips up almost everyone the first time. When you look at a
Secret, its values are **base64-encoded**, and base64 *looks* scrambled:

```
YXBpLXRva2Vu
```

It is not encrypted. base64 is a reversible **encoding** — `base64 -d` turns it straight back
into the original text, no key required. You'll do exactly that later in this lab and watch the
token reappear. So encoding is not what protects a Secret. Two things do:

- **RBAC.** Reading a Secret requires the `get`/`list` verb on `secrets` in that namespace.
  That is a **privileged** verb, granted narrowly — least privilege. A plaintext env value has
  no such gate: `get deploy` is enough. Moving the value into a Secret puts it behind a
  separate, tighter permission.
- **Encryption at rest.** The platform encrypts Secret data in **etcd** (the cluster
  datastore), so a copy of the disk or a backup doesn't hand over every credential. This is
  configured platform-side — you inherit it; you don't set it up.

{{< note >}}
The **Secret** object, `secretKeyRef`, and RBAC verbs are standard Kubernetes — see
[Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) and
[encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/).
*How* {{< param product_short >}} configures etcd encryption and scopes secret-read RBAC is
platform policy under [governance]({{< param dcs_docs_base_url >}}/governance/overview).
{{< /note >}}

Keep that distinction in mind for the rest of the lab: **the encoding hides nothing; the
access control and the at-rest encryption do the protecting.** Now let's make a leak visible.
