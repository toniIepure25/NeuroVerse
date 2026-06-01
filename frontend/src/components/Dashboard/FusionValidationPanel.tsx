import { useEffect, useState } from 'react'
import {
  getFusionAdapters,
  getLatestFusionValidation,
  runFusionCalibration,
  runFusionValidation,
  validateImaginaManifest,
} from '../../api/client'
import type {
  FusionAdaptersResponse,
  FusionCalibrateResponse,
  FusionValidateResponse,
  FusionValidationLatestResponse,
  ImaginaManifestValidationResponse,
} from '../../types/research'

function shortPath(path?: string | null): string {
  if (!path) return '—'
  return path.replace(/\\/g, '/').split('/').slice(-3).join('/')
}

type FusionValidationTab = 'adapters' | 'validation' | 'imagina'

export function FusionValidationPanel() {
  const [tab, setTab] = useState<FusionValidationTab>('validation')
  const [adapters, setAdapters] = useState<FusionAdaptersResponse | null>(null)
  const [validation, setValidation] = useState<FusionValidateResponse | null>(null)
  const [latestValidation, setLatestValidation] = useState<FusionValidationLatestResponse | null>(null)
  const [calibration, setCalibration] = useState<FusionCalibrateResponse | null>(null)
  const [imaginaResult, setImaginaResult] = useState<ImaginaManifestValidationResponse | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function loadAdapters() {
    try {
      const data = await getFusionAdapters()
      setAdapters(data)
    } catch {
      // silent
    }
  }

  async function loadLatestValidation() {
    try {
      const data = await getLatestFusionValidation()
      setLatestValidation(data)
    } catch {
      // No latest validation yet
    }
  }

  useEffect(() => {
    void loadAdapters()
    void loadLatestValidation()
  }, [])

  async function onRunValidation() {
    setBusy(true)
    setError(null)
    try {
      const result = await runFusionValidation()
      setValidation(result)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Fusion validation failed')
    } finally {
      setBusy(false)
    }
  }

  async function onRunCalibration() {
    setBusy(true)
    setError(null)
    try {
      const result = await runFusionCalibration()
      setCalibration(result)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Fusion calibration failed')
    } finally {
      setBusy(false)
    }
  }

  async function onValidateImagina() {
    setBusy(true)
    setError(null)
    try {
      const result = await validateImaginaManifest()
      setImaginaResult(result)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'IMAGINA manifest validation failed')
    } finally {
      setBusy(false)
    }
  }

  const tabClasses = (t: FusionValidationTab) =>
    `px-2 py-1 text-[11px] rounded ${
      tab === t
        ? 'bg-neuro-accent/20 text-neuro-accent border border-neuro-accent/30'
        : 'text-neuro-muted hover:text-neuro-text border border-neuro-border'
    }`

  return (
    <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
      <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
        Fusion Validation &amp; Adapters
      </p>

      {/* Tab bar */}
      <div className="mb-3 flex gap-1.5">
        <button type="button" className={tabClasses('validation')} onClick={() => setTab('validation')}>
          Validation
        </button>
        <button type="button" className={tabClasses('adapters')} onClick={() => setTab('adapters')}>
          Adapters
        </button>
        <button type="button" className={tabClasses('imagina')} onClick={() => setTab('imagina')}>
          IMAGINA Bridge
        </button>
      </div>

      {/* Validation Tab */}
      {tab === 'validation' && (
        <div className="space-y-2">
          <div className="flex gap-1.5">
            <button
              type="button"
              onClick={() => void onRunValidation()}
              disabled={busy}
              className="rounded border border-neuro-border px-2 py-1 text-xs text-neuro-muted hover:text-neuro-text disabled:opacity-40"
            >
              {busy ? 'Running...' : 'Run Validation'}
            </button>
            <button
              type="button"
              onClick={() => void onRunCalibration()}
              disabled={busy}
              className="rounded border border-neuro-border px-2 py-1 text-xs text-neuro-muted hover:text-neuro-text disabled:opacity-40"
            >
              {busy ? 'Running...' : 'Calibrate'}
            </button>
          </div>

          {validation && (
            <div className="rounded border border-neuro-border bg-neuro-surface/40 p-2 text-xs">
              <div className="mb-1 flex items-center gap-2">
                <span className={validation.all_checks_passed ? 'text-emerald-400' : 'text-neuro-danger'}>
                  {validation.all_checks_passed ? '✅ All checks passed' : '❌ Some checks failed'}
                </span>
                <span className="text-neuro-muted">Run: {validation.run_id}</span>
              </div>
              <p className="text-[11px] text-neuro-muted">
                Summary: {shortPath(validation.artifact_paths.summary_md)}
              </p>
              {validation.artifact_paths.ablation_csv && (
                <p className="text-[11px] text-neuro-muted">
                  Ablation: {shortPath(validation.artifact_paths.ablation_csv)}
                </p>
              )}
            </div>
          )}

          {!validation && latestValidation && (
            <div className="rounded border border-neuro-border bg-neuro-surface/40 p-2 text-xs">
              <div className="mb-1 flex items-center gap-2">
                <span className={latestValidation.all_checks_passed ? 'text-emerald-400' : 'text-neuro-danger'}>
                  {latestValidation.all_checks_passed ? '✅ Latest passed' : '❌ Latest had failures'}
                </span>
                <span className="text-neuro-muted">Run: {latestValidation.run_id}</span>
              </div>
            </div>
          )}

          {calibration && (
            <div className="rounded border border-neuro-border bg-neuro-surface/40 p-2 text-xs">
              <p className="text-emerald-400">Calibration profile: {calibration.profile_id}</p>
              <p className="text-[11px] text-neuro-muted">
                Report: {shortPath(calibration.report_paths.json)}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Adapters Tab */}
      {tab === 'adapters' && (
        <div className="space-y-1.5">
          {adapters?.adapters.map((a) => (
            <div
              key={a.adapter_id}
              className="flex items-center justify-between rounded border border-neuro-border bg-neuro-surface/40 px-2 py-1 text-xs"
            >
              <div>
                <span className="text-neuro-text">{a.adapter_id}</span>
                <span className="ml-1.5 text-neuro-muted">({a.modality_id})</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={`text-[10px] rounded px-1.5 py-0.5 ${
                  a.source_type === 'simulated'
                    ? 'bg-amber-950/40 text-amber-400'
                    : a.source_type === 'user_input'
                    ? 'bg-blue-950/40 text-blue-400'
                    : 'bg-neuro-surface text-neuro-muted'
                }`}>
                  {a.source_type}
                </span>
                <span className={a.available ? 'text-emerald-400' : 'text-neuro-danger'}>
                  {a.available ? '●' : '○'}
                </span>
              </div>
            </div>
          ))}
          {!adapters && <p className="text-xs text-neuro-muted">Loading adapters…</p>}
        </div>
      )}

      {/* IMAGINA Bridge Tab */}
      {tab === 'imagina' && (
        <div className="space-y-2">
          <button
            type="button"
            onClick={() => void onValidateImagina()}
            disabled={busy}
            className="rounded border border-neuro-border px-2 py-1 text-xs text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            {busy ? 'Validating...' : 'Validate Example Manifest'}
          </button>

          {imaginaResult && (
            <div className="rounded border border-neuro-border bg-neuro-surface/40 p-2 text-xs">
              <div className="mb-1 flex items-center gap-2">
                <span className={imaginaResult.valid ? 'text-emerald-400' : 'text-neuro-danger'}>
                  {imaginaResult.valid ? '✅ Manifest valid' : '❌ Manifest invalid'}
                </span>
                <span className="text-neuro-muted">{imaginaResult.sample_count} samples</span>
              </div>
              {imaginaResult.dataset_name && (
                <p className="text-[11px] text-neuro-muted">
                  Dataset: {imaginaResult.dataset_name} ({imaginaResult.modality})
                </p>
              )}
              {imaginaResult.tasks && imaginaResult.tasks.length > 0 && (
                <p className="text-[11px] text-neuro-muted">
                  Tasks: {imaginaResult.tasks.join(', ')}
                </p>
              )}
              {imaginaResult.warnings.length > 0 && (
                <div className="mt-1">
                  {imaginaResult.warnings.map((w, i) => (
                    <p key={i} className="text-[10px] text-amber-400">⚠ {w}</p>
                  ))}
                </div>
              )}
              {imaginaResult.issues.length > 0 && (
                <div className="mt-1">
                  {imaginaResult.issues.map((issue, i) => (
                    <p key={i} className="text-[10px] text-neuro-danger">✗ {issue}</p>
                  ))}
                </div>
              )}
              <p className="mt-1 text-[10px] text-neuro-muted italic">
                {imaginaResult.not_a_trained_model ? 'Not a trained model — proxy interface only.' : ''}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Disclaimers */}
      <p className="mt-2 text-[11px] leading-relaxed text-neuro-muted">
        Fusion validation is behavioral testing under simulated conditions. It does not prove accuracy
        against ground-truth cognitive states. IMAGINA plugin outputs are imagery-quality proxies, not
        decoded thoughts or dreams. Closed-loop from real EEG is disabled by default.
      </p>

      {error && <p className="mt-2 text-xs text-neuro-danger">{error}</p>}
    </section>
  )
}
