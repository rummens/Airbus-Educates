> **Test-run artifact — not created in GitLab.** Produced by `dcs-user-story-authoring`.
>
> | | |
> |---|---|
> | Work item | Issue (project level) |
> | Title | `PoC for unidirectional metric forwarding from an air-gapped national cluster` |
> | Namespace | `<group>/<project>` — inferred from the parent epic's existing children |
> | Parent epic | `Cross Country Metric Aggregation` |
> | Milestone | `Release 5` (parent stream is `Development Stream R5`) |
> | Labels | `type::spike`, `P::1`, `component::monitoring` |
>
> **Label reasoning:** `type::spike` — the outcome is a recorded architecture decision,
> not a shipped component. `P::1` — first in the epic's work order; every other story
> depends on the transport choice. `component::monitoring` — exact live value assumed;
> a real run copies it from `list_labels`.
> **No diagram:** the parent epic already carries the topology, and this story's
> deliverable is a comparison of three options rather than one flow. Repeating the epic
> diagram here would be noise.
> **A real run would ask:** nothing. `type::` and `P::` both follow from the split order.

---

# Description

**As a** Platform Engineer, **I want** the outbound-only forwarding options tested before
we commit to one, **So that** the release is built on a transport that provably clears
the national firewalls instead of one we hope will.

Validate that platform metrics can be forwarded from an air-gapped national cluster to
the central instance using an outbound-only push, before any component is committed to
the release. The PoC compares Prometheus `remote_write` into **Thanos Receive**,
Prometheus Agent mode with the same target, and a **Pushgateway** relay, and ends in a
recorded decision with the firewall requirement written down.

Runs against one national cluster (DE) and the central Sandbox cluster. No production
national environment is touched.

* **Key Requirements:**
    * **Outbound only:** every candidate must work with the national cluster's
      firewall permitting a single outbound destination and port, and with **no**
      inbound rule of any kind. A candidate that needs a central scrape or a reverse
      tunnel is rejected on the spot.
    * **Deny-by-default filtering:** the candidate must be able to drop every series
      that is not explicitly allowlisted, in the national cluster, *before*
      transmission — filtering centrally is not acceptable.
    * **Country identity:** every forwarded series must arrive centrally carrying a
      national instance identifier label, applied at the source.
    * **Offline tolerance:** measure what happens when the central endpoint is
      unreachable for 24 hours — queue growth, disk usage, and whether the agent
      recovers without manual intervention.
    * **Deliverable:** a comparison written into the epic's design document covering
      transport, resource cost per country, failure behaviour, and the exact firewall
      change request text a country team can submit.

**Acceptance Criteria**

- [ ] All three candidates are exercised against the DE cluster and the Sandbox
      central cluster, with the results recorded in the epic's design document.
- [ ] The chosen candidate forwards a metric from DE and it is queryable centrally,
      carrying the national identifier label.
- [ ] A metric that is not on the allowlist is demonstrably absent from the central
      store after being present in the national cluster.
- [ ] The 24-hour central-outage behaviour is measured and documented for the chosen
      candidate, including peak local disk usage.
- [ ] The firewall change request text (destination, port, protocol, direction) is
      written and reviewed by one country network contact.
- [ ] A decision is recorded naming the chosen transport and the reason the other two
      were rejected.

## External References

* Parent epic: `https://<host>/groups/<group>/-/epics/<iid>`
* Prometheus remote write: https://prometheus.io/docs/practices/remote_write/
* Prometheus Agent mode: https://prometheus.io/blog/2021/11/16/agent/
* Thanos Receive: https://thanos.io/tip/components/receive.md/
* Pushgateway, and when not to use it:
  https://prometheus.io/docs/practices/pushing/
