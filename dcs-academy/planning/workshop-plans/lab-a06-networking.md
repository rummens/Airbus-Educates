# Workshop Plan: lab-a06-networking

## 1. Workshop Metadata

- **Name:** `lab-a06-networking`
- **Title:** Networking & Exposing Apps
- **Description:** Expose an application on DCS with a Route and DCS DNS naming, reach it in the browser, and understand egress restrictions in an air-gapped platform.
- **Duration:** 55m (near the 60m ceiling — if it runs long, split network policies into its own short workshop)
- **Difficulty:** beginner
- **Type:** Core (Module A — Foundations)
- **Prerequisites:** A02 (Kubernetes Essentials on DCS)
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled
- Examiner: `enabled: true`
- Session ingress + dashboard: define a session ingress for the sample app and an "App" dashboard tab (browser access via session proxy)
- Workshop image: `dcs-workshop-base`
- Sample image: reuse `{{< param dcs_registry >}}/samples/hello-dcs:1.0`

## 3. Learning Objectives

- Reach a Service in-cluster by DNS.
- Explain the DCS traffic chain: **Service → Route → External Load Balancer** with DCS-managed DNS.
- Expose an app to the browser via the session proxy, and create an OpenShift Route.
- Construct a Route host from the session hostname (policy-compliant).
- Explain how **Network Policies** (label-based) isolate workloads on the shared cluster, and egress restrictions on the air-gapped platform.

Mapped to DO180 module 4 (expose apps inside and outside the cluster) + DCS networking (docs: Services/Routes/Ingress, External Load Balancer, Network Policies).

## 4. Connection to Previous Workshop

A02 deployed `hello-dcs` and reached it in-cluster via `curl`. This workshop takes the same app and exposes it **externally** (browser), then covers DCS DNS/egress. Do not re-teach Deployment/Service creation — deploy quickly and move to exposure.

## 5. Exercise Files to Create

- `exercises/hello-dcs.yaml` — Deployment+Service (reused from A02).
- `exercises/route.yaml` — OpenShift Route, `host: hello-dcs-$(session_hostname)` — but see design note: prefer session proxy for the embedded tab; Route is the explicit-object exercise.
- `exercises/README.md` — placeholder.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro page. DCS-specific: **networking** blurb + link `{{< param dcs_docs_base_url >}}/concepts/networking`.
- **`01-in-cluster-access.md`**
  - Deploy `hello-dcs.yaml` → polling check ready (experience note).
  - `curl http://hello-dcs.$SESSION_NAMESPACE.svc:8080` → check: HTTP 200. [Service DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) upstream.
- **`02-expose-to-browser.md`**
  - Session proxy: app exposed via `spec.session.ingresses` + dashboard tab; `dashboard:open-dashboard` App → check: proxied endpoint returns 200 (examiner `url:` test against the session-proxy host).
  - Explain why the session proxy is preferred (HTTPS, no mixed content, auth-gated) — see openshift-reference. Guide learner back to terminal afterward.
- **`03-routes-and-dns.md`**
  - Explain the chain **Service → Route → External Load Balancer** (DCS-managed DNS) — inline blurb + DCS networking docs.
  - `editor:open-file` route.yaml; explain [Route](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html) upstream + DCS DNS naming (DCS docs).
  - `oc apply -f route.yaml` → check: Route admitted, host = `hello-dcs-<session_hostname>`.
  - `curl` the Route host → check: reachable.
  - **Note on hostname policy:** host must include `session_hostname` or Kyverno rejects it — call out the requirement.
- **`04-network-policies-and-egress.md`**
  - Concept: **Network Policies** isolate workloads on the shared cluster by matching **labels**; default posture is restrictive. Inline blurb + DCS docs; [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) upstream.
  - Apply/inspect a NetworkPolicy scoping access to the app → check: policy present; a disallowed pod-to-pod call is blocked (diagnose-style + hint).
  - Egress: `oc exec ... -- curl -m 5 https://example.com` → check asserts it **fails/times out** (air-gapped egress). Hint explains egress restriction + egress-IP concept. DCS networking docs link.
- **`99-workshop-summary.md`** — recap in-cluster vs external, session proxy vs Route, egress. **Challenge**: expose a second port/path or create a Route for a given service (examiner-validated) + hint + reveal. **Check Your Understanding** (3 Q): how to reach a Service in-cluster; why Route host must include the session hostname; why external calls fail.

## 7. Terminal Working Directory Tracking

- Split terminal possible (deploy in one, curl in other) — if used, track each independently. Otherwise single terminal in `~/exercises`, manifests by relative name.
- Dashboard tab visibility: after the App tab is shown, any later `terminal:execute` switches back to Terminal — guide the learner back to the App tab when needed.

## 8. Design Notes

- Capstone of Foundations: ties together deploy (A02), namespaces (A03), and exposure. Reuses the shared `hello-dcs` app — no new images.
- Session proxy vs Route: teach both but be explicit that the session proxy is the DCS-preferred path for browser access; the Route exercise exists to teach the object and the hostname policy.
- The egress-fails demonstration makes "air-gapped" concrete and memorable.
- After Foundations, learner is ready for any track. Developer B01 assumes A02+A06 (deploy + expose).
