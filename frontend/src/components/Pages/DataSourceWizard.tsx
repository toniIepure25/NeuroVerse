import { useEffect, useMemo, useState } from 'react'
import {
  createProtocolRun,
  getStaticDataSources,
  listDataSources,
  preflightDataSource,
  refreshDataSource,
} from '../../api/client'
import type {
  DataSourceAvailability,
  DataSourceListResponse,
  DataSourceStatus,
} from '../../types/research'

type WizardMode = 'live_backend' | 'static_portfolio'
const PROTOCOL_CENTER_HANDOFF_KEY = 'neuroverse.protocolCenter.activeRunId'

type DataSourceWizardProps = {
  onNavigate?: (page: string) => void
}

const STATIC_SOURCES: DataSourceStatus[] = [
  {
    source_id: 'simulator',
    title: 'Built-in Simulator',
    mode: 'simulator',
    description: 'No-hardware source for the default reviewer demo and protocol run.',
    availability: 'available',
    can_run_now: false,
    can_validate_now: false,
    can_auto_run_protocol: false,
    recommended_protocol_id: 'synthetic_demo_protocol',
    required_inputs: [],
    missing_requirements: ['Start backend for live protocol preflight/start actions.'],
    installed_dependencies: {},
    detected_resources: { source: 'static_portfolio_metadata' },
    latest_evidence_paths: {},
    safety_status: { closed_loop_allowed: false },
    closed_loop_allowed: false,
    physical_hardware_validated: false,
    what_it_proves: [
      'End-to-end software demo can be reproduced when backend is running.',
      'Multimodal Fusion v1 can generate safe simulated proxy evidence.',
    ],
    what_it_does_not_prove: [
      'Real EEG dynamics or physical hardware validation.',
      'Decoded thoughts, dreams, or clinical mental-state measurements.',
    ],
    limitations: [
      'Static portfolio mode is informational only.',
      'The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.',
    ],
    next_actions: [
      'Run make dev for live readiness checks.',
      'Run the multimodal fusion demo protocol or POST /api/v1/fusion/demo-sample.',
    ],
    commands: [
      'POST /api/v1/fusion/demo-sample',
      'make protocol-run-demo',
      'make generate-evidence-pack',
      'make static-portfolio-build',
    ],
    protocol_preflight: null,
  },
  {
    source_id: 'physionet_eegbci_replay',
    title: 'PhysioNet EEGBCI EDF Replay',
    mode: 'public_eeg_replay',
    description: 'Public EEG dataset replay and benchmark source.',
    availability: 'unknown',
    can_run_now: false,
    can_validate_now: false,
    can_auto_run_protocol: false,
    recommended_protocol_id: 'eeg_lsl_replay_shadow_protocol',
    required_inputs: [],
    missing_requirements: ['Backend required to inspect local EDF availability.'],
    installed_dependencies: {},
    detected_resources: {},
    latest_evidence_paths: {},
    safety_status: { closed_loop_allowed: false },
    closed_loop_allowed: false,
    physical_hardware_validated: false,
    what_it_proves: ['Controlled public EEG proxy-task workflows when local data exists.'],
    what_it_does_not_prove: ['Unrestricted mental-state inference.'],
    limitations: ['Replay is not live physical hardware validation.'],
    next_actions: ['Run make physionet-eegbci-download locally.', 'Start backend for live checks.'],
    commands: ['make physionet-eegbci-download', 'make raw-bci-benchmark-small'],
    protocol_preflight: null,
  },
  {
    source_id: 'lsl_stream',
    title: 'LSL Stream',
    mode: 'lsl_stream',
    description: 'Local Lab Streaming Layer EEG stream.',
    availability: 'unknown',
    can_run_now: false,
    can_validate_now: false,
    can_auto_run_protocol: false,
    recommended_protocol_id: 'eeg_lsl_replay_shadow_protocol',
    required_inputs: [],
    missing_requirements: ['Backend required to discover local LSL streams.'],
    installed_dependencies: {},
    detected_resources: {},
    latest_evidence_paths: {},
    safety_status: { closed_loop_allowed: false },
    closed_loop_allowed: false,
    physical_hardware_validated: false,
    what_it_proves: ['Timing and stream integration when pylsl and a stream are available.'],
    what_it_does_not_prove: ['That a stream contains high-quality human EEG.'],
    limitations: ['Closed-loop from real EEG is disabled by default.'],
    next_actions: ['Run make eeg-lsl-replay-demo locally.', 'Refresh after backend starts.'],
    commands: ['make eeg-lsl-replay-demo', 'make validate-eeg-lsl-demo'],
    protocol_preflight: null,
  },
  {
    source_id: 'brainflow_synthetic',
    title: 'BrainFlow SyntheticBoard',
    mode: 'brainflow_synthetic',
    description: 'Synthetic BrainFlow hardware path.',
    availability: 'unknown',
    can_run_now: false,
    can_validate_now: false,
    can_auto_run_protocol: false,
    recommended_protocol_id: 'brainflow_synthetic_shadow_protocol',
    required_inputs: [],
    missing_requirements: ['Backend required to check BrainFlow installation.'],
    installed_dependencies: {},
    detected_resources: { physical_or_synthetic: 'synthetic' },
    latest_evidence_paths: {},
    safety_status: { closed_loop_allowed: false },
    closed_loop_allowed: false,
    physical_hardware_validated: false,
    what_it_proves: ['BrainFlow software-path integration when dependency exists.'],
    what_it_does_not_prove: ['Real OpenBCI physical validation.'],
    limitations: ['BrainFlow SyntheticBoard is not real OpenBCI physical validation.'],
    next_actions: ['Install hardware extras locally if needed.', 'Start backend for live checks.'],
    commands: ['make validate-brainflow-synthetic', 'make shadow-brainflow-synthetic'],
    protocol_preflight: null,
  },
  {
    source_id: 'openbci_cyton',
    title: 'OpenBCI Cyton',
    mode: 'physical_openbci',
    description: 'Prepared record-only physical OpenBCI Cyton path.',
    availability: 'unavailable',
    can_run_now: false,
    can_validate_now: false,
    can_auto_run_protocol: false,
    recommended_protocol_id: 'physical_openbci_trial_protocol',
    required_inputs: ['PORT', 'PROFILE_ID'],
    missing_requirements: ['Backend and explicit PORT are required for live hardware checks.'],
    installed_dependencies: {},
    detected_resources: {},
    latest_evidence_paths: {},
    safety_status: { closed_loop_allowed: false },
    closed_loop_allowed: false,
    physical_hardware_validated: false,
    what_it_proves: ['Only a real passing report can prove stream quality and integration.'],
    what_it_does_not_prove: ['Clinical validity or unrestricted mental-state inference.'],
    limitations: [
      'OpenBCI/Galea physical validation remains unperformed unless a real device report exists.',
      'Closed-loop from real EEG is disabled by default.',
    ],
    next_actions: ['Connect board locally, start backend, then refresh.'],
    commands: ['make discover-brainflow-devices', 'make validate-openbci-cyton PORT=/dev/ttyUSB0'],
    protocol_preflight: null,
  },
  {
    source_id: 'openbci_ganglion',
    title: 'OpenBCI Ganglion',
    mode: 'physical_openbci',
    description: 'Prepared record-only physical OpenBCI Ganglion path.',
    availability: 'unavailable',
    can_run_now: false,
    can_validate_now: false,
    can_auto_run_protocol: false,
    recommended_protocol_id: 'physical_openbci_trial_protocol',
    required_inputs: ['PORT', 'PROFILE_ID'],
    missing_requirements: ['Backend and explicit PORT are required for live hardware checks.'],
    installed_dependencies: {},
    detected_resources: {},
    latest_evidence_paths: {},
    safety_status: { closed_loop_allowed: false },
    closed_loop_allowed: false,
    physical_hardware_validated: false,
    what_it_proves: ['Only a real passing report can prove stream quality and integration.'],
    what_it_does_not_prove: ['Clinical validity or unrestricted mental-state inference.'],
    limitations: [
      'OpenBCI/Galea physical validation remains unperformed unless a real device report exists.',
      'Closed-loop from real EEG is disabled by default.',
    ],
    next_actions: ['Connect board locally, start backend, then refresh.'],
    commands: ['make discover-brainflow-devices', 'make validate-openbci-ganglion PORT=/dev/ttyUSB0'],
    protocol_preflight: null,
  },
]

function availabilityClass(availability: DataSourceAvailability): string {
  switch (availability) {
    case 'available':
      return 'bg-emerald-950/60 text-emerald-400'
    case 'partially_available':
      return 'bg-amber-950/60 text-amber-300'
    case 'unavailable':
      return 'bg-red-950/50 text-neuro-danger'
    default:
      return 'bg-neuro-bg text-neuro-muted'
  }
}

function shortPath(path: string | null | undefined): string {
  if (!path) return 'None yet'
  return path.replace(/\\/g, '/').split('/').slice(-4).join('/')
}

function sourceMeta(source: DataSourceStatus): string {
  const deps = Object.entries(source.installed_dependencies)
  if (deps.length === 0) return 'Backend required for live dependency checks'
  return deps.map(([key, value]) => `${key}: ${value ? 'ok' : 'missing'}`).join(' | ')
}

export function DataSourceWizard({ onNavigate }: DataSourceWizardProps) {
  const [sources, setSources] = useState<DataSourceStatus[]>(STATIC_SOURCES)
  const [mode, setMode] = useState<WizardMode>('static_portfolio')
  const [selectedId, setSelectedId] = useState(STATIC_SOURCES[0].source_id)
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [port, setPort] = useState('')
  const [statusMessage, setStatusMessage] = useState<string | null>(null)
  const [createdRunId, setCreatedRunId] = useState<string | null>(null)

  async function loadSources() {
    setLoading(true)
    setError(null)
    try {
      const data: DataSourceListResponse = await listDataSources()
      setSources(data.sources)
      setMode(data.mode)
      if (!data.sources.some((source) => source.source_id === selectedId)) {
        setSelectedId(data.sources[0]?.source_id ?? STATIC_SOURCES[0].source_id)
      }
    } catch (e) {
      setMode('static_portfolio')
      const liveError = e instanceof Error ? e.message : 'Backend unavailable'
      try {
        const staticData = await getStaticDataSources()
        setSources(staticData.sources.length > 0 ? staticData.sources : STATIC_SOURCES)
        setError(liveError)
      } catch {
        setSources(STATIC_SOURCES)
        setError(liveError)
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSources()
  }, [])

  const selected = useMemo(
    () => sources.find((source) => source.source_id === selectedId) ?? sources[0],
    [sources, selectedId],
  )

  const protocolInputs: Record<string, string> = selected?.mode === 'physical_openbci'
    ? {
        PORT: port,
        PROFILE_ID: selected.source_id === 'openbci_ganglion'
          ? 'openbci_ganglion_4ch'
          : 'openbci_cyton_8ch',
      }
    : {}

  async function onRefreshSelected() {
    if (!selected || mode !== 'live_backend') return
    setBusy('refresh')
    setStatusMessage(null)
    try {
      const updated = await refreshDataSource(selected.source_id)
      setSources((current) => current.map((source) => (
        source.source_id === updated.source_id ? updated : source
      )))
      setStatusMessage(`Refreshed ${updated.title}`)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Refresh failed')
    } finally {
      setBusy(null)
    }
  }

  async function onRunPreflight() {
    if (!selected || mode !== 'live_backend') return
    setBusy('preflight')
    setStatusMessage(null)
    try {
      const updated = await preflightDataSource(selected.source_id, protocolInputs)
      setSources((current) => current.map((source) => (
        source.source_id === updated.source_id ? updated : source
      )))
      setStatusMessage(
        updated.protocol_preflight?.can_start
          ? 'Preflight can start safely.'
          : 'Preflight found missing requirements.',
      )
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Preflight failed')
    } finally {
      setBusy(null)
    }
  }

  async function onStartProtocol() {
    if (!selected || mode !== 'live_backend' || !selected.protocol_preflight?.can_start) return
    if (selected.mode === 'physical_openbci' && !port) {
      setStatusMessage('Enter PORT before creating a physical hardware protocol run.')
      return
    }
    setBusy('start')
    setStatusMessage(null)
    try {
      const run = await createProtocolRun(selected.recommended_protocol_id, protocolInputs)
      setCreatedRunId(run.run_id)
      window.localStorage.setItem(PROTOCOL_CENTER_HANDOFF_KEY, run.run_id)
      setStatusMessage(`Created protocol run ${run.run_id}. Opening Protocol Center.`)
      onNavigate?.('protocols')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Protocol start failed')
    } finally {
      setBusy(null)
    }
  }

  function onOpenCreatedRun() {
    if (!createdRunId) return
    window.localStorage.setItem(PROTOCOL_CENTER_HANDOFF_KEY, createdRunId)
    onNavigate?.('protocols')
  }

  if (!selected) return null

  const resources = selected.detected_resources
  const evidenceEntries = Object.entries(selected.latest_evidence_paths ?? {})
  const canUseLiveActions = mode === 'live_backend'

  return (
    <div className="flex h-full flex-col overflow-y-auto bg-neuro-bg p-8 text-neuro-text">
      <div className="mx-auto max-w-6xl space-y-8 pb-16">
        <header className="space-y-4">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 className="text-4xl font-extrabold tracking-tight text-white">Data Source Wizard</h1>
              <p className="mt-3 max-w-3xl text-neuro-muted">
                Select a source, inspect readiness, run protocol preflight, and create safe
                protocol runs without confusing synthetic, replay, and physical hardware evidence.
              </p>
            </div>
            <button
              onClick={loadSources}
              className="rounded border border-neuro-border bg-neuro-surface px-3 py-2 text-xs text-neuro-accent hover:border-neuro-accent"
            >
              {loading ? 'Refreshing...' : 'Refresh All'}
            </button>
          </div>

          <div className={`rounded-lg border p-4 text-xs ${
            mode === 'live_backend'
              ? 'border-emerald-500/20 bg-emerald-950/10'
              : 'border-amber-500/20 bg-amber-950/10'
          }`}>
            <span className={mode === 'live_backend' ? 'font-semibold text-emerald-400' : 'font-semibold text-amber-400'}>
              {mode === 'live_backend' ? 'Live backend readiness' : 'Static portfolio mode'}
            </span>
            <span className="text-neuro-muted">
              {' '}
              {mode === 'live_backend'
                ? 'Dependency, stream, dataset, evidence, and protocol readiness are checked by FastAPI.'
                : 'Readiness is informational only. Start backend for live checks.'}
            </span>
            {error && <p className="mt-1 font-mono text-[10px] text-neuro-muted">{error}</p>}
          </div>
        </header>

        <section className="rounded-lg border border-neuro-border bg-neuro-surface p-5">
          <div className="grid grid-cols-1 gap-3 md:grid-cols-3 xl:grid-cols-6">
            {sources.map((source) => (
              <button
                key={source.source_id}
                onClick={() => setSelectedId(source.source_id)}
                className={`rounded border p-4 text-left transition ${
                  source.source_id === selected.source_id
                    ? 'border-neuro-accent bg-neuro-bg'
                    : 'border-neuro-border/60 bg-neuro-surface hover:border-neuro-accent/50'
                }`}
              >
                <span className={`mb-3 inline-block rounded px-2 py-0.5 text-[10px] font-semibold ${availabilityClass(source.availability)}`}>
                  {source.availability.replace('_', ' ')}
                </span>
                <p className="text-sm font-bold text-white">{source.title}</p>
                <p className="mt-1 text-[11px] text-neuro-muted">{source.mode.replace('_', ' ')}</p>
                <p className="mt-3 text-[10px] text-neuro-muted">
                  {mode === 'static_portfolio'
                    ? 'Snapshot only'
                    : source.can_run_now ? 'Can run now' : 'Setup required'}
                </p>
              </button>
            ))}
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
            <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-wider text-neuro-muted">Selected source</p>
                <h2 className="text-2xl font-bold text-white">{selected.title}</h2>
              </div>
              <span className={`rounded px-2 py-1 text-xs font-semibold ${availabilityClass(selected.availability)}`}>
                {selected.availability.replace('_', ' ')}
              </span>
            </div>

            <p className="mb-5 text-sm leading-relaxed text-neuro-muted">{selected.description}</p>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <Metric
                label="Run now"
                value={mode === 'static_portfolio' ? 'Static only' : selected.can_run_now ? 'Yes' : 'No'}
              />
              <Metric
                label="Validate now"
                value={mode === 'static_portfolio' ? 'Static only' : selected.can_validate_now ? 'Yes' : 'No'}
              />
              <Metric
                label="Auto-run protocol"
                value={mode === 'static_portfolio' ? 'Static only' : selected.can_auto_run_protocol ? 'Yes' : 'No'}
              />
            </div>

            {selected.mode === 'physical_openbci' && (
              <div className="mt-5 rounded border border-neuro-border/60 bg-neuro-bg p-4">
                <label className="block text-xs font-semibold text-neuro-accent" htmlFor="openbci-port">
                  PORT required for physical hardware preflight
                </label>
                <input
                  id="openbci-port"
                  value={port}
                  onChange={(event) => setPort(event.target.value)}
                  placeholder="/dev/ttyUSB0"
                  className="mt-2 w-full rounded border border-neuro-border bg-neuro-surface px-3 py-2 text-sm text-neuro-text outline-none focus:border-neuro-accent"
                />
                <p className="mt-2 text-[11px] text-neuro-muted">
                  OpenBCI runs are record-only/manual. The wizard will not auto-run physical hardware.
                </p>
              </div>
            )}

            <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2">
              <ListBlock title="Missing Requirements" items={selected.missing_requirements} tone="danger" />
              <ListBlock title="Next Actions" items={selected.next_actions} tone="accent" />
              <ListBlock title="What It Proves" items={selected.what_it_proves} tone="success" />
              <ListBlock title="What It Does Not Prove" items={selected.what_it_does_not_prove} tone="danger" />
            </div>

            <div className="mt-5 rounded border border-amber-500/20 bg-amber-950/10 p-4 text-xs text-neuro-muted">
              <p className="font-semibold text-amber-400">Safety framing</p>
              <p className="mt-1">
                Closed-loop from real EEG is disabled by default. BrainFlow SyntheticBoard is not real
                OpenBCI physical validation. OpenBCI/Galea physical validation remains unperformed
                unless a real device report exists.
              </p>
            </div>
          </div>

          <aside className="space-y-6">
            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
              <h3 className="mb-3 text-sm font-semibold text-white">Protocol Integration</h3>
              <div className="space-y-2 text-xs text-neuro-muted">
                <p>Recommended protocol:</p>
                <p className="font-mono text-neuro-accent">{selected.recommended_protocol_id}</p>
                {selected.protocol_preflight && (
                  <div className="rounded border border-neuro-border/50 bg-neuro-bg p-3">
                    <p>Can start: {selected.protocol_preflight.can_start ? 'yes' : 'no'}</p>
                    <p>Can auto-run: {selected.protocol_preflight.can_auto_run ? 'yes' : 'no'}</p>
                    <p>Policy: {selected.protocol_preflight.auto_run_policy}</p>
                  </div>
                )}
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                <button
                  disabled={!canUseLiveActions || busy !== null}
                  onClick={onRefreshSelected}
                  className="rounded border border-neuro-border px-3 py-2 text-xs text-neuro-accent disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Refresh
                </button>
                <button
                  disabled={!canUseLiveActions || busy !== null}
                  onClick={onRunPreflight}
                  className="rounded border border-neuro-accent/60 px-3 py-2 text-xs text-neuro-accent disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Run Preflight
                </button>
                <button
                  disabled={!canUseLiveActions || busy !== null || !selected.protocol_preflight?.can_start}
                  onClick={onStartProtocol}
                  className="rounded bg-neuro-accent px-3 py-2 text-xs font-semibold text-neuro-bg disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Start Protocol
                </button>
                {createdRunId && (
                  <button
                    onClick={onOpenCreatedRun}
                    className="rounded border border-neuro-border px-3 py-2 text-xs text-neuro-accent hover:border-neuro-accent"
                  >
                    Open Created Run
                  </button>
                )}
              </div>
              {statusMessage && <p className="mt-3 text-xs text-neuro-muted">{statusMessage}</p>}
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
              <h3 className="mb-3 text-sm font-semibold text-white">Dependencies</h3>
              <p className="text-xs text-neuro-muted">{sourceMeta(selected)}</p>
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
              <h3 className="mb-3 text-sm font-semibold text-white">Detected Resources</h3>
              <pre className="max-h-48 overflow-auto rounded bg-neuro-bg p-3 text-[10px] text-neuro-muted">
                {JSON.stringify(resources, null, 2)}
              </pre>
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
              <h3 className="mb-3 text-sm font-semibold text-white">Latest Evidence</h3>
              <div className="space-y-2 text-[11px] text-neuro-muted">
                {evidenceEntries.length === 0 && <p>No evidence paths in static fallback.</p>}
                {evidenceEntries.map(([key, value]) => (
                  <p key={key}>
                    <span className="text-neuro-accent">{key}:</span> {shortPath(value)}
                  </p>
                ))}
              </div>
            </div>

            <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
              <h3 className="mb-3 text-sm font-semibold text-white">Commands</h3>
              <div className="space-y-2 font-mono text-[11px] text-neuro-accent">
                {selected.commands.map((command) => (
                  <div key={command} className="rounded border border-neuro-border/40 bg-neuro-bg p-3">
                    {command}
                  </div>
                ))}
              </div>
            </div>
          </aside>
        </section>
      </div>
    </div>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded border border-neuro-border/50 bg-neuro-bg p-3">
      <p className="text-[10px] uppercase tracking-wider text-neuro-muted">{label}</p>
      <p className="mt-1 text-sm font-semibold text-white">{value}</p>
    </div>
  )
}

function ListBlock({
  title,
  items,
  tone,
}: {
  title: string
  items: string[]
  tone: 'accent' | 'success' | 'danger'
}) {
  const color = tone === 'success'
    ? 'text-emerald-400'
    : tone === 'danger'
      ? 'text-neuro-danger'
      : 'text-neuro-accent'
  return (
    <div>
      <h3 className={`mb-2 text-sm font-semibold ${color}`}>{title}</h3>
      {items.length === 0 ? (
        <p className="text-sm text-neuro-muted">None.</p>
      ) : (
        <ul className="space-y-1.5">
          {items.map((item) => (
            <li key={item} className="text-sm leading-relaxed text-neuro-muted">- {item}</li>
          ))}
        </ul>
      )}
    </div>
  )
}
