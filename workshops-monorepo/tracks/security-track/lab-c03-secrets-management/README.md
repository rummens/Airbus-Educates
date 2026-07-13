# lab-c03-secrets-management

**Secrets Management on DCS** — Security & Compliance (Module C) elective for the DCS Academy.

Learners spot the three common secret-leak paths (baked into the image, printed to logs,
inline in a manifest / env dump), move a plaintext credential into a Kubernetes `Secret`
consumed via `secretKeyRef`, and verify it is no longer exposed. Along the way they see the
key misconception head-on: a Secret is base64-**encoded**, not encrypted — what protects it is
**RBAC** + platform **etcd encryption at rest**. Prerequisite: Module A (esp. A02).

Built with the `airbus-educates-workshop-authoring` skill. See the plan at
`planning/workshop-plans/lab-c03-secrets-management.md`.
