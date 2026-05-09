import { create } from 'zustand'
import type {
  AdaptationActionPayload,
  BaseEvent,
  FeaturePayload,
  SafetyDecisionPayload,
  StatePredictionPayload,
} from '../types/events'
import type { ConnectionStatus, EnvironmentState, SessionInfo } from '../types/state'

interface TimelineEntry {
  timestamp: number
  type: string
  summary: string
}

interface NeuroVerseState {
  connection: ConnectionStatus
  session: SessionInfo
  cognitiveState: StatePredictionPayload | null
  safetyState: SafetyDecisionPayload | null
  adaptationAction: AdaptationActionPayload | null
  features: FeaturePayload | null
  environment: EnvironmentState
  timeline: TimelineEntry[]
  eventCount: number

  setConnection: (status: ConnectionStatus) => void
  setSession: (info: SessionInfo) => void
  handleEvent: (event: BaseEvent) => void
  reset: () => void
}

const DEFAULT_ENV: EnvironmentState = {
  fogDensity: 0.5,
  lightIntensity: 0.5,
  particleCount: 200,
  motionSpeed: 0.5,
  objectGlow: 0,
  frozen: false,
}

function applyAdaptation(env: EnvironmentState, action: AdaptationActionPayload): EnvironmentState {
  const i = action.intensity
  switch (action.action) {
    case 'IncreaseSceneClarity':
      return { ...env, fogDensity: Math.max(0.05, env.fogDensity - i * 0.3), lightIntensity: Math.min(1, env.lightIntensity + i * 0.2), frozen: false }
    case 'SmoothEnvironmentMotion':
      return { ...env, motionSpeed: Math.max(0.05, env.motionSpeed - i * 0.3), frozen: false }
    case 'SimplifyEnvironment':
      return { ...env, particleCount: Math.max(20, 200 - i * 150), fogDensity: Math.min(1, env.fogDensity + i * 0.1), frozen: false }
    case 'StabilizeVisualField':
      return { ...env, motionSpeed: Math.max(0.02, env.motionSpeed - i * 0.4), frozen: false }
    case 'GenerateSymbolicObject':
      return { ...env, objectGlow: Math.min(1, i * 0.9), frozen: false }
    case 'ReduceVisualComplexity':
      return { ...env, particleCount: Math.max(20, 200 - i * 120), motionSpeed: Math.max(0.1, env.motionSpeed - i * 0.2), frozen: false }
    case 'FreezeAdaptation':
      return { ...env, frozen: true }
    case 'MaintainBaseline':
    default:
      return { ...env, frozen: false }
  }
}

function summarizeEvent(event: BaseEvent): string {
  const p = event.payload
  switch (event.event_type) {
    case 'neuroverse.state.predicted': {
      const s = p as unknown as StatePredictionPayload
      return `Focus ${(s.focus * 100).toFixed(0)}% | Stress ${(s.stress * 100).toFixed(0)}%`
    }
    case 'neuroverse.safety.decision': {
      const d = p as unknown as SafetyDecisionPayload
      return `${d.decision}: ${d.reason}`
    }
    case 'neuroverse.adaptation.action': {
      const a = p as unknown as AdaptationActionPayload
      return `${a.action} (${(a.intensity * 100).toFixed(0)}%)`
    }
    default:
      return event.event_type.split('.').pop() || event.event_type
  }
}

export const useNeuroVerseStore = create<NeuroVerseState>((set) => ({
  connection: 'disconnected',
  session: { session_id: null, is_running: false },
  cognitiveState: null,
  safetyState: null,
  adaptationAction: null,
  features: null,
  environment: { ...DEFAULT_ENV },
  timeline: [],
  eventCount: 0,

  setConnection: (status) => set({ connection: status }),

  setSession: (info) => set({ session: info }),

  handleEvent: (event) =>
    set((state) => {
      const entry: TimelineEntry = {
        timestamp: event.timestamp,
        type: event.event_type,
        summary: summarizeEvent(event),
      }
      const timeline = [entry, ...state.timeline].slice(0, 100)
      const eventCount = state.eventCount + 1

      switch (event.event_type) {
        case 'neuroverse.state.predicted':
          return { cognitiveState: event.payload as unknown as StatePredictionPayload, timeline, eventCount }
        case 'neuroverse.safety.decision':
          return { safetyState: event.payload as unknown as SafetyDecisionPayload, timeline, eventCount }
        case 'neuroverse.adaptation.action': {
          const action = event.payload as unknown as AdaptationActionPayload
          return {
            adaptationAction: action,
            environment: applyAdaptation(state.environment, action),
            timeline,
            eventCount,
          }
        }
        case 'neuroverse.features.extracted':
          return { features: event.payload as unknown as FeaturePayload, timeline, eventCount }
        default:
          return { timeline, eventCount }
      }
    }),

  reset: () =>
    set({
      cognitiveState: null,
      safetyState: null,
      adaptationAction: null,
      features: null,
      environment: { ...DEFAULT_ENV },
      timeline: [],
      eventCount: 0,
    }),
}))
