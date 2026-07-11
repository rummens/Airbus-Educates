# Content Depth Reference

**House rule: workshops teach concepts, they do not just script commands.** A learner who finishes a workshop should understand *what* each thing is, *why* it exists, and *how* it relates to the others — not merely have clicked through a sequence. Thin "run this, now run this" content is the most common failure mode; this reference is the standard that prevents it.

The benchmark is the Educates reference course `lab-k8s-fundamentals` (~16 pages for a single fundamentals topic): one concept per page, each with real explanation.

## The standards

### 1. One concept per page

Give each concept its own page. Do not cram Deployment + Service + scaling + logging onto one page. Granular pages (a dozen or more for a foundational workshop) read better, checkpoint better, and let the examiner verify each concept independently. A page title names one idea (`Replicasets and Pods`, `Service Networking`, `Replicas and Scaling`).

### 2. Explain what / why / how — before and around the command

Every concept page leads with explanation, not a command. Cover:

- **What** it is, in plain language.
- **Why** it exists — the problem it solves. (E.g. *"A Pod's IP changes when it is recreated, so you cannot rely on it; a Service gives a stable address and load-balances across Pods."*)
- **How** it relates to other concepts — ownership, templates, lifecycle. (E.g. *"A Deployment is a template for a ReplicaSet, which is a template for Pods; delete the Deployment and the ReplicaSet and Pods go with it."*)
- **Trade-offs / production nuance** — imperative vs declarative, why to keep config in git, why not to edit a ReplicaSet directly, when the default is wrong.

The command is the *demonstration* of the concept, not the content itself. A page that is 80% prose and 20% command is usually right for a concept page.

### 3. Show the expected output

After a command, show what the learner should see, and explain it:

````markdown
```terminal:execute
command: oc get all -o name -l app=blog
```

You should see output similar to:

```
pod/blog-6b8999855c-6jjhj
deployment.apps/blog
replicaset.apps/blog-6b8999855c
```

Although you only created the Deployment, it created a ReplicaSet, which created the Pods…
````

Expected output lets a learner confirm success and understand what the command reveals. Never leave a command's result to the imagination.

### 4. Explain flags and options

When a command uses a non-obvious flag, say what it does (`--dry-run=client` shows what *would* be created and validates without creating it). Point learners at `--help` / `oc explain` so they can self-serve.

### 5. Build progressively; use a real application

Prefer a coherent, realistic sample application carried across the workshop over throwaway snippets. A strong pattern (from the reference course): deploy the whole app once to show the goal, delete part of it, then rebuild it piece by piece so each concept is motivated by the app's needs. Evolve the manifests in versioned steps (v1 → v2 → …) as concepts are added.

### 6. Demonstrate dynamic behaviour with split terminals

For behaviour that unfolds over time (self-healing, rollout, scaling), use the split terminal: `watch` the resource in one terminal, cause the change in the other, and narrate what the learner sees. Static output alone does not convey that Kubernetes *reacts*.

### 7. Cover the concept completely — don't skip the foundational ones

A fundamentals workshop that omits labels/selectors, resource querying, ownership relationships, logs, or exec is incomplete, however tidy. When scoping, list the concepts a competent user of the topic needs and make sure each is taught. It is better to split into more workshops than to drop concepts.

## Depth over brevity (reconciling with workshop length)

The 20–60 minute sizing target is a guide, not a licence to thin content. When full, well-explained coverage of a topic runs long:

- **Split into multiple sequential workshops** — each still deep — rather than compressing explanations out.
- A dense foundational topic may legitimately run 60–90 minutes; that is preferable to a 25-minute workshop that only scripts commands.
- Never drop the *why* to hit a time box. If something must give, narrow the scope (fewer concepts, taught well), not the depth per concept.

## Use analogies — and taper them with skill level

Ground new abstractions in something the learner already knows. For DCS's audience, the **virtual-machine world** is the richest source: a container vs a VM, a Deployment vs a VM template/scale-set, a Service vs a load-balancer VIP, a namespace vs a resource pool/tenant. A one-line analogy before the precise definition makes a concept land.

**Taper analogies as courses get more advanced.** Beginner Foundations content should lean on analogies heavily; intermediate content uses them sparingly for genuinely new ideas; advanced content mostly drops them (the learner now thinks in the domain's own terms, and over-analogizing becomes noise). As a rule of thumb: lots in Module A, few by the track electives, almost none in advanced material.

Keep analogies honest — note where they break down (a container is *not* a lightweight VM; it shares the host kernel). A misleading analogy is worse than none.

## Diagrams and images — teach the structure visually

Some concepts are inherently structural or relational and are far clearer as a picture than as prose. **Add a diagram wherever a relationship, flow, or hierarchy is being taught**, e.g.:

- The **Deployment → ReplicaSet → Pod** ownership chain (A02) — a boxes-and-arrows diagram makes the "who owns/creates what" instantly obvious.
- **Service → Pods** label-selector routing; the **Service → Route → Load Balancer** request path.
- The DEV/PROD namespace lifecycle and promotion.

Practical notes:
- Author diagrams as **SVG** in the page bundle (air-gapped: local, not external), referenced with `{{< baseurl >}}` or a relative path — see [images-in-workshop-pages.md](images-in-workshop-pages.md).
- One clear diagram per structural concept beats a wall of text. A02 in particular should have several (ownership chain, service routing).
- Screenshots help for UI steps (console/editor), but prefer diagrams for concepts.

## Support all learning styles

Every concept page should offer more than one way in, so visual, verbal, and hands-on learners each get traction:

- **Verbal/reading** — the what/why/how prose and expected output.
- **Visual** — a diagram of the relationship (above) and, where relevant, a screenshot.
- **Relational** — an analogy to something known (the VM world).
- **Kinesthetic** — the clickable action the learner runs, and the end-of-workshop challenge.

Not every page needs all four, but a foundational concept should hit at least the prose + a visual or analogy + the hands-on action.

## Estimating duration realistically

Do not over-estimate. Learners move through guided, clickable content faster than the page count suggests — most click through a page in **~2–4 minutes**, and reading-only pages faster. Estimate roughly `pages × ~3 min` plus real wait time (image pulls, rollouts), then round to a friendly figure; when unsure, err **lower** — an over-long estimate deters learners. A ~10-page guided Foundations workshop is typically **30–40 minutes**, not 60+. Validate against a real click-through when you can, and correct the estimate to what it actually took.

## Anti-patterns (reject these)

- A page that is a list of commands with one sentence each.
- "Run this command" with no explanation of what it does or why.
- No expected output shown.
- Multiple unrelated concepts crammed onto one page.
- Skipping foundational concepts because they are "obvious."
- Cutting explanation to stay under a time target.

## Checklist

- [ ] Each page covers a single concept, named in its title
- [ ] Every concept page explains what / why / how, not just steps
- [ ] Trade-offs or production nuance are noted where they exist
- [ ] Expected output is shown and explained after commands
- [ ] Non-obvious flags are explained; `--help`/`oc explain` pointed to
- [ ] A coherent sample application motivates the concepts (progressive build where it fits)
- [ ] Dynamic behaviour is shown with split-terminal `watch` where relevant
- [ ] No foundational concept for the topic is skipped
- [ ] Structural/relational concepts have a diagram (SVG in the page bundle); UI steps have screenshots where helpful
- [ ] New abstractions are grounded in an analogy (VM world for DCS), tapering with skill level
- [ ] Each foundational concept offers multiple ways in (prose + visual/analogy + hands-on)
- [ ] Duration estimate is realistic (~3 min/guided page + waits) and errs low, not inflated
- [ ] Depth was not sacrificed to hit a time target; long topics were split instead
