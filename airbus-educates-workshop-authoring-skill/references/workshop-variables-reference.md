# Workshop Variables Reference

**House rule: never hardcode an infrastructure value or the product name.** Every image registry host, domain, route host, namespace, external endpoint, tool version, and the product/service name the workshop is delivered under must come from a variable. This lets the same workshop source be deployed to a different cluster, registry, or product context without editing the instruction pages.

There are three planes of variables. Pick the lowest-effort plane that reaches every context where the value is used.

## Plane 1 — Cluster/platform data variables (no rebuild, ever)

Educates injects these automatically and they differ per cluster and per session. Always use them instead of literals. See [data-variables-reference.md](data-variables-reference.md) for the full list. The ones that most often get wrongly hardcoded:

| Value you might be tempted to hardcode | Use instead |
|---|---|
| Published image registry host | `$(image_repository)` |
| Ingress/route base domain | `$(ingress_domain)` |
| `http` / `https` scheme | `$(ingress_protocol)` / `{{< param ingress_protocol >}}` |
| Session namespace / project | `$(session_namespace)` / `{{< param session_namespace >}}` |
| Session hostname (for route/ingress hosts) | `$(session_hostname)` / `{{< param session_hostname >}}` |
| Session image registry host | `$(registry_host)` / `{{< param registry_host >}}` |
| Git server host | `{{< param git_host >}}` |

These require **no rebuild and no configuration** — they resolve at session start on whatever cluster the workshop runs on.

## Plane 2 — Author params in `workshop/config.yaml` (content)

For values the **author** controls and wants swappable in one place — the product name, an external/mirror image registry, an external documentation base, tool versions, a display label — declare them once under `params:` in `workshop/config.yaml`:

```yaml
# workshop/config.yaml
params:
  product_name: "ACME Container Platform"
  product_short: "ACME"
  external_registry: "registry.example.com"
  app_version: "1.4.2"
```

Read them in instructions with the same `param` shortcode used for platform variables — Hugo falls back to site params when the name is not a built-in data variable:

```markdown
This workshop is delivered as part of **{{< param product_name >}}**.

Pull the sample image from `{{< param external_registry >}}/samples/app:{{< param app_version >}}`.
```

Changing a Plane-2 value is a **one-line edit in one file**. It is baked into the published files, so it takes effect on the next publish/session start — there is no need to touch any instruction page.

**`product_name` is mandatory.** Every workshop declares `product_name` (and optionally `product_short`) in `workshop/config.yaml`, and the introduction page renders it (see [introduction-page-reference.md](introduction-page-reference.md)). When the workshop is part of a course, the course sets the default product name — see the course-design skill's course brief.

### The mandatory param trio (DCS)

Every DCS academy workshop declares these three params in `workshop/config.yaml`:

```yaml
# workshop/config.yaml
params:
  product_name: "Digital Container Service (DCS)"
  dcs_registry: "harbor.example.dcs/dcs-academy"        # Harbor project for images (placeholder)
  dcs_docs_base_url: "https://docs.example.dcs"          # DCS docs portal base (placeholder)
```

- `product_name` — the product/service the workshop is delivered under; rendered via `{{< param product_name >}}`.
- `dcs_registry` — the Harbor location for all author-chosen application/tool images. Every image reference uses `{{< param dcs_registry >}}/...` so the air-gapped registry is declared once. See [air-gapped-images-reference.md](air-gapped-images-reference.md).
- `dcs_docs_base_url` — the base URL of the DCS documentation portal. DCS-specific concept links are built as `{{< param dcs_docs_base_url >}}<path>`. See [documentation-links-reference.md](documentation-links-reference.md) and [dcs-concepts-reference.md](dcs-concepts-reference.md).

All three default to placeholders and are re-pointable without editing content — change the one line (or override per-deployment via Plane 3) and every page updates. Standard cluster infrastructure (registry the workshop-files come from, domains, hostnames) still uses Plane-1 data variables like `$(image_repository)`.

## Plane 3 — Session env for values needed in the terminal AND definition

Plane-2 params are only visible to the content renderer. When the **same** author-controlled value is also needed in the terminal or in the workshop definition, set it once as a session environment variable:

```yaml
# Path: spec.session
session:
  env:
  - name: EXTERNAL_REGISTRY
    value: registry.example.com
```

It is then available in the terminal as `$EXTERNAL_REGISTRY` and can be referenced elsewhere in the definition. To also expose it to the content renderer as `{{< param external_registry >}}`, either mirror it in `workshop/config.yaml` params, or export it from a `setup.d` script into `$WORKSHOP_ENV` (see [workshop-setup-reference.md](workshop-setup-reference.md), "Setting Persistent Environment Variables"), which makes exported variables available as Hugo data variables.

Keep a single source of truth: if a value lives in both `config.yaml` params and `session.env`, note in a comment that the two must be kept in sync, or derive one from the other in `setup.d`.

## Deploy-time override without touching workshop files

For true per-deployment overrides (e.g. a different registry per environment) without editing the workshop source at all, the operator can set `spec.session.env` on the **WorkshopEnvironment** / **TrainingPortal**, or pass `request.parameters`, which override the workshop's own values. Design workshops so the override points are Plane-2/Plane-3 variables — never literals buried in prose — so this lever actually works.

## Applying the rule while authoring

- Before writing any hostname, registry, domain, version, or product reference, ask: *which plane does this belong to?* If it is cluster infrastructure → Plane 1. If author-controlled and content-only → Plane 2. If author-controlled and also needed in terminal/definition → Plane 3.
- The only literals that should appear in instructions are things intrinsic to the subject matter (e.g. a Kubernetes field name), never environment- or product-specific values.
- Seed `workshop/config.yaml` with a `params:` block at workshop creation time containing at least `product_name`, even if empty, so the variable point exists from the start.

## Checklist

- [ ] `workshop/config.yaml` exists and declares the param trio: `product_name`, `dcs_registry`, `dcs_docs_base_url`
- [ ] No hardcoded registry host, domain, route/ingress host, or namespace anywhere in content, definition, or scripts — each uses the correct plane
- [ ] All application/tool image references use `{{< param dcs_registry >}}` (no external registries — see [air-gapped-images-reference.md](air-gapped-images-reference.md))
- [ ] DCS-specific concept links use `{{< param dcs_docs_base_url >}}`
- [ ] The introduction page renders `{{< param product_name >}}`
- [ ] Any author-controlled value used in more than one context has a single source of truth
