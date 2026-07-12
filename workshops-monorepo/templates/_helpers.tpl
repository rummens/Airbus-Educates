{{/* Common labels for the objects this chart owns (Track CRs, TrainingPortal). */}}
{{- define "ws.labels" -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: dcs-academy
{{- with .Values.labels }}
{{ toYaml . }}
{{- end }}
{{- end -}}
