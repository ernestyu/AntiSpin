import hashlib
from pathlib import Path

import yaml

from src.config import build_config_report, compute_config_hash, load_config


def test_default_config_hash_stable():
    cfg = load_config("configs/default.yaml")
    h1 = compute_config_hash(cfg)
    h2 = compute_config_hash(cfg)
    assert h1 == h2
    assert h1.startswith("sha256:")


def test_hash_matches_manual_dump():
    cfg = load_config("configs/default.yaml")
    raw = yaml.safe_dump(cfg, sort_keys=True, allow_unicode=True).encode("utf-8")
    expected = "sha256:" + hashlib.sha256(raw).hexdigest()
    assert compute_config_hash(cfg) == expected


def test_config_report_contains_fingerprints(tmp_path: Path):
    cfg = load_config("configs/default.yaml")
    report = build_config_report(cfg)
    info = report["report_info"]
    assert info["config_hash"].startswith("sha256:")
    assert info["model_fingerprint"]["bi_encoder"]
    assert info["score_normalization"]["sim_clip_floor"] == cfg["alignment"]["mean_sim"]["sim_clip_floor"]
