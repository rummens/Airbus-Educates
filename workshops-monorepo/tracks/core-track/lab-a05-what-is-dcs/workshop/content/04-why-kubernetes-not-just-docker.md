---
title: Why Kubernetes, Not Just Docker?
---

You now know a container is a running instance of an image. [Docker](https://docs.docker.com/get-started/)
can start one container on one machine — which is fine on your laptop. But a shared
platform running many teams' applications needs much more than "start a container here."
That's what [Kubernetes](https://kubernetes.io/docs/concepts/overview/) — and OpenShift,
which builds on it — adds.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/kubernetes
```

Kubernetes adds four things a shared platform needs:

## Scheduling

You say *"run this,"* and the platform decides **where** it runs, picking a machine with
room to spare. You never hand-place a workload on a specific server.

*With plain Docker:* you SSH to a chosen host and run `docker run` there yourself —
nothing finds a machine with room or balances across hosts.

## Self-healing

If a container crashes, the platform **restarts or reschedules it automatically** —
usually before anyone notices. If a machine fails, the platform moves your work to another one.

*With plain Docker:* a crashed container stays down until someone runs `docker run`
again. `--restart` helps on one host, but if that host dies, so does your app.

## Scaling

Need more copies to handle load? You **ask for N replicas**, up or down, and the
platform starts or stops copies to match. You do not clone VMs or redeploy by hand.

*With plain Docker:* more copies means running `docker run` by hand N times and wiring
up your own load balancer in front of them.

## Declarative desired-state

You **describe the end state you want** ("three copies of this image, reachable here")
and the platform **continuously reconciles** the cluster toward it.

**Declarative** means the desired state is written down, and the platform keeps making it
true.

*With plain Docker:* `docker run` is fire-and-forget — there is no record of what
*should* be running, so nothing notices or repairs drift when reality changes.

## Next

Next, a short tour of your session and the `oc` commands you use in every lab.
