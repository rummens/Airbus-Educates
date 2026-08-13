---
title: Summary
---

You gave your app real configuration, changed it live, and — when it broke — diagnosed and
fixed it from the cluster's own signals.

## What You Did

- Externalised config into a **ConfigMap**, consumed as **env vars** and a **mounted file**.
- Stored a credential in a **Secret** and confirmed injection **without printing the value**.
- Rolled the app onto a changed value with `oc rollout restart`.
- Diagnosed a broken app (`describe`, `events`, `logs`), fixed the one bad line, and verified recovery.

## Common failure signatures

| Status | Usually means |
|---|---|
| `ImagePullBackOff` / `ErrImagePull` | Image name/tag wrong or not in the registry |
| `CreateContainerConfigError` | A referenced ConfigMap/Secret (or key) is missing |
| `CrashLoopBackOff` | Container starts then exits — read `oc logs --previous` |
| `Pending` | Can't be scheduled — quota, resources, or node constraints |

## Check Your Understanding

1. What's the difference between a **ConfigMap** and a **Secret**?

{{< note >}}
**Answer:** Both hold key/value config outside the image. A Secret is for sensitive
values — access-restricted by RBAC and kept out of manifests/logs — while a ConfigMap is
for non-secret settings.
{{< /note >}}

2. Why is base64 in a Secret **not** encryption?

{{< note >}}
**Answer:** Base64 is a reversible encoding — anyone can decode it. Secrets are protected
by RBAC and handling discipline, not by base64.
{{< /note >}}

3. What triggers a **rollout**?

{{< note >}}
**Answer:** A change to the Deployment's Pod template (image, env, `oc rollout restart`,
etc.). Editing a ConfigMap alone does **not** — you must roll the Pods to pick it up.
{{< /note >}}

4. A Pod won't start. **Where do you look first?**

{{< note >}}
**Answer:** `oc describe pod <p>` (its Events), then `oc get events`. They usually name
the missing/blocked resource directly.
{{< /note >}}

5. What does `oc logs --previous` give you?

{{< note >}}
**Answer:** The logs of the **previous, crashed** container instance — essential for
`CrashLoopBackOff`, where the current container may not be running to log from.
{{< /note >}}

## Next Steps

Your app still only answers a **local** tunnel — no stable in-cluster address, no external
URL. **A03 — Expose Your App** gives it a Service and a real DCS Route, reachable from
outside your session.
