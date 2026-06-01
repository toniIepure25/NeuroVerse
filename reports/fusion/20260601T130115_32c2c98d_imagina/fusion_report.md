# Multimodal Fusion / IMAGINA Proxy Report

Run ID: `20260601T130115_32c2c98d_imagina`
Generated: `2026-06-01T13:01:15.185879+00:00`

> Multimodal fusion outputs are experimental proxy estimates, not clinical or unrestricted mental-state measurements.
> The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.
> Closed-loop from real EEG is disabled by default.
> IMAGINA plugin outputs are experimental imagery-quality proxies, not decoded thoughts or dreams.

## Fusion Output

- Focus proxy: `0.571`
- Relaxation proxy: `0.530`
- Workload proxy: `0.491`
- Stress/arousal proxy: `0.474`
- Fatigue proxy: `0.406`
- Imagery engagement proxy: `0.669`
- Imagery quality proxy: `0.596077848`
- Confidence: `0.480`
- Uncertainty: `0.520`
- Safety recommendation: `wait`

## Modalities
- `eeg`: present
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
  "mode": "replay",
  "intensity_cap": 0.48,
  "parameters": {
    "clarity": 0.274172928,
    "fog_reduction": 0.15079511040000002,
    "motion_smoothness": 0.25437696000000004,
    "breathing_pulse": 0.11446963200000002,
    "scene_simplification": 0.227724288,
    "guidance_cue": 0.19487846400000003,
    "symbolic_object_glow": 0.28611736703999996,
    "freeze_adaptation": false
  },
  "limitations": [
    "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
    "Closed-loop from real EEG is disabled by default."
  ]
}
```
