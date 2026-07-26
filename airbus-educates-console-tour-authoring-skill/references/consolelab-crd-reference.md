# ConsoleLab CRD reference

`consolelabs.academy.dcs/v1alpha1`, cluster-scoped, operator-free catalog data — the same pattern
as the portal's `Track` CRD. The CRD ships with the **console plugin** repository
(`Airbus-Academy-Console-Plugin/deploy/base/crd.yaml`); the workshops chart only fills it with
instances.

## Skeleton

```yaml
apiVersion: academy.dcs/v1alpha1
kind: ConsoleLab
metadata:
  name: lab-u01-container-access        # == folder name; this is the lab ID in launch URLs
  annotations:
    argocd.argoproj.io/sync-wave: "5"
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
spec:
  title: Inspect and enter a running container
  description: >-                       # shown in the console's own lab catalog
    ...
  completionText: >-                    # shown when the last step verifies
    ...
  visibility: default | hidden          # default: listed for anyone. hidden: launch URL only
  mode: assisted | timed                # assisted: the learner acts. timed: the engine acts
  timerDelay: 5s                        # timed mode only
  context:                              # optional: a resource whose live phase is displayed
    primaryResource: labPod
    resources:
      labPod: { apiVersion: v1, kind: Pod, label: Lab pod, name: ..., namespace: ..., listPath: ..., consolePath: ..., tabs: {...} }
  steps: [...]
```

`mode` is only the default: the catalog offers both **Start lab** (assisted) and **Watch demo**
(timed), and a launch URL may pass `?mode=timed`. Author every lab as `assisted`; timed is a
presentation of the same content, not separate content.

## Launch parameters

Any `<<name>>` in the spec is substituted at launch from the URL query string.

```text
/academy/lessons/lab-u01-container-access/start?ns=lab-user-17&podName=web-1
```

- `ns` is an alias for `<<namespace>>` and is **always supplied by the portal**. Never declare it
  as a lab parameter and never hardcode a namespace.
- Any other placeholder (`<<podName>>`, `<<secondNamespace>>`) must be declared in the paired
  Workshop's `academy.dcs/console-lab-params`, or the lab refuses to start and names what is
  missing.
- Values are restricted to characters legal in a Kubernetes name or console path; anything else
  is dropped rather than substituted.
- **Why `<<>>` and not `{{}}`:** the file is rendered by Helm (`tpl`) at deploy time, so `{{ }}`
  belongs to Helm and `$( )` to Educates. A placeholder that must survive to the browser needs a
  third delimiter. You may use real Helm expressions in the same file for deploy-time values.

For a default lab, `<<namespace>>` falls back to the project the console is currently scoped to.
That is what makes a default tour usable by any learner in their own project.

## Steps

```yaml
steps:
  - id: open-pods                       # stable, kebab-case, unique in the lab
    title: Open Pods                    # imperative, 2–5 words
    description: >-                     # see step-writing-reference.md
      ...
    target: { type: consoleElement, id: navigationLink, value: Pods }
    complete:
      operation: { type: navigate, path: '/k8s/ns/<<namespace>>/core~v1~Pod' }
      verify: { type: route, path: '/k8s/ns/<<namespace>>/core~v1~Pod' }
```

A step is: **highlight this** (`target`), **this is how it gets done** (`operation`, used by
Continue and by timed mode), **this proves it happened** (`verify`, watched continuously).

### Targets

| `type` | Resolves | Use for |
|---|---|---|
| `quickStartId` | element with `data-quickstart-id="<value>"` | navigation sections: `qs-nav-home`, `qs-nav-workloads`, `qs-nav-networking`, `qs-nav-storage` |
| `href` | anchor whose URL matches `value` (GVK and legacy plural forms both match) | a link to a specific object or tab |
| `consoleElement` | a named control via the version adapter | `namespaceSelector`, `namespaceFilter`, `namespaceOption` (exact option text in `value`), `navigationLink` (exact sidebar link name), `resourceSearch` |

### Operations

| `type` | Does |
|---|---|
| `activateTarget` | clicks the highlighted control |
| `navigate` | routes to `path` |
| `fillTarget` | types `value` into the highlighted input |

### Verifications

| `type` | Advances when |
|---|---|
| `route` | the browser reaches a URL equivalent to `path` |
| `targetAttribute` | the target carries `attribute: value` (use for expandable sections: a click alone does not prove the section opened) |
| `targetValue` | the highlighted input contains `value` exactly |
| `namespace` | the current route is scoped to `value` |

Route comparison is tolerant of the console's alternative URLs for the same page
(`apps~v1~Deployment` ↔ `deployments`, a project-scoped list ↔ the all-namespaces list) but
**not** of a different namespace. To assert the scope itself, use `namespace`.

## Placement rules — the common way to strand a learner

The target of step *N* must exist on the page step *N-1* leaves the learner on.

- **The project selector only renders on namespaced pages.** A tour that starts on the launcher
  page cannot target `namespaceSelector` as its first step.
- **Navigation sections are an accordion.** Expanding Storage collapses Home. If a later step
  targets a link under a section you closed, re-expand it in its own step first.
- **Exact object paths need exact names.** `/k8s/ns/x/pods/lab-app` only resolves if the pod is
  literally named `lab-app` — so a paired Workshop must create a bare Pod, not a Deployment
  whose pods carry a generated suffix.
- A step whose target never appears does not fail loudly: assisted mode waits, and the learner
  has to press Continue. Treat "Continue was required" as a bug in the lab.

## What not to put in a lab

CSS selectors, JavaScript, or anything executable. The launcher accepts a lab name plus
parameters and resolves all behaviour from the cluster's lab content; targets are limited to the
three trusted kinds above so a launch URL can never point the engine at arbitrary markup.
