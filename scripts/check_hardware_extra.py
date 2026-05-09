"""Report optional NeuroVerse hardware dependency availability."""

from __future__ import annotations

import importlib.util
import json

INSTALL_HINT = 'cd backend && pip install -e ".[hardware]"'


def main() -> None:
    status = {
        "pylsl": _available("pylsl"),
        "brainflow": _available("brainflow"),
        "pyxdf": _available("pyxdf"),
        "mne": _available("mne"),
        "install_hint": INSTALL_HINT,
        "hardware_closed_loop_default": "disabled",
    }
    print(json.dumps(status, indent=2))


def _available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


if __name__ == "__main__":
    main()
