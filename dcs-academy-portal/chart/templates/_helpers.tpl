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

{{/*
Workshop content image ref for source.type=image, applying the registry
override (air-gap → Harbor). Arg: dict "ctx" $ "ws" <workshop>
*/}}
{{- define "portal.workshopImage" -}}
{{- $ctx := .ctx -}}
{{- $img := .ws.source.image -}}
{{- $host := $ctx.Values.global.registry.host -}}
{{- if $host -}}
{{- $path := regexReplaceAll "^[^/]+/" $img.repository "" -}}
{{- printf "%s/%s:%s" $host $path (toString $img.tag) -}}
{{- else -}}
{{- printf "%s:%s" $img.repository (toString $img.tag) -}}
{{- end -}}
{{- end -}}

{{/*
Whether vcluster is on for a workshop (per-workshop override beats global).
Arg: dict "ctx" $ "ws" <workshop>
*/}}
{{- define "portal.vcluster" -}}
{{- $ws := .ws -}}
{{- if hasKey (default dict $ws.session) "vcluster" -}}
{{- $ws.session.vcluster -}}
{{- else -}}
{{- .ctx.Values.vcluster.enabled -}}
{{- end -}}
{{- end -}}

{{/* CNPG cluster name. */}}
{{- define "portal.cnpgName" -}}
{{- printf "%s-db" .Chart.Name -}}
{{- end -}}

{{/* Public academy host the oauth-proxy serves. */}}
{{- define "portal.authHostname" -}}
{{- printf "%s.%s" .Values.auth.hostname .Values.educates.ingressDomain -}}
{{- end -}}

{{/* oauth-proxy image, registry-overridable (air-gap → Harbor). */}}
{{- define "portal.oauthProxyImage" -}}
{{- if .Values.auth.proxyImage -}}
{{- .Values.auth.proxyImage -}}
{{- else -}}
{{- $host := .Values.global.registry.host -}}
{{- $reg := ternary $host .Values.auth.proxyImageRegistry (ne $host "") -}}
{{- printf "%s/%s:%s" $reg .Values.auth.proxyImageRepository .Values.auth.proxyImageTag -}}
{{- end -}}
{{- end -}}
