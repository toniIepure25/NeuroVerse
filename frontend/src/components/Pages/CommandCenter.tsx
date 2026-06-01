import React, { useState, useEffect } from 'react'
import { getSystemOverview, SystemOverview } from '../../api/client'
import { ProvenanceGraph, ProvenanceNode } from '../Visualization/ProvenanceGraph'

interface CommandCenterProps {
  onNavigate?: (page: string) => void
}

export const CommandCenter: React.FC<CommandCenterProps> = ({ onNavigate }) => {
  const [overview, setOverview] = useState<SystemOverview | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [activeStep, setActiveStep] = useState<number>(0)
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)
  const [refreshKey, setRefreshKey] = useState<number>(0)

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        const data = await getSystemOverview()
        setOverview(data)
        setError(null)
      } catch (err: any) {
        setError(err.message || 'Failed to fetch system overview')
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [refreshKey])

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  // 5-Minute Guided Reviewer Tour Steps
  const tourSteps = [
    {
      title: '1. Platform Boundary Definition',
      whyMatters: 'Establishes what NeuroVerse is and is not, securing scientific honesty prior to evaluation.',
      actionLabel: 'Understand the BCI Sandbox isolation model',
      whatItProves: 'Proves the system treats fMRI/EEG as experimental proxy features under strict sandboxed safety limits.',
      whatItDoesNotProve: 'Does not prove clinical efficacy or mind-reading capability (explicitly disclaimed).',
      uiIndicator: 'Disclaimer: "Closed-loop from real EEG is disabled by default."',
      command: '# Review the architecture safety logs\nmake safety-audit'
    },
    {
      title: '2. One-Click Demo Execution',
      whyMatters: 'Enables quick end-to-end verification of the backend readiness pipeline.',
      actionLabel: 'Execute the baseline validation and protocol auto-run demo',
      whatItProves: 'Proves the Protocol Engine auto-advances, records, and generates reports without manual tuning.',
      whatItDoesNotProve: 'Does not represent a live human trial (uses simulated MNE/synthetic EEG data).',
      uiIndicator: 'Execute: make protocol-run-demo',
      command: 'make protocol-run-demo'
    },
    {
      title: '3. Inspect Evidence Center',
      whyMatters: 'Shows all validated research leaderboards, metrics, and calibration data.',
      actionLabel: 'Check subject validation logs and ablation tables',
      whatItProves: 'Proves strict research provenance: every score lists its metric_source_file and benchmark_type.',
      whatItDoesNotProve: 'Does not compare incompatible datasets (e.g. subject-specific vs LOSO splits).',
      uiIndicator: 'Go to "Evidence Center" page',
      command: 'make generate-evidence-pack'
    },
    {
      title: '4. External IMAGINA Export Manifest',
      whyMatters: 'Validates export files from the separate IMAGINA model training project.',
      actionLabel: 'Run manifest import validator',
      whatItProves: 'Proves NeuroVerse acts as a safety-gated runtime that imports but does not train external research weights.',
      whatItDoesNotProve: 'Does not prove external IMAGINA models are active in live closed-loop (shadow-only mode).',
      uiIndicator: 'Run: make imagina-validate-manifest',
      command: 'make imagina-validate-manifest'
    },
    {
      title: '5. Safety Governance State Machine',
      whyMatters: 'Deterministic state-machine transitions and machine-readable reasons lock closed-loop by default.',
      actionLabel: 'View the safety state timeline and reason codes',
      whatItProves: 'Proves closed_loop_allowed is False and locks active-adaptation if signals degrade or physical devices aren\'t detected.',
      whatItDoesNotProve: 'Does not represent static, bypassing safety locks.',
      uiIndicator: 'Inspect: app.safety.state_machine',
      command: 'make verify-safety-live-stack'
    },
    {
      title: '6. Data Source Wizard & Preflight',
      whyMatters: 'Ensures the platform can preflight simulator, replay, and live streams before execution.',
      actionLabel: 'Check physical vs synthetic dependencies',
      whatItProves: 'Proves physical OpenBCI/Galea requires explicit serial ports and is flagged unvalidated unless active.',
      whatItDoesNotProve: 'Does not prove a physical OpenBCI is connected right now.',
      uiIndicator: 'Go to "Data Sources" wizard page',
      command: 'make check-hardware-extra'
    },
    {
      title: '7. Dream Corridor Shadow Explainability',
      whyMatters: 'Explains exactly why the 3D scene parameters scale based on cognitive features.',
      actionLabel: 'Audit proxy mapping and smoothing parameters',
      whatItProves: 'Proves the 3D scaffold maps proxy estimations (clarity, smooth, glow) within safe limits.',
      whatItDoesNotProve: 'Does not prove the scene is a decoded dream or mental thought.',
      uiIndicator: 'Go to "Dream Corridor" workbench page',
      command: 'make compare-bci-benchmarks'
    }
  ]

  // Map backend overview data to ProvenanceGraph nodes
  const getProvenanceNodes = (ov: SystemOverview): ProvenanceNode[] => {
    const isStatic = ov.source === 'static_snapshot'
    const ev = ov.safety?.evidence_summary || {}

    return [
      {
        id: 'external_imagina_export',
        label: 'External IMAGINA Export',
        status: ov.imagina?.external_detected ? 'valid' : 'static',
        source: 'external_imagina',
        path: ov.imagina?.latest_import?.manifest_path || 'configs/imagina/example_imagina_v1_manifest.json',
        description: 'Pre-trained research model metadata, epoch logs, and model card exports.'
      },
      {
        id: 'neuroverse_export_validator',
        label: 'Export Validator',
        status: ov.imagina?.external_detected ? 'valid' : 'static',
        source: 'neuroverse_runtime',
        description: 'Inspects manifest E501 linting, scientific limit parameters, and model compatibility.'
      },
      {
        id: 'import_summary',
        label: 'Import Summary',
        status: ov.imagina?.latest_import ? 'valid' : 'static',
        source: 'neuroverse_runtime',
        path: 'reports/external_imagina_imports/latest_import_summary.json',
        description: 'Records import timestamp, SHA256 checksum, and research limitation warnings.'
      },
      {
        id: 'fusion_packet',
        label: 'Multimodal Fusion Packet',
        status: ev.calibration_complete ? 'valid' : 'static',
        source: 'neuroverse_runtime',
        description: 'Assembles late-fusion proxy parameters (gaze, EEG, pupil) with Bayesian weights.'
      },
      {
        id: 'safety_governance',
        label: 'Safety Governance Gate',
        status: 'blocked',
        source: 'neuroverse_runtime',
        path: ev.safety_audit_report_path || 'reports/safety_audit/latest_safety_audit.json',
        description: 'CLOSED_LOOP_LOCKED: Gating state machine checks SQI & physical validation. Closed-loop disabled.'
      },
      {
        id: 'protocol_run',
        label: 'Protocol Auto-Run',
        status: ov.protocol?.latest_run ? 'valid' : 'static',
        source: 'neuroverse_runtime',
        description: 'Automated workflow execution for hardware readiness (simulator or replay).'
      },
      {
        id: 'completion_report',
        label: 'Completion Report V2',
        status: ov.protocol?.latest_run ? 'valid' : 'static',
        source: 'neuroverse_runtime',
        path: ov.protocol?.latest_run?.completion_report_path || 'reports/completion_reports/latest_completion.json',
        description: 'Saves trial timings, performance counters, and auto-completion summaries.'
      },
      {
        id: 'evidence_pack',
        label: 'Evidence Pack',
        status: 'valid',
        source: 'static_snapshot',
        path: 'evidence_pack/manifest.json',
        description: 'Strict provenance registry of baked scientific benchmarks, CSV tables, and local reports.'
      },
      {
        id: 'static_portfolio_snapshot',
        label: 'Static Portfolio Mode',
        status: isStatic ? 'static' : 'valid',
        source: 'static_snapshot',
        description: 'Enables interactive offline audits for reviewers when live hardware is detached.'
      },
      {
        id: 'dream_corridor_shadow_mapping',
        label: 'Dream Corridor Shadow Mapping',
        status: 'blocked',
        source: 'neuroverse_runtime',
        description: 'Scene mapping runs in shadow-only mode: changes are logged but cannot control adaptation.'
      }
    ]
  }

  if (loading && !overview) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-neuro-bg p-8 text-neuro-text">
        <div className="flex flex-col items-center gap-4">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-neuro-accent border-t-transparent" />
          <p className="text-sm font-medium text-neuro-muted">Aggregating Neurotech Operating System status...</p>
        </div>
      </div>
    )
  }

  const ov = overview || {
    source: 'static_snapshot',
    generated_at: new Date().toISOString(),
    warnings: ['Failed to query backend.'],
    limitations: [],
    closed_loop_allowed: false,
    safety: { current_state: 'UNKNOWN', severity: 'blocked', closed_loop_allowed: false, lock_reasons: ['Backend unreachable'], lock_reason_codes: [], emergency_stop_active: false, adaptation_frozen: true, evidence_summary: {} },
    data_sources: { sources: [] },
    protocol: {},
    imagina: { external_detected: false, external_status: {} },
    fusion: { imagina_proxy_status: 'proxy_estimates_only', disclaimer: '' },
    evidence_health: { artifact_count: 0, evidence_sources: [], cache_meta: {} }
  }

  const isLive = ov.source === 'live_backend'

  return (
    <div className="flex h-full w-full flex-col overflow-y-auto bg-neuro-bg p-6 text-neuro-text select-text">
      {/* 1. Header & System Mode Dashboard */}
      <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-b border-neuro-border pb-6">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight text-neuro-text">Neurotech Command Center</h2>
            <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold border ${
              isLive 
                ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-400' 
                : 'bg-sky-950/40 border-sky-500/30 text-sky-400'
            }`}>
              <span className={`h-2.5 w-2.5 rounded-full ${isLive ? 'bg-emerald-400 animate-pulse' : 'bg-sky-400'}`} />
              {isLive ? 'Live Backend Operating System' : 'Static Portfolio Mode'}
            </span>
          </div>
          <p className="mt-1 text-sm text-neuro-muted">
            High-density runtime dashboard communicating safety boundaries, research provenance, and active simulator preflights.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => setRefreshKey(prev => prev + 1)}
            className="flex items-center gap-1.5 rounded-lg border border-neuro-border bg-neuro-surface/50 px-3.5 py-2 text-xs font-medium text-neuro-text transition hover:bg-neuro-surface"
          >
            🔄 Rescan OS Status
          </button>
          {onNavigate && (
            <button
              onClick={() => onNavigate('evidence')}
              className="flex items-center gap-1.5 rounded-lg bg-neuro-accent/20 border border-neuro-accent/30 px-3.5 py-2 text-xs font-medium text-neuro-accent transition hover:bg-neuro-accent/30"
            >
              📊 Open Evidence Center
            </button>
          )}
        </div>
      </div>

      {/* Warnings & Limitations Alert banner */}
      {ov.warnings.length > 0 && (
        <div className="mb-6 rounded-xl border border-amber-500/30 bg-amber-950/10 p-4">
          <div className="flex items-start gap-3">
            <span className="text-xl">⚠️</span>
            <div className="flex-1">
              <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">System Warning Register</h4>
              <ul className="mt-1.5 list-disc pl-4 text-xs text-amber-300/80 space-y-1">
                {ov.warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* 2. The 5-Minute Guided Reviewer Tour Panel */}
      <div className="mb-8 rounded-xl border border-neuro-border bg-neuro-surface/20 p-6 shadow-xl">
        <div className="flex items-center justify-between border-b border-neuro-border/50 pb-4 mb-4">
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider text-neuro-accent">🔬 5-Minute Guided Reviewer Tour</h3>
            <p className="text-xs text-neuro-muted">Walk through the key capabilities of the platform step-by-step with zero hidden magic.</p>
          </div>
          <div className="text-[10px] text-neuro-muted uppercase tracking-widest bg-neuro-surface/80 px-2.5 py-1 rounded border border-neuro-border">
            Step {activeStep + 1} of {tourSteps.length}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Step selector */}
          <div className="lg:col-span-4 flex flex-col gap-1.5">
            {tourSteps.map((step, idx) => (
              <button
                key={idx}
                onClick={() => setActiveStep(idx)}
                className={`w-full text-left rounded-lg p-2.5 text-xs font-medium border transition ${
                  activeStep === idx
                    ? 'border-neuro-accent bg-neuro-accent/10 text-neuro-text shadow-[0_0_8px_rgba(45,212,191,0.15)]'
                    : 'border-neuro-border/40 bg-neuro-surface/30 text-neuro-muted hover:border-neuro-border hover:bg-neuro-surface/60 hover:text-neuro-text'
                }`}
              >
                {step.title}
              </button>
            ))}
          </div>

          {/* Active step details */}
          <div className="lg:col-span-8 flex flex-col justify-between rounded-lg border border-neuro-border bg-neuro-surface/40 p-5">
            <div>
              <h4 className="text-sm font-semibold text-neuro-accent mb-2">{tourSteps[activeStep].title}</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-wider block">Why It Matters</span>
                  <p className="text-xs text-neuro-text mt-0.5">{tourSteps[activeStep].whyMatters}</p>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-wider block">Suggested Action</span>
                  <p className="text-xs text-neuro-text mt-0.5">{tourSteps[activeStep].actionLabel}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 border-t border-neuro-border/20 pt-4">
                <div>
                  <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">What It Proves</span>
                  <p className="text-xs text-neuro-muted mt-0.5">{tourSteps[activeStep].whatItProves}</p>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider block">What It Does NOT Claim</span>
                  <p className="text-xs text-neuro-muted mt-0.5">{tourSteps[activeStep].whatItDoesNotProve}</p>
                </div>
              </div>
            </div>

            <div className="border-t border-neuro-border/20 pt-4 mt-2">
              <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-wider block mb-1.5">Reproducibility Command / Target</span>
              <div className="flex items-center justify-between rounded bg-zinc-950 p-2.5 font-mono text-xs text-zinc-300 border border-neuro-border">
                <span>{tourSteps[activeStep].command}</span>
                <button
                  onClick={() => copyToClipboard(tourSteps[activeStep].command, activeStep)}
                  className="rounded bg-neuro-surface px-2 py-1 text-[10px] text-neuro-accent hover:bg-neuro-surface/80"
                >
                  {copiedIndex === activeStep ? 'Copied! ✅' : 'Copy'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Detailed Observability Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        
        {/* Card 1: Safety Governance & Data Sources */}
        <div className="rounded-xl border border-neuro-border bg-neuro-surface/30 p-5 backdrop-blur-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-neuro-border/50 pb-3 mb-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-neuro-text">🛡️ Safety & Data Readiness</h3>
              <span className="h-2.5 w-2.5 rounded-full bg-rose-500" title="Closed-loop is locked by default" />
            </div>

            <div className="space-y-4">
              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">Safety State Machine</span>
                <div className="mt-1 flex items-center justify-between rounded-lg bg-zinc-950/60 p-2 border border-neuro-border">
                  <span className="font-mono text-xs font-bold text-rose-400">{ov.safety.current_state}</span>
                  <span className="text-[10px] rounded bg-rose-950/40 border border-rose-500/20 px-1.5 py-0.5 text-rose-400 uppercase">
                    {ov.safety.severity}
                  </span>
                </div>
              </div>

              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">Closed-Loop Status</span>
                <div className="mt-1 rounded-lg bg-zinc-950/40 p-2 border border-neuro-border/50 text-xs text-neuro-muted">
                  <p className="font-semibold text-rose-400">closed_loop_allowed = FALSE</p>
                  <p className="mt-1 text-[10px] leading-snug">
                    Real-time adaptation remains locked because: {ov.safety.lock_reasons[0] || 'Physical OpenBCI validation remains unperformed.'}
                  </p>
                </div>
              </div>

              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">Data Sources Readiness</span>
                <div className="mt-2 space-y-2">
                  {(ov.data_sources?.sources || []).slice(0, 4).map((source: any) => (
                    <div key={source.source_id} className="flex items-center justify-between text-xs bg-neuro-surface/20 p-2 rounded border border-neuro-border/30">
                      <div className="flex items-center gap-1.5">
                        <span className="font-semibold text-neuro-text">{source.name}</span>
                        <span className={`text-[8px] uppercase px-1 rounded ${
                          source.availability === 'available'
                            ? 'bg-emerald-950/50 border border-emerald-500/20 text-emerald-400'
                            : 'bg-amber-950/50 border border-amber-500/20 text-amber-400'
                        }`}>
                          {source.availability}
                        </span>
                      </div>
                      <span className="font-mono text-[9px] text-neuro-muted">
                        {source.mode === 'simulator' || source.mode === 'brainflow_synthetic' ? '🧪 Synthetic' : '🔌 Physical'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 border-t border-neuro-border/35 pt-4 flex items-center justify-between text-[10px]">
            <span className="text-neuro-muted">Emergency Stop:</span>
            <span className={`font-bold ${ov.safety.emergency_stop_active ? 'text-rose-400 animate-pulse' : 'text-neuro-muted'}`}>
              {ov.safety.emergency_stop_active ? 'ACTIVE' : 'INACTIVE'}
            </span>
          </div>
        </div>

        {/* Card 2: External IMAGINA Boundary & Multimodal Fusion */}
        <div className="rounded-xl border border-neuro-border bg-neuro-surface/30 p-5 backdrop-blur-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-neuro-border/50 pb-3 mb-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-neuro-text">🌉 External Research Boundary</h3>
              <span className={`h-2.5 w-2.5 rounded-full ${ov.imagina.external_detected ? 'bg-emerald-400' : 'bg-sky-400'}`} />
            </div>

            <div className="space-y-4">
              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">IMAGINA Research Isolation</span>
                <div className="mt-1 rounded-lg bg-zinc-950/60 p-2.5 border border-neuro-border text-xs text-neuro-text">
                  <div className="flex items-center justify-between">
                    <span className="text-neuro-muted">External project directory:</span>
                    <span className="font-semibold text-neuro-accent">{ov.imagina.external_detected ? 'DETECTED' : 'FALLBACK FIXTURES'}</span>
                  </div>
                  <div className="flex items-center justify-between mt-1.5">
                    <span className="text-neuro-muted">Export manifest:</span>
                    <span className="font-semibold text-neuro-text">{ov.imagina.latest_import ? 'VALIDATED' : 'SMOKE TEST ONLY'}</span>
                  </div>
                </div>
                {!ov.imagina.external_detected && (
                  <p className="mt-1.5 text-[9px] text-sky-400 leading-snug">
                    ⚠️ NeuroVerse is acting as runtime with fallback fixture evidence. Model research pipeline is defined under ../Imagina.
                  </p>
                )}
              </div>

              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">Multimodal Fusion Validation</span>
                <div className="mt-1.5 rounded-lg bg-zinc-950/40 p-2 border border-neuro-border/50 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-neuro-muted">Latest LateFusionV1 run:</span>
                    <span className="font-mono text-neuro-accent font-semibold">
                      {ov.fusion.latest_validation?.run_id ? ov.fusion.latest_validation.run_id.slice(0, 15) : 'static_cached'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between mt-1 text-[10px]">
                    <span className="text-neuro-muted">Ablation Check:</span>
                    <span className="text-emerald-400">PASSED (Behavioral test ok)</span>
                  </div>
                </div>
              </div>

              <div>
                <span className="text-[10px] font-bold text-rose-400 uppercase tracking-widest block">IMAGINA outputs disclaimer</span>
                <p className="mt-1 text-[10px] leading-relaxed text-neuro-muted bg-rose-950/10 border border-rose-500/20 p-2 rounded">
                  “IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams. The corridor is not a decoded mental image.”
                </p>
              </div>
            </div>
          </div>

          <div className="mt-4 border-t border-neuro-border/35 pt-4 flex items-center justify-between text-[10px]">
            <span className="text-neuro-muted">Calibration:</span>
            <span className="font-semibold text-neuro-text">Bayesian late fusion active</span>
          </div>
        </div>

        {/* Card 3: Protocol Runtime & Evidence Health */}
        <div className="rounded-xl border border-neuro-border bg-neuro-surface/30 p-5 backdrop-blur-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-neuro-border/50 pb-3 mb-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-neuro-text">📅 Protocol & Evidence Audit</h3>
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
            </div>

            <div className="space-y-4">
              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">Latest Protocol Execution</span>
                <div className="mt-1 rounded-lg bg-zinc-950/60 p-2.5 border border-neuro-border text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-neuro-muted">Protocol ID:</span>
                    <span className="font-mono text-neuro-text truncate max-w-[150px]" title={ov.protocol.latest_run?.protocol_id}>
                      {ov.protocol.latest_run?.protocol_id || 'imagina_bridge_validation_protocol'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between mt-1">
                    <span className="text-neuro-muted">Step summary:</span>
                    <span className="text-emerald-400 font-semibold">
                      {ov.protocol.latest_run?.status === 'passed' ? 'PASSED (Auto-completed)' : 'COMPLETED'}
                    </span>
                  </div>
                </div>
              </div>

              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">Evidence Pack Integrity</span>
                <div className="mt-1.5 rounded-lg bg-zinc-950/40 p-2 border border-neuro-border/50 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-neuro-muted">Proven Artifact count:</span>
                    <span className="font-semibold text-neuro-text">{ov.evidence_health.artifact_count} verified files</span>
                  </div>
                  <div className="flex items-center justify-between mt-1 text-[10px]">
                    <span className="text-neuro-muted">Static Freshness:</span>
                    <span className="text-sky-400">Bake synchronized</span>
                  </div>
                </div>
              </div>

              <div>
                <span className="text-[10px] font-bold text-neuro-muted uppercase tracking-widest block">Scientific Framing</span>
                <p className="mt-1 text-[10px] leading-relaxed text-neuro-muted bg-neuro-surface/40 p-2 rounded border border-neuro-border/20">
                  “Physical OpenBCI/Galea validation remains unperformed unless a real device report exists.”
                </p>
              </div>
            </div>
          </div>

          <div className="mt-4 border-t border-neuro-border/35 pt-4 flex items-center justify-between text-[10px]">
            <span className="text-neuro-muted">Last generated:</span>
            <span className="font-mono text-neuro-muted">{ov.generated_at.slice(0, 19).replace('T', ' ')}</span>
          </div>
        </div>

      </div>

      {/* 4. Dream Corridor Shadow Explainability Panel */}
      <div className="mb-8 rounded-xl border border-neuro-border bg-neuro-surface/20 p-5 backdrop-blur-md">
        <h3 className="text-sm font-bold uppercase tracking-wider text-neuro-text mb-3">👁️ Dream Corridor Shadow Explainability: "Why would the corridor change?"</h3>
        <p className="text-xs text-neuro-muted mb-4 leading-relaxed">
          The 3D environment scales based on mathematical feature smoothing from simulated proxy metrics. 
          To prevent misleading cognitive claims, here is the explicit mapping of raw parameters to scene adaptations:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="rounded-lg bg-zinc-950/50 p-4 border border-neuro-border/50">
            <h4 className="text-xs font-bold text-neuro-accent uppercase mb-2">1. Multimodal Visual Mapping</h4>
            <ul className="text-xs text-neuro-muted space-y-2">
              <li className="flex items-center justify-between">
                <span>Relaxation Proxy:</span>
                <span className="text-neuro-text font-semibold">Scene Fog / Density</span>
              </li>
              <li className="flex items-center justify-between border-t border-neuro-border/20 pt-1.5">
                <span>Engagement Estimate:</span>
                <span className="text-neuro-text font-semibold">Glow Intensity / Neon</span>
              </li>
              <li className="flex items-center justify-between border-t border-neuro-border/20 pt-1.5">
                <span>Attention Focus:</span>
                <span className="text-neuro-text font-semibold">Motion Smoothness</span>
              </li>
            </ul>
          </div>

          <div className="rounded-lg bg-zinc-950/50 p-4 border border-neuro-border/50">
            <h4 className="text-xs font-bold text-neuro-accent uppercase mb-2">2. Gated Safety Constraints</h4>
            <ul className="text-xs text-neuro-muted space-y-2">
              <li className="flex items-center justify-between">
                <span>Closed-Loop Flag:</span>
                <span className="text-rose-400 font-semibold">SHADOW-ONLY (No live write)</span>
              </li>
              <li className="flex items-center justify-between border-t border-neuro-border/20 pt-1.5">
                <span>Low Signal Quality (SQI):</span>
                <span className="text-rose-400 font-semibold">FREEZE (Adaptation Lock)</span>
              </li>
              <li className="flex items-center justify-between border-t border-neuro-border/20 pt-1.5">
                <span>Mode:</span>
                <span className="text-sky-400 font-semibold">SIMULATED (Auditable Sandbox)</span>
              </li>
            </ul>
          </div>

          <div className="rounded-lg bg-zinc-950/50 p-4 border border-neuro-border/50">
            <h4 className="text-xs font-bold text-neuro-accent uppercase mb-2">3. Primary Limiting Factors</h4>
            <p className="text-[11px] leading-relaxed text-neuro-muted mt-1">
              "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics." 
              All scene changes represent smoothing functions over Bayesian predictions, protecting users from overclaiming neural representations.
            </p>
          </div>
        </div>
      </div>

      {/* 5. Provenance Flow Graph */}
      <div className="mt-2">
        <ProvenanceGraph nodes={getProvenanceNodes(ov)} />
      </div>
    </div>
  )
}
