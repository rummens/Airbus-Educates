# Cloud Development with OpenShift Dev Spaces

**Develop *on* DCS, not just deploy to it — a browser-based IDE running inside the cluster.**

Every prior lab either deployed a ready-made image or turned your code into one with
a BuildConfig — neither lets you edit and run source *while it's inside the
cluster*. This lab introduces [OpenShift Dev Spaces](https://developers.redhat.com/products/openshift-dev-spaces/overview):
you read the devfile that defines a workspace, walk through launching one from a
Harbor-mirrored dev image, and trace the fastest inner loop this course has —
edit, run, and reach a code change with no image build in between. It closes with
an explicit line between the Educates editor, Dev Spaces, a BuildConfig, and
`oc apply` — four tools, one job each.

- **Track:** Developer — Build on DCS · Lab 3
- **Audience:** Intermediate — done "From Docker to Kubernetes on DCS"
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** lab-b01-docker-to-k8s; comfortable with `oc apply`-style deployment and basic git

## By the end of this lab you'll be able to

- Explain what OpenShift Dev Spaces is and why an in-cluster, browser-based IDE fits an air-gapped, regulated platform.
- Read a `devfile.yaml` and identify its dev image, its source, and its run command.
- Walk through launching a workspace and making a code change run **inside the cluster**.
- Place Dev Spaces correctly among the Educates editor, a BuildConfig (code → image), and `oc apply` (deploy).

## What you'll do

Read a devfile for the `hello-dcs` sample, walk through what happens when it's
handed to Dev Spaces to launch a workspace, trace the edit-run-reach loop a
workspace gives you, and finish by drawing a clear line between four tools that
all touch "your code" but never substitute for one another.
