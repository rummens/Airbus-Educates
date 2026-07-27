---
title: The Terminal
---

The **Terminal** tab on the right is a shell connected to your {{< param product_short >}}
session. It starts in the `~/exercises` directory, where each lab's files live, and every
command is run with [`oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html),
the OpenShift command line.

Notice it's **split** into two panes, one above the other — an **upper** pane
(`execute-1`) and a **lower** pane (`execute-2`). Many labs use both: one to `watch`
something while the other makes a change. Let's run a command in each.

## Run a command in the upper pane

Click the box below. It types and runs the command for you in the **upper** terminal —
`oc whoami` prints the identity you're logged in as:

```terminal:execute
command: oc whoami
```

You should see a username. That confirms your session is authenticated — you never had to
log in by hand.

```examiner:execute-test
name: verify-whoami
title: Verify you are authenticated
timeout: 10
```

## Run a command in the lower pane

Now the **lower** pane. This box targets terminal session 2 — watch the bottom half of
the terminal area:

```terminal:execute
command: oc status
session: 2
```

`oc status` gives a quick overview of what's running in your project. It's empty for
now — you'll change that in the later labs. The point here is only that the command ran
in the **lower** pane while the upper one kept its output.

```examiner:execute-test
name: verify-status
title: Verify oc status runs against your project
timeout: 10
```

{{< note >}}
You *can* type in either pane yourself, but the guided actions do the typing for you —
and they always target the right pane, so you don't have to think about it.
{{< /note >}}
