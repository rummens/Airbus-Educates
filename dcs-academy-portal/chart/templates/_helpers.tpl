{{- define "portal.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{- define "portal.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/* Portal image ref, applying the registry override (air-gap → Harbor). */}}
{{- define "portal.image" -}}
{{- $host := .Values.global.registry.host -}}
{{- $repo := .Values.image.repository -}}
{{- if $host -}}
{{- $path := regexReplaceAll "^[^/]+/" $repo "" -}}
{{- printf "%s/%s:%s" $host $path (toString .Values.image.tag) -}}
{{- else -}}
{{- printf "%s:%s" $repo (toString .Values.image.tag) -}}
{{- end -}}
{{- end -}}

{{/* The Educates portal-UI namespace (<portalName>-ui). */}}
{{- define "portal.uiNamespace" -}}
{{- printf "%s-ui" .Values.educates.portalName -}}
{{- end -}}

{{/* CNPG cluster name. */}}
{{- define "portal.cnpgName" -}}
{{- printf "%s-db" .Chart.Name -}}
{{- end -}}

{{/* Public academy host the oauth-proxy serves. */}}
{{- define "portal.authHostname" -}}
{{- printf "%s.%s" .Values.auth.hostname .Values.educates.ingressDomain -}}
{{- end -}}

