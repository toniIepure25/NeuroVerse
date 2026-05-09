"""Local NeuroVerse preflight checks."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    checks = {
        "python_version": {
            "ok": sys.version_info >= (3, 10),
            "value": ".".join(map(str, sys.version_info[:3])),
        },
        "node_available": {"ok": shutil.which("node") is not None},
        "npm_available": {"ok": shutil.which("npm") is not None},
        "backend_package": {"ok": (ROOT / "backend" / "pyproject.toml").exists()},
        "frontend_package": {"ok": (ROOT / "frontend" / "package.json").exists()},
        "sessions_writable": {"ok": _is_writable(ROOT / "backend" / "data" / "sessions")},
        "reports_writable": {"ok": _is_writable(ROOT / "reports")},
        "models_dir": {"ok": (ROOT / "models").exists()},
        "synthetic_dataset_config": {
            "ok": (ROOT / "configs" / "datasets" / "synthetic.yaml").exists()
        },
        "optional_brainflow": {"ok": importlib.util.find_spec("brainflow") is not None},
        "optional_pylsl": {"ok": importlib.util.find_spec("pylsl") is not None},
        "optional_pyxdf": {"ok": importlib.util.find_spec("pyxdf") is not None},
        "optional_mne": {"ok": importlib.util.find_spec("mne") is not None},
    }
    print(json.dumps(checks, indent=2))
    required = [
        "python_version",
        "node_available",
        "npm_available",
        "backend_package",
        "frontend_package",
        "sessions_writable",
        "reports_writable",
        "synthetic_dataset_config",
    ]
    failed = [name for name in required if not checks[name]["ok"]]
    if failed:
        raise SystemExit(f"Preflight failed: {', '.join(failed)}")


def _is_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".neuroverse_preflight"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    main()
