# lab-b02-config-and-secrets — Configuration & Secrets

Developer-track (Module B) workshop. The learner externalises the `hello-dcs` sample app's
config into a ConfigMap (env + mounted file), injects a credential via a Secret without leaking
it, and rolls out a config change on the same image.

- **Track:** Developer (`academy.dcs/track: dev`), order 20 · **Difficulty:** intermediate · **Duration:** 35m
- **Prerequisites:** B01 (Deploy Your First App).
- **Sample app:** `hello-dcs` (`{{< param dcs_registry >}}/samples/hello-dcs:1.0`), pre-deployed via `session.objects` (config still baked in — the problem this lab solves).
- **Note:** hello-dcs is a static server, so config/secret **delivery** is verified at the container boundary with `oc exec` (printenv / cat), not via the HTTP body.
- **Session:** native OpenShift namespace (no vcluster).
