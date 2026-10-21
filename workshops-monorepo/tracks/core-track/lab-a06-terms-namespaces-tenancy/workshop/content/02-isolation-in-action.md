---
title: Isolation in Action
---

Now see isolation directly. Two extra namespaces were created for you when this session
started: `app-a` and `app-b` (their full names are your session namespace with `-app-a`
and `-app-b` on the end).

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/isolation
```

Confirm they exist. `oc get projects` lists the namespaces **you** may see.

On {{< param product_name >}} that is your own, never the whole cluster — so it is the
command to reach for instead of `oc get namespaces`, which needs cluster-wide rights nobody
gets here.

```terminal:execute
command: oc get projects | grep "$(oc project -q)-app-" | tee ~/exercises/peers.txt
```

```section:begin
name: breakdown-list-peer-namespaces
prefix: Breakdown
title: What each part of the command does
```

- **`oc get projects`** — lists the namespaces you are allowed to see.
- **`| grep "$(oc project -q)-app-"`** — keeps only the lines that contain your namespace
  name followed by `-app-`: your two peer namespaces. `$(oc project -q)` runs first and
  inserts your namespace name (`-q` prints the name alone).
- **`| tee ~/exercises/peers.txt`** — shows the output in the terminal and also saves a copy to
  that file, so the check below can read it.

```section:end
name: breakdown-list-peer-namespaces
```

```examiner:execute-test
name: verify-two-namespaces
title: Verify both app-a and app-b namespaces exist
timeout: 10
```

## One manifest, no namespace baked in

Open the app you'll deploy:

```editor:open-file
file: ~/exercises/app.yaml
```

It is a single Deployment named **`hello`** — a fixed name, on purpose. Notice there is no
`namespace:` field. That is what makes the demo work: the same file targets whichever
namespace you name on the command line.

## Deploy the same app into both namespaces

The important flag on this page is **`-n <namespace>`**. Every `oc` command runs against
exactly one namespace, and `-n` is how you pick which.

- **Leave it off** — the command uses your *current* namespace.
- **Add `-n app-a`** — it targets `app-a` instead.

The command and the manifest stay the same. Only the `-n` value changes where the app is
created.

You will use the **split terminal**. In the **upper** pane, deploy into `app-a`:

```terminal:execute
command: envsubst < app.yaml | oc apply -n "$(oc project -q)-app-a" -f -
```

```section:begin
name: breakdown-deploy-app-a
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < app.yaml`** — reads `app.yaml` (`<` feeds the file in) and replaces
  `${DCS_REGISTRY}` with the registry address from your session.
- **`| oc apply`** — the pipe hands the filled-in manifest to `oc apply`.
- **`-n "$(oc project -q)-app-a"`** — runs the command in the `app-a` namespace:
  `$(oc project -q)` inserts your session namespace name, and `-app-a` is added to
  the end.
- **`-f -`** — reads the manifest from the pipe (standard input) instead of from a
  file.

```section:end
name: breakdown-deploy-app-a
```

```examiner:execute-test
name: verify-rollout-a
title: Verify hello is available in app-a
timeout: 10
retries: .INF
delay: 2
```

Now the **lower** pane — the identical manifest into `app-b`, changing only the `-n` value:

```terminal:execute
command: envsubst < app.yaml | oc apply -n "$(oc project -q)-app-b" -f -
session: 2
```

```section:begin
name: breakdown-deploy-app-b
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < app.yaml`** — reads `app.yaml` (`<` feeds the file in) and replaces
  `${DCS_REGISTRY}` with the registry address from your session.
- **`| oc apply`** — the pipe hands the filled-in manifest to `oc apply`.
- **`-n "$(oc project -q)-app-b"`** — runs the command in the `app-b` namespace:
  `$(oc project -q)` inserts your session namespace name, and `-app-b` is added to
  the end.
- **`-f -`** — reads the manifest from the pipe (standard input) instead of from a
  file.

```section:end
name: breakdown-deploy-app-b
```

```examiner:execute-test
name: verify-rollout-b
title: Verify hello is available in app-b
timeout: 10
retries: .INF
delay: 2
```

{{< note >}}
**📌 Note:** using `envsubst` to fill in a `${VAR}` before piping to `oc apply` is the house pattern for
any manifest that carries a variable.
{{< /note >}}

## Same name, two independent copies

Both namespaces now have a Deployment called `hello`, with the identical name and no clash.
Read the one in `app-a`:

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-a"
```

```section:begin
name: breakdown-read-app-a
prefix: Breakdown
title: What each part of the command does
```

- **`oc get deploy hello`** — shows the Deployment named `hello`.
- **`-n "$(oc project -q)-app-a"`** — runs the command in the `app-a` namespace:
  `$(oc project -q)` inserts your session namespace name, and `-app-a` is added to
  the end.

```section:end
name: breakdown-read-app-a
```

Now read the one in `app-b`:

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-b"
```

```section:begin
name: breakdown-read-app-b
prefix: Breakdown
title: What each part of the command does
```

- **`oc get deploy hello`** — shows the Deployment named `hello`.
- **`-n "$(oc project -q)-app-b"`** — runs the command in the `app-b` namespace:
  `$(oc project -q)` inserts your session namespace name, and `-app-b` is added to
  the end.

```section:end
name: breakdown-read-app-b
```

```examiner:execute-test
name: verify-same-name
title: Verify the same name exists independently in both
timeout: 10
retries: 3
delay: 2
```

On a single cluster you have two Deployments called `hello`. They do not clash because
each is in its own namespace.

## Actions don't leak

Scale the copy in `app-a` down to zero. `--replicas=0` sets the desired number of running
copies to zero, so the platform stops the Pod in `app-a`:

```terminal:execute
command: oc scale deploy/hello --replicas=0 -n "$(oc project -q)-app-a"
```

```section:begin
name: breakdown-scale-app-a
prefix: Breakdown
title: What each part of the command does
```

- **`oc scale deploy/hello --replicas=0`** — sets the desired number of copies of `hello`
  to zero.
- **`-n "$(oc project -q)-app-a"`** — runs the command in the `app-a` namespace:
  `$(oc project -q)` inserts your session namespace name, and `-app-a` is added to
  the end.

```section:end
name: breakdown-scale-app-a
```

Now read both Deployments and confirm that only `app-a` changed. First `app-a`, which
should show `0/0` (scaled to zero):

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-a"
```

```section:begin
name: breakdown-recheck-app-a
prefix: Breakdown
title: What each part of the command does
```

- **`oc get deploy hello`** — shows the Deployment named `hello`.
- **`-n "$(oc project -q)-app-a"`** — runs the command in the `app-a` namespace:
  `$(oc project -q)` inserts your session namespace name, and `-app-a` is added to
  the end.

```section:end
name: breakdown-recheck-app-a
```

Then `app-b`, which should still show `1/1` — unchanged by the action you took in `app-a`:

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-b"
```

```section:begin
name: breakdown-recheck-app-b
prefix: Breakdown
title: What each part of the command does
```

- **`oc get deploy hello`** — shows the Deployment named `hello`.
- **`-n "$(oc project -q)-app-b"`** — runs the command in the `app-b` namespace:
  `$(oc project -q)` inserts your session namespace name, and `-app-b` is added to
  the end.

```section:end
name: breakdown-recheck-app-b
```

The check below confirms it:

```examiner:execute-test
name: verify-isolation
title: Verify scaling app-a did not affect app-b
timeout: 10
retries: .INF
delay: 2
```

`app-a` is now empty and `app-b` is unchanged. **Names, objects and actions are all
scoped to the namespace.**
