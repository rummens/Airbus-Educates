# Project: DCS Academy (Educates course)

Interactive learning academy for the **Digital Container Service (DCS)**, Airbus Defence and Space's on-prem, multi-national (Europe), OpenShift-based container service. Built as Educates workshops.

- Project overview, directory structure, and module map: [README.md](README.md)
- Full course vision, standards, and design principles: [planning/course-brief.md](planning/course-brief.md)
- Curated external references for course subject matter (consult before web search): [planning/resources.md](planning/resources.md)

## Skills

- **airbus-educates-course-design** — course planning: topics, workshop breakdowns, per-workshop plans (in `planning/`).
- **airbus-educates-workshop-authoring** — workshop implementation: YAML, instruction pages, exercise files (in `workshops/`). It owns the detail of the house standards below.

## Course conventions

- **Target:** OpenShift; all commands use `oc`, never `kubectl`.
- **Workshop naming:** `lab-{code}-{name}`, code = module letter + two-digit number (e.g. `lab-a01-what-is-dcs`).
- **Base images:** `dcs-workshop-base` (default) and `dcs-tools`, both in Harbor.
- **Namespace model:** vcluster where the prod/dev distinction must be tangible.

## House standards (this fork)

- **Param trio** in every `workshop/config.yaml`: `product_name` = "Digital Container Service (DCS)", `dcs_registry` (Harbor project, placeholder), `dcs_docs_base_url` (DCS docs portal, placeholder).
- **Air-gapped images:** every image from Harbor (`$(image_repository)` / `{{< param dcs_registry >}}`); no external registries.
- **Mandatory introduction page** on every workshop.
- **Doc links (hybrid):** standard constructs → upstream docs; DCS-specific concepts → `{{< param dcs_docs_base_url >}}` + inline blurb. DCS concepts are defined once in the authoring skill's `dcs-concepts-reference`.
- **Assessment:** examiner step checks + a knowledge check per workshop.
- **Variablize everything** — no hardcoded registries, domains, routes, namespaces, or versions.

## Design principle

Fully guided experience via Educates clickable actions — learners click, they don't type by hand. See [planning/course-brief.md](planning/course-brief.md).
