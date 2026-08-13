Exercise files for "Building Images with BuildConfigs".

- `buildconfig-s2i.yaml` — the BuildConfig you'll apply and run, using the **S2I**
  (Source-to-Image) strategy. Points at a small provided git repository (the build
  *source*) and pushes its output to the `hello-dcs-built` ImageStream.
- `buildconfig-dockerfile.yaml` — the same build, using the **Dockerfile** strategy
  instead. You read this one for contrast; the workshop runs the S2I BuildConfig.
- `imagestream.yaml` — the ImageStream both BuildConfigs push their output to.
- `deployment.yaml` — a Deployment referencing the image *you* build in this lab
  (`hello-dcs-built`), not a pre-built Harbor sample.

Manifests with a `${...}` placeholder are applied with `envsubst`, never plain `oc apply`
— see the first page for why.
