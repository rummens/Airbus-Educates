# lab-c02-pod-security-scc

**Pod Security & SCC on DCS** — Security & Compliance (Module C) workshop for the DCS Academy.

Learners see why DCS runs tenant workloads under the **restricted** Pod Security Standard and
the **restricted-v2** SCC: they deploy a compliant Pod, watch a root/privileged Pod get
**rejected at admission**, read the rejection, and remediate the `securityContext` so it is
admitted. Runs on the native OpenShift session namespace — the namespace's default restricted
enforcement is the whole point, so the security policy is left untouched.

Built with the `airbus-educates-workshop-authoring` skill. See the plan at
`planning/workshop-plans/lab-c02-pod-security-scc.md`.
