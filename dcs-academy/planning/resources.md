# Course Resources

Curated external documentation for the DCS Academy subject matter. Consult this before searching the web. Two classes, matching the hybrid doc-link standard:

- **Upstream** — for standard Kubernetes/OpenShift constructs (linked directly from workshops).
- **DCS docs portal** — for DCS-specific concepts, referenced via the `dcs_docs_base_url` param (placeholder until the portal URL is confirmed).

## Upstream references

| Topic | URL |
|---|---|
| OpenShift Container Platform | https://docs.openshift.com/container-platform/latest/ |
| OpenShift CLI (`oc`) | https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html |
| OpenShift Routes | https://docs.openshift.com/container-platform/latest/networking/routes/route-configuration.html |
| OpenShift Security Context Constraints | https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html |
| Kubernetes concepts | https://kubernetes.io/docs/concepts/ |
| Kubernetes workloads (Deployments) | https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ |
| ConfigMaps & Secrets | https://kubernetes.io/docs/concepts/configuration/ |
| RBAC | https://kubernetes.io/docs/reference/access-authn-authz/rbac/ |
| Harbor | https://goharbor.io/docs/ |
| Prometheus | https://prometheus.io/docs/ |
| Grafana | https://grafana.com/docs/ |

## DCS docs portal (via `dcs_docs_base_url`)

| DCS concept | Path (param-relative) |
|---|---|
| Namespace types (prod/dev) | `/concepts/namespace-types` |
| Registry (Harbor) | `/concepts/registry` |
| Tenancy & access | `/concepts/tenancy-and-access` |
| Networking on DCS | `/concepts/networking` |

The blurbs and teaching notes for these live in the authoring skill's `dcs-concepts-reference`.

## Training curriculum references (design inspiration)

Used to shape the Foundations sequence. Proven ordering: intro/console → CLI & API health → run/troubleshoot pods → deploy managed & networked apps → config & storage → reliability → updates.

| Source | URL |
|---|---|
| Red Hat DO180 (OpenShift Administration I) outline | https://www.redhat.com/en/services/training/red-hat-openshift-administration-i-operating-a-production-cluster |
| Coursera — Fundamentals of Containers, Kubernetes & OpenShift (developers) | https://www.coursera.org/learn/fundamentals-of-red-hat-openshift-for-developers |
| Red Hat learn.openshift.com — Foundations of OpenShift | https://learn.openshift.com/introduction/deploying-images/ |
| Red Hat interactive labs | https://www.redhat.com/en/interactive-labs/openshift |
| Instruqt lab structure & tasks (authoring patterns) | https://docs.labs.instruqt.com/configuration/lab-structure/ |
| Skillable — building successful hands-on labs | https://docs.skillable.com/docs/building-successful-hand-on-labs |

## Curation Notes

- Registry, docs portal URL, and Harbor project are **placeholders** — replace with confirmed values when available. No workshop rebuild is needed to re-point them (they are params).
