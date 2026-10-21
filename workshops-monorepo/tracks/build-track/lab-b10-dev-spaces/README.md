# Dev Spaces

**Optional lab: develop inside the cluster with OpenShift Dev Spaces.**

The rest of the track used git as a **build source**: code in, image out. **OpenShift Dev
Spaces** uses it as an **in-cluster IDE**: a workspace defined by a **devfile** in the
repository, running on the cluster, with the same registry and the same security posture as
anything else you deploy.

You read a devfile field by field: the image the workspace develops in, the endpoints it
exposes and the commands it can run. Then you place Dev Spaces next to the three other ways
this track has worked with code.

> **📌 This is mostly a reading lab.** Dev Spaces is operator-provided and this training
> cluster does not run it. What you learn about the devfile applies on a real instance, and the
> lab says which steps need one.

- **Track:** Build & Run (optional)
- **Audience:** Intermediate
- **Duration:** ~18 min
- **Format:** Guided reading with a hands-on devfile inspection, in your own OpenShift session namespace
- **Prerequisites:** **Build Your Image on DCS**, which is the contrast this lab is built on.

## By the end of this lab you will be able to

- Explain what Dev Spaces is, and how an IDE on the cluster differs from one on your laptop.
- Read a devfile: components, endpoints, commands.
- Say what a workspace costs: it runs as Pods in your namespace and counts against your quota.
- Choose between the Educates editor, your laptop, a BuildConfig and Dev Spaces.

## What you will do

1. **Learn** the model: the IDE runs as a workload in your namespace.
2. **Read** a devfile, field by field, and verify it is a valid one.
3. **Walk** the launch of a workspace and what it provisions.
4. **Compare** the four ways this track has used a repository.
