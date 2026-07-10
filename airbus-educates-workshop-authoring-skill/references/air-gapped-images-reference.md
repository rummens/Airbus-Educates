# Air-Gapped Images Reference

**House rule: every container image referenced anywhere in a workshop must be pulled from the DCS registry (Harbor). No external registries.** Workshop sessions run fully air-gapped — `docker.io`, `quay.io`, `ghcr.io`, `registry.k8s.io`, and any public registry are unreachable. An image reference that points outside Harbor will fail to pull and break the workshop.

This applies to **all** image references: the workshop container image, sample application images deployed by learners, images pulled by the virtual cluster, sidecars, init containers, and anything in `session.objects` / `environment.objects` / `request.objects`.

## Where image references appear — and how to write them

| Reference site | How to write it |
|---|---|
| Published workshop files image | `$(image_repository)/<name>-files:$(workshop_version)` (already the skill default) |
| Workshop container image | A DCS base image in Harbor — see below |
| Sample app image in exercise YAML / `session.objects` | `{{< param dcs_registry >}}/<project>/<image>:<tag>` (content) or `$(dcs_registry)`-derived value in the definition |
| vcluster component images | Mirrored in Harbor; configure the vcluster to pull from `$(image_repository)` / Harbor |

`$(image_repository)` is the cluster-provided registry Educates itself uses and is always correct for workshop-files images. For **application and tool images the author chooses**, use the `dcs_registry` param so the Harbor location is declared once and re-pointable without rebuild. See [workshop-variables-reference.md](workshop-variables-reference.md).

Never write a bare image like `nginx:latest` or `python:3.12` in any manifest or command — resolve it to its Harbor-mirrored path via `{{< param dcs_registry >}}`.

## The DCS registry model (catalogs & mirroring)

Images do not arrive in Harbor by magic — DCS has a defined model, and workshops should reflect it (see [dcs-concepts-reference.md](dcs-concepts-reference.md)):

- **DCS Catalogs** — curated image sets provided by the platform.
- **Allowed External Registries** — a permitted set of upstreams.
- **Proxy-Cached Catalog** — a caching proxy for permitted upstream images. **Not usable from PROD namespaces** — a workshop that pulls via the proxy cache must do so from a DEV-type namespace, or note the restriction.
- **Image mirroring** — bringing an external image into DCS Harbor (External→DCS Harbor) or copying between DCS Harbor projects (DCS Harbor→DCS Harbor) is requested via an **ITSM ticket**, not done ad hoc. When a workshop conceptually needs a new upstream image, the real-world step is "request a mirror"; in the workshop, the image is already mirrored — point at the ITSM process via docs rather than having the learner mirror live.
- **Robot accounts** — pushes/pulls for automation use a Harbor **robot account**, not a personal login. Workshops that push (e.g. Foundations A04) use robot-account credentials.
- **Helm charts** — Harbor also stores Helm charts; the same catalog/registry rules apply.
- **GitOps** — repo creation and permission management are done "the GitOps way"; a workshop that needs a repo models the request/activation rather than clicking in a UI.

## Workshop container base images

DCS academy workshops use one of **two** base images, both mirrored in Harbor and both extending a common base:

- **`dcs-workshop-base`** — `oc`, shell + prompt theming, git, `jq`/`yq`/`curl`, product params, docs launcher. Used by Foundations, Architect/Onboarding, and most Security workshops.
- **`dcs-tools`** — extends `dcs-workshop-base` with build tooling (`podman`/`buildah`, language runtimes), `k9s`, `trivy`, and observability CLIs. Used by Developer, Observability, and hands-on Security workshops.

Set the workshop image in `resources/workshop.yaml`:

```yaml
# Path: spec.workshop
workshop:
  image: "$(image_repository)/dcs-workshop-base:$(workshop_version)"
```

Pick `dcs-tools` only when the workshop genuinely needs its extra tooling — prefer the smaller `dcs-workshop-base` otherwise. Do not introduce a third workshop image; extend via `setup.d` scripts (see [workshop-setup-reference.md](workshop-setup-reference.md)) for one-off tool needs, and only promote a tool into a base image if several workshops need it.

## Security policy under air-gap

Because upstream images cannot be pulled, choose Harbor-mirrored images that already tolerate OpenShift's arbitrary non-root UID (see [openshift-reference.md](openshift-reference.md)). Mirroring an image does not change whether it runs as root — verify the image is OpenShift-friendly before relying on it, or relax the policy to `baseline` with a stated reason.

## Emitting the image list for mirroring

Every image a workshop references must be present in Harbor before the workshop can run. Keep the set of images minimal and shared across workshops, and emit the full list so operators can mirror it. See [image-manifest-reference.md](image-manifest-reference.md).

## Checklist

- [ ] No external registry (`docker.io`, `quay.io`, `ghcr.io`, `registry.k8s.io`, …) referenced anywhere in content, definition, exercise files, or scripts
- [ ] Workshop image is `dcs-workshop-base` or `dcs-tools` via `$(image_repository)`
- [ ] Every application/tool image uses `{{< param dcs_registry >}}` — no bare image names
- [ ] vcluster component images are Harbor-mirrored
- [ ] All referenced images are listed for Harbor mirroring (see image-manifest-reference.md)
