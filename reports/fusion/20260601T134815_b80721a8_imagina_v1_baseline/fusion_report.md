# Multimodal Fusion / IMAGINA Proxy Report

Run ID: `20260601T134815_b80721a8_imagina_v1_baseline`
Generated: `2026-06-01T13:48:15.954039+00:00`

> Multimodal fusion outputs are experimental proxy estimates, not clinical or unrestricted mental-state measurements.
> The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.
> Closed-loop from real EEG is disabled by default.
> IMAGINA plugin outputs are experimental imagery-quality proxies, not decoded thoughts or dreams.

## Fusion Output

- Focus proxy: `0.594`
- Relaxation proxy: `0.530`
- Workload proxy: `0.481`
- Stress/arousal proxy: `0.469`
- Fatigue proxy: `0.374`
- Imagery engagement proxy: `0.506`
- Imagery quality proxy: `0.430985`
- Confidence: `0.400`
- Uncertainty: `0.600`
- Safety recommendation: `wait`

## Modalities
- `eeg`: present

## Proposed Dream Corridor Mapping

This mapping is proposed for simulated/shadow display only and does not execute real adaptation.

```json
{
  "mapping_mode": "proposed_shadow_only",
  "executed_real_action": false,
  "closed_loop_allowed": false,
  "usable_in_modes": [
    "simulated",
    "demo",
    "shadow"
  ],
  "blocked_for_real_eeg_closed_loop": true,
  "mode": "replay",
  "intensity_cap": 0.3999999999999999,
  "parameters": {
    "clarity": 0.23779299999999995,
    "fog_reduction": 0.13078615,
    "motion_smoothness": 0.21187779999999998,
    "breathing_pulse": 0.09534501,
    "scene_simplification": 0.18758229999999995,
    "guidance_cue": 0.14978929999999996,
    "symbolic_object_glow": 0.17239399999999996,
    "freeze_adaptation": false
  },
  "limitations": [
    "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
    "Closed-loop from real EEG is disabled by default."
  ]
}
```
