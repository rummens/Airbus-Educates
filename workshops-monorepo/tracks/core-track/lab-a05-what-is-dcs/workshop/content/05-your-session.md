---
title: Your Session
---

On the right you have a **terminal** already connected to
{{< param product_short >}} and pointed at your own namespace. Every command in this
academy is run with [`oc`](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/cli_tools/openshift-cli-oc#cli-getting-started),
the OpenShift command line tool. Click the command blocks below to run them — you never
have to type them by hand.

Your session also has an **editor** tab for viewing files and manifests, and the
terminal is **split** into an upper pane (`execute-1`) and a lower pane (`execute-2`) —
the same split terminal you've been using in the hands-on labs.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/session
```

## Who Am I?

First, confirm who you are logged in as:

```terminal:execute
command: oc whoami | tee ~/exercises/whoami.txt
```

```examiner:execute-test
name: verify-whoami
title: Verify you are authenticated
timeout: 10
```

## Can I Reach the Cluster?

Check that your `oc` client can talk to the {{< param product_short >}} cluster:

```terminal:execute
command: oc version | tee ~/exercises/version.txt
```

```examiner:execute-test
name: verify-oc-version
title: Verify the cluster API is reachable
timeout: 10
```

## Which Namespace Am I In?

On {{< param product_short >}}, your work lives in a **namespace**. OpenShift calls it a
**project**, which is why the command is `oc project`. Yours is already selected. Show its name:

```terminal:execute
command: oc project -q | tee ~/exercises/project.txt
```

```examiner:execute-test
name: verify-project
title: Verify your namespace is selected
timeout: 10
```

{{< note >}}
**📌 Note:** your namespace name is also available in the terminal as `$SESSION_NAMESPACE`. Because it
is already your default, most `oc` commands need no `-n` flag.
{{< /note >}}

## What's In My Namespace?

`oc status` gives a quick overview of what is running in your namespace. Each lab runs in
its own fresh session namespace, so this one starts clean:

```terminal:execute
command: oc status | tee ~/exercises/status.txt
```

```examiner:execute-test
name: verify-status
title: Verify oc status runs against your namespace
timeout: 10
```

{{< note >}}
**💡 Prefer a visual view?** {{< param product_short >}} has a web console too — the whole
**Console track** is a guided tour of it. For now, the terminal is all you need.
{{< /note >}}
