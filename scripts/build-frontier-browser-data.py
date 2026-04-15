#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SHOWCASE_ROOT = ROOT / "output" / "pcg" / "showcase"
BROWSER_ROOT = ROOT / "docs" / "results" / "frontier-browser"
ASSET_ROOT = BROWSER_ROOT / "assets"


def humanize_case_name(case_id: str) -> str:
    parts = case_id.split("_")
    if len(parts) != 4:
        return case_id.replace("_", " ")

    return (
        f"pop={parts[0].removeprefix('pop')}, "
        f"mut={parts[1].removeprefix('mut')}.{parts[2]}, "
        f"seed={parts[3].removeprefix('seed')}"
    )


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


def build_case(case_dir: Path) -> dict:
    summary = load_json(case_dir / "summary.json")
    frontier = load_json(case_dir / "frontier_summary.json")
    config = load_json(case_dir / "config.json")
    logs = load_json(case_dir / "logs.json")

    browser_case_asset_root = ASSET_ROOT / case_dir.name
    best_png_path = copy_asset(case_dir / "best_level.png", browser_case_asset_root / "best_level.png")
    best_txt_path = maybe_copy_text(case_dir / "best_level.txt", browser_case_asset_root / "best_level.txt")

    case = {
        "id": case_dir.name,
        "title": humanize_case_name(case_dir.name),
        "algorithm": summary.get("algorithm"),
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
        entry = {
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
        }
        case["frontier"].append(entry)
    return case


def main() -> None:
    BROWSER_ROOT.mkdir(parents=True, exist_ok=True)
    if ASSET_ROOT.exists():
        shutil.rmtree(ASSET_ROOT)
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)

    cases = []
    for case_dir in sorted(SHOWCASE_ROOT.iterdir()):
        if not case_dir.is_dir():
            continue
        if not (case_dir / "summary.json").exists():
            continue
        cases.append(build_case(case_dir))

    payload = {
        "project": "EA Lab A8 Mario PCG",
        "cases": cases,
    }
    payload_text = json.dumps(payload, indent=2)
    (BROWSER_ROOT / "browser_data.json").write_text(
        payload_text + "\n",
        encoding="utf-8",
    )
    (BROWSER_ROOT / "browser_data.js").write_text(
        "window.BROWSER_DATA = " + payload_text + ";\n",
        encoding="utf-8",
    )
    print("Browser data:", BROWSER_ROOT / "browser_data.json")


if __name__ == "__main__":
    main()
