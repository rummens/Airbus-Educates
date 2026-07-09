{{- define "workshops.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{/*
Resolve a workshop content image ref for source.type=image, applying the
registry override. Arg: dict "ctx" $ "ws" <workshop>
*/}}
{{- define "workshops.image" -}}
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
{{- define "workshops.vcluster" -}}
{{- $ws := .ws -}}
{{- if hasKey (default dict $ws.session) "vcluster" -}}
{{- $ws.session.vcluster -}}
{{- else -}}
{{- .ctx.Values.vcluster.enabled -}}
{{- end -}}
{{- end -}}
