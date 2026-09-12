# Harbor: Projects, Push & Scan

**On DCS the registry decides what may run. An image it will not serve cannot start.**

You inspect an image without pulling it, request a **Harbor project** as a Kubernetes object
through Crossplane's Harbor provider, and copy an image between registries with `skopeo`.

Then you read two real vulnerability reports and work out which image the PROD gate refuses,
and what to do about it.

Three rules shape the rest: the **catalogs** images may come from, the Harbor project your
namespace may be given, and the asymmetry between namespace types. **A DEV project takes any
push. A PROD project takes none, and serves only images below CVE severity 9.**

The last page covers the two ways an image reaches PROD: a mirror from DEV, or the green
catalog of images already cleared.

> **⚠️ Watch out:** no `docker`, no `podman`. `skopeo` talks to registries directly, which is
> why it is the tool you get on a platform that will not give you a daemon.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~35 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** **Build Your Image on DCS** and **From Docker to Kubernetes**.

## By the end of this lab you'll be able to

- Inspect an image without pulling it, and say why its digest matters more than its tag.
- Request a Harbor project as a Kubernetes object, and read the fields that carry the DEV and PROD rules.
- Copy an image between registries with `skopeo`.
- Name the DCS catalogs and what each is for.
- State the DEV/PROD project rules, including the CVE threshold.
- Read a scan report and decide whether an image passes the gate.
- Describe the two routes into a PROD project.

## What you'll do

1. **Pull** from the registry, and name the rules behind it.
2. **Inspect** an image's metadata and runtime config without downloading it.
3. **Request** a Harbor project through Crossplane, and read what it asks for.
4. **Copy** an image into your own namespace's registry.
5. **Read** a clean report and a failing one.
6. **List** the Critical findings and decide what to do about each.
