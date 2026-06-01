import { useEffect, useMemo, useState } from 'react'
import {
  generateFusionDemoSample,
  getFusionStatus,
  getLatestFusion,
} from '../../api/client'
import type { FusionOutput, FusionStatusResponse } from '../../types/research'

function pct(value?: number | null): string {
  if (value == null || Number.isNaN(value)) return '—'
  return `${Math.round(value * 100)}%`
}

function shortPath(path?: string | null): string {
  if (!path) return '—'
  return path.replace(/\\/g, '/').split('/').slice(-4).join('/')
}

function tone(recommendation?: string): string {
  if (recommendation === 'allow_shadow') return 'text-emerald-400'
  if (recommendation === 'wait') return 'text-amber-400'
  return 'text-neuro-danger'
}

export function FusionPanel() {
  const [status, setStatus] = useState<FusionStatusResponse | null>(null)
  const [output, setOutput] = useState<FusionOutput | null>(null)
  const [reportPath, setReportPath] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function refresh() {
    try {
      setError(null)
      const fusionStatus = await getFusionStatus()
      setStatus(fusionStatus)
      try {
        const latest = await getLatestFusion()
        setOutput(latest.output)
      } catch {
        // No latest fusion sample yet.
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Fusion status unavailable')
    }
  }

  async function onDemoSample() {
    setBusy(true)
    setError(null)
    try {
      const sample = await generateFusionDemoSample()
      setOutput(sample.output)
      setReportPath(sample.report_paths?.json ?? null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Fusion demo sample failed')
    } finally {
      setBusy(false)
    }
  }

  useEffect(() => {
    void refresh()
  }, [])

  const mapping = useMemo(
    () => output?.proposed_visual_mapping?.parameters as Record<string, number> | undefined,
    [output],
  )

  return (
    <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
      <div className="mb-2 flex items-center justify-between gap-2">
        <p className="text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Multimodal Fusion / IMAGINA Proxy
        </p>
        <button
          type="button"
          onClick={() => void onDemoSample()}
          disabled={busy}
          className="rounded border border-neuro-border px-2 py-1 text-xs text-neuro-muted hover:text-neuro-text disabled:opacity-40"
        >
          {busy ? 'Generating' : 'Demo Sample'}
        </button>
      </div>

      <div className="mb-2 flex flex-wrap gap-1.5 text-[10px]">
        {(status?.available_modalities ?? ['eeg', 'gaze', 'physiology', 'self_report', 'imagina']).map((modality) => (
          <span
            key={modality}
            className={`rounded px-1.5 py-0.5 ${
              output?.missing_modalities?.includes(modality)
                ? 'bg-neuro-surface text-neuro-muted'
                : 'bg-emerald-950/40 text-emerald-400'
            }`}
          >
            {modality.replace('_', ' ')}
          </span>
        ))}
      </div>

      {output ? (
        <div className="space-y-2 text-xs">
          <dl className="grid grid-cols-2 gap-x-3 gap-y-1">
            <dt className="text-neuro-muted">Focus proxy</dt>
            <dd className="text-neuro-text">{pct(output.focus_proxy)}</dd>
            <dt className="text-neuro-muted">Relaxation proxy</dt>
            <dd className="text-neuro-text">{pct(output.relaxation_proxy)}</dd>
            <dt className="text-neuro-muted">Workload proxy</dt>
            <dd className="text-neuro-text">{pct(output.workload_proxy)}</dd>
            <dt className="text-neuro-muted">Stress/arousal proxy</dt>
            <dd className="text-neuro-text">{pct(output.stress_arousal_proxy)}</dd>
            <dt className="text-neuro-muted">Fatigue proxy</dt>
            <dd className="text-neuro-text">{pct(output.fatigue_proxy)}</dd>
            <dt className="text-neuro-muted">Imagery engagement</dt>
            <dd className="text-neuro-text">{pct(output.imagery_engagement_proxy)}</dd>
            <dt className="text-neuro-muted">Imagery quality</dt>
            <dd className="text-neuro-text">{pct(output.imagery_quality_proxy)}</dd>
            <dt className="text-neuro-muted">Uncertainty</dt>
            <dd className="text-neuro-text">{pct(output.uncertainty)}</dd>
            <dt className="text-neuro-muted">Confidence</dt>
            <dd className="text-neuro-text">{pct(output.overall_confidence)}</dd>
            <dt className="text-neuro-muted">Safety</dt>
            <dd className={tone(output.safety_recommendation)}>{output.safety_recommendation}</dd>
          </dl>

          {mapping && (
            <p className="text-[11px] text-neuro-muted">
              Proposed shadow mapping: clarity {pct(mapping.clarity)}, glow {pct(mapping.symbolic_object_glow)},
              intensity cap {pct(output.proposed_visual_mapping?.intensity_cap as number)}
            </p>
          )}
          <p className="text-[11px] text-neuro-muted">
            Weights: {Object.entries(output.modality_weights).map(([k, v]) => `${k} ${pct(v)}`).join(' · ') || '—'}
          </p>
          <p className="text-[11px] text-neuro-muted">
            Missing: {output.missing_modalities.length ? output.missing_modalities.join(', ') : 'none'}
          </p>
          {reportPath && (
            <p className="text-[11px] text-emerald-400">Report: {shortPath(reportPath)}</p>
          )}
        </div>
      ) : (
        <p className="text-xs text-neuro-muted">No fusion sample yet.</p>
      )}

      <p className="mt-2 text-[11px] leading-relaxed text-neuro-muted">
        Multimodal fusion outputs are experimental proxy estimates, not clinical or unrestricted
        mental-state measurements. The corridor is not a decoded mental image. Closed-loop from
        real EEG is disabled by default. IMAGINA plugin outputs are imagery-quality proxies, not
        decoded thoughts or dreams.
      </p>
      {error && <p className="mt-2 text-xs text-neuro-danger">{error}</p>}
    </section>
  )
}

