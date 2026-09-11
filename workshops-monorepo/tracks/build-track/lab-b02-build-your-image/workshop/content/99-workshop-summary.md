---
title: Summary
---

You built a container image with no Docker anywhere, ran it, changed it, and built it again.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Created** a BuildConfig and its ImageStream with one `oc new-build`.
2. **Ran** a build from the files in your session, and watched the log: upload, steps, push.
3. **Deployed** the result by its **ImageStream tag**, and proved the values were baked in.
4. **Changed** the source, built again, and found the running app **unchanged**.
5. **Rolled out** the new image deliberately, and met the triggers that do it automatically.

## Check Your Understanding

1. What is the difference between a BuildConfig and a Build?

{{< note >}}
**❓ Answer:** the **BuildConfig** is the recipe — input, strategy, output — and you create it
once. A **Build** is one run of it, with its own Pod, log and status, kept afterwards as the
record. Every rebuild is a new Build.
{{< /note >}}

2. Your build finished successfully and the app still behaves the old way. What happened?

{{< note >}}
**❓ Answer:** nothing told the Deployment. A new image does not restart anything — the Pod
keeps the image it started with until a rollout replaces it, by hand or through an image
trigger.
{{< /note >}}

3. Why does `FROM` have to name an image from the platform's registry?

{{< note >}}
**❓ Answer:** the platform is **air-gapped**. A build runs inside the cluster, so it can only
pull what the cluster can reach. A base image that has not been mirrored makes the build fail
at its first instruction.
{{< /note >}}

4. Your build pushed to your DEV Harbor project. How does that image reach PROD?

{{< note >}}
**❓ Answer:** not by pushing — a PROD project accepts none. Either it is **mirrored** from the
DEV project as a promotion, requested through ITSM, or you use an already-cleared image from
the **green catalog**. And PROD pulls only images below the CVE threshold.
{{< /note >}}

## Next Steps

You have an image and a registry to put it in. **Harbor: Projects, Push & Scan** is where the
registry stops being a URL: catalogs, the project your namespace gets, what a scan reports, and
the gate that decides what PROD will run.
