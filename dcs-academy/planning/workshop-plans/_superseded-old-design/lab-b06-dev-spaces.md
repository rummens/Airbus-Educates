# Workshop Plan: lab-b06-dev-spaces

## 1. Workshop Metadata

- **Name:** `lab-b06-dev-spaces`
- **Title:** Cloud Development with OpenShift Dev Spaces
- **Description:** Develop *on* DCS, not just deploy to it — launch a browser-based, in-cluster dev environment from a devfile, change the sample app and run it inside the cluster, all from Harbor-mirrored images on an air-gapped platform.
- **Duration:** 45m
- **Difficulty:** intermediate
- **Type:** Elective (Module B — Developer)
- **Prerequisites:** B01 (Deploy Your First App); A09 (Operators) for the "platform installs it, you use it" framing
- **product_name:** Digital Container Service (DCS)
- **Status:** Planned — [tasks](../tasks.md#module-b--developer) (confirm a Dev Spaces instance + Harbor-mirrored UDI, else deliver as a screenshot concept lab)

## 2. Workshop Configuration

- Terminal: `enabled: true`, `layout: split`
- Editor: enabled (contrast the Educates editor with Dev Spaces)
- OpenShift access: enabled; `security.token.enabled: true`
- Web console: enabled
- Examiner: `enabled: true` (checks adapt to live vs concept delivery — see Design Notes)
- **Extra dashboard tab:** the Dev Spaces dashboard URL surfaced as a session dashboard tab (when live).
- Budget: `medium`
- **vcluster decision:** `false` — native session namespace; Dev Spaces is a platform service the session *consumes*, not something the session installs.
- Workshop image: `dcs-workshop-base`
- Dev image: a **Harbor-mirrored** Universal Developer Image (UDI) referenced from the devfile via `{{< param dcs_registry >}}`.

## 3. Learning Objectives

After completing this workshop, the learner will be able to:

- Explain what OpenShift Dev Spaces is (in-cluster, browser IDEs; upstream Eclipse Che) and why it fits an air-gapped platform.
- Launch (or inspect) a workspace from a `devfile.yaml` pointing at the sample app.
- Make a code change and run the app **inside the cluster** from the workspace.
- Position Dev Spaces vs the Educates workshop editor vs a plain `oc apply` deploy.

## 4. Connection to Previous Workshop

**Already known:** deploy the sample app with `oc` (B01); operators are platform-installed, tenant-consumed (A09); the Educates editor from every prior lab.

**New here:** a *real* on-platform developer environment (Dev Spaces); the **devfile** as the environment spec; the boundary between "the workshop editor" and "the day-to-day tenant IDE."

**Do NOT re-teach:** `oc apply`/deploy (B01); the operator concept (A09) — reference it to explain who installs Dev Spaces.

## 5. Exercise Files to Create

- `exercises/devfile.yaml` — a devfile for the sample app: a UDI/dev component image via `{{< param dcs_registry >}}`, the app repo/source, and a `run` command that starts hello-dcs on 8080. No external devfile-registry references (air-gapped).
- `exercises/README.md` — placeholder + a note on live vs concept delivery.

## 6. Workshop Instruction Pages

- **`00-workshop-overview.md`** — intro + first-time note; frame the question "how do I develop *on* DCS?"; objectives; open `devfile.yaml`.
- **`01-what-is-dev-spaces.md`** — Dev Spaces = in-cluster browser IDE (Eclipse Che upstream), operator-installed by the platform team (recap A09), consistent + policy-compliant + air-gapped. Why it beats a laptop for a regulated, air-gapped platform. DCS-specific concept → `{{< param dcs_docs_base_url >}}/services/dev-spaces`. Examiner: none (concept).
- **`02-the-devfile.md`** — read `devfile.yaml`: components (the Harbor UDI), commands (build/run), the source. Emphasise images come from Harbor via the param — no external registry. Examiner: devfile present and references `{{< param dcs_registry >}}` (static check).
- **`03-launch-a-workspace.md`** — open the Dev Spaces dashboard tab; start a workspace from the devfile; wait for the IDE. **(Concept fallback:** annotated screenshots of the same flow.) Examiner (live): workspace/Pod for the user's workspace reaches Running; (concept): a knowledge check stands in.
- **`04-change-and-run.md`** — in the workspace terminal, edit the app's response string, run it (the devfile `run` command), open the app's port — see the change live, inside the cluster. Compare to B01's `oc apply` loop. Examiner (live): the app in the workspace serves the changed string.
- **`05-dev-spaces-vs-the-rest.md`** — the boundary: Educates editor = *this workshop*; Dev Spaces = *your real tenant IDE*; `oc apply` = *deploy*. When to use which. Examiner: none (concept) + feeds the summary check.
- **`99-workshop-summary.md`** — recap Dev Spaces / devfile / develop-on-DCS. Bridge to Module F (GitLab): clone from your tenant's GitLab straight into a workspace. Check Your Understanding (4–5 Q). End of the Developer track — suggest Modules E (Observability) / F (Operators).

## 7. Terminal Working Directory Tracking

- **Starting directory:** `~/exercises` (Educates terminal).
- **Note:** the *workspace* terminal is a separate shell inside Dev Spaces with its own working directory (the cloned repo). Keep Educates-terminal commands vs workspace-terminal commands clearly labelled in the instructions.
- Patterns (Educates terminal): `oc get checluster -A` / `oc get pods -l ...` to observe the workspace; workspace terminal runs the devfile `run` command.

## 8. Design Notes

- Covers **course-topics idea 11b** (cloud development / Dev Spaces).
- **Delivery gate:** requires a Dev Spaces instance pre-installed by the platform team + a Harbor-mirrored UDI. If unavailable in the test cluster, ship as an **annotated, screenshot-driven concept lab** (guided tour) — the plan's page structure supports both; the examiner checks degrade to knowledge checks in concept mode.
- **Air-gapped, always:** every workspace/component image comes from Harbor via `{{< param dcs_registry >}}`; point Che/devfile at the mirrored registry; no external devfile registries.
- **Boundary clarity is the point:** learners routinely confuse the Educates editor with a real IDE — this lab draws the line explicitly (workshop editor vs Dev Spaces vs deploy).
- Forward hooks: Module F **GitLab** (clone-to-workspace) and **Argo CD/GitOps** (workspace → git → deploy) build on this.
