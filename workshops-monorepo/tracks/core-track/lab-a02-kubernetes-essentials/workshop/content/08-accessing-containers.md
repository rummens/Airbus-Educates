---
title: Accessing Containers
---

Sometimes logs aren't enough and you need to look *inside* a running container — to check
a file, an environment variable, or network connectivity from the app's point of view.
`oc exec` runs a command inside a container; `oc rsh` opens an interactive shell.

Run a single command inside the app's container:

```terminal:execute
command: oc exec deployment/hello-dcs -- env
```

You'll see the container's environment variables. The `--` separates `oc`'s own options
from the command you want to run inside the container.

```examiner:execute-test
name: verify-exec
title: Verify you can exec into the container
args:
- hello-dcs
timeout: 10
```

For an interactive session you would use:

```
oc rsh deployment/hello-dcs
```

which drops you into a shell in the container (type `exit` to leave). We won't keep a
shell open here, but it's invaluable for exploratory debugging.

## A Word of Caution

Exec is for **inspection**, not repair. Anything you change inside a running container is
lost the moment that Pod is replaced — and remember from the self-healing section how
readily that happens. If you find yourself fixing something live, that's a signal the fix
belongs in the image or the Deployment manifest instead, so it survives the next rollout.

{{< note >}}
On {{< param product_short >}}, containers run as a non-root user under a restrictive
security policy, so some actions inside the container (installing packages, writing to
system paths) will be denied by design. That's expected — see the OpenShift security model.
{{< /note >}}
