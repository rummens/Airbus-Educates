# Workshop Plan: lab-o02-logs

## 1. Metadata
- **Name:** `lab-o02-logs` · **Title:** Logs
- **Duration:** 20m · **Difficulty:** intermediate · **Track:** Operate & Observe, order `20`
- **Prerequisites (curricular):** Core *Configure & Troubleshoot Your App*; helpful: *Metrics & Monitoring*
- **Status:** New lab, 2026-09-11. Live-verified 17/17.

## 2. Hands-on half, taught half
- **Hands-on:** `oc logs` done properly — by workload rather than Pod name, across every replica with `--prefix`, bounded with `--since`, followed with `-f`, and then `--previous` to recover a **crashed** container's output. A deliberately failing workload prints a fatal line and exits 1.
- **Taught:** aggregation. CRC cannot host a LokiStack (too heavy — the author's call, 2026-09-11), so the page shows the LogQL you would run on a cluster that has one, in the label-selector-first shape that mirrors the metrics lab.

## 3. Design notes
- The lab **ends on an absence**: the crashing Deployment is deleted and `oc logs` has nothing left to read. `verify-logs-gone-with-pod` asserts it, because that gap is precisely what an aggregated store fills.
- `--previous` is framed as the flag that pays for the lab: the logs explaining a crash belong to the container that crashed, not the one that replaced it.
- The secrets warning sits on the aggregation page on purpose — `oc logs` feels private, a central store never is.

## 4. Open
When a LokiStack is reachable (a real DCS cluster, or a bigger test cluster), the LogQL section can become hands-on and gain checks. Nothing else about the lab needs to change.
