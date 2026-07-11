# DCS Academy images

Container images for the academy, pushed to `ghcr.io/rummens/*`.

| Image | Base | Purpose |
|---|---|---|
| `dcs-workshop-base:dev` | `educates-base-environment` (Fedora, pinned digest) + `oc` | Workshop **session** image for the basic courses. |
| `hello-dcs:dev` / `samples/hello-dcs:1.0` | Red Hat **UBI9 nginx** (hardened, non-root, arbitrary-UID) | Sample **application** deployed by the workshops. |

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

`deploy_workshop.py` defaults to `--image ghcr.io/rummens/dcs-workshop-base:dev`
and `--registry ghcr.io/rummens` (so exercise `${DCS_REGISTRY}/samples/hello-dcs:1.0`
resolves). The workshops' own `config.yaml`/`resources` keep placeholder values —
the real DCS Harbor is substituted at deploy time, not baked in.
