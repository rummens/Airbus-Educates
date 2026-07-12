---
title: Fix & Verify
---

You have a hypothesis: the Deployment references **`hello-dcs:2.0`**, a tag that was never
mirrored into the **{{< param product_name >}}** Harbor registry, so the kubelet can't pull
it — `ImagePullBackOff`. The mirrored, working tag is **`:1.0`** (the one every other lab
uses). The fix is a single edit.

## Make the fix

Open the manifest:

```editor:open-file
file: ~/exercises/broken-deployment.yaml
```

Change the image tag from `2.0` to `1.0`:

```editor:replace-matching-text
file: ~/exercises/broken-deployment.yaml
match: "hello-dcs:2.0"
replace: "hello-dcs:1.0"
```

Apply the corrected Deployment:

```terminal:execute
command: oc apply -f ~/exercises/broken-deployment.yaml
```

Watch the rollout complete:

```terminal:execute
command: oc rollout status deployment/hello-dcs
```

Expected: `deployment "hello-dcs" successfully rolled out`. The old, un-pullable Pod is
replaced by one running the mirrored `:1.0` image, which pulls cleanly from Harbor.

## Verify recovery

Confirm the loop is closed — a **Ready** Pod **and** the Service serving traffic again:

```examiner:execute-test
name: verify-recovered
title: App has recovered — pod Ready and serving 200
args:
- hello-dcs
- hello-dcs
- "8080"
timeout: 10
retries: 6
delay: 3
```

{{< note >}}
That's the whole loop, closed: you **observed** the bad state, **read the signals**
(`describe`/events pointed at a pull failure), formed **one hypothesis** (wrong tag), made
the **smallest change** that tests it, and **verified**. No wipe-and-redeploy on a hunch.
{{< /note >}}

## Why this failure is a {{< param product_short >}} classic

On an air-gapped platform, "the image won't pull" almost always means **the tag isn't in
Harbor** — not that Docker Hub is down (you can't reach it anyway). When you promote a new
version, mirroring the tag into Harbor is part of the job. An `ImagePullBackOff` on
{{< param product_short >}} is your reminder to check the mirror.
