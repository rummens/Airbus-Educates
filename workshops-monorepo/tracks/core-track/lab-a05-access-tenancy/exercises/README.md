Exercise files for "Access & Tenancy".

- `sample-role.yaml` — a `Role` (`pod-reader`) plus a `RoleBinding` (`pod-reader-binding`) you
  inspect in the editor and apply to your own namespace in the closing challenge, to see RBAC
  take effect. The binding grants the `system:authenticated` group read access to Pods, so it
  needs no per-learner username and applies cleanly in any session namespace.
