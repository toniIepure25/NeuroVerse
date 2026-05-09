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
              <span className="text-neuro-muted block mb-1"># Generate Evidence Artifacts</span>
              make generate-evidence-pack<br />
              make release-check
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

        {/* D. Safety */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white border-b border-neuro-border pb-2">D. Safety Evidence</h2>
          <p className="text-sm text-neuro-muted">
            The safety gate is the most important feature of the system.
          </p>

          <div className="rounded-lg border border-neuro-border bg-neuro-surface p-6">
            <p className="text-sm text-neuro-text/90 mb-4">
              NeuroVerse explicitly separates <strong>Inference</strong> from <strong>Adaptation</strong>. By default, the system runs in "Shadow Mode". 
              Real physiological inputs are processed, metrics are logged, and cognitive proxies are estimated—but the 3D environment remains completely locked.
            </p>
            <div className="bg-neuro-bg rounded p-4 text-xs space-y-2 font-mono text-neuro-muted">
              <p>[SAFE] adaptation_locked = True</p>
              <p>[SAFE] physical_hardware_override = False</p>
              <p>[SAFE] real_adaptation_actions_emitted = 0</p>
            </div>
            <p className="mt-4 text-xs italic text-neuro-muted">
              Why? Because BCI models overfit easily. Allowing an uncalibrated EEG headset to alter a user's visual environment in real-time is unsafe and scientifically unsound without an explicit, monitored override.
            </p>
          </div>
        </section>

      </div>
    </div>
  )
}
