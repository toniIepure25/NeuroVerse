import type { BaseEvent } from '../types/events'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/neurostream'
const RECONNECT_DELAY_MS = 3000
const MAX_RECONNECT_DELAY_MS = 15000

type EventHandler = (event: BaseEvent) => void
type StatusHandler = (status: 'connecting' | 'connected' | 'disconnected' | 'error') => void

class NeuroVerseWebSocket {
  private ws: WebSocket | null = null
  private onEvent: EventHandler | null = null
  private onStatus: StatusHandler | null = null
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private reconnectDelay = RECONNECT_DELAY_MS
  private shouldReconnect = true

  connect(onEvent: EventHandler, onStatus: StatusHandler): void {
    this.onEvent = onEvent
    this.onStatus = onStatus
    this.shouldReconnect = true
    this._connect()
  }

  disconnect(): void {
    this.shouldReconnect = false
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.onStatus?.('disconnected')
  }

  private _connect(): void {
    this.onStatus?.('connecting')
    try {
      this.ws = new WebSocket(WS_URL)
    } catch {
      this.onStatus?.('error')
      this._scheduleReconnect()
      return
    }

    this.ws.onopen = () => {
      this.reconnectDelay = RECONNECT_DELAY_MS
      this.onStatus?.('connected')
    }

    this.ws.onmessage = (msg) => {
      try {
        const data = JSON.parse(msg.data) as BaseEvent
        this.onEvent?.(data)
      } catch {
        // ignore unparseable messages
      }
    }

    this.ws.onerror = () => {
      this.onStatus?.('error')
    }

    this.ws.onclose = () => {
      this.onStatus?.('disconnected')
      this.ws = null
      if (this.shouldReconnect) {
        this._scheduleReconnect()
      }
    }
  }

  private _scheduleReconnect(): void {
    if (this.reconnectTimer) return
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null
      this._connect()
      this.reconnectDelay = Math.min(this.reconnectDelay * 1.5, MAX_RECONNECT_DELAY_MS)
    }, this.reconnectDelay)
  }
}

export const wsClient = new NeuroVerseWebSocket()
