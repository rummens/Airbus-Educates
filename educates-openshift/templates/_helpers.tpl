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
Resolve a workshop content image.
Arg: dict "ctx" $ "ws" <workshop map>
*/}}
{{- define "educates.workshopImage" -}}
{{- $ctx := .ctx -}}
{{- $ws := .ws -}}
{{- if $ws.image -}}
{{- $ws.image -}}
{{- else -}}
{{- $host := $ctx.Values.global.registry.host -}}
{{- $base := ternary $host "ghcr.io" (ne $host "") -}}
{{- printf "%s/educates/%s-files:%s" $base $ws.name (toString $ws.version) -}}
{{- end -}}
{{- end -}}

{{/*
oauth-proxy image.
*/}}
{{- define "educates.oauthProxyImage" -}}
{{- if .Values.auth.proxyImage -}}
{{- .Values.auth.proxyImage -}}
{{- else -}}
{{- $host := .Values.global.registry.host -}}
{{- $reg := ternary $host .Values.auth.proxyImageRegistry (ne $host "") -}}
{{- printf "%s/%s:%s" $reg .Values.auth.proxyImageRepository .Values.auth.proxyImageTag -}}
{{- end -}}
{{- end -}}

{{/*
Portal hostnames.
*/}}
{{- define "educates.portalHostname" -}}
{{- printf "%s-ui.%s" .Values.portal.name .Values.educates.ingressDomain -}}
{{- end -}}

{{- define "educates.authHostname" -}}
{{- if .Values.auth.hostname -}}
{{- .Values.auth.hostname -}}
{{- else -}}
{{- printf "%s-secure.%s" .Values.portal.name .Values.educates.ingressDomain -}}
{{- end -}}
{{- end -}}

{{/*
Effective session security policy (vcluster needs baseline, not restricted).
Arg: dict "ctx" $ "ws" <workshop map>
*/}}
{{- define "educates.sessionPolicy" -}}
{{- /* Main session namespace keeps the workshop's own policy. vcluster's SCC
       needs are handled in the -vc namespace via session.objects, not here. */ -}}
{{ .ws.policy }}
{{- end -}}

{{/*
Effective session budget (vcluster raises it).
Arg: dict "ctx" $ "ws" <workshop map>
*/}}
{{- define "educates.sessionBudget" -}}
{{- if .ctx.Values.vcluster.enabled -}}{{ .ctx.Values.vcluster.budget }}{{- else -}}{{ .ws.budget }}{{- end -}}
{{- end -}}
