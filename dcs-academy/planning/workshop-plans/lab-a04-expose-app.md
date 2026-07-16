# Workshop Plan: lab-a04-expose-app

## 1. Workshop Metadata

- **Name:** `lab-a04-expose-app`
- **Title:** Expose Your App
- **Description:** Give your app a stable in-cluster address with a Service, then expose it for real with a Route on DCS-managed DNS — reachable outside the session — and surface it as a new dashboard tab inside the session too.
- **Duration:** 30m
- **Difficulty:** intermediate
- **Type:** Core (Module A — Core / Fundamentals)
- **Prerequisites:** A02 (Deploy Your First App)
- **product_name:** Digital Container Service (DCS)
- **Status:** New target design (2026-07-16 rework) — [tasks](../tasks.md#module-a--core--fundamentals-restructure)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (view/apply Service + Route manifests)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: **not** enabled — console tour is A08.
- Examiner: `enabled: true`
- Budget: `medium`
- Workshop image: `dcs-workshop-base`
- Sample app: hello-dcs, pre-deployed via `session.objects` (starts where A02/A03 left the learner).
- **Session dashboard tab:** define a dashboard tab pointing at the app so it appears **inside the session** (via the Route or session proxy). Guide the learner back to Terminal after showing it.
- **PROD-type namespace:** a **Route requires a PROD-type namespace**, so provision one for the Route exercise (the plain session namespace is not enough). Provision via session setup / a `session.objects` namespace object.
- **Routes RBAC:** Educates' default session role **excludes routes** — grant them via a **Role + RoleBinding in `session.objects`** (as fixed in the old A06). Without this the `oc apply` of the Route is forbidden.
- **vcluster decision:** `false` — plain session namespace for the Service; a **separate provisioned PROD-type namespace** for the Route. No vcluster needed.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:
- Explain the DCS traffic chain: **Service → Route → external load balancer** with DCS-managed DNS.
- Note that if customers stay within the "*.apps" domain, DCS takes care of exposure via that external LB and certificates. Customers can optionally request other DNS records but this is not automated and therefore not recommend for development/testing or this lab.
- Give the app a stable in-cluster address with a **Service** and reach it by DNS.
- Expose the app externally with a real **Route** in a PROD-type namespace and reach it **outside the session**. Briefly mention that Route is just an OpenShift specific version of an Ingress (used in opensource upstream K8s)
- Surface the running app as a **new in-session dashboard tab**.
- State that a **Route requires a PROD-type namespace** (the "why" is Developer track B06).

## 4. Connection to Previous Workshop

**Already known** (from A02/A03): the hello-dcs Deployment; labels/selectors (A02 reveal); rolling out changes; reaching the app **locally** with `oc port-forward` (A02) — explicitly the limitation this workshop removes; applying declarative manifests (A03).

**What is new here:**
- The **Service** — a stable in-cluster address in front of ephemeral pods (port-forward from A02 was per-session and manual).
- The **Route** — real external exposure on DCS DNS via the external load balancer, reachable from a normal browser outside the session.
- A **session dashboard tab** for the app.
- The rule that Routes live in **PROD-type namespaces**.

**What should NOT be re-taught:** Deployment/pod mechanics (A02); how labels/selectors work (A02 — the Service reuses the same selector, reference it); rollout mechanics (A03).

## 5. Exercise Files to Create

- `exercises/service.yaml` — Service `hello-dcs`, port 8080 → targetPort 8080, selector `app: hello-dcs` (matches the A02 Deployment).
- `exercises/route.yaml` — OpenShift Route for `hello-dcs`, `host` on DCS-managed DNS (constructed to be policy-compliant — see hostname note). Applied **into the provisioned PROD-type namespace.**
- `exercises/README.md` — placeholder.
- (Optional, if kept) `exercises/networkpolicy-observe.md` note — the pre-provisioned NetworkPolicy to inspect (see page 04).

Note: if the Route host uses `${DCS_...}`-style substitution, apply with `envsubst < route.yaml | oc apply -f -`, never plain `oc apply` (carry-forward bug). Prefer ytt params where possible.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note. Recap the A02/A03 gap: "you could only reach your app locally — let's give it a real address." Objectives; DCS-specific networking blurb + `{{< param dcs_docs_base_url >}}/concepts/networking`.
- **`01-a-stable-address.md`** — why a Service: pods are ephemeral, IPs change; a Service is a stable name + ClusterIP that load-balances to matching pods (reuses the A02 selector — reference, don't re-teach labels). `editor:open-file` `service.yaml`; `oc apply -f service.yaml`; `oc get endpoints hello-dcs`; in-cluster `curl http://hello-dcs.$SESSION_NAMESPACE.svc:8080` from the terminal. [Service DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) upstream. Examiner: Service has endpoints **and** responds HTTP 200.
- **`02-the-traffic-chain.md`** — concept, folded: **Service → Route → external load balancer**, with DCS managing the DNS name. Why in-cluster DNS isn't reachable from outside and the Route is what bridges that. Inline blurb + DCS networking docs; [Route](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html) upstream. **SVG diagram** of the chain (structural concept → page bundle). No commands.
- **`03-expose-it-for-real.md`** — the payoff. Call out that a **Route requires a PROD-type namespace** — that's why this step targets the provisioned PROD-type namespace (hook: "you'll learn *why* PROD namespaces enforce this in Developer B06"). `editor:open-file` `route.yaml`; `oc apply -f route.yaml` **into the PROD-type namespace** (via `-n <prod-ns>` or `envsubst` if templated); `oc get route` shows admitted host on DCS DNS; `curl` the Route host → reachable from outside the session proxy. **Hostname policy note:** the host must be policy-compliant (include the session/tenant identifier) or Kyverno rejects it — call it out. Examiner: Route admitted (host set) **and** the Route URL responds HTTP 200.
- **`04-see-it-in-the-session.md`** — surface the running app as a **new in-session dashboard tab** (`dashboard:open-dashboard` App / `dashboard:create-dashboard` pointing at the Route or session-proxy URL). One line on session proxy vs Route (proxy = HTTPS + auth-gated, convenient in-session; Route = the real external URL). Guide the learner back to Terminal afterward (later `terminal:execute` switches tabs away). Examiner: the proxied/Route endpoint returns 200 (`url:` examiner test).
- **`05-network-policies-and-egress.md`** *(keep from old A06 — observe only)* — **NetworkPolicy** isolates workloads on the shared cluster by matching **labels**; default posture is restrictive. **Tenants cannot self-create them yet** (DCS roadmap) → **inspect a pre-provisioned policy**: `oc get/describe networkpolicy` — do NOT author one. Then air-gapped egress: `oc exec deploy/hello-dcs -- curl -m 5 https://example.com` → examiner asserts it **fails/times out** (egress blocked). Inline blurbs + DCS docs; [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) upstream. Examiner: NetworkPolicy present; egress call fails.
- **`99-workshop-summary.md`** — recap Service vs Route, in-cluster vs external, the dashboard tab, PROD-namespace requirement, observe-only NetworkPolicy + air-gapped egress. Deliberate gap: the app still loses data on restart → motivates **A05 (Storage)**. **Check Your Understanding** (4 Q): how to reach a Service in-cluster; what a Route adds; why a Route needs a PROD-type namespace; why the egress call failed.

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises`. No `cd`.
- **Split terminal:** upper `execute-1` = apply/`curl`; lower `execute-2` optional for `watch oc get route,endpoints`.
- **Cross-namespace:** the Route step targets the provisioned **PROD-type namespace** (`-n <prod-ns>`); everything else stays in the session namespace — track the `-n` on the Route commands.
- **Dashboard tab visibility:** after the App tab is shown (page 04), any later `terminal:execute` switches back to Terminal — guide the learner back to the App tab when needed.
- Patterns: `oc apply -f service.yaml`, `oc get endpoints/route`, `curl http://hello-dcs.$SESSION_NAMESPACE.svc:8080`, `oc apply -f route.yaml -n <prod-ns>` (or `envsubst`), `curl https://<route-host>`, `oc get/describe networkpolicy`, `oc exec ... -- curl -m 5 https://example.com`.

## 8. Design Notes

- Covers **course-topics idea 6** — reframes old **A06 (Networking)** from "networking concepts" to "**expose your app properly**," and trims it from ~55m to a tight 30m by dropping the in-cluster-only framing (Service is now the *first* real step, not a recap) and keeping NetworkPolicy/egress as a single observe page.
- **Real Route + PROD namespace (confirmed):** provision a PROD-type namespace and grant routes via a Role+RoleBinding in `session.objects` (Educates' default session role excludes routes — this was the fix that made old A06 work). The Route is the "expose for real" moment; the session-proxy dashboard tab is the convenient in-session view.
- **Hook, don't teach:** the *why* behind "Routes need a PROD-type namespace" (Kyverno/DEV-PROD policy) is Developer track **B06** — A04 states the rule and points forward, per the Core-teaches-terms / Developer-teaches-mechanisms split.
- **NetworkPolicy observe-only (confirmed):** tenants can't self-create them yet; inspect a pre-provisioned one. The egress-fails demo makes "air-gapped" concrete and memorable — keep it.
- Reuses the shared **hello-dcs** app — no new images. Deliberate gap for A05: no persistence yet.
