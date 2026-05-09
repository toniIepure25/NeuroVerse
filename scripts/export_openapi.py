import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

try:
    from app.main import create_app
    app = create_app()
    openapi_schema = app.openapi()
except Exception as e:
    print(f"Failed to export OpenAPI due to runtime state missing: {e}")
    openapi_schema = None

docs_dir = ROOT / "docs"
docs_dir.mkdir(parents=True, exist_ok=True)

if openapi_schema:
    with open(docs_dir / "openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)

    md_lines = ["# NeuroVerse API Reference\n"]
    md_lines.append("This document summarizes the available REST and WebSocket endpoints.\n")
    
    paths = openapi_schema.get("paths", {})
    
    grouped = {}
    for path, methods in paths.items():
        if path.startswith("/api/v1/health") or path.startswith("/api/v1/runtime"):
            group = "Health & Runtime"
        elif path.startswith("/api/v1/sessions"):
            group = "Sessions"
        elif path.startswith("/api/v1/replay"):
            group = "Replay"
        elif path.startswith("/api/v1/acquisition"):
            group = "Acquisition"
        elif path.startswith("/api/v1/calibration"):
            group = "Calibration"
        elif path.startswith("/api/v1/hardware-trials"):
            group = "Hardware Trials"
        elif path.startswith("/api/v1/shadow"):
            group = "Shadow Mode"
        elif path.startswith("/api/evaluation") or path.startswith("/api/models") or path.startswith("/api/datasets"):
            group = "Models & Evaluation"
        else:
            group = "Other"
            
        if group not in grouped:
            grouped[group] = []
        
        for method, info in methods.items():
            grouped[group].append({
                "method": method.upper(),
                "path": path,
                "summary": info.get("summary", ""),
                "description": info.get("description", "")
            })
            
    for group, routes in sorted(grouped.items()):
        md_lines.append(f"## {group}\n")
        for r in routes:
            md_lines.append(f"### `{r['method']} {r['path']}`")
            md_lines.append(f"**Purpose**: {r['summary']}")
            if r['description']:
                md_lines.append(f"**Details**: {r['description']}")
            md_lines.append("\n---\n")

    with open(docs_dir / "API_REFERENCE.md", "w") as f:
        f.write("\n".join(md_lines))
        
    print("API docs exported successfully.")
else:
    print("OpenAPI export failed, generating partial API Reference.")
    md_lines = ["# NeuroVerse API Reference\n"]
    md_lines.append("Partial export due to missing runtime context. Please run `make dev` and view `http://localhost:8000/docs`.")
    with open(docs_dir / "API_REFERENCE.md", "w") as f:
        f.write("\n".join(md_lines))
