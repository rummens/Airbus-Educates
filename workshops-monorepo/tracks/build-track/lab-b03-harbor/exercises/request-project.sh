#!/usr/bin/env bash
# Ask for the Harbor project, if this cluster has the provider that makes them.
#
# The Academy's training cluster does not run the Harbor provider — there is no Harbor
# behind it. So the script does the real thing where it can, and reads the manifest back
# where it cannot, rather than failing at a step that is not the lesson.
set -uo pipefail
CRD=projects.project.harbor.crossplane.io

if oc get crd "$CRD" >/dev/null 2>&1; then
  echo "Harbor provider found. Creating the project."
  envsubst < ~/exercises/harbor-project.yaml | oc apply -f -
  oc wait --for=condition=Ready "project.project.harbor.crossplane.io/${SESSION_NAMESPACE}-scratch" --timeout=180s
  exit
fi

echo "This training cluster does not run the Harbor provider, so there is no project to create."
echo "Reading back what the manifest asks for instead. On DCS, this is what would be built:"
echo
envsubst < ~/exercises/harbor-project.yaml | yq '{
  "project": .spec.forProvider.name,
  "public": .spec.forProvider.public,
  "scan on push": .spec.forProvider.vulnerabilityScanning,
  "refuse to serve at": (.spec.forProvider.deploymentSecurity | select(. != "") // "nothing is refused (DEV)"),
  "storage quota": (.spec.forProvider.storageQuota / 1073741824 | tostring + " GiB")
}'
