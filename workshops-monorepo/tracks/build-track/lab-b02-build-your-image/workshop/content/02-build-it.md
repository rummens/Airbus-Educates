---
title: Build It
---

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/build
```

## Read what will be built

```editor:open-file
file: ~/exercises/app/Containerfile
```

Two lines that matter:

- **`FROM {{< param dcs_registry >}}/samples/hello-dcs:1.0`** takes the base from the
  platform's registry. On an air-gapped cluster a `FROM` that names a public registry fails,
  because there is nothing to reach.
- **`ENV GREETING=…`** is your change, baked **into the image**. Unlike `oc set env`, this
  value ships with the artefact and is the same everywhere it runs.

## Create the BuildConfig

```editor:open-file
file: ~/exercises/buildconfig.yaml
```

Two objects: an **ImageStream** for the output to land in, and the **BuildConfig** itself.
Three fields in it are the whole recipe:

- **`source.type: Binary`** means the input is handed over at start time. With a git server
  the cluster can reach, this would be `git:` instead: same object, same strategy, different
  source.
- **`strategy.dockerStrategy.dockerfilePath: Containerfile`** names the file to build. The
  default is a file called exactly `Dockerfile`, and this project uses the `Containerfile`
  spelling.
- **`output.to`** is the ImageStream tag the finished image is pushed to.

```terminal:execute
command: |-
  cd ~/exercises/app
  envsubst < Containerfile > Containerfile.resolved && mv Containerfile.resolved Containerfile
  oc apply -f ~/exercises/buildconfig.yaml
```

```section:begin
name: breakdown-resolve-and-create
prefix: Breakdown
title: What each part of the command does
```

- **`cd ~/exercises/app`** — moves to the directory that holds the build input.
- **`envsubst < Containerfile > Containerfile.resolved`** — writes a copy of the Containerfile with `${DCS_REGISTRY}` replaced by the registry address from your session.
- **`&& mv Containerfile.resolved Containerfile`** — if that worked, replaces the original with the resolved copy. The BuildConfig reads the file named `Containerfile`.
- **`oc apply -f ~/exercises/buildconfig.yaml`** — creates the ImageStream and the BuildConfig.

```section:end
name: breakdown-resolve-and-create
```

```examiner:execute-test
name: verify-buildconfig-created
title: Verify the BuildConfig and its ImageStream exist
timeout: 60
retries: .INF
delay: 3
```

{{< note >}}
**💡 Tip:** `oc new-build --binary --strategy=docker --name=hello-built` generates the same
two objects in one line. It assumes the file is called `Dockerfile`, which is the assumption
this manifest had to override.
{{< /note >}}

{{< note >}}
**📌 Why `envsubst` first.** A `Containerfile` is read by the build, not by Kubernetes, so
nothing expands `${DCS_REGISTRY}` for it. Resolving it before the build is the same house rule
as every manifest in this track.
{{< /note >}}

## Run a build

```terminal:execute
command: |-
  cd ~/exercises/app
  oc start-build hello-built --from-dir=. --follow
```

`--from-dir=.` uploads this directory as the build's input; `--follow` streams the log so you
watch it happen.

```examiner:execute-test
name: verify-build-completed
title: Verify the build completed successfully
timeout: 300
retries: .INF
delay: 5
```

{{< note >}}
**⏳ This takes a moment:** the first build pulls the base image before it can do anything.
{{< /note >}}

Three things in that log are worth recognising:

1. **Uploading** — your files going to the build Pod.
2. **`STEP n/n`** — each Containerfile instruction being executed, in the cluster.
3. **Pushing** — the finished image going to the registry, with a digest.

## Look at what ran

```terminal:execute
command: oc get builds
```

```examiner:execute-test
name: verify-build-recorded
title: Verify the build is recorded with its status
timeout: 60
retries: .INF
delay: 3
```

`hello-built-1` is the first run of that recipe, kept with its status. A failed build stays
in this list too.
