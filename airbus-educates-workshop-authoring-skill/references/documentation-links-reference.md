# Documentation Links Reference

**House rule: every technical concept links to its official documentation on first mention.** When a workshop page first introduces a concept, tool, resource type, or API — a Deployment, a Route, `oc`, Helm, a language feature — make that first mention a Markdown link to the canonical upstream documentation. Subsequent mentions on the same page do not need to be linked again.

This gives learners an immediate path to authoritative depth without the workshop having to re-explain everything, and keeps the workshop focused on the hands-on exercise.

## Rules

- **First mention only.** Link the first time a concept appears on a page. Repeated mentions stay plain text.
- **Official upstream sources.** Link the canonical vendor/project documentation (OpenShift, Kubernetes, the tool's own site) — not blog posts, Stack Overflow, or tutorials.
- **Link the concept, not a generic word.** Link "[Deployment](url)", not the word "deployment" used in plain English.
- **Prefer version-stable URLs.** Use `.../latest/...` or the docs site's canonical path so links do not rot. Avoid deep-linking to a specific patch version unless the workshop pins that version.
- **Inline Markdown links.** `[Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)`. In the introduction page's Prerequisites and Further Reading, links are expected; in body pages, weave them into the prose naturally.
- **Don't over-link.** One link per concept per page. A paragraph with ten links helps no one — link the concepts that matter to the exercise.

## Two link classes: standard vs DCS-specific (hybrid)

DCS is air-gapped, and some concepts are DCS-specific. This produces two classes of link:

- **Standard constructs** (Kubernetes/OpenShift primitives — Deployment, Secret, ServiceAccount, Route, Pod, etc.): link to **official upstream** documentation using the canonical bases below. These links may be unreachable from inside an air-gapped session, but they remain valuable — learners open them from their own machine — so keep them.
- **DCS-specific concepts** (namespace types, Harbor registry, tenancy & access, networking on DCS, and anything else particular to the platform): link to the **DCS documentation portal** via the `dcs_docs_base_url` param, and **also give an inline blurb** so an air-gapped learner understands the concept without following the link. The canonical source for these concepts, their blurbs, and their doc paths is [dcs-concepts-reference.md](dcs-concepts-reference.md).

```markdown
Deploy the app with a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
into your [dev namespace]({{< param dcs_docs_base_url >}}/concepts/namespace-types). On DCS, a dev
namespace favours fast iteration; changes are promoted to a prod namespace rather than edited in place.
```

Here `Deployment` → upstream (standard construct); `dev namespace` → DCS portal via param, with an inline blurb. Never link a DCS-specific concept to upstream, and never link a standard construct to the DCS portal.

`dcs_docs_base_url` is one of the mandatory param trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`) — see [workshop-variables-reference.md](workshop-variables-reference.md). It defaults to a placeholder and is re-pointable without a rebuild.

## Reference internal documentation for depth and procedures

Beyond linking a concept's docs, actively point learners at **internal DCS documentation** where it adds value — procedures the workshop only summarises (requesting a quota increase, image mirroring, onboarding a tenant — all ITSM flows), and deeper reading on DCS-specific concepts. Link via the `dcs_docs_base_url` param so it re-points without a rebuild:

```markdown
On DCS, a quota increase is requested through an ITSM ticket — see
[Requesting a quota increase]({{< param dcs_docs_base_url >}}/quotas/increase).
```

Prefer internal docs for anything DCS-operational (the workshop teaches the concept; the internal doc is the source of truth for the real-world procedure). Like analogies, this can taper as courses advance — early workshops hand-hold with links to onboarding/how-to pages; advanced ones assume the learner knows where the portal is.

## Canonical documentation bases

Use these roots to construct links. Confirm the exact deep path when in doubt; these are the stable entry points.

| Concept area | Canonical documentation base |
|---|---|
| OpenShift Container Platform | https://docs.openshift.com/container-platform/latest/ |
| OpenShift CLI (`oc`) | https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html |
| OpenShift Routes | https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html |
| OpenShift Security Context Constraints | https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html |
| Kubernetes concepts (Pods, Deployments, Services, etc.) | https://kubernetes.io/docs/concepts/ |
| Kubernetes API reference | https://kubernetes.io/docs/reference/kubernetes-api/ |
| `kubectl`/CLI reference | https://kubernetes.io/docs/reference/kubectl/ |
| Helm | https://helm.sh/docs/ |
| Kustomize | https://kubectl.docs.kubernetes.io/references/kustomize/ |
| Containers / OCI images | https://kubernetes.io/docs/concepts/containers/ |
| Prometheus | https://prometheus.io/docs/ |
| Grafana | https://grafana.com/docs/ |
| Argo CD | https://argo-cd.readthedocs.io/en/stable/ |
| Tekton / OpenShift Pipelines | https://docs.openshift.com/pipelines/latest/ |
| Educates platform | https://docs.educates.dev/ |

For subject matter outside this table (a programming language, a framework, a specific product), link that project's official documentation site. When a course exists, prefer the links recorded in the course's `planning/resources.md` — they have already been vetted for the course subject.

## Examples

Good — concept linked on first mention, plain thereafter:

```markdown
Create a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
to run the application. The Deployment ensures the desired number of replicas stay running.
```

Good — OpenShift resource linked:

```markdown
Expose the service with a [Route](https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html).
```

Avoid — no link on a concept's first mention:

```markdown
Create a Deployment to run the application.   <!-- missing docs link -->
```

## Checklist

- [ ] Every concept, tool, and resource type is linked on first mention on each page
- [ ] Standard constructs link to canonical upstream sources, not third-party articles
- [ ] DCS-specific concepts link to `{{< param dcs_docs_base_url >}}` and carry an inline blurb (see [dcs-concepts-reference.md](dcs-concepts-reference.md))
- [ ] No standard construct is mislinked to the DCS portal, and no DCS concept to upstream
- [ ] No concept is linked more than once per page
- [ ] Introduction page Prerequisites/Further Reading use these links
