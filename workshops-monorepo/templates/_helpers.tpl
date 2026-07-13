{{/* Common labels for the objects this chart owns (Track CRs, TrainingPortal). */}}
{{- define "ws.labels" -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: dcs-academy
{{- with .Values.labels }}
{{ toYaml . }}
{{- end }}
{{- end -}}

{{/* Portal labels (used by NetworkPolicy). */}}
{{- define "portal.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{/* Portal selector labels (used by NetworkPolicy). */}}
{{- define "portal.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/* The Educates portal-UI namespace (<portalName>-ui). */}}
{{- define "portal.uiNamespace" -}}
{{- printf "%s-ui" .Values.educates.portalName -}}
{{- end -}}