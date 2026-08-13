---
title: Summary
---

You took your own git source and turned it into a running image on
**{{< param product_name >}}** — no laptop Docker, no manual push — then rebuilt it and
watched a fresh image take over.

## What You Did

- **Explained** why DCS builds images on-cluster instead of on a laptop, and read the
  BuildConfig → Build Pod → image → Harbor flow.
- **Connected** a git repository as a build source in a BuildConfig, and compared the
  **S2I** and **Dockerfile** strategies.
- **Built** an image with `oc start-build` and watched it push into Harbor.
- **Deployed** the image you built, using the same Deployment skills from A01/B01.
- **Rebuilt** it and confirmed a fresh image — with a new digest — replaced the old one.

## Check Your Understanding

1. What's the difference between the **S2I** and **Dockerfile** build strategies?

{{< note >}}
**Answer:** S2I uses a pre-built builder image that knows how to "assemble" your source
into a runnable image — no Dockerfile needed. The Dockerfile strategy builds from a
Dockerfile you maintain yourself. Same source and output; only the *how* differs.
{{< /note >}}

2. What does a BuildConfig's `output.to` actually point at, and what does the ImageStream do?

{{< note >}}
**Answer:** `output.to` names an **ImageStreamTag** — a tag on an **ImageStream**, which is
OpenShift's tracking object for the versions of one image over time. On DCS, the
ImageStream is backed by your session-scoped Harbor project, so the pushed image lands in
Harbor via your session's robot account.
{{< /note >}}

3. Why did the second build produce a different image even though the source repo didn't change?

{{< note >}}
**Answer:** Every build run produces fresh layers with a new timestamp, so the resulting
image gets a new digest regardless of whether the source text changed. A rebuild always
yields a genuinely new image — which is exactly what an automated pipeline relies on.
{{< /note >}}

4. In a real project, what would normally trigger a build instead of you running
   `oc start-build` by hand?

{{< note >}}
**Answer:** A **Webhook** trigger — configured against your git host, it calls a
generated webhook URL after each push, starting a build automatically. **ImageChange**
and **ConfigChange** triggers cover the other two cases: a builder/base image update, and
bootstrapping the first build when the BuildConfig is created.
{{< /note >}}

## Next Steps

You connected git as a **build source** — code in, image out. **B03 — Dev Spaces**
connects git for a different purpose: an **in-cluster IDE**, so you can edit and run code
directly against the cluster without a build at all. Same git repository model, opposite
job.

Where does the image you built here actually live, and is it safe to run? **B04 — Harbor
& Image Scanning** picks up exactly there: inspecting the image you pushed today and the
vulnerability scan gate it passes through before anything deploys it in PROD.

<!--
DESIGN NOTE (not learner-visible): this workshop is authored assuming two pieces of
session-provisioned infrastructure that are UNCONFIRMED as of this writing — see
dcs-academy/planning/tasks.md, "Module B — Developer restructure":

1. A session-scoped, PUSH-CAPABLE Harbor project + robot account (tasks.md P1: "B02 has
   no clean fallback for build-and-push" — unlike B04's read-only robot, this lab cannot
   degrade to inspect-only if the push credential isn't actually provisioned per session).
   This workshop assumes the BuildConfig's output push lands at
   {{< param dcs_registry >}}/{{ session_namespace }}/hello-dcs-built:latest-built via a
   robot account already wired to the session — content and manifests reference this via
   ${DCS_REGISTRY} and the session namespace, never a hardcoded credential, so no rework
   is needed if the real plumbing differs, but the underlying capability itself is not
   confirmed to exist yet.

2. An air-gapped-reachable git build source for ${BUILD_SOURCE_REPO} (tasks.md P2:
   "Unresolved" — mirrored GitLab vs. an in-cluster seeded git repo). This workshop
   treats the repo as a read-only mirror already reachable in-session with no write
   access, and does not ask the learner to push a change to it (see 05-rebuild-on-change.md,
   which simulates a source change by re-triggering the build rather than editing the
   remote repo) — this sidesteps needing git write access, but the repo's mere
  *reachability* in an air-gapped session is still the open dependency.

Do not treat either as validated infrastructure until confirmed against a real session.
-->
