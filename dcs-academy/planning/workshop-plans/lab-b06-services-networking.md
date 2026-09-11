# Workshop Plan: lab-b06-services-networking

## 1. Workshop Metadata

- **Name:** `lab-b06-services-networking`
- **Title:** Services & Cluster Networking
- **Description:** Take "expose it" apart — ClusterIP, headless and ExternalName Services, what each puts in cluster DNS, why NodePort and LoadBalancer are the wrong tools on DCS, and where a Route fits.
- **Duration:** 20m
- **Difficulty:** intermediate
- **Track:** Build & Run (`build`), order `60`
- **Prerequisites (curricular only):** Core *Expose Your App*; helpful: **Health & Resources** (endpoints follow readiness)
- **Status:** New lab, written 2026-09-11.

## 2. Workshop Configuration

Terminal `split`, editor, slides, examiner. Budget `medium`. **vcluster `false`** — cluster DNS and endpoints in the learner's own namespace are the subject. Self-contained: the learner applies every manifest; no `session.objects`.

`dcs.airbus.com/lifecycle: dev` deliberately: the lab explains Routes but does **not** create one, because a Route needs a PROD-type namespace. That constraint is part of the lesson, not a gap.

## 3. Learning Objectives

- Name the Service types and say what each is for.
- Resolve a Service through cluster DNS and explain the answer.
- Tell a ClusterIP and a headless Service apart **by their DNS records**.
- Use an ExternalName Service as a stable name for something elsewhere.
- Say why NodePort and LoadBalancer are the wrong tools here, and what replaces them.

## 4. Verified behaviour (measured, not assumed)

Everything this lab claims was checked on a live cluster before it was written:

| Claim | Measured |
|---|---|
| ClusterIP resolves to one address, its own | `getent hosts` → `10.217.5.253 probe-cip…` (= `.spec.clusterIP`) |
| Headless resolves to one address per ready Pod | `getent hosts` → two Pod IPs (`10.217.0.101`, `.102`) |
| ExternalName follows the CNAME to its target | `getent hosts` → target IP **and** the target's own name in the answer |
| A session user may create NodePort / LoadBalancer | both created, exit 0, from inside a session pod |
| NodePort gets a real node port | `8080:30113/TCP` |
| LoadBalancer never gets an address on-prem | `EXTERNAL-IP <pending>`, indefinitely |

The session image has **no `nslookup`, `dig` or `host`** — only `getent` and `python3`. All DNS steps and checks use `getent hosts`.

## 5. Exercise Files

`deployment.yaml` (2 replicas, so every Service has >1 endpoint) · `service-clusterip.yaml` · `service-headless.yaml` (`clusterIP: None`) · `service-externalname.yaml` · `service-nodeport.yaml` · `service-loadbalancer.yaml`

**The ExternalName target is `kubernetes.default.svc.cluster.local`** — it must be something that genuinely resolves on an air-gapped cluster, or the demo teaches nothing. The manifest and the page both say that the real-world case is an outside host, which additionally needs the managed egress proxy.

## 6. Instruction Pages

- **`00-workshop-overview.md`** — five answers hiding behind one phrase; objectives; positioned as the depth behind Core's happy path.
- **`01-service-types/`** — the five types, then which three a tenant uses here and why. **SVG** `service-types.svg`.
- **`02-clusterip-and-dns.md`** — deploy, apply, Service vs endpoints, resolve by hand (one address, the Service's own), `curl` through the name.
- **`03-headless-services.md`** — `clusterIP: None`, `CLUSTER-IP: None` in the table, resolve (one record per Pod), the StatefulSet forward pointer, the no-failover warning.
- **`04-externalname.md`** — the alias, no endpoints to have, follow the CNAME, what it is good for, and the egress warning (a name is not access).
- **`05-nodeport-and-loadbalancer.md`** — apply both, read what each got, why each is wrong here, the Route as the supported path with its PROD constraint, then delete both.
- **`98-your-feedback.md`**, **`99-workshop-summary.md`** — standard, 4-question knowledge check.

## 7. Examiner Coverage (11 checks, one per command)

`verify-app-ready` · `verify-clusterip-endpoints` · `verify-clusterip-single-ip` · `verify-clusterip-http` · `verify-headless-created` · `verify-headless-per-pod` · `verify-externalname-created` · `verify-externalname-resolves` · `verify-nodeport-assigned` · `verify-loadbalancer-pending` · `verify-wrong-types-removed`

Two are unusual on purpose:

- **`verify-loadbalancer-pending` asserts an absence.** On a cluster that *does* fulfil LoadBalancer Services it fails loudly — correct, because the page's claim would not hold there.
- **`verify-headless-per-pod` also asserts a negative:** none of the returned addresses may be the ClusterIP Service's virtual IP, so a mis-authored headless Service cannot pass by accident.

## 8. Design Notes

- The DNS answers *are* the lesson, so every type is resolved by hand rather than described.
- NodePort and LoadBalancer are **applied, not just discussed** — the learner sees that "created successfully" and "usable" are different things, which is the actual trap.
- The lab cleans up after itself: a permanently pending LoadBalancer left in a namespace is exactly the confusing artefact the page warns about.
