# Workshop Plan: lab-b10-dev-spaces

## 1. Metadata
- **Name:** `lab-b10-dev-spaces` · **Title:** Dev Spaces
- **Duration:** 18m · **Difficulty:** intermediate · **Track:** Build & Run, order `100`, **optional** (`academy.dcs/optional: "true"`)
- **Prerequisites (curricular):** *Build Your Image on DCS* — the contrast the lab is built on
- **Status:** Re-authored from the superseded dev-track lab, 2026-09-11. Live-verified 4/4.

## 2. A concept lab, by necessity and by admission
Dev Spaces is operator-provided and the test cluster has no `checlusters.org.eclipse.che` CRD. The lab says which steps need a real instance rather than pretending. What **is** asserted: the devfile exists, sources its dev image from the platform registry rather than a public one, and is a structurally valid 2.x devfile with a container component and commands.

## 3. What was deleted from the quarry
`verify-checluster` exited 0 whatever it found ("either outcome is informative"). That is decoration, not a test — a grader that cannot fail proves nothing. Removed; the "is it installed here" step is content with a note.

## 4. Design notes
- The lab's real contribution is the **four jobs, one repository** comparison: the Educates editor, your laptop, a BuildConfig (git as build source) and Dev Spaces (git as development environment).
- Marked optional so the catalog badges it and the track's required path stays ten labs minus this one.
