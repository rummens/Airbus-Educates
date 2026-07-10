# DCS Academy

Interactive learning academy for the **Digital Container Service (DCS)** — Airbus Defence and Space's on-prem, multi-national (Europe), OpenShift-based container service. Delivered as [Educates](https://educates.dev/) workshops.

> This is the **course source** (planning + workshops). It is separate from the deployment charts in the parent repo. It can be split into its own repository later; the skills assume `planning/` and `workshops/` live at this course root.

## Layout

```
dcs-academy/
├── planning/            # Course design (see planning/course-brief.md)
├── workshops/           # Educates workshop implementations (created per plan)
└── scripts/
    └── collect-images.sh   # Emit the image manifest for Harbor mirroring
```

## Structure

Shared **Foundations** core module (everyone), then role tracks branch as electives:

| Module | Track | Audience |
|---|---|---|
| A — Foundations | core | everyone |
| B — Developer | elective | app developers |
| C — Security & Compliance | elective | security & compliance |
| D — Architect / Onboarding | elective | architects, new joiners |
| E — Observability | elective (cross-track) | dev + architect |

See [planning/course-brief.md](planning/course-brief.md) for the full vision, standards, and module map.

## Skills

- Course planning: `airbus-educates-course-design`
- Workshop implementation: `airbus-educates-workshop-authoring`

## Standards (enforced by the authoring skill)

OpenShift/`oc` · air-gapped images from Harbor · mandatory intro page · hybrid doc links (upstream for standard constructs, DCS docs portal for DCS concepts) · full variablization via the param trio (`product_name`, `dcs_registry`, `dcs_docs_base_url`) · examiner checks + knowledge check per workshop · vcluster for the prod/dev namespace model.
