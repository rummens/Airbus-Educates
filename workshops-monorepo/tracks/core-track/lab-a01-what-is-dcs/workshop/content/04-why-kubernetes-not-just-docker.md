---
title: Why Kubernetes, Not Just Docker?
---

You now know a container is a running instance of an image. [Docker](https://docs.docker.com/get-started/)
can start one container on one machine — which is fine on your laptop. But a shared
platform running many teams' applications needs much more than "start a container here."
That's what [Kubernetes](https://kubernetes.io/docs/concepts/overview/) — and OpenShift,
which builds on it — adds. It's the "why" behind everything you'll do in the next few
workshops.

Here are the four wins that matter most.

## Scheduling

You say *"run this,"* and the platform decides **where** it runs, picking a machine with
room to spare. You never hand-place a workload on a specific server.

*VM-world analogy:* instead of you walking to a rack and choosing which physical host
gets the new VM, a dispatcher finds a free spot for you.

## Self-healing

If a container crashes, the platform **restarts or reschedules it automatically** —
usually before anyone notices. Losing a machine just means your work is moved elsewhere.

*VM-world analogy:* like having an operator who is always watching, and reboots or
re-hosts a failed VM the instant it goes down — without a support ticket.

## Scaling

Need more copies to handle load? You **ask for N replicas**, up or down, and the
platform makes it so. No cloning VMs by hand, no manual redeploy.

*VM-world analogy:* instead of provisioning five more VMs one by one, you say "make it
five" and they appear (and disappear again when you say "make it two").

## Declarative desired-state

This is the big shift. You **describe the end state you want** — "three copies of this
image, reachable here" — and the platform **continuously reconciles reality toward it**.
Contrast that with running `docker run` by hand: that's **imperative**, a one-time
command with no memory. If the container dies, nothing brings it back. Declarative means
the desired state is written down, and the platform keeps making it true.

*VM-world analogy:* instead of a runbook of steps someone has to execute (and re-execute
after every failure), you file the target configuration once and the system keeps the
estate matching it.

## Next

That's the "why." Next, you'll open your session and run your first commands — the start
of the hands-on payoff in the workshops that follow.
