# Module B — Developer Track (Elective)

For app developers deploying and running their applications on DCS. Sequential within the track, carrying one evolving **sample application** (choose a small, Harbor-mirrorable web app). Builds on Foundations.

## Workshop Structure Conventions

Same conventions as [course-module-a.md](course-module-a.md). Names: `lab-b0N-name`. All follow the house standards.

**Sample app:** **`hello-dcs`** — the repo's small non-root web app (port 8080), reused across B01–B05. Its image lives in Harbor via `{{< param dcs_registry >}}/samples/hello-dcs:1.0` (already Harbor-mirrorable; also used in A02/A03/A06). B06 uses a Harbor-mirrored UDI referenced from a devfile.

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

### Workshop B06: Cloud Development with OpenShift Dev Spaces

**Directory name:** `lab-b06-dev-spaces`
**Covers ideas:** 11b (see course-topics.md)
**Type:** Elective (Developer)
**Prerequisites:** B01
**Learning objectives:** Explain what **OpenShift Dev Spaces** is (in-cluster, browser-based dev environments — upstream Eclipse Che) and why it fits an **air-gapped** platform; launch a workspace from a devfile against the sample app repo; make a code change and run it **inside the cluster**; understand how Dev Spaces relates to the Educates editor and to normal `oc` deploys.
**Narrative arc:** "How do I develop *on* DCS, not just deploy to it?" → Dev Spaces gives every developer a consistent, policy-compliant, air-gapped IDE in the cluster → open a workspace from the sample app's **devfile** → edit + run the app in the workspace → push/deploy with the skills from B01.
**Code exercises:** Open (or inspect) a Dev Spaces workspace from a `devfile.yaml`; run the app in the workspace terminal; make a small change and see it live; compare with the plain `oc apply` flow from B01.
**Key code examples:** A `devfile.yaml` for the sample app referencing a **Harbor-mirrored** dev/UDI image via `{{< param dcs_registry >}}`; the Dev Spaces dashboard URL surfaced as a session dashboard tab.
**Design notes:**
- Dev Spaces is an OpenShift operator-provided service — it must be **installed by the platform team** (ties to A09 operators / Module F). This workshop **uses** it, it does not install it. If a Dev Spaces instance isn't available in the test cluster, deliver the workspace/devfile walkthrough as an annotated, screenshot-driven concept lab (guided tour) rather than live.
- All workspace images come from **Harbor** (air-gapped): mirror the Universal Developer Image (UDI) / chosen stack. No external devfile registries — point `che`/devfile at the mirrored registry.
- Clarify the boundary vs the built-in Educates VS Code editor: the Educates editor is for the *workshop*; **Dev Spaces is the real on-platform dev environment** a tenant would use day to day.
- DCS-specific concept → `{{< param dcs_docs_base_url >}}/services/dev-spaces`; [OpenShift Dev Spaces](https://docs.openshift.com/dev-spaces/latest/) upstream; [devfile](https://devfile.io/) upstream.

## Future Expansion Ideas

- Blue/green or canary rollout workshop (once CI/CD module exists).
- Multi-service app (front + back + db) tying B02/B03/B05 together.
- Dev Spaces + GitLab (Module F) integration: clone from the tenant's GitLab straight into a workspace.
