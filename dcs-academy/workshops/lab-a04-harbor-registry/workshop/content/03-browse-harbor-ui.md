---
title: Browse the Harbor UI
---

The command line is one view of Harbor; the **web UI** is the other, and it's where you'll
usually browse projects, tags, and scan results. This page tours it — and explains why you
can pull but not push.

## The same content, two views

First, the CLI view — list the tags in the sample repository:

```terminal:execute
command: skopeo list-tags docker://$DCS_REGISTRY/samples/hello-dcs
```

You'll see the tags available for that repository (e.g. `1.0`).

```examiner:execute-test
name: verify-tags
title: List tags for the sample repository
args:
- $DCS_REGISTRY/samples/hello-dcs
timeout: 30
retries: 3
delay: 3
```

Now the same content in the Harbor UI. Open the **Harbor** tab:

```dashboard:open-dashboard
name: Harbor
```

In the UI, open the `samples` **project**, then the `hello-dcs` **repository**. You'll see
the same tags and digests you just listed, plus each artifact's **vulnerability scan
result** — a severity summary Harbor computes for every image. Browsing here is how you'd
check "is this image clean?" before using it.

Return to the terminal when you're done:

```dashboard:open-dashboard
name: Terminal
```

{{< note >}}
If the embedded Harbor tab isn't available in your environment, the same information is on
the command line (`skopeo list-tags`, `skopeo inspect`) and via the Harbor API — the UI is a
convenience, not the only way.
{{< /note >}}

## Why pull-only?

Your session can **pull** but not **push**. Pushing to Harbor requires a **dedicated
project** with a **push-capable robot account**, and on {{< param product_short >}} projects
and their permissions are managed **the GitOps way** — declared in git and provisioned by
the platform, not created ad hoc per session. That's more than a lab should stand up, so
pushing is covered here as a concept:

1. A team is granted a Harbor project (via an ITSM request).
2. A push robot account is issued for it (GitOps-managed).
3. CI (not a person) pushes built images to that project.

So in Foundations you consume images; producing and pushing them is a Developer/CI concern.
