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
  SafetyStateResponse,
  SafetyTimelineResponse,
  SafetyBlockedActionsResponse,
  SafetyClosedLoopResponse,
  DataSourceListResponse,
  DataSourceStatus,
  FusionDemoSampleResponse,
  FusionOutput,
  FusionStatusResponse,
  FusionAdaptersResponse,
  FusionCalibrateResponse,
  FusionValidateResponse,
  FusionValidationLatestResponse,
  ImaginaManifestValidationResponse,
  FusionValidationSnapshot,
} from '../types/research'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const STATIC_BASE_URL = import.meta.env.BASE_URL || '/'

function staticAsset(path: string): string {
  return `${STATIC_BASE_URL.replace(/\/$/, '')}/${path.replace(/^\//, '')}`
}

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

export async function getFusionStatus(): Promise<FusionStatusResponse> {
  return request('/api/v1/fusion/status')
}

export async function generateFusionDemoSample(): Promise<FusionDemoSampleResponse> {
  return request('/api/v1/fusion/demo-sample', { method: 'POST' })
}

export async function getLatestFusion(): Promise<{ output: FusionOutput }> {
  return request('/api/v1/fusion/latest')
}

export async function getFusionAdapters(): Promise<FusionAdaptersResponse> {
  return request('/api/v1/fusion/adapters')
}

export async function runFusionCalibration(): Promise<FusionCalibrateResponse> {
  return request('/api/v1/fusion/calibrate', { method: 'POST' })
}

export async function runFusionValidation(): Promise<FusionValidateResponse> {
  return request('/api/v1/fusion/validate', { method: 'POST' })
}

export async function getLatestFusionValidation(): Promise<FusionValidationLatestResponse> {
  return request('/api/v1/fusion/validation/latest')
}

export async function validateImaginaManifest(
  manifestPath?: string,
): Promise<ImaginaManifestValidationResponse> {
  return request('/api/v1/fusion/imagina/manifest/validate', {
    method: 'POST',
    body: manifestPath ? JSON.stringify({ manifest_path: manifestPath }) : undefined,
  })
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

// ---------------------------------------------------------------------------
//  Safety governance
// ---------------------------------------------------------------------------

export async function getSafetyState(): Promise<SafetyStateResponse> {
  return request('/api/v1/safety/state')
}

export async function getSafetyTimeline(limit = 20): Promise<SafetyTimelineResponse> {
  return request(`/api/v1/safety/timeline?limit=${limit}`)
}

export async function getSafetyBlockedActions(limit = 20): Promise<SafetyBlockedActionsResponse> {
  return request(`/api/v1/safety/blocked-actions?limit=${limit}`)
}

export async function getSafetyClosedLoopStatus(): Promise<SafetyClosedLoopResponse> {
  return request('/api/v1/safety/closed-loop')
}

export async function resetSafetyState(reason = 'operator reset'): Promise<Record<string, unknown>> {
  return request('/api/v1/safety/reset', {
    method: 'POST',
    body: JSON.stringify({ reason }),
  })
}

export async function safetyFreeze(reason = 'operator freeze'): Promise<Record<string, unknown>> {
  return request('/api/v1/safety/freeze', {
    method: 'POST',
    body: JSON.stringify({ reason }),
  })
}

export async function safetyUnfreeze(): Promise<Record<string, unknown>> {
  return request('/api/v1/safety/unfreeze', { method: 'POST' })
}

export async function safetyEmergencyStop(reason = 'operator emergency stop'): Promise<Record<string, unknown>> {
  return request('/api/v1/safety/emergency-stop', {
    method: 'POST',
    body: JSON.stringify({ reason }),
  })
}

export async function safetyClearEmergency(): Promise<Record<string, unknown>> {
  return request('/api/v1/safety/clear-emergency', { method: 'POST' })
}

export async function refreshSafetyEvidence(): Promise<Record<string, unknown>> {
  return request('/api/v1/safety/evidence/refresh', { method: 'POST' })
}

// ---------------------------------------------------------------------------
//  Protocol engine
// ---------------------------------------------------------------------------

import type {
  AutoRunEvidence,
  AutoRunEvidenceSnapshot,
  CompletionReport,
  PreflightResult,
  ProtocolDefinition,
  ProtocolRun,
  ProtocolRunSummary,
} from '../types/research'

export async function listProtocols(): Promise<ProtocolDefinition[]> {
  return request('/api/v1/protocols')
}

export async function getProtocol(protocolId: string): Promise<ProtocolDefinition> {
  return request(`/api/v1/protocols/${protocolId}`)
}

export async function createProtocolRun(
  protocolId: string,
  inputs: Record<string, string> = {},
): Promise<ProtocolRun> {
  return request(`/api/v1/protocols/${protocolId}/runs`, {
    method: 'POST',
    body: JSON.stringify({ inputs }),
  })
}

export async function listProtocolRuns(): Promise<ProtocolRunSummary[]> {
  return request('/api/v1/protocol-runs')
}

export async function getProtocolRun(runId: string): Promise<ProtocolRun> {
  return request(`/api/v1/protocol-runs/${runId}`)
}

export async function runProtocolStep(
  runId: string,
  stepId: string,
): Promise<Record<string, unknown>> {
  return request(`/api/v1/protocol-runs/${runId}/steps/${stepId}/run`, {
    method: 'POST',
  })
}

export async function completeProtocolRun(runId: string): Promise<Record<string, unknown>> {
  return request(`/api/v1/protocol-runs/${runId}/complete`, { method: 'POST' })
}

export async function getProtocolRunReport(runId: string): Promise<ProtocolRun> {
  return request(`/api/v1/protocol-runs/${runId}/report`)
}

export async function getProtocolCompletionReport(
  runId: string,
): Promise<CompletionReport> {
  return request(`/api/v1/protocol-runs/${runId}/completion-report`)
}

export async function getLatestAutoRun(): Promise<AutoRunEvidence> {
  return request('/api/v1/protocol-runs/latest-auto-run')
}

export async function getStaticLatestAutoRun(): Promise<AutoRunEvidence> {
  const res = await fetch(staticAsset('evidence/latest_auto_run_protocol.json'), {
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    throw new Error(`Static evidence unavailable: ${res.status} ${res.statusText}`)
  }
  return res.json()
}

export async function getLatestAutoRunSnapshot(): Promise<AutoRunEvidenceSnapshot> {
  try {
    const evidence = await getLatestAutoRun()
    return { evidence, source: 'live_backend' }
  } catch (liveError) {
    try {
      const evidence = await getStaticLatestAutoRun()
      const detail = liveError instanceof Error ? liveError.message : 'Backend unavailable'
      return { evidence, source: 'static_baked_snapshot', detail }
    } catch (staticError) {
      const liveMessage = liveError instanceof Error ? liveError.message : 'Backend unavailable'
      const staticMessage = staticError instanceof Error ? staticError.message : 'Static evidence unavailable'
      throw new Error(`${liveMessage}; ${staticMessage}`)
    }
  }
}

export async function getLatestAutoRunReport(): Promise<CompletionReport> {
  return request('/api/v1/protocol-runs/latest-auto-run/report')
}

export async function getProtocolPreflight(
  protocolId: string,
  inputs: Record<string, string> = {},
): Promise<PreflightResult> {
  if (Object.keys(inputs).length === 0) {
    return request(`/api/v1/protocols/${protocolId}/preflight`)
  }
  return request(`/api/v1/protocols/${protocolId}/preflight`, {
    method: 'POST',
    body: JSON.stringify({ inputs }),
  })
}

// ---------------------------------------------------------------------------
//  Data source readiness
// ---------------------------------------------------------------------------

export async function listDataSources(): Promise<DataSourceListResponse> {
  return request('/api/v1/data-sources')
}

export async function getStaticDataSources(): Promise<DataSourceListResponse> {
  const res = await fetch(staticAsset('evidence/data_source_readiness_snapshot.json'), {
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    throw new Error(`Static data-source snapshot unavailable: ${res.status} ${res.statusText}`)
  }
  const data = (await res.json()) as DataSourceListResponse
  return { ...data, mode: 'static_portfolio' }
}

export async function refreshDataSource(sourceId: string): Promise<DataSourceStatus> {
  return request(`/api/v1/data-sources/${sourceId}/refresh`, { method: 'POST' })
}

export async function preflightDataSource(
  sourceId: string,
  inputs: Record<string, string> = {},
): Promise<DataSourceStatus> {
  return request(`/api/v1/data-sources/${sourceId}/preflight`, {
    method: 'POST',
    body: JSON.stringify({ inputs }),
  })
}

export async function runAllProtocolSteps(runId: string): Promise<Record<string, unknown>> {
  return request(`/api/v1/protocol-runs/${runId}/run-all`, { method: 'POST' })
}

export async function stopProtocolOrchestration(runId: string): Promise<Record<string, unknown>> {
  return request(`/api/v1/protocol-runs/${runId}/stop`, { method: 'POST' })
}

export async function cancelProtocolStep(
  runId: string,
  stepId: string,
): Promise<Record<string, unknown>> {
  return request(`/api/v1/protocol-runs/${runId}/steps/${stepId}/cancel`, { method: 'POST' })
}

/**
 * Open a Server-Sent Events stream for live protocol run status.
 * Returns a cleanup function; call it to close the stream.
 * Falls back silently — the caller should also poll if needed.
 */
export function streamProtocolRunStatus(
  runId: string,
  onUpdate: (data: Record<string, unknown>) => void,
  onDone: () => void,
  onError: () => void,
): () => void {
  let es: EventSource | null = null
  try {
    es = new EventSource(`/api/v1/protocol-runs/${runId}/status/stream`)
    es.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data as string) as Record<string, unknown>
        if (data.done || data.error || data.timeout) {
          es?.close()
          onDone()
          return
        }
        onUpdate(data)
      } catch {
        // ignore JSON parse errors
      }
    }
    es.onerror = () => {
      es?.close()
      onError()
    }
  } catch {
    onError()
  }
  return () => es?.close()
}

export async function getStaticFusionValidationSummary(): Promise<FusionValidationLatestResponse> {
  const res = await fetch(staticAsset('evidence/latest_fusion_validation_summary.json'), {
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    throw new Error(`Static fusion validation summary unavailable: ${res.status} ${res.statusText}`)
  }
  return res.json()
}

export async function getStaticFusionCalibrationProfile(): Promise<FusionCalibrateResponse> {
  const res = await fetch(staticAsset('evidence/latest_fusion_calibration_profile.json'), {
    headers: { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    throw new Error(`Static fusion calibration profile unavailable: ${res.status} ${res.statusText}`)
  }
  return res.json()
}

export async function getLatestFusionValidationSnapshot(): Promise<FusionValidationSnapshot> {
  try {
    // Attempt live backend queries
    const validation = await getLatestFusionValidation()
    let calibration: FusionCalibrateResponse | null = null
    try {
      // Get adapters to show statuses
      const adapters = await getFusionAdapters()
      return { source: 'live_backend', validation, adapters, calibration }
    } catch {
      return { source: 'live_backend', validation }
    }
  } catch (liveError) {
    try {
      // Fallback to static baked snapshot
      const validation = await getStaticFusionValidationSummary()
      let calibration: FusionCalibrateResponse | null = null
      try {
        calibration = await getStaticFusionCalibrationProfile()
      } catch {
        // silent
      }
      const detail = liveError instanceof Error ? liveError.message : 'Backend unavailable'
      return {
        source: 'static_baked_snapshot',
        validation,
        calibration,
        detail,
      }
    } catch (staticError) {
      const liveMessage = liveError instanceof Error ? liveError.message : 'Backend unavailable'
      const staticMessage = staticError instanceof Error ? staticError.message : 'Static evidence unavailable'
      throw new Error(`Fusion evidence error: ${liveMessage}; ${staticMessage}`)
    }
  }
}


export interface ExternalImaginaStatus {
  project_root: string
  exists: boolean
  detected_version: string | null
  available_artifacts: string[]
  latest_model_path: string | null
  latest_report_path: string | null
  latest_metrics_path: string | null
  latest_prediction_path: string | null
  integration_ready: boolean
  limitations: string[]
  warnings: string[]
}

export interface ExternalImaginaModelArtifact {
  model_id: string
  artifact_type: string
  path: string
  created_at: string
  metrics?: any
  model_card?: string
  target: string
  modality: string
  paradigm: string
  source_project: string
}

export interface ImaginaStatus {
  status: string
  plugin_id: string
  active_source: string
  external_project_status?: ExternalImaginaStatus
  internal_fixture_status?: {
    available: boolean
    latest_model: any
    warnings: string[]
  }
  proxy_estimates_only: boolean
  not_decoded_content: boolean
  closed_loop_allowed: boolean
  limitations: string[]
  provenance: {
    version: string
    timestamp: string
    scientific_framing?: string
  }
}

export interface ImaginaModel {
  model_id: string
  path: string
  model_type: string
  dataset_id: string
  target: string
  registered_at: string
  imagina_model: boolean
  source_project?: string
  metrics?: {
    accuracy: number
    balanced_accuracy: number
    macro_f1: number
    confusion_matrix: number[][]
    sample_count: number
    subject_count: number
    split_strategy: string
    leakage_warnings: string[]
  }
}

export async function getImaginaStatus(): Promise<ImaginaStatus> {
  return request('/api/v1/imagina/status')
}

export async function getExternalImaginaStatus(): Promise<ExternalImaginaStatus> {
  return request('/api/v1/imagina/external/status')
}

export async function getExternalImaginaArtifacts(): Promise<{ project_root: string; artifacts: ExternalImaginaModelArtifact[] }> {
  return request('/api/v1/imagina/external/artifacts')
}

export async function refreshExternalImagina(): Promise<{ status: string; external_project_status: ExternalImaginaStatus; artifact_count: number }> {
  return request('/api/v1/imagina/external/refresh', { method: 'POST' })
}

export async function getImaginaModels(): Promise<ImaginaModel[]> {
  const data = await request<{ models: ImaginaModel[] }>('/api/v1/imagina/models')
  return data.models
}

export async function trainImaginaBaseline(
  modelType: string = 'logistic_regression',
  splitStrategy: string = 'fixture',
): Promise<any> {
  return request('/api/v1/imagina/train-baseline', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      manifest_path: 'configs/imagina/example_imagina_v1_manifest.json',
      model_type: modelType,
      split_strategy: splitStrategy,
      target_type: 'classification',
    }),
  })
}

export async function getLatestContractImport(): Promise<any> {
  return request('/api/v1/imagina/external/imports/latest')
}

export async function validateExportContract(manifestPath: string): Promise<any> {
  return request('/api/v1/imagina/external/validate-export', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ manifest_path: manifestPath }),
  })
}

export async function importExportContract(manifestPath: string): Promise<any> {
  return request('/api/v1/imagina/external/import-export', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ manifest_path: manifestPath }),
  })
}

export interface SystemOverview {
  source: 'live_backend' | 'static_snapshot'
  generated_at: string
  warnings: string[]
  limitations: string[]
  closed_loop_allowed: boolean
  safety: {
    current_state: string
    severity: string
    closed_loop_allowed: boolean
    lock_reasons: string[]
    lock_reason_codes: string[]
    emergency_stop_active: boolean
    adaptation_frozen: boolean
    evidence_summary: any
    safety_audit_report_path?: string
  }
  data_sources: any
  protocol: {
    latest_run?: any
  }
  imagina: {
    external_detected: boolean
    external_status: any
    latest_import?: any
  }
  fusion: {
    latest_validation?: any
    imagina_proxy_status: string
    disclaimer: string
  }
  evidence_health: {
    artifact_count: number
    evidence_sources: string[]
    cache_meta: any
  }
}

export async function getSystemOverview(): Promise<SystemOverview> {
  try {
    return await request<SystemOverview>('/api/v1/system/overview')
  } catch (err) {
    console.warn('Backend unavailable, falling back to static portfolio evidence:', err)
    return getStaticSystemOverview()
  }
}

export async function getStaticSystemOverview(): Promise<SystemOverview> {
  try {
    // 1. Fetch manifest.json
    const manifestRes = await fetch(staticAsset('evidence/manifest.json'))
    const manifest = manifestRes.ok ? await manifestRes.json() : { baked_at: new Date().toISOString() }

    // 2. Fetch data sources readiness
    let dataSources = { sources: [] }
    try {
      const dsRes = await fetch(staticAsset('evidence/data_source_readiness_snapshot.json'))
      if (dsRes.ok) dataSources = await dsRes.json()
    } catch {
      // ignore
    }

    // 3. Fetch external imagina status
    let imaginaStatus = { exists: false }
    try {
      const imgRes = await fetch(staticAsset('evidence/external_imagina_status.json'))
      if (imgRes.ok) imaginaStatus = await imgRes.json()
    } catch {
      // ignore
    }

    // 4. Fetch latest auto run protocol
    let latestRun = null
    try {
      const runRes = await fetch(staticAsset('evidence/latest_auto_run_protocol.json'))
      if (runRes.ok) latestRun = await runRes.json()
    } catch {
      // ignore
    }

    // 5. Fetch latest fusion validation summary
    let fusionValidation = null
    try {
      const fvRes = await fetch(staticAsset('evidence/latest_fusion_validation_summary.json'))
      if (fvRes.ok) fusionValidation = await fvRes.json()
    } catch {
      // ignore
    }

    const limitations = [
      'Closed-loop from real EEG is disabled by default.',
      'The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.',
      'IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams.',
      'Static evidence is a baked snapshot, not live runtime evidence.',
      'Physical OpenBCI/Galea validation remains unperformed unless a real device report exists.'
    ]

    return {
      source: 'static_snapshot',
      generated_at: manifest.baked_at || new Date().toISOString(),
      warnings: [
        'Static evidence is a baked snapshot, not live runtime evidence. Live streaming is unavailable.',
        'Physical OpenBCI/Galea validation remains unperformed.'
      ],
      limitations,
      closed_loop_allowed: false,
      safety: {
        current_state: 'CLOSED_LOOP_LOCKED',
        severity: 'blocked',
        closed_loop_allowed: false,
        lock_reasons: ['Static snapshot mode does not allow real-time loop transitions.'],
        lock_reason_codes: ['STATIC_MODE_LOCKED'],
        emergency_stop_active: false,
        adaptation_frozen: true,
        evidence_summary: {
          signal_quality_ok: false,
          timing_ok: false,
          validation_report_present: true,
          validation_passed: true,
          brainflow_synthetic_validated: true,
          lsl_synthetic_validated: true,
          physical_hardware_validated: false,
          calibration_complete: true,
          shadow_inference_passed: true
        }
      },
      data_sources: dataSources,
      protocol: {
        latest_run: latestRun
      },
      imagina: {
        external_detected: imaginaStatus.exists || false,
        external_status: imaginaStatus
      },
      fusion: {
        latest_validation: fusionValidation,
        imagina_proxy_status: 'proxy_estimates_only',
        disclaimer: 'IMAGINA exports are experimental imagery proxy artifacts, not decoded thoughts or dreams.'
      },
      evidence_health: {
        artifact_count: manifest.files?.length || 0,
        evidence_sources: (manifest.files || []).map((f: any) => f.name),
        cache_meta: { cache_hit: true, source: 'baked_manifest' }
      }
    }
  } catch (err) {
    console.error('Failed to load static system overview:', err)
    // Absolute minimum fallback
    return {
      source: 'static_snapshot',
      generated_at: new Date().toISOString(),
      warnings: ['All evidence files failed to load.'],
      limitations: ['Closed-loop from real EEG is disabled by default.'],
      closed_loop_allowed: false,
      safety: {
        current_state: 'CLOSED_LOOP_LOCKED',
        severity: 'blocked',
        closed_loop_allowed: false,
        lock_reasons: ['No evidence could be loaded.'],
        lock_reason_codes: ['NO_EVIDENCE'],
        emergency_stop_active: false,
        adaptation_frozen: true,
        evidence_summary: {}
      },
      data_sources: { sources: [] },
      protocol: {},
      imagina: { external_detected: false, external_status: {} },
      fusion: { imagina_proxy_status: 'proxy_estimates_only', disclaimer: '' },
      evidence_health: { artifact_count: 0, evidence_sources: [], cache_meta: {} }
    }
  }
}

