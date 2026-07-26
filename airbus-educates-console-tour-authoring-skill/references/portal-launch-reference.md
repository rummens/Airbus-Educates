# Hidden labs: pairing with a Workshop and launching from the portal

A hidden console lab needs an environment. That environment is a **normal Educates session** —
the portal allocates it exactly as it would for a terminal lab, so the session namespace, its
quota, its objects, capacity limits and the session reaper all work unchanged. The only
difference is the final redirect: instead of the workshop dashboard, the browser is sent to the
OpenShift console with the lab's launch URL.

## The chain

1. The learner presses **Start** on the course page.
2. The portal allocates an Educates session. `spec.session.objects` create the lab's resources
   in the session namespace.
3. The portal waits until the session **and the lab's own pods** are ready.
4. The portal creates a `RoleBinding` giving the signed-in learner the
   `academy-console-lab-user` ClusterRole **in that session namespace**. Educates exposes no
   data variable carrying the human's identity — the session runs as its ServiceAccount — so
   session objects cannot do this and the portal must.
5. The browser is redirected to
   `https://<console>/academy/lessons/<lab>/start?ns=<session namespace>&<params>&returnUrl=…`,
   and the plugin scopes the console to that project and starts the tour.
6. **Finish** returns to the portal, which records the completion and terminates the session.

## The Workshop CR

`workshops-monorepo/tracks/<track>/<lab>/resources/workshop.yaml`:

```yaml
metadata:
  name: lab-u01-container-access          # == the ConsoleLab name and the folder name
  labels:
    academy.dcs/track: core
    academy.dcs/order: "90"
    academy.dcs/lab-format: console       # THIS is what makes the portal redirect
    dcs.airbus.com/lifecycle: dev
  annotations:
    academy.dcs/console-lab: lab-u01-container-access
    academy.dcs/console-lab-params: podName=lab-app     # everything except ns
    academy.dcs/orphaned: "0s"            # see below — mandatory for console labs
    academy.dcs/expires: 60m
spec:
  workshop:
    image: "{{ .Values.workshopImages.base }}"   # no content files: nobody opens the dashboard
  session:
    namespaces: { budget: medium, security: { token: { enabled: true } } }
    applications:                                 # nothing to click through in the dashboard
      terminal: { enabled: false }
      editor:   { enabled: false }
      console:  { enabled: false }
      slides:   { enabled: false }
    objects: [...]
```

### Traps, each of which cost a debugging round

- **`academy.dcs/orphaned: "0s"` is mandatory.** Orphan detection watches the workshop dashboard,
  which a console-lab learner never opens; with the default the session is reclaimed mid-lab.
  The CRD types this as a string matching `^\d+(s|m|h)$` — a unit is required, so `"0s"`, never
  `"0"`. A unitless value renders as a YAML integer and breaks the ArgoCD diff for the whole
  application, not just that lab.
- **Name the lab's objects explicitly.** The ConsoleLab navigates to exact paths like
  `/k8s/ns/<ns>/pods/lab-app`. Use a bare `Pod`, not a `Deployment`, whose pod name carries a
  generated suffix that cannot be templated into the lab.
- **Label the lab's pods** with `training.educates.dev/session.name: $(session_name)` so the
  portal's readiness feed waits for them. Without it the learner is redirected to the console
  before the pod the tour talks about exists.
- **Images in `session.objects` are really pulled.** Unlike an image merely named in workshop
  content, this one runs — take it from `values.workshopImages.*` so an air-gapped install
  repoints it in one place.
- **Do not set `ns` in `console-lab-params`.** The portal always injects the session namespace;
  a declared `ns` is ignored as a reserved key.

## Two namespaces

A lab that compares projects (for example `lab-u02-namespace-scope`) needs a second namespace.
Declare it as a normal parameter (`secondNamespace=…`) and provision it with Educates' secondary
session namespaces. Do not invent a second session.

## RBAC

`academy-console-lab-user` (portal chart, `templates/02-console-lab-rbac.yaml`) is roughly `edit`
minus the ability to create RoleBindings, granted namespace-scoped to one learner in their own
session namespace. The portal ServiceAccount may bind **that role and no other** — the RBAC
`bind` verb names it explicitly, so the API server itself refuses an attempt to bind anything
wider. If a lab needs a permission the role lacks, extend the role deliberately; never widen the
portal's grant.

## returnUrl

The portal builds `returnUrl` from its **public** origin and the plugin honours it only when the
origin matches `AcademySettings.spec.portalUrl` exactly. A mismatch (typically `http://` from a
TLS-terminating route) silently disables the return, and Finish only dismisses the panel. The
plugin logs a warning naming both origins when it refuses one.

## Lifecycle

- **Finish** → the portal records the completion and terminates the session.
- **Stop** → ends the tour but leaves the environment running; the learner can restart it or let
  it expire.
- Nothing else changes: `expires`, the session reaper and **My sessions** work as for any lab.
