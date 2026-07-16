---
title: Isolation in Action
---

Talk is cheap — let's *see* isolation. Two extra namespaces were created for you when
this session started: `app-a` and `app-b` (their full names are your session namespace
with `-app-a` / `-app-b` on the end). Confirm they exist:

```terminal:execute
command: oc get namespaces | grep "$(oc project -q)-app-"
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

It's a single Deployment named **`hello`** — a fixed name, on purpose. Notice there's no
`namespace:` field. That's the trick: the same file targets whichever namespace you name
on the command line.

## Deploy the same app into both namespaces

You'll use the **split terminal**. In the **upper** pane, deploy into `app-a`:

```terminal:execute
command: envsubst < app.yaml | oc apply -n "$(oc project -q)-app-a" -f -
```

```examiner:execute-test
name: verify-rollout-a
title: Verify hello is available in app-a
timeout: 10
retries: .INF
delay: 2
```

Now the **lower** pane — the *identical* manifest into `app-b`:

```terminal:execute
command: envsubst < app.yaml | oc apply -n "$(oc project -q)-app-b" -f -
session: 2
```

```examiner:execute-test
name: verify-rollout-b
title: Verify hello is available in app-b
timeout: 10
retries: .INF
delay: 2
```

{{< note >}}
`envsubst` fills in the registry from the `DCS_REGISTRY` variable before `oc apply`
reads the manifest — the house pattern for any manifest carrying a `${VAR}`.
{{< /note >}}

## Same name, two independent copies

Both namespaces now have a Deployment called `hello` — the identical name, no clash:

```terminal:execute
command: oc get deploy hello -n "$(oc project -q)-app-a" && oc get deploy hello -n "$(oc project -q)-app-b"
```

```examiner:execute-test
name: verify-same-name
title: Verify the same name exists independently in both
timeout: 10
```

On a single cluster you have two things both called `hello`, and neither knows the other
exists. The namespace is the boundary that makes that safe.

## Actions don't leak

Scale the copy in `app-a` down to zero — and watch `app-b` stay exactly as it was:

```terminal:execute
command: oc scale deploy/hello --replicas=0 -n "$(oc project -q)-app-a"
```

The check below reads both namespaces and reports each one's state:

```examiner:execute-test
name: verify-isolation
title: Verify scaling app-a did not affect app-b
timeout: 10
retries: .INF
delay: 2
```

`app-a` is now empty; `app-b` is untouched. **Names, objects, and actions are all scoped
to the namespace.** That's the whole idea.
