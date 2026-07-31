# DCS Academy — lab catalog

This repo holds the **content of every DCS Academy lab**: the pages you read, the slides,
the exercise files and the checks that confirm a step worked.

You do **not** need this repo to take a lab. Labs run in your browser from the
**DCS Academy portal** (`academy.<your cluster domain>`) — pick a lab, press *Start
session*, and a private environment is created for you. The portal's **Help** page explains
the lab window, the clickable quick actions, tracks and trophies.

Read this repo when you want to see what a lab teaches without starting it, review the
wording of a page, or check which labs exist.

## How it is organised

```
tracks/
  core-track/                          <- a TRACK: one learning path
    track.yaml                         <- the track's title, order and description
    lab-a00-environment-tour/          <- a LAB
      README.md                        <- what this lab is about, in one paragraph
      workshop/
        content/                       <- the pages a learner reads, in page order
          00-workshop-overview.md      <- what you'll learn, prerequisites, duration
          01-quick-actions.md
          …
          98-your-feedback.md          <- the feedback form page
          99-workshop-summary.md       <- recap + knowledge check
        slides/slides.md               <- the slide deck, one slide per lab page
        examiner/tests/                <- the "Verify" checks the lab runs for you
        config.yaml                    <- text substitutions (product name, doc links)
      exercises/                       <- files the lab opens in the editor
      resources/workshop.yaml          <- the lab's technical definition
  dev-track/ · security-track/ · console-track/
```

## Finding your way

- **Tracks** are the learning paths: `core-track` (start here), `dev-track`,
  `security-track`, `console-track`.
- **Lab codes** carry the order: `a00`–`a07` are the Core labs in sequence, `b*` the
  Developer labs, `c*` the Security labs, `u*` the guided console tours. The number in a
  lab folder name is the order it is meant to be taken in.
- **Lab pages** are the numbered files under `workshop/content/`. They are shown in that
  numeric order, `00-workshop-overview.md` first. A page with its own folder (e.g.
  `02-the-dashboard-layout/index.md`) simply keeps an image next to it.
- **Start with a lab's `README.md`** for the summary, then `workshop/content/00-workshop-overview.md`
  for what it teaches and how long it takes.
- **Two kinds of lab.** A *terminal lab* has `workshop/content/` pages and runs in the lab
  window. A *console lab* has no content pages — it is a guided tour of the OpenShift web
  console, and its steps live outside this repo.

## Found a mistake, or something unclear?

Use the **Feedback** tab inside the lab — that is where a rating and a comment reach the
team fastest. A pull request against the page in question works too; wording fixes are
welcome.

## Working on the catalog itself?

Chart, deploy order, authoring standards and the contract a new lab has to satisfy:
**[DEVELOPING.md](DEVELOPING.md)**.
