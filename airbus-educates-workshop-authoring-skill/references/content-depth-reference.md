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
- [ ] Depth was not sacrificed to hit a time target; long topics were split instead
