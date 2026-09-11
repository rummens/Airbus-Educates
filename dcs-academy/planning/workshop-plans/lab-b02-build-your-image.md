# Workshop Plan: lab-b02-build-your-image

## 1. Metadata
- **Name:** `lab-b02-build-your-image` · **Title:** Build Your Image on DCS
- **Duration:** 25m · **Difficulty:** intermediate · **Track:** Build & Run, order `20`
- **Prerequisites (curricular):** *From Docker to Kubernetes*, Core *Deploy Your First App*
- **Status:** New lab, 2026-09-11. Live-verified 19/19.

## 2. The blocker, and how it was removed
The lab was blocked for months on "an air-gapped-reachable git build source". It is built with a **binary build** instead: the learner's own session files are handed to the build with `oc start-build --from-dir`. No git server needs to be reachable, the lab runs anywhere, and the objects and commands are identical to a git-source build. Git sources and their triggers are taught on the rebuild page, where they are the point rather than a dependency.

## 3. Measured before authoring
| Fact | Measured |
|---|---|
| Builds in the Educates session role | **No** — `create buildconfigs/builds/imagestreams` all `no` |
| Docker strategy | gated separately as `builds/docker`; granted explicitly |
| Default Dockerfile name | the strategy looks for **`Dockerfile`**; a `Containerfile` fails with `open /tmp/build/inputs/Dockerfile: no such file or directory` |

The RBAC is granted in `session.objects`, in the session's own namespace, bound to the session ServiceAccount in the **workshop** namespace.

## 4. Design notes
- The BuildConfig is a **written-out manifest**, not `oc new-build`: every field is a decision worth reading, and it must set `dockerStrategy.dockerfilePath: Containerfile`. `oc new-build` stays in a tip as the shortcut that makes the assumption.
- The sharpest page is the rebuild: the second build succeeds and **the running app does not change**. `verify-app-still-old` asserts that, and fails if something restarted the Pod early — the lesson cannot be silently lost.
- The last page names what differs on DCS (base from Harbor, output to the DEV project, promotion by mirror or green catalog) and what does not (every object and command used here).
