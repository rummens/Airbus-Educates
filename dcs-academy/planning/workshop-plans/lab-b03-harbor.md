# Workshop Plan: lab-b03-harbor

## 1. Metadata
- **Name:** `lab-b03-harbor` · **Title:** Harbor: Projects, Push & Scan
- **Duration:** 35m · **Difficulty:** intermediate · **Track:** Build & Run, order `30`
- **Prerequisites (curricular):** *Build Your Image on DCS*, *From Docker to Kubernetes*
- **Status:** New lab, 2026-09-11. Live-verified 18/18. Page 03 (Harbor project via
  Crossplane) added 2026-09-12 and not yet live-verified — CRC was stopped before it could
  run.

## 2. Mechanics exercised, policy taught
The split is deliberate and stated in the lab:
- **Exercised for real:** `skopeo inspect` (digest, layers, labels), `skopeo inspect --config` (the `User` line the restricted SCC cares about), and a genuine **registry-to-registry copy** into the cluster's registry. That copy is the operation a promotion performs, so the learner does the mechanic before meeting the process around it.
- **Taught:** catalogs (including the **green catalog**), the per-namespace Harbor project, and the asymmetry: **DEV takes pushes of anything, PROD takes none and pulls only below CVE severity 9**. Promotion is a mirror requested through **ITSM**, or a cleared image.
- **Requested, conditionally exercised:** the Harbor project itself, as a Crossplane
  `Project` (`project.harbor.crossplane.io/v1alpha1`, the upjet-based provider-harbor kind).
  The Academy cluster has no Harbor and no provider, so `request-project.sh` branches: with
  the CRD present it applies the CR and waits for `Ready`; without it, it renders the manifest
  with `yq` and reads the request back. The examiner check asserts whichever of those two is
  true, so the lab is honest on both kinds of cluster.

## 3. Measured before authoring
| Fact | Measured |
|---|---|
| `skopeo` | already in `dcs-workshop-base`; no docker/podman anywhere |
| Registry credentials | the cluster registry checks the **token only** — the username is ignored (`unused`, `builder`, `sa` all work) |
| `$(oc whoami)` as username | **breaks**: expands to `system:serviceaccount:<ns>:<name>`, and the colons break `user:password` parsing with "authentication required" |

## 4. Design notes
- The `Project` CR carries the DEV/PROD rules as fields, which is why it earns a page:
  `vulnerabilityScanning: true` is what produces the report read two pages later, and
  `deploymentSecurity` is the CVE < 9 rule in one field (empty for DEV, `critical` for PROD).
  The provider kind is a **placeholder to retune** against whatever DCS actually exposes.
- Scan reports are **fixtures** in the shape Harbor's scanner produces, read with `jq`. The lab says so where it matters; the fields and the gate arithmetic are what transfer.
- Asserted arithmetic: `Critical=0` passes, `Critical=2` does not, and `fixable` is the number to read first because most findings are one newer base away.
- A scan verdict belongs to a **digest**, which is the lab's second argument for why floating tags are refused.
