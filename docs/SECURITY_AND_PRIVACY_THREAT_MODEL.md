# Security and Privacy Threat Model

This document outlines the security architecture, privacy postures, risk assessments, and secure deployment guidelines for the **NeuroVerse** research platform runtime. It serves as an audit-grade reference for engineering reviewers and security coordinators.

---

## 1. Executive Summary & Security Philosophy

NeuroVerse handles multi-channel electroencephalography (EEG) and synthesized multimodal cognitive state indicators. Because neural and physiological data represents highly sensitive personal information, NeuroVerse implements a strict **local-first, sandboxed-by-default, and zero-trust-network** architectural philosophy.

```
+-----------------------------------------------------------------------------------+
|                              NEUROVERSE SECURITY BOUNDS                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Live Hardware / Replay ] ---> [ Local Async Ingestion Loop (FastAPI) ]          |
|                                                  |                                |
|                                   (Local WebSocket Port 8000)                     |
|                                                  |                                |
|                                                  v                                |
|  [ Zero Internet Access ] <--- [ Local Visual Interface (Vite / React) ]          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Risk Matrix & Threat Assessments

| Threat Area | Risk Level | Mitigation Strategy | Status |
|---|---|---|---|
| **Neural Data Leakage (Network)** | High | **Zero Cloud Transmission**: All raw streaming buffers, event tags, and feature metrics are computed strictly locally. No telemetry or telemetry-adjacent packages exist. | **Enforced** |
| **Unauthorized Adaptive Commands** | Medium | **Safety Lock Invariance**: The real-time visual adaptation loop is locked by default to a shadow-inference mode (`closed_loop_allowed: false`), preventing unsafe visual/sensory feedback adjustments from noisy raw sources. | **Enforced** |
| **Path Traversal / External Imports** | Low | **Path Boundaries**: Ingestion pipelines scanning external directories (e.g. `../Imagina`) restrict target file reads to verified JSON/CSV schema configurations using strict root constraints. | **Enforced** |
| **Prototype API Exposure** | Medium | **LAN-Only Listening**: The default launch parameters bind Uvicorn to localhost `127.0.0.1:8000`, blocking raw incoming sockets from adjacent machines. | **Enforced** |
| **Unauthenticated Controls** | Medium | **Zero Remote Command Scope**: Since the research prototype does not implement credentials or OAuth, it must never be exposed to public networks with the API server enabled. | **Documented** |

---

## 3. Threat Vector Analysis & Hardening Detail

### 3.1 Neural Data Privacy & Local Boundaries
* **Threat Vector**: Interception of raw neurophysiological potentials (e.g., LSL streams or local dataset files) via network sniffers or telemetry reporting.
* **Hardening Implementation**: 
  - Raw EEG data remains entirely inside memory bounds within the local Python process. 
  - Inter-process communication utilizes local Lab Streaming Layer (LSL) or local secure loopback WebSockets. 
  - There are no default API configurations that send neural traces to third-party endpoints or remote LLM processors.

### 3.2 External IMAGINA Artifact Import Safety
* **Threat Vector**: Ingestion of malicious, corrupted, or crafted configuration files from external research folders (e.g., `../Imagina`) that attempt to hijack python standard runtime or cause buffer overflows.
* **Hardening Implementation**:
  - The Imagina export contract specifies explicit, schema-validated JSON keys (`version`, `imagery_metrics`, `closed_loop_allowed`).
  - Python's `json.load()` parsing strictly enforces schema validation and isolates key inputs.
  - Path resolution strictly maps imports relative to the defined absolute path of `Imagina` or the local NeuroVerse sandbox, avoiding directory traversal (`../../etc/passwd`).

### 3.3 Static Evidence Redaction & Recruiter Safety
* **Threat Vector**: Inadvertently exposing actual human subjects' raw biological records or personal identifiers inside baked evidence packs or static portfolios.
* **Hardening Implementation**:
  - All public benchmarks utilize strictly anonymized public open-access datasets (e.g. PhysioNet motor imagery S001-S010).
  - Continuous QA verification scripts (e.g. `check_static_portfolio.py`) inspect baked files prior to build and assert that no personal records or un-redacted session metadata has been published.
  - The static output uniformly asserts `"closed_loop_allowed": false`.

---

## 4. Secure Deployment Postures

Depending on the presentation environment, follow one of the three recommended security postures:

```
                  +----------------------------------------------+
                  |         Select Presentation Mode             |
                  +----------------------------------------------+
                                  |
            +---------------------+---------------------+
            |                     |                     |
            v                     v                     v
+-----------------------+ +-----------------------+ +-----------------------+
|   Local Interactive   | |  Private Local LAN    | |  Public Static Demo   |
|   (Developer / Recruiter) | (Technical Lab Reviews) | (GitHub Pages / S3)  |
|                       | |                       | |                       |
| - Bind to 127.0.0.1   | | - Bind to 0.0.0.0     | | - Static Build Only   |
| - Safe default state  | | - Strict local router | | - No live FastAPI     |
| - Local memory sandb. | | - Single-session lock | | - Zero runtime API    |
+-----------------------+ +-----------------------+ +-----------------------+
```

### Posture A: Local Interactive Walkthrough (Recommended for 1-on-1 Interviews)
* **Configuration**: `make dev`
* **Target Interface**: `127.0.0.1:8000` (FastAPI) and `127.0.0.1:5173` (Vite UI).
* **Security Benefits**: Loopback interfaces prevent external network access, fully isolating both raw signals and control outputs within local memory space.

### Posture B: Private Lab Demonstration (Internal Network Only)
* **Configuration**: Bind Uvicorn to `0.0.0.0` on a secure local WiFi router.
* **Target Interface**: Private internal IP (e.g. `192.168.1.50`).
* **Security Cautions**: Never expose this configuration directly to the wide public internet. Enable host-based firewalls to restrict inbound connections to presentation client devices only.

### Posture C: Serverless Public Portfolio (Recruiter & Github Pages Deployment)
* **Configuration**: `make static-portfolio-build`
* **Target Interface**: Static HTML hosting (Vercel, Netlify, Github Pages, AWS S3).
* **Security Benefits**: Completely eliminates the live Python backend runtime process. The dashboard loads statically baked JSON templates where `"closed_loop_allowed": false` is hardcoded. There are zero live network ports, zero remote commands, and zero remote injection surfaces.

---

## 5. System Limitations & Non-Claims

NeuroVerse is an **exploratory research-grade runtime** and does not claim:
1. **Clinical-Grade Ingress Protection**: It is not compliant with medical device data security standards (e.g., HIPAA, IEC 62304) and should not be used in clinical trials.
2. **Multi-User Cryptographic Authentication**: There are no default database credential vaults or active user authentication managers inside the local FastAPI loop.
3. **Defense Against Local Administrators**: Since all scripts execute within the user space, users with local root access can modify configuration keys or bypass the safety loop overrides manually. The safety gate acts as a software engineering process control, not a cryptographic boundary against local developers.
