# Image Manifest Reference

Because DCS is air-gapped, **every image a workshop references must exist in Harbor before the workshop runs** (see [air-gapped-images-reference.md](air-gapped-images-reference.md)). To make mirroring reliable, the academy maintains a single **image manifest** — the deduplicated list of every image used across all workshops — which operators feed into the Harbor mirroring workflow.

Keep the set small: shared base images and a small library of sample-app/tool images reused across workshops. A new bare image in one workshop means one more thing to mirror — reuse before introducing.

## What must be in the manifest

- The two workshop base images (`dcs-workshop-base`, `dcs-tools`)
- The workshop-files images published per workshop (`<name>-files`)
- Every application/tool image referenced via `{{< param dcs_registry >}}` in content, exercise files, or `*.objects`
- vcluster component images

## Producing the manifest

Because all image references are variablized, they can be scanned mechanically. Provide a `scripts/collect-images.sh` at the course root that greps workshop sources for image references and emits a sorted, deduplicated list. It resolves the `dcs_registry` param value from each workshop's `workshop/config.yaml` so the output is concrete Harbor paths.

Run it whenever workshops are added or changed, and hand the output to the Harbor mirroring process (the same one behind the repo's `OFFLINE-MIRROR-IMAGES.md`). The manifest is a generated artefact — do not hand-maintain it.

```bash
# from the course root
./scripts/collect-images.sh > image-manifest.txt
```

The script should:

1. Find every `image:` field in `resources/workshop.yaml`, `workshop/content/**`, and `exercises/**` across all workshops.
2. Expand `{{< param dcs_registry >}}` / `$(image_repository)` using each workshop's declared values (or leave the variable visible with a warning if it cannot resolve).
3. Flag any reference to a **non-Harbor** registry as an error — that is a house-standard violation, not something to silently mirror.
4. Output one image per line, sorted and deduplicated.

## No silent gaps

If the collector cannot resolve a reference, it must say so rather than drop it — an unmirrored image is a broken workshop at delivery time. Treat an unresolved or external reference as a failure to fix in the workshop, not an entry to mirror as-is.

## Checklist

- [ ] `scripts/collect-images.sh` exists at the course root and runs clean
- [ ] The manifest is regenerated after any workshop image change
- [ ] The collector flags (does not silently pass) external-registry references
- [ ] The manifest has been handed to the Harbor mirroring workflow before delivery
