# DCS Academy images

Container images for the academy, pushed to `ghcr.io/rummens/*`.

| Image | Base | Purpose |
|---|---|---|
| `dcs-workshop-base:develop` | `educates-base-environment` (Fedora, pinned digest) + `oc` | Workshop **session** image for the basic courses. |
| `hello-dcs:dev` / `samples/hello-dcs:1.0` | Red Hat **UBI9 Python** (hardened, non-root, arbitrary-UID, multiarch) | Sample **application** deployed by the workshops. Dependency-free stdlib HTTP server on `:8080`. Env-driven: `GREETING` (headline, changeable live with `oc set env`), `MODE=CLI\|UI` (CLI = plain text for `curl`; UI = styled HTML that prints the app's own external Route URL from the request Host header), `PORT`, `VERSION`. `/healthz` for probes. |
| `dcs-academy-portal:dev` | Python slim | The custom academy portal (UI + BFF + reverse-proxy). |
| `educates-mirror:dev` | Red Hat **UBI9-minimal** + `imgpkg` | Air-gap helper: relocates the Educates installer imgpkg bundle into a private registry. Run by the platform chart's `bundleMirror` Job, or standalone. No container engine/virtualization needed. |
| `dcs-ci:dev` | Python slim + `git` + `curl` | CI base for the **no-cluster test tier** (`.gitlab-ci.yml` stage `test`). Bakes what `portal-tests` + `workshop-static` need so jobs skip per-run `apt-get`. Cluster tier (stage `e2e`) runs on the `crc` runner, not this image. |

## Why the workshop base isn't a Red Hat image

An Educates workshop *session* image must extend `educates-base-environment` —
the dashboard, terminal, editor, content renderer and supervisor live there. A
from-scratch Red Hat image cannot function as a workshop image. That base
already ships `jq`, `yq`, `curl`, `git`, `envsubst`, `kubectl`; the only tool
the basic courses were missing is `oc`, which the Containerfile adds. The Red
Hat hardened base (UBI9) is used where it fits: the **application** image
(`hello-dcs`), which runs as an ordinary workload under the restricted policy.

## Build

```bash
./build.sh              # arm64 (CRC), default
MULTIARCH=1 ./build.sh  # amd64 + arm64 for x86 clusters too
```

After the first push, make the ghcr packages **public** so clusters can pull
them without a pull secret.

## Use in a workshop (CRC testing)

`deploy_workshop.py` defaults to `--image ghcr.io/rummens/dcs-workshop-base:develop`
and `--registry ghcr.io/rummens` (so exercise `${DCS_REGISTRY}/samples/hello-dcs:1.0`
resolves). The workshops' own `config.yaml`/`resources` keep placeholder values —
the real DCS Harbor is substituted at deploy time, not baked in.
