"""Configuration loader and config-hash helpers for AntiSpin."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.utils.hashing import load_yaml, stable_hash
from src.utils.io import save_json


def load_config(path: str | Path = "configs/default.yaml") -> Dict[str, Any]:
    """Load project config from YAML."""
    return load_yaml(path)


def compute_config_hash(config: Dict[str, Any]) -> str:
    """Compute a stable config hash for provenance tracking."""
    return stable_hash(config)


def build_config_report(config: Dict[str, Any]) -> Dict[str, Any]:
    """Build a minimal JSON payload that records config fingerprint."""
    config_hash = compute_config_hash(config)

    models = config.get("models", {})
    reranker = models.get("reranker", {})
    preprocess = config.get("preprocess", {})
    alignment = config.get("alignment", {})

    score_norm_mode = reranker.get("score_normalization", "sigmoid")
    score_normalization = {
        "rerank_score": "sigmoid(logit)" if score_norm_mode == "sigmoid" else "none",
        "tau_mapping": "(tau+1)/2",
        "sim_clip_floor": alignment.get("mean_sim", {}).get("sim_clip_floor", 0.70),
    }

    model_fingerprint = {
        "bi_encoder": models.get("bi_encoder", {}).get("name", ""),
        "reranker": reranker.get("name", ""),
        "token_explain_model": models.get("token_explain_model", {}).get("name", ""),
    }

    preprocess_fingerprint = {
        "seg_strategy": preprocess.get("segmentation", {}).get("method", ""),
        "public_domain_filter": bool(config.get("public_domain_filter", {}).get("enabled", False)),
        "stopword_removed": bool(preprocess.get("stopword_removed", False)),
    }

    return {
        "report_info": {
            "schema_version": str(config.get("schema_version", "1.0")),
            "config_hash": config_hash,
            "score_normalization": score_normalization,
            "model_fingerprint": model_fingerprint,
            "preprocess_fingerprint": preprocess_fingerprint,
        }
    }


def save_report(report: Dict[str, Any], path: str | Path) -> Path:
    """Persist a report JSON to disk."""
    return save_json(report, path)

