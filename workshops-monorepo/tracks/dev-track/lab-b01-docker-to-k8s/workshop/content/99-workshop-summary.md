---
title: Summary
---

You took a docker-compose file for `hello-dcs` and migrated it, line by line, onto
**{{< param product_name >}}** — and worked out exactly which lines couldn't come along.

## What You Did

- **Mapped** the Docker/compose model onto Kubernetes objects: container → Pod/Deployment,
  `ports:` → Service, `environment:` → ConfigMap, `volumes:` → Volume.
- **Translated** the compose `hello-dcs` service into a Deployment, filled in its Harbor
  image, and applied it with `envsubst | oc apply -f -`.
- **Translated** `ports: "8080:8080"` into a Service and reached it by stable cluster DNS.
- **Translated** `environment: GREETING` into a ConfigMap, wired it in with
  `oc set env --from=configmap/...`, and watched the rollout serve the migrated value.
- **Identified** the four compose lines that don't translate at all — an external
  `:latest` image, `user: root`, `privileged: true`, and a host bind mount — and which DCS
  control rejects each one.

## Check Your Understanding

1. What's the difference between how `docker run` and Kubernetes decide what should be
   running?

{{< note >}}
**Answer:** `docker run` is **imperative** — you tell the daemon what to do, once. A
Deployment is **declarative** — you state the desired end state, and the platform
continuously reconciles reality to match it (that's why a killed Pod comes back without
you running anything).
{{< /note >}}

2. Why does `ports: "8080:8080"` become a Service instead of another Deployment field?

{{< note >}}
**Answer:** `ports:` publishes onto the *Docker host's* port — there's no single host to
publish onto in a cluster. A Service gives a stable, cluster-wide name that load-balances
to whichever Pods currently match its selector, regardless of which node they land on.
{{< /note >}}

3. Name the four things in the compose file that DCS rejects, and the control behind each.

{{< note >}}
**Answer:** an image from `docker.io` (air-gapped, Harbor-only) tagged `:latest` (floating
tags banned); `user: root` and `privileged: true` (both blocked by the restricted Security
Context Constraint); and a host bind mount of `/var/run/docker.sock` (no host-path access —
storage is always a namespace-scoped Volume).
{{< /note >}}

4. If `hello-dcs`'s image already runs as UID 1001, why did the compose file's `user: root`
   line matter at all?

{{< note >}}
**Answer:** it didn't change anything about the image — it's a property the image itself
already fixes. The point is that a *naive* lift-and-shift might assume root is available
(many Docker images do), and that assumption is exactly what the restricted SCC catches.
{{< /note >}}

## Next Steps

You migrated an image someone else already built. **B02** picks up where this leaves off:
building *your own* code into an image on-cluster with a BuildConfig, so the next thing you
migrate is something you wrote yourself.
