---
title: Summary
---

You have worked the registry as an object rather than as a string in a manifest.

Open the closing slide (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

1. **Named** the catalogs, and what a tenant's own Harbor project is for.
2. **Requested** a Harbor project as a Kubernetes object, through Crossplane's Harbor
   provider, and read the fields that carry the DEV and PROD rules.
3. **Inspected** an image without pulling it: digest, layers, labels and runtime config.
4. **Copied** an image between registries with `skopeo`, and saw that a promotion is that
   operation plus a process.
5. **Read** two scan reports and decided which image the PROD gate would refuse.
6. **Listed** the Critical findings with their packages and fixed versions.

## Check Your Understanding

1. Why does {{< param product_short >}} refuse a floating tag like `latest`?

{{< note >}}
**❓ Answer:** because a tag **moves**. A scan verdict belongs to a **digest**, so if the tag
can point somewhere else tomorrow, the thing that was scanned and the thing that runs are not
provably the same bytes.
{{< /note >}}

2. Your build pushed an image with two Critical findings into your DEV project. What happens
   next?

{{< note >}}
**❓ Answer:** DEV takes it, with no CVE limitation. It cannot be promoted, because a PROD
project pulls only below the threshold. The fix is to rebuild on a newer base, checking
`fixable` first, or to take the exception route if there is genuinely no fix.
{{< /note >}}

3. Name the two ways an image can end up in a PROD project.

{{< note >}}
**❓ Answer:** it comes from the **green catalog** of already-cleared images, or it is
**mirrored** from the DEV project as a promotion — requested through ITSM, because PROD accepts
no pushes at all.
{{< /note >}}

4. Why use a robot account rather than your own credentials in a pipeline?

{{< note >}}
**❓ Answer:** it belongs to the system, not to you: it survives your password changing or your
leaving, it is scoped to one project, and it can be revoked on its own without breaking
anything else you do.
{{< /note >}}

## Next Steps

That is the artefact's whole journey — built, stored, scanned, promoted. The rest of the
**Build & Run** track is about the workload it becomes: sizing it, scaling it, exposing it,
giving it state, and keeping it alive through the platform's maintenance.
