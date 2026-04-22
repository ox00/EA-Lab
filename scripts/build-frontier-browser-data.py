#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BROWSER_ROOT = ROOT / "docs" / "results" / "frontier-browser"
ASSET_ROOT = BROWSER_ROOT / "assets"
CASE_SOURCES = [
    ("core baseline", ROOT / "output" / "pcg" / "v31_compare" / "core_3obj_seed7"),
    ("family showcase", ROOT / "output" / "pcg" / "v31_compare" / "family_4obj_seed27"),
    ("curve showcase", ROOT / "output" / "pcg" / "v32_curve_compare" / "curve_4obj_seed27"),
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_asset(source: Path, target: Path) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target.relative_to(BROWSER_ROOT).as_posix()


def maybe_copy_text(source: Path, target: Path) -> str | None:
    if not source.exists():
        return None
    return copy_asset(source, target)


def build_case(label: str, case_dir: Path) -> dict:
    summary = load_json(case_dir / "summary.json")
    frontier = load_json(case_dir / "frontier_summary.json")
    config = load_json(case_dir / "config.json")
    logs = load_json(case_dir / "logs.json")

    browser_case_asset_root = ASSET_ROOT / case_dir.name
    best_png_path = copy_asset(case_dir / "best_level.png", browser_case_asset_root / "best_level.png")
    best_txt_path = maybe_copy_text(case_dir / "best_level.txt", browser_case_asset_root / "best_level.txt")

    case = {
        "id": case_dir.name,
        "title": label,
        "algorithm": summary.get("algorithm"),
        "objective_mode": summary.get("nsga2_objective_mode"),
        "config": {
            "population_size": config.get("population_size"),
            "mutation_rate": config.get("mutation_rate"),
            "generations": config.get("generations"),
            "seed": config.get("seed"),
            "num_segments": config.get("num_segments"),
            "segment_width": config.get("segment_width"),
            "target_difficulty": config.get("target_difficulty"),
            "target_emptiness": config.get("target_emptiness"),
        },
        "evaluation": summary.get("evaluation", {}),
        "constraints": summary.get("constraints", {}),
        "best_level": {
            "png_path": best_png_path,
            "ascii_path": best_txt_path,
            "chromosome": summary.get("best_chromosome", []),
            "segment_metadata": summary.get("best_segment_metadata", []),
        },
        "logs": logs,
        "frontier": [],
        "final_front_hv": logs[-1].get("first_front_hv") if logs else None,
        "final_front_spread": logs[-1].get("first_front_spread") if logs else None,
        "final_front_size": logs[-1].get("first_front_size") if logs else None,
    }

    for item in frontier.get("levels", []):
        rank = item.get("rank")
        png_source = case_dir / item["png_path"]
        ascii_source = case_dir / item["ascii_path"]
        case["frontier"].append(
            {
                "rank": rank,
                "png_path": copy_asset(
                    png_source,
                    browser_case_asset_root / "frontier_levels" / f"frontier_{rank:02d}.png",
                ),
                "ascii_path": maybe_copy_text(
                    ascii_source,
                    browser_case_asset_root / "frontier_levels" / f"frontier_{rank:02d}.txt",
                ),
                "evaluation": item.get("individual", {}).get("evaluation", {}),
                "constraints": item.get("individual", {}).get("constraints", {}),
                "chromosome": item.get("individual", {}).get("chromosome", []),
                "segment_metadata": item.get("individual", {}).get("segment_metadata", []),
            }
        )
    return case


def build_compare_summary(cases: list[dict]) -> list[dict]:
    rows = []
    for case in cases:
        rows.append(
            {
                "title": case["title"],
                "objective_mode": case["objective_mode"],
                "difficulty_error": case["evaluation"].get("difficulty_error"),
                "emptiness_error": case["evaluation"].get("emptiness_error"),
                "difficulty_curve_error": case["evaluation"].get("difficulty_curve_error"),
                "family_balance": case["evaluation"].get("family_balance"),
                "front_hv": case.get("final_front_hv"),
                "front_spread": case.get("final_front_spread"),
                "front_size": case.get("final_front_size"),
            }
        )
    return rows


def main() -> None:
    BROWSER_ROOT.mkdir(parents=True, exist_ok=True)
    if ASSET_ROOT.exists():
        shutil.rmtree(ASSET_ROOT)
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)

    cases = [build_case(label, case_dir) for label, case_dir in CASE_SOURCES]
    payload = {
        "project": "EA Lab A8 Mario PCG",
        "cases": cases,
        "compare_summary": build_compare_summary(cases),
    }

    payload_text = json.dumps(payload, indent=2)
    (BROWSER_ROOT / "browser_data.json").write_text(payload_text + "\n", encoding="utf-8")
    (BROWSER_ROOT / "browser_data.js").write_text("window.BROWSER_DATA = " + payload_text + ";\n", encoding="utf-8")
    print("Browser data:", BROWSER_ROOT / "browser_data.json")


if __name__ == "__main__":
    main()
