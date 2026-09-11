<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# DEV vs PROD Namespaces

Not a naming convention — a **policy posture**. Same cluster, same Kubernetes, same registry, two different answers to the same YAML.

**In this lab:** the label and the policy · DEV moves fast · PROD makes you prove it · promotion.

Digital Container Service · DCS Academy

---

<!-- id: types -->
## Two types, one difference

Both namespaces are ordinary Kubernetes. What separates them is a label, and the admission policy that reads it.

```
oc get namespace $DEV_NS $PROD_NS --show-labels
```

- `route-requires-prod` — a Route in a DEV-type namespace is denied.
- `prod-requires-resources` — a container in a PROD-type namespace must declare CPU and memory, requests **and** limits.
- A representative slice of the real posture, enforced through the cluster's real admission path.

![A DEV namespace admits an unsized workload but refuses a Route; PROD does the opposite](namespace-types.svg)

---

<!-- id: dev -->
## DEV moves fast

The manifest people actually write first: no resources block, nothing finished.

```
envsubst < hello-dcs-unsized.yaml | oc apply -f - -n $DEV_NS   # admitted
oc apply -f route.yaml -n $DEV_NS                              # refused
```

- Accepted without comment — DEV is staying out of your way.
- The Route is refused: *"A Route needs a PROD-type namespace."*
- A Route publishes on the platform's **external edge**. That is a production act.
- So: iterate in DEV, publish from PROD.

---

<!-- id: prod -->
## PROD makes you prove it

The same unsized manifest, one namespace over.

```
envsubst < hello-dcs-unsized.yaml | oc apply -f - -n $PROD_NS  # refused
envsubst < hello-dcs-sized.yaml   | oc apply -f - -n $PROD_NS  # admitted
oc apply -f route.yaml -n $PROD_NS                             # admitted, real host
```

- Refused at **`oc apply`** — nothing created, nothing to debug later.
- The message names the rule and the failing path, down to the container index.
- "autogen" in the rule name: the Pod rule is auto-derived for the Deployment.
- One `resources` block is the whole difference between refused and admitted.

---

<!-- id: promotion -->
## Promotion

Two running states from two different manifests is exactly what promotion prevents.

- **The same image**, by tag or digest — from the **green catalog**, or mirrored from the DEV project by request.
- **The same manifest**, with only environment values differing. Sized, because PROD insists.
- **Not** an edit in place: untested, and the next promotion silently overwrites it.
- PROD's refusal was the platform checking that what you are promoting is promotable.

---

<!-- id: next -->
## What's next

You can read the platform's answer, and the rule behind it, for any namespace you are given.

**Next lab — Operators on DCS:** the pattern behind the platform services you use, CRD versus CR, and the ownership split — the platform owns the operator, you own the instance.

Digital Container Service · DCS Academy
