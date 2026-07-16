---
title: Your Session
---

Time to get hands-on. On the right you have a **terminal** already connected to
{{< param product_short >}} and pointed at your own project. Every command in this
academy is run with [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html),
the OpenShift command line tool. Click the command blocks below to run them — you never
have to type them by hand.

Your session also has an **editor** tab for viewing files and manifests, and the
terminal is **split** into an upper pane (`execute-1`) and a lower pane (`execute-2`) —
worth knowing now, because the next workshop uses both.

## Who Am I?

First, confirm who you are logged in as:

```terminal:execute
command: oc whoami
```

```examiner:execute-test
name: verify-whoami
title: Verify you are authenticated
timeout: 10
```

## Can I Reach the Cluster?

Check that your `oc` client can talk to the {{< param product_short >}} cluster:

```terminal:execute
command: oc version
```

```examiner:execute-test
name: verify-oc-version
title: Verify the cluster API is reachable
timeout: 10
```

## Which Project Am I In?

On {{< param product_short >}}, your work lives in a **project** (an OpenShift project
wrapping a Kubernetes namespace). Yours is already selected. Show its name:

```terminal:execute
command: oc project -q
```

```examiner:execute-test
name: verify-project
title: Verify your project is selected
timeout: 10
```

{{< note >}}
Your project name is also available in the terminal as `$SESSION_NAMESPACE`. Because it
is already your default, most `oc` commands need no `-n` flag.
{{< /note >}}

## What's In My Project?

`oc status` gives a quick overview of what is running in your project. It's empty for
now — you'll change that in the next workshop:

```terminal:execute
command: oc status
```

```examiner:execute-test
name: verify-status
title: Verify oc status runs against your project
timeout: 10
```

{{< note >}}
Prefer a visual view? {{< param product_short >}} has a web console too — you'll get a
full guided tour of it in **A08: The OpenShift Console**. For now, the terminal is all
you need.
{{< /note >}}
