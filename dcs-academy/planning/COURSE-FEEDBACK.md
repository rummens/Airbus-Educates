# Course Feedback — tracking

Author feedback captured 2026-07-16 while walking the built Core labs. Status per item:
`[ ]` todo · `[x]` done · `[~]` in progress · `[?]` needs a decision (don't do blindly).
Another session can pick up any `[ ]`/`[~]`. Verify with the CRC smoke harness
(`test/workshops/run_track.sh <lab-dir>`) after content changes; push origin/main first
(git-source reads origin/main).

## Lab 0 — lab-a00-environment-tour
- [x] Explain the **evaluator** (the green "Verify" examiner checks) — what they are, why they gate progress. Add to the dashboard-layout / a dedicated blurb.
- [x] Explain **why the native Kubernetes Dashboard, not the OpenShift console** (embedding limitation: real console can't be iframed — `educates-openshift-console-limitation` memory). Page 04 names the distinction but not the *why*.

## Lab 1 — lab-a01-what-is-dcs
- [x] Page 3 (`03-containers-and-images`) needs an **image** (added image-vs-container.svg; page now a bundle) (SVG — container vs image, or containers-vs-VM).
- [?] Add **slides** to this lab — too much text, too little action. (Educates `slides` app / reveal deck. Bigger change — confirm approach.)
- [x] Page ~5 (`04-why-kubernetes-not-just-docker`): reframed 4 VM-world analogies → plain-Docker contrasts; should compare **K8s vs Docker** (not containers vs VMs). Reframe: what Docker-on-one-box can't do that K8s does.
- [?] **Move A01 toward the END of the module** — too much theory up front, not enough action. (Reorder = renumber churn: academy.dcs/order labels + cross-refs + deploy. Decision needed; low-churn option = just bump its `academy.dcs/order` so it sorts later, keep the dir name.)

## Lab 2 — lab-a02-deploy-first-app
- [x] Page 2 (`01-deploy-it`): added `oc get deployment,pods` 'See it running' (pods up), not just the create.
- [x] Page 3 (`02-customise-it`): before/after via `oc set env --list` (no GREETING → GREETING set); served before/after also across reach+change pages of the greeting change.

## General
- [~] **Route not ready on forward** → OpenShift "Application is not available" page; waiting + reload fixes. Add a **readiness probe before forwarding** (portal launch flow: gate the redirect on the session/route answering 200). Portal app work (`educates.py`/`app.py`/`launch.html`).
- [ ] **Auth error after reload** — suspected stale/old workshop session that just restarted, token no longer valid. Investigate session/token lifecycle on re-open (oauth handshake vs restarted session pod).
- [x] **Lab durations too high** — undershoot to get more people through the door. Lower `spec.duration` + README + overview "Estimated time" across labs.

## Durations — proposed lower values (was → new)
- a00 10m→5m · a01 20m→15m · a02 30m→20m · a03 30m→20m · a04 30m→20m · a05 30m→20m · a06 30m→20m · a07 20m→10m · a08 25m→15m
