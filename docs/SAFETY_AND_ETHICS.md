# Safety and Ethics

## Disclaimer

NeuroVerse is a **research prototype**. It is not a medical device, clinical tool, or validated diagnostic system. No claims are made about therapeutic efficacy, clinical accuracy, or health benefits.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

## Core Principles

### Neural Privacy
- All biosignal processing occurs locally. No neural data is transmitted to external servers.
- Session recordings are stored on the local filesystem only.
- Users control when recording starts and stops.

### Research-Only Use
- This system is intended for research, education, and prototyping purposes only.
- It should not be used for clinical diagnosis, treatment decisions, or medical purposes.
- Cognitive state estimates are physiological correlates and research proxies, not validated biomarkers.

### No Medical Claims
- The system does not diagnose any condition.
- "Focus," "stress," "fatigue," and other labels are estimated proxies based on simplified physiological correlates.
- These estimates have not been clinically validated.

### Cognitive Liberty
- Users must provide informed consent before any biosignal recording.
- Users can stop a session at any time.
- No coercive use of cognitive state data is intended or supported.

## Safety Architecture

### Signal Quality Gating
- The safety gate blocks adaptation actions when signal quality drops below configured thresholds.
- Low-quality signals trigger WAIT or BLOCKED states to prevent unreliable adaptations.

### Confidence Gating
- Adaptation actions require minimum model confidence (default 0.45).
- Very low confidence (< 0.25) triggers a full FREEZE.

### Intensity Limiting
- High stress states automatically reduce adaptation intensity.
- Smoothing prevents abrupt visual changes that could cause discomfort.
- Cooldown timers prevent rapid oscillation between opposing actions.

### Emergency Stop
- Users can stop any session immediately via the dashboard.
- The FreezeAdaptation action halts all environmental changes.
- Runtime emergency stop and freeze controls are exposed through `/api/v1/runtime/...`
  and are recorded as auditable events when a session is active.

### Hardware Validation
- Real hardware should begin in record-only validation mode.
- Hardware closed-loop adaptation is disabled by default.
- Timestamp, channel mapping, SQI, calibration, and shadow inference should be reviewed before closed-loop use.
- EEG replay over LSL is an event-locked validation workflow. Marker labels are task annotations, not decoded mental content, and shadow inference emits no real adaptation actions.

### Overstimulation Prevention
- The behavior tree prioritizes stress reduction over engagement enhancement.
- When multiple states conflict, the system defaults to conservative actions (MaintainBaseline, SimplifyEnvironment).

## Limitations

### Inference Accuracy
- The heuristic model uses simplified weighted formulas, not validated ML models.
- Learned Phase 2 baselines are trained on dataset-derived proxy labels and should not be interpreted
  as direct measurements of cognition, emotion, intent, or clinical state.
- Learned models remain proxy estimators. Activating one should be treated as a controlled engineering experiment, not as a validated participant assessment.
- Cross-individual variation in biosignals means the same features may indicate different states for different people.
- Simulated signals do not capture the full complexity of real physiological data.

### Sensor Limitations
- The current implementation uses simulated sensors. Real hardware will introduce additional noise, artifacts, and failure modes.
- EEG signals are particularly susceptible to motion artifacts, electrode impedance changes, and environmental interference.
- Real EEG replay from a local public or fixture file validates streaming, timing, marker alignment, and reporting infrastructure. It does not clinically validate the cognitive proxy model.

### Ethical Considerations for Future Development
- Real hardware integration requires IRB approval for human subjects research.
- Adaptive environments that respond to cognitive state raise questions about autonomy and manipulation.
- Researchers should consider the power dynamics inherent in systems that infer internal mental states.

## Guidelines for Responsible Development

1. Always present cognitive state estimates as approximations, not facts.
2. Never use cognitive state data to make consequential decisions about users without their explicit consent.
3. Validate any ML models against diverse populations before deployment.
4. Include uncertainty quantification in all state estimates.
5. Provide users with full access to and control over their recorded data.
6. Document all assumptions, limitations, and failure modes.
