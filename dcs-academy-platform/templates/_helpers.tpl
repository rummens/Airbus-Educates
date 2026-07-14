{{/*
Common labels.
*/}}
{{- define "educates.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{/*
Installer bundle image. Swaps host to global.registry.host when set, preserving
the repo path so mirrors live at <host>/educates/educates-installer:<version>.
*/}}
{{- define "educates.installerImage" -}}
{{- $repo := .Values.educates.installer.bundleRepository -}}
{{- $host := .Values.global.registry.host -}}
{{- if $host -}}
{{- /* replace the leading registry host (first path segment before first "/") */ -}}
{{- $path := regexReplaceAll "^[^/]+/" $repo "" -}}
{{- printf "%s/%s:%s" $host $path .Values.educates.version -}}
{{- else -}}
{{- printf "%s:%s" $repo .Values.educates.version -}}
{{- end -}}
{{- end -}}

{{/*
Bundle-mirror image (imgpkg baked in). Host-swapped to global.registry.host like
every other image, so set global.registry.host AND mirror this one small image
into that registry first (plain image — Harbor replication is fine) so the Job can
pull it in the air gap.
*/}}
{{- define "educates.mirrorImage" -}}
{{- $ref := .Values.bundleMirror.image -}}
{{- $host := .Values.global.registry.host -}}
{{- if $host -}}
{{- printf "%s/%s" $host (regexReplaceAll "^[^/]+/" $ref "") -}}
{{- else -}}
{{- $ref -}}
{{- end -}}
{{- end -}}

{{/*
kube-state-metrics image (custom-resource metrics exporter).
*/}}
{{- define "educates.ksmImage" -}}
{{- if .Values.monitoring.ksmImage -}}
{{- .Values.monitoring.ksmImage -}}
{{- else -}}
{{- $host := .Values.global.registry.host -}}
{{- $reg := ternary $host .Values.monitoring.ksmRegistry (ne $host "") -}}
{{- printf "%s/%s:%s" $reg .Values.monitoring.ksmRepository .Values.monitoring.ksmTag -}}
{{- end -}}
{{- end -}}
