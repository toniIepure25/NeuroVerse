export interface BaseEvent {
  event_id: string
  session_id: string
  event_type: string
  timestamp: number
  source: string
  correlation_id?: string
  payload: Record<string, unknown>
  metadata?: Record<string, unknown>
}

export interface StatePredictionPayload {
  focus: number
  relaxation: number
  workload: number
  stress: number
  fatigue: number
  imagery_engagement: number
  confidence: number
  model_version: string
  feature_window_ms: number
}

export interface SafetyDecisionPayload {
  decision: 'ALLOWED' | 'BLOCKED' | 'WAIT' | 'ASK'
  reason: string
  sqi_scores: Record<string, number>
  confidence: number
  blocked_actions: string[]
  safety_level: 'normal' | 'caution' | 'freeze'
}

export interface AdaptationActionPayload {
  action: string
  intensity: number
  duration_ms: number
  source_state: string
  reason: string
  parameters: Record<string, unknown>
}

export interface FeaturePayload {
  eeg: Record<string, number>
  physio: Record<string, number>
  gaze: Record<string, number>
  multimodal: Record<string, number>
  sqi_scores: Record<string, number>
}
