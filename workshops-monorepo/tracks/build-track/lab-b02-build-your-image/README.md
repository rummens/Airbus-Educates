# Build Your Image on DCS

**There is no Docker daemon on this platform, and you do not need one.**

A **BuildConfig** builds your image inside the cluster. It takes your files and a
`Containerfile`, runs the build in a Pod, and pushes the result to a registry. No privileged
tooling runs on your laptop.

You create one, feed it the files from your session, follow the build log, then deploy the
image you made, referenced by an **ImageStream tag** rather than a registry URL.

Then a change and a second build, where you find that a new image does **not** restart
anything, and meet the triggers that connect "a build finished" to "the new version is live".

> **💡 Tip:** a build is a workload like any other. It queues, it has logs, it can fail, and it
> draws on your namespace budget.

- **Track:** Build & Run
- **Audience:** Intermediate
- **Duration:** ~25 min
- **Format:** Hands-on and guided, with a split terminal and editor in your own OpenShift session namespace
- **Prerequisites:** **From Docker to Kubernetes** (why the Docker workflow does not transfer) and the Core lab **Deploy Your First App**.

## By the end of this lab you'll be able to

- Explain what a BuildConfig, a Build and an ImageStream each are.
- Build an image on the cluster from your own files.
- Read a build log, and tell a build failure from a deploy failure.
- Deploy an image by its ImageStream tag.
- Say what triggers a rebuild, and where the image goes on DCS.

## What you'll do

1. **Create** a BuildConfig and its ImageStream from a manifest.
2. **Build** from the files in your session, and watch the log.
3. **Deploy** what you built, and prove the values came from the image.
4. **Change** the source and build again.
5. **Roll out** the new image, and meet the triggers that automate it.
