# Module B — Build & Run (Track `build`)

For developers who have had their quick win in Core and now want to **build for** DCS and run
what they built properly. Ten labs, roughly four hours, every one live-verified on a real
cluster.

Replaces the old Developer track (superseded 2026-09-11 — see
[TRACK-PLAN-build-operate.md](TRACK-PLAN-build-operate.md)). The platform-mechanism material
that used to sit here now lives in [Operate & Observe](course-module-o.md).

## The arc

An artefact, followed end to end: a mental model, an image, a registry that governs it, then
the workload it becomes — sized, autoscaled, reachable, stateful, and survivable.

| Order | Lab | Duration | Verified |
|---|---|---|---|
| 10 | [From Docker to Kubernetes](workshop-plans/lab-b01-docker-to-k8s.md) | 25m | 22/22 |
| 20 | [Build Your Image on DCS](workshop-plans/lab-b02-build-your-image.md) | 25m | 19/19 |
| 30 | [Harbor: Projects, Push & Scan](workshop-plans/lab-b03-harbor.md) | 30m | 18/18 |
| 40 | [Health & Resources](workshop-plans/lab-b04-health-resources.md) | 25m | 21/21 |
| 50 | [Autoscaling](workshop-plans/lab-b05-autoscaling.md) | 20m | 15/15 |
| 60 | [Services & Cluster Networking](workshop-plans/lab-b06-services-networking.md) | 20m | 24/24 |
| 70 | [Stateful Workloads](workshop-plans/lab-b07-stateful-workloads.md) | 25m | 25/25 |
| 80 | [Short-Lived & Helper Containers](workshop-plans/lab-b08-short-lived-containers.md) | 25m | 28/28 |
| 90 | [Resilience & Scheduling](workshop-plans/lab-b09-resilience-scheduling.md) | 25m | 22/22 |
| 100 | [Dev Spaces](workshop-plans/lab-b10-dev-spaces.md) *(optional)* | 18m | 4/4 |

### Optional console companions

Each sits directly after the terminal lab it complements, marked `academy.dcs/optional`, so
the catalog badges it and leaves it out of the required path and the track trophy.

| Order | Console lab | Pairs with | Duration |
|---|---|---|---|
| 25 | Builds in the console | Build Your Image on DCS | 8m |
| 45 | Health & resources in the console | Health & Resources | 8m |
| 55 | Autoscaling in the console | Autoscaling | 7m |

They apply the concepts and introduce none: every step names the `oc` command it stands in
for, and says what the console is actually better at.

## Decisions that shaped the track

- **b01 is the on-ramp**, and it now teaches the **SCC** properly rather than naming it: the
  learner asks for a root container and reads the refusal, which distinguishes "an SCC you may
  use, refusing your request" from "an SCC that is not yours".
- **b02 uses a binary build.** The long-standing "needs an air-gapped git source" blocker was
  removed by dropping the dependency: the learner's session files are the input, and the
  objects are identical to a git-source build.
- **b03 separates mechanics from policy** and says which is which. `skopeo` is exercised for
  real; the DEV/PROD project rules and the scan gate are taught, with fixtures.
- **b08 folds three topics into one** (Jobs, CronJobs, init containers and sidecars) because
  they answer one question: how long is this container supposed to run?
- **b10 is optional** and marked as such in the catalog: Dev Spaces is operator-provided and
  cannot be exercised on a training cluster.

## Not here, on purpose

Tenancy and RBAC, DEV/PROD policy, metrics, logs and operators — all in **Operate & Observe**.
Security governance (classification, provenance, supply chain) belongs to the Security track
when it is replanned.
