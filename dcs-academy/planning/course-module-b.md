# Module B — Developer Track (Elective)

For app developers deploying and running their applications on DCS. Sequential within the track, carrying one evolving **sample application** (choose a small, Harbor-mirrorable web app). Builds on Foundations.

## Workshop Structure Conventions

Same conventions as [course-module-a.md](course-module-a.md). Names: `lab-b0N-name`. All follow the house standards.

**Sample app:** one web app (TBD — see `tasks.md`), reused across B01–B05. Its image lives in Harbor via `{{< param dcs_registry >}}`.

---

### Workshop B01: Deploy Your First App on DCS

**Directory name:** `lab-b01-deploy-first-app`
**Covers ideas:** 7
**Type:** Elective (Developer)
**Prerequisites:** Module A (Foundations)
**Learning objectives:** Deploy the sample app to a dev namespace; expose it; confirm it runs.
**Narrative arc:** Meet the sample app → deploy it → expose it via the session proxy → verify it responds.
**Code exercises:** Apply Deployment + Service; add session ingress/dashboard; examiner check that it is reachable.
**Key code examples:** Deployment/Service with `{{< param dcs_registry >}}` image; session ingress.

### Workshop B02: Configuration & Secrets

**Directory name:** `lab-b02-config-and-secrets`
**Covers ideas:** 8
**Type:** Elective (Developer)
**Prerequisites:** B01
**Learning objectives:** Externalise config via ConfigMap; inject secrets safely; roll out a config change.
**Narrative arc:** App needs config → move it to a ConfigMap → add a Secret → observe rollout.
**Code exercises:** Create ConfigMap/Secret, mount them, trigger a rollout, verify.
**Key code examples:** ConfigMap/Secret + volume/env wiring. Constructs → upstream.

### Workshop B03: Scaling, Health & Resources

**Directory name:** `lab-b03-scaling-health`
**Covers ideas:** 9
**Type:** Elective (Developer)
**Prerequisites:** B01
**Learning objectives:** Set replicas; add liveness/readiness probes; set requests/limits within quota.
**Narrative arc:** Scale up → hit the quota → right-size requests/limits → add probes for reliability.
**Code exercises:** Scale the app; add probes; set resources; examiner checks readiness.
**Key code examples:** Probes + resources block (mind the namespace budget). Constructs → upstream.

### Workshop B04: Debugging & Logs

**Directory name:** `lab-b04-debugging-logs`
**Covers ideas:** 10
**Type:** Elective (Developer)
**Prerequisites:** B01
**Learning objectives:** Diagnose a failing workload using logs, events, and describe; fix it.
**Narrative arc:** App is broken (pre-seeded fault) → inspect logs/events → identify cause → fix → verify.
**Code exercises:** `oc logs`, `oc describe`, `oc get events`; apply a fix; examiner confirms recovery.
**Key code examples:** A deliberately broken manifest the learner repairs. "Observe and diagnose" style.

### Workshop B05: Stateful Workloads & Storage *(optional)*

**Directory name:** `lab-b05-stateful-storage`
**Covers ideas:** 11
**Type:** Elective (Developer)
**Prerequisites:** B01
**Learning objectives:** Request storage via a PVC; understand DCS storage classes; run a stateful workload.
**Narrative arc:** App needs to persist data → request a PVC → attach it → verify persistence across a restart.
**Code exercises:** Create PVC, mount it, write data, restart, confirm data survives.
**Key code examples:** PVC + volume mount using a DCS storage class. Constructs → upstream.

## Future Expansion Ideas

- Blue/green or canary rollout workshop (once CI/CD module exists).
- Multi-service app (front + back + db) tying B02/B03/B05 together.
