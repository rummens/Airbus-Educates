Exercise files for the Scaling, Health & Resources workshop.

- `deployment-oversized.yaml` — hello-dcs asking for more than the namespace budget allows
  (used to trigger, then diagnose, a quota rejection).
- `deployment-probes.yaml` — the right-sized hello-dcs with readiness + liveness probes.

The `hello-dcs` Deployment and Service are already running in your namespace when the
session starts.
