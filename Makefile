.PHONY: dev backend frontend test lint build smoke docker-up docker-down docker-config demo generate-session replay-session install install-backend install-hardware-extra check-hardware-extra prepare-synthetic validate-dataset validate-synthetic-dataset train-baseline train-synthetic-baseline evaluate-synthetic-baseline replay-synthetic-dataset fusion-ablation phase2-test phase2-report research-demo phase25-test smoke-api frontend-check preflight generate-evidence-pack hardware-status validate-synthetic-hardware calibration-synthetic shadow-synthetic validate-brainflow-synthetic calibration-brainflow-synthetic shadow-brainflow-synthetic discover-brainflow-devices discover-openbci physical-eeg-trial-synthetic physical-eeg-trial-openbci-cyton physical-eeg-trial-openbci-ganglion validate-openbci-cyton calibration-openbci-cyton shadow-openbci-cyton validate-openbci-ganglion export-latest-session lsl-stream-demo discover-lsl validate-lsl-demo calibration-lsl-demo shadow-lsl-demo lsl-live-validation-suite eeg-lsl-replay-demo validate-eeg-lsl-demo calibration-eeg-lsl-demo shadow-eeg-lsl-demo eeg-lsl-live-suite inspect-eeg-fixture inspect-eeg-file prepare-eeg-fixture-events prepare-eeg-file-events train-eeg-fixture-classifier shadow-eeg-classifier-demo compare-eeg-shadow public-eeg-fixture-suite public-eeg-file-suite physionet-eegbci-info physionet-eegbci-config physionet-eegbci-download physionet-eegbci-download-medium physionet-eegbci-config-medium inspect-physionet-eegbci inspect-physionet-eegbci-medium prepare-physionet-eegbci-events train-physionet-eegbci-classifier real-public-eeg-suite real-public-eeg-file-suite bci-benchmark-small bci-benchmark-existing bci-benchmark-medium prepare-raw-epochs-small prepare-raw-epochs-medium raw-bci-benchmark-small raw-bci-benchmark-medium raw-bci-group-subject-medium raw-bci-loso-small raw-bci-loso-medium compare-bci-benchmarks compare-bci-benchmarks-medium shadow-best-raw-bci-model live-shadow-best-raw-bci-model shadow-best-bci-model physionet-mi-lsl-replay lsl-demo-full export-api-docs release-check

# Development
dev:
	@echo "Starting backend and frontend in parallel..."
	$(MAKE) backend & $(MAKE) frontend & wait

backend:
	cd backend && pip install -e ".[dev]" -q && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm install && npm run dev

install:
	cd backend && pip install -e ".[dev]"
	cd frontend && npm install

install-backend:
	cd backend && pip install -e ".[dev]"

install-hardware-extra:
	cd backend && pip install -e ".[hardware]"

check-hardware-extra:
	python3 scripts/check_hardware_extra.py

# Testing
test:
	cd backend && python3 -m pytest app/tests/ -v

lint:
	cd backend && python3 -m ruff check app/ --fix
	cd backend && python3 -m ruff format app/

build:
	cd frontend && npm run build

smoke: smoke-api frontend-check

preflight:
	python3 scripts/preflight_check.py

# Docker
docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

docker-config:
	docker compose config

# Demo
demo:
	@echo "Starting NeuroVerse demo..."
	@echo "1. Backend at http://localhost:8000"
	@echo "2. Frontend at http://localhost:5173"
	@echo "3. Start a session via the dashboard or:"
	@echo "   curl -X POST http://localhost:8000/api/session/start"
	$(MAKE) dev

generate-session:
	python3 scripts/generate_synthetic_session.py --duration 180 --output data/simulated/sample_session.csv

replay-session:
	@echo "Usage: make replay-session SESSION_ID=<session_id>"
	python3 scripts/replay_session.py --session-id $(SESSION_ID)

prepare-synthetic:
	python3 scripts/prepare_dataset.py --config configs/datasets/synthetic.yaml --target phase_label --output data/processed/synthetic_features.parquet

validate-dataset: validate-synthetic-dataset

validate-synthetic-dataset:
	python3 scripts/validate_dataset.py --dataset-config configs/datasets/synthetic.yaml --target phase_label

train-baseline: train-synthetic-baseline

train-synthetic-baseline:
	python3 scripts/train_baseline.py --dataset-config configs/datasets/synthetic.yaml --experiment-config configs/experiments/workload_baseline.yaml --model random_forest --target phase_label --output models/synthetic_phase_rf

evaluate-synthetic-baseline:
	python3 scripts/evaluate_model.py --model-dir models/synthetic_phase_rf --dataset-config configs/datasets/synthetic.yaml --target phase_label --output reports/synthetic_phase_rf_metrics.json

replay-synthetic-dataset:
	python3 scripts/replay_dataset.py --dataset-config configs/datasets/synthetic.yaml --speed 2.0 --session-id synthetic_dataset_replay

fusion-ablation:
	python3 scripts/train_baseline.py --dataset-config configs/datasets/synthetic.yaml --experiment-config configs/experiments/fusion_ablation.yaml --model random_forest --target phase_label --output models/synthetic_fusion_ablation

phase2-test:
	cd backend && python3 -m pytest app/tests/ -v

phase2-report:
	python3 scripts/generate_experiment_report.py --dataset-config configs/datasets/synthetic.yaml --model-dir models/synthetic_phase_rf --experiment-id synthetic_phase_rf

research-demo:
	@echo "Running NeuroVerse research workflow..."
	$(MAKE) prepare-synthetic
	$(MAKE) validate-synthetic-dataset
	$(MAKE) train-synthetic-baseline
	$(MAKE) evaluate-synthetic-baseline
	$(MAKE) phase2-report
	$(MAKE) replay-synthetic-dataset
	$(MAKE) generate-evidence-pack
	@echo "Start the UI with: make dev"
	@echo "Open the Research panel in the right dashboard sidebar."

phase25-test:
	cd backend && python3 -m pytest app/tests/ -v
	cd frontend && npm run lint

smoke-api:
	cd backend && python3 -c 'from app.main import create_app; app=create_app(); paths={r.path for r in app.routes if hasattr(r,"path")}; expected={"/api/runtime/status","/api/v1/runtime/status","/api/v1/runtime/latency","/api/v1/runtime/metrics","/api/v1/runtime/emergency-stop","/api/v1/runtime/freeze","/api/v1/runtime/unfreeze","/api/v1/health/deep","/api/v1/acquisition/status","/api/v1/acquisition/validation/status","/api/v1/acquisition/profiles","/api/v1/acquisition/lsl/status","/api/v1/acquisition/lsl/streams","/api/v1/acquisition/lsl/streams/{stream_id}/metadata","/api/v1/acquisition/lsl/select","/api/v1/calibration/start","/api/v1/acquisition/shadow/start","/api/v1/sessions/{session_id}/export","/api/v1/sessions/{session_id}/delete","/api/models/active","/api/models/deactivate","/api/evaluation/latest","/api/sessions/{session_id}/summary"}; missing=sorted(expected-paths); assert not missing, missing; print("API smoke ok")'

frontend-check:
	cd frontend && npm run lint

generate-evidence-pack:
	python3 scripts/generate_evidence_pack.py

export-api-docs:
	python3 scripts/export_openapi.py

release-check:
	python3 scripts/check_release_artifacts.py

hardware-status:
	@echo "GET http://localhost:8000/api/v1/acquisition/status"

validate-synthetic-hardware:
	python3 scripts/run_hardware_validation.py --adapter simulator --profile-id synthetic_multimodal --duration-seconds 2

calibration-synthetic:
	python3 scripts/run_calibration.py --duration-seconds 2

shadow-synthetic:
	python3 scripts/run_shadow_mode.py --duration-seconds 2

validate-brainflow-synthetic:
	python3 scripts/run_hardware_validation.py --adapter brainflow --profile-id brainflow_synthetic_eeg --duration-seconds 3

calibration-brainflow-synthetic:
	python3 scripts/run_calibration.py --source brainflow --profile-id brainflow_synthetic_eeg --duration-seconds 3

shadow-brainflow-synthetic:
	python3 scripts/run_shadow_mode.py --source brainflow --profile-id brainflow_synthetic_eeg --duration-seconds 3

discover-brainflow-devices:
	python3 scripts/discover_brainflow_devices.py

discover-openbci: discover-brainflow-devices

physical-eeg-trial-synthetic:
	python3 scripts/run_physical_eeg_trial.py --profile-id brainflow_synthetic_eeg --synthetic --eyes-open-seconds 5 --eyes-closed-seconds 5 --shadow-seconds 3

physical-eeg-trial-openbci-cyton:
	@test -n "$(PORT)" || (echo "Usage: make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0"; exit 2)
	python3 scripts/run_physical_eeg_trial.py --profile-id openbci_cyton_8ch --port $(PORT) --eyes-open-seconds 30 --eyes-closed-seconds 30 --shadow-seconds 30

physical-eeg-trial-openbci-ganglion:
	@test -n "$(PORT)" || (echo "Usage: make physical-eeg-trial-openbci-ganglion PORT=/dev/ttyUSB0"; exit 2)
	python3 scripts/run_physical_eeg_trial.py --profile-id openbci_ganglion_4ch --port $(PORT) --eyes-open-seconds 30 --eyes-closed-seconds 30 --shadow-seconds 30

validate-openbci-cyton:
	@test -n "$(PORT)" || (echo "Usage: make validate-openbci-cyton PORT=/dev/ttyUSB0"; exit 2)
	python3 scripts/run_hardware_validation.py --adapter brainflow --profile-id openbci_cyton_8ch --serial-port $(PORT) --duration-seconds 30

calibration-openbci-cyton:
	@test -n "$(PORT)" || (echo "Usage: make calibration-openbci-cyton PORT=/dev/ttyUSB0"; exit 2)
	python3 scripts/run_calibration.py --source brainflow --profile-id openbci_cyton_8ch --serial-port $(PORT) --duration-seconds 20

shadow-openbci-cyton:
	@test -n "$(PORT)" || (echo "Usage: make shadow-openbci-cyton PORT=/dev/ttyUSB0"; exit 2)
	python3 scripts/run_shadow_mode.py --source brainflow --profile-id openbci_cyton_8ch --serial-port $(PORT) --duration-seconds 30

validate-openbci-ganglion:
	@test -n "$(PORT)" || (echo "Usage: make validate-openbci-ganglion PORT=/dev/ttyUSB0"; exit 2)
	python3 scripts/run_hardware_validation.py --adapter brainflow --profile-id openbci_ganglion_4ch --serial-port $(PORT) --duration-seconds 30

export-latest-session:
	python3 -c 'from pathlib import Path; import sys; p=sorted(Path("data/sessions").glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True); print(p[0].stem if p else "no sessions"); sys.exit(1 if not p else 0)' | xargs -I{} python3 scripts/export_session.py --session-id {}

lsl-stream-demo:
	python3 scripts/lsl_synthetic_streamer.py --phase-markers

discover-lsl:
	python3 scripts/discover_lsl_streams.py --stream-type EEG

validate-lsl-demo:
	python3 scripts/run_lsl_validation.py --stream-name NeuroVerseSyntheticEEG --stream-type EEG --profile-id lsl_synthetic_eeg --duration-seconds 5

calibration-lsl-demo:
	python3 scripts/run_calibration.py --source lsl --stream-name NeuroVerseSyntheticEEG --stream-type EEG --profile-id lsl_synthetic_eeg --duration-seconds 5

shadow-lsl-demo:
	python3 scripts/run_shadow_mode.py --source lsl --stream-name NeuroVerseSyntheticEEG --stream-type EEG --profile-id lsl_synthetic_eeg --duration-seconds 5

lsl-live-validation-suite:
	python3 scripts/run_lsl_live_validation_suite.py --with-markers

eeg-lsl-replay-demo:
	python3 scripts/eeg_lsl_replay_streamer.py --fixture-mode --markers --stream-name NeuroVerseReplayEEG --marker-stream-name NeuroVerseReplayMarkers --duration 45

validate-eeg-lsl-demo:
	python3 scripts/run_lsl_validation.py --stream-name NeuroVerseReplayEEG --stream-type EEG --marker-stream-name NeuroVerseReplayMarkers --profile-id eeg_lsl_10_20_fixture --duration-seconds 6 --source-type eeg_lsl_replay

calibration-eeg-lsl-demo:
	python3 scripts/run_calibration.py --source eeg_lsl_replay --stream-name NeuroVerseReplayEEG --stream-type EEG --marker-stream-name NeuroVerseReplayMarkers --profile-id eeg_lsl_10_20_fixture --duration-seconds 6

shadow-eeg-lsl-demo:
	python3 scripts/run_shadow_mode.py --source eeg_lsl_replay --stream-name NeuroVerseReplayEEG --stream-type EEG --marker-stream-name NeuroVerseReplayMarkers --profile-id eeg_lsl_10_20_fixture --duration-seconds 6

eeg-lsl-live-suite:
	python3 scripts/run_eeg_lsl_validation_suite.py --fixture-mode --with-markers

inspect-eeg-fixture:
	python3 scripts/inspect_eeg_file.py --fixture-mode --output reports/eeg_file_inspection/fixture_inspection.json

inspect-eeg-file:
	@echo "Usage: make inspect-eeg-file FILE=/path/to/local.edf"
	python3 scripts/inspect_eeg_file.py --input-file $(FILE)

prepare-eeg-fixture-events:
	python3 scripts/prepare_event_locked_dataset.py --fixture-mode --output data/processed/eeg_fixture_event_features.csv

prepare-eeg-file-events:
	@echo "Usage: make prepare-eeg-file-events FILE=/path/to/local.edf"
	python3 scripts/prepare_event_locked_dataset.py --input-file $(FILE) --output data/processed/eeg_file_event_features.csv

train-eeg-fixture-classifier:
	python3 scripts/train_eeg_event_classifier.py --features data/processed/eeg_fixture_event_features.csv --model logistic_regression --output models/eeg_event_classifier_fixture

shadow-eeg-classifier-demo:
	python3 scripts/run_shadow_mode.py --source eeg_lsl_replay --stream-name NeuroVerseReplayEEG --stream-type EEG --marker-stream-name NeuroVerseReplayMarkers --profile-id eeg_lsl_10_20_fixture --duration-seconds 8 --model-id eeg_event_classifier_fixture

compare-eeg-shadow:
	@echo "Use scripts/compare_heuristic_vs_eeg_classifier.py with explicit report paths, or run make public-eeg-fixture-suite."

public-eeg-fixture-suite:
	python3 scripts/run_public_eeg_validation_suite.py --fixture-mode

public-eeg-file-suite:
	@echo "Usage: make public-eeg-file-suite FILE=/path/to/local.edf"
	python3 scripts/run_public_eeg_validation_suite.py --input-file $(FILE)

physionet-eegbci-info:
	python3 scripts/prepare_physionet_eegbci.py --info

physionet-eegbci-config:
	python3 scripts/prepare_physionet_eegbci.py --local-root $(or $(LOCAL_ROOT),data/external/eegbci) --subjects $(or $(SUBJECTS),1 2 3) --runs $(or $(RUNS),4 8 12) --output-config configs/datasets/physionet_eegbci_local.yaml

physionet-eegbci-download:
	python3 scripts/prepare_physionet_eegbci.py --download --local-root $(or $(LOCAL_ROOT),data/external/eegbci) --subjects $(or $(SUBJECTS),1 2 3) --runs $(or $(RUNS),4 8 12) --output-config configs/datasets/physionet_eegbci_local.yaml

physionet-eegbci-config-medium:
	python3 scripts/prepare_physionet_eegbci.py --local-root $(or $(LOCAL_ROOT),data/external/eegbci) --subjects 1 2 3 4 5 6 7 8 9 10 --runs 4 8 12 --output-config configs/datasets/physionet_eegbci_local.yaml

physionet-eegbci-download-medium:
	python3 scripts/prepare_physionet_eegbci.py --download --local-root $(or $(LOCAL_ROOT),data/external/eegbci) --subjects 1 2 3 4 5 6 7 8 9 10 --runs 4 8 12 --output-config configs/datasets/physionet_eegbci_local.yaml

inspect-physionet-eegbci:
	python3 scripts/inspect_eeg_dataset.py --dataset-config configs/datasets/physionet_eegbci_local.yaml --output reports/public_eeg_inspection/physionet_eegbci_inspection.json

inspect-physionet-eegbci-medium:
	python3 scripts/inspect_eeg_dataset.py --dataset-config configs/datasets/physionet_eegbci_local.yaml --output reports/public_eeg_inspection/physionet_eegbci_medium_inspection.json

prepare-physionet-eegbci-events:
	python3 scripts/prepare_event_locked_dataset.py --dataset-config configs/datasets/physionet_eegbci_local.yaml --output data/processed/physionet_eegbci_event_features.csv --tmin 0.0 --tmax 2.0

prepare-physionet-eegbci-events-mi:
	python3 scripts/prepare_event_locked_dataset.py --dataset-config configs/datasets/physionet_eegbci_local.yaml --output data/processed/physionet_eegbci_event_features_mi.csv --tmin 0.5 --tmax 2.5 --bandpass-low 7 --bandpass-high 35 --baseline-correction --feature-set combined

train-physionet-eegbci-classifier:
	python3 scripts/train_eeg_event_classifier.py --features data/processed/physionet_eegbci_event_features.csv --model logistic_regression --split group_run --output models/physionet_eegbci_event_lr

real-public-eeg-suite:
	python3 scripts/run_real_public_eeg_validation_suite.py --dataset-config $(or $(DATASET_CONFIG),configs/datasets/physionet_eegbci_local.yaml)

real-public-eeg-file-suite:
	@echo "Usage: make real-public-eeg-file-suite FILE=/path/to/local.edf"
	python3 scripts/run_real_public_eeg_validation_suite.py --input-file $(FILE)

bci-benchmark-small:
	python3 scripts/run_bci_benchmark.py --features data/processed/physionet_eegbci_event_features.csv --dataset-config configs/datasets/physionet_eegbci_local.yaml --models logistic_regression ridge_classifier random_forest hist_gradient_boosting svm_linear csp_lda csp_logreg --split group_run --output reports/bci_benchmark/physionet_eegbci_small

bci-benchmark-existing:
	python3 scripts/run_bci_benchmark.py --features $(or $(FEATURES),data/processed/physionet_eegbci_event_features.csv) --dataset-config $(or $(DATASET_CONFIG),configs/datasets/physionet_eegbci_local.yaml) --models logistic_regression ridge_classifier random_forest hist_gradient_boosting svm_linear --split $(or $(SPLIT),group_run) --output $(or $(OUTPUT),reports/bci_benchmark/custom_existing)

bci-benchmark-medium:
	@echo "Download explicitly first if needed: make physionet-eegbci-download SUBJECTS=\"1 2 3 4 5 6 7 8 9 10\" RUNS=\"4 8 12\""
	python3 scripts/run_bci_benchmark.py --features data/processed/physionet_eegbci_event_features.csv --dataset-config configs/datasets/physionet_eegbci_local.yaml --models logistic_regression ridge_classifier random_forest hist_gradient_boosting svm_linear --split group_run --output reports/bci_benchmark/physionet_eegbci_medium

shadow-best-bci-model:
	@echo "Best benchmark models are registered for shadow-only review. Re-run the real-public suite to generate LSL shadow reports with the current classifier path."

prepare-raw-epochs-small:
	python3 scripts/prepare_raw_epoch_dataset.py --dataset-config configs/datasets/physionet_eegbci_local.yaml --subjects 1 2 3 --runs 4 8 12 --labels LEFT_HAND_IMAGERY RIGHT_HAND_IMAGERY --exclude-rest --tmin 0.5 --tmax 2.5 --bandpass-low 7 --bandpass-high 35 --output data/processed/physionet_eegbci_raw_epochs_small.npz

prepare-raw-epochs-medium:
	@echo "Download/configure explicitly first if needed: make physionet-eegbci-download SUBJECTS=\"1 2 3 4 5 6 7 8 9 10\" RUNS=\"4 8 12\""
	python3 scripts/prepare_raw_epoch_dataset.py --dataset-config configs/datasets/physionet_eegbci_local.yaml --subjects 1 2 3 4 5 6 7 8 9 10 --runs 4 8 12 --labels LEFT_HAND_IMAGERY RIGHT_HAND_IMAGERY --exclude-rest --tmin 0.5 --tmax 2.5 --bandpass-low 7 --bandpass-high 35 --output data/processed/physionet_eegbci_raw_epochs_medium.npz

raw-bci-benchmark-small:
	python3 scripts/run_raw_epoch_bci_benchmark.py --epochs data/processed/physionet_eegbci_raw_epochs_small.npz --models csp_lda csp_logreg csp_svm_linear fbcsp_logreg fbcsp_lda --split group_run --output reports/bci_raw_epoch_benchmark/physionet_eegbci_small

raw-bci-benchmark-medium:
	@test -f data/processed/physionet_eegbci_raw_epochs_medium.npz || (echo "Missing medium raw epochs. Run make physionet-eegbci-download-medium, make physionet-eegbci-config-medium, then make prepare-raw-epochs-medium."; exit 1)
	python3 scripts/run_raw_epoch_bci_benchmark.py --epochs data/processed/physionet_eegbci_raw_epochs_medium.npz --models csp_lda csp_logreg csp_svm_linear fbcsp_logreg fbcsp_lda --split group_run --output reports/bci_raw_epoch_benchmark/physionet_eegbci_medium

raw-bci-group-subject-medium:
	@test -f data/processed/physionet_eegbci_raw_epochs_medium.npz || (echo "Missing medium raw epochs. Run make physionet-eegbci-download-medium, make physionet-eegbci-config-medium, then make prepare-raw-epochs-medium."; exit 1)
	python3 scripts/run_raw_epoch_bci_benchmark.py --epochs data/processed/physionet_eegbci_raw_epochs_medium.npz --models csp_lda csp_logreg fbcsp_logreg --split group_subject --output reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_group_subject

raw-bci-loso-small:
	python3 scripts/run_raw_epoch_bci_benchmark.py --epochs data/processed/physionet_eegbci_raw_epochs_small.npz --models csp_lda csp_logreg --split leave_one_subject_out --output reports/bci_raw_epoch_benchmark/physionet_eegbci_small_loso

raw-bci-loso-medium:
	@test -f data/processed/physionet_eegbci_raw_epochs_medium.npz || (echo "Missing medium raw epochs. Run make physionet-eegbci-download-medium, make physionet-eegbci-config-medium, then make prepare-raw-epochs-medium."; exit 1)
	python3 scripts/run_raw_epoch_bci_benchmark.py --epochs data/processed/physionet_eegbci_raw_epochs_medium.npz --models csp_lda csp_logreg fbcsp_logreg --split leave_one_subject_out --output reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_loso

compare-bci-benchmarks:
	python3 scripts/compare_bci_benchmarks.py --flattened reports/bci_benchmark/physionet_eegbci_small --raw reports/bci_raw_epoch_benchmark/physionet_eegbci_small --output reports/bci_benchmark_comparison/physionet_eegbci_small

compare-bci-benchmarks-medium:
	python3 scripts/compare_bci_benchmarks.py --flattened reports/bci_benchmark/physionet_eegbci_small --raw reports/bci_raw_epoch_benchmark/physionet_eegbci_small --medium-group-run reports/bci_raw_epoch_benchmark/physionet_eegbci_medium --medium-group-subject reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_group_subject --medium-loso reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_loso --live-shadow $(or $(LIVE_SHADOW),reports/raw_bci_shadow/latest) --output reports/bci_benchmark_comparison/physionet_eegbci_medium

shadow-best-raw-bci-model:
	python3 scripts/run_best_raw_bci_shadow.py --best-model reports/bci_raw_epoch_benchmark/physionet_eegbci_small/best_model.json --epochs data/processed/physionet_eegbci_raw_epochs_small.npz --output reports/raw_bci_shadow/physionet_eegbci_small_shadow.json

live-shadow-best-raw-bci-model:
	python3 scripts/run_live_raw_bci_shadow.py --best-model $(or $(BEST_MODEL),reports/bci_raw_epoch_benchmark/physionet_eegbci_small/best_model.json) --epochs $(or $(EPOCHS),data/processed/physionet_eegbci_raw_epochs_small.npz) --output-dir reports/raw_bci_shadow

physionet-mi-lsl-replay:
	@echo "Usage: make physionet-mi-lsl-replay FILE=/path/to/local.edf"
	python3 scripts/eeg_lsl_replay_streamer.py --input-file $(FILE) --stream-name NeuroVerseReplayEEG --marker-stream-name NeuroVerseReplayMarkers --markers

lsl-demo-full:
	@echo "Terminal 1: make lsl-stream-demo"
	@echo "Terminal 2: make discover-lsl validate-lsl-demo calibration-lsl-demo shadow-lsl-demo generate-evidence-pack"
	@echo "One-shot local suite when pylsl is installed: make lsl-live-validation-suite"
	@echo "EEG replay fixture suite: make eeg-lsl-live-suite"
