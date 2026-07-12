---
title: Summary
---

Your app is now configured the way real apps are on **{{< param product_name >}}** — settings
and credentials live outside the image and change without a rebuild.

## What You Did

- Moved settings into a **ConfigMap** and delivered them as env vars **and** a mounted file.
- Injected a credential from a **Secret** — and proved it was set **without printing its value**.
- Learned that base64 is **not** encryption; Secrets are protected by RBAC and by never being committed.
- **Rolled out** a config change on the same image and verified the new value in the container.

## Challenge

Now do it yourself, unguided. Change `FEATURE_FLAG` in the ConfigMap to `stable`, roll it out,
and confirm the container sees it. When you think it's done, run the check.

```examiner:execute-test
name: verify-config-delivered
title: Challenge — the ConfigMap is delivered to the container
timeout: 8
retries: 4
delay: 3
```

{{< note >}}
**Hint:** edit `configmap.yaml`, `oc apply` it, then `oc rollout restart deploy/hello-dcs`.
Env vars from a ConfigMap are read at container start, so a rollout is needed to pick them up.
{{< /note >}}

## Check Your Understanding

1. When do you use a **ConfigMap** vs a **Secret**?

{{< note >}}
**Answer:** ConfigMap for non-sensitive settings; Secret for sensitive values (tokens,
passwords, keys). Secrets are RBAC-guarded and kept out of logs and images.
{{< /note >}}

2. Is a Kubernetes Secret encrypted?

{{< note >}}
**Answer:** No — the value is base64-**encoded**, which is trivially decodable. Protection comes
from RBAC (who can read it) and from never committing it to git.
{{< /note >}}

3. You changed a ConfigMap but the running Pods still show the old value. Why, and how do you fix it?

{{< note >}}
**Answer:** Env vars from a ConfigMap are set at container start, so existing Pods keep the old
value. Trigger a rollout (`oc rollout restart`) to start new Pods that read the new value.
{{< /note >}}

4. Why is baking config and secrets into the image a bad idea on an air-gapped platform?

{{< note >}}
**Answer:** The image is mirrored and cached everywhere — a baked-in secret leaks everywhere,
and you'd need a rebuild per environment. Externalising config lets one mirrored image run
anywhere with the right ConfigMap/Secret.
{{< /note >}}

## Next Steps

Next in the Developer track: **Scaling, Health & Resources** — you'll scale the app, meet your
namespace quota, right-size it, and add health probes.
