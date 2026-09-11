---
title: The Mental Model
---

Start from the file you already know. The compose file for `hello-dcs` sits in your
exercises directory — an **image**, a **port mapping**, an **environment variable**, and a
few lines that only make sense on a single Docker host.

Everything in it has a Kubernetes equivalent. This page names them before you touch any YAML.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/mental-model
```

## Read the source of truth

```editor:open-file
file: ~/exercises/docker-compose.yml
```

The same file, from the terminal, so the check below can confirm it is there to work with:

```terminal:execute
command: cat docker-compose.yml
```

```examiner:execute-test
name: verify-compose-readable
title: Verify the compose file is present in your session
timeout: 10
retries: 3
delay: 2
```

{{< note >}}
**📌 The colours on that button.** A check is **amber** while it waits or runs, **green**
when the state it describes is true, and **red** when it is not — red means fix the step
above, then click again.
{{< /note >}}

## Same ideas, different shape

The biggest shift is not *what* the objects do. It is *how* you describe them.

**Imperative** — `docker run` and `docker compose up` tell the Docker daemon what to do
right now, in order.

**Declarative** — Kubernetes takes the state you *want* and keeps working to make reality
match it. That is why a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) that
dies is **replaced** without you running anything. Nobody re-ran a command; the platform
re-converged on the declared state.

{{< note >}}
**💡 Tip:** if you have used compose's `restart: always`, self-healing is not new to you.
Kubernetes applies the same idea to every object, not just to container restarts.
{{< /note >}}

## The mapping

|  | Docker / Compose | Kubernetes on {{< param product_short >}} |
|---|---|---|
| **Runs your image** | a container (`docker run`, or one compose service) | a [Pod](https://kubernetes.io/docs/concepts/workloads/pods/), managed by a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) |
| **Publishes a port** | `ports: "8080:8080"` — binds the Docker host's port | a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) — a stable in-cluster name, not a host port |
| **Sets config** | `environment:` / `-e KEY=value` | a [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/), referenced as env vars |
| **Persists data** | `volumes:` / `-v host:container` | a [Volume](https://kubernetes.io/docs/concepts/storage/volumes/) backed by a PersistentVolumeClaim — never a host path |

![Docker world mapped onto Kubernetes objects](mental-model.svg)

## Next

You will fill in and apply the three manifests already sitting in `~/exercises` —
`deployment.yaml`, `service.yaml`, `configmap.yaml` — one per row of that table, in the
order the compose file lists them.
