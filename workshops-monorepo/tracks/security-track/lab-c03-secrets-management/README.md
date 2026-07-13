# Secrets Management on DCS

**Spot a credential leaking through images, logs, and env dumps; move it into a Kubernetes Secret sourced by reference; and prove it's no longer exposed.**

A credential ends up in the wrong place more than anything else — an API token, a database password, a signing key. The moment one is written in plaintext where it shouldn't be, it has leaked. On the Digital Container Service (DCS) handling credentials correctly is also a governance obligation: the platform's Terms & Conditions make secret and data protection the tenant's responsibility. In this lab you'll take a Deployment that leaks a token three different ways, move it into a Kubernetes Secret, wire the workload to it by reference, and verify the leak is gone — meeting head-on the single most common misconception about Secrets.

- **Track:** Security & Compliance — Secure on DCS · Lab 3 of 5
- **Audience:** Intermediate — comfortable applying manifests, setting env on a Deployment, and reading logs with `oc`
- **Duration:** ~40 min
- **Format:** Hands-on, guided — split terminal, runs in your OpenShift session namespace
- **Prerequisites:** the Core track, especially lab-a02-kubernetes-essentials; familiar with Deployments and container env vars.

## By the end of this lab you'll be able to

- Identify the three common secret-leak paths: baked into the image, printed to logs, and inline in a manifest or env dump.
- Explain that a Kubernetes Secret is base64-encoded, not encrypted, and that its protection comes from RBAC plus platform etcd encryption at rest — not from the encoding.
- Move a plaintext credential into a Secret and consume it via `secretKeyRef` rather than a literal value.
- Verify a secret is not exposed — not in an env dump, not as a literal in the rendered workload.
- Describe the stronger options DCS offers (sealed / external secrets) at a concept level.

## What you'll do

- Inspect a Deployment that leaks a token via image, logs, and an inline env value.
- Create a Kubernetes Secret and rewire the workload to consume the credential by `secretKeyRef`.
- Confirm the encoding-vs-encryption distinction, then verify the token no longer appears in any dump or rendered manifest.
