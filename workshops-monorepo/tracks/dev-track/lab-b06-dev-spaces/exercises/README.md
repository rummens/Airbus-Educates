Exercise files for the Cloud Development with OpenShift Dev Spaces workshop.

- `devfile.yaml` — the reproducible workspace definition for the sample app. All images come
  from the DCS Harbor registry via `${DCS_REGISTRY}` (air-gapped — no external registries).

**Delivery note:** the live steps need a Dev Spaces instance pre-installed by the platform
team and a Harbor-mirrored UDI. If none is available, this workshop runs as an annotated,
screenshot-driven concept walkthrough — the devfile and the concepts still apply.
