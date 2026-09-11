# Workshop Plan: lab-o05-operators

## 1. Metadata
- **Name:** `lab-o05-operators` · **Title:** Operators on DCS
- **Duration:** 25m · **Difficulty:** advanced · **Track:** Operate & Observe, order `50`
- **Prerequisites (curricular):** *Stateful Workloads*, *RBAC & Tenancy*
- **Status:** Re-authored from the superseded `lab-b08-operators`, 2026-09-11. Live-verified 12/12.

## 2. Three environment truths, each of which changed the lab
| Fact | Consequence |
|---|---|
| A tenant **cannot list CRDs** (cluster-scoped) | the lab reads the API through **discovery** — `oc api-resources --api-group=…`, `oc explain` — which any authenticated user may do |
| The session role has **no `postgresql.cnpg.io` rules** | `session.objects` grants the operator's kinds in a namespace of the session's own |
| The CNPG operand **cannot exec** in any Educates-managed namespace | `educates-restricted` uses `runAsUser: MustRunAsNonRoot` where `restricted-v2` assigns a UID from the namespace range → `exec container process /controller/manager: Permission denied`. Binding `educates-privileged-scc` does not help; the session pins its SCC. |

## 3. What the lab asserts instead of a booted database
The **reconcile**: the volume claim, the Services, the secrets and the Pods the operator built from four lines of spec, plus the status it writes back. A warning on the page says plainly that the database process stops short here for an Academy-environment reason, and that the same CR boots on a real tenant namespace (verified: healthy in ~40s in a plain namespace).

## 4. Design notes
- The CR deliberately sets **no `imageName`**: the platform configures which operand image the operator may run. That absent field *is* "the platform owns the operator", and it also makes the manifest portable.
- Positioned as the bridge to the Operators track (GitLab, Argo CD, CloudNativePG), which owns the depth.
