# Multimodal Fusion / IMAGINA Proxy Report

Run ID: `20260601T195655_ad319402`
Generated: `2026-06-01T19:56:56.767261+00:00`

> Multimodal fusion outputs are experimental proxy estimates, not clinical or unrestricted mental-state measurements.
> The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.
> Closed-loop from real EEG is disabled by default.
> IMAGINA plugin outputs are experimental imagery-quality proxies, not decoded thoughts or dreams.

## Fusion Output

- Focus proxy: `0.621`
- Relaxation proxy: `0.554`
- Workload proxy: `0.456`
- Stress/arousal proxy: `0.426`
- Fatigue proxy: `0.381`
- Imagery engagement proxy: `0.556`
- Imagery quality proxy: `0.48798499999999995`
- Confidence: `0.720`
- Uncertainty: `0.280`
- Safety recommendation: `allow_shadow`

## Modalities
- `eeg`: present
- `gaze`: present
- `physiology`: present
- `behavior`: present
- `self_report`: present

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
  "mode": "simulated",
  "intensity_cap": 0.72,
  "parameters": {
    "clarity": 0.446817276,
    "fog_reduction": 0.2457495018,
    "motion_smoothness": 0.39889378799999997,
    "breathing_pulse": 0.17950220460000002,
    "scene_simplification": 0.30636216,
    "guidance_cue": 0.274632264,
    "symbolic_object_glow": 0.3513492,
    "freeze_adaptation": false
  },
  "limitations": [
    "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
    "Closed-loop from real EEG is disabled by default."
  ]
}
```
