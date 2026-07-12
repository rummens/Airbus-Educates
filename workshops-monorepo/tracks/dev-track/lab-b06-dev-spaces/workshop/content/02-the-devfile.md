---
title: The Devfile
---

A workspace isn't hand-built — it's declared in a [devfile](https://devfile.io/), a small YAML
spec that says which tools image to use, where the source comes from, and how to run the app.
Same idea as a manifest, but for your *development environment* instead of your deployment.

Look at the one for the sample app:

```editor:open-file
file: ~/exercises/devfile.yaml
```

Three things to notice:

- **`components[].container.image`** — the tools image. It's a **Harbor-mirrored** Universal
  Developer Image referenced via `${DCS_REGISTRY}` — never a public image. On an air-gapped
  platform the workspace image must come from Harbor like everything else.
- **`endpoints`** — port `8080` is exposed so you can open the running app from the workspace.
- **`commands[].exec`** — a `run` command that starts the app on 8080, mirroring how it runs as
  a Pod.

Confirm the devfile respects the air-gapped registry rule:

```examiner:execute-test
name: verify-devfile-registry
title: The devfile pulls its image from Harbor (no external registries)
timeout: 5
```

{{< note >}}
Because the environment is declared, it's **reproducible**: anyone who opens this devfile gets
the identical setup. That's the whole point — the devfile is to your dev environment what the
Deployment manifest is to your running app.
{{< /note >}}
