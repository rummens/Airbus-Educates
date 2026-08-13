---
title: Summary
---

You looked at what it means to develop **on** **{{< param product_name >}}**, not
just deploy to it — a devfile, an in-cluster browser IDE, and the fastest possible
loop from an edited line of code to that line running inside the cluster.

## What You Did

- **Explained** what OpenShift Dev Spaces is — an in-cluster, browser-based IDE
  (upstream Eclipse Che), installed and operated by the platform team, that
  removes laptop tool drift and the need for outbound cluster/Harbor access.
- **Read** a `devfile.yaml` and identified its three jobs: `components` (the
  Harbor-mirrored dev image), `projects` (the cloned source), and `commands`
  (the `run` action) — and saw `${DCS_REGISTRY}` resolve the same way it does in
  every other lab.
- **Walked through** launching a workspace from that devfile: submit → provision
  → clone → running IDE — the same Pod-level reconciliation every other lab's
  Deployment has already shown you, triggered by the Che Operator instead of by
  `oc apply`.
- **Traced** the edit → run → reach loop a workspace gives you, and why it skips
  the image-build step that B02's BuildConfig deliberately has.
- **Placed** Dev Spaces, the Educates editor, BuildConfig (B02), and `oc apply`
  (A01/B01) on one timeline: write it, build it, run it — four tools, one job
  each, never substitutes for one another.

## Check Your Understanding

1. What's the core difference between the Educates editor you've used all
   course and OpenShift Dev Spaces?

{{< note >}}
**Answer:** The Educates editor is scaffolding for *this training session only* —
it has no connection to real source control and disappears when the session
ends. Dev Spaces is a real, platform-provided development environment your
organisation runs day to day, backed by an actual Pod in your namespace.
{{< /note >}}

2. Where does a Dev Spaces workspace's dev-container image come from, and how is
   that expressed in the devfile?

{{< note >}}
**Answer:** Harbor, like every other DCS image — the devfile's `components[].container.image`
is `${DCS_REGISTRY}/devspaces/udi:latest`, never a hardcoded or public registry.
{{< /note >}}

3. Why doesn't editing code in a workspace require a new image build to see the
   change run, the way B02's BuildConfig does?

{{< note >}}
**Answer:** A workspace runs the cloned source directly (`python3 server.py`)
from disk — there's no image in the loop. BuildConfig exists for the opposite
case: turning *finished* source into a deployable image once you're done
iterating.
{{< /note >}}

4. A teammate asks whether Dev Spaces replaces `oc apply`. What's the honest
   answer?

{{< note >}}
**Answer:** No — they solve different problems. Dev Spaces is where you *write
and iterate on* code; `oc apply` (A01/B01) is how a *built* image ends up
running in a real namespace. A workspace never deploys anything by itself.
{{< /note >}}

5. Who installs and upgrades Dev Spaces on your DCS cluster — you, or the
   platform team?

{{< note >}}
**Answer:** The platform team, via an Operator. You consume Dev Spaces (launch
workspaces, develop in them); you never manage its installation or lifecycle —
the same ownership split as every other DCS-provided platform service.
{{< /note >}}

## Next Steps

**Building Images with BuildConfigs** (`lab-b02-image-buildconfigs`) is this
lab's twin — it connects the same git repository as a **build source** instead
of an IDE, so your finished code becomes a Harbor image. From here, **Harbor
& Image Scanning** (`lab-b04-harbor-scanning`) picks up where your built image
lands: how it's scanned, and what a vulnerability gate means for what you can
deploy. Further out, Module F's **GitLab** lab extends this exact workflow —
cloning straight from your tenant's own GitLab into a Dev Spaces workspace,
instead of the provided sample repo used here.

{{< note >}}
**A provisioning note, for the record.** This workshop's devfile clones from
`${WORKSPACE_SOURCE_REPO}` — a small, in-platform git repository reachable
without external egress. The concrete air-gapped hosting for that repo (a
mirror into the tenant's GitLab vs. a small in-cluster git service) is the same
open provisioning question tracked for B02's `${BUILD_SOURCE_REPO}`; both
resolve to the same answer once that's settled. Likewise, whether the **Dev
Spaces** dashboard tab shows a live instance depends on whether your cluster has
Dev Spaces and a Harbor-mirrored UDI provisioned yet — the content here is
written for the real thing either way.
{{< /note >}}
