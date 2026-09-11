---
title: Summary
---

You took a `docker-compose.yml` for `hello-dcs` and migrated it onto
**{{< param product_name >}}** — then worked out which lines could not come along.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Mapped** the compose model onto Kubernetes objects — container → Pod/Deployment,
   `ports:` → Service, `environment:` → ConfigMap, `volumes:` → Volume.
2. **Translated** the compose service into a **Deployment**, filled in its registry image,
   and applied it with `envsubst | oc apply -f -`.
3. **Translated** `ports: "8080:8080"` into a **Service**, and reached it by cluster DNS.
4. **Translated** `environment: GREETING` into a **ConfigMap**, wired it in with
   `oc set env --from`, and watched the rollout serve the migrated value.
5. **Identified** the four lines {{< param product_short >}} rejects, and the control behind
   each.
6. **Met the SCC properly**: asked for root, read the refusal, found which constraints are
   yours to use, and saw the uid and group your container actually runs as.

## Check Your Understanding

1. What is the difference between how `docker run` and a Deployment decide what should be
   running?

{{< note >}}
**❓ Answer:** `docker run` is **imperative** — you tell the daemon what to do, once. A
Deployment is **declarative** — you state the desired end state and the platform keeps
reconciling reality to match it. That is why a killed Pod comes back without you running
anything.
{{< /note >}}

2. Why does `ports: "8080:8080"` become a Service instead of another Deployment field?

{{< note >}}
**❓ Answer:** `ports:` publishes onto the *Docker host's* port, and a cluster has no single
host to publish onto. A Service gives a stable cluster-wide name that load-balances to
whichever Pods currently match its selector, on whichever node they land.
{{< /note >}}

3. Name the four things in the compose file {{< param product_short >}} rejects, and the
   control behind each.

{{< note >}}
**❓ Answer:** an image from `docker.io` (air-gapped, Harbor only) tagged `:latest` (floating
tags are not reproducible or scannable); `user: root` and `privileged: true` (both blocked by
the **restricted SCC**); and the host bind mount of `/var/run/docker.sock` (no host paths —
storage is always a namespace-scoped Volume).
{{< /note >}}

4. A colleague's image is refused here with "not usable by user or serviceaccount". What does
   that message tell you to do?

{{< note >}}
**❓ Answer:** **not** to go looking for the permission. That wording means an SCC which would
have allowed the request exists but is not yours — the permissive ones belong to the platform.
The fix is in the image or the manifest. ("Invalid value" is the other case: an SCC you *may*
use, refusing one specific ask.)
{{< /note >}}

5. If the `hello-dcs` image already runs as UID 1001, why did `user: root` matter at all?

{{< note >}}
**❓ Answer:** it changed nothing about this image — the image already fixes it. The point is
that a naive lift-and-shift *assumes* root is available, as many Docker images do, and that
assumption is exactly what the restricted SCC catches.
{{< /note >}}

## Next Steps

You migrated an image somebody else built.

**Build Your Image on DCS** picks up there: pointing a **BuildConfig** at a git repository so
the platform builds *your* code into an image and pushes it to the registry — no Docker
daemon anywhere in sight.
