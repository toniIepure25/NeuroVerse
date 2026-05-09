import type {
  DatasetInfo,
  EvaluationReportItem,
  AcquisitionStatus,
  AcquisitionProfileSummary,
  HardwareValidationReport,
  HardwareValidationStatus,
  LslStatus,
  LslStreamInfo,
  LslStreamsResponse,
  ModelListResponse,
  ModelMetadata,
  RuntimeLatency,
  RuntimeMetrics,
  RuntimeStatus,
  SessionSummary,
  PublicEegReportResponse,
  BciBenchmarkResponse,
  RawBciShadowResponse,
  BrainflowDeviceDiscovery,
  HardwareTrialResponse,
} from '../types/research'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`
    try {
      const data = (await res.json()) as { detail?: string }
      if (data.detail) detail = data.detail
    } catch {
      // keep default error text
    }
    throw new Error(`API error: ${detail}`)
  }
  return res.json()
}

export async function startSession(): Promise<{ status: string; session_id: string }> {
  return request('/api/session/start', { method: 'POST' })
}

export async function stopSession(): Promise<{ status: string; session_id?: string }> {
  return request('/api/session/stop', { method: 'POST' })
}

export async function listSessions(): Promise<Array<{ session_id: string; event_count: number }>> {
  return request('/api/sessions')
}

export async function getHealth(): Promise<{ status: string }> {
  return request('/health')
}

export async function startReplay(
  sessionId: string,
  speed = 1.0
): Promise<{ status: string; event_count: number }> {
  return request(`/api/replay/${sessionId}?speed=${speed}`, { method: 'POST' })
}

export async function getRuntimeStatus(): Promise<RuntimeStatus> {
  return request('/api/runtime/status')
}

export async function getRuntimeLatency(): Promise<RuntimeLatency> {
  return request('/api/runtime/latency')
}

export async function getRuntimeMetrics(): Promise<RuntimeMetrics> {
  return request('/api/runtime/metrics')
}

export async function getAcquisitionStatus(): Promise<AcquisitionStatus> {
  return request('/api/v1/acquisition/status')
}

export async function getLslStatus(): Promise<LslStatus> {
  return request('/api/v1/acquisition/lsl/status')
}

export async function getBrainflowDevices(): Promise<BrainflowDeviceDiscovery> {
  return request('/api/v1/acquisition/brainflow/devices')
}

export async function getLatestHardwareTrial(): Promise<HardwareTrialResponse> {
  return request('/api/v1/hardware-trials/latest')
}

export async function discoverLslStreams(): Promise<LslStreamsResponse> {
  return request('/api/v1/acquisition/lsl/streams?stream_type=EEG')
}

export async function getLslStreamMetadata(streamId: string): Promise<LslStreamInfo> {
  return request(`/api/v1/acquisition/lsl/streams/${streamId}/metadata`)
}

export async function selectLslStream(stream: LslStreamInfo): Promise<AcquisitionStatus> {
  return request('/api/v1/acquisition/lsl/select', {
    method: 'POST',
    body: JSON.stringify({
      stream_name: stream.name,
      stream_type: stream.type,
      source_id: stream.source_id,
      profile_id: 'lsl_synthetic_eeg',
    }),
  })
}

export async function getHardwareValidationStatus(): Promise<HardwareValidationStatus> {
  return request('/api/v1/acquisition/validation/status')
}

export async function listAcquisitionProfiles(): Promise<AcquisitionProfileSummary[]> {
  return request('/api/v1/acquisition/profiles')
}

export async function startSyntheticHardwareValidation(): Promise<HardwareValidationReport> {
  return request('/api/v1/acquisition/validation/start', {
    method: 'POST',
    body: JSON.stringify({
      adapter: 'simulator',
      profile_id: 'synthetic_multimodal',
      duration_seconds: 2,
      record_windows: true,
      run_sqi: true,
    }),
  })
}

export async function startBrainflowSyntheticValidation(): Promise<HardwareValidationReport> {
  return request('/api/v1/acquisition/validation/start', {
    method: 'POST',
    body: JSON.stringify({
      adapter_type: 'brainflow',
      adapter: 'brainflow',
      profile_id: 'brainflow_synthetic_eeg',
      duration_seconds: 3,
      record_windows: true,
      run_sqi: true,
    }),
  })
}

export async function startBrainflowSyntheticCalibration(): Promise<Record<string, unknown>> {
  return request('/api/v1/calibration/start', {
    method: 'POST',
    body: JSON.stringify({
      source: 'brainflow',
      profile_id: 'brainflow_synthetic_eeg',
      duration_seconds: 3,
      protocol: 'resting_baseline',
    }),
  })
}

export async function startBrainflowSyntheticShadow(): Promise<Record<string, unknown>> {
  return request('/api/v1/acquisition/shadow/start', {
    method: 'POST',
    body: JSON.stringify({
      source: 'brainflow',
      profile_id: 'brainflow_synthetic_eeg',
      duration_seconds: 3,
      shadow_only: true,
    }),
  })
}

export async function startLslValidation(stream?: LslStreamInfo): Promise<HardwareValidationReport> {
  return request('/api/v1/acquisition/validation/start', {
    method: 'POST',
    body: JSON.stringify({
      adapter_type: 'lsl',
      adapter: 'lsl',
      stream_name: stream?.name ?? 'NeuroVerseSyntheticEEG',
      stream_type: stream?.type ?? 'EEG',
      source_id: stream?.source_id,
      profile_id: 'lsl_synthetic_eeg',
      duration_seconds: 5,
      record_windows: true,
      run_sqi: true,
    }),
  })
}

export async function startLslCalibration(stream?: LslStreamInfo): Promise<Record<string, unknown>> {
  return request('/api/v1/calibration/start', {
    method: 'POST',
    body: JSON.stringify({
      source: 'lsl',
      stream_name: stream?.name ?? 'NeuroVerseSyntheticEEG',
      stream_type: stream?.type ?? 'EEG',
      source_id: stream?.source_id,
      profile_id: 'lsl_synthetic_eeg',
      duration_seconds: 5,
    }),
  })
}

export async function startLslShadow(stream?: LslStreamInfo): Promise<Record<string, unknown>> {
  return request('/api/v1/acquisition/shadow/start', {
    method: 'POST',
    body: JSON.stringify({
      source: 'lsl',
      stream_name: stream?.name ?? 'NeuroVerseSyntheticEEG',
      stream_type: stream?.type ?? 'EEG',
      source_id: stream?.source_id,
      profile_id: 'lsl_synthetic_eeg',
      duration_seconds: 5,
    }),
  })
}

export async function startEegLslValidation(stream?: LslStreamInfo): Promise<HardwareValidationReport> {
  return request('/api/v1/acquisition/validation/start', {
    method: 'POST',
    body: JSON.stringify({
      adapter_type: 'lsl',
      adapter: 'lsl',
      stream_name: stream?.name ?? 'NeuroVerseReplayEEG',
      stream_type: stream?.type ?? 'EEG',
      source_id: stream?.source_id,
      marker_stream_name: 'NeuroVerseReplayMarkers',
      marker_stream_type: 'Markers',
      profile_id: 'eeg_lsl_10_20_fixture',
      duration_seconds: 6,
      record_windows: true,
      run_sqi: true,
    }),
  })
}

export async function getHardwareValidationReport(reportId: string): Promise<HardwareValidationReport> {
  return request(`/api/v1/acquisition/validation/reports/${reportId}`)
}

export async function emergencyStop(reason = 'operator emergency stop'): Promise<RuntimeStatus> {
  return request('/api/v1/runtime/emergency-stop', {
    method: 'POST',
    body: JSON.stringify({ reason }),
  })
}

export async function freezeAdaptation(reason = 'operator freeze'): Promise<RuntimeStatus> {
  return request('/api/v1/runtime/freeze', {
    method: 'POST',
    body: JSON.stringify({ reason }),
  })
}

export async function unfreezeAdaptation(): Promise<RuntimeStatus> {
  return request('/api/v1/runtime/unfreeze', { method: 'POST' })
}

export async function listModels(): Promise<ModelListResponse> {
  return request('/api/models')
}

export async function getActiveModel(): Promise<RuntimeStatus> {
  return request('/api/models/active')
}

export async function getModel(modelId: string): Promise<ModelMetadata> {
  return request(`/api/models/${modelId}`)
}

export async function activateModel(modelId: string): Promise<RuntimeStatus> {
  return request(`/api/models/${modelId}/activate`, { method: 'POST' })
}

export async function deactivateModel(): Promise<RuntimeStatus> {
  return request('/api/models/deactivate', { method: 'POST' })
}

export async function listDatasets(): Promise<DatasetInfo[]> {
  return request('/api/datasets')
}

export async function listEvaluationReports(): Promise<EvaluationReportItem[]> {
  return request('/api/evaluation/reports')
}

export async function getLatestEvaluationReport(): Promise<EvaluationReportItem> {
  return request('/api/evaluation/latest')
}

export async function getLatestPublicEegReport(): Promise<PublicEegReportResponse> {
  return request('/api/v1/eeg/public/latest')
}

export async function getLatestRealPublicEegReport(): Promise<PublicEegReportResponse> {
  return request('/api/v1/eeg/real-public/latest')
}

export async function getLatestBciBenchmarkReport(): Promise<BciBenchmarkResponse> {
  return request('/api/v1/eeg/bci-benchmark/latest')
}

export async function getLatestRawBciBenchmarkReport(): Promise<BciBenchmarkResponse> {
  return request('/api/v1/eeg/raw-bci-benchmark/latest')
}

export async function getLatestBciBenchmarkComparison(): Promise<BciBenchmarkResponse> {
  return request('/api/v1/eeg/bci-benchmark-comparison/latest')
}

export async function getLatestRawBciShadowReport(): Promise<RawBciShadowResponse> {
  return request('/api/v1/eeg/raw-bci-shadow/latest')
}

export async function getEvaluationReport(reportId: string): Promise<EvaluationReportItem> {
  return request(`/api/evaluation/reports/${reportId}`)
}

export async function getSessionSummary(sessionId: string): Promise<SessionSummary> {
  return request(`/api/sessions/${sessionId}/summary`)
}
