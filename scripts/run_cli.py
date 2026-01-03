"""Minimal entrypoint for stage 0: load config and write a config-hash JSON."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import build_config_report, load_config, save_report
from src.utils.io import ensure_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="AntiSpin stage0 config check.")
    parser.add_argument(
        "--config",
        default="configs/default.yaml",
        help="Path to YAML config.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output JSON path. Defaults to <paths.json_dir>/config_check.json.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    report = build_config_report(config)

    default_json_dir = Path(config.get("paths", {}).get("json_dir", "workspace/outputs/json"))
    output_path = Path(args.output) if args.output else default_json_dir / "config_check.json"
    ensure_dir(output_path.parent)

    save_report(report, output_path)
    print(f"config_hash: {report['report_info']['config_hash']}")
    print(f"report written to: {output_path}")


if __name__ == "__main__":
    main()
