# Course Brief Reference

The course brief (`planning/course-brief.md`) is the highest-level planning artefact for a course. It captures the course vision, scope, audience, and design principles established during the initial planning phase. Everything that follows — topics, workshop breakdowns, per-workshop plans — flows from the decisions made here.

## When to Create

The course brief is the first document created when starting a new course. It should be written before brainstorming specific topics, as it provides the framing that guides topic selection. For focused courses (1–3 workshops), the course brief can be lighter — a few paragraphs establishing vision, audience, scope, and design principles. The full section structure described below is recommended for standard and comprehensive courses.

## Standard Sections

### Course Vision

Describe what the course covers and the overall learning goals. This should answer:

- What is the subject matter?
- How does the course progress (e.g., from fundamentals to advanced)?
- For courses with multiple modules: is there an organising theme or narrative thread that connects the modules?
- What makes this course distinctive or valuable?

Keep this concise — a few paragraphs, not pages. For focused courses, the vision can simply describe what the workshop(s) will teach and why, without needing to describe inter-module connections. The vision guides topic selection but does not enumerate topics (that happens in `course-topics.md`).

### Target Audience

Describe who the course is for:

- What experience levels does the course accommodate? (beginner, intermediate, advanced, or a progression)
- What prior knowledge is assumed at entry points?
- How does the course support different entry points for different experience levels?

If the course uses a core/elective model, explain how different audiences navigate it (e.g., beginners start at the beginning, experienced learners skip early core workshops). For focused courses, a simple statement of who the workshop(s) are for and what prior knowledge is assumed is sufficient.

### Product/Service

*Include this section for all courses (house standard).*

Record the product or service the course is delivered under. This exact string becomes the default `product_name` variable used by every workshop in the course (rendered on each workshop's introduction page via `{{< param product_name >}}`). Individual workshops can override it, but the course default lives here so the whole course reads consistently.

- **Product/service name** — the full name (e.g. "ACME Container Platform")
- **Short form** *(optional)* — a short label for inline use (e.g. "ACME"), mapped to `product_short`

### Delivery Platform

State that the course is delivered on the Educates training platform, targeting **OpenShift**. Include:

- Each workshop is a self-contained Educates workshop providing an interactive browser-based environment
- The environment includes an embedded terminal, VS Code editor, and step-by-step instructions
- Commands target OpenShift via the `oc` CLI

This section is brief and largely the same across courses, but it establishes the platform context for readers who may not be familiar with Educates.

### Platform Standards

*Include this section for all courses (house standard).*

State the standards that apply to every workshop in the course. These are enforced in implementation by the airbus-educates-workshop-authoring skill; recording them here keeps plans and workshops aligned:

- **OpenShift/`oc`** — all commands use `oc`, never `kubectl`; prefer Routes / the session proxy over raw Ingress
- **Mandatory introduction page** — every workshop opens with a `00-workshop-overview.md` overview (product framing, objectives, prerequisites, environment, time/difficulty)
- **Documentation links (hybrid)** — standard Kubernetes/OpenShift constructs link to official upstream docs; DCS-specific concepts link to the DCS docs portal via `dcs_docs_base_url` with an inline blurb (air-gapped)
- **Variablization + param trio** — no hardcoded registries, domains, routes, namespaces, or versions; every workshop declares `product_name`, `dcs_registry`, and `dcs_docs_base_url` so it redeploys without a rebuild
- **Air-gapped images** — all images from Harbor (`$(image_repository)` / `dcs_registry`); no external registries; workshops use the shared `dcs-workshop-base` / `dcs-tools` images
- **Assessment** — every command has an Educates examiner verification (forming an automated test pipeline) and every workshop ends with a knowledge check
- **Multi-namespace realism** — use a virtual cluster where the prod/dev namespace model must be tangible

Record the concrete values for this course here: the product name, the Harbor project (`dcs_registry`), the DCS docs base URL (placeholder acceptable), and the shared base-image names.

### Course Structure

*Include this section for all courses. Every course has at least one module. For focused courses with a single module, this section can be brief — a sentence or two describing the module's theme.*

Provide a high-level overview of how the course is divided into modules. For each module:

- A title or theme
- A brief description (1-3 sentences) of what the module covers
- How it relates to other modules (builds on, extends, applies, etc.)

This is an overview, not a detailed breakdown — the detailed breakdown happens in the workshop breakdown files.

### Navigation Model

*Include this section for standard and comprehensive courses. For focused courses (1–3 workshops), a navigation model section is not needed — workshops are standalone or follow a simple linear order.*

Describe how workshops relate to each other and how learners navigate the course.

For courses using the **core/elective model** (recommended for comprehensive courses where learners pick and choose):

- **Core workshops** form the mandatory learning path within each module. They build directly on each other and cannot be skipped.
- **Elective workshops** branch off the core at defined points. They share core prerequisites but are independent of each other. Learners can take them in any order, skip them, or return later.
- Each workshop states its prerequisites explicitly.

For **linear courses** (where all workshops are taken in sequence):

- Describe the expected sequence and any flexibility points.

Include indicative prerequisite chains if the course structure is complex enough to benefit from them — which topics form strict chains, which are peers.

### Design Principles

State the design principles that apply to all workshops in the course:

**Hands-on guided experience** (recommended default for Educates courses): Every workshop should have a meaningful hands-on code component. The recommended approach is to drive all code interaction — viewing, running, and modifying — through Educates clickable actions, so learners can focus on concepts rather than mechanics. However, the course author may choose a less guided approach where learners type commands or code themselves, depending on the audience and learning goals. The course brief should state which approach the course will use and why.

**Conceptual material handling**: Conceptual or scene-setting material should be folded into neighbouring practical workshops as introductory context, not left as standalone text-only workshops. Topics that are primarily conceptual can be restructured as "observe and diagnose" exercises.

Add any course-specific design principles relevant to the particular subject matter.

### Scope and Growth Path

*Include this section for focused and standard courses. Optional for comprehensive courses.*

Record the course scope (focused, standard, or comprehensive) and, for non-comprehensive courses, suggest directions for future expansion. This supports users who build courses incrementally — starting with a few workshops and adding more over time.

Example: "This focused course covers X with 2 workshops. If expanded, natural next steps could include Y (which could become a third workshop building on Workshop A02) and Z (which could form the basis of a second module covering advanced topics)."

The growth path is not a commitment — it captures ideas that the user can act on later when they return to extend the course.

## What Not to Include

The course brief focuses on course content and structure. The following are out of scope:

- **Deployment infrastructure** — Index sites, learning management systems, authentication services, and hosting are separate concerns.
- **Specific topics or workshops** — The brief describes the shape of the course, not its detailed contents. Topics are enumerated in `course-topics.md`.
- **Implementation details** — Workshop YAML configuration, clickable action syntax, and Educates platform specifics are handled by the educates-workshop-authoring skill.
