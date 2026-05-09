export type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error'

export interface SessionInfo {
  session_id: string | null
  is_running: boolean
}

export interface EnvironmentState {
  fogDensity: number
  lightIntensity: number
  particleCount: number
  motionSpeed: number
  objectGlow: number
  frozen: boolean
}
