---
title: What Changes on DCS
---

You built into the cluster's own registry, because that is what this training cluster has.
On **{{< param product_name >}}** three things differ, and all three follow from air-gapping.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/on-dcs
```

## 1. The base image comes from Harbor

`FROM` must name something the platform already has. There is no reaching out to a public
registry mid-build, so an image whose base is not mirrored does not build at all.

That makes it an inventory question: **what is your base, and is it in the registry?** The
**Harbor** lab answers it properly.

## 2. The output goes to your tenant's project

A tenant may have a **Harbor project of its own**, scoped per namespace today. The rules are
asymmetric on purpose:

- **A DEV project takes pushes**, of anything. That is where a build's output lands.
- **A PROD project takes no pushes at all**, and pulls only images below the CVE threshold.

So a build publishes into DEV. Getting that image into PROD is a **promotion**, meaning a
mirror between projects requested through ITSM, or you take an already-cleared image from the
**green catalog**.

## 3. The builder itself is platform-provided

There is no daemon on your laptop and none on the cluster. The build runs in a Pod with a
builder image the platform supplies and keeps patched. You choose what goes *in* your image;
the platform owns what *does* the building.

{{< note >}}
**📌 Note:** this is the same ownership split as the Operators lab. The platform owns the
machinery, you own what it produces.
{{< /note >}}

## What does not change

Everything you just did. The BuildConfig, the Build, the log, the ImageStream tag and the
rebuild are the same objects and the same commands. Only the endpoints differ, and those are
values in a manifest.
