"""External client for Imagina integration discovery."""

from __future__ import annotations

import os
from pathlib import Path

from app.integrations.imagina.contract import ExternalImaginaStatus


def resolve_external_imagina_root(project_root: str | None = None) -> Path:
    """Resolve the absolute path to the external Imagina project root."""
    root_str = project_root or os.environ.get("NEUROVERSE_IMAGINA_ROOT", "../Imagina")
    path = Path(root_str)
    if not path.is_absolute():
        # Resolve relative to the NeuroVerse repository root
        # app/integrations/imagina/external_client.py -> parents[4] is NeuroVerse/
        repo_root = Path(__file__).resolve().parents[4]
        path = (repo_root / root_str).resolve()
    return path


def detect_external_imagina_project(project_root: str | None = None) -> ExternalImaginaStatus:
    """Scan and verify the presence of the external Imagina project."""
    target_path = resolve_external_imagina_root(project_root)
    exists = target_path.exists() and target_path.is_dir()

    if not exists:
        return ExternalImaginaStatus(
            project_root=str(target_path),
            exists=False,
            integration_ready=False,
            warnings=[f"External Imagina project not found at resolved path: {target_path}"],
        )

    # Check for signature files and directories
    sigs = ["README.md", "backend", "frontend", "research", "scripts"]
    warnings = []
    available_artifacts = []

    for sig in sigs:
        sig_path = target_path / sig
        if not sig_path.exists():
            warnings.append(f"Missing signature directory/file: {sig}")
        else:
            available_artifacts.append(sig)

    # Detect version from README or pyproject.toml if present
    detected_version = "1.0"
    pyproject = target_path / "backend" / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            for line in content.splitlines():
                if "version =" in line or "version=" in line:
                    detected_version = line.split("=")[-1].strip().strip('"').strip("'")
                    break
        except Exception:
            pass

    integration_ready = len(warnings) == 0

    return ExternalImaginaStatus(
        project_root=str(target_path),
        exists=True,
        detected_version=detected_version,
        available_artifacts=available_artifacts,
        integration_ready=integration_ready,
        warnings=warnings,
    )
