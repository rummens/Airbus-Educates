# Testing a console lab

A console lab is coupled to console markup and to a live namespace. Reading the YAML proves
nothing. Run it.

## 1. Render and apply the content

```bash
helm template w workshops-monorepo --show-only templates/consolelabs.yaml | oc apply -f -
oc get consolelabs
```

Rendering through Helm (not `oc apply -f` on the raw file) is the point: it catches a `{{ }}`
that should have been `<<>>`, and a literal `{{` inside a comment, both of which fail at deploy
time rather than in review.

The `consolelabs.academy.dcs` CRD must already exist — it ships with the console plugin
deployment, not with this chart. If `oc apply` rejects a step with
`Unsupported value: "acknowledge"` (or any other operation/verification), the cluster is running
an older CRD than the engine: apply the plugin repo's copy first, and remember that ArgoCD's
selfHeal reverts a hand-applied CRD within minutes, so the plugin repo has to be pushed for the
change to stick.

```bash
bin/pluginctl render ocp-4.22 -s templates/crds.yaml | oc apply -f -   # console plugin repo
```

## 2. Run the tour as a learner

**Default lab** — open the console, select a project, then
**Home → Academy labs → Start lab**.

**Hidden lab** — provision the environment the way the portal does:

```bash
cd test/workshops
./deploy_workshop.py lab-u01-container-access     # Workshop + Environment + Session, portal-less
oc get pods -n lab-u01-container-access-01
```

then open the launch URL by hand:

```text
https://<console-host>/academy/lessons/lab-u01-container-access/start?ns=lab-u01-container-access-01&podName=lab-app
```

`deploy_workshop.py` **synthesises** its own Workshop CR and does not run Helm, so it drops the
`academy.dcs/*` annotations and leaves `{{ .Values… }}` unrendered in `session.objects` — patch
the image by hand for a local run, or test the annotations through the portal instead.

Tear down with `./deploy_workshop.py <lab> --delete`.

If `<lab>-01` does not exist and `deploy_workshop.py` reports the environment as already
present, the standalone `WorkshopEnvironment`/`WorkshopSession` pair was deleted at some point.
Recreate them directly — Educates names the session namespace `<environment>-<session id>`:

```bash
oc apply -f - <<'EOF'
apiVersion: training.educates.dev/v1beta1
kind: WorkshopEnvironment
metadata: { name: lab-u01-container-access }
spec: { workshop: { name: lab-u01-container-access } }
---
apiVersion: training.educates.dev/v1beta1
kind: WorkshopSession
metadata: { name: lab-u01-container-access-w01 }
spec:
  environment: { name: lab-u01-container-access }
  session: { id: "01", password: educates, username: educates }
EOF
```

## 3. What to check

- **Every step advances on its own.** Walk the tour performing each action yourself and never
  touching Continue. A step that needs Continue is a broken target or a wrong verification —
  Continue is a failsafe for console upgrades, not a substitute for a working detector. **Next**
  on an `acknowledge` step is not Continue: it is that step's own action.
- **Every step is anchored.** The guidance bubble must appear beside the highlight. If the
  workflow panel says *"Waiting for the console element"* instead, the engine cannot measure the
  target even though it exists — the step is unusable, and no amount of reading the YAML shows
  it.
- **No step is skipped.** Watch the step counter. A step whose verification is already true when
  it becomes current flashes past; its text is never read.
- **The namespace is right.** Start the lab with a *different* project selected first. The
  launcher must switch the console to the lab's namespace; the tour must never run in the
  project that happened to be open.
- **Back works.** It must return to the previous step and stay there.
- **No step strands the learner.** Watch for a highlight that never appears — usually a target on
  a page the previous step did not open, or a nav section the accordion closed.
- **Completion.** The completion text appears, and for a portal-launched lab **Finish** returns
  to the portal, records the completion and terminates the session.

## 4. Repo checks

```bash
test/workshops/label_check.py --all        # lifecycle labels + expires/orphaned format
helm template w workshops-monorepo >/dev/null   # the whole chart still renders
```

`label_check.py` rejects an `academy.dcs/expires|orphaned` that is not `^\d+(s|m|h)$` — the check
exists because a unitless `"0"` breaks the ArgoCD diff for the entire application.

The content checkers (`coverage_check.py`, `link_check.py`) skip console labs: they have no
`workshop/content` directory and no README, which they report as `skip`, not as a failure.

## 5. Automated coverage

The console plugin repository holds a Playwright suite that exercises the engine against a live
console, including a portal-launch reproduction (wrong project selected first, launch with `ns`,
run to completion, Finish returns).

`tests/e2e/specs/hidden-labs.spec.ts` covers hidden labs **generically**: it reads each
ConsoleLab from the cluster and performs the learner action for every step, asserting that the
target exists on the page the previous step ended on and that the lab advances without Continue.
A new lab therefore needs no new spec — add its name to `ACADEMY_HIDDEN_LABS` and its launch
parameters to that file's `LAB_PARAMS`, with the lab's session namespace already provisioned.
Two things the spec needs when a lab uses a control no lab used before:

- its `targetLocator` map must learn the new `consoleElement` id, or the run fails with
  `unknown consoleElement id: …`;
- Playwright's `toBeVisible()` means "in the DOM with a box", **not** "on screen", so the spec
  also asserts the guidance bubble rendered. Keep that assertion: without it a target below the
  fold passes the test while the learner is told to press Continue.

```bash
cd tests/e2e   # in the console plugin repo
CONSOLE_URL=https://console-openshift-console.apps-crc.testing CONSOLE_PASSWORD=<kubeadmin> \
  npx playwright test specs/hidden-labs.spec.ts --workers=1
```

Do this for every new lab. The manual walkthrough above stays the quicker check while writing
the steps; the spec is what keeps them working after a console upgrade.
