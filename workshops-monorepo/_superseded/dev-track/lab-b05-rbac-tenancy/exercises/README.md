Exercise files for the RBAC, Tenancy & Namespaces workshop.

- `serviceaccount-viewer.yaml` — a ServiceAccount, `viewer-bot`, standing in for a non-human
  subject you'll grant (and then test) permissions for.
- `role-viewer.yaml`           — a namespaced Role granting read-only verbs on a couple of
  resource types — a clean least-privilege example.
- `rolebinding-viewer.yaml`    — binds `role-viewer` to `viewer-bot` in your own namespace.
