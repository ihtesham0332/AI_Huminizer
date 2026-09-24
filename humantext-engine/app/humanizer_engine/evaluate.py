"""Evaluation harness: run the engine over a golden set and print regression metrics.

    python -m humanizer_engine.evaluate eval_data/golden.jsonl --level 3
Each line: {"text": "..."}. Gate thresholds make this usable in CI.
"""
from __future__ import annotations
import argparse, json, os, sys
from statistics import mean

from .pipeline import HumanizerEngine
from .providers import AnthropicProvider, MockProvider


def run(path: str, level: int, provider) -> dict:
    eng = HumanizerEngine(provider)
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    agg = {"docs": 0, "entity_loss": 0, "fallback_rate": [], "fidelity": [], "before": [], "after": []}
    for r in rows:
        res = eng.humanize_sync(r["text"], level=level)
        rep = res.report
        agg["docs"] += 1
        agg["entity_loss"] += len(rep["entities_lost"])
        agg["fallback_rate"].append(rep["fallback"] / max(1, rep["paragraphs"]))
        for k, key in (("fidelity", "mean_fidelity"), ("before", "template_score_before"),
                       ("after", "template_score_after")):
            if rep[key] is not None:
                agg[k].append(rep[key])
    m = lambda x: round(mean(x), 3) if x else None
    return {"docs": agg["docs"], "entity_loss": agg["entity_loss"], "fallback_rate": m(agg["fallback_rate"]),
            "mean_fidelity": m(agg["fidelity"]), "template_before": m(agg["before"]),
            "template_after": m(agg["after"])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("golden"); ap.add_argument("--level", type=int, default=3)
    ap.add_argument("--provider", choices=["mock", "anthropic"], default="mock")
    a = ap.parse_args()
    prov = AnthropicProvider() if a.provider == "anthropic" else MockProvider()
    out = run(a.golden, a.level, prov)
    print(json.dumps(out, indent=2))
    ok = out["entity_loss"] == 0 and (out["template_after"] is None or out["template_after"] <= out["template_before"])
    print("GATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
