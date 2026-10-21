---
title: Change and Run It
---

The devfile, the workspace and the cloned source let you **edit code and run it inside the
cluster in one step**. On an air-gapped platform, a laptop cannot do this.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/inside
```

{{< note >}}
**📌 There are two different terminals.** Every other page in this course
used the **Educates terminal** (the one in this dashboard). From here on, "the
terminal" means the **workspace terminal**, a separate shell running *inside*
the Dev Spaces workspace Pod, with its own working directory (the cloned
`hello-dcs` repo). Commands typed there never touch this session's terminal, and
vice versa.
{{< /note >}}

## The loop

Inside the workspace, three things happen in sequence:

![Edit, run, and reach the change, all inside the workspace](edit-run-reach.svg)

1. **Edit.** Open `server.py` in the workspace's own editor and change the
   `GREETING` default, the same string **Deploy Your First App** taught you to change with
   `oc set env`, except here you are editing the *source*, not an environment
   variable on a running Deployment.
2. **Run.** Trigger the `run-hello-dcs` command from page 02's devfile (one
   click), or `python3 server.py` typed directly into the workspace terminal. It
   starts on port 8080, **inside the workspace container**, using the exact
   `commandLine` the devfile declared.
3. **Reach it.** Dev Spaces exposes the devfile's `endpoints` entry (`targetPort:
   8080`) as a workspace preview URL. Open it to see your edited greeting, served
   by a process running inside your namespace.

## Three ways to get a code change running

- **`oc apply`** (**Deploy Your First App**) deploys an image somebody already built. You
  never touch source.
- **A BuildConfig** (**Build Your Image on DCS**) turns your source into a *new image* on
  every change. That is the production-shaped path, with a build cycle between editing a line
  and seeing it run.
- **A Dev Spaces workspace**, this lab, runs your source directly with no image build in
  between. It is the fastest inner loop, and it is meant for active development rather than
  for what ships.

A workspace is where you iterate, a BuildConfig turns the result into a deployable image,
and `oc apply` puts that image into a namespace. The next page compares them side by side.

## Check your understanding

Why does editing `GREETING` in the workspace show up immediately when you run the
app, with no image build step, unlike **Build Your Image on DCS**?

{{< note >}}
**❓ Answer:** The workspace runs the source directly (`python3 server.py`)
from the cloned project on disk, so there is no image to build. **Build Your Image on DCS**'s BuildConfig
exists because a *deployed* Pod runs from a built image, not live
source. Dev Spaces skips the build, so you get faster feedback while you write code.
{{< /note >}}
