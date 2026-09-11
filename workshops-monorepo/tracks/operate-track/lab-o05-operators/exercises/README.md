Exercise files for the Operators on DCS workshop.

- `sample-cr.yaml` — a CloudNativePG `Cluster`: the **instance you own**. It declares what
  you want (how many PostgreSQL instances, how much storage) and nothing about how to run
  it. The operator creates the StatefulSet, the volumes, the Services and the probes.

`imageName` is deliberately absent: on DCS the platform configures the operator with the
operand image it may run, from the DCS registry. Choosing it is not the tenant's job.
