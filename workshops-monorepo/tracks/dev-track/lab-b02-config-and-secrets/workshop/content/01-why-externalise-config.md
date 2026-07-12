---
title: Why Externalise Config
---

Baking configuration into an image ties one build to one environment. The
[twelve-factor](https://12factor.net/config) principle — and the way you work on
{{< param product_name >}} — is the opposite: **build once, configure per environment**.

## Why it matters here

- **One image, many environments.** The same `hello-dcs:1.0` image runs in your DEV namespace
  and, later, in PROD — only the config differs. No rebuild to change a setting.
- **Air-gapped promotion.** On {{< param product_short >}} you promote by **mirroring an image
  once** and shipping *config* alongside it — not by rebuilding a new image per environment.
- **Secrets never belong in images.** An image is copied everywhere and cached in Harbor; a
  credential baked into it is a credential leaked everywhere.

## Two objects for two jobs

- [**ConfigMap**](https://docs.openshift.com/container-platform/latest/nodes/pods/nodes-pods-configmaps.html)
  — non-secret settings (greetings, flags, URLs, whole config files).
- [**Secret**](https://docs.openshift.com/container-platform/latest/nodes/pods/nodes-pods-secrets.html)
  — sensitive values (tokens, passwords, keys), handled with more care.

Both are delivered into the container the same two ways: as **environment variables** or as
**mounted files**. That's the whole toolkit — the next pages wire each one in.

{{< note >}}
The `hello-dcs` app is a tiny static server — it doesn't itself read these values. That's fine:
this workshop is about **delivering** config into a container correctly. You'll verify delivery
at the container boundary with `oc exec` (read the env var, read the mounted file), which is
exactly how you'd confirm a real app is receiving its config.
{{< /note >}}
