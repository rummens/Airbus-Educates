<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Harbor: Projects, Push & Scan

How the DCS registry decides which images may run.

**In this lab:** catalogs and projects · asking for a project · inspect without pulling · copy between registries · read a scan · how an image reaches PROD.

Digital Container Service · DCS Academy

---

<!-- id: rules -->
## Catalogs, projects, and the asymmetry

Three rules govern what you may pull and push.

- **Catalogs** — DCS, allowed-external, proxy-cached, and the **green catalog** of cleared images.
- **Projects** — a tenant may get one, scoped **per namespace** today (per-tenant is the direction).
- **DEV takes pushes**, of anything, with no CVE limitation.
- **PROD takes none**, and pulls only **below CVE severity 9**.
- Unfixable finding in something you need? That is the **security exception** process.

![Catalogs supply images; DEV projects accept pushes, PROD accepts none and pulls below the CVE threshold](registry-rules.svg)

---

<!-- id: inspect -->
## Look without pulling

`skopeo` asks the registry directly — no daemon, nothing downloaded.

```
skopeo inspect docker://$DCS_REGISTRY/samples/hello-dcs:1.0
skopeo inspect --config docker://$DCS_REGISTRY/samples/hello-dcs:1.0
```

- **Digest** — the real identity. Content-addressed: same digest, same bytes.
- **RepoTags** — tags move; digests do not.
- **Layers** — images that share a base share layers, so rebuilds are faster.
- **--config** — `User`, `Env`, `Cmd`. Check `User` before you meet the restricted SCC.

---

<!-- id: project -->
## Ask for a project

A Harbor project is a Kubernetes object. Crossplane's Harbor provider reconciles it.

```
apiVersion: project.harbor.crossplane.io/v1alpha1
kind: Project
spec:
  forProvider:
    name: my-namespace-scratch
    public: false
    vulnerabilityScanning: true
    deploymentSecurity: ""     # DEV: serve anything. PROD: "critical"
```

- **`vulnerabilityScanning`** — scan on push, which is what produces the report.
- **`deploymentSecurity`** — the severity Harbor refuses to serve. `critical` is the CVE < 9 rule.
- Delete the object, the provider deletes the project.

---

<!-- id: copy -->
## Copy it somewhere else

One command moves an image between registries. This is the operation behind every mirror, import and promotion.

```
skopeo copy --dest-tls-verify=false \
  --dest-creds "unused:$(oc whoami -t)" \
  docker://$DCS_REGISTRY/samples/hello-dcs:1.0 \
  docker://image-registry.openshift-image-registry.svc:5000/$SESSION_NAMESPACE/mirrored:1.0
```

- Copies layers as they are, so digests stay the same.
- Credentials: only the **token** is checked. Use `unused` as the username, not `$(oc whoami)`. On DCS, use a Harbor **robot account** scoped to one project.
- A promotion is this copy, requested through ITSM, into a project that accepts no other route.

---

<!-- id: scan -->
## Read a scan

The verdict is four numbers in `summary.severityCount`; the decision is in the detail.

```
jq '{artifact, summary}' scan-report-flagged.json
jq -r '.vulnerabilities[] | select(.severity=="Critical")
       | "\(.id) \(.package) \(.installedVersion) → \(.FixedVersion // "no fix")"' \
  scan-report-flagged.json
```

- Critical is 9.0+, so a flagged image is refused by PROD but allowed in DEV.
- **`fixable`** is the number to read first: most findings are fixed by rebuilding on a newer base.
- No fix available → remove it, replace it, or take the exception route.
- The verdict attaches to a **digest** — re-pushing a tag does not inherit it.

---

<!-- id: promotion -->
## Getting into PROD

There are two routes into PROD.

- **The green catalog** — already cleared. A cleared base also helps your own builds pass.
- **Promotion** — a mirror from DEV, requested through **ITSM**, with the digest preserved and the gate enforced.
- **Robot accounts** for automation: scoped to one project, revocable, and not tied to any person's account.
- No push access means no unreviewed image can reach PROD, even by accident.

---

<!-- id: next -->
## What's next

You can follow one artefact end to end: built on the cluster, pushed to DEV, scanned, promoted or replaced, and finally deployed into a PROD namespace that enforces its own policies.

The rest of **Build & Run** is about the workload it becomes — sizing, scaling, exposing, state, and surviving the platform's maintenance.

Digital Container Service · DCS Academy
