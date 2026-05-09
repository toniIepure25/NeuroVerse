import { useEffect, useState } from 'react'
import { startSession, stopSession } from '../../api/client'
import { wsClient } from '../../api/websocket'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

function connectionDotClass(status: string): string {
  switch (status) {
    case 'connected':
      return 'bg-neuro-success'
    case 'connecting':
      return 'bg-neuro-warning animate-pulse'
    case 'error':
      return 'bg-neuro-danger'
    default:
      return 'bg-neuro-muted'
  }
}

function connectionLabel(status: string): string {
  switch (status) {
    case 'connected':
      return 'Connected'
    case 'connecting':
      return 'Connecting'
    case 'error':
      return 'Error'
    default:
      return 'Disconnected'
  }
}

export function SessionControls() {
  const connection = useNeuroVerseStore((state) => state.connection)
  const session = useNeuroVerseStore((state) => state.session)
  const eventCount = useNeuroVerseStore((state) => state.eventCount)
  const setConnection = useNeuroVerseStore((state) => state.setConnection)
  const setSession = useNeuroVerseStore((state) => state.setSession)
  const handleEvent = useNeuroVerseStore((state) => state.handleEvent)

  const [busy, setBusy] = useState<'start' | 'stop' | null>(null)
  const [apiError, setApiError] = useState<string | null>(null)

  useEffect(() => {
    wsClient.connect(handleEvent, setConnection)
    return () => {
      wsClient.disconnect()
    }
  }, [handleEvent, setConnection])

  async function onStart() {
    setApiError(null)
    setBusy('start')
    try {
      const r = await startSession()
      setSession({ session_id: r.session_id, is_running: true })
    } catch (e) {
      setApiError(e instanceof Error ? e.message : 'Start failed')
    } finally {
      setBusy(null)
    }
  }

  async function onStop() {
    setApiError(null)
    setBusy('stop')
    try {
      const r = await stopSession()
      setSession({
        session_id: r.session_id ?? null,
        is_running: false,
      })
    } catch (e) {
      setApiError(e instanceof Error ? e.message : 'Stop failed')
    } finally {
      setBusy(null)
    }
  }

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 font-sans">
      <h3 className="mb-3 text-sm font-medium text-neuro-text">Session</h3>

      <div className="mb-4 flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={onStart}
          disabled={busy !== null || session.is_running}
          className="rounded-md bg-neuro-success px-4 py-2 text-sm font-medium text-neuro-bg shadow-sm transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {busy === 'start' ? 'Starting…' : 'Start Session'}
        </button>
        <button
          type="button"
          onClick={onStop}
          disabled={busy !== null || !session.is_running}
          className="rounded-md bg-neuro-danger px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {busy === 'stop' ? 'Stopping…' : 'Stop Session'}
        </button>
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-neuro-muted">Session ID</span>
          <span className="break-all font-mono text-xs text-neuro-text">
            {session.session_id ?? '—'}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`h-2.5 w-2.5 shrink-0 rounded-full ${connectionDotClass(connection)}`}
            aria-hidden
          />
          <span className="text-neuro-muted">Connection</span>
          <span className="text-neuro-text">{connectionLabel(connection)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-neuro-muted">Events</span>
          <span className="font-mono tabular-nums text-neuro-text">{eventCount}</span>
        </div>
      </div>

      {apiError && (
        <p className="mt-3 text-xs text-neuro-danger" role="alert">
          {apiError}
        </p>
      )}
    </div>
  )
}
