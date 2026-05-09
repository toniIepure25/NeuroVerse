# Research Notes

## Important: Verification Required

All references, tools, and datasets listed here require independent verification before use in any publication or formal research context. This document serves as a starting point for literature review, not a validated bibliography.

## Relevant Datasets

### DEAP Dataset
- Multimodal dataset for emotion analysis using EEG, physiological signals, and video
- 32 participants, 40 music video stimuli
- Includes EEG (32 channels), EMG, EOG, GSR, temperature, respiration, blood volume
- Note: Access requires approval from the dataset authors

### SEED Dataset
- EEG-based emotion recognition dataset from SJTU
- 15 subjects, 3 sessions each, film clip stimuli
- Labels: positive, negative, neutral

### PhysioNet Motor Imagery
- EEG motor imagery dataset
- Useful for testing BCI classification pipelines
- Open access

### CLARE Dataset
- Cognitive Load and Affective Response in E-learning
- Note: Verify availability and access terms before use

## Tools and Libraries

### BrainFlow
- Uniform API for various EEG boards (OpenBCI, Muse, etc.)
- Python, C++, Java, C# bindings
- Board-agnostic data acquisition

### Lab Streaming Layer (LSL)
- Multi-device time synchronization protocol
- pylsl Python bindings
- Standard for multi-modal physiological recording

### MNE-Python
- EEG/MEG analysis toolkit
- Filtering, epoching, source localization, connectivity
- Well-documented, widely used in neuroscience

### NeuroKit2
- Physiological signal processing (ECG, EDA, EMG, EEG)
- Feature extraction and quality assessment
- Good for rapid prototyping

## Related Concepts

### Engagement Index
- Beta / (Alpha + Theta) ratio
- Pope et al. (1995) proposed this as an EEG-based engagement metric
- Widely used but not universally validated across tasks and populations

### Frontal Theta
- Theta power at frontal sites (Fz, F3, F4) associated with cognitive workload
- Gevins & Smith (2000, 2003) showed frontal theta increases with working memory load

### Alpha Suppression
- Event-related desynchronization (ERD) in alpha band during active processing
- Pfurtscheller & Lopes da Silva (1999)

### Heart Rate Variability (HRV)
- RMSSD as parasympathetic activity proxy
- Task Force of ESC and NASPE (1996) guidelines
- Lower HRV associated with stress and cognitive load

### Electrodermal Activity (EDA)
- Tonic level reflects general arousal
- Phasic responses (SCRs) reflect event-related arousal
- Boucsein (2012) "Electrodermal Activity" reference text

### Conformal Prediction
- Vovk, Gammerman, Shafer (2005) "Algorithmic Learning in a Random World"
- Distribution-free prediction intervals
- Angelopoulos & Bates (2022) "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification"

## Limitations of Current Approach

- Heuristic state estimation has not been validated against labeled data
- Simulated signals do not capture real physiological variability
- Cross-individual differences in EEG patterns are not accounted for
- The engagement index and other composite metrics are approximations
- No formal evaluation against ground truth cognitive state labels has been conducted
