# lab-b05-stateful-storage — Stateful Workloads & Storage

Developer-track (Module B) workshop. The learner gives the `hello-dcs` sample app
persistence: request a PVC from a DCS storage class, mount it, write data, and prove it
survives a pod restart.

- **Track:** Developer (`academy.dcs/track: dev`), order 50 · **Difficulty:** intermediate · **Duration:** 35m
- **Prerequisites:** B01 (Deploy Your First App); A07 (Storage) for the platform view.
- **Sample app:** `hello-dcs` (`{{< param dcs_registry >}}/samples/hello-dcs:1.0`), pre-deployed via `session.objects`.
- **Storage class:** parameterised as `{{< param dcs_storage_class >}}` — never hard-coded.
- **Session:** native OpenShift namespace (no vcluster).

Optional lab in the B chain — self-contained, skippable without breaking B06.
