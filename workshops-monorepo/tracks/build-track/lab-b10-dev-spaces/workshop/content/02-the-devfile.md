---
title: The Devfile
---

A [devfile](https://devfile.io/docs/2.2.0/what-is-a-devfile) is to a Dev Spaces
workspace what a Deployment manifest is to a running app: a single YAML document
that fully describes the desired environment, so anyone (or any automation) can
recreate the same workspace from it.

Open the slide for this page (📊 **Slides** tab):

```dashboard:reload-dashboard
name: Slides
url: {{< param ingress_protocol >}}://{{< param session_hostname >}}/slides/#/devfile
```

Open the devfile for `hello-dcs`:

```editor:open-file
file: ~/exercises/devfile.yaml
```

## The three sections

A devfile has three main sections.

**`components`** say where you develop. Highlight the dev container:

```editor:select-matching-text
file: ~/exercises/devfile.yaml
text: |2
  components:
    - name: dev
      container:
        image: ${DCS_REGISTRY}/devspaces/udi:latest
```

This is a **Universal Developer Image (UDI)**, a general-purpose toolchain
container (compilers, `git`, common language runtimes) that Red Hat ships for Dev
Spaces. On DCS it is mirrored into Harbor like every other image. The component's
`image` is `${DCS_REGISTRY}/devspaces/udi:latest`, the same placeholder the other
labs' manifests use, so no public registry is involved. The placeholder is filled
in with `envsubst` before the file is used, as in every other lab.

**`projects`** say what you develop: the git source Dev Spaces clones into the
workspace when it starts, so your editor opens with the `hello-dcs` code already
checked out.

**`commands`** say how to run it. Highlight the run command:

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

The command's `group.kind: run`, below the highlighted lines, marks it as the
workspace's default run action. The Dev Spaces IDE shows it as a one-click command,
so you do not have to remember the invocation. It runs `python3 server.py`, the same
entrypoint the `hello-dcs` container image runs in production, against the source in
the workspace.

## See the placeholder resolve

The raw file contains the literal text `${DCS_REGISTRY}`, so the devfile never
hardcodes a registry:

```terminal:execute
command: grep 'image:' ~/exercises/devfile.yaml
```

```examiner:execute-test
name: verify-devfile
title: Verify devfile.yaml is present and Harbor-parameterized
timeout: 5
```

Check that it has the structure of a devfile, with a schema version, components and commands:

```terminal:execute
command: |-
  yq '{"schemaVersion": .schemaVersion, "components": (.components | length), "commands": (.commands | length)}' ~/exercises/devfile.yaml
```

```section:begin
name: breakdown-devfile-structure
prefix: Breakdown
title: What each part of the command does
```

- **`yq '…'`** — reads a YAML file and prints the result of the expression in quotes.
- **`{ … }`** — builds a new map with the three keys listed inside it.
- **`"schemaVersion": .schemaVersion`** — copies the devfile's `schemaVersion` value.
- **`"components": (.components | length)`** — takes the `components` list and counts its items.
- **`"commands": (.commands | length)`** — counts the items in the `commands` list the same way.
- **`~/exercises/devfile.yaml`** — the file to read.

```section:end
name: breakdown-devfile-structure
```

```examiner:execute-test
name: verify-devfile-structure
title: Verify the devfile declares a container to develop in and commands to run
timeout: 30
retries: 3
delay: 2
```

Now resolve it the way the session does, substituting the real registry host:

```terminal:execute
command: envsubst < ~/exercises/devfile.yaml | grep 'image:'
```

```section:begin
name: breakdown-resolve-placeholder
prefix: Breakdown
title: What each part of the command does
```

- **`envsubst < ~/exercises/devfile.yaml`** — reads the devfile and replaces each `${VAR}` placeholder with the value from your session; `${DCS_REGISTRY}` becomes your Harbor registry host.
- **`| grep 'image:'`** — keeps only the line with `image:`, so you can compare it with the raw line above.

```section:end
name: breakdown-resolve-placeholder
```

The file you hand to Dev Spaces never names a registry. Once `envsubst` fills in the
placeholder, the image points to your platform's Harbor, so the same devfile works on
any DCS cluster without editing.

```examiner:execute-test
name: verify-devfile
title: Verify devfile.yaml is present and Harbor-parameterized
timeout: 5
```

Next, launch a workspace from it.
