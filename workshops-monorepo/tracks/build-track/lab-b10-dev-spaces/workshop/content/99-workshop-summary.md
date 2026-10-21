---
title: Summary
---

You have looked at what it means to develop **on** **{{< param product_name >}}** rather
than only deploy to it: a devfile, an in-cluster browser IDE, and the loop from an edited
line of code to that line running inside the cluster.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/next
```

## What You Did

- **Explained** what OpenShift Dev Spaces is: an in-cluster, browser-based IDE
  (upstream Eclipse Che), installed and operated by the platform team, that
  removes laptop tool drift and the need for outbound cluster/Harbor access.
- **Read** a `devfile.yaml` and identified its three jobs: `components` (the
  Harbor-mirrored dev image), `projects` (the cloned source), and `commands`
  (the `run` action), and saw `${DCS_REGISTRY}` resolve the same way it does in
  every other lab.
- **Walked through** launching a workspace from that devfile: submit → provision
  → clone → running IDE, the same Pod-level reconciliation every other lab's
  Deployment has already shown you, triggered by the Che Operator instead of by
  `oc apply`.
- **Traced** the edit → run → reach loop a workspace gives you, and why it skips
  the image-build step that **Build Your Image on DCS**'s BuildConfig deliberately has.
- **Placed** Dev Spaces, the Educates editor, BuildConfig (**Build Your Image on DCS**), and `oc apply`
  (**Deploy Your First App**) on one timeline (write, build, deploy), with one job for each
  tool.

## Check Your Understanding

1. What is the main difference between the Educates editor you have used all
   course and OpenShift Dev Spaces?

{{< note >}}
**❓ Answer:** The Educates editor exists for *this training session only*. It
has no connection to your source control and disappears when the session
ends. Dev Spaces is a platform-provided development environment your
organisation uses day to day, running as a Pod in your namespace.
{{< /note >}}

2. Where does a Dev Spaces workspace's dev-container image come from, and how is
   that expressed in the devfile?

{{< note >}}
**❓ Answer:** Harbor, like every other DCS image. The devfile's `components[].container.image`
is `${DCS_REGISTRY}/devspaces/udi:latest`, never a hardcoded or public registry.
{{< /note >}}

3. Why does a code change in a workspace run without a new image build, unlike
   **Build Your Image on DCS**'s BuildConfig?

{{< note >}}
**❓ Answer:** A workspace runs the cloned source directly (`python3 server.py`)
from disk, so no image is involved. BuildConfig exists for the opposite
case: turning *finished* source into a deployable image once you are done
iterating.
{{< /note >}}

4. A teammate asks whether Dev Spaces replaces `oc apply`. What do you tell
   them?

{{< note >}}
**❓ Answer:** No, they solve different problems. Dev Spaces is where you *write
and iterate on* code; `oc apply` (**Deploy Your First App**) is how a *built* image ends up
running in a real namespace. A workspace never deploys anything by itself.
{{< /note >}}

5. Who installs and upgrades Dev Spaces on your DCS cluster: you, or the
   platform team?

{{< note >}}
**❓ Answer:** The platform team, via an Operator. You consume Dev Spaces (launch
workspaces, develop in them); you never manage its installation or lifecycle.
This is the same ownership split as every other DCS-provided platform service.
{{< /note >}}

## Next Steps

**Build Your Image on DCS** uses the same source as a **build source**
rather than as an IDE, so your finished code becomes an image in the registry. **Harbor:
Projects, Push & Scan** picks up where that image lands: the project it goes to, how it is
scanned, and what the CVE gate means for what may run in PROD.

With the Build & Run track finished, **Operate & Observe** is what to do with the result:
metrics, logs, RBAC and tenancy, DEV against PROD, and the operators behind the platform's
own services.

{{< note >}}
**📌 Provisioning:** this lab's devfile clones from
`${WORKSPACE_SOURCE_REPO}`, an in-platform git repository reachable without external egress.
Where that repository lives on a given cluster (a mirror into the tenant's GitLab or a small
in-cluster git service) is a platform decision rather than a lab one. Whether the **Dev
Spaces** tab shows a live instance likewise depends on whether your cluster has Dev Spaces and
a Harbor-mirrored UDI provisioned. The steps describe a cluster that has Dev Spaces.
{{< /note >}}
