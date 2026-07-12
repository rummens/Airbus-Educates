# lab-b06-dev-spaces — Cloud Development with OpenShift Dev Spaces

Developer-track (Module B) workshop. The learner develops *on* DCS: launches an in-cluster
browser IDE from a devfile (Harbor UDI), changes and runs the sample app inside the cluster,
and learns the boundary between the Educates editor, Dev Spaces, and `oc apply`.

- **Track:** Developer (`academy.dcs/track: dev`), order 60 · **Difficulty:** intermediate · **Duration:** 45m
- **Prerequisites:** B01 (Deploy Your First App); A09 (Operators) for the install/consume framing.
- **Session:** native OpenShift namespace (no vcluster) — Dev Spaces is a platform-installed service the session consumes.

**Delivery gate:** live steps require a pre-installed Dev Spaces instance + a Harbor-mirrored
UDI. Set the Helm value `devSpacesUrl` to surface the **Dev Spaces** dashboard tab; leave it
unset and the workshop degrades cleanly to an annotated, screenshot-driven concept walkthrough
(examiner checks that can't run live become knowledge checks).
