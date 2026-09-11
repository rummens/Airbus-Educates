---
title: The Devfile
---

A [devfile](https://devfile.io/docs/2.2.0/what-is-a-devfile) is to a Dev Spaces
workspace what a Deployment manifest is to a running app: a single YAML document
that fully describes the desired environment, so anyone (or any automation) can
recreate the same workspace from it. Open the one for `hello-dcs`:

```editor:open-file
file: ~/exercises/devfile.yaml
```

## The three things every devfile answers

A devfile always answers the same three questions. `hello-dcs`'s does it in three
sections:

**Where do I develop?** — `components`. Highlight the dev container:

```editor:select-matching-text
file: ~/exercises/devfile.yaml
text: |2
  components:
    - name: dev
      container:
        image: ${DCS_REGISTRY}/devspaces/udi:latest
```

This is a **Universal Developer Image (UDI)** — a general-purpose toolchain
container (compilers, `git`, common language runtimes) that Red Hat ships for Dev
Spaces. On DCS it's mirrored into Harbor like every other image: notice the
component's `image` is `${DCS_REGISTRY}/devspaces/udi:latest`, never a public
registry — the exact same `${DCS_REGISTRY}` placeholder every prior lab's
manifests have used, resolved from Harbor at workspace start, air-gapped end to
end.

**What do I develop?** — `projects`. This is the git source Dev Spaces clones into
the workspace when it starts, so your editor opens with the actual `hello-dcs`
code already checked out — not a blank container.

**How do I run it?** — `commands`. Highlight the run command:

```editor:select-matching-text
file: ~/exercises/devfile.yaml
text: |2
  commands:
    - id: run-hello-dcs
      exec:
        component: dev
        workingDir: ${PROJECTS_ROOT}/hello-dcs
        commandLine: python3 server.py
```

`group.kind: run` marks this as the workspace's default "run" action — it shows up
as a one-click command in the Dev Spaces IDE, so you never have to remember the
exact invocation. It's the same `python3 server.py` entrypoint the `hello-dcs`
container image runs in production — you're not running a different app, you're
running the same app's source, live.

## See the placeholder resolve

The raw file has `${DCS_REGISTRY}` literally in it — that's deliberate, so the
devfile never hardcodes a registry:

```terminal:execute
command: grep 'image:' ~/exercises/devfile.yaml
```

```examiner:execute-test
name: verify-devfile
title: Verify devfile.yaml is present and Harbor-parameterized
timeout: 5
```

Now resolve it the way the session does, substituting the real registry host:

```terminal:execute
command: envsubst < ~/exercises/devfile.yaml | grep 'image:'
```

The before/after tells the whole story: the file you'll hand to Dev Spaces never
names a specific registry, but at workspace-creation time it resolves to your
platform's real Harbor path — no rebuild, no edit, on any DCS cluster.

```examiner:execute-test
name: verify-devfile
title: Verify devfile.yaml is present and Harbor-parameterized
timeout: 5
```

With the devfile understood, it's time to use it.
