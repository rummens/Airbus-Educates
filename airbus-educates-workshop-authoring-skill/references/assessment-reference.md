# Assessment Reference

**House standard: every command in a workshop has an examiner verification, and every workshop ends with a knowledge check.** This is a hard rule, not a "where it matters" guideline. Its purpose is twofold: learners never advance on assumption, and — critically — the examiner tests form an **automated test pipeline** that can run every workshop end-to-end (headless) to prove it still works. A command with no verification is a hole in that pipeline.

Two mechanisms, both required:

1. **Examiner verification for every command** — every `terminal:execute` (and any other state-changing action) is paired with an `examiner:execute-test` that asserts the expected outcome. Read-only/inspection commands are verified by asserting the observable state they were meant to reveal exists.
2. **A knowledge check** per workshop — a short recap that tests comprehension, not just completion.

## Why every command (automated pipeline)

Examiner tests are plain scripts in `workshop/examiner/tests/`. Because there is one asserting the outcome of every command, a CI pipeline can spin up a session, run the tests in order, and get a pass/fail for the whole workshop without a human clicking through it. This only holds if coverage is total — the moment a command has no test, the pipeline silently stops verifying from that point. So: **one test per command, no exceptions.** Where several commands form one atomic outcome, a single test asserting that outcome covers them; where a command has a distinct observable effect, it gets its own test.

## Enabling the examiner

Set in `resources/workshop.yaml`:

```yaml
# Path: spec.session
session:
  applications:
    examiner:
      enabled: true
```

## Examiner step checks

Place test scripts in `workshop/examiner/tests/` (executable, exit `0` = pass). Invoke them with `examiner:execute-test` clickable actions. See [clickable-actions/examiner-actions.md](clickable-actions/examiner-actions.md) for full syntax (args, retries, polling, form inputs).

**Where to add checks:** after every command. Each `terminal:execute` is immediately followed by an `examiner:execute-test` asserting its outcome — a created resource, a reachable endpoint, a value in output, an expected state. Use polling (`retries: .INF`, `delay`) for asynchronous outcomes like a Deployment becoming ready. Group only genuinely atomic command sequences under a single test.

```markdown
```examiner:execute-test
name: verify-app-running
title: Verify the sample app is running
args:
- sample-app
timeout: 5
retries: .INF
delay: 1
```
```

**Guidance:**
- Write checks against DCS/OpenShift reality using `oc` inside the test script.
- Keep tests idempotent and re-runnable — a learner may click a check multiple times, and examiner checks must stay reliable across session resets (see reset/idempotency guidance in your workshop plan).
- Every command is verified (see the every-command rule above). For a purely observational command, assert the observable state it was meant to reveal exists — do not skip it.
- A test script counts as a runtime image dependency only if it pulls one — keep tests to shell + `oc`.

**Emit a diagnostic message on failure.** A check that just exits `1` is useless to a stuck learner and to the CI pipeline reading logs. On failure, print *what* was expected and *what* was found, then exit non-zero:

```bash
#!/bin/bash
# workshop/examiner/tests/verify-app-running
name="${1:-sample-app}"
if ! oc get deployment "$name" >/dev/null 2>&1; then
  echo "Deployment '$name' not found in $(oc project -q). Did the apply step run?" >&2
  exit 1
fi
ready=$(oc get deployment "$name" -o jsonpath='{.status.readyReplicas}')
if [ "${ready:-0}" -lt 1 ]; then
  echo "Deployment '$name' exists but has 0 ready replicas — check pod events with 'oc get events'." >&2
  exit 1
fi
echo "OK: deployment '$name' is ready."

## Hints and revealing solutions (optional)

Guided workshops rarely leave a learner stuck, but for steps that ask the learner to *figure something out* (a diagnose-and-fix step, an end-of-workshop challenge), offer graduated help — the pattern peer platforms (Instruqt `solve.sh`) use:

- **Hint** — a collapsible nudge that points at the approach without giving the answer:

  ```markdown
  {{< note >}}
  **Hint:** the pod is crash-looping. Check its recent events and logs before changing anything.
  {{< /note >}}
  ```

- **Reveal solution** — for a stuck learner, a clickable action that applies the correct state so they can continue rather than abandon the workshop. Put it after the hint, clearly labelled as the answer:

  ````markdown
  If you are stuck, apply the fix directly:

  ```terminal:execute
  command: oc set resources deployment/sample-app --limits=memory=128Mi
  ```
  ````

Use sparingly and only where the learner is expected to problem-solve — for ordinary guided steps the clickable action already *is* the solution.

## End-of-workshop challenge (optional, recommended)

Beyond click-through steps, a workshop can end with **one unguided challenge** — a task stated as an outcome with no step-by-step instructions, validated by the examiner. This tests whether the learner can apply what they practised, not just follow along, and it gives the automated pipeline a higher-order assertion.

```markdown
## Challenge

Without step-by-step guidance: scale the sample app to 3 replicas, and make sure it
stays within the namespace quota. Then run the check below.
```

Pair it with an `examiner:execute-test` that validates the outcome, and offer a hint + reveal-solution (above) for learners who need them. Keep it short — one challenge, tied to the workshop's main objective.

## Knowledge check per workshop

End each workshop (before or within `99-workshop-summary.md`) with a **Check Your Understanding** section: 2–4 questions recapping the workshop's key ideas. Educates has no native quiz widget, so use one of these patterns:

**Preferred — examiner-validated answer.** Ask the learner to demonstrate understanding by producing a result an examiner test validates (e.g. "scale the app to 3 replicas and verify"). This tests doing, not recall, and reuses the examiner.

**Recap questions with revealable answers.** For conceptual recall, pose questions and hide the answer in a collapsible block so the learner self-checks:

```markdown
## Check Your Understanding

1. Which namespace type enforces change control on DCS — dev or prod?

{{< note >}}
**Answer:** prod. Dev namespaces favour fast iteration; changes are promoted from dev to prod.
{{< /note >}}
```

Keep questions tied to the stated learning objectives — one question per major objective. Link any DCS concept in the answer to its docs (see [dcs-concepts-reference.md](dcs-concepts-reference.md)).

## Checklist

- [ ] `spec.session.applications.examiner.enabled: true`
- [ ] **Every command has an `examiner:execute-test`** asserting its outcome — no command is unverified (automated-pipeline requirement)
- [ ] Atomic command sequences share one test; distinct observable effects each get their own
- [ ] Examiner tests use `oc`, are idempotent, headless-runnable, and poll for async outcomes
- [ ] Every check emits a diagnostic message on failure (expected vs found), not a bare exit 1
- [ ] Test names/order let a CI pipeline run the whole workshop end-to-end
- [ ] Diagnose/challenge steps offer a hint and a reveal-solution; ordinary guided steps need neither
- [ ] Workshop ends with a **Check Your Understanding** section, one question per major learning objective (optionally an unguided challenge tied to the main objective)
- [ ] Conceptual answers link DCS concepts to `dcs_docs_base_url` and standard constructs to upstream docs
