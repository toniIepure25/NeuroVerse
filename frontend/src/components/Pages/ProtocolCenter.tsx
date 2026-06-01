import { useEffect, useRef, useState } from 'react'
import {
  cancelProtocolStep,
  completeProtocolRun,
  createProtocolRun,
  getProtocolCompletionReport,
  getProtocolRun,
  listProtocolRuns,
  listProtocols,
  runAllProtocolSteps,
  runProtocolStep,
  stopProtocolOrchestration,
  streamProtocolRunStatus,
} from '../../api/client'
import type {
  CompletionReport,
  PreflightResult,
  ProtocolDefinition,
  ProtocolRun,
  ProtocolRunSummary,
  ProtocolStepResult,
  ProtocolStepStatus,
} from '../../types/research'

const PROTOCOL_CENTER_HANDOFF_KEY = 'neuroverse.protocolCenter.activeRunId'

// ---------------------------------------------------------------------------
//  Helpers
// ---------------------------------------------------------------------------

function modeBadge(mode: string): string {
  switch (mode) {
    case 'simulated': return 'bg-emerald-950/60 text-emerald-400'
    case 'replay': return 'bg-blue-950/60 text-blue-400'
    case 'brainflow_synthetic': return 'bg-indigo-950/60 text-indigo-400'
    case 'physical_hardware': return 'bg-amber-950/60 text-amber-300'
    default: return 'bg-neuro-bg text-neuro-muted'
  }
}

function orchStatusColor(status: string | undefined): string {
  switch (status) {
    case 'running': return 'text-blue-400'
    case 'completed': return 'text-emerald-400'
    case 'stopped_failed': return 'text-neuro-danger'
    case 'stopped_blocked': return 'text-amber-400'
    case 'stopped_manual_required': return 'text-indigo-400'
    case 'cancelled': return 'text-neuro-muted'
    default: return 'text-neuro-muted'
  }
}

function orchStatusLabel(status: string | undefined): string {
  switch (status) {
    case 'running': return 'Orchestrating…'
    case 'completed': return 'All steps completed'
    case 'stopped_failed': return 'Stopped — step failed'
    case 'stopped_blocked': return 'Stopped — step blocked'
    case 'stopped_manual_required': return 'Stopped — manual step required'
    case 'cancelled': return 'Cancelled by user'
    case 'idle': return ''
    default: return ''
  }
}

function stepStatusIcon(status: ProtocolStepStatus): string {
  switch (status) {
    case 'passed': return '✓'
    case 'failed': return '✗'
    case 'running': return '▷'
    case 'skipped': return '—'
    case 'blocked': return '⊘'
    case 'manual_command_required': return '⚙'
    default: return '○'
  }
}

function stepStatusColor(status: ProtocolStepStatus | string): string {
  switch (status) {
    case 'passed': return 'text-emerald-400'
    case 'failed': return 'text-neuro-danger'
    case 'running': return 'text-blue-400'
    case 'blocked': return 'text-amber-400'
    case 'manual_command_required': return 'text-indigo-400'
    default: return 'text-neuro-muted'
  }
}

function shortPath(p: string | null | undefined): string {
  if (!p) return '—'
  return p.replace(/\\/g, '/').split('/').slice(-3).join('/')
}

function fmtDuration(s: number | null | undefined): string {
  if (s == null) return ''
  if (s < 60) return `${s.toFixed(1)}s`
  return `${Math.floor(s / 60)}m ${(s % 60).toFixed(0)}s`
}

function stepCounts(steps: ProtocolStepResult[]) {
  return {
    passed: steps.filter(s => s.status === 'passed').length,
    failed: steps.filter(s => s.status === 'failed').length,
    blocked: steps.filter(s => s.status === 'blocked').length,
    manual: steps.filter(s => s.status === 'manual_command_required').length,
    running: steps.filter(s => s.status === 'running').length,
    pending: steps.filter(s => s.status === 'pending').length,
    total: steps.length,
  }
}

// ---------------------------------------------------------------------------
//  Sub-components
// ---------------------------------------------------------------------------

function PreflightPanel({ pf, onRunAll }: {
  pf: PreflightResult
  onRunAll: () => void
}) {
  const hasIssues = pf.blocking_issues.length > 0
  const hasWarnings = pf.warnings.length > 0

  return (
    <div className={`rounded border px-3 py-2.5 text-[11px] space-y-1.5 ${
      hasIssues
        ? 'border-neuro-danger/50 bg-red-950/20'
        : hasWarnings
        ? 'border-amber-500/30 bg-amber-950/10'
        : 'border-emerald-500/30 bg-emerald-950/10'
    }`}>
      <div className="flex items-center justify-between gap-3">
        <span className="font-semibold text-neuro-text">
          {pf.reviewer_demo_recommended && (
            <span className="mr-1.5 rounded bg-emerald-900/60 px-1.5 py-0.5 text-[9px] text-emerald-400">
              ★ DEMO
            </span>
          )}
          Preflight
          <span className={`ml-2 ${hasIssues ? 'text-neuro-danger' : pf.can_auto_run ? 'text-emerald-400' : 'text-amber-400'}`}>
            {hasIssues ? 'BLOCKED' : pf.can_auto_run ? 'READY' : 'PARTIAL'}
          </span>
        </span>

        {pf.can_auto_run && !hasIssues && (
          <button
            type="button"
            onClick={onRunAll}
            className="rounded bg-emerald-800/60 px-2.5 py-1 text-[10px] font-medium text-emerald-300 hover:bg-emerald-700/60 transition-colors"
          >
            {pf.auto_run_label || 'Run All Steps'}
          </button>
        )}
      </div>

      {hasIssues && (
        <ul className="space-y-0.5">
          {pf.blocking_issues.map((issue, i) => (
            <li key={i} className="text-neuro-danger">✗ {issue}</li>
          ))}
        </ul>
      )}
      {hasWarnings && (
        <ul className="space-y-0.5">
          {pf.warnings.slice(0, 3).map((w, i) => (
            <li key={i} className="text-amber-400/80">! {w}</li>
          ))}
        </ul>
      )}
      <div className="text-neuro-muted/70 flex gap-3">
        <span>{pf.executable_steps.length} executable</span>
        {pf.manual_steps.length > 0 && (
          <span className="text-indigo-400/80">{pf.manual_steps.length} manual</span>
        )}
      </div>
    </div>
  )
}

function ProtocolCard({ protocol, onStart, busy }: {
  protocol: ProtocolDefinition
  onStart: (p: ProtocolDefinition) => void
  busy: boolean
}) {
  const needsPort = protocol.required_inputs?.includes('PORT')
  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 flex flex-col gap-3">
      <div>
        <div className="flex items-center gap-2 mb-0.5">
          <p className="text-sm font-semibold text-neuro-text">{protocol.title}</p>
          {protocol.reviewer_demo_recommended && (
            <span className="rounded bg-emerald-900/50 px-1.5 py-0.5 text-[9px] text-emerald-400 font-medium">
              ★ DEMO
            </span>
          )}
        </div>
        <p className="text-[11px] text-neuro-muted">{protocol.description}</p>
      </div>

      <div className="flex flex-wrap gap-1.5 text-[10px]">
        <span className={`rounded px-1.5 py-0.5 font-medium ${modeBadge(protocol.mode)}`}>
          {protocol.mode.replace('_', ' ')}
        </span>
        <span className="rounded bg-neuro-bg px-1.5 py-0.5 text-neuro-muted">
          ~{protocol.estimated_duration_seconds}s
        </span>
        <span className="rounded bg-red-950/40 px-1.5 py-0.5 text-neuro-danger">CL locked</span>
        {protocol.supports_auto_run && (
          <span className="rounded bg-emerald-950/40 px-1.5 py-0.5 text-emerald-400">
            {protocol.auto_run_policy === 'full' ? '▶ auto-run' : '▶ partial auto'}
          </span>
        )}
        {needsPort && (
          <span className="rounded bg-amber-950/40 px-1.5 py-0.5 text-amber-400">
            requires PORT
          </span>
        )}
      </div>

      <div className="text-[10px] text-neuro-muted">
        {protocol.steps.length} steps · {protocol.tags?.slice(0, 3).join(', ') || 'no tags'}
      </div>

      <button
        type="button"
        onClick={() => onStart(protocol)}
        disabled={busy}
        className="w-full rounded bg-neuro-accent/80 px-3 py-1.5 text-xs font-medium text-white hover:bg-neuro-accent disabled:opacity-40"
      >
        {busy ? 'Starting…' : 'Start Protocol'}
      </button>
    </div>
  )
}

function LogTail({ lines }: { lines: string[] | undefined }) {
  if (!lines || lines.length === 0) return null
  return (
    <pre className="mt-1 max-h-20 overflow-y-auto rounded bg-neuro-bg px-2 py-1 text-[9px] text-neuro-muted font-mono leading-relaxed">
      {lines.slice(-6).join('\n')}
    </pre>
  )
}

function StepRow({ step, anyRunning, onRun, onCancel }: {
  step: ProtocolStepResult
  anyRunning: boolean
  onRun: (stepId: string) => void
  onCancel: (stepId: string) => void
}) {
  const isRunning = step.status === 'running'
  return (
    <div className="flex items-start gap-2 py-2 border-b border-neuro-border/40 last:border-0">
      <span className={`text-sm shrink-0 mt-0.5 ${stepStatusColor(step.status)} ${isRunning ? 'animate-pulse' : ''}`}>
        {stepStatusIcon(step.status)}
      </span>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <p className="text-xs text-neuro-text">{step.title}</p>
          {step.execution_mode && step.status !== 'pending' && (
            <span className="text-[9px] text-neuro-muted bg-neuro-bg rounded px-1">
              {step.execution_mode.replace('_', ' ')}
            </span>
          )}
          {step.duration_seconds != null && step.status !== 'running' && (
            <span className="text-[9px] text-neuro-muted">{fmtDuration(step.duration_seconds)}</span>
          )}
        </div>

        {isRunning && (
          <div className="mt-1 h-0.5 w-full rounded bg-neuro-border overflow-hidden">
            <div
              className="h-full bg-blue-500 transition-all duration-500"
              style={{ width: step.progress_percent != null ? `${step.progress_percent}%` : '55%' }}
            />
          </div>
        )}

        {step.error_message && (
          <p className="text-[11px] text-neuro-danger mt-0.5">{step.error_message}</p>
        )}
        {step.block_reason && (
          <p className="text-[11px] text-amber-400 mt-0.5">⊘ {step.block_reason}</p>
        )}
        {step.manual_command && (
          <code className="block text-[10px] text-indigo-400 mt-1 bg-neuro-bg rounded px-1.5 py-0.5 break-all">
            {step.manual_command}
          </code>
        )}

        {(isRunning || step.status === 'failed') && <LogTail lines={step.log_lines} />}

        {step.artifact_paths?.map(p => (
          <p key={p} className="text-[10px] text-neuro-muted mt-0.5">📄 {shortPath(p)}</p>
        ))}
      </div>

      <div className="shrink-0 flex flex-col gap-1">
        {step.status === 'pending' && (
          <button
            type="button"
            onClick={() => onRun(step.step_id)}
            disabled={anyRunning}
            className="rounded border border-neuro-border px-2 py-0.5 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Run
          </button>
        )}
        {isRunning && (
          <button
            type="button"
            onClick={() => onCancel(step.step_id)}
            className="rounded border border-neuro-danger/50 px-2 py-0.5 text-[11px] text-neuro-danger hover:bg-red-950/30"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  )
}

function CompletionReportPanel({ run }: { run: ProtocolRun }) {
  const [report, setReport] = useState<CompletionReport | null>(null)

  // Fetch backend completion report when the run is finished
  useEffect(() => {
    if (!run.final_report_generated || !run.run_id) return
    getProtocolCompletionReport(run.run_id)
      .then(setReport)
      .catch(() => {
        // Fallback: report not yet generated — panel will use local fallback
      })
  }, [run.run_id, run.final_report_generated])

  if (!run.auto_completed && !run.final_report_generated) return null

  // Use backend data when available, fallback to mode-derived content
  const proves: string[] = report?.what_this_proves.length
    ? report.what_this_proves
    : run.mode === 'simulated'
    ? [
        'Full pipeline validated end-to-end (simulator → calibration → shadow → audit → report)',
        'Safety gate confirmed: closed-loop adaptation blocked by default',
        'Protocol orchestration, evidence aggregation, and report generation all function correctly',
      ]
    : run.mode === 'brainflow_synthetic'
    ? [
        'BrainFlow SyntheticBoard integration through the acquisition layer',
        'Hardware ingestion pipeline validated with synthetic EEG data',
        'Safety gate confirmed: no closed-loop adaptation emitted',
      ]
    : ['Protocol steps executed and evidence collected.']

  const notProves: string[] = report?.what_this_does_not_prove.length
    ? report.what_this_does_not_prove
    : [
        'Real EEG neural dynamics (signals are simulated or synthetic)',
        'Closed-loop adaptation — explicitly locked by safety gate',
        'Clinical performance or mental-state inference accuracy',
        'Thought reading or dream decoding of any kind',
      ]

  return (
    <div className="rounded border border-emerald-500/30 bg-emerald-950/10 px-3 py-3 space-y-2 text-[11px]">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-emerald-400 font-semibold">
          ✓ {run.auto_completed ? 'Auto-Completed' : 'Final Report Generated'}
        </span>
        <span className="rounded bg-red-950/40 px-1.5 py-0.5 text-neuro-danger text-[9px]">
          closed_loop_allowed: false
        </span>
        {report && (
          <span className="text-[9px] text-neuro-muted">source: backend report v{report.report_version}</span>
        )}
      </div>

      {run.protocol_completion_report_path && (
        <p className="text-neuro-muted/80">
          📄 <code className="text-[9px]">{shortPath(run.protocol_completion_report_path)}</code>
        </p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-1">
        <div>
          <p className="text-emerald-400/80 font-medium mb-1">✓ What this run proves</p>
          {proves.map((p, i) => (
            <p key={i} className="text-neuro-muted/80 leading-relaxed">• {p}</p>
          ))}
        </div>
        <div>
          <p className="text-neuro-danger/80 font-medium mb-1">✗ What this run does not prove</p>
          {notProves.map((p, i) => (
            <p key={i} className="text-neuro-muted/80 leading-relaxed">• {p}</p>
          ))}
        </div>
      </div>
    </div>
  )
}

function OrchestrationBanner({ run, onRunAll, onStop }: {
  run: ProtocolRun
  onRunAll: () => void
  onStop: () => void
}) {
  const status = run.orchestration_status ?? 'idle'
  const isRunning = status === 'running'
  const label = orchStatusLabel(status)

  if (status === 'idle' && !run.auto_advance) return null

  return (
    <div className={`rounded border px-3 py-2 text-[11px] flex items-center justify-between gap-3 ${
      isRunning
        ? 'border-blue-500/30 bg-blue-950/20'
        : status === 'completed'
        ? 'border-emerald-500/30 bg-emerald-950/10'
        : status === 'stopped_failed'
        ? 'border-neuro-danger/30 bg-red-950/10'
        : status === 'stopped_manual_required'
        ? 'border-indigo-500/30 bg-indigo-950/10'
        : 'border-neuro-border bg-neuro-bg/40'
    }`}>
      <div className="flex-1 min-w-0">
        <span className={`font-medium ${orchStatusColor(status)}`}>
          {isRunning && <span className="animate-pulse mr-1">●</span>}
          {label}
        </span>
        {run.orchestration_stop_reason && !isRunning && (
          <p className="text-neuro-muted/80 mt-0.5 truncate">{run.orchestration_stop_reason}</p>
        )}
      </div>
      {isRunning && (
        <button
          type="button"
          onClick={onStop}
          className="rounded border border-neuro-danger/50 px-2 py-0.5 text-[10px] text-neuro-danger hover:bg-red-950/30 shrink-0"
        >
          Stop
        </button>
      )}
      {!isRunning && status !== 'completed' && status !== 'idle' && (
        <button
          type="button"
          onClick={onRunAll}
          className="rounded border border-neuro-border px-2 py-0.5 text-[10px] text-neuro-muted hover:text-neuro-text shrink-0"
        >
          Resume
        </button>
      )}
    </div>
  )
}

function ProgressSummary({ steps }: { steps: ProtocolStepResult[] }) {
  const c = stepCounts(steps)
  return (
    <div className="flex gap-3 text-[10px] text-neuro-muted flex-wrap">
      {c.passed > 0 && <span className="text-emerald-400">✓ {c.passed} passed</span>}
      {c.running > 0 && <span className="text-blue-400 animate-pulse">▷ {c.running} running</span>}
      {c.failed > 0 && <span className="text-neuro-danger">✗ {c.failed} failed</span>}
      {c.blocked > 0 && <span className="text-amber-400">⊘ {c.blocked} blocked</span>}
      {c.manual > 0 && <span className="text-indigo-400">⚙ {c.manual} manual</span>}
      {c.pending > 0 && <span>○ {c.pending} pending</span>}
    </div>
  )
}

function RunPanel({ run, onRunStep, onCancelStep, onRunAll, onStop, onComplete, anyRunning, busy }: {
  run: ProtocolRun
  onRunStep: (stepId: string) => void
  onCancelStep: (stepId: string) => void
  onRunAll: () => void
  onStop: () => void
  onComplete: () => void
  anyRunning: boolean
  busy: boolean
}) {
  const overall = run.overall_status ?? run.status
  const orchStatus = run.orchestration_status ?? 'idle'
  const pf = run.preflight_result

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 flex flex-col gap-3">
      {/* Header */}
      <div className="flex items-center justify-between gap-2">
        <div>
          <p className="text-sm font-semibold text-neuro-text">{run.protocol_title}</p>
          <p className="text-[10px] text-neuro-muted font-mono">{run.run_id}</p>
        </div>
        <div className="flex items-center gap-2">
          {anyRunning && <span className="text-[10px] text-blue-400 animate-pulse">● running</span>}
          <span className={`text-[11px] rounded px-2 py-0.5 ${stepStatusColor(overall as ProtocolStepStatus)}`}>
            {overall}
          </span>
        </div>
      </div>

      {/* Safety lock */}
      <div className="text-[10px] rounded border border-neuro-border/50 bg-neuro-bg/40 px-2 py-1.5 flex items-center gap-2">
        <span className="text-neuro-danger font-medium">🔒</span>
        <span className="text-neuro-muted">
          Closed-loop from real EEG is disabled by default.{' '}
          <span className="text-neuro-danger">closed_loop_allowed: false</span>
        </span>
      </div>

      {/* Preflight (if available from run creation) */}
      {pf && (
        <PreflightPanel
          pf={pf as unknown as PreflightResult}
          onRunAll={onRunAll}
        />
      )}

      {/* Orchestration banner */}
      <OrchestrationBanner run={run} onRunAll={onRunAll} onStop={onStop} />

      {/* Completion report panel — shown after auto-complete */}
      <CompletionReportPanel run={run} />

      {/* Progress summary */}
      <ProgressSummary steps={run.steps} />

      {/* Steps */}
      <div className="flex flex-col">
        {run.steps.map(step => (
          <StepRow
            key={step.step_id}
            step={step}
            anyRunning={anyRunning}
            onRun={onRunStep}
            onCancel={onCancelStep}
          />
        ))}
      </div>

      {/* Actions */}
      <div className="flex gap-2 flex-wrap">
        {/* Run All button (if preflight not shown already) */}
        {!pf && pf !== null && (
          <button
            type="button"
            onClick={onRunAll}
            disabled={anyRunning || busy}
            className="rounded bg-emerald-800/60 px-3 py-1 text-xs text-emerald-300 hover:bg-emerald-700/60 disabled:opacity-40"
          >
            Run All Steps
          </button>
        )}

        <button
          type="button"
          onClick={onComplete}
          disabled={busy || anyRunning}
          title={anyRunning ? 'Wait for running step to finish' : undefined}
          className="rounded border border-neuro-border px-3 py-1 text-xs text-neuro-muted hover:text-neuro-text disabled:opacity-40"
        >
          {anyRunning ? 'Step running…' : 'Complete & Save Report'}
        </button>
      </div>

      {run.final_report_path && (
        <p className="text-[10px] text-emerald-400">
          Report saved: <code>{shortPath(run.final_report_path)}</code>
        </p>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
//  Main Protocol Center page
// ---------------------------------------------------------------------------

export function ProtocolCenter() {
  const [protocols, setProtocols] = useState<ProtocolDefinition[]>([])
  const [runs, setRuns] = useState<ProtocolRunSummary[]>([])
  const [activeRun, setActiveRun] = useState<ProtocolRun | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sseCleanupRef = useRef<(() => void) | null>(null)
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const anyRunning =
    (activeRun?.is_step_running === true) ||
    (activeRun?.orchestration_status === 'running') ||
    (activeRun?.steps.some(s => s.status === 'running') ?? false)

  // ---------------------------------------------------------------------------
  //  Streaming / polling
  // ---------------------------------------------------------------------------

  function stopStreaming() {
    if (sseCleanupRef.current) { sseCleanupRef.current(); sseCleanupRef.current = null }
    if (pollingRef.current !== null) { clearInterval(pollingRef.current); pollingRef.current = null }
  }

  function startPolling(runId: string) {
    if (pollingRef.current !== null) return
    pollingRef.current = setInterval(async () => {
      try {
        const updated = await getProtocolRun(runId)
        setActiveRun(updated)
        const stillRunning =
          updated.is_step_running === true ||
          updated.orchestration_status === 'running' ||
          updated.steps.some(s => s.status === 'running')
        if (!stillRunning) { clearInterval(pollingRef.current!); pollingRef.current = null }
      } catch {
        clearInterval(pollingRef.current!); pollingRef.current = null
      }
    }, 1500)
  }

  function startStreaming(runId: string) {
    stopStreaming()
    let sseWorking = false
    const cleanup = streamProtocolRunStatus(
      runId,
      (_data) => {
        sseWorking = true
        getProtocolRun(runId).then(setActiveRun).catch(() => {})
      },
      () => { getProtocolRun(runId).then(setActiveRun).catch(() => {}) },
      () => { if (!sseWorking) startPolling(runId) },
    )
    sseCleanupRef.current = cleanup
    setTimeout(() => {
      if (!sseWorking && activeRun?.run_id === runId) startPolling(runId)
    }, 3000)
  }

  useEffect(() => {
    if (!activeRun) { stopStreaming(); return }
    if (anyRunning) { startStreaming(activeRun.run_id) }
    else { stopStreaming() }
    return stopStreaming
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeRun?.run_id, anyRunning])

  useEffect(() => () => stopStreaming(), [])

  // ---------------------------------------------------------------------------
  //  Data fetching
  // ---------------------------------------------------------------------------

  async function refresh() {
    try {
      const [pl, rl] = await Promise.all([listProtocols(), listProtocolRuns()])
      setProtocols(pl)
      setRuns(rl)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Protocol center unavailable')
    }
  }

  useEffect(() => { void refresh() }, [])

  useEffect(() => {
    const handoffRunId = window.localStorage.getItem(PROTOCOL_CENTER_HANDOFF_KEY)
    if (!handoffRunId) return

    let cancelled = false
    window.localStorage.removeItem(PROTOCOL_CENTER_HANDOFF_KEY)
    setError(null)
    getProtocolRun(handoffRunId)
      .then((run) => {
        if (!cancelled) setActiveRun(run)
      })
      .catch((e) => {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : `Failed to open run ${handoffRunId}`)
        }
      })
    return () => { cancelled = true }
  }, [])

  // ---------------------------------------------------------------------------
  //  Actions
  // ---------------------------------------------------------------------------

  async function onStart(protocol: ProtocolDefinition) {
    setBusy(true)
    setError(null)
    try {
      const run = await createProtocolRun(protocol.protocol_id)
      setActiveRun(run)
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start protocol')
    } finally {
      setBusy(false)
    }
  }

  async function onRunStep(stepId: string) {
    if (!activeRun) return
    setError(null)
    try {
      await runProtocolStep(activeRun.run_id, stepId)
      const updated = await getProtocolRun(activeRun.run_id)
      setActiveRun(updated)
    } catch (e) {
      const msg = e instanceof Error ? e.message : `Step ${stepId} failed`
      setError(msg)
      try { setActiveRun(await getProtocolRun(activeRun.run_id)) } catch { /* ignore */ }
    }
  }

  async function onCancelStep(stepId: string) {
    if (!activeRun) return
    setError(null)
    try { await cancelProtocolStep(activeRun.run_id, stepId) } catch (e) {
      setError(e instanceof Error ? e.message : 'Cancel failed')
    }
  }

  async function onRunAll() {
    if (!activeRun) return
    setError(null)
    try {
      await runAllProtocolSteps(activeRun.run_id)
      const updated = await getProtocolRun(activeRun.run_id)
      setActiveRun(updated)
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Run-all failed'
      setError(msg)
      try { setActiveRun(await getProtocolRun(activeRun.run_id)) } catch { /* ignore */ }
    }
  }

  async function onStop() {
    if (!activeRun) return
    setError(null)
    try {
      await stopProtocolOrchestration(activeRun.run_id)
      const updated = await getProtocolRun(activeRun.run_id)
      setActiveRun(updated)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Stop failed')
    }
  }

  async function onComplete() {
    if (!activeRun) return
    setBusy(true)
    setError(null)
    try {
      await completeProtocolRun(activeRun.run_id)
      const updated = await getProtocolRun(activeRun.run_id)
      setActiveRun(updated)
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Complete failed')
    } finally {
      setBusy(false)
    }
  }

  // ---------------------------------------------------------------------------
  //  Render
  // ---------------------------------------------------------------------------

  return (
    <div className="flex h-full flex-col overflow-y-auto bg-neuro-bg p-8 text-neuro-text">
      <div className="mx-auto max-w-5xl space-y-10 pb-16">
        <header className="space-y-3">
          <h1 className="text-4xl font-extrabold tracking-tight text-white">Protocol Center</h1>
          <p className="max-w-3xl text-neuro-muted">
            Choose a predefined protocol to run the NeuroVerse pipeline step-by-step.
            Protocols marked <span className="text-emerald-400">★ DEMO</span> support one-click
            auto-run and are recommended for reviewer demonstrations.
          </p>
          <div className="rounded-md border border-neuro-border bg-neuro-surface px-4 py-2 text-[11px] text-neuro-muted">
            <strong className="text-neuro-danger">Closed-loop from real EEG is disabled by default.</strong>{' '}
            All protocols run in shadow-only or record-only mode.
            Physical hardware steps require an explicit serial PORT and remain record-only.
          </div>
        </header>

        {/* Active run */}
        {activeRun && (
          <section className="space-y-3">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-white">Active Run</h2>
              <button
                type="button"
                onClick={() => { stopStreaming(); setActiveRun(null) }}
                className="text-xs text-neuro-muted hover:text-neuro-text"
              >
                Dismiss
              </button>
            </div>
            <RunPanel
              run={activeRun}
              onRunStep={onRunStep}
              onCancelStep={onCancelStep}
              onRunAll={onRunAll}
              onStop={onStop}
              onComplete={onComplete}
              anyRunning={anyRunning}
              busy={busy}
            />
          </section>
        )}

        {/* Protocol library */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white border-b border-neuro-border pb-2 flex-1">
              Available Protocols
            </h2>
            <button
              type="button"
              onClick={() => void refresh()}
              className="ml-4 text-xs text-neuro-muted hover:text-neuro-text"
            >
              Refresh
            </button>
          </div>
          {protocols.length === 0 ? (
            <p className="text-neuro-muted">Loading protocols…</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {protocols.map(p => (
                <ProtocolCard key={p.protocol_id} protocol={p} onStart={onStart} busy={busy} />
              ))}
            </div>
          )}
        </section>

        {/* Recent runs */}
        {runs.length > 0 && (
          <section className="space-y-3">
            <h2 className="text-xl font-bold text-white border-b border-neuro-border pb-2">
              Recent Protocol Runs
            </h2>
            <div className="space-y-2">
              {runs.slice(0, 8).map(r => (
                <div
                  key={r.run_id ?? ''}
                  className="flex items-center justify-between rounded border border-neuro-border bg-neuro-surface px-4 py-2 text-xs"
                >
                  <div>
                    <span className="font-medium text-neuro-text">{r.protocol_title ?? '—'}</span>
                    <span className="ml-2 text-neuro-muted font-mono">{r.run_id ?? ''}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={stepStatusColor((r.status ?? 'pending') as ProtocolStepStatus)}>
                      {r.status ?? 'pending'}
                    </span>
                    <span className="text-neuro-muted">{r.mode ?? '—'}</span>
                    <button
                      type="button"
                      onClick={async () => {
                        try { setActiveRun(await getProtocolRun(r.run_id!)) }
                        catch (e) { setError(e instanceof Error ? e.message : 'Load failed') }
                      }}
                      className="text-neuro-muted hover:text-neuro-accent"
                    >
                      Open
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {error && (
          <p
            className="rounded-md border border-neuro-danger/50 bg-red-950/20 px-4 py-2 text-sm text-neuro-danger"
            role="alert"
          >
            {error}
          </p>
        )}

        <p className="rounded-md border border-neuro-border bg-neuro-bg/60 p-4 text-[11px] leading-relaxed text-neuro-muted">
          The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.
          Hardware validation confirms stream quality and software integration; it does not validate clinical or
          unrestricted mental-state inference. Physical OpenBCI/Galea hardware remains unvalidated unless
          a real device report is present.
        </p>
      </div>
    </div>
  )
}
