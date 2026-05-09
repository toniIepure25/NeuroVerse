# Deployment Readiness

NeuroVerse is engineered as a local-first research platform. Because it handles high-frequency data streams and relies on local hardware bindings, cloud deployment comes with strict limitations.

## 1. Local Development (Recommended)

The standard way to run the platform is entirely on your local machine.

```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Or simply:
make dev
```
**Capabilities**: Full access to LSL streams, BrainFlow C++ bindings, offline dataset benchmarks, and physical hardware ports (Bluetooth/USB).

## 2. Docker Compose (Local/Edge Deployment)

A `docker-compose.yml` is provided for containerized deployment, typically useful for edge devices or local servers.

```bash
docker compose up --build
```
**Capabilities**: Fast reproducible environment. 
**Caveats**: 
- BrainFlow and LSL require host network access to discover streams. The `docker-compose.yml` configures `network_mode: "host"` to enable this.
- Access to physical USB/Bluetooth dongles requires explicit device mounting (`--device=/dev/ttyUSB0` or similar).

## 3. Frontend-Only Static Deploy (Public Portfolio)

For portfolio visibility, the React frontend can be built and deployed statically to Vercel, Netlify, or GitHub Pages.

```bash
cd frontend
npm run build
```

**Capabilities**: Recruiters and reviewers can view the Landing Page, Evidence Center, and Hiring Page UI.
**Caveats**: The `ResearchPanel` and `DreamCorridor` will fail to connect to the WebSocket backend (`ws://localhost:8000`). The UI will correctly display a disconnected status and fall back to static evidence. This is expected and safe for public portfolios.

## 4. Backend Cloud Deployment Limitations

Deploying the FastAPI backend to a cloud provider (e.g., AWS, Render, Heroku) is **not recommended** unless purely running synthetic data or replaying EDF datasets.

Why?
- **LSL (Lab Streaming Layer)** discovers streams via local UDP broadcasts. It cannot easily bridge from a local desktop running an EEG headset to a cloud server over the open internet without an explicit proxy relay.
- **Latency**: Closed-loop BCI systems require sub-100ms latency. Cloud round-trips defeat the purpose of real-time adaptation.
- **Privacy**: Streaming raw, unencrypted neural data to a cloud server violates standard research ethics without explicit IRB approval and end-to-end encryption.

## 5. Environment Variables

The system relies on minimal environment variables, mostly for overrides:

- `LSL_POLL_RATE`: Defaults to `100` (Hz). Adjust based on system capacity.
- `NEUROVERSE_DEBUG_MODE`: Enables detailed epoch logging.
- `PHYSICAL_OVERRIDE`: A strict boolean. Must be set to `True` for the Safety Gate to allow real hardware adaptation. Defaults to `False`.

## 6. What Can Be Shown Publicly

You can publicly host:
- The React frontend (with broken WS connection).
- The `reports/` JSON and MD files.
- The `evidence_pack/` inventory.
- Pre-recorded demo videos of the local system.

To run physical hardware (OpenBCI), you must clone the repo locally and execute `make dev`.
