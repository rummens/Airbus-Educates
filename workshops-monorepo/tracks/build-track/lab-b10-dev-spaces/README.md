# Dev Spaces

**Optional — the fourth thing you can do with a git repository on this platform.**

The rest of the track used git as a **build source**: code in, image out. **OpenShift Dev
Spaces** uses it as an **in-cluster IDE** — a workspace defined by a **devfile** in the
repository, running on the cluster, under the same registry and the same security posture as
anything else you deploy.

You read a real devfile field by field — the image the workspace develops in, the endpoints it
exposes, the commands it can run — then place Dev Spaces next to the three other ways this
track has worked with code.

> **📌 Mostly a reading lab here.** Dev Spaces is operator-provided and this training cluster
> does not run it. The devfile and the model are what transfer, and the lab is explicit about
> which steps need a real instance.

- **Track:** Build & Run — optional
- **Audience:** Intermediate
- **Duration:** ~18 min
- **Format:** Guided reading with a hands-on devfile inspection, in your own OpenShift session namespace
- **Prerequisites:** **Build Your Image on DCS** — it is the contrast this lab is built on.

## By the end of this lab you'll be able to

- Explain what Dev Spaces is, and why an IDE on the cluster is a different proposition from one on your laptop.
- Read a devfile: components, endpoints, commands.
- Say what a workspace costs — it is Pods in your namespace, against your quota.
- Choose between the Educates editor, your laptop, a BuildConfig and Dev Spaces.

## What you'll do

1. **Meet** the model: an IDE that is a workload like any other.
2. **Read** a devfile, field by field, and verify it is a valid one.
3. **Walk** the launch of a workspace and what it provisions.
4. **Compare** the four ways this track has used a repository.
