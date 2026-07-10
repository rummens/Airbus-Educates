{{/*
kapp-controller image, digest-pinned, with registry-host override for air-gap.
*/}}
{{- define "kappController.image" -}}
{{- $repo := .Values.image.repository -}}
{{- $host := .Values.global.registry.host -}}
{{- if $host -}}
{{- $path := regexReplaceAll "^[^/]+/" $repo "" -}}
{{- printf "%s/%s@%s" $host $path .Values.image.digest -}}
{{- else -}}
{{- printf "%s@%s" $repo .Values.image.digest -}}
{{- end -}}
{{- end -}}
