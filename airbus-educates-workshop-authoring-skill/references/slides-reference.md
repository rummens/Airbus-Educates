# Slides Reference (house standard)

Every lab ships a **slide deck**: a visual, one-slide-per-page summary of the lab that
learners can skim to recall a topic, and — because the same files are served by the DCS
Academy portal outside a session — re-read later without starting a container. Community
feedback rates the slides highly; treat them as a first-class deliverable, not an add-on.

## What a deck is made of

Two files in `workshop/slides/`:

- **`index.html`** — a self-contained renderer. **Copy it verbatim** from
  [slides/index.html](slides/index.html); do not hand-edit it per lab. It fetches
  `slides.md`, splits it into slides, and renders a small markdown subset. No reveal.js, no
  CDN — DCS is air-gapped. The same file renders identically in the session Slides tab and
  in the portal.
- **`slides.md`** — the content you author. One slide per instruction page, in page order.

Enable the built-in Slides tab in `resources/workshop.yaml`:

```yaml
# Path: spec.session.applications
slides:
  enabled: true
```

## slides.md format

- Slides are separated by a line containing only `---`.
- Give a slide a stable **id** with an id-comment on its own line: `<!-- id: images -->`.
  The id is how a content page deep-links to the slide (below). Use short, stable ids.
- Supported markdown: `#`/`##` headings, paragraphs, `-` bullet lists, `**bold**`,
  `` `code` ``, ```` ``` ```` fenced code blocks, `![alt](image.svg)`, `[text](url)`.
- First slide: a title slide with the lab name and a one-line "In this lab: …" overview.
- Last slide: a short "what's next" close.

## Slides must be genuinely helpful — not bare bullets

A slide that is three terse bullets is not enough (a real piece of community feedback). Each
concept slide should carry:

- a **short explanatory sentence or two** (the idea, in plain language),
- **3–5 bullets** of the key points,
- the **key command(s)** for that page in a fenced block, and where useful the **expected result**,
- the page's **diagram**, when it has one (see below).

Keep it skimmable — bullets and a snippet, not paragraphs of prose. The page holds the full
explanation; the slide is the memorable summary. The renderer scrolls a slide that is taller
than the screen, but prefer slides that mostly fit.

## Put the page's diagram on its slide

If an instruction page has an SVG diagram (a relationship, flow, or hierarchy — e.g.
Deployment → ReplicaSet → Pod), **put the same diagram on that page's slide.** Learners
remember the picture; repeating it on the slide is exactly what makes the deck stick.

Because the session serves slides from `workshop/slides/` (a different root than the content
page bundle), **copy the SVG into `workshop/slides/`** and reference it by filename:

```
![Deployment creates a ReplicaSet, which creates the Pod](deployment-chain.svg)
```

Yes, the SVG then exists twice (in the page bundle and in `slides/`). That is intentional and
simple; if you edit the diagram later, update both copies.

## Linking a content page to its slide — use a clickable action

On each content page, add a jump to that page's slide. **Use a `dashboard:reload-dashboard`
clickable action targeting the built-in `Slides` tab** — it reliably opens the Slides tab
*and* lands on the right slide:

````markdown
Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/<id>
```
````

Do **not** use a plain markdown link like `[…](/slides/#/<id>)` — Educates does not reliably
route it, so it navigates the instructions pane into the deck (renders wrong). The
`reload-dashboard` action is the only reliable way to set a dashboard tab's URL (see
[clickable-actions/dashboard-actions.md](clickable-actions/dashboard-actions.md)). The
renderer reads the `#/<id>` hash on load and scrolls to that slide.

## Serving decks outside a session (portal)

The DCS Academy portal serves each lab's `workshop/slides/` directory at `/slides/<lab>/` via
a git-sync sidecar, and shows an "Open slides" button on the course page. Authors do nothing
extra for this — it works because the deck is self-contained and fetches `slides.md`
relatively. It is another reason to keep the deck self-explanatory (no session context).

## Testing a deck locally

Any static server (the deck fetches `slides.md`, so `file://` will not work):

```bash
cd workshop/slides && python3 -m http.server 8080
# open http://localhost:8080/  — deep-link a slide with http://localhost:8080/#/<id>
```

## Checklist

- [ ] `workshop/slides/index.html` copied verbatim from the skill; `slides.enabled: true` set
- [ ] One slide per instruction page, in order; title slide + "what's next" close
- [ ] Each concept slide has explanation + bullets + command(s) + (where useful) expected output
- [ ] Every page diagram is copied into `slides/` and shown on its slide
- [ ] Each content page links to its slide via a `dashboard:reload-dashboard` action (not a plain link)
- [ ] Each slide has a stable `id`; links use the `/slides/#/<id>` form
