---
title: The Terminal
---

The **Terminal** tab on the right is a shell connected to your {{< param product_short >}}
session.

It starts in the `~/exercises` directory, where each lab's files live. Every command runs
with [`oc`](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/cli_tools/openshift-cli-oc#cli-getting-started),
the OpenShift command line.

Notice it is **split** into two panes, one above the other:

- the **upper** pane — `execute-1`, the default for a command box;
- the **lower** pane — `execute-2`.

Many labs use both: one to `watch` something while the other makes a change. Run a command
in each.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/terminal
```

## Run a command in the upper pane

Click the box below. It types and runs the command for you in the **upper** terminal —
`oc whoami` prints the identity you're logged in as:

```terminal:execute
command: oc whoami | tee ~/exercises/whoami.txt
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
command: oc status | tee ~/exercises/status.txt
session: 2
```

`oc status` gives a quick overview of what's running in your namespace. It is empty for
now; later labs deploy apps into it. This step only shows that the command ran in the
**lower** pane while the upper pane kept its output.

```examiner:execute-test
name: verify-status
title: Verify oc status runs against your namespace
timeout: 10
```

{{< note >}}
**💡 Tip:** you *can* type in either pane yourself. The guided actions do the typing for
you, and they always target the right pane — so you do not have to think about it.
{{< /note >}}
