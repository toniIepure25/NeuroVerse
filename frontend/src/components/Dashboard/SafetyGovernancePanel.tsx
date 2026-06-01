import { useEffect, useRef, useState } from 'react'
import {
  getSafetyState,
  getSafetyTimeline,
  getSafetyBlockedActions,
  getSafetyClosedLoopStatus,
  safetyEmergencyStop,
  safetyFreeze,
  safetyUnfreeze,
  safetyClearEmergency,
  refreshSafetyEvidence,
} from '../../api/client'
import { useNeuroVerseStore } from '../../store/neuroverseStore'
import type {
  SafetyStateResponse,
  SafetyTimelineResponse,
  SafetyBlockedActionsResponse,
  SafetyClosedLoopResponse,
  SafetyEvidenceSummary,
  SafetyGovernanceUpdatePayload,
  EvidenceCacheMeta,
} from '../../types/research'

function severityBadge(severity: string): string {
  switch (severity) {
    case 'emergency':
      return 'bg-red-950/90 text-red-300 ring-red-500/50'
    case 'blocked':
      return 'bg-orange-950/90 text-orange-300 ring-orange-500/50'
    case 'warning':
      return 'bg-amber-950/90 text-amber-300 ring-amber-500/40'
    default:
      return 'bg-emerald-950/90 text-emerald-300 ring-emerald-500/40'
  }
}

function relativeTime(ts: string): string {
  try {
    const diff = (Date.now() - new Date(ts).getTime()) / 1000
    if (diff < 60) return `${Math.round(diff)}s ago`
    if (diff < 3600) return `${Math.round(diff / 60)}m ago`
    return `${Math.round(diff / 3600)}h ago`
  } catch {
    return ts
  }
}

function shortPath(p: string | null | undefined): string {
  if (!p) return '—'
  // Show just the last 2 path segments for readability
  const parts = p.replace(/\\/g, '/').split('/')
  return parts.slice(-2).join('/')
}

function BoolBadge({ ok, label }: { ok?: boolean; label: string }) {
  return (
    <span className={`inline-flex items-center rounded px-1.5 py-0.5 text-[10px] font-medium ${
      ok ? 'bg-emerald-950/60 text-emerald-400' : 'bg-red-950/40 text-neuro-danger/80'
    }`}>
      {ok ? '✓' : '✗'} {label}
    </span>
  )
}

function SqiDisplay({ ev }: { ev: SafetyEvidenceSummary }) {
  const displaySqi = ev.best_sqi_mean ?? ev.latest_sqi_mean
  const source = ev.signal_quality_source
  if (displaySqi == null && !source) return null
  return (
    <dl className="grid grid-cols-2 gap-x-3 gap-y-0.5 text-[10px]">
      {displaySqi != null && (
        <>
          <dt className="text-neuro-muted">
            {ev.best_sqi_mean != null ? 'Best SQI' : 'SQI mean'}
            {source && source !== 'unknown' ? (
              <span className="ml-1 text-neuro-border">({source.replace('_', ' ')})</span>
            ) : null}
          </dt>
          <dd className="text-neuro-text font-mono">{displaySqi.toFixed(3)}</dd>
        </>
      )}
      {(ev.best_jitter_p95_ms ?? ev.latest_jitter_p95_ms) != null && (
        <>
          <dt className="text-neuro-muted">
            {ev.best_jitter_p95_ms != null ? 'Best jitter p95' : 'Jitter p95'}
          </dt>
          <dd className="text-neuro-text font-mono">
            {((ev.best_jitter_p95_ms ?? ev.latest_jitter_p95_ms) as number).toFixed(3)} ms
          </dd>
        </>
      )}
    </dl>
  )
}

function EvidenceSummaryBlock({ ev }: { ev: SafetyEvidenceSummary }) {
  return (
    <div className="mt-2 space-y-2">
      <div className="flex flex-wrap gap-1">
        <BoolBadge ok={ev.validation_passed} label="HW validated" />
        <BoolBadge ok={ev.calibration_complete} label="Calibrated" />
        <BoolBadge ok={ev.shadow_inference_passed} label="Shadow passed" />
        <BoolBadge ok={ev.signal_quality_ok} label="SQI ok" />
        <BoolBadge ok={ev.timing_ok} label="Timing ok" />
        <BoolBadge ok={ev.lsl_live_validation_passed} label="LSL valid" />
      </div>

      <div className="flex flex-wrap gap-1">
        {ev.brainflow_synthetic_validated && (
          <span className="inline-flex rounded px-1.5 py-0.5 text-[10px] bg-blue-950/40 text-blue-400">
            BrainFlow synthetic ✓
          </span>
        )}
        {ev.lsl_synthetic_validated && (
          <span className="inline-flex rounded px-1.5 py-0.5 text-[10px] bg-blue-950/40 text-blue-400">
            LSL synthetic ✓
          </span>
        )}
        {ev.lsl_replay_validated && (
          <span className="inline-flex rounded px-1.5 py-0.5 text-[10px] bg-blue-950/40 text-blue-400">
            LSL replay ✓
          </span>
        )}
        {ev.physical_hardware_validated ? (
          <span className="inline-flex rounded px-1.5 py-0.5 text-[10px] bg-amber-950/60 text-amber-300">
            Physical HW ✓
          </span>
        ) : (
          <span className="inline-flex rounded px-1.5 py-0.5 text-[10px] bg-neuro-bg text-neuro-muted">
            Physical HW unvalidated
          </span>
        )}
      </div>

      <SqiDisplay ev={ev} />

      {/* Evidence warnings */}
      {ev.evidence_warnings && ev.evidence_warnings.length > 0 && (
        <div className="rounded border border-amber-700/40 bg-amber-950/20 px-2 py-1">
          {ev.evidence_warnings.map((w, i) => (
            <p key={i} className="text-[10px] text-amber-400">⚠ {w}</p>
          ))}
        </div>
      )}

      {/* Evidence sources */}
      {ev.evidence_sources && ev.evidence_sources.length > 0 && (
        <details>
          <summary className="cursor-pointer text-[10px] text-neuro-accent">
            Evidence sources ({ev.evidence_sources.length})
          </summary>
          <ul className="mt-1 space-y-0.5 pl-2">
            {ev.evidence_sources.map((s, i) => (
              <li key={i} className="text-[10px] font-mono text-neuro-muted">{s}</li>
            ))}
          </ul>
        </details>
      )}

      <div className="space-y-0.5 text-[10px]">
        {/* Show valid path when latest failed */}
        {ev.latest_failed_validation_report_path && ev.latest_valid_validation_report_path && (
          <p className="text-amber-400/80">
            <span className="text-neuro-border">HW (valid): </span>
            <code>{shortPath(ev.latest_valid_validation_report_path)}</code>
          </p>
        )}
        {ev.latest_validation_report_path && !ev.latest_failed_validation_report_path && (
          <p className="text-neuro-muted">
            <span className="text-neuro-border">HW: </span>
            <code className="text-neuro-muted">{shortPath(ev.latest_validation_report_path)}</code>
          </p>
        )}
        {ev.latest_calibration_report_path && (
          <p className="text-neuro-muted">
            <span className="text-neuro-border">Cal: </span>
            <code className="text-neuro-muted">{shortPath(ev.latest_calibration_report_path)}</code>
          </p>
        )}
        {ev.latest_shadow_report_path && (
          <p className="text-neuro-muted">
            <span className="text-neuro-border">Shadow: </span>
            <code className="text-neuro-muted">{shortPath(ev.latest_shadow_report_path)}</code>
          </p>
        )}
        {ev.safety_audit_report_path && (
          <p className="text-neuro-muted">
            <span className="text-neuro-border">Audit: </span>
            <code className="text-neuro-muted">{shortPath(ev.safety_audit_report_path)}</code>
          </p>
        )}
      </div>
    </div>
  )
}

function CacheStatusBar({
  meta,
  onRefresh,
  busy,
}: {
  meta: EvidenceCacheMeta | null | undefined
  onRefresh: () => void
  busy: boolean
}) {
  if (!meta) return null
  const isHit = meta.cache_hit
  const refreshCount = meta.refresh_count ?? 0
  const cachedAt = meta.cached_at ? new Date(meta.cached_at).toLocaleTimeString() : '—'
  return (
    <div className="flex items-center justify-between gap-2 rounded border border-neuro-border/50 bg-neuro-bg/40 px-2 py-1">
      <div className="flex items-center gap-2 text-[10px] text-neuro-muted">
        <span
          className={`rounded px-1 py-0.5 font-medium ${
            isHit
              ? 'bg-blue-950/40 text-blue-400'
              : 'bg-emerald-950/40 text-emerald-400'
          }`}
        >
          {isHit ? 'cached' : 'fresh'}
        </span>
        <span>at {cachedAt}</span>
        <span className="text-neuro-border">·</span>
        <span>{refreshCount}× refreshed</span>
        {meta.invalidation_reason && (
          <>
            <span className="text-neuro-border">·</span>
            <span className="text-amber-400/70 truncate max-w-[120px]" title={meta.invalidation_reason}>
              inv: {meta.invalidation_reason.slice(0, 20)}
            </span>
          </>
        )}
      </div>
      <button
        type="button"
        onClick={onRefresh}
        disabled={busy}
        className="rounded border border-neuro-border px-1.5 py-0.5 text-[10px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
      >
        {busy ? '…' : 'Refresh evidence'}
      </button>
    </div>
  )
}

export function SafetyGovernancePanel() {
  const [state, setState] = useState<SafetyStateResponse | null>(null)
  const [timeline, setTimeline] = useState<SafetyTimelineResponse | null>(null)
  const [blocked, setBlocked] = useState<SafetyBlockedActionsResponse | null>(null)
  const [closedLoop, setClosedLoop] = useState<SafetyClosedLoopResponse | null>(null)
  const [busy, setBusy] = useState<string | null>(null)
  const [refreshingEvidence, setRefreshingEvidence] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const governanceUpdate = useNeuroVerseStore((s) => s.governanceUpdate)
  const prevGovernanceUpdate = useRef<SafetyGovernanceUpdatePayload | null>(null)

  async function refresh() {
    try {
      setError(null)
      const [stateData, timelineData, blockedData, clData] = await Promise.all([
        getSafetyState(),
        getSafetyTimeline(15),
        getSafetyBlockedActions(10),
        getSafetyClosedLoopStatus(),
      ])
      setState(stateData)
      setTimeline(timelineData)
      setBlocked(blockedData)
      setClosedLoop(clData)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Safety governance unavailable')
    }
  }

  async function onEvidenceRefresh() {
    setRefreshingEvidence(true)
    setError(null)
    try {
      await refreshSafetyEvidence()
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Evidence refresh failed')
    } finally {
      setRefreshingEvidence(false)
    }
  }

  async function onControl(action: 'emergency' | 'freeze' | 'unfreeze' | 'clear') {
    setBusy(action)
    setError(null)
    try {
      if (action === 'emergency') await safetyEmergencyStop()
      if (action === 'freeze') await safetyFreeze()
      if (action === 'unfreeze') await safetyUnfreeze()
      if (action === 'clear') await safetyClearEmergency()
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : `Action ${action} failed`)
    } finally {
      setBusy(null)
    }
  }

  useEffect(() => {
    void refresh()
    const timer = window.setInterval(() => void refresh(), 15000)
    return () => window.clearInterval(timer)
  }, [])

  // Trigger immediate refresh when a WS governance update arrives
  useEffect(() => {
    if (governanceUpdate && governanceUpdate !== prevGovernanceUpdate.current) {
      prevGovernanceUpdate.current = governanceUpdate
      void refresh()
    }
  }, [governanceUpdate])

  const severity = state?.severity ?? 'info'
  const isEmergency = state?.emergency_stop_active
  const isFrozen = state?.adaptation_frozen
  const ev = state?.evidence_summary ?? closedLoop?.evidence_summary
  const cacheMeta = ev?.evidence_cache ?? null

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 font-sans flex flex-col gap-4">
      <div className="flex items-center justify-between gap-2">
        <h3 className="text-sm font-medium text-neuro-text">Safety Governance</h3>
        <button
          type="button"
          onClick={() => void refresh()}
          className="rounded border border-neuro-border px-2 py-1 text-xs text-neuro-muted hover:text-neuro-text"
        >
          Refresh
        </button>
      </div>

      {/* Disclaimer */}
      <p className="rounded-md border border-neuro-border bg-neuro-bg/60 p-2 text-[11px] leading-relaxed text-neuro-muted">
        Closed-loop from real EEG is disabled by default. NeuroVerse uses record-only validation
        and shadow-only inference unless explicitly validated and configured.
      </p>

      {/* Evidence cache status */}
      <CacheStatusBar
        meta={cacheMeta}
        onRefresh={() => void onEvidenceRefresh()}
        busy={refreshingEvidence}
      />

      {/* Current safety state */}
      <section className="rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Safety State
        </p>
        {state ? (
          <>
            <div className="mb-2 flex items-center gap-2">
              <span
                className={`inline-flex rounded px-2 py-0.5 text-xs font-semibold ring-1 ${severityBadge(severity)}`}
              >
                {state.state_id}
              </span>
              <span className="text-xs text-neuro-muted">{state.label}</span>
            </div>
            <p className="mb-2 text-[11px] text-neuro-muted">{state.description}</p>
            <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
              <dt className="text-neuro-muted">Severity</dt>
              <dd className="text-neuro-text">{severity}</dd>
              <dt className="text-neuro-muted">Emergency stop</dt>
              <dd className={isEmergency ? 'text-neuro-danger' : 'text-neuro-text'}>
                {isEmergency ? 'ACTIVE' : 'no'}
              </dd>
              <dt className="text-neuro-muted">Frozen</dt>
              <dd className={isFrozen ? 'text-amber-400' : 'text-neuro-text'}>
                {isFrozen ? 'yes' : 'no'}
              </dd>
            </dl>
            {state.allowed_actions.length > 0 && (
              <div className="mt-2">
                <p className="text-[10px] uppercase tracking-wide text-neuro-muted mb-1">Allowed</p>
                <div className="flex flex-wrap gap-1">
                  {state.allowed_actions.map((a) => (
                    <span key={a} className="rounded bg-emerald-950/40 px-1.5 py-0.5 text-[10px] text-emerald-400">
                      {a}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {state.blocked_actions.length > 0 && (
              <div className="mt-2">
                <p className="text-[10px] uppercase tracking-wide text-neuro-muted mb-1">Blocked</p>
                <div className="flex flex-wrap gap-1">
                  {state.blocked_actions.map((a) => (
                    <span key={a} className="rounded bg-red-950/40 px-1.5 py-0.5 text-[10px] text-neuro-danger">
                      {a}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <p className="text-xs text-neuro-muted">Loading safety state…</p>
        )}

        {/* Controls */}
        <div className="mt-3 grid grid-cols-2 gap-2">
          <button
            type="button"
            onClick={() => void onControl('emergency')}
            disabled={busy !== null || isEmergency}
            className="rounded bg-neuro-danger px-2 py-1.5 text-[11px] font-medium text-white disabled:opacity-40"
          >
            Emergency Stop
          </button>
          <button
            type="button"
            onClick={() => void onControl('freeze')}
            disabled={busy !== null || isFrozen}
            className="rounded border border-neuro-border px-2 py-1.5 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Freeze
          </button>
          <button
            type="button"
            onClick={() => void onControl('unfreeze')}
            disabled={busy !== null || isEmergency || !isFrozen}
            className="rounded border border-neuro-border px-2 py-1.5 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Unfreeze
          </button>
          <button
            type="button"
            onClick={() => void onControl('clear')}
            disabled={busy !== null || !isEmergency}
            className="rounded border border-amber-700/50 px-2 py-1.5 text-[11px] text-amber-400 hover:text-amber-300 disabled:opacity-40"
          >
            Clear Emergency
          </button>
        </div>
      </section>

      {/* Closed-loop governance */}
      <section className="rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Closed-Loop Lock
        </p>
        {closedLoop ? (
          <>
            <div className="mb-2 flex items-center gap-2">
              <span
                className={`inline-flex rounded px-2 py-0.5 text-xs font-semibold ring-1 ${
                  closedLoop.closed_loop_allowed
                    ? 'bg-emerald-950/80 text-emerald-300 ring-emerald-500/40'
                    : 'bg-red-950/80 text-neuro-danger ring-red-500/40'
                }`}
              >
                {closedLoop.closed_loop_allowed ? 'UNLOCKED' : 'LOCKED'}
              </span>
            </div>
            {closedLoop.lock_reasons.length > 0 && (
              <div className="mb-2">
                <p className="text-[10px] uppercase tracking-wide text-neuro-muted mb-1">
                  Lock reasons
                </p>
                <ul className="space-y-0.5 border-l-2 border-neuro-danger/40 pl-2">
                  {closedLoop.lock_reasons.slice(0, 4).map((r, i) => (
                    <li key={i} className="text-[11px] text-neuro-muted">{r}</li>
                  ))}
                  {closedLoop.lock_reasons.length > 4 && (
                    <li className="text-[11px] text-neuro-muted">
                      +{closedLoop.lock_reasons.length - 4} more
                    </li>
                  )}
                </ul>
              </div>
            )}
            {closedLoop.required_unlock_conditions.length > 0 && (
              <details>
                <summary className="cursor-pointer text-[11px] text-neuro-accent">
                  Required unlock conditions ({closedLoop.required_unlock_conditions.length})
                </summary>
                <ul className="mt-1 space-y-0.5 pl-2">
                  {closedLoop.required_unlock_conditions.map((c, i) => (
                    <li key={i} className="text-[11px] text-neuro-muted">{c}</li>
                  ))}
                </ul>
              </details>
            )}
          </>
        ) : (
          <p className="text-xs text-neuro-muted">Loading governance status…</p>
        )}
      </section>

      {/* Evidence provenance */}
      {ev && (
        <section className="rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
          <p className="mb-1 text-xs font-medium uppercase tracking-wide text-neuro-muted">
            Evidence Provenance
          </p>
          <p className="text-[10px] text-neuro-muted mb-2">
            Derived from latest disk reports. BrainFlow Synthetic and LSL synthetic do not
            constitute physical hardware validation.
          </p>
          <EvidenceSummaryBlock ev={ev} />
        </section>
      )}

      {/* State transition timeline */}
      <section className="rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Safety Timeline
          {timeline && (
            <span className="ml-2 text-[10px] text-neuro-border">
              ({timeline.total_transitions} total)
            </span>
          )}
        </p>
        {timeline && timeline.timeline.length > 0 ? (
          <ol className="space-y-1.5">
            {timeline.timeline
              .slice()
              .reverse()
              .slice(0, 8)
              .map((t) => (
                <li key={t.transition_id} className="flex items-start gap-2 text-[11px]">
                  <span className="mt-0.5 shrink-0 text-neuro-border">
                    {relativeTime(t.timestamp)}
                  </span>
                  <span className="min-w-0">
                    <span className="font-mono text-neuro-muted">{t.from_state}</span>
                    <span className="mx-1 text-neuro-border">→</span>
                    <span
                      className={`font-mono ${
                        t.severity === 'emergency'
                          ? 'text-neuro-danger'
                          : t.severity === 'blocked'
                            ? 'text-amber-400'
                            : 'text-neuro-text'
                      }`}
                    >
                      {t.to_state}
                    </span>
                    {t.reason && (
                      <span className="ml-1 text-neuro-muted truncate">
                        · {t.reason.slice(0, 60)}
                      </span>
                    )}
                  </span>
                </li>
              ))}
          </ol>
        ) : (
          <p className="text-xs text-neuro-muted">
            {timeline ? 'No transitions recorded yet.' : 'Loading timeline…'}
          </p>
        )}
      </section>

      {/* Blocked actions */}
      {blocked && blocked.blocked_actions.length > 0 && (
        <section className="rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
          <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
            Blocked Actions ({blocked.total_blocked} total)
          </p>
          <ul className="space-y-1.5">
            {blocked.blocked_actions.slice(0, 5).map((b) => (
              <li key={b.record_id} className="flex items-start gap-2 text-[11px]">
                <span className="mt-0.5 shrink-0 text-neuro-border">
                  {relativeTime(b.timestamp)}
                </span>
                <span className="min-w-0">
                  <span className="font-mono text-neuro-danger">{b.action_attempted}</span>
                  <span className="ml-1 text-neuro-muted">· {b.reason_code}</span>
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {error && (
        <p className="text-xs text-neuro-danger" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
