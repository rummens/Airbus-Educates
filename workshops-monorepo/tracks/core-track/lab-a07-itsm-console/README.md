# The ITSM Console — Self-Service on DCS

**Some things you just do. Some things you request. This lab draws the line — and shows you where the requests happen.**

> **Rough draft.** Screenshot-driven tour; the ITSM-console-in-session embedding spike is
> still open, and screenshots are placeholders. Content is complete enough to review.

On DCS you deploy, scale, and configure your own apps with `oc` — but some actions (more
quota, mirroring an image, a new repo, an S3 bucket, a security exception) go through an
**ITSM request**. This short lab names that split, sorts a handful of tasks into the right
bucket, and walks one request — a quota increase — from form to provisioned change.

- **Track:** Core / Fundamentals · Lab 7
- **Audience:** Beginner — you've done A05
- **Duration:** ~10 min
- **Format:** Guided tour + knowledge check (screenshot-driven)
- **Prerequisites:** A05 (What is DCS?).

## By the end of this lab you'll be able to

- Explain that DCS self-service runs through ITSM requests, and where the console is.
- Tell which actions need a ticket vs which are self-service `oc`.
- Describe the request → approval → provisioning loop.
