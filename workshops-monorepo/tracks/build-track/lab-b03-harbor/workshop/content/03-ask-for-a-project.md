---
title: Ask for a Project
---

A Harbor project is not something you click into existence. On {{< param product_short >}} you
declare it as a Kubernetes object and the platform builds it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/project
```

## Who creates the project

{{< param product_short >}} runs **Crossplane** with a **Harbor provider**. Crossplane turns an
external system into Kubernetes objects: you apply a manifest, a controller calls the Harbor API
until Harbor matches it, and it keeps checking.

That means your Harbor project is requested the same way as everything else you have created in
this course. Same `oc apply`, same object, same reconciliation loop.

Open the manifest:

```editor:open-file
file: ~/exercises/harbor-project.yaml
```

## What the fields do

Four of them carry the rules from the previous page:

- **`name`** is the project in Harbor, and the first path element of every image in it:
  `harbor.dcs/<name>/<repository>:<tag>`.
- **`public: false`** keeps it private. A public project is readable without credentials.
- **`vulnerabilityScanning: true`** scans every image on push. Without it the CVE rules have
  nothing to work from.
- **`deploymentSecurity`** is the severity at which Harbor refuses to serve an image. Empty is
  the DEV setting: serve anything. A PROD project sets `critical`, which is the CVE < 9 rule
  written as one field, because 9.0 and above is what Critical means.

`storageQuota` caps how much the project may hold. This one asks for 1 GiB, which is plenty for
a lab.

{{< note >}}
**📌 `providerConfigRef` is not yours.** It names the credentials the provider uses to talk to
Harbor, and the platform owns that object. You reference it; you cannot read it.
{{< /note >}}

## Ask for it

```terminal:execute
command: bash ~/exercises/request-project.sh
```

```examiner:execute-test
name: verify-project-requested
title: Verify your Harbor project request is valid
timeout: 200
retries: .INF
delay: 5
```

{{< warning >}}
**⚠️ There is no Harbor behind this training cluster.** The Academy runs without one, so the
Harbor provider is not installed and there is no project to create. The script notices, and
reads your manifest back to you instead of failing.

On {{< param product_short >}} the same command creates the project, and the next page pushes
into it. Here the cluster's own registry stands in for the destination.
{{< /warning >}}

## When you no longer need it

Delete the object and the provider deletes the project, with the images in it. That is the part
people find uncomfortable about declarative infrastructure, and it is also the point: the
manifest is the truth, and Harbor follows it.

A scratch project like this one is for experiments. Your namespace's real project is created
with the namespace, and you will find it already there.
