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
