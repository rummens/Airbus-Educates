# Building Images with BuildConfigs

**Get *your* code into an image without a local Docker.**

Every lab so far started from an image someone else already built. This one builds
one yourself, on the cluster. You point a **BuildConfig** at a git repository, DCS
schedules a **Build Pod** that turns your source into an image — using either the
**S2I** (Source-to-Image, no Dockerfile needed) or **Dockerfile** strategy — pushes the
result into Harbor, and you deploy it with the same skills you already have. Then you
trigger a second build and see a fresh image land, the same way an automated pipeline
would after a real commit.

- **Track:** Developer — Build on DCS · Lab 2
- **Audience:** Intermediate — comfortable with Deployments and `oc apply`
- **Duration:** ~30 min
- **Format:** Hands-on, guided — split terminal, runs in your own OpenShift session namespace
- **Prerequisites:** lab-b01-docker-to-k8s; lab-a01-deploy-first-app — comfortable with `oc apply` and reading a Deployment manifest

## By the end of this lab you'll be able to

- Explain how DCS builds images **on the cluster** — BuildConfig + Build Pod — instead of on a laptop.
- Connect a git repository as a **build source** and choose between the S2I and Dockerfile strategies.
- Build an image on-cluster and watch it land in Harbor.
- Deploy the image you just built, using the same Deployment skills from earlier labs.
- Trigger a rebuild and confirm a fresh image replaces the old one.

## What you'll do

Apply a BuildConfig that points at a provided git repository, run the build and follow
its log as it pushes to Harbor, deploy the resulting image, then start a second build to
see the rebuild-and-redeploy cycle a CI pipeline would automate for you.
