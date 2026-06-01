export interface RuntimeStatus {
  current_session_id?: string | null
  active_estimator?: 'heuristic' | 'learned' | string
  active_model_id?: string | null
  prediction_semantics?: string | null
  current_data_source?: string
  current_dataset_id?: string | null
  current_replay_status?: string | null
  last_safety_decision?: Record<string, unknown> | null
  last_adaptation_action?: Record<string, unknown> | null
  engine_running?: boolean
  engine_session_id?: string | null
  service_status?: string
  backend_version?: string
  environment_mode?: string
  uptime_seconds?: number
  event_counts?: RuntimeMetrics
  websocket?: {
    connected_clients?: number
    dropped_events?: number
  }
  emergency_stop_active?: boolean
  adaptation_frozen?: boolean
  freeze_reason?: string | null
  hardware_validation_state?: string
  latest_hardware_validation_report_id?: string | null
}

export interface RuntimeLatency {
  uptime_seconds?: number
  latency_ms?: Record<
    string,
    {
      count?: number
      mean?: number | null
      p50?: number | null
      p95?: number | null
      p99?: number | null
      max?: number | null
      last_samples?: number[]
    }
  >
}

export interface RuntimeMetrics {
  ticks_processed?: number
  events_emitted?: number
  connected_clients?: number
  dropped_events?: number
  safety_block_rate?: number
  freeze_events?: number
  average_confidence?: number | null
  average_multimodal_sqi?: number | null
  current_tick_rate_hz?: number | null
  average_end_to_end_latency_ms?: number | null
  uptime_seconds?: number
}

export interface AcquisitionStatus {
  active_adapter?: string
  active_config?: Record<string, unknown>
  last_error?: string | null
  optional_dependencies?: Record<string, boolean>
  available_adapters?: Record<
    string,
    {
      status?: Record<string, unknown>
      capabilities?: Record<string, unknown>
    }
  >
}

export interface HardwareValidationStatus {
  state?: string
  active_report_id?: string | null
  last_report_id?: string | null
  closed_loop_allowed?: boolean
  reason?: string
}

export interface HardwareValidationReport {
  report_id?: string
  adapter?: string
  profile_id?: string | null
  passed?: boolean
  closed_loop_allowed?: boolean
  timing?: {
    pass?: boolean
    quality?: string
    expected_rate_hz?: number | null
    observed_rate_hz?: number | null
    drift_percent?: number | null
    jitter_ms_mean?: number | null
    jitter_ms_p50?: number | null
    jitter_ms_p95?: number | null
    jitter_ms_p99?: number | null
    jitter_ms_max?: number | null
    gap_count?: number
    duplicate_count?: number
    monotonic_timestamp_pass?: boolean
    clock_offset_estimate?: number | null
    clock_offset_jitter?: number | null
  }
  channel_mapping?: {
    observed_channel_count?: number
    observed_channel_names?: string[]
    profile_validation?: {
      ok?: boolean
      warnings?: string[]
      errors?: string[]
    } | null
  }
  sqi_summary?: {
    mean?: number | null
    min?: number | null
    max?: number | null
  }
  warnings?: string[]
  failure_reasons?: string[]
  board?: {
    board_name?: string | null
    board_id?: number | string | null
    physical_or_synthetic?: string | null
    serial_port?: string | null
    eeg_channel_indices?: number[]
  }
  markers?: {
    marker_stream_found?: boolean
    marker_count?: number
    marker_labels?: string[]
    markers_per_label?: Record<string, number>
    first_marker_time?: number | null
    last_marker_time?: number | null
    aligned_window_count?: number
    unaligned_marker_count?: number
    marker_alignment_pass?: boolean
    marker_alignment_warnings?: string[]
  }
  artifact_summary?: {
    nan_inf_count?: number
    bad_channel_candidates?: string[]
    mean_peak_to_peak?: number | null
    warnings?: string[]
  }
  stream_metadata?: LslStreamInfo
}

export interface AcquisitionProfileSummary {
  profile_id?: string
  adapter_type?: string
  device_name?: string
  validation?: {
    ok?: boolean
    channel_count?: number
    modalities?: string[]
    warnings?: string[]
    errors?: string[]
  }
}

export interface LslStatus {
  pylsl_available?: boolean
  install_hint?: string | null
  selected_stream?: LslStreamInfo | null
  active_stream_status?: Record<string, unknown>
  last_error?: string | null
}

export interface LslStreamInfo {
  stream_id: string
  name?: string | null
  type?: string | null
  source_id?: string | null
  uid?: string | null
  hostname?: string | null
  channel_count?: number | null
  nominal_srate?: number | null
  channel_format?: string | null
  created_at?: number | null
  metadata_summary?: Record<string, unknown>
  channel_names?: string[]
}

export interface LslStreamsResponse {
  available?: boolean
  install_hint?: string
  streams: LslStreamInfo[]
}

export interface ModelRegistryItem {
  model_id: string
  path?: string
  model_type?: string
  dataset_id?: string
  target?: string
  prediction_semantics?: string
  feature_count?: number
  metrics?: EvaluationReportItem['metrics']
  registered_at?: string
}

export interface ModelListResponse {
  active: RuntimeStatus
  models: ModelRegistryItem[]
}

export interface ModelMetadata extends ModelRegistryItem {
  prediction_semantics?: string
  feature_names?: string[]
  metrics?: Record<string, unknown>
  limitations?: string
  intended_use?: string
  not_intended_use?: string
}

export interface DatasetInfo {
  dataset_id?: string
  name?: string
  source?: string
  config?: string
  local_path?: string | null
  modalities?: string[]
  subjects?: string[]
  sessions?: string[]
  labels?: string[]
  error?: string
}

export interface EvaluationReportItem {
  report_id?: string
  path?: string
  metrics?: {
    accuracy?: number | null
    balanced_accuracy?: number | null
    macro_f1?: number | null
    ece?: number | null
    safety_block_rate?: number | null
  }
  markdown?: string
  report?: null
}

export interface PublicEegReportResponse {
  report: {
    run_id?: string
    fixture_mode?: boolean
    source_mode?: string
    dataset_config?: string | null
    input_file?: string | null
    split_strategy?: string
    model_dir?: string
    closed_loop_allowed?: boolean
    failures?: string[]
    feature_summary?: {
      row_count?: number
      label_distribution?: Record<string, number>
      subject_distribution?: Record<string, number>
      run_distribution?: Record<string, number>
    }
    classifier_metrics?: {
      balanced_accuracy?: number
      macro_f1?: number
      accuracy?: number
      weighted_f1?: number
      split_warnings?: string[]
    }
    classifier_shadow?: {
      accuracy?: number
      predictions?: Array<{
        marker_label?: string
        predicted_label?: string
        confidence?: number | null
      }>
    }
    lsl?: {
      validation?: HardwareValidationReport
      failure?: string
    }
    comparison?: {
      classifier_accuracy?: number | null
      classifier_model_id?: string
      closed_loop_allowed?: boolean
    }
  } | null
  path?: string
  markdown?: string
}

export interface BciBenchmarkResponse {
  report: {
    benchmark_id?: string
    split_strategy?: string
    primary_metric?: string
    binary_left_right?: boolean
    closed_loop_allowed?: boolean
    shape?: number[]
    label_distribution?: Record<string, number>
    leakage_warnings?: string[]
    loso?: {
      available?: boolean
      mean_balanced_accuracy?: number | null
      mean_macro_f1?: number | null
      reason?: string
    }
    filter_summary?: {
      kept_rows?: number
      label_distribution?: Record<string, number>
      subjects?: string[]
      runs?: string[]
    }
    best_model?: {
      model?: string
      model_id?: string
      status?: string
      n_components?: number
      metrics?: {
        accuracy?: number | null
        balanced_accuracy?: number | null
        macro_f1?: number | null
        weighted_f1?: number | null
      }
      bootstrap_confidence_intervals?: {
        available?: boolean
        balanced_accuracy?: {
          lower_95?: number
          upper_95?: number
        }
        macro_f1?: {
          lower_95?: number
          upper_95?: number
        }
      }
    } | null
    models?: Array<{
      model?: string
      status?: string
      n_components?: number
      reason?: string
      metrics?: {
        accuracy?: number | null
        balanced_accuracy?: number | null
        macro_f1?: number | null
      }
    }>
  } | null
  path?: string
  markdown?: string
}

export interface RawBciShadowResponse {
  report: {
    run_id?: string
    mode?: 'live_lsl' | 'fallback_offline' | string
    status?: string
    model_id?: string
    model?: string
    model_type?: string
    markers_seen?: number
    target_markers_seen?: number
    epochs_built?: number
    prediction_count?: number
    missed_epochs?: number
    missed_epoch_reasons?: Record<string, number>
    metrics?: {
      accuracy?: number | null
      balanced_accuracy?: number | null
      macro_f1?: number | null
    }
    closed_loop_allowed?: boolean
    real_adaptation_actions_emitted?: number
    live_lsl_stream_used?: boolean
    fallback_reason?: string | null
  } | null
  path?: string
  markdown?: string
}

export interface BrainflowDeviceDiscovery {
  pyserial_available?: boolean
  devices?: Array<{
    device?: string
    description?: string | null
    manufacturer?: string | null
    vid?: string | null
    pid?: string | null
    likely_openbci?: boolean
  }>
  warnings?: string[]
  next_commands?: Record<string, string>
}

export interface HardwareTrialResponse {
  report: {
    trial_id?: string
    trial_status?: string
    protocol?: string
    profile_id?: string
    physical_device_detected?: boolean
    synthetic_mode?: boolean
    closed_loop_allowed?: boolean
    real_adaptation_actions_emitted?: number
    board?: {
      board_name?: string | null
      board_id?: number | string | null
      serial_port?: string | null
      physical_or_synthetic?: string | null
    }
    validation?: HardwareValidationReport
    alpha_reactivity?: {
      status?: string
      aggregate_alpha_ratio?: number | null
      posterior_alpha_ratio?: number | null
      posterior_channels?: string[]
      warnings?: string[]
    }
    calibration?: {
      calibration_id?: string
      baseline_sqi?: number | null
    }
    shadow?: {
      window_count?: number
      real_adaptation_actions_emitted?: number
      closed_loop_allowed?: boolean
    }
    reason?: string
    next_commands?: Record<string, string>
  } | null
  path?: string
  message?: string
  next_commands?: Record<string, string>
}

export interface SessionSummary {
  session_id: string
  total_events?: number
  safety_block_rate?: number
  action_distribution?: Record<string, number>
  state_averages?: Record<string, number | null>
}

// ---------------------------------------------------------------------------
//  Safety governance
// ---------------------------------------------------------------------------

export interface SafetyGovernanceResult {
  closed_loop_allowed: boolean
  lock_reasons: string[]
  lock_reason_codes: string[]
  required_unlock_conditions: string[]
}

export interface EvidenceCacheMeta {
  cache_hit: boolean
  cached_at: string
  expires_at: string
  ttl_seconds: number
  refresh_count: number
  invalidation_reason?: string | null
}

export interface SafetyEvidenceSummary {
  // Quality booleans
  signal_quality_ok?: boolean
  signal_quality_source?: 'hardware_validation' | 'calibration' | 'shadow' | 'unknown' | string
  signal_quality_note?: string
  timing_ok?: boolean
  calibration_complete?: boolean
  shadow_inference_passed?: boolean
  // Validation flags
  validation_report_present?: boolean
  validation_passed?: boolean
  brainflow_synthetic_validated?: boolean
  lsl_synthetic_validated?: boolean
  lsl_replay_validated?: boolean
  physical_hardware_validated?: boolean
  lsl_live_validation_passed?: boolean
  // SQI
  latest_sqi_mean?: number | null
  latest_sqi_min?: number | null
  best_sqi_mean?: number | null
  best_sqi_min?: number | null
  // Timing
  latest_jitter_p95_ms?: number | null
  latest_drift_percent?: number | null
  best_jitter_p95_ms?: number | null
  // Report paths
  latest_validation_report_path?: string | null
  latest_calibration_report_path?: string | null
  latest_shadow_report_path?: string | null
  latest_physical_trial_report_path?: string | null
  latest_valid_validation_report_path?: string | null
  latest_failed_validation_report_path?: string | null
  safety_audit_report_path?: string | null
  // Provenance
  adapter?: string | null
  evidence_sources?: string[]
  evidence_warnings?: string[]
  note?: string
  // Cache metadata
  evidence_cache?: EvidenceCacheMeta
}

export interface SafetyGovernanceUpdatePayload {
  current_state?: string
  severity?: string
  closed_loop_allowed?: boolean
  lock_reasons?: string[]
  lock_reason_codes?: string[]
  emergency_stop_active?: boolean
  adaptation_frozen?: boolean
  evidence_summary?: SafetyEvidenceSummary
}

export interface SafetyStateResponse {
  state_id: string
  label: string
  description: string
  severity: 'info' | 'warning' | 'blocked' | 'emergency' | string
  allowed_actions: string[]
  blocked_actions: string[]
  required_conditions_to_exit: string[]
  timestamp: string
  session_id?: string | null
  governance?: SafetyGovernanceResult
  evidence_summary?: SafetyEvidenceSummary
  emergency_stop_active?: boolean
  adaptation_frozen?: boolean
}

export interface SafetyTransition {
  transition_id: string
  timestamp: string
  from_state: string
  to_state: string
  reason_code: string
  reason: string
  source: string
  session_id?: string | null
  severity: string
  automatic_or_manual: string
  operator_action?: string | null
}

export interface SafetyBlockedAction {
  record_id: string
  timestamp: string
  action_attempted: string
  reason_code: string
  reason: string
  current_state: string
  severity: string
  source: string
  session_id?: string | null
}

export interface SafetyTimelineResponse {
  timeline: SafetyTransition[]
  total_transitions: number
  timestamp: string
}

export interface SafetyBlockedActionsResponse {
  blocked_actions: SafetyBlockedAction[]
  total_blocked: number
  timestamp: string
}

export interface SafetyClosedLoopResponse extends SafetyGovernanceResult {
  timestamp: string
  note: string
  evidence_summary?: SafetyEvidenceSummary
}

// ---------------------------------------------------------------------------
//  Multimodal Fusion / IMAGINA proxy
// ---------------------------------------------------------------------------

export type FusionSafetyRecommendation = 'allow_shadow' | 'wait' | 'block'

export interface FusionOutput {
  focus_proxy: number
  relaxation_proxy: number
  workload_proxy: number
  stress_arousal_proxy: number
  fatigue_proxy: number
  imagery_engagement_proxy: number
  imagery_quality_proxy?: number | null
  overall_confidence: number
  uncertainty: number
  missing_modalities: string[]
  modality_weights: Record<string, number>
  safety_recommendation: FusionSafetyRecommendation
  safety_reason_codes: string[]
  limitations: string[]
  provenance: Record<string, unknown>
  timestamp: string
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
  proposed_visual_mapping: Record<string, unknown>
  imagina_plugin?: {
    imagery_quality_proxy: number
    imagery_stability_proxy: number
    imagery_engagement_proxy: number
    confidence: number
    limitations: string[]
    not_decoded_content: boolean
    source: string
    provenance: Record<string, unknown>
  } | null
}

export interface FusionDemoSampleResponse {
  output: FusionOutput
  report_paths: {
    json: string
    markdown: string
  }
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
  limitations: string[]
}

export interface FusionStatusResponse {
  available_modalities: string[]
  plugin_status: Record<string, unknown>
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
  limitations: string[]
  provenance: Record<string, unknown>
}

// Fusion adapter types
export interface FusionAdapterStatus {
  adapter_id: string
  modality_id: string
  source_type: string
  available: boolean
  hardware_connected?: boolean
  limitations: string[]
  demo_mode?: boolean
  has_pending?: boolean
  loaded?: boolean
  total_rows?: number
  file_path?: string | null
}

export interface FusionAdaptersResponse {
  adapters: FusionAdapterStatus[]
  adapter_statuses: Record<string, FusionAdapterStatus>
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
  limitations: string[]
}

// Fusion calibration types
export interface FusionCalibrateResponse {
  profile_id: string
  source: string
  report_paths: {
    json: string
    markdown: string
  }
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
  limitations: string[]
  provenance: Record<string, unknown>
}

// Fusion validation types
export interface FusionValidationScenarioResult {
  description: string
  missing_modalities: string[]
  uncertainty: number
  overall_confidence: number
  safety_recommendation: FusionSafetyRecommendation
  safety_reason_codes: string[]
  focus_proxy: number
  relaxation_proxy: number
  workload_proxy: number
  modality_weights: Record<string, number>
}

export interface FusionValidationCheck {
  check: string
  description: string
  passed: boolean
  [key: string]: unknown
}

export interface FusionValidateResponse {
  run_id: string
  all_checks_passed: boolean
  report_dir: string
  artifact_paths: {
    summary_json: string
    summary_md: string
    ablation_csv?: string
  }
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
  limitations: string[]
}

export interface FusionValidationLatestResponse {
  run_id: string
  all_checks_passed: boolean
  report_dir: string
  artifact_paths: {
    summary_json: string
    summary_md: string
  }
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
}

// IMAGINA bridge types
export interface ImaginaManifestValidationResponse {
  valid: boolean
  issues: string[]
  warnings: string[]
  sample_count: number
  dataset_name?: string
  modality?: string
  tasks?: string[]
  labels?: string[]
  not_a_trained_model?: boolean
  limitations: string[]
  proxy_estimates_only: boolean
  closed_loop_allowed: boolean
  manifest_path: string
}

// ---------------------------------------------------------------------------
//  Protocol engine
// ---------------------------------------------------------------------------

export type ProtocolMode = 'simulated' | 'replay' | 'brainflow_synthetic' | 'physical_hardware'
export type ProtocolStepStatus =
  | 'pending'
  | 'running'
  | 'passed'
  | 'failed'
  | 'skipped'
  | 'blocked'
  | 'manual_command_required'

export interface ProtocolStepDefinition {
  step_id: string
  title: string
  description: string
  action: string
  command?: string | null
  required_inputs?: string[]
  optional?: boolean
  produces_artifact?: string | null
  notes?: string | null
}

export interface ProtocolDefinition {
  protocol_id: string
  title: string
  description: string
  mode: ProtocolMode
  steps: ProtocolStepDefinition[]
  required_inputs?: string[]
  generated_artifacts?: string[]
  safety_requirements?: string[]
  closed_loop_allowed_default: boolean
  scientific_limitations?: string
  estimated_duration_seconds?: number
  tags?: string[]
  current_safety_state?: string | null
  closed_loop_allowed?: boolean
  supports_auto_run?: boolean
  auto_run_policy?: string
  reviewer_demo_recommended?: boolean
}

export interface PreflightResult {
  protocol_id: string
  can_start: boolean
  can_auto_run: boolean
  blocking_issues: string[]
  warnings: string[]
  manual_steps: string[]
  executable_steps: string[]
  required_inputs: string[]
  closed_loop_allowed: boolean
  safety_summary?: Record<string, unknown> | null
  auto_run_label?: string
  auto_run_policy?: string
  reviewer_demo_recommended?: boolean
}

export interface ProtocolStepResult {
  step_id: string
  title: string
  status: ProtocolStepStatus
  started_at?: string | null
  completed_at?: string | null
  last_updated_at?: string | null
  artifact_paths?: string[]
  safety_state_snapshot?: Record<string, unknown> | null
  stdout?: string | null
  stderr?: string | null
  error_message?: string | null
  notes?: string | null
  manual_command?: string | null
  block_reason?: string | null
  progress_percent?: number | null
  log_lines?: string[]
  duration_seconds?: number | null
  execution_mode?: string | null
  exit_code?: number | null
  log_file_path?: string | null
}

export interface ProtocolRun {
  run_id: string
  protocol_id: string
  protocol_title: string
  mode: ProtocolMode
  status: ProtocolStepStatus
  overall_status?: ProtocolStepStatus
  current_step_id?: string | null
  created_at: string
  updated_at: string
  completed_at?: string | null
  steps: ProtocolStepResult[]
  inputs?: Record<string, string>
  safety_summary?: Record<string, unknown> | null
  evidence_summary?: Record<string, unknown> | null
  final_report_path?: string | null
  closed_loop_allowed: boolean
  scientific_disclaimer?: string
  is_step_running?: boolean
  // Orchestration state
  auto_advance?: boolean
  orchestration_status?: string
  orchestration_started_at?: string | null
  orchestration_completed_at?: string | null
  orchestration_stop_reason?: string | null
  preflight_result?: PreflightResult | null
  // Auto-completion
  auto_completed?: boolean
  auto_completed_at?: string | null
  protocol_completion_report_path?: string | null
  final_report_generated?: boolean
  final_report_generation_reason?: string | null
}

export interface ProtocolRunSummary {
  run_id: string | null
  protocol_id: string | null
  protocol_title: string | null
  mode: string | null
  status: string | null
  created_at: string | null
  completed_at: string | null
}

// ---------------------------------------------------------------------------
//  Auto-run evidence (from /api/v1/protocol-runs/latest-auto-run)
// ---------------------------------------------------------------------------

export interface StepSummary {
  total: number
  passed: number
  failed: number
  blocked: number
  manual: number
  skipped: number
}

export interface AutoRunEvidence {
  run_id: string
  protocol_id: string
  protocol_title: string
  mode: string
  status: string
  auto_completed: boolean
  auto_completed_at: string | null
  final_report_generated: boolean
  final_report_path: string | null
  protocol_completion_report_path: string | null
  orchestration_status: string
  orchestration_stop_reason?: string | null
  closed_loop_allowed: boolean
  created_at: string | null
  completed_at: string | null
  step_summary: StepSummary
  artifact_paths: string[]
  artifact_count: number
  what_this_proves: string[]
  what_this_does_not_prove: string[]
  scientific_limitations: string
  scientific_disclaimer: string
  safety_summary: Record<string, unknown> | null
  generated_at: string | null
  report_version?: string
}

export type AutoRunEvidenceSource = 'live_backend' | 'static_baked_snapshot'

export interface AutoRunEvidenceSnapshot {
  evidence: AutoRunEvidence
  source: AutoRunEvidenceSource
  detail?: string
}

export interface CompletionReport extends AutoRunEvidence {
  step_timeline: Array<{
    step_id: string
    title: string
    status: string
    started_at: string | null
    completed_at: string | null
    duration_seconds: number | null
    execution_mode: string | null
    artifact_paths: string[]
    log_file_path: string | null
    error_message: string | null
  }>
  all_artifacts: string[]
  evidence_summary: Record<string, unknown> | null
}

// ---------------------------------------------------------------------------
//  Data source readiness assistant
// ---------------------------------------------------------------------------

export type DataSourceMode =
  | 'simulator'
  | 'public_eeg_replay'
  | 'lsl_stream'
  | 'brainflow_synthetic'
  | 'physical_openbci'

export type DataSourceAvailability =
  | 'available'
  | 'partially_available'
  | 'unavailable'
  | 'unknown'

export interface DataSourcePreflightSummary {
  protocol_id: string
  protocol_title?: string | null
  can_start: boolean
  can_auto_run: boolean
  missing_inputs: string[]
  warnings: string[]
  auto_run_policy: string
}

export interface DataSourceStatus {
  source_id: string
  title: string
  mode: DataSourceMode
  description: string
  availability: DataSourceAvailability
  can_run_now: boolean
  can_validate_now: boolean
  can_auto_run_protocol: boolean
  recommended_protocol_id: string
  required_inputs: string[]
  missing_requirements: string[]
  installed_dependencies: Record<string, boolean>
  detected_resources: Record<string, unknown>
  latest_evidence_paths: Record<string, string | null>
  safety_status: Record<string, unknown>
  closed_loop_allowed: boolean
  physical_hardware_validated: boolean
  what_it_proves: string[]
  what_it_does_not_prove: string[]
  limitations: string[]
  next_actions: string[]
  commands: string[]
  protocol_preflight?: DataSourcePreflightSummary | null
}

export interface DataSourceListResponse {
  generated_at: string
  mode: 'live_backend' | 'static_portfolio'
  sources: DataSourceStatus[]
  static_portfolio_note?: string
}

// ---------------------------------------------------------------------------
//  Fusion validation snapshot types
// ---------------------------------------------------------------------------

export interface FusionValidationSnapshot {
  source: 'live_backend' | 'static_baked_snapshot'
  detail?: string
  validation?: FusionValidateResponse | FusionValidationLatestResponse | null
  calibration?: FusionCalibrateResponse | null
  adapters?: FusionAdaptersResponse | null
  manifest?: ImaginaManifestValidationResponse | null
}

