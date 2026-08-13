Exercise files for "Configure & Troubleshoot Your App".

- `configmap.yaml`             — non-secret config the app reads (greeting + mode).
- `secret.yaml`                — an Opaque Secret holding one credential-shaped key.
- `deployment-configured.yaml` — the app wired to the ConfigMap (env + mounted file) and the Secret.
- `broken-deployment.yaml`     — the same app with ONE seeded fault for you to diagnose and fix.
