<!-- Edit this file: one slide per line of three dashes. Give a slide a deep-link id with an id-comment on its own line. Markdown: headings, - lists, **bold**, `code`, fenced code, ![alt](img), [text](url). -->

<!-- id: intro -->
# Logs

Reading Pod logs with `oc`, and where that stops being enough.

**In this lab:** where logs live · reading them with intent · the logs of a crash · where `oc logs` stops · the aggregated store.

Digital Container Service · DCS Academy

---

<!-- id: where -->
## Where logs live

A container has no log file to configure. It writes to stdout, and the platform takes it from there.

- The runtime writes it to a **file on the node**; `oc logs` reads that file.
- A **collector** reads the same file and ships it to the central store.
- Nothing parses your lines on the way — whatever structure they have is the structure you gave them.
- Do **not** write logs to a file inside the container: nothing collects it and it dies with the Pod.

![A container writes to stdout; the runtime writes it to a node file that oc logs reads and rotation discards, while a collector ships it to a store that outlives the Pod](log-path.svg)

---

<!-- id: reading -->
## Reading with intent

`oc logs <pod>` prints everything since startup, which on a busy app is unreadable. The flags are what make it useful.

```
oc logs deploy/hello-dcs --tail=20
oc logs -l app=hello-dcs --tail=5 --prefix
oc logs -l app=hello-dcs --since=5m
oc logs -f deploy/hello-dcs
```

- `deploy/…` reads **one** Pod. `-l` reads them all, and `--prefix` is what tells them apart.
- `--since=5m` is the incident flag: what was it saying five minutes ago.
- `-f` follows live, and ends when the Pod does.

---

<!-- id: crash -->
## The logs of a crash

The container that failed has already been replaced, and the new one's log does not show the error.

```
oc get pods -l app=flaky          # RESTARTS climbing
oc logs <pod> --previous --tail=20
```

- **`--previous`** reads the **last terminated** container in that Pod.
- That is where the fatal line is: *cannot reach the database at db.internal:5432*.
- Run it first on any crash-looping Pod.
- Between restarts there may be no running container to read at all.

---

<!-- id: aggregation -->
## When the Pod is gone

Delete the workload and `oc logs` has nothing to read. The central store keeps lines after the Pod and node are gone.

```
{namespace="my-team-dev", app="hello-dcs"} |= "FATAL"
sum by (pod) (rate({namespace="my-team-dev"} |= "FATAL" [5m]))
```

- A **collector** per node ships every line to a **LokiStack**, with labels.
- **LogQL**: select by labels first, then filter lines — `|=`, `!=`, `|~`.
- The same `rate()` and `sum by` as metrics, over log lines.
- Authorized per namespace, exactly like metrics.
- **Never log a secret.** The central store keeps it for the full retention period, readable by everyone entitled to the namespace.

---

<!-- id: next -->
## What's next

You can read logs by workload and time window, recover a crashed container's output, and you know where `oc logs` stops.

Metrics and logs both stop at your namespace boundary. **RBAC & Tenancy** is where that boundary is drawn, and **DEV vs PROD Namespaces** is what the platform enforces on top of it.

Digital Container Service · DCS Academy
