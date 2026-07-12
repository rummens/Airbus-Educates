---
title: A Secret
---

A Secret looks like a ConfigMap but is for **sensitive** values. It's guarded by RBAC, kept out
of most logs, and meant to be handled carefully.

{{< note >}}
**Base64 is not encryption.** Kubernetes stores Secret values base64-**encoded**, which anyone
with read access can decode. A Secret's protection comes from **RBAC** (who may read it) and
from **not committing it to git** — never from the encoding. `stringData` in `secret.yaml` is
plain text for this workshop only.
{{< /note >}}

## Create it

```editor:open-file
file: ~/exercises/secret.yaml
```

```terminal:execute
command: oc apply -f ~/exercises/secret.yaml
```

The Deployment you applied already injects one Secret key as an env var via `secretKeyRef`
(look for `API_TOKEN` in `deployment-configured.yaml`). Confirm the Secret exists and is wired
in:

```examiner:execute-test
name: verify-secret-referenced
title: Secret exists and is injected by the Deployment
args:
- hello-dcs-secret
timeout: 5
```

## Prove it's set — without printing it

You can confirm the credential is present **without echoing its value**. List env var names
only:

```terminal:execute
command: oc exec deployment/hello-dcs -- sh -c 'printenv | cut -d= -f1 | grep API_TOKEN'
```

Expected: `API_TOKEN` — the name, not the value. That's the habit to build: verify a secret is
delivered without ever splashing it across the terminal or logs.

{{< note >}}
Deeper secrets practice (rotation, external secret stores, avoiding secrets in images/logs) is
covered in the **Security & Compliance** module. Here the point is simple and important:
credentials come from a **Secret**, injected at runtime — never baked into the image.
{{< /note >}}
