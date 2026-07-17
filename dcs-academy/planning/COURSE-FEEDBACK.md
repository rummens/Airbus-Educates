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
- [x] Add **slides** to this lab — done: a01 has a `slides` app enabled in `workshop.yaml` and a `workshop/slides/index.html` deck (self-contained, air-gapped, no reveal.js CDN).
- [x] Page ~5 (`04-why-kubernetes-not-just-docker`): reframed 4 VM-world analogies → plain-Docker contrasts; should compare **K8s vs Docker** (not containers vs VMs). Reframe: what Docker-on-one-box can't do that K8s does.
- [x] **Move A01 toward the END of the module** — done via the low-churn path: `academy.dcs/order: "55"` sorts a01 after the hands-on quick-wins (a02=20, a03=30, a04=40, a05=50), before the orientation labs (a06=60…). Dir name kept; a01 overview already says "if you'd rather start by doing, jump to Deploy Your First App."

## Lab 2 — lab-a02-deploy-first-app
- [x] Page 2 (`01-deploy-it`): added `oc get deployment,pods` 'See it running' (pods up), not just the create.
- [x] Page 3 (`02-customise-it`): before/after via `oc set env --list` (no GREETING → GREETING set); served before/after also across reach+change pages of the greeting change.

## General
- [x] **Route not ready on forward** → done. `k8sclient.session_route_ready` now two-stage-gates the redirect: Route must be **Admitted** AND HTTP-probe the host (a router 503 "Application is not available" = not ready; 200/401/3xx = serving). `launch.html` also keeps a 2.5s settle. No-RBAC falls through to the probe (never fails open early). Tests updated + a new `_route_http_ok` test; 90% gate holds.
- [x] **Auth error after reload** → done. Root cause: the launch redirected before the server-side **claim** established the portal session cookie the session-host oauth handshake needs → first load 401'd (a reload fixed it). `launch.html` now `await`s the claim (`claimDone`) before redirecting.
- [x] **Lab durations too high** — undershoot to get more people through the door. Lower `spec.duration` + README + overview "Estimated time" across labs.

## Durations — proposed lower values (was → new)
- a00 10m→5m · a01 20m→15m · a02 30m→20m · a03 30m→20m · a04 30m→20m · a05 30m→20m · a06 30m→20m · a07 20m→10m · a08 25m→15m

---

# Round 1 verification (2026-07-16)

All `[x]` items above **verified in-repo**: durations match the proposed values; a00 has the
evaluator blurb + console-embedding "why"; a01 has image-vs-container.svg on page 3 and the
K8s-vs-Docker reframe; a02 has the before/after (`oc set env --list`).

**Update (2026-07-16, round 2 close-out):** every remaining item above is now closed. The
two portal items (Route-readiness gate, auth-error-after-reload) were already implemented in
the working tree but left uncommitted and un-tested — verified, finished (stale `app.py`
comment fixed, portal tests updated to the new two-stage behaviour + new `_route_http_ok`
test), and marked done. Both `[?]` decisions were already satisfied by prior work (a01 slides
deck exists; a01 `order=55` sorts it late) — marked done, no further decision needed.
⚠️ The portal changes can't be validated on CRC (portal crashloops on arm64) — validate on a
real cluster after deploy.

# Round 2 feedback (2026-07-16) — status

## Lab 3 (a03)
- [x] p3 Secret "does not show" — `grep -o '^API_TOKEN='` printed a bare key; replaced with a test-and-report (`set — N chars, value hidden`).
- [x] p4 show the ConfigMap change — added visible `printenv GREETING` before (old) and after (new) the rollout.
- [x] p6 `oc logs … || echo "(…)"` not detected — simplified to the plain `oc logs`; interpretation moved to prose.

## Lab 4 (a04)
- [x] External LB is a security requirement, not native K8s — added note on the traffic-chain page.
- [x] p3 Service missing link — linked; also linked the Service bullet in the chain.
- [x] p5 "Application is not ready" tab — root cause: session-proxy ingress had no `host:`, so it targeted the workshop pod. Added `host: hello-dcs.$(session_namespace).svc.cluster.local` + `protocol: http`.
- [x] p6 whitelisted-egress-via-proxy — added note: deny-by-default, approved destinations via managed proxy only when explicitly enabled.

## Lab 5 (a05)
- [x] p2 PersistentVolume missing link — added (PV/PVC now use distinct anchors).
- [x] p3 `/data` Permission denied + "why didn't tests catch it" — root cause: non-root image can't write a root-owned mount. Fix (per author): mount under the image's writable home `/opt/app-root/src/data`. **Test integrity fixed**: the smoke plan was secretly `oc patch`-ing `fsGroup` onto a manifest that lacked it (green over a broken lab); the note now names it a CRC-only shim and flags that real-DCS File-storage write-perms are **not** covered by CRC. ⚠️ validate the mount-path fix on real DCS.
- [x] ephemeral-first demo — new page `02-ephemeral-storage.md` (deploy without storage → write → delete Pod → gone), from the Storage-101 lightning-talk demo; pages renumbered 03/04/05.
- [x] p5 residency wording — reframed to classification level (national vs international/NATO → physically separated disks → dedicated SC), not DE-vs-ES residency.
- [x] p5 S3 "harsh" — reframed: S3 **is** available on DCS, via ITSM request (not self-service), "same platform, different path".

## Lab 6 (a06)
- [x] p3 `-n` clarity — added an explicit explanation that `-n <namespace>` selects the target namespace, before first use.
- [x] p3 verify b unchanged — added a visible side-by-side `oc get deploy` of app-a (0/0) and app-b (1/1) after scaling.
- [x] p5 label readability — output now one label per line (`| tr ',' '\n' | tr -d '{}"'`).
- [x] lifecycle label dev/prod per lab — verified: all Core = `dev`, a04 = `prod` (only Route lab); **a01 was missing it — added `dev`**. Added static test `test/workshops/label_check.py` (wired into CI) that asserts every lab declares it and `prod` ⇔ creates a Route. ⚠️ runtime **injection** onto the session namespace is currently a no-op: the Kyverno propagation policy is disabled because Kyverno is off on OpenShift (see a04 comment + portal `workshopEnvLabel`). Needs a non-Kyverno path if PROD enforcement is turned on.

## General
- [x] Core track all `beginner` — a03/a04/a05 were `intermediate` → `beginner`.
- [x] First page repeats the lab title — every `00-workshop-overview.md` `title` is now the lab's own title, not "Workshop Overview".
- [x] Clearer commands — added first-use flag explanations (esp. `-n` in a06); encoded as a house standard in the authoring skill.

## Skills / prevention (author + planning)
- [x] Authoring skill: intro-page title = lab title; "show the change" (visible before/after) + explain flags on first use (content-depth); keep clickable commands simple (clickable-actions); session-proxy tab → Service needs `host:` (dashboard); non-root writable mount path + no hardcoded fsGroup (openshift); test-integrity / name-the-coverage-gap (local-cluster); egress-proxy + S3 + NATO classification accuracy (dcs-concepts); matching SKILL.md checklist lines.
- [x] Planning skill: core/foundations track = `beginner` (difficulty tracks audience, not topic); a05 plan doc synced to the as-built pages.
