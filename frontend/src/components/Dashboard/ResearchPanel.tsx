import { useEffect, useMemo, useState } from 'react'
import {
  activateModel,
  deactivateModel,
  discoverLslStreams,
  emergencyStop,
  freezeAdaptation,
  getAcquisitionStatus,
  getBrainflowDevices,
  getHardwareValidationReport,
  getHardwareValidationStatus,
  getLatestHardwareTrial,
  getLatestBciBenchmarkReport,
  getLatestRawBciBenchmarkReport,
  getLatestEvaluationReport,
  getLatestPublicEegReport,
  getLatestRealPublicEegReport,
  getLatestRawBciShadowReport,
  getLslStatus,
  getLslStreamMetadata,
  getModel,
  getRuntimeLatency,
  getRuntimeMetrics,
  getRuntimeStatus,
  listAcquisitionProfiles,
  listDatasets,
  listModels,
  selectLslStream,
  startBrainflowSyntheticCalibration,
  startBrainflowSyntheticShadow,
  startBrainflowSyntheticValidation,
  startLslCalibration,
  startEegLslValidation,
  startLslShadow,
  startLslValidation,
  startSyntheticHardwareValidation,
  unfreezeAdaptation,
} from '../../api/client'
import { useNeuroVerseStore } from '../../store/neuroverseStore'
import type {
  DatasetInfo,
  EvaluationReportItem,
  AcquisitionStatus,
  AcquisitionProfileSummary,
  HardwareValidationReport,
  HardwareValidationStatus,
  LslStatus,
  LslStreamInfo,
  ModelListResponse,
  ModelMetadata,
  RuntimeLatency,
  RuntimeMetrics,
  RuntimeStatus,
  PublicEegReportResponse,
  BciBenchmarkResponse,
  RawBciShadowResponse,
  BrainflowDeviceDiscovery,
  HardwareTrialResponse,
} from '../../types/research'

function pct(value?: number | null): string {
  if (value == null || Number.isNaN(value)) return '—'
  return `${Math.round(value * 100)}%`
}

function short(value?: string | null): string {
  return value && value.length > 0 ? value : '—'
}

function ms(value?: number | null): string {
  if (value == null || Number.isNaN(value)) return '—'
  return `${Math.round(value)} ms`
}

export function ResearchPanel() {
  const connection = useNeuroVerseStore((state) => state.connection)
  const session = useNeuroVerseStore((state) => state.session)
  const [runtime, setRuntime] = useState<RuntimeStatus | null>(null)
  const [latency, setLatency] = useState<RuntimeLatency | null>(null)
  const [metrics, setMetrics] = useState<RuntimeMetrics | null>(null)
  const [acquisition, setAcquisition] = useState<AcquisitionStatus | null>(null)
  const [validation, setValidation] = useState<HardwareValidationStatus | null>(null)
  const [validationReport, setValidationReport] = useState<HardwareValidationReport | null>(null)
  const [lslStatus, setLslStatus] = useState<LslStatus | null>(null)
  const [lslStreams, setLslStreams] = useState<LslStreamInfo[]>([])
  const [selectedLslStream, setSelectedLslStream] = useState<LslStreamInfo | null>(null)
  const [lslReportStatus, setLslReportStatus] = useState<string | null>(null)
  const [profiles, setProfiles] = useState<AcquisitionProfileSummary[]>([])
  const [models, setModels] = useState<ModelListResponse | null>(null)
  const [modelDetails, setModelDetails] = useState<Record<string, ModelMetadata>>({})
  const [datasets, setDatasets] = useState<DatasetInfo[]>([])
  const [latestReport, setLatestReport] = useState<EvaluationReportItem | null>(null)
  const [publicEegReport, setPublicEegReport] = useState<PublicEegReportResponse | null>(null)
  const [realPublicEegReport, setRealPublicEegReport] =
    useState<PublicEegReportResponse | null>(null)
  const [bciBenchmarkReport, setBciBenchmarkReport] = useState<BciBenchmarkResponse | null>(null)
  const [rawBciBenchmarkReport, setRawBciBenchmarkReport] =
    useState<BciBenchmarkResponse | null>(null)
  const [rawBciShadowReport, setRawBciShadowReport] = useState<RawBciShadowResponse | null>(null)
  const [brainflowDevices, setBrainflowDevices] = useState<BrainflowDeviceDiscovery | null>(null)
  const [hardwareTrialReport, setHardwareTrialReport] = useState<HardwareTrialResponse | null>(null)
  const [busyModel, setBusyModel] = useState<string | null>(null)
  const [busyControl, setBusyControl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function refresh() {
    try {
      setError(null)
      const [
        runtimeData,
        latencyData,
        metricsData,
        acquisitionData,
        lslData,
        validationData,
        profileData,
        modelData,
        datasetData,
        reportData,
        publicEegData,
        realPublicEegData,
        bciBenchmarkData,
        rawBciBenchmarkData,
        rawBciShadowData,
        brainflowDeviceData,
        hardwareTrialData,
      ] = await Promise.all([
        getRuntimeStatus(),
        getRuntimeLatency(),
        getRuntimeMetrics(),
        getAcquisitionStatus(),
        getLslStatus(),
        getHardwareValidationStatus(),
        listAcquisitionProfiles(),
        listModels(),
        listDatasets(),
        getLatestEvaluationReport(),
        getLatestPublicEegReport(),
        getLatestRealPublicEegReport(),
        getLatestBciBenchmarkReport(),
        getLatestRawBciBenchmarkReport(),
        getLatestRawBciShadowReport(),
        getBrainflowDevices(),
        getLatestHardwareTrial(),
      ])
      setRuntime(runtimeData)
      setLatency(latencyData)
      setMetrics(metricsData)
      setAcquisition(acquisitionData)
      setLslStatus(lslData)
      setValidation(validationData)
      setProfiles(profileData)
      setModels(modelData)
      setDatasets(datasetData)
      setLatestReport(reportData.report === null ? null : reportData)
      setPublicEegReport(publicEegData)
      setRealPublicEegReport(realPublicEegData)
      setBciBenchmarkReport(bciBenchmarkData)
      setRawBciBenchmarkReport(rawBciBenchmarkData)
      setRawBciShadowReport(rawBciShadowData)
      setBrainflowDevices(brainflowDeviceData)
      setHardwareTrialReport(hardwareTrialData)
      const detailEntries = await Promise.all(
        modelData.models.slice(0, 6).map(async (item) => {
          try {
            return [item.model_id, await getModel(item.model_id)] as const
          } catch {
            return [item.model_id, item as ModelMetadata] as const
          }
        })
      )
      setModelDetails(Object.fromEntries(detailEntries))
      if (validationData.last_report_id) {
        try {
          setValidationReport(await getHardwareValidationReport(validationData.last_report_id))
        } catch {
          setValidationReport(null)
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Research status unavailable')
    }
  }

  async function onRuntimeControl(action: 'emergency' | 'freeze' | 'unfreeze') {
    setBusyControl(action)
    setError(null)
    try {
      if (action === 'emergency') await emergencyStop()
      if (action === 'freeze') await freezeAdaptation()
      if (action === 'unfreeze') await unfreezeAdaptation()
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Runtime control failed')
    } finally {
      setBusyControl(null)
    }
  }

  async function onSyntheticValidation() {
    setBusyControl('validation')
    setError(null)
    try {
      const report = await startSyntheticHardwareValidation()
      setValidationReport(report)
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Validation failed')
    } finally {
      setBusyControl(null)
    }
  }

  async function onBrainflowAction(action: 'validation' | 'calibration' | 'shadow') {
    setBusyControl(`brainflow-${action}`)
    setError(null)
    try {
      if (action === 'validation') {
        const report = await startBrainflowSyntheticValidation()
        setValidationReport(report)
      }
      if (action === 'calibration') {
        await startBrainflowSyntheticCalibration()
      }
      if (action === 'shadow') {
        await startBrainflowSyntheticShadow()
      }
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'BrainFlow action failed')
    } finally {
      setBusyControl(null)
    }
  }

  async function onDiscoverLsl() {
    setBusyControl('lsl-discover')
    setError(null)
    try {
      const response = await discoverLslStreams()
      setLslStreams(response.streams)
      setLslReportStatus(
        response.streams.length === 0 ? 'No LSL streams detected. Start make lsl-stream-demo.' : null
      )
    } catch (e) {
      setError(e instanceof Error ? e.message : 'LSL discovery failed')
    } finally {
      setBusyControl(null)
    }
  }

  async function onSelectLsl(stream: LslStreamInfo) {
    setBusyControl('lsl-select')
    setError(null)
    try {
      const metadata = await getLslStreamMetadata(stream.stream_id)
      setSelectedLslStream(metadata)
      await selectLslStream(metadata)
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'LSL stream selection failed')
    } finally {
      setBusyControl(null)
    }
  }

  async function onLslAction(action: 'validation' | 'calibration' | 'shadow' | 'eeg-validation') {
    setBusyControl(`lsl-${action}`)
    setError(null)
    try {
      if (action === 'validation') {
        const report = await startLslValidation(selectedLslStream ?? undefined)
        setValidationReport(report)
        setLslReportStatus(`Validation ${report.passed ? 'passed' : 'failed'}`)
      }
      if (action === 'eeg-validation') {
        const report = await startEegLslValidation(selectedLslStream ?? undefined)
        setValidationReport(report)
        setLslReportStatus(`EEG replay validation ${report.passed ? 'passed' : 'failed'}`)
      }
      if (action === 'calibration') {
        await startLslCalibration(selectedLslStream ?? undefined)
        setLslReportStatus('LSL calibration report written')
      }
      if (action === 'shadow') {
        await startLslShadow(selectedLslStream ?? undefined)
        setLslReportStatus('LSL shadow report written')
      }
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : `LSL ${action} failed`)
    } finally {
      setBusyControl(null)
    }
  }

  useEffect(() => {
    void refresh()
    const timer = window.setInterval(() => void refresh(), 10000)
    return () => window.clearInterval(timer)
  }, [])

  async function onActivate(modelId: string) {
    setBusyModel(modelId)
    setError(null)
    try {
      await activateModel(modelId)
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Activation failed')
    } finally {
      setBusyModel(null)
    }
  }

  async function onDeactivate() {
    setBusyModel('__deactivate__')
    setError(null)
    try {
      await deactivateModel()
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Deactivation failed')
    } finally {
      setBusyModel(null)
    }
  }

  const active = runtime ?? models?.active
  const reportMetrics = latestReport?.metrics
  const visibleDatasets = useMemo(() => datasets.slice(0, 4), [datasets])
  const bestFbcspRaw = useMemo(
    () =>
      (rawBciBenchmarkReport?.report?.models ?? [])
        .filter((item) => item.status === 'ok' && item.model?.startsWith('fbcsp'))
        .sort(
          (a, b) =>
            (b.metrics?.balanced_accuracy ?? -1) - (a.metrics?.balanced_accuracy ?? -1)
        )[0],
    [rawBciBenchmarkReport]
  )

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 font-sans flex flex-col h-full overflow-y-auto">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h3 className="text-sm font-medium text-neuro-text">Research Panel</h3>
        <button
          type="button"
          onClick={() => void refresh()}
          className="rounded border border-neuro-border px-2 py-1 text-xs text-neuro-muted hover:text-neuro-text"
        >
          Refresh
        </button>
      </div>

      <div className="mb-4 rounded-md bg-neuro-accent/10 p-3 border border-neuro-accent/20">
        <div className="flex justify-between items-center mb-1">
          <p className="text-xs font-semibold text-neuro-accent">NeuroVerse v1.1.0-rc1</p>
          <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-neuro-surface border border-neuro-border text-neuro-muted uppercase tracking-widest">public EEG + simulated hardware + safety-locked</span>
        </div>
        <p className="text-[11px] text-neuro-text mb-2">Safety Gate: Closed-loop adaptation is locked by default. Validated workflows operate in shadow mode.</p>
        <div className="flex flex-wrap gap-2 text-[10px]">
          <a href="/evidence_pack/README.md" target="_blank" className="underline text-neuro-muted hover:text-neuro-accent">Evidence Pack</a>
          <span className="text-neuro-border">•</span>
          <a href="/reports/bci_raw_epoch_benchmark/physionet_eegbci_small/benchmark_summary.md" target="_blank" className="underline text-neuro-muted hover:text-neuro-accent">BCI Benchmark</a>
          <span className="text-neuro-border">•</span>
          <a href="/reports/hardware_trials/" target="_blank" className="underline text-neuro-muted hover:text-neuro-accent">Hardware Validation</a>
        </div>
      </div>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Runtime
        </p>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
          <dt className="text-neuro-muted">Connection</dt>
          <dd className="text-neuro-text">{connection}</dd>
          <dt className="text-neuro-muted">Estimator</dt>
          <dd className="text-neuro-text">{short(active?.active_estimator)}</dd>
          <dt className="text-neuro-muted">Model</dt>
          <dd className="break-all font-mono text-neuro-text">{short(active?.active_model_id)}</dd>
          <dt className="text-neuro-muted">Source</dt>
          <dd className="text-neuro-text">{short(active?.current_data_source)}</dd>
          <dt className="text-neuro-muted">Session</dt>
          <dd className="break-all font-mono text-neuro-text">
            {short(active?.current_session_id ?? session.session_id)}
          </dd>
          <dt className="text-neuro-muted">Replay</dt>
          <dd className="text-neuro-text">{short(active?.current_replay_status)}</dd>
          <dt className="text-neuro-muted">Frozen</dt>
          <dd className="text-neuro-text">{active?.adaptation_frozen ? 'yes' : 'no'}</dd>
        </dl>
        <div className="mt-3 grid grid-cols-3 gap-2">
          <button
            type="button"
            onClick={() => void onRuntimeControl('emergency')}
            disabled={busyControl !== null}
            className="rounded bg-neuro-danger px-2 py-1 text-[11px] font-medium text-white disabled:opacity-40"
          >
            Stop
          </button>
          <button
            type="button"
            onClick={() => void onRuntimeControl('freeze')}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Freeze
          </button>
          <button
            type="button"
            onClick={() => void onRuntimeControl('unfreeze')}
            disabled={busyControl !== null || active?.emergency_stop_active}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Unfreeze
          </button>
        </div>
        {active?.freeze_reason && (
          <p className="mt-2 text-[11px] text-neuro-muted">{active.freeze_reason}</p>
        )}
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Public EEG / BCI Classifier
        </p>
        {publicEegReport?.report ? (
          <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
            <dt className="text-neuro-muted">Run</dt>
            <dd className="truncate text-neuro-text">{short(publicEegReport.report.run_id)}</dd>
            <dt className="text-neuro-muted">Source</dt>
            <dd className="text-neuro-text">
              {publicEegReport.report.fixture_mode ? 'fixture' : 'local file'}
            </dd>
            <dt className="text-neuro-muted">Model</dt>
            <dd className="truncate text-neuro-text">{short(publicEegReport.report.model_dir)}</dd>
            <dt className="text-neuro-muted">Balanced acc</dt>
            <dd className="text-neuro-text">
              {pct(publicEegReport.report.classifier_metrics?.balanced_accuracy)}
            </dd>
            <dt className="text-neuro-muted">Macro F1</dt>
            <dd className="text-neuro-text">
              {pct(publicEegReport.report.classifier_metrics?.macro_f1)}
            </dd>
            <dt className="text-neuro-muted">Predictions</dt>
            <dd className="text-neuro-text">
              {publicEegReport.report.classifier_shadow?.predictions?.length ?? 0}
            </dd>
            <dt className="text-neuro-muted">Closed loop</dt>
            <dd className="text-neuro-text">
              {publicEegReport.report.closed_loop_allowed ? 'unlocked' : 'locked'}
            </dd>
          </dl>
        ) : (
          <p className="text-xs text-neuro-muted">
            No public EEG validation run yet. Run make public-eeg-fixture-suite.
          </p>
        )}
        <p className="mt-2 text-[11px] text-neuro-muted">
          Learned EEG classifiers are shadow-only by default and predict controlled task labels.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Real Public EEG Evidence
        </p>
        {realPublicEegReport?.report ? (
          <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
            <dt className="text-neuro-muted">Run</dt>
            <dd className="truncate text-neuro-text">{short(realPublicEegReport.report.run_id)}</dd>
            <dt className="text-neuro-muted">Source</dt>
            <dd className="text-neuro-text">{short(realPublicEegReport.report.source_mode)}</dd>
            <dt className="text-neuro-muted">Split</dt>
            <dd className="text-neuro-text">{short(realPublicEegReport.report.split_strategy)}</dd>
            <dt className="text-neuro-muted">Epochs</dt>
            <dd className="text-neuro-text">
              {realPublicEegReport.report.feature_summary?.row_count ?? '—'}
            </dd>
            <dt className="text-neuro-muted">Balanced acc</dt>
            <dd className="text-neuro-text">
              {pct(realPublicEegReport.report.classifier_metrics?.balanced_accuracy)}
            </dd>
            <dt className="text-neuro-muted">Macro F1</dt>
            <dd className="text-neuro-text">
              {pct(realPublicEegReport.report.classifier_metrics?.macro_f1)}
            </dd>
            <dt className="text-neuro-muted">LSL validation</dt>
            <dd className="text-neuro-text">
              {realPublicEegReport.report.lsl?.validation?.passed === undefined
                ? '—'
                : realPublicEegReport.report.lsl.validation.passed ? 'pass' : 'warn'}
            </dd>
            <dt className="text-neuro-muted">Closed loop</dt>
            <dd className="text-neuro-text">
              {realPublicEegReport.report.closed_loop_allowed ? 'unlocked' : 'locked'}
            </dd>
          </dl>
        ) : (
          <p className="text-xs text-neuro-muted">
            No real public EEG run yet. Run make real-public-eeg-suite with a local dataset config.
          </p>
        )}
        <p className="mt-2 text-[11px] text-neuro-muted">
          This classifier predicts controlled event labels, not thoughts.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          BCI Benchmark
        </p>
        {bciBenchmarkReport?.report ? (
          <>
            <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
              <dt className="text-neuro-muted">Benchmark</dt>
              <dd className="truncate text-neuro-text">
                {short(bciBenchmarkReport.report.benchmark_id)}
              </dd>
              <dt className="text-neuro-muted">Split</dt>
              <dd className="text-neuro-text">{short(bciBenchmarkReport.report.split_strategy)}</dd>
              <dt className="text-neuro-muted">Rows</dt>
              <dd className="text-neuro-text">
                {bciBenchmarkReport.report.filter_summary?.kept_rows ?? '—'}
              </dd>
              <dt className="text-neuro-muted">Best model</dt>
              <dd className="truncate text-neuro-text">
                {short(bciBenchmarkReport.report.best_model?.model)}
              </dd>
              <dt className="text-neuro-muted">Balanced acc</dt>
              <dd className="text-neuro-text">
                {pct(bciBenchmarkReport.report.best_model?.metrics?.balanced_accuracy)}
              </dd>
              <dt className="text-neuro-muted">Macro F1</dt>
              <dd className="text-neuro-text">
                {pct(bciBenchmarkReport.report.best_model?.metrics?.macro_f1)}
              </dd>
              <dt className="text-neuro-muted">CI bal acc</dt>
              <dd className="text-neuro-text">
                {bciBenchmarkReport.report.best_model?.bootstrap_confidence_intervals?.balanced_accuracy
                  ? `${pct(bciBenchmarkReport.report.best_model.bootstrap_confidence_intervals.balanced_accuracy.lower_95)}-${pct(bciBenchmarkReport.report.best_model.bootstrap_confidence_intervals.balanced_accuracy.upper_95)}`
                  : '—'}
              </dd>
              <dt className="text-neuro-muted">Closed loop</dt>
              <dd className="text-neuro-text">
                {bciBenchmarkReport.report.closed_loop_allowed ? 'unlocked' : 'locked'}
              </dd>
            </dl>
            <ul className="mt-2 space-y-1 text-[11px] text-neuro-muted">
              {(bciBenchmarkReport.report.models ?? []).slice(0, 4).map((item) => (
                <li key={`${item.model}-${item.status}`}>
                  {item.model}: {item.status}
                  {item.metrics?.balanced_accuracy != null
                    ? ` · bal ${pct(item.metrics.balanced_accuracy)}`
                    : item.reason ? ` · ${item.reason}` : ''}
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p className="text-xs text-neuro-muted">
            No BCI benchmark yet. Run make bci-benchmark-small.
          </p>
        )}
        <p className="mt-2 text-[11px] text-neuro-muted">
          This benchmark predicts controlled task labels from event-locked EEG. It is not a
          thought decoder.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Raw-Epoch CSP Benchmark
        </p>
        {rawBciBenchmarkReport?.report ? (
          <>
            <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
              <dt className="text-neuro-muted">Benchmark</dt>
              <dd className="truncate text-neuro-text">
                {short(rawBciBenchmarkReport.report.benchmark_id)}
              </dd>
              <dt className="text-neuro-muted">Split</dt>
              <dd className="text-neuro-text">{short(rawBciBenchmarkReport.report.split_strategy)}</dd>
              <dt className="text-neuro-muted">Epochs</dt>
              <dd className="text-neuro-text">{rawBciBenchmarkReport.report.shape?.[0] ?? '—'}</dd>
              <dt className="text-neuro-muted">Best model</dt>
              <dd className="truncate text-neuro-text">
                {short(rawBciBenchmarkReport.report.best_model?.model)}
                {rawBciBenchmarkReport.report.best_model?.n_components
                  ? ` csp=${rawBciBenchmarkReport.report.best_model.n_components}`
                  : ''}
              </dd>
              <dt className="text-neuro-muted">Balanced acc</dt>
              <dd className="text-neuro-text">
                {pct(rawBciBenchmarkReport.report.best_model?.metrics?.balanced_accuracy)}
              </dd>
              <dt className="text-neuro-muted">Macro F1</dt>
              <dd className="text-neuro-text">
                {pct(rawBciBenchmarkReport.report.best_model?.metrics?.macro_f1)}
              </dd>
              <dt className="text-neuro-muted">LOSO</dt>
              <dd className="text-neuro-text">
                {rawBciBenchmarkReport.report.loso?.available
                  ? pct(rawBciBenchmarkReport.report.loso.mean_balanced_accuracy)
                  : 'not run'}
              </dd>
              <dt className="text-neuro-muted">Best FBCSP</dt>
              <dd className="text-neuro-text">
                {bestFbcspRaw
                  ? `${pct(bestFbcspRaw.metrics?.balanced_accuracy)} bal`
                  : 'not run'}
              </dd>
              <dt className="text-neuro-muted">Closed loop</dt>
              <dd className="text-neuro-text">
                {rawBciBenchmarkReport.report.closed_loop_allowed ? 'unlocked' : 'locked'}
              </dd>
            </dl>
            <ul className="mt-2 space-y-1 text-[11px] text-neuro-muted">
              {(rawBciBenchmarkReport.report.models ?? []).slice(0, 4).map((item) => (
                <li key={`${item.model}-${item.n_components}-${item.status}`}>
                  {item.model} csp={item.n_components}: {item.status}
                  {item.metrics?.balanced_accuracy != null
                    ? ` · bal ${pct(item.metrics.balanced_accuracy)}`
                    : item.reason ? ` · ${item.reason}` : ''}
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p className="text-xs text-neuro-muted">
            No raw-epoch CSP benchmark yet. Run make raw-bci-benchmark-small.
          </p>
        )}
        <p className="mt-2 text-[11px] text-neuro-muted">
          CSP is fit inside train splits on raw EEG epochs. This is shadow-only BCI
          benchmark evidence, not corridor control.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Live Raw BCI Shadow
        </p>
        {rawBciShadowReport?.report ? (
          <>
            <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
              <dt className="text-neuro-muted">Mode</dt>
              <dd className="text-neuro-text">{short(rawBciShadowReport.report.mode)}</dd>
              <dt className="text-neuro-muted">Model</dt>
              <dd className="truncate text-neuro-text">{short(rawBciShadowReport.report.model_id)}</dd>
              <dt className="text-neuro-muted">Markers</dt>
              <dd className="text-neuro-text">{rawBciShadowReport.report.markers_seen ?? '—'}</dd>
              <dt className="text-neuro-muted">Epochs</dt>
              <dd className="text-neuro-text">{rawBciShadowReport.report.epochs_built ?? '—'}</dd>
              <dt className="text-neuro-muted">Predictions</dt>
              <dd className="text-neuro-text">{rawBciShadowReport.report.prediction_count ?? '—'}</dd>
              <dt className="text-neuro-muted">Missed</dt>
              <dd className="text-neuro-text">{rawBciShadowReport.report.missed_epochs ?? 0}</dd>
              <dt className="text-neuro-muted">Balanced acc</dt>
              <dd className="text-neuro-text">
                {pct(rawBciShadowReport.report.metrics?.balanced_accuracy)}
              </dd>
              <dt className="text-neuro-muted">Actions</dt>
              <dd className="text-neuro-text">
                {rawBciShadowReport.report.real_adaptation_actions_emitted ?? 0}
              </dd>
              <dt className="text-neuro-muted">Closed loop</dt>
              <dd className="text-neuro-text">
                {rawBciShadowReport.report.closed_loop_allowed ? 'unlocked' : 'locked'}
              </dd>
            </dl>
            {rawBciShadowReport.report.fallback_reason ? (
              <p className="mt-2 text-[11px] text-neuro-muted">
                Fallback reason: {rawBciShadowReport.report.fallback_reason}
              </p>
            ) : null}
          </>
        ) : (
          <p className="text-xs text-neuro-muted">
            No live raw BCI shadow report yet. Run make live-shadow-best-raw-bci-model.
          </p>
        )}
        <p className="mt-2 text-[11px] text-neuro-muted">
          Live shadow predicts controlled task labels from replayed EEG markers and emits no
          Dream Corridor adaptation actions.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <div className="mb-2 flex items-center justify-between gap-2">
          <p className="text-xs font-medium uppercase tracking-wide text-neuro-muted">
            LSL Validation
          </p>
          <button
            type="button"
            onClick={() => void onDiscoverLsl()}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Discover
          </button>
        </div>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
          <dt className="text-neuro-muted">pylsl</dt>
          <dd className="text-neuro-text">{lslStatus?.pylsl_available ? 'available' : 'not installed'}</dd>
          <dt className="text-neuro-muted">Live demo</dt>
          <dd className="text-neuro-text">make lsl-stream-demo</dd>
          <dt className="text-neuro-muted">Selected</dt>
          <dd className="break-all text-neuro-text">{short(selectedLslStream?.name)}</dd>
          <dt className="text-neuro-muted">Timing</dt>
          <dd className="text-neuro-text">{short(validationReport?.timing?.quality)}</dd>
          <dt className="text-neuro-muted">Rate</dt>
          <dd className="text-neuro-text">{selectedLslStream?.nominal_srate ?? '—'} Hz</dd>
          <dt className="text-neuro-muted">Channels</dt>
          <dd className="text-neuro-text">{selectedLslStream?.channel_count ?? '—'}</dd>
          <dt className="text-neuro-muted">Clock offset</dt>
          <dd className="text-neuro-text">
            {validationReport?.timing?.clock_offset_estimate?.toFixed(4) ?? '—'}
          </dd>
          <dt className="text-neuro-muted">Duplicates</dt>
          <dd className="text-neuro-text">{validationReport?.timing?.duplicate_count ?? '—'}</dd>
        </dl>
        {lslStreams.length === 0 ? (
          <p className="mt-2 text-[11px] text-neuro-muted">
            {lslStatus?.install_hint ?? 'No LSL streams detected. Start make lsl-stream-demo.'}
          </p>
        ) : (
          <ul className="mt-2 space-y-2">
            {lslStreams.slice(0, 3).map((stream) => (
              <li key={stream.stream_id} className="rounded border border-neuro-border p-2 text-[11px]">
                <button
                  type="button"
                  onClick={() => void onSelectLsl(stream)}
                  className="text-left font-mono text-neuro-text hover:text-neuro-accent"
                >
                  {stream.name ?? 'unnamed'} · {stream.type ?? 'unknown'} ·{' '}
                  {stream.channel_count ?? '—'} ch · {stream.nominal_srate ?? '—'} Hz
                </button>
              </li>
            ))}
          </ul>
        )}
        <div className="mt-3 grid grid-cols-3 gap-2">
          <button
            type="button"
            onClick={() => void onLslAction('validation')}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Validate
          </button>
          <button
            type="button"
            onClick={() => void onLslAction('calibration')}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Calibrate
          </button>
          <button
            type="button"
            onClick={() => void onLslAction('shadow')}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Shadow
          </button>
        </div>
        {lslReportStatus && <p className="mt-2 text-[11px] text-neuro-muted">{lslReportStatus}</p>}
        <p className="mt-2 text-[11px] text-neuro-muted">
          LSL closed-loop adaptation is disabled until validation, calibration, and shadow
          inference pass.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          EEG Replay over LSL
        </p>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
          <dt className="text-neuro-muted">Start stream</dt>
          <dd className="text-neuro-text">make eeg-lsl-replay-demo</dd>
          <dt className="text-neuro-muted">Suite</dt>
          <dd className="text-neuro-text">make eeg-lsl-live-suite</dd>
          <dt className="text-neuro-muted">Markers</dt>
          <dd className="text-neuro-text">
            {validationReport?.markers?.marker_count ?? '—'}
          </dd>
          <dt className="text-neuro-muted">Alignment</dt>
          <dd className="text-neuro-text">
            {validationReport?.markers?.marker_alignment_pass === undefined
              ? '—'
              : validationReport.markers.marker_alignment_pass ? 'pass' : 'warn'}
          </dd>
          <dt className="text-neuro-muted">SQI</dt>
          <dd className="text-neuro-text">{pct(validationReport?.sqi_summary?.mean)}</dd>
          <dt className="text-neuro-muted">Bad channels</dt>
          <dd className="text-neuro-text">
            {validationReport?.artifact_summary?.bad_channel_candidates?.length ?? 0}
          </dd>
        </dl>
        <button
          type="button"
          onClick={() => void onLslAction('eeg-validation')}
          disabled={busyControl !== null}
          className="mt-3 rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
        >
          Validate EEG Replay
        </button>
        <p className="mt-2 text-[11px] text-neuro-muted">
          Real EEG replay and fixture mode remain record-only; the corridor stays safety-locked.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          System Metrics
        </p>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
          <dt className="text-neuro-muted">Tick latency</dt>
          <dd className="text-neuro-text">{ms(latency?.latency_ms?.total_tick?.mean)}</dd>
          <dt className="text-neuro-muted">P95 latency</dt>
          <dd className="text-neuro-text">{ms(latency?.latency_ms?.total_tick?.p95)}</dd>
          <dt className="text-neuro-muted">Ticks</dt>
          <dd className="text-neuro-text">{metrics?.ticks_processed ?? 0}</dd>
          <dt className="text-neuro-muted">Dropped events</dt>
          <dd className="text-neuro-text">{metrics?.dropped_events ?? 0}</dd>
          <dt className="text-neuro-muted">Clients</dt>
          <dd className="text-neuro-text">{metrics?.connected_clients ?? 0}</dd>
          <dt className="text-neuro-muted">Avg SQI</dt>
          <dd className="text-neuro-text">{pct(metrics?.average_multimodal_sqi)}</dd>
        </dl>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Acquisition
        </p>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
          <dt className="text-neuro-muted">Adapter</dt>
          <dd className="text-neuro-text">{short(acquisition?.active_adapter)}</dd>
          <dt className="text-neuro-muted">BrainFlow</dt>
          <dd className="text-neuro-text">
            {acquisition?.optional_dependencies?.brainflow ? 'available' : 'not installed'}
          </dd>
          <dt className="text-neuro-muted">LSL</dt>
          <dd className="text-neuro-text">
            {acquisition?.optional_dependencies?.pylsl ? 'available' : 'not installed'}
          </dd>
          <dt className="text-neuro-muted">XDF</dt>
          <dd className="text-neuro-text">
            {acquisition?.optional_dependencies?.pyxdf ? 'available' : 'not installed'}
          </dd>
        </dl>
        {acquisition?.last_error && (
          <p className="mt-2 text-xs text-neuro-danger">{acquisition.last_error}</p>
        )}
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Physical EEG Trial
        </p>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
          <dt className="text-neuro-muted">Serial devices</dt>
          <dd className="text-neuro-text">{brainflowDevices?.devices?.length ?? 0}</dd>
          <dt className="text-neuro-muted">pyserial</dt>
          <dd className="text-neuro-text">
            {brainflowDevices?.pyserial_available ? 'available' : 'not installed'}
          </dd>
          <dt className="text-neuro-muted">Trial</dt>
          <dd className="truncate text-neuro-text">
            {short(hardwareTrialReport?.report?.trial_id)}
          </dd>
          <dt className="text-neuro-muted">Mode</dt>
          <dd className="text-neuro-text">
            {hardwareTrialReport?.report?.synthetic_mode
              ? 'synthetic'
              : hardwareTrialReport?.report?.physical_device_detected
                ? 'physical'
                : 'no device'}
          </dd>
          <dt className="text-neuro-muted">Alpha status</dt>
          <dd className="text-neuro-text">
            {short(hardwareTrialReport?.report?.alpha_reactivity?.status)}
          </dd>
          <dt className="text-neuro-muted">Alpha ratio</dt>
          <dd className="text-neuro-text">
            {hardwareTrialReport?.report?.alpha_reactivity?.aggregate_alpha_ratio?.toFixed(2) ?? '—'}
          </dd>
          <dt className="text-neuro-muted">SQI</dt>
          <dd className="text-neuro-text">
            {pct(hardwareTrialReport?.report?.validation?.sqi_summary?.mean)}
          </dd>
          <dt className="text-neuro-muted">Shadow actions</dt>
          <dd className="text-neuro-text">
            {hardwareTrialReport?.report?.shadow?.real_adaptation_actions_emitted
              ?? hardwareTrialReport?.report?.real_adaptation_actions_emitted
              ?? 0}
          </dd>
          <dt className="text-neuro-muted">Closed loop</dt>
          <dd className="text-neuro-text">
            {hardwareTrialReport?.report?.closed_loop_allowed ? 'unlocked' : 'locked'}
          </dd>
        </dl>
        {brainflowDevices?.devices && brainflowDevices.devices.length > 0 ? (
          <ul className="mt-2 space-y-1 text-[11px] text-neuro-muted">
            {brainflowDevices.devices.slice(0, 3).map((device) => (
              <li key={device.device}>
                {device.device} {device.likely_openbci ? '· likely OpenBCI' : ''}
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-[11px] text-neuro-muted">
            No serial device detected. Run make discover-brainflow-devices, then use
            make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0 when a board is connected.
          </p>
        )}
        {hardwareTrialReport?.report?.reason && (
          <p className="mt-2 text-[11px] text-neuro-muted">
            {hardwareTrialReport.report.reason}
          </p>
        )}
        <p className="mt-2 text-[11px] text-neuro-muted">
          Eyes-open / eyes-closed alpha reactivity is a record-only sanity check, not a
          medical test or corridor-control signal.
        </p>
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <div className="mb-2 flex items-center justify-between gap-2">
          <p className="text-xs font-medium uppercase tracking-wide text-neuro-muted">
            Hardware Validation
          </p>
          <button
            type="button"
            onClick={() => void onSyntheticValidation()}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            Validate
          </button>
        </div>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs">
          <dt className="text-neuro-muted">State</dt>
          <dd className="text-neuro-text">{short(validation?.state)}</dd>
          <dt className="text-neuro-muted">Board</dt>
          <dd className="truncate text-neuro-text">
            {short(validationReport?.board?.board_name as string | undefined)}
          </dd>
          <dt className="text-neuro-muted">Closed loop</dt>
          <dd className="text-neuro-text">{validation?.closed_loop_allowed ? 'allowed' : 'locked'}</dd>
          <dt className="text-neuro-muted">Observed rate</dt>
          <dd className="text-neuro-text">
            {validationReport?.timing?.observed_rate_hz?.toFixed(1) ?? '—'} Hz
          </dd>
          <dt className="text-neuro-muted">Jitter p95</dt>
          <dd className="text-neuro-text">{ms(validationReport?.timing?.jitter_ms_p95)}</dd>
          <dt className="text-neuro-muted">Gaps</dt>
          <dd className="text-neuro-text">{validationReport?.timing?.gap_count ?? '—'}</dd>
          <dt className="text-neuro-muted">Channels</dt>
          <dd className="text-neuro-text">
            {validationReport?.channel_mapping?.observed_channel_count ?? '—'}
          </dd>
        </dl>
        {validation?.reason && <p className="mt-2 text-[11px] text-neuro-muted">{validation.reason}</p>}
        {profiles.length === 0 ? (
          <p className="mt-2 text-[11px] text-neuro-muted">No acquisition profiles found.</p>
        ) : (
          <p className="mt-2 text-[11px] text-neuro-muted">
            Profiles {profiles.length} ·{' '}
            {profiles.filter((profile) => profile.validation?.ok).length} valid
          </p>
        )}
        <div className="mt-3 grid grid-cols-3 gap-2">
          <button
            type="button"
            onClick={() => void onBrainflowAction('validation')}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            BF Validate
          </button>
          <button
            type="button"
            onClick={() => void onBrainflowAction('calibration')}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            BF Calibrate
          </button>
          <button
            type="button"
            onClick={() => void onBrainflowAction('shadow')}
            disabled={busyControl !== null}
            className="rounded border border-neuro-border px-2 py-1 text-[11px] text-neuro-muted hover:text-neuro-text disabled:opacity-40"
          >
            BF Shadow
          </button>
        </div>
        <p className="mt-2 text-[11px] text-neuro-muted">
          BrainFlow controls use the SyntheticBoard by default. Physical OpenBCI trials must
          pass an explicit serial port and remain record-only.
        </p>
      </section>

      <section className="mb-4">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-xs font-medium uppercase tracking-wide text-neuro-muted">
            Model Registry
          </p>
          <button
            type="button"
            onClick={() => void onDeactivate()}
            disabled={busyModel !== null || active?.active_estimator !== 'learned'}
            className="rounded border border-neuro-border px-2 py-1 text-xs text-neuro-muted hover:text-neuro-text disabled:cursor-not-allowed disabled:opacity-40"
          >
            Heuristic
          </button>
        </div>
        {!models || models.models.length === 0 ? (
          <p className="rounded-md bg-neuro-bg/50 p-3 text-xs text-neuro-muted">No models registered.</p>
        ) : (
          <ul className="space-y-2">
            {models.models.slice(0, 4).map((model) => {
              const details = modelDetails[model.model_id]
              const isActive = active?.active_model_id === model.model_id
              return (
                <li key={model.model_id} className="rounded-md border border-neuro-border bg-neuro-bg/40 p-2">
                  <div className="mb-1 flex items-start justify-between gap-2">
                    <div>
                      <p className="break-all font-mono text-xs text-neuro-text">{model.model_id}</p>
                      <p className="text-[11px] text-neuro-muted">
                        {short(model.model_type)} · {short(model.target)} ·{' '}
                        {short(details?.prediction_semantics ?? model.prediction_semantics)}
                      </p>
                      {model.metrics && (
                        <p className="text-[11px] text-neuro-muted">
                          Acc {pct(model.metrics.accuracy)} · F1 {pct(model.metrics.macro_f1)}
                        </p>
                      )}
                    </div>
                    <button
                      type="button"
                      onClick={() => void onActivate(model.model_id)}
                      disabled={busyModel !== null || isActive}
                      className="rounded bg-neuro-accent px-2 py-1 text-[11px] font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      {isActive ? 'Active' : busyModel === model.model_id ? 'Activating' : 'Activate'}
                    </button>
                  </div>
                </li>
              )
            })}
          </ul>
        )}
      </section>

      <section className="mb-4 rounded-md border border-neuro-border bg-neuro-bg/40 p-3">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Latest Evaluation
        </p>
        {latestReport ? (
          <div className="space-y-1 text-xs">
            <p className="break-all font-mono text-neuro-text">{latestReport.report_id}</p>
            <p className="text-neuro-muted">
              Accuracy {pct(reportMetrics?.accuracy)} · Balanced {pct(reportMetrics?.balanced_accuracy)}
            </p>
            <p className="text-neuro-muted">
              Macro F1 {pct(reportMetrics?.macro_f1)} · ECE {pct(reportMetrics?.ece)}
            </p>
            {latestReport.markdown && (
              <details className="mt-2">
                <summary className="cursor-pointer text-neuro-accent">Report text</summary>
                <pre className="mt-2 max-h-40 overflow-auto whitespace-pre-wrap rounded bg-black/30 p-2 text-[11px] text-neuro-muted">
                  {latestReport.markdown.slice(0, 2000)}
                </pre>
              </details>
            )}
          </div>
        ) : (
          <p className="text-xs text-neuro-muted">No evaluation reports yet.</p>
        )}
      </section>

      <section className="mb-4">
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
          Datasets
        </p>
        {visibleDatasets.length === 0 ? (
          <p className="rounded-md bg-neuro-bg/50 p-3 text-xs text-neuro-muted">No dataset configs found.</p>
        ) : (
          <ul className="space-y-2">
            {visibleDatasets.map((dataset) => (
              <li key={dataset.dataset_id ?? dataset.config} className="rounded-md border border-neuro-border bg-neuro-bg/40 p-2 text-xs">
                <p className="font-mono text-neuro-text">{dataset.dataset_id ?? 'unknown'}</p>
                <p className="text-neuro-muted">
                  {short(dataset.source)} · {(dataset.modalities ?? []).join(', ') || 'no modalities'}
                </p>
                <p className="text-neuro-muted">
                  Subjects {(dataset.subjects ?? []).length} · Sessions {(dataset.sessions ?? []).length}
                </p>
                {dataset.error && <p className="mt-1 text-neuro-danger">{dataset.error}</p>}
              </li>
            ))}
          </ul>
        )}
      </section>

      <p className="rounded-md border border-neuro-border bg-neuro-bg/60 p-3 text-[11px] leading-relaxed text-neuro-muted">
        NeuroVerse estimates cognitive proxies from simulated or dataset-derived signals. It is a
        research prototype, not a medical device, and does not read thoughts. The corridor is not a
        decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.
      </p>

      {error && (
        <p className="mt-3 text-xs text-neuro-danger" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
