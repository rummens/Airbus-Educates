---
title: What Changes on DCS
---

You built into the cluster's own registry, because that is what this training cluster has. On
**{{< param product_name >}}** three things differ — and each one follows from air-gapping.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/on-dcs
```

## 1. The base image comes from Harbor

`FROM` must name something the platform already has. There is no reaching out to a public
registry mid-build, so an image whose base is not mirrored does not build at all.

That is not an obstacle so much as an inventory question: **what is your base, and is it in the
registry?** The **Harbor** lab is where that gets answered properly.

## 2. The output goes to your tenant's project

A tenant may have a **Harbor project of its own**, scoped per namespace today. The rules are
asymmetric on purpose:

- **A DEV project takes pushes**, of anything. That is where a build's output lands.
- **A PROD project takes no pushes at all**, and pulls only images below the CVE threshold.

So a build publishes into DEV, and getting that image into PROD is a **promotion** — a mirror
between projects, requested through ITSM — or you take a cleared image from the **green
catalog** instead.

## 3. The builder itself is platform-provided

No daemon on your laptop, and none on the cluster either: the build runs in a Pod, with a
builder image the platform supplies and keeps patched. You choose what goes *in* your image;
the platform owns what *does* the building.

{{< note >}}
**📌 Note:** this is the same ownership split as the Operators track — the platform owns the
machinery, you own the thing it produces.
{{< /note >}}

## What does not change

Everything you just did. The BuildConfig, the Build, the log, the ImageStream tag, the rebuild:
identical objects and identical commands. Only the endpoints differ, and they are values in a
manifest rather than a different way of working.

That is the whole reason this lab is worth doing on a training cluster: the muscle memory
transfers exactly.
