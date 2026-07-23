# DEV vs PROD Namespaces & Policies

**See why your Route needed a PROD namespace — and what makes PROD a PROD.**

Back in the Core track you exposed an app with a Route, and were told it needed a
PROD-type namespace — no further explanation. Here you get one, hands-on: DCS gives you
a DEV namespace and a PROD namespace side by side, you deploy the identical workload into
both, and watch the two behave differently. A Route you try to create in DEV is rejected;
the same Route in PROD is admitted. The same workload, deployed unchanged, is accepted in
DEV and rejected in PROD until it declares proper resource requests and limits. You then
read the Kyverno policy that draws that line, and see why DCS has you promote a workload
from DEV to PROD rather than edit PROD in place.

- **Track:** Developer — Build on DCS · Lab 6
- **Audience:** Intermediate — comfortable deploying and troubleshooting an app on DCS
- **Duration:** ~20 min
- **Format:** Hands-on, guided — terminal, runs in a per-session virtual cluster giving you two real namespaces to compare
- **Prerequisites:** lab-b05-rbac-tenancy; comfortable with `oc apply`, Deployments, Services and Routes (Core track)

## By the end of this lab you'll be able to

- Distinguish DCS's DEV and PROD namespace types by their **policy posture**, not just their names.
- Explain the two concrete differences: PROD enforces harsher policies (Kyverno) **and** can host a Route; DEV has looser policies **but** cannot host a Route.
- Deploy a workload to DEV, watch a Route get rejected there, then create the same Route successfully in PROD.
- Read a Kyverno policy that PROD enforces and explain what it checks.
- Describe promotion — moving a workload from DEV to PROD instead of editing PROD in place — and the trade-off the split buys you.

## What you'll do

Create a DEV namespace and a PROD namespace, apply the policy that treats them
differently, deploy the `hello-dcs` sample into each and compare what happens, try to
expose it with a Route in both, and finish by reading the policy itself and the
promotion model it implies.

## Before you start

This lab assumes you've done lab-b05-rbac-tenancy (or already know the
Tenant → Namespace model and basic RBAC) and lab-a03-expose-app (Services and Routes). If
a Route or a `Deployment` manifest is unfamiliar, do those first — this lab builds on them
rather than re-teaching them.
