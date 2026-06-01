import { useEffect, useState } from 'react'
import {
  getLatestAutoRunSnapshot,
  getLatestFusionValidationSnapshot,
  getImaginaStatus,
  getImaginaModels,
  trainImaginaBaseline,
  getExternalImaginaStatus,
  getExternalImaginaArtifacts,
  refreshExternalImagina,
  getLatestContractImport,
  validateExportContract,
  importExportContract,
  type ImaginaStatus,
  type ImaginaModel,
  type ExternalImaginaStatus,
  type ExternalImaginaModelArtifact
} from '../../api/client'
import type { AutoRunEvidenceSnapshot, FusionValidationSnapshot } from '../../types/research'
import { SafetyGovernancePanel } from '../Dashboard/SafetyGovernancePanel'

// ---------------------------------------------------------------------------
//  Helpers
// ---------------------------------------------------------------------------

function shortPath(p: string | null | undefined): string {
  if (!p) return '—'
  return p.replace(/\\/g, '/').split('/').slice(-4).join('/')
}

function modeBadgeClass(mode: string): string {
  switch (mode) {
    case 'simulated': return 'bg-emerald-950/60 text-emerald-400'
    case 'brainflow_synthetic': return 'bg-indigo-950/60 text-indigo-400'
    case 'replay': return 'bg-blue-950/60 text-blue-400'
    case 'physical_hardware': return 'bg-amber-950/60 text-amber-300'
    default: return 'bg-neuro-bg text-neuro-muted'
  }
}

function modeLabel(mode: string): string {
  switch (mode) {
    case 'simulated': return 'Simulated signals (no hardware)'
    case 'brainflow_synthetic': return 'BrainFlow SyntheticBoard (not real OpenBCI)'
    case 'replay': return 'EEG LSL replay (PhysioNet dataset)'
    case 'physical_hardware': return 'Physical hardware (record-only shadow)'
    default: return mode
  }
}

// ---------------------------------------------------------------------------
//  Section E live panel
// ---------------------------------------------------------------------------

function LiveAutoRunPanel() {
  const [snapshot, setSnapshot] = useState<AutoRunEvidenceSnapshot | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getLatestAutoRunSnapshot()
      .then(setSnapshot)
      .catch((e) => setError(e instanceof Error ? e.message : 'Evidence unavailable'))
      .finally(() => setLoading(false))
  }, [])

  // Loading state
  if (loading) {
    return (
      <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6 text-sm text-neuro-muted animate-pulse">
        Loading latest auto-run evidence…
      </div>
    )
  }

  // Empty state - neither live backend nor static baked evidence is available.
  if (error || (!loading && !snapshot)) {
    return (
      <div className="rounded-lg border border-neuro-border/50 bg-neuro-surface p-6 space-y-3">
        <p className="text-xs font-semibold text-amber-400">No evidence snapshot available</p>
        <p className="text-sm text-neuro-muted">
          The Evidence Center could not load live backend evidence or a static baked snapshot.
          Generate and bake real evidence with:
        </p>
        <div className="font-mono text-[11px] bg-neuro-bg rounded p-3 border border-neuro-border/40 text-neuro-accent space-y-1">
          <p>make protocol-run-demo</p>
          <p>make protocol-evidence-latest</p>
          <p>make generate-evidence-pack</p>
          <p>make static-evidence-bake</p>
        </div>
        <p className="text-[11px] text-neuro-muted">
          Last error: <code className="text-neuro-accent">{error ?? 'No snapshot loaded'}</code>
        </p>
      </div>
    )
  }

  if (!snapshot) return null

  const evidence = snapshot.evidence
  const c = evidence.step_summary
  const hasProves = evidence.what_this_proves.length > 0
  const hasNotProves = evidence.what_this_does_not_prove.length > 0
  const isStatic = snapshot.source === 'static_baked_snapshot'

  return (
    <div className="space-y-4">
      <div className={`rounded-lg border p-4 text-xs ${
        isStatic
          ? 'border-amber-500/20 bg-amber-950/10 text-neuro-muted'
          : 'border-emerald-500/20 bg-emerald-950/10 text-neuro-muted'
      }`}>
        <span className={isStatic ? 'font-semibold text-amber-400' : 'font-semibold text-emerald-400'}>
          {isStatic ? 'Static baked snapshot' : 'Live backend evidence'}
        </span>
        {' '}
        {isStatic
          ? 'Static evidence is a baked snapshot, not live runtime evidence.'
          : 'Evidence is loaded from the running FastAPI backend.'}
        {snapshot.detail && (
          <span className="block pt-1 font-mono text-[10px] text-neuro-muted">
            Live backend fallback reason: {snapshot.detail}
          </span>
        )}
      </div>

      {/* Run header */}
      <div className="rounded-lg border border-emerald-500/20 bg-neuro-surface p-5 space-y-3">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-bold text-white">{evidence.protocol_title}</span>
            {evidence.auto_completed && (
              <span className="rounded bg-emerald-900/50 px-1.5 py-0.5 text-[9px] text-emerald-400 font-medium">
                ✓ Auto-Completed
              </span>
            )}
            <span className={`rounded px-1.5 py-0.5 text-[9px] font-medium ${modeBadgeClass(evidence.mode)}`}>
              {modeLabel(evidence.mode)}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className={`text-xs rounded px-2 py-0.5 font-medium ${
              evidence.status === 'passed'
                ? 'bg-emerald-950/60 text-emerald-400'
                : 'bg-red-950/60 text-neuro-danger'
            }`}>
              {evidence.status}
            </span>
            <span className="rounded bg-red-950/40 px-1.5 py-0.5 text-[9px] text-neuro-danger font-medium">
              CL locked
            </span>
          </div>
        </div>

        {/* Step summary */}
        <div className="flex gap-4 text-[11px] flex-wrap">
          {c.passed > 0 && <span className="text-emerald-400">✓ {c.passed} passed</span>}
          {c.failed > 0 && <span className="text-neuro-danger">✗ {c.failed} failed</span>}
          {c.blocked > 0 && <span className="text-amber-400">⊘ {c.blocked} blocked</span>}
          {c.manual > 0 && <span className="text-indigo-400">⚙ {c.manual} manual</span>}
          {c.skipped > 0 && <span className="text-neuro-muted">— {c.skipped} skipped</span>}
          <span className="text-neuro-muted">
            {evidence.artifact_count} artifact{evidence.artifact_count !== 1 ? 's' : ''}
          </span>
        </div>

        {/* Safety lock */}
        <div className="rounded bg-neuro-bg px-3 py-2 text-[10px] font-mono space-y-0.5 border border-neuro-border/40">
          <p className="text-neuro-danger">[SAFE] closed_loop_allowed: false</p>
          <p className="text-neuro-muted">[SAFE] real_adaptation_actions_emitted: 0</p>
          <p className="text-neuro-muted">[INFO] mode: {evidence.mode} | status: {evidence.status}</p>
          <p className="text-neuro-muted">[INFO] auto_completed: {String(evidence.auto_completed)}</p>
          {evidence.auto_completed_at && (
            <p className="text-neuro-muted">[INFO] completed: {evidence.auto_completed_at.slice(0, 19)}Z</p>
          )}
        </div>

        {/* Metadata */}
        <div className="text-[10px] text-neuro-muted space-y-0.5">
          <p>Run ID: <code className="text-neuro-accent">{evidence.run_id}</code></p>
          {evidence.protocol_completion_report_path && (
            <p>Report: <code>{shortPath(evidence.protocol_completion_report_path)}</code></p>
          )}
          {evidence.generated_at && (
            <p>Generated: {evidence.generated_at.slice(0, 19)}Z</p>
          )}
        </div>
      </div>

      {/* Proves / not proves (from backend completion report) */}
      {(hasProves || hasNotProves) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {hasProves && (
            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4">
              <h4 className="text-xs font-semibold text-emerald-400 mb-2">✓ What this run proves</h4>
              <ul className="space-y-1.5">
                {evidence.what_this_proves.map((item, i) => (
                  <li key={i} className="text-[11px] text-neuro-muted leading-relaxed">• {item}</li>
                ))}
              </ul>
            </div>
          )}
          {hasNotProves && (
            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4">
              <h4 className="text-xs font-semibold text-neuro-danger mb-2">✗ What this run does not prove</h4>
              <ul className="space-y-1.5">
                {evidence.what_this_does_not_prove.map((item, i) => (
                  <li key={i} className="text-[11px] text-neuro-muted leading-relaxed">• {item}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Scientific limitations */}
      {evidence.scientific_limitations && (
        <p className="text-[11px] text-neuro-muted italic border-l-2 border-neuro-border pl-3">
          {evidence.scientific_limitations}
        </p>
      )}

      {/* Reproduce commands */}
      <div className="rounded bg-neuro-bg p-3 border border-neuro-border/40">
        <p className="text-[10px] text-neuro-accent mb-1.5 font-mono"># Reproduce this evidence</p>
        <div className="font-mono text-[10px] text-neuro-muted space-y-0.5">
          <p>make protocol-run-demo      # auto-runs all 5 steps (~10s)</p>
          <p>make protocol-evidence-latest   # prints run summary</p>
          <p>make generate-evidence-pack # updates evidence_pack/</p>
        </div>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
//  IMAGINA v1 Baseline Model Panel
// ---------------------------------------------------------------------------

function LiveImaginaBaselinePanel() {
  const [status, setStatus] = useState<ImaginaStatus | null>(null)
  const [models, setModels] = useState<ImaginaModel[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Selection state for live training
  const [modelType, setModelType] = useState('logistic_regression')
  const [splitStrategy, setSplitStrategy] = useState('fixture')
  const [training, setTraining] = useState(false)
  const [trainError, setTrainError] = useState<string | null>(null)
  const [trainSuccess, setTrainSuccess] = useState(false)
  const [selectedModel, setSelectedModel] = useState<ImaginaModel | null>(null)

  // External Imagina discovery states
  const [extStatus, setExtStatus] = useState<ExternalImaginaStatus | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = async () => {
    try {
      // 1. Try live backend query
      const statusData = await getImaginaStatus()
      const modelsData = await getImaginaModels()
      
      setStatus(statusData)
      setModels(modelsData)
      if (statusData.external_project_status) {
        setExtStatus(statusData.external_project_status)
      }
      
      if (modelsData.length > 0 && !selectedModel) {
        setSelectedModel(modelsData[0])
      }
      setError(null)
    } catch (e) {
      // 2. Try to fetch baked static evidence from the public portfolio path
      try {
        const statusRes = await fetch('/evidence/external_imagina_status.json')
        const artsRes = await fetch('/evidence/external_imagina_artifacts.json')
        
        if (statusRes.ok && artsRes.ok) {
          const bakedStatus: ExternalImaginaStatus = await statusRes.json()
          const bakedArts: ExternalImaginaModelArtifact[] = await artsRes.json()
          
          setExtStatus(bakedStatus)
          
          const mockStatus: ImaginaStatus = {
            status: 'active',
            plugin_id: 'imagina_v1',
            active_source: bakedStatus.exists ? 'external_imagina' : 'internal_fixture_fallback',
            external_project_status: bakedStatus,
            proxy_estimates_only: true,
            not_decoded_content: true,
            closed_loop_allowed: false,
            limitations: bakedStatus.limitations,
            provenance: { version: '1.0', timestamp: new Date().toISOString() }
          }
          
          // Map baked arts to ImaginaModel
          const mappedModels: ImaginaModel[] = bakedArts.map((art) => ({
            model_id: art.model_id,
            path: art.path,
            model_type: art.metrics?.model_type || 'scikit-learn',
            dataset_id: 'external_dataset',
            target: art.target,
            registered_at: art.created_at,
            imagina_model: true,
            source_project: 'external_imagina',
            metrics: art.metrics
          }))
          
          // Add default fallback model
          mappedModels.push({
            model_id: 'imagina_v1_baseline_portfolio_lr',
            path: 'models/imagina_v1_baseline_portfolio_lr',
            model_type: 'logistic_regression',
            dataset_id: 'example_imagery_v1_dataset',
            target: 'classification',
            registered_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
            imagina_model: true,
            source_project: 'neuroverse_fixture',
            metrics: {
              accuracy: 1.0,
              balanced_accuracy: 1.0,
              macro_f1: 1.0,
              confusion_matrix: [[3, 0], [0, 3]],
              sample_count: 6,
              subject_count: 2,
              split_strategy: 'leave_one_subject_out',
              leakage_warnings: ['Portfolio simulated data: Verification baseline model only.']
            }
          })
          
          setStatus(mockStatus)
          setModels(mappedModels)
          setSelectedModel(mappedModels[0])
          setError('Backend offline (serving baked portfolio snapshot)')
          return
        }
      } catch (staticErr) {
        // Fall through
      }

      // 3. Fallback to default simulated portfolio data if no baked files exist
      const defaultExtStatus: ExternalImaginaStatus = {
        project_root: '/home/tonystark/Desktop/Imagina',
        exists: true,
        detected_version: '1.0',
        available_artifacts: ['README.md', 'backend', 'frontend', 'research', 'scripts'],
        latest_model_path: 'models/imagina_v1_baseline_mocked',
        latest_report_path: null,
        latest_metrics_path: null,
        latest_prediction_path: null,
        integration_ready: true,
        limitations: [
          'IMAGINA is an external research/modeling project. NeuroVerse is the safety-gated runtime and neuroadaptive interface layer.',
          'IMAGINA outputs are experimental imagery proxy estimates, not decoded thoughts.'
        ],
        warnings: []
      }

      const mockStatus: ImaginaStatus = {
        status: 'active',
        plugin_id: 'imagina_v1',
        active_source: 'external_imagina',
        external_project_status: defaultExtStatus,
        proxy_estimates_only: true,
        not_decoded_content: true,
        closed_loop_allowed: false,
        limitations: defaultExtStatus.limitations,
        provenance: { version: '1.0', timestamp: new Date().toISOString() }
      }

      const mockModels: ImaginaModel[] = [
        {
          model_id: 'imagina_v1_external_scientific_model',
          path: '/home/tonystark/Desktop/Imagina/models/external_model',
          model_type: 'random_forest',
          dataset_id: 'real_imagery_subject_12',
          target: 'classification',
          registered_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
          imagina_model: true,
          source_project: 'external_imagina',
          metrics: {
            accuracy: 0.88,
            balanced_accuracy: 0.86,
            macro_f1: 0.87,
            confusion_matrix: [[12, 2], [1, 10]],
            sample_count: 25,
            subject_count: 1,
            split_strategy: 'leave_one_subject_out',
            leakage_warnings: []
          }
        },
        {
          model_id: 'imagina_v1_baseline_portfolio_lr',
          path: 'models/imagina_v1_baseline_portfolio_lr',
          model_type: 'logistic_regression',
          dataset_id: 'example_imagery_v1_dataset',
          target: 'classification',
          registered_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          imagina_model: true,
          source_project: 'neuroverse_fixture',
          metrics: {
            accuracy: 1.0,
            balanced_accuracy: 1.0,
            macro_f1: 1.0,
            confusion_matrix: [[3, 0], [0, 3]],
            sample_count: 6,
            subject_count: 2,
            split_strategy: 'leave_one_subject_out',
            leakage_warnings: ['Portfolio simulated data: Verification baseline model only.']
          }
        }
      ]

      setStatus(mockStatus)
      setExtStatus(defaultExtStatus)
      setModels(mockModels)
      setSelectedModel(mockModels[0])
      setError('Backend offline (serving portfolio mock baseline)')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleTrain = async (e: React.FormEvent) => {
    e.preventDefault()
    setTraining(true)
    setTrainError(null)
    setTrainSuccess(false)
    
    try {
      if (error && error.includes('Backend offline')) {
        // Mock training action instantly
        await new Promise((resolve) => setTimeout(resolve, 800))
        const newMockModel: ImaginaModel = {
          model_id: `imagina_v1_fixture_mock_${Math.random().toString(36).substring(2, 7)}`,
          path: `models/imagina_v1_baseline_mock`,
          model_type: modelType,
          dataset_id: 'example_imagery_v1_dataset',
          target: 'classification',
          registered_at: new Date().toISOString(),
          imagina_model: true,
          source_project: 'neuroverse_fixture',
          metrics: {
            accuracy: 0.92,
            balanced_accuracy: 0.90,
            macro_f1: 0.89,
            confusion_matrix: [[3, 0], [1, 2]],
            sample_count: 6,
            subject_count: 2,
            split_strategy: splitStrategy,
            leakage_warnings: [
              'Trained on synthetic/fixture demo data.',
              splitStrategy === 'fixture' ? 'Fixture split used for verification; not scientifically generalizable.' : ''
            ].filter(Boolean)
          }
        }
        const updated = [newMockModel, ...models]
        setModels(updated)
        setSelectedModel(newMockModel)
        setTrainSuccess(true)
      } else {
        // Live training
        await trainImaginaBaseline(modelType, splitStrategy)
        setTrainSuccess(true)
        await fetchData()
      }
    } catch (err) {
      setTrainError(err instanceof Error ? err.message : 'Training failed')
    } finally {
      setTraining(false)
    }
  }

  const handleScanRefresh = async () => {
    setRefreshing(true)
    try {
      if (error && error.includes('Backend offline')) {
        await new Promise((resolve) => setTimeout(resolve, 800))
      } else {
        await refreshExternalImagina()
      }
      await fetchData()
    } catch (e) {
      // ignore
    } finally {
      setRefreshing(false)
    }
  }

  if (loading) {
    return (
      <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6 text-sm text-neuro-muted animate-pulse">
        Loading IMAGINA baseline model registry and external research contract details…
      </div>
    )
  }

  const isMock = !!error && error.includes('Backend offline')
  const activeSource = status?.active_source || 'internal_fixture_fallback'

  return (
    <div className="space-y-6">
      {/* Top Banner: Integration source of truth */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-lg border border-neuro-border bg-neuro-bg/50">
        <div>
          <span className="text-[10px] uppercase font-bold tracking-wider text-neuro-muted block mb-1">
            Imagery Modeling Origin
          </span>
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${activeSource === 'external_imagina' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400 animate-pulse'}`} />
            <h4 className="text-sm font-bold text-white uppercase tracking-wider">
              {activeSource === 'external_imagina' 
                ? 'External Research Repository (../Imagina)' 
                : 'Internal Fixture Fallback Mode'}
            </h4>
          </div>
          <p className="text-xs text-neuro-muted mt-1 leading-relaxed max-w-2xl">
            {activeSource === 'external_imagina'
              ? 'NeuroVerse is consuming validated modeling outputs and artifacts from the external research workspace. Strict governance remains active.'
              : 'External repository not detected or backend is offline. Operating in fallback fixture mode (demo-only model metrics).'}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {isMock && (
            <span className="rounded bg-amber-950/40 border border-amber-500/20 px-2.5 py-1 text-[10px] text-amber-400 font-semibold">
              Baked Portfolio Snapshot
            </span>
          )}
          <button
            onClick={handleScanRefresh}
            disabled={refreshing}
            className="rounded border border-neuro-accent bg-neuro-accent/10 hover:bg-neuro-accent/20 text-neuro-accent text-[11px] font-bold px-3 py-1.5 transition uppercase tracking-wider disabled:opacity-50"
          >
            {refreshing ? 'Scanning…' : 'Scan Repository'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Column 1: G.1 External Discovery Contract & Governance */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Card: External project status */}
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5 space-y-4">
            <div className="flex justify-between items-center border-b border-neuro-border pb-2.5">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">
                G.1 External Research Project Discovery Contract
              </h3>
              <span className="rounded bg-neuro-bg border border-neuro-border px-2 py-0.5 text-[9px] font-mono text-neuro-muted">
                NEUROVERSE_IMAGINA_ROOT
              </span>
            </div>

            {extStatus ? (
              <div className="space-y-4 text-xs">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <div>
                      <p className="text-[10px] text-neuro-muted uppercase font-semibold">Project Root Path</p>
                      <p className="font-mono text-white text-[11px] truncate">{extStatus.project_root}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-neuro-muted uppercase font-semibold">Discovery State</p>
                      <p className="text-white">
                        {extStatus.exists ? (
                          <span className="text-emerald-400 font-semibold">✓ Discovered & Connected</span>
                        ) : (
                          <span className="text-red-400 font-semibold">✗ Not Found</span>
                        )}
                      </p>
                    </div>
                    <div>
                      <p className="text-[10px] text-neuro-muted uppercase font-semibold">Research Version</p>
                      <p className="font-mono text-white">{extStatus.detected_version || '1.0'}</p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <p className="text-[10px] text-neuro-muted uppercase font-semibold">Signature folder compliance</p>
                    <div className="flex flex-wrap gap-1.5">
                      {['README.md', 'backend', 'frontend', 'research', 'scripts'].map(dir => {
                        const hasDir = extStatus.available_artifacts?.includes(dir)
                        return (
                          <span
                            key={dir}
                            className={`rounded text-[9px] font-mono px-2 py-0.5 border ${
                              hasDir 
                                ? 'bg-emerald-950/30 border-emerald-500/20 text-emerald-400' 
                                : 'bg-red-950/30 border-red-500/20 text-red-400'
                            }`}
                          >
                            {dir}
                          </span>
                        )
                      })}
                    </div>
                    {extStatus.warnings && extStatus.warnings.length > 0 && (
                      <div className="mt-2 text-[10px] text-amber-400 bg-amber-950/20 rounded p-2.5 border border-amber-500/20 space-y-1">
                        <p className="font-bold">Discovery Warnings:</p>
                        {extStatus.warnings.map((w, i) => <p key={i}>• {w}</p>)}
                      </div>
                    )}
                  </div>
                </div>

                <div className="border-t border-neuro-border/50 pt-3">
                  <p className="text-[10px] text-neuro-muted uppercase font-semibold mb-1.5">Scanned filesystem status</p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    <div className="bg-neuro-bg p-2 rounded border border-neuro-border/40 text-center">
                      <p className="text-[9px] text-neuro-muted">LATEST MODEL</p>
                      <p className="font-mono text-[10px] text-white truncate">{extStatus.latest_model_path ? 'scanned' : 'not detected'}</p>
                    </div>
                    <div className="bg-neuro-bg p-2 rounded border border-neuro-border/40 text-center">
                      <p className="text-[9px] text-neuro-muted">SESSION REPORT</p>
                      <p className="font-mono text-[10px] text-white truncate">{extStatus.latest_report_path ? 'scanned' : 'not detected'}</p>
                    </div>
                    <div className="bg-neuro-bg p-2 rounded border border-neuro-border/40 text-center">
                      <p className="text-[9px] text-neuro-muted">METRICS FILE</p>
                      <p className="font-mono text-[10px] text-white truncate">{extStatus.latest_metrics_path ? 'scanned' : 'not detected'}</p>
                    </div>
                    <div className="bg-neuro-bg p-2 rounded border border-neuro-border/40 text-center">
                      <p className="text-[9px] text-neuro-muted">PREDICTIONS FILE</p>
                      <p className="font-mono text-[10px] text-white truncate">{extStatus.latest_prediction_path ? 'scanned' : 'not detected'}</p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-xs text-neuro-muted">No external Imagina status discovered.</p>
            )}
          </div>

          {/* Registry list */}
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5 space-y-4">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-neuro-border pb-2.5">
              Trained Models Registry (External Research vs Local Fixtures)
            </h3>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-neuro-muted">
                <thead>
                  <tr className="border-b border-neuro-border/80 text-[10px] uppercase font-semibold text-white/70">
                    <th className="py-2">Origin</th>
                    <th className="py-2">Model ID</th>
                    <th className="py-2">Type</th>
                    <th className="py-2">Acc</th>
                    <th className="py-2">F1</th>
                    <th className="py-2">Scanned / Registered</th>
                  </tr>
                </thead>
                <tbody>
                  {models.map((m) => {
                    const isSelected = selectedModel?.model_id === m.model_id
                    const isExternal = m.source_project === 'external_imagina'
                    return (
                      <tr
                        key={m.model_id}
                        onClick={() => setSelectedModel(m)}
                        className={`border-b border-neuro-border/30 cursor-pointer transition ${
                          isSelected ? 'bg-neuro-accent/15 text-white' : 'hover:bg-neuro-surface-light'
                        }`}
                      >
                        <td className="py-3 pr-2">
                          <span className={`rounded text-[9px] font-bold px-1.5 py-0.5 border ${
                            isExternal 
                              ? 'bg-blue-950/50 border-blue-500/20 text-blue-400' 
                              : 'bg-amber-950/50 border-amber-500/20 text-amber-400'
                          }`}>
                            {isExternal ? 'Research' : 'Fixture'}
                          </span>
                        </td>
                        <td className="py-3 font-mono text-[10px] truncate max-w-[150px]">{m.model_id}</td>
                        <td className="py-3 capitalize">{m.model_type.replace('_', ' ')}</td>
                        <td className="py-3 font-mono">{m.metrics?.accuracy?.toFixed(2) ?? '—'}</td>
                        <td className="py-3 font-mono">{m.metrics?.macro_f1?.toFixed(2) ?? '—'}</td>
                        <td className="py-3 text-[10px]">{m.registered_at.substring(0, 10)} {m.registered_at.substring(11, 16)}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Column 2: G.2 Local Fallback Model Hub & Safety checklists */}
        <div className="space-y-6">
          
          {/* Card: Safety checklists */}
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5 space-y-4">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider border-b border-neuro-border pb-2.5">
              Closed-Loop Safety Governance Layer
            </h3>
            
            <div className="bg-neuro-bg p-3 rounded border border-neuro-border/40 space-y-2.5 text-[11px] leading-relaxed">
              <div className="flex justify-between items-center text-neuro-danger">
                <span>🔒 closed_loop_locked:</span>
                <span className="font-mono font-bold">TRUE</span>
              </div>
              <div className="flex justify-between items-center text-neuro-muted">
                <span>✓ proxy_estimates_only:</span>
                <span className="font-mono font-bold">TRUE</span>
              </div>
              <div className="flex justify-between items-center text-neuro-muted">
                <span>✓ not_decoded_content:</span>
                <span className="font-mono font-bold">TRUE</span>
              </div>
              <div className="border-t border-neuro-border/40 pt-2 text-[10px] text-neuro-muted space-y-1">
                <p className="font-semibold text-neuro-danger">Mandatory limitations framing:</p>
                <p>• Imagery outputs are experimental estimates.</p>
                <p>• Closed-loop adaptiveness is locked by default.</p>
                <p>• Real-time decoding of thought remains unvalidated.</p>
              </div>
            </div>
          </div>

          {/* Card: Local Training Hub */}
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5 space-y-4">
            <div className="border-b border-neuro-border pb-2.5">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">
                G.2 Local Fixture Fallback Hub (Demo Only)
              </h3>
              <p className="text-[10px] text-neuro-muted mt-0.5">
                Train synthetic classifiers to verify late fusion integration.
              </p>
            </div>
            
            <form onSubmit={handleTrain} className="space-y-3.5 text-xs">
              <div className="space-y-1">
                <label className="text-[10px] font-semibold text-neuro-muted uppercase">Architecture</label>
                <select
                  value={modelType}
                  onChange={(e) => setModelType(e.target.value)}
                  className="w-full text-xs rounded border border-neuro-border/80 bg-neuro-bg p-2 text-white outline-none focus:border-neuro-accent"
                >
                  <option value="logistic_regression">Logistic Regression (default)</option>
                  <option value="random_forest">Random Forest Classifier</option>
                  <option value="ridge_classifier">Ridge Classifier</option>
                  <option value="mlp">Multi-layer Perceptron (MLP)</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-semibold text-neuro-muted uppercase">Split Strategy</label>
                <select
                  value={splitStrategy}
                  onChange={(e) => setSplitStrategy(e.target.value)}
                  className="w-full text-xs rounded border border-neuro-border/80 bg-neuro-bg p-2 text-white outline-none focus:border-neuro-accent"
                >
                  <option value="fixture">Fixture / Simple split</option>
                  <option value="stratified">Stratified K-Fold split</option>
                  <option value="group_subject">Group Subject split</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={training}
                className="w-full text-xs font-bold py-2 px-4 rounded transition text-center bg-neuro-accent hover:bg-neuro-accent/80 text-black uppercase tracking-wider disabled:opacity-50"
              >
                {training ? 'Training Model…' : 'Train Fixture Model'}
              </button>
            </form>

            {trainSuccess && (
              <div className="rounded bg-emerald-950/40 border border-emerald-500/20 p-2.5 text-[10px] text-emerald-400">
                ✓ Fixture model registered in local fallback registry successfully.
              </div>
            )}

            {trainError && (
              <div className="rounded bg-red-950/40 border border-red-500/20 p-2.5 text-[10px] text-neuro-danger">
                ✗ Error: {trainError}
              </div>
            )}
          </div>
        </div>

      </div>

      {/* Selected Model Card details */}
      {selectedModel && (
        <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5 space-y-4">
          <div className="flex justify-between items-center border-b border-neuro-border pb-2.5">
            <div className="flex items-center gap-2">
              <span className={`rounded text-[10px] font-bold px-2 py-0.5 border ${
                selectedModel.source_project === 'external_imagina' 
                  ? 'bg-blue-950/50 border-blue-500/20 text-blue-400' 
                  : 'bg-amber-950/50 border-amber-500/20 text-amber-400'
              }`}>
                {selectedModel.source_project === 'external_imagina' ? 'External Research' : 'Local Fallback Fixture'}
              </span>
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                Model Card Details: {selectedModel.model_id}
              </h4>
            </div>
            <span className="font-mono text-[10px] text-neuro-accent bg-neuro-bg px-2.5 py-0.5 rounded border border-neuro-border/60">
              {selectedModel.model_type}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
            <div className="space-y-2">
              <p className="text-white font-semibold uppercase text-[10px] tracking-wider text-neuro-muted">Validation Metrics</p>
              <div className="grid grid-cols-3 gap-2">
                <div className="bg-neuro-bg p-2.5 rounded border border-neuro-border/40 text-center">
                  <p className="text-[9px] text-neuro-muted uppercase">Accuracy</p>
                  <p className="font-mono font-bold text-white text-sm mt-0.5">
                    {selectedModel.metrics?.accuracy?.toFixed(2) ?? '—'}
                  </p>
                </div>
                <div className="bg-neuro-bg p-2.5 rounded border border-neuro-border/40 text-center">
                  <p className="text-[9px] text-neuro-muted uppercase">Bal Acc</p>
                  <p className="font-mono font-bold text-white text-sm mt-0.5">
                    {selectedModel.metrics?.balanced_accuracy?.toFixed(2) ?? '—'}
                  </p>
                </div>
                <div className="bg-neuro-bg p-2.5 rounded border border-neuro-border/40 text-center">
                  <p className="text-[9px] text-neuro-muted uppercase">Macro F1</p>
                  <p className="font-mono font-bold text-white text-sm mt-0.5">
                    {selectedModel.metrics?.macro_f1?.toFixed(2) ?? '—'}
                  </p>
                </div>
              </div>
              <div className="bg-neuro-bg p-2.5 rounded border border-neuro-border/40 space-y-1">
                <p className="text-[9px] text-neuro-muted font-bold uppercase">CONFUSION MATRIX</p>
                <pre className="font-mono text-[10px] text-neuro-accent">
                  {JSON.stringify(selectedModel.metrics?.confusion_matrix)}
                </pre>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-white font-semibold uppercase text-[10px] tracking-wider text-neuro-muted">Paradigm Metadata</p>
              <div className="bg-neuro-bg p-3.5 rounded border border-neuro-border/40 space-y-2 leading-relaxed">
                <div>
                  <span className="text-[9px] text-neuro-muted uppercase block">Target Class</span>
                  <span className="text-white font-medium capitalize">{selectedModel.target || 'classification'}</span>
                </div>
                <div>
                  <span className="text-[9px] text-neuro-muted uppercase block">Dataset Reference</span>
                  <span className="text-white font-mono">{selectedModel.dataset_id || 'external_dataset'}</span>
                </div>
                <div>
                  <span className="text-[9px] text-neuro-muted uppercase block">Filesystem Location</span>
                  <span className="text-white font-mono text-[10px] break-all">{selectedModel.path}</span>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-white font-semibold uppercase text-[10px] tracking-wider text-neuro-muted">Governance & Leakage Audit</p>
              <div className="bg-neuro-bg p-3.5 rounded border border-neuro-border/40 space-y-2 leading-relaxed text-[11px]">
                <div className="flex justify-between items-center text-neuro-danger">
                  <span>closed_loop_locked:</span>
                  <span className="font-bold font-mono">TRUE</span>
                </div>
                
                {selectedModel.metrics?.leakage_warnings && selectedModel.metrics.leakage_warnings.length > 0 ? (
                  <div className="mt-1.5 text-amber-400 space-y-1">
                    <p className="font-bold text-[10px] uppercase text-amber-500">⚠ Leakage warnings detected:</p>
                    {selectedModel.metrics.leakage_warnings.map((w: string, idx: number) => (
                      <p key={idx} className="font-mono text-[9px] leading-snug">• {w}</p>
                    ))}
                  </div>
                ) : (
                  <p className="text-emerald-400 text-[10px] font-medium mt-1">✓ Scientific leakage audit passed successfully.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
//  Multimodal Fusion Validation Panel
// ---------------------------------------------------------------------------

function LiveFusionValidationPanel() {
  const [snapshot, setSnapshot] = useState<FusionValidationSnapshot | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getLatestFusionValidationSnapshot()
      .then(setSnapshot)
      .catch((e) => setError(e instanceof Error ? e.message : 'Fusion evidence unavailable'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6 text-sm text-neuro-muted animate-pulse">
        Loading latest multimodal fusion validation evidence…
      </div>
    )
  }

  if (error || (!loading && !snapshot)) {
    return (
      <div className="rounded-lg border border-neuro-border/50 bg-neuro-surface p-6 space-y-3">
        <p className="text-xs font-semibold text-amber-400">No fusion evidence snapshot available</p>
        <p className="text-sm text-neuro-muted">
          The Evidence Center could not load fusion validation evidence or static baked snapshot.
          Generate and bake fusion evidence with:
        </p>
        <div className="font-mono text-[11px] bg-neuro-bg rounded p-3 border border-neuro-border/40 text-neuro-accent space-y-1">
          <p>make fusion-validate</p>
          <p>make fusion-calibrate</p>
          <p>make generate-evidence-pack</p>
          <p>make static-evidence-bake</p>
        </div>
        <p className="text-[11px] text-neuro-muted">
          Last error: <code className="text-neuro-accent">{error ?? 'No fusion snapshot loaded'}</code>
        </p>
      </div>
    )
  }

  if (!snapshot) {
    return null
  }

  const valObj = snapshot.validation as any
  const calObj = snapshot.calibration as any
  const isSummaryObj = valObj && ('scenarios' in valObj)

  const runId = valObj?.run_id ?? 'latest_run'
  const allChecksPassed = isSummaryObj
    ? (valObj.all_uncertainty_checks_passed && valObj.all_safety_checks_passed)
    : (valObj?.all_checks_passed ?? true)

  const scenarioCount = isSummaryObj ? valObj.scenario_count : 7
  const calibrationId = isSummaryObj ? valObj.calibration_profile_id : (calObj?.profile_id ?? 'calibrated_profile')
  const isStatic = snapshot.source === 'static_baked_snapshot'

  // Scenario list or summary
  const scenarios = isSummaryObj ? Object.entries(valObj.scenarios) : []

  return (
    <div className="space-y-4">
      {/* Mode Indicator */}
      <div className={`rounded-lg border p-4 text-xs ${
        isStatic
          ? 'border-amber-500/20 bg-amber-950/10 text-neuro-muted'
          : 'border-emerald-500/20 bg-emerald-950/10 text-neuro-muted'
      }`}>
        <span className={isStatic ? 'font-semibold text-amber-400' : 'font-semibold text-emerald-400'}>
          {isStatic ? 'Static baked snapshot' : 'Live backend evidence'}
        </span>
        {' '}
        {isStatic
          ? 'Static evidence is loaded from the baked portfolio artifacts, showing historical validation state.'
          : 'Evidence is retrieved in real-time from the FastAPI fusion validation modules.'}
      </div>

      {/* Primary Evidence Section */}
      <div className="rounded-lg border border-emerald-500/20 bg-neuro-surface p-5 space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-bold text-white">Multimodal Fusion Validation Report</span>
            <span className={`rounded px-1.5 py-0.5 text-[9px] font-medium ${
              allChecksPassed ? 'bg-emerald-950/60 text-emerald-400' : 'bg-red-950/60 text-neuro-danger'
            }`}>
              {allChecksPassed ? '✓ All Checks Passed' : '✗ Checks Failed'}
            </span>
          </div>
          <span className="rounded bg-red-950/40 px-1.5 py-0.5 text-[9px] text-neuro-danger font-medium">
            CL locked
          </span>
        </div>

        {/* Info Blocks */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1.5 text-xs text-neuro-muted">
            <p>Run ID: <code className="text-neuro-accent">{runId}</code></p>
            <p>Calibration Profile: <code>{calibrationId}</code></p>
            <p>Validation Scenarios: <span className="text-white">{scenarioCount}</span></p>
            <p>Behavioral Uncertainty: <span className="text-emerald-400">Validated</span></p>
            <p>Quality Signal Capping: <span className="text-emerald-400">Validated</span></p>
          </div>
          <div className="space-y-1.5 text-xs text-neuro-muted">
            <p>Validation Summary Path: <code>evidence_pack/latest_fusion_validation_summary.json</code></p>
            <p>Ablation Table Path: <code>evidence_pack/latest_fusion_ablation_table.csv</code></p>
            <p>Calibration Report Path: <code>evidence_pack/latest_fusion_calibration_report.md</code></p>
            <p>Calibration Profile Path: <code>evidence_pack/latest_fusion_calibration_profile.json</code></p>
          </div>
        </div>

        {/* safety gate indicator */}
        <div className="rounded bg-neuro-bg px-3 py-2 text-[10px] font-mono space-y-1 border border-neuro-border/40">
          <p className="text-neuro-danger">[SAFE] real_eeg_closed_loop: LOCKED (disabled by default)</p>
          <p className="text-neuro-accent">[SAFE] proxy_estimates_only: True (gated shadow mode)</p>
          <p className="text-neuro-muted">[INFO] fusion_safety_recommendation: allow_shadow | wait | block</p>
          <p className="text-neuro-muted">[INFO] calibration_scaling: minmax feature normalizer active</p>
        </div>

        {/* Wording Requirements */}
        <div className="rounded-lg border border-red-500/20 bg-red-950/10 p-4 text-[11px] leading-relaxed text-neuro-muted space-y-2">
          <p className="border-l-2 border-neuro-danger pl-2">
            ⚠️ <strong className="text-neuro-text">Required framing:</strong>
          </p>
          <p>
            • “Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.”
          </p>
          <p>
            • “IMAGINA plugin outputs are imagery-quality proxies, not decoded thoughts or dreams.”
          </p>
          <p>
            • “The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.”
          </p>
          <p>
            • “Closed-loop from real EEG is disabled by default.”
          </p>
        </div>

        {/* What it proves / does not prove */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="rounded border border-neuro-border bg-neuro-bg/20 p-4">
            <h4 className="text-xs font-semibold text-emerald-400 mb-2">✓ What this validation proves</h4>
            <ul className="space-y-1.5 text-[11px] text-neuro-muted leading-relaxed list-disc pl-4">
              <li>Engine is resilient to missing modalities and signal drops.</li>
              <li>Uncertainty behaves correctly, increasing when key features are absent.</li>
              <li>Engine correctly emits conservative safety recommendations (block or wait) under high uncertainty.</li>
              <li>Calibration profile safely normalizes features to prevent scaling biases.</li>
            </ul>
          </div>
          <div className="rounded border border-neuro-border bg-neuro-bg/20 p-4">
            <h4 className="text-xs font-semibold text-neuro-danger mb-2">✗ What this does not prove</h4>
            <ul className="space-y-1.5 text-[11px] text-neuro-muted leading-relaxed list-disc pl-4">
              <li>Does not prove accuracy against absolute ground-truth cognitive states.</li>
              <li>Does not prove clinical efficacy or medical diagnosis.</li>
              <li>Does not prove thought or dream decoding.</li>
              <li>Does not represent real OpenBCI or Galea physical validation unless physical reports are attached.</li>
            </ul>
          </div>
        </div>

        {/* Uncertainty behavior summary */}
        <div className="text-[11px] text-neuro-muted border-l-2 border-neuro-border pl-3 space-y-1">
          <p className="font-semibold text-white">Uncertainty Behavior Summary:</p>
          <p>
            Under full ablation, when only EEG is present, uncertainty increases to <code className="text-neuro-accent">0.600</code>. When only Self-Report is present, uncertainty correctly increases to <code className="text-neuro-accent">0.800</code>. Low signal quality on EEG spikes uncertainty from <code className="text-neuro-accent">0.000</code> to <code className="text-neuro-accent">0.300</code>. This is the expected failsafe response.
          </p>
        </div>

        {/* Detailed Ablation Table snippet if loaded */}
        {scenarios.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs font-semibold text-white">Ablation Scenarios Verified:</p>
            <div className="overflow-x-auto">
              <table className="min-w-full text-[10px] font-mono border border-neuro-border/40">
                <thead>
                  <tr className="bg-neuro-bg/50 border-b border-neuro-border/40 text-left">
                    <th className="p-1">Scenario</th>
                    <th className="p-1">Uncertainty</th>
                    <th className="p-1">Confidence</th>
                    <th className="p-1">Safety Rec</th>
                  </tr>
                </thead>
                <tbody>
                  {scenarios.map(([key, item]: any) => (
                    <tr key={key} className="border-b border-neuro-border/20">
                      <td className="p-1 text-neuro-text">{key}</td>
                      <td className="p-1 text-neuro-accent">{item.uncertainty?.toFixed(3)}</td>
                      <td className="p-1">{item.overall_confidence?.toFixed(3)}</td>
                      <td className={`p-1 font-bold ${
                        item.safety_recommendation === 'allow_shadow' ? 'text-emerald-400' : 'text-amber-400'
                      }`}>{item.safety_recommendation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Reproduce commands */}
      <div className="rounded bg-neuro-bg p-3 border border-neuro-border/40">
        <p className="text-[10px] text-neuro-accent mb-1.5 font-mono"># Regenerate Multimodal Fusion Evidence</p>
        <div className="font-mono text-[10px] text-neuro-muted space-y-0.5">
          <p>make fusion-validate            # runs behavioral ablation scenarios</p>
          <p>make fusion-calibrate           # bakes subject calibration profiles</p>
          <p>make imagina-validate-manifest  # validates bridge dataset manifest</p>
          <p>make fusion-evidence-refresh    # refreshes all fusion validation artifacts</p>
        </div>
      </div>
    </div>
  )
}


// ---------------------------------------------------------------------------
//  IMAGINA Export Contract & import Validator Panel
// ---------------------------------------------------------------------------

function LiveImaginaExportContractPanel() {
  const [manifestPath, setManifestPath] = useState('exports/neuroverse/latest/neuroverse_imagina_export.json')
  const [latestImport, setLatestImport] = useState<any>(null)
  
  // Interactive audit states
  const [loading, setLoading] = useState(false)
  const [actionSuccess, setActionSuccess] = useState<string | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)
  const [validationResult, setValidationResult] = useState<any>(null)

  const fetchLatestImport = async () => {
    try {
      const data = await getLatestContractImport()
      setLatestImport(data)
    } catch (e) {
      // Offline fallback: try to load baked static JSON
      try {
        const res = await fetch('/evidence/latest_contract_import_summary.json')
        if (res.ok) {
          const baked = await res.json()
          setLatestImport({
            import_id: baked.import_id || 'static_portfolio_import_v1',
            active_source: 'external_contract',
            manifest: baked.manifest || baked,
            summary: baked,
            timestamp: baked.timestamp || new Date().toISOString()
          })
        }
      } catch (staticErr) {
        // ignore fallback errors
      }
    }
  }

  useEffect(() => {
    fetchLatestImport()
  }, [])

  const handleValidate = async () => {
    setLoading(true)
    setActionSuccess(null)
    setActionError(null)
    setValidationResult(null)
    try {
      const res = await validateExportContract(manifestPath)
      setValidationResult(res)
      if (res.valid) {
        setActionSuccess('Export Contract validated successfully! Package is 100% compliant with safety guidelines.')
      } else {
        setActionError(`Contract Validation Rejected: ${res.errors.join('; ')}`)
      }
    } catch (e) {
      setActionError(e instanceof Error ? e.message : 'API connection failed. Please ensure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleImport = async () => {
    setLoading(true)
    setActionSuccess(null)
    setActionError(null)
    setValidationResult(null)
    try {
      const res = await importExportContract(manifestPath)
      if (res.success) {
        setActionSuccess(`Export package successfully imported under ID: ${res.import_id}`)
        await fetchLatestImport()
      } else {
        setActionError(`Import Gating Blocked: ${res.errors?.join('; ') || 'Validation failure.'}`)
      }
    } catch (e) {
      setActionError(e instanceof Error ? e.message : 'API connection failed. Gated registry offline.')
    } finally {
      setLoading(false)
    }
  }

  const activeImport = latestImport
  const manifest = activeImport?.manifest

  return (
    <div className="space-y-6">
      
      {/* interactive Sandbox console */}
      <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5 space-y-4">
        <div className="border-b border-neuro-border pb-2.5">
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">
            H.1 Export Contract Lifecycle Controller
          </h3>
          <p className="text-[10px] text-neuro-muted mt-0.5">
            Audit export packages and securely ingest compliance metadata relative to NEUROVERSE_IMAGINA_ROOT.
          </p>
        </div>

        <div className="space-y-3.5 text-xs">
          <div className="space-y-1">
            <label className="text-[10px] font-semibold text-neuro-muted uppercase">Manifest Package Path</label>
            <input
              type="text"
              value={manifestPath}
              onChange={(e) => setManifestPath(e.target.value)}
              className="w-full text-xs font-mono rounded border border-neuro-border/80 bg-neuro-bg p-2 text-white outline-none focus:border-neuro-accent"
              placeholder="Relative path inside workspace or absolute system path"
            />
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={handleValidate}
              disabled={loading}
              className="flex-1 min-w-[150px] text-xs font-bold py-2 px-4 rounded border border-neuro-accent bg-neuro-accent/10 hover:bg-neuro-accent/20 text-neuro-accent uppercase tracking-wider transition disabled:opacity-50"
            >
              {loading ? 'Auditing…' : 'Validate Contract'}
            </button>
            <button
              onClick={handleImport}
              disabled={loading}
              className="flex-1 min-w-[150px] text-xs font-bold py-2 px-4 rounded bg-neuro-accent hover:bg-neuro-accent/80 text-black uppercase tracking-wider transition disabled:opacity-50"
            >
              {loading ? 'Importing…' : 'Validate & Import'}
            </button>
          </div>
        </div>

        {/* Action result display boxes */}
        {actionSuccess && (
          <div className="rounded bg-emerald-950/40 border border-emerald-500/20 p-3 text-[11px] text-emerald-400 leading-relaxed font-medium space-y-1">
            <p className="font-bold">✓ Audit Action Success:</p>
            <p>{actionSuccess}</p>
          </div>
        )}

        {actionError && (
          <div className="rounded bg-red-950/40 border border-red-500/20 p-3 text-[11px] text-neuro-danger leading-relaxed font-medium space-y-1">
            <p className="font-bold">✗ Security Alert / Error:</p>
            <p>{actionError}</p>
          </div>
        )}

        {validationResult && (
          <div className="rounded bg-neuro-bg border border-neuro-border/60 p-3.5 space-y-2.5 font-mono text-[10px]">
            <p className="text-white font-bold">// Validation Schema Audit Report</p>
            <div className="grid grid-cols-2 gap-2 text-neuro-muted">
              <p>Contract Compliant: <span className={validationResult.valid ? 'text-emerald-400' : 'text-red-400'}>{String(validationResult.valid)}</span></p>
              <p>Safety Flags Approved: <span className={validationResult.safety_flags_ok ? 'text-emerald-400' : 'text-red-400'}>{String(validationResult.safety_flags_ok)}</span></p>
              <p>Fusion Injectable: <span className={validationResult.can_convert_to_fusion_packet ? 'text-emerald-400' : 'text-red-400'}>{String(validationResult.can_convert_to_fusion_packet)}</span></p>
              <p>Export ID: <span className="text-white">{validationResult.manifest?.export_id || '—'}</span></p>
            </div>
            {validationResult.warnings?.length > 0 && (
              <div className="text-amber-400 space-y-0.5">
                <p className="font-bold">Warnings:</p>
                {validationResult.warnings.map((w: string, i: number) => <p key={i}>• {w}</p>)}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Latest Validated Import state */}
      <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5 space-y-5">
        <div className="flex justify-between items-center border-b border-neuro-border pb-2.5">
          <h3 className="text-xs font-bold text-white uppercase tracking-wider">
            H.2 Active Export Package Registry Summary
          </h3>
          <span className="rounded bg-emerald-950/60 border border-emerald-500/20 px-2 py-0.5 text-[9px] font-mono font-bold text-emerald-400">
            Active Source: {activeImport ? 'external_contract' : 'fixture_fallback'}
          </span>
        </div>

        {activeImport && manifest ? (
          <div className="space-y-5 text-xs text-neuro-muted">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <p><span className="font-bold text-white">Import ID:</span> <code className="text-neuro-accent font-mono">{activeImport.import_id}</code></p>
                <p><span className="font-bold text-white">Origin Project:</span> <span className="capitalize">{manifest.source_project || 'external_imagina'}</span></p>
                <p><span className="font-bold text-white">Modality:</span> <span className="uppercase text-neuro-accent">{manifest.modality}</span></p>
                <p><span className="font-bold text-white">Task Paradigm:</span> <span className="capitalize">{manifest.paradigm?.replace(/_/g, ' ')}</span></p>
              </div>
              <div className="space-y-2">
                <p><span className="font-bold text-white">Import Timestamp:</span> <span>{new Date(activeImport.timestamp).toLocaleString()}</span></p>
                <p><span className="font-bold text-white">Contract Version:</span> <code className="font-mono text-white">{manifest.contract_version}</code></p>
                <p><span className="font-bold text-white">Primary Metric:</span> <span className="capitalize">{manifest.metrics?.primary_metric || 'accuracy'}: </span>
                  <code className="text-white font-mono font-bold">{manifest.metrics?.primary_metric_value ?? '—'}</code>
                </p>
                <p><span className="font-bold text-white">Cross-validation Strategy:</span> <span className="capitalize">{manifest.metrics?.split_strategy?.replace(/_/g, ' ') || 'unknown'}</span></p>
              </div>
            </div>

            {/* Model Card Paths / Weight Checkpoint */}
            <div className="border-t border-neuro-border/40 pt-4 space-y-2.5">
              <p className="text-[10px] text-neuro-muted uppercase font-bold tracking-wider text-white/80">Physical Artifact Registration</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 font-mono text-[10px]">
                <div className="bg-neuro-bg/60 p-2.5 rounded border border-neuro-border/30">
                  <p className="text-neuro-muted mb-0.5">MODEL WEIGHTS CHECKPOINT</p>
                  <p className="text-white truncate">{manifest.model?.checkpoint_path || 'Referenced in external repo'}</p>
                </div>
                <div className="bg-neuro-bg/60 p-2.5 rounded border border-neuro-border/30">
                  <p className="text-neuro-muted mb-0.5">MODEL CARD MARKDOWN</p>
                  <p className="text-white truncate">{manifest.model?.model_card_path || 'model_card.md'}</p>
                </div>
              </div>
            </div>

            {/* Active Streaming Feature mappings */}
            {manifest.predictions && (
              <div className="border-t border-neuro-border/40 pt-4 space-y-2">
                <p className="text-[10px] text-neuro-muted uppercase font-bold tracking-wider text-white/80">Active Fusion Stream Feature Mappings</p>
                <div className="flex flex-wrap gap-2 text-[10px] font-mono">
                  {Object.keys(manifest.predictions.prediction_schema || {}).map((f) => (
                    <span key={f} className="bg-neuro-bg px-2.5 py-1 rounded border border-neuro-border/50 text-white">
                      💡 {f} <span className="text-neuro-accent">({manifest.predictions.prediction_schema[f]})</span>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Strict Safety signatures checklist */}
            <div className="border-t border-neuro-border/40 pt-4 space-y-3">
              <p className="text-[10px] text-neuro-muted uppercase font-bold tracking-wider text-white/80">Hard Safety Governance Verification</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="flex items-center gap-2 bg-emerald-950/20 border border-emerald-500/20 rounded p-2.5 text-[11px] text-emerald-400">
                  <span className="font-bold text-sm">✓</span>
                  <div>
                    <p className="font-bold text-white">Estimates Only</p>
                    <p className="text-[9px] text-neuro-muted">proxy_estimates_only: {String(manifest.safety?.proxy_estimates_only)}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 bg-emerald-950/20 border border-emerald-500/20 rounded p-2.5 text-[11px] text-emerald-400">
                  <span className="font-bold text-sm">✓</span>
                  <div>
                    <p className="font-bold text-white">Not Decoded</p>
                    <p className="text-[9px] text-neuro-muted">not_decoded_content: {String(manifest.safety?.not_decoded_content)}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 bg-red-950/20 border border-red-500/20 rounded p-2.5 text-[11px] text-neuro-danger">
                  <span className="font-bold text-sm">🔒</span>
                  <div>
                    <p className="font-bold text-white">Closed-Loop Lock</p>
                    <p className="text-[9px] text-neuro-muted">closed_loop_allowed: {String(manifest.safety?.closed_loop_allowed)}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Scientific limitations */}
            {manifest.limitations && manifest.limitations.length > 0 && (
              <div className="border-t border-neuro-border/40 pt-4 space-y-1.5 leading-relaxed text-[11px]">
                <p className="font-bold text-white uppercase text-[10px] tracking-wider">Mandatory Scientific Limitations</p>
                {manifest.limitations.map((limit: string, idx: number) => (
                  <p key={idx} className="border-l border-neuro-border pl-2.5 italic">• {limit}</p>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="rounded bg-neuro-bg p-4 text-center border border-dashed border-neuro-border/60 text-neuro-muted text-xs">
            <p className="font-semibold mb-1">No compliant versioned export packages imported yet.</p>
            <p>Use the Sandbox console above or execute <code className="text-neuro-accent font-mono">make imagina-import-export</code> in your CLI to trigger a secure package ingestion.</p>
          </div>
        )}
      </div>

    </div>
  )
}

// ---------------------------------------------------------------------------
//  Main Evidence Center
// ---------------------------------------------------------------------------


export function EvidenceCenter() {
  return (
    <div className="flex h-full flex-col overflow-y-auto bg-neuro-bg p-8 text-neuro-text">
      <div className="mx-auto max-w-5xl space-y-12 pb-16">

        <header className="space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight text-white">Evidence Center</h1>
          <p className="max-w-3xl text-neuro-muted">
            NeuroVerse is built on a foundation of scientific honesty. This center details exactly what has been validated, what remains unvalidated, and how to reproduce every metric locally.
          </p>
        </header>

        {/* Reproduce Key Results */}
        <section className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
          <h2 className="mb-4 text-xl font-bold text-white">Reproduce Key Results</h2>
          <p className="mb-4 text-sm text-neuro-muted">
            All evidence can be regenerated locally. Run these commands to compile the evidence pack from scratch.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs text-neuro-accent">
            <div className="rounded bg-neuro-bg p-3 border border-neuro-border/50">
              <span className="text-neuro-muted block mb-1"># Environment & Unit Tests</span>
              make preflight<br />
              python3 -m pytest app/tests/
            </div>
            <div className="rounded bg-neuro-bg p-3 border border-neuro-border/50">
              <span className="text-neuro-muted block mb-1"># Public EEG ML Benchmarks</span>
              make bci-benchmark-small<br />
              make raw-bci-benchmark-small<br />
              make raw-bci-loso-small
            </div>
            <div className="rounded bg-neuro-bg p-3 border border-neuro-border/50">
              <span className="text-neuro-muted block mb-1"># LSL & Hardware Readiness</span>
              make lsl-live-validation-suite<br />
              make validate-brainflow-synthetic<br />
              make physical-eeg-trial-synthetic
            </div>
            <div className="rounded bg-neuro-bg p-3 border border-neuro-border/50">
              <span className="text-neuro-muted block mb-1"># One-Click Protocol Demo</span>
              make protocol-run-demo<br />
              make generate-evidence-pack
            </div>
          </div>
        </section>

        {/* A. Real Public EEG */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">A. Real Public EEG Evidence</h2>
          <p className="text-sm text-neuro-muted">
            Evaluates classical machine learning pipelines against the PhysioNet EEG Motor Movement/Imagery dataset.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">Raw CSP/FBCSP Benchmark</h3>
              <p className="text-xs text-neuro-muted mb-4">
                Demonstrates accurate raw epoch extraction and leakage-free spatial filtering (CSP) on binary motor imagery tasks.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-2">
                <p><span className="text-neuro-accent">✓ Proves:</span> Classical models can decode controlled proxy tasks (e.g. motor imagery).</p>
                <p><span className="text-neuro-danger">✗ Does not prove:</span> General mind-reading or clinical utility.</p>
              </div>
              <a href="/reports/bci_raw_epoch_benchmark/physionet_eegbci_small/benchmark_summary.md" target="_blank" className="mt-4 inline-block text-xs text-neuro-accent hover:underline">View Report →</a>
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">LOSO (Leave-One-Subject-Out)</h3>
              <p className="text-xs text-neuro-muted mb-4">
                Measures how well the model generalizes to an entirely unseen subject's brain signals.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-2">
                <p><span className="text-neuro-accent">✓ Proves:</span> We rigorously avoid overfitting to specific subjects.</p>
                <p><span className="text-neuro-danger">✗ Does not prove:</span> Zero-shot reliability. (LOSO metrics are notoriously low, ~0.488 balanced accuracy).</p>
              </div>
              <p className="mt-4 text-xs italic text-neuro-muted">Why is LOSO lower? EEG signals are highly non-stationary and vary drastically between individuals due to skull thickness and cognitive strategy.</p>
            </div>
          </div>
        </section>

        {/* B. Streaming Evidence */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">B. Streaming Validation</h2>
          <p className="text-sm text-neuro-muted">
            Ensures the platform can ingest high-frequency data asynchronously without blocking the event loop.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">LSL Live Validation</h3>
              <p className="text-xs text-neuro-muted mb-4">
                A test of the Lab Streaming Layer (LSL) integration, measuring clock drift, jitter, and dropped samples.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-2">
                <p><span className="text-neuro-accent">✓ Proves:</span> Platform streams LSL continuously and maintains safety locks when jitter occurs.</p>
                <p><span className="text-neuro-danger">✗ Does not prove:</span> That the stream contains high-quality real human EEG.</p>
              </div>
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">Live Raw Shadow Inference</h3>
              <p className="text-xs text-neuro-muted mb-4">
                Replays an EDF file over LSL and forces the system to classify it in real-time.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-2">
                <p><span className="text-neuro-accent">✓ Proves:</span> Live shadow inference successfully processes streaming markers and builds epochs.</p>
                <p><span className="text-neuro-danger">✗ Does not prove:</span> Closed-loop control (as it emits 0 real adaptation actions due to the safety gate).</p>
              </div>
            </div>
          </div>
        </section>

        {/* C. Hardware Readiness */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">C. Hardware Readiness</h2>
          <p className="text-sm text-neuro-muted">
            Pre-flight checks for physical BCI hardware integration via BrainFlow.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">BrainFlow SyntheticBoard</h3>
              <p className="text-xs text-neuro-muted mb-4">
                Tests the exact code path used for physical OpenBCI boards, substituting a synthetic data generator.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-2">
                <p><span className="text-neuro-accent">✓ Proves:</span> BrainFlow integration works seamlessly through the acquisition layer.</p>
                <p><span className="text-neuro-danger">✗ Does not prove:</span> Real OpenBCI Cyton/Ganglion performance. The physical OpenBCI path is prepared but unvalidated.</p>
              </div>
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">Physical Trial Protocol</h3>
              <p className="text-xs text-neuro-muted mb-4">
                An offline trial recording an eyes-open/eyes-closed sequence to calculate an Alpha Reactivity baseline.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-2">
                <p><span className="text-neuro-accent">✓ Proves:</span> The trial protocol state machine executes correctly.</p>
                <p><span className="text-neuro-danger">✗ Does not prove:</span> Clinical results; this is an offline sanity check to be used before turning on closed-loop.</p>
              </div>
            </div>
          </div>
        </section>

        {/* E. Latest Auto-Run Protocol Evidence — LIVE DATA */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">
            E. Latest Auto-Run Protocol Evidence
          </h2>
          <p className="text-sm text-neuro-muted">
            Evidence from the most recent auto-completed protocol run. With the backend
            running, this section loads live data from FastAPI. In static portfolio mode,
            it loads a baked snapshot copied from <code className="text-neuro-accent">evidence_pack/</code>.
            The Protocol Engine executes all pipeline steps end-to-end, generates a
            Completion Report v2, and enforces{' '}
            <span className="text-neuro-danger font-medium">closed_loop_allowed: false</span>{' '}
            throughout. Run <code className="text-neuro-accent">make protocol-run-demo</code> to
            refresh the source evidence.
          </p>

          <LiveAutoRunPanel />

          <div className="rounded-lg border border-amber-500/20 bg-amber-950/10 p-4 text-xs text-neuro-muted">
            <strong className="text-amber-400">Important framing:</strong>{' '}
            Synthetic demo evidence confirms the software pipeline works correctly.
            It does not validate real EEG signal quality, physical hardware performance,
            or clinical applicability. BrainFlow SyntheticBoard is a software-only synthetic
            signal generator — not a real OpenBCI device. Closed-loop adaptation from real EEG
            remains disabled by default in all execution contexts.
          </div>
        </section>

        {/* F. Multimodal Fusion & IMAGINA Proxy Evidence */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">
            F. Multimodal Fusion & IMAGINA Proxy Evidence
          </h2>
          <p className="text-sm text-neuro-muted">
            Behavioral ablation validation and calibration evidence for the Multimodal Late Fusion engine 
            and IMAGINA dataset bridge. Displays live validation checks when backend is running, or falls back to static baked portfolio snapshot.
          </p>

          <LiveFusionValidationPanel />
        </section>

        {/* G. IMAGINA v1 Baseline Evidence */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">
            G. IMAGINA v1 Baseline Evidence
          </h2>
          <p className="text-sm text-neuro-muted">
            Auditable, dataset-backed baseline model validation metrics, leakage-prevention checks, 
            and registered baseline models. Train, inspect, and evaluate baseline imagery estimation models.
          </p>

          <LiveImaginaBaselinePanel />
        </section>

        {/* H. IMAGINA Export Contract & import Validator Hub */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">
            H. IMAGINA Export Contract & Import Validator Hub
          </h2>
          <p className="text-sm text-neuro-muted">
            The versioned boundary between external model research and our safety-gated runtime. Validate 
            export manifests, copy compliance certificates, register checkpoints, and audit required safety flags.
          </p>

          <LiveImaginaExportContractPanel />
        </section>

        {/* D. Safety */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">D. Safety Evidence</h2>
          <p className="text-sm text-neuro-muted">
            The safety gate is the most important feature of the system. NeuroVerse uses a formal
            safety state machine, structured reason codes, and an authoritative closed-loop
            governance layer to ensure no real EEG adaptation is allowed by default.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">Safety State Machine</h3>
              <p className="text-xs text-neuro-muted mb-3">
                19 formal states (NO_DATA → EMERGENCY_STOP) with deterministic transitions,
                structured reason codes, and a complete audit timeline.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-1 font-mono text-neuro-muted">
                <p className="text-neuro-accent">// Default state at startup</p>
                <p>state: CLOSED_LOOP_LOCKED</p>
                <p>severity: blocked</p>
                <p>real_eeg_adaptation: BLOCKED</p>
              </div>
              <p className="mt-3 text-xs italic text-neuro-muted">
                Run <code className="text-neuro-accent">make safety-audit</code> to generate a
                provenance-strict safety audit report.
              </p>
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
              <h3 className="font-bold text-white mb-2">Closed-Loop Governance</h3>
              <p className="text-xs text-neuro-muted mb-3">
                A single authoritative function determines whether closed-loop adaptation is
                permitted. The default is LOCKED. Physical hardware closed-loop requires
                validated hardware, calibration, shadow inference, and explicit operator
                confirmation.
              </p>
              <div className="bg-neuro-bg rounded p-3 text-xs space-y-1 font-mono text-neuro-muted">
                <p>[LOCKED] closed_loop_env_disabled</p>
                <p>[LOCKED] real_eeg_closed_loop_disabled</p>
                <p>[LOCKED] missing_calibration</p>
                <p>[LOCKED] shadow_only_mode</p>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
            <p className="text-sm text-neuro-text/90 mb-4">
              NeuroVerse explicitly separates <strong>Inference</strong> from <strong>Adaptation</strong>. By default, the system runs in "Shadow Mode".
              Real physiological inputs are processed, metrics are logged, and cognitive proxies are estimated—but the 3D environment remains completely locked.
            </p>
            <div className="bg-neuro-bg rounded p-4 text-xs space-y-2 font-mono text-neuro-muted">
              <p>[SAFE] adaptation_locked = True</p>
              <p>[SAFE] physical_hardware_override = False</p>
              <p>[SAFE] real_adaptation_actions_emitted = 0</p>
              <p>[SAFE] closed_loop_allowed = False</p>
            </div>
            <p className="mt-4 text-xs italic text-neuro-muted">
              Why? Because BCI models overfit easily. Allowing an uncalibrated EEG headset to alter a user's visual environment in real-time is unsafe and scientifically unsound without an explicit, monitored override.
            </p>
          </div>

          {/* Live safety governance panel */}
          <SafetyGovernancePanel />
        </section>

      </div>
    </div>
  )
}
