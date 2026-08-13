Exercise files for "Pod Security & SCC on DCS".

- `pod-compliant.yaml` — a Pod running the sample image with a correct **restricted**
  `securityContext` (`runAsNonRoot`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`,
  `seccompProfile: RuntimeDefault`). It is admitted and runs.
- `pod-root.yaml` — the same image but requesting `runAsUser: 0` + `privileged: true` with no
  restrictions. Admission (restricted PSA / restricted-v2 SCC) **rejects** it. On page 04 you
  edit this file in place to make it compliant.

Both Pods reference the image through the `${DCS_REGISTRY}` environment variable so the manifest
is not tied to a specific registry; apply them with `envsubst` (the instructions do this for you).
