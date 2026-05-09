"""Discover serial devices that may be usable with BrainFlow/OpenBCI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.acquisition.brainflow_adapter import discover_brainflow_devices


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover local BrainFlow/OpenBCI serial devices")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    report = discover_brainflow_devices()
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print("BrainFlow/OpenBCI device discovery")
    print(f"pyserial available: {report['pyserial_available']}")
    if report["devices"]:
        for device in report["devices"]:
            marker = "likely OpenBCI" if device.get("likely_openbci") else "serial device"
            print(f"- {device['device']} ({marker})")
            if device.get("description"):
                print(f"  description: {device['description']}")
            if device.get("manufacturer"):
                print(f"  manufacturer: {device['manufacturer']}")
            if device.get("vid") or device.get("pid"):
                print(f"  vid/pid: {device.get('vid') or '—'}:{device.get('pid') or '—'}")
    else:
        print("- no serial devices detected")
    for warning in report.get("warnings", []):
        print(f"warning: {warning}")
    print("Next commands:")
    for label, command in report.get("next_commands", {}).items():
        print(f"- {label}: {command}")


if __name__ == "__main__":
    main()
