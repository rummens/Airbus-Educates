# Workshop Plan: lab-b03-harbor

## 1. Metadata
- **Name:** `lab-b03-harbor` · **Title:** Harbor: Projects, Push & Scan
- **Duration:** 30m · **Difficulty:** intermediate · **Track:** Build & Run, order `30`
- **Prerequisites (curricular):** *Build Your Image on DCS*, *From Docker to Kubernetes*
- **Status:** New lab, 2026-09-11. Live-verified 18/18.

## 2. Mechanics exercised, policy taught
The split is deliberate and stated in the lab:
- **Exercised for real:** `skopeo inspect` (digest, layers, labels), `skopeo inspect --config` (the `User` line the restricted SCC cares about), and a genuine **registry-to-registry copy** into the cluster's registry. That copy is the operation a promotion performs, so the learner does the mechanic before meeting the process around it.
- **Taught:** catalogs (including the **green catalog**), the per-namespace Harbor project, and the asymmetry — **DEV takes pushes of anything, PROD takes none and pulls only below CVE severity 9**. Promotion is a mirror requested through **ITSM**, or a cleared image.

## 3. Measured before authoring
| Fact | Measured |
|---|---|
| `skopeo` | already in `dcs-workshop-base`; no docker/podman anywhere |
| Registry credentials | the cluster registry checks the **token only** — the username is ignored (`unused`, `builder`, `sa` all work) |
| `$(oc whoami)` as username | **breaks**: expands to `system:serviceaccount:<ns>:<name>`, and the colons break `user:password` parsing with "authentication required" |

## 4. Design notes
- Scan reports are **fixtures** in the shape Harbor's scanner produces, read with `jq`. The lab says so where it matters; the fields and the gate arithmetic are what transfer.
- Asserted arithmetic: `Critical=0` passes, `Critical=2` does not, and `fixable` is the number to read first because most findings are one newer base away.
- A scan verdict belongs to a **digest**, which is the lab's second argument for why floating tags are refused.
