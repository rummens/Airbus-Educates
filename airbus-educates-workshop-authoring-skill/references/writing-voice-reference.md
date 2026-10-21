# Writing Voice Reference — written, not generated

**House rule: learner-facing text reads like a trainer wrote it, not like a model generated it.**
A learner rated a lab down "because of the AI feeling", and a review of every track in
October 2026 found ~570 sentences that still read machine-written after a first plain-voice
pass. The tells below are the ones that review counted, most frequent first. Each is a
habit, not a single word, so a find-and-replace does not fix it — rewrite the sentence.

**Applies to:** instruction pages, slides, `README.md`, `workshop.yaml` `description` and
`academy.dcs/details`, `track.yaml`, ConsoleLab step text (`title`/`description`/`completionText`),
examiner script messages, and exercise files the learner opens.

The fix is almost always the same: **state the fact, in a normal sentence, once.** Keep the
facts, the code, the links and the params; change only the wording.

## The tells

| # | Tell | Looks like | Write instead |
|---|---|---|---|
| 1 | **Reveal / antithesis formula** — a contrast that exists for rhythm, not information | "A Service is not one thing." · "It is a replacement, not a restart." · "The fix is not a smaller budget. It is…" · "assumes the concepts, not the clicks" | The positive statement: "OpenShift replaces the Pod; it does not restart it in place." Keep a contrast only when the learner would otherwise believe the wrong half ("base64 is encoding, not encryption" stays). |
| 2 | **"That is the point" framing** | "…is the whole point." · "That is the whole difference." · "The trick:" · "The answer:" · "The catch:" · "Here's the thing" · "That is what X is for." | Delete the frame; keep the fact it introduces. |
| 3 | **Mic-drop fragments and punchline closers** — one- to four-word sentences or paragraphs for effect, usually ending a page or section | "Refused." · "Nothing." · "That's persistent storage." · "One character off." · "Boring, and usually right." · "Build few." | A full sentence that says what happened: "PROD refuses the Pod and names the policy." |
| 4 | **Personification** — objects that think, speak, remember or decide | crash "explains itself" · app "has something to say" · Job "reaches a verdict" · the cluster "remembers" · "makes reality match" · "make the app work for its living" · "puts the work where it belongs" · "they outlive you" | Literal verbs: shows, logs, records, exits with code 0, creates, keeps. |
| 5 | **Triplets and negative triplets** | "no SSH key, no VPN, no local git clone" · "No error, no data, no clue" · "write it, build it, run it" · "same registry, same SCC, same quota" | List the items once, plainly, or as a bulleted list if there really are three things to act on. |
| 6 | **Symmetric paired sentences** | "Metrics tell you that… Logs tell you what…" · "Scale-up provisions. Scale-down does not delete." · "The console wins for X. The CLI still wins for Y." | One sentence with "and"/"but", or a two-row list. |
| 7 | **Dramatic em dash** — a dash used as a pause before a punchline | "PROD keeps running — which, after a promotion, is the whole idea." | A full stop, a colon, or parentheses. Dashes are fine in `**term** — definition` list items. Max one per paragraph otherwise. When removing a dash, **do not leave a comma splice** ("stop the watch, it is served its purpose" is wrong — use a full stop). |
| 8 | **Teaser hand-offs and meta narration** | "…and the next tab is where it is kept." · "the interesting one" · "the one people are surprised by" · "which brings us to" · "as promised" · "notice that" · "With X understood, it is time to…" · "You have now…" | Say what the next step does: "Open the ReplicaSets tab to see the object between the Deployment and its Pods." Drop transitions that only announce. |
| 9 | **Rhetorical question set-ups** | "## Why does this matter?" · "Why not just let teams push to PROD?" followed by the answer | A heading that names the topic ("## What changes in PROD"); a statement instead of the question. A genuine learner question in a Q&A or knowledge check is fine. |
| 10 | **Intensifiers and filler** | genuinely · actually · simply · just (as filler) · really · for real · precisely · exactly · completely · honest | Delete. "just" is fine when it means "a moment ago" ("the Pod you just created"). |
| 11 | **Buzzwords** | seamless · robust · powerful · leverage · empower · unlock · journey · landscape · delve · harness · streamline · elevate · magic · under the hood · game-changer · at its core · in a nutshell · hands-on · deep dive · first-class | The plain word, or nothing. |
| 12 | **Repeated taglines and templated catalog copy** — one hook line reused in README, overview, intro slide and summary; every card in a track opening with a bold aphorism; every description sharing one shape | "Every lab so far…" ×3 · "the easy half" ×4 · "Your feedback directly shapes…" on 8 pages · console cards all "You did X in Y. This lab walks the same…" | Say a thing once, where it is needed. Catalog descriptions start with **what the learner does** and differ in shape from card to card. Shared boilerplate belongs in one template/banner, not pasted into every lab. |
| 13 | **Cute idiom / catchphrase** | "somebody pays for" · "yours to babysit" · "lives happily in DEV" · "the map / the territory" · "earns its keep" | The literal statement: "costs storage", "you must monitor it", "runs in DEV". |

VM-world analogies and the sanctioned call-out labels (`**💡 Tip:**`, `**⚠️ Watch out:**`,
`**📌 …:**`, `**⏳ …:**`) are **not** tells — they are house style. See
[content-depth-reference.md](content-depth-reference.md#use-analogies--and-taper-them-with-skill-level)
and [content-formatting-reference.md](content-formatting-reference.md).

## Examples (real, from the October 2026 review)

| Before | After |
|---|---|
| Now make the app work for its living. The workshop image ships a small load tool… | Next, put the app under load. The workshop image includes a small load tool… |
| Nothing. The Pod is gone, the node's file went with it… | The command returns no logs: the Pod is gone, and its log file on the node was deleted with it. |
| That is the point — the Pod churned, the storage did not. | The Pod was replaced, but the data on the volume is still there. |
| Green means the step really worked — not "the page scrolled past", but… | A green check means the step's result is on the cluster. |
| What you did not have to write is the point. | You did not write the StatefulSet, Services or Secrets; the Operator created them. |
| The mapping is the easy half. The last step is the one that changes how you build images. | The last step matters most for your own images: it lists what DCS refuses, and why. |

## Accuracy beats rhythm

Punchlines are where facts go wrong, because they are written for the sound. The review
found "One character off." for `conf` vs `config` (two characters) and "runs in exactly one
of those places" for a root image (it runs on a laptop and on plain Kubernetes). When
rewriting a punchline, re-check the fact it carries.

## Self-check before you finish a page

1. Run `test/workshops/style_check.py <lab>` — it flags the mechanical tells (buzzwords,
   intensifiers, "the point" framing, punchline-fragment paragraphs) as warnings, and fails
   on `docs.openshift.com` links and complex commands with no breakdown. Comma splices,
   personification and reveal formulas need the read-aloud pass below.
2. Read the page aloud. Any sentence you could delete without losing a fact is the finding.
3. Read the page's last paragraph twice — closers are where most tells sit.
4. Grep the lab for its hook line: if it appears in more than one file, keep one.

## Checklist

- [ ] No reveal formulas, "the point" framing, or mic-drop fragments (tells 1–3)
- [ ] No personified objects (tell 4); no decorative triplets or paired sentences (tells 5–6)
- [ ] Em dashes only in `**term** — definition` items or ≤1 per paragraph; no comma splices left where a dash was removed (tell 7)
- [ ] No teaser hand-offs, meta narration, rhetorical set-ups (tells 8–9)
- [ ] No intensifiers or buzzwords (tells 10–11)
- [ ] Each hook/tagline appears once per lab; catalog descriptions are not templated (tell 12)
- [ ] `style_check.py <lab>` reports nothing, or each remaining hit is a deliberate, factual contrast
