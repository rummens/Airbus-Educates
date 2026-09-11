# Workshop Plan: lab-o03-rbac-tenancy

## 1. Metadata
- **Name:** `lab-o03-rbac-tenancy` · **Title:** RBAC & Tenancy
- **Duration:** 25m · **Difficulty:** intermediate · **Track:** Operate & Observe, order `30`
- **Prerequisites (curricular):** Core *Terms — Namespaces & Tenancy*
- **Status:** Re-authored from the superseded `lab-b05-rbac-tenancy`, 2026-09-11. Live-verified 32/32.

## 2. Shape
Starts from the question rather than the objects: `oc auth can-i --list`, then a direct yes/no, then the same question pointed at another namespace (refused — tenancy, enforced). Only then the objects behind the answer: Role vs ClusterRole, RoleBinding vs ClusterRoleBinding, rules as apiGroups × resources × verbs, subjects.

The proof is the **before/after pair**: create a ServiceAccount, show it can do nothing, grant a read-only Role, show exactly what changed — and that `delete pods` still answers `no`.

## 3. Repairs to the quarry
The prose carried damage from an old rename script: "In Core the **Terms — Namespaces & Tenancy** lab you learned", and a prerequisite line naming the same lab twice. Repaired rather than shipped. The RoleBinding names its subject exactly (`system:serviceaccount:<ns>:viewer-bot`), so it is applied through `envsubst`.

## 4. Design notes
- Ends on quotas: what the namespace was given, and why an increase is an ITSM request rather than a field you edit.
- 16 graders, the largest set in either track, because almost every step here is a question with a checkable answer.
