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

Two shell features appear as well:

- **`$(oc project -q)`** — runs `oc project -q` first and substitutes its output: your
  active namespace, with `-q` for the quiet, name-only form.
- **`|`** — the pipe sends that list into `grep`, which keeps only the lines matching your
  two peer namespaces.

```terminal:execute
command: oc get projects | grep "$(oc project -q)-app-" | tee ~/exercises/peers.txt
```

```examiner:execute-test
name: verify-two-namespaces
title: ✅ Verify both app-a and app-b namespaces exist
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

Same command, same manifest. Only the `-n` value decides where the app is created.

The deploy command combines three parts:

1. **`envsubst < app.yaml`** — reads `app.yaml` (the `<` feeds the file in as input) and
   replaces `${DCS_REGISTRY}` with the registry value.
2. **`|`** — the pipe sends that filled-in manifest to `oc apply`.
3. **`-f -`** — tells `oc apply` to read the manifest from that piped input instead of from
   a file. The `-` means "standard input".

You will use the **split terminal**. In the **upper** pane, deploy into `app-a`:

```terminal:execute
command: envsubst < app.yaml | oc apply -n "$(oc project -q)-app-a" -f -
```

```examiner:execute-test
name: verify-rollout-a
title: ✅ Verify hello is available in app-a
timeout: 10
retries: .INF
delay: 2
```

Now the **lower** pane — the identical manifest into `app-b`, changing only the `-n` value:

```terminal:execute
command: envsubst < app.yaml | oc apply -n "$(oc project -q)-app-b" -f -
session: 2
```

```examiner:execute-test
name: verify-rollout-b
title: ✅ Verify hello is available in app-b
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

Now read the one in `app-b`:

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-b"
```

```examiner:execute-test
name: verify-same-name
title: ✅ Verify the same name exists independently in both
timeout: 10
retries: 3
delay: 2
```

On a single cluster you have two Deployments both called `hello`, and neither knows the
other exists. The namespace is the boundary that makes that safe.

## Actions don't leak

Scale the copy in `app-a` down to zero. `--replicas=0` sets the desired number of running
copies to zero, so the platform stops the Pod in `app-a`:

```terminal:execute
command: oc scale deploy/hello --replicas=0 -n "$(oc project -q)-app-a"
```

Now read both Deployments and confirm that only `app-a` changed. First `app-a`, which
should show `0/0` (scaled to zero):

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-a"
```

Then `app-b`, which should still show `1/1` — unchanged by the action you took in `app-a`:

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-b"
```

The check below confirms it:

```examiner:execute-test
name: verify-isolation
title: ✅ Verify scaling app-a did not affect app-b
timeout: 10
retries: .INF
delay: 2
```

`app-a` is now empty; `app-b` is unchanged. **Names, objects, and actions are all scoped
to the namespace.** That is the core idea.
