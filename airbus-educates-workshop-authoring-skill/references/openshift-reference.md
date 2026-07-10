# OpenShift Reference

This skill targets **OpenShift** as the primary Kubernetes distribution. Workshops are authored and deployed against OpenShift, so the `oc` CLI, OpenShift `Route` objects, and Security Context Constraints (SCCs) are the defaults — not plain `kubectl` and `Ingress`.

This reference is the OpenShift companion to [kubernetes-access-reference.md](kubernetes-access-reference.md). Where that reference shows generic Kubernetes patterns, the OpenShift equivalents below take precedence for this skill's output.

## CLI: use `oc`, not `kubectl`

Every command in workshop instructions, exercise scripts, and setup scripts uses `oc`. The `oc` binary is a superset of `kubectl`, so any `kubectl <args>` becomes `oc <args>` verbatim. The workshop container image used for OpenShift workshops includes `oc` on the PATH.

**In terminal clickable actions:**

````markdown
```terminal:execute
command: oc get pods
```
````

**When first mentioning the CLI in instructions**, link the docs (see [documentation-links-reference.md](documentation-links-reference.md)):

```markdown
Inspect the running pods with the [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) command line tool.
```

Do **not** mix `kubectl` and `oc` in the same workshop. If a learner already knows `kubectl`, add a single one-line note that `oc` accepts the same subcommands — do not switch back and forth.

## Projects, not raw namespaces

OpenShift wraps namespaces as **projects**. Each Educates session still maps to one namespace (`session_namespace`), which OpenShift also exposes as a project.

- Prefer `oc project` / `oc get project` phrasing in prose when talking about the working context.
- The session namespace is already the active project in the session — instructions rarely need `oc project <name>`.
- Reference the name with `{{< param session_namespace >}}` (instructions) or `$SESSION_NAMESPACE` (terminal), exactly as in [kubernetes-access-reference.md](kubernetes-access-reference.md).

```markdown
All resources are created in your project, `{{< param session_namespace >}}`.
```

Do not add `oc login` steps. The session's kubeconfig is already authenticated and scoped to the session namespace; a manual login would break RBAC scoping.

## Routes over Ingress

On OpenShift, expose HTTP services with a **Route** rather than a raw `Ingress` where a manual object is genuinely needed. However, the **workshop session proxy remains the preferred mechanism** for browser-facing services (see the "Workshop Session Proxy for Services" section of [kubernetes-access-reference.md](kubernetes-access-reference.md)) — it gives automatic HTTPS, no mixed-content errors, and authentication gating that a hand-written Route does not.

Decision order for exposing a service to the browser:

1. **Session proxy** (`spec.session.ingresses` + `spec.session.dashboards`) — default for anything embedded in the dashboard.
2. **OpenShift Route** — only when the learning objective is specifically about Routes, or an external client outside the session must reach the service.
3. Raw `Ingress` — avoid on OpenShift; use a Route instead.

### Route hostname requirement

Like Ingress hostnames, a Route hostname **must incorporate the session hostname** or the session's Kyverno policy will reject it. Prefix the service name to `session_hostname`:

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: app
spec:
  host: app-$(session_hostname)
  to:
    kind: Service
    name: app
  port:
    targetPort: 8080
```

In instructions, use `app-{{< param session_hostname >}}` for the host, and build the browser URL with `{{< param ingress_protocol >}}://app-{{< param session_hostname >}}`.

Never hardcode a route host, a cluster app domain, or `*.apps.<cluster>` — derive the host from `session_hostname` and the URL scheme from `ingress_protocol`. See [workshop-variables-reference.md](workshop-variables-reference.md).

## Security Context Constraints (SCC) vs pod security policy

Educates enforces a **restricted** pod security policy on the session namespace (see [kubernetes-access-reference.md](kubernetes-access-reference.md)). On OpenShift this aligns with the `restricted-v2` SCC:

- Containers must **not run as root**.
- Containers must **not bind privileged ports** (< 1024).
- Containers must tolerate a **random, non-zero UID** assigned by OpenShift, and must not assume a specific UID. Files the process writes must be group-writable (group `0`).

Consequences for workshop content:

- Images that assume UID 0 or a fixed UID (many upstream `nginx`, `postgres`, `mysql`, `redis`, `mongo` images) fail under the default policy. Prefer OpenShift-friendly variants (e.g. `registry.redhat.io/rhel9/...`, `bitnami/*` images that support arbitrary UIDs, or `image-registry.openshift-image-registry.svc` builds) when possible.
- If an image genuinely needs to run as root or bind port 80, relax the policy to `baseline` in the workshop definition, exactly as documented in [kubernetes-access-reference.md](kubernetes-access-reference.md):

```yaml
# Path: spec.session
session:
  namespaces:
    security:
      policy: baseline
```

Only relax when required, and prefer picking an arbitrary-UID-tolerant image over relaxing the policy. Do **not** instruct learners to run `oc adm policy add-scc-to-user` — sessions cannot modify SCC bindings, and the Educates policy layer, not raw SCC edits, governs what the session may deploy.

## Console

When the OpenShift/Kubernetes web console is enabled, follow the console patterns in [kubernetes-access-reference.md](kubernetes-access-reference.md). The Educates console tab embeds the same generic console; OpenShift-specific console deep-links (developer/administrator perspectives) are not guaranteed and should not be linked from instructions.

## Checklist additions for OpenShift workshops

- [ ] All commands use `oc`, never `kubectl` (no mixing within a workshop)
- [ ] No `oc login` step is present (the session is pre-authenticated)
- [ ] Browser-facing services use the session proxy unless the objective is specifically about Routes
- [ ] Any manual `Route` uses `host: app-$(session_hostname)` / `app-{{< param session_hostname >}}` and never a hardcoded app domain
- [ ] Images tolerate an arbitrary non-root UID, or the policy is deliberately relaxed to `baseline` with a stated reason
- [ ] No `oc adm policy` / SCC-binding commands are given to learners
