#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import shutil
from collections import Counter
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


def read_text_if_exists(source: Path) -> str | None:
    if not source.exists():
        return None
    return source.read_text(encoding="utf-8")


def build_case(label: str, case_dir: Path) -> dict:
    summary = load_json(case_dir / "summary.json")
    frontier = load_json(case_dir / "frontier_summary.json")
    config = load_json(case_dir / "config.json")
    logs = load_json(case_dir / "logs.json")

    browser_case_asset_root = ASSET_ROOT / case_dir.name
    best_png_path = copy_asset(case_dir / "best_level.png", browser_case_asset_root / "best_level.png")
    best_txt_path = maybe_copy_text(case_dir / "best_level.txt", browser_case_asset_root / "best_level.txt")
    best_txt_inline = read_text_if_exists(case_dir / "best_level.txt")

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
            "ascii_text": best_txt_inline,
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
                "ascii_text": read_text_if_exists(ascii_source),
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


PHYSICS_SPEC = {
    "frame_dt": 1 / 30,
    "tile_size": 20,
    "actor_width_ratio": 0.72,
    "actor_height_ratio": 0.90,
    "run_speed": 150,
    "jump_velocity": -420,
    "gravity": 600,
    "max_fall_speed": 420,
    "action_frames": 4,
    "goal_tolerance_px": 10,
    "max_expansions": 50000,
}
PHYSICS_ACTIONS = ("R", "RJ", "RR", "N", "J")
SOLID_TILES = {"#", "B", "?", "P"}


def js_round(value: float) -> int:
    return math.floor(value + 0.5) if value >= 0 else math.ceil(value - 0.5)


def parse_ascii_grid(ascii_text: str) -> list[list[str]]:
    return [list(line) for line in ascii_text.strip().splitlines()]


def physics_action_frame_limit(action_label: str) -> int:
    return PHYSICS_SPEC["action_frames"] * 2 if action_label == "RR" else PHYSICS_SPEC["action_frames"]


def physics_action_input(action_label: str, frame_index: int) -> dict[str, bool]:
    jump_frame = frame_index == 0
    if action_label == "RJ":
        return {"move_left": False, "move_right": True, "jump": jump_frame}
    if action_label in {"R", "RR"}:
        return {"move_left": False, "move_right": True, "jump": False}
    if action_label == "J":
        return {"move_left": False, "move_right": False, "jump": jump_frame}
    return {"move_left": False, "move_right": False, "jump": False}


def tile_at(grid: list[list[str]], col: int, row: int) -> str:
    if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
        return "."
    return grid[row][col]


def find_tile(grid: list[list[str]], target: str) -> tuple[int, int] | None:
    for row_index, row in enumerate(grid):
        for col_index, tile in enumerate(row):
            if tile == target:
                return row_index, col_index
    return None


def actor_geometry() -> tuple[float, float]:
    return (
        PHYSICS_SPEC["tile_size"] * PHYSICS_SPEC["actor_width_ratio"],
        PHYSICS_SPEC["tile_size"] * PHYSICS_SPEC["actor_height_ratio"],
    )


def intersects_solid(grid: list[list[str]], actor: dict[str, float], next_x: float, next_y: float) -> tuple[int, int] | None:
    tile_size = PHYSICS_SPEC["tile_size"]
    min_col = math.floor(next_x / tile_size)
    max_col = math.floor((next_x + actor["width"] - 1) / tile_size)
    min_row = math.floor(next_y / tile_size)
    max_row = math.floor((next_y + actor["height"] - 1) / tile_size)

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if tile_at(grid, col, row) in SOLID_TILES:
                return row, col
    return None


def spawn_physics_actor(grid: list[list[str]]) -> dict[str, float]:
    tile_size = PHYSICS_SPEC["tile_size"]
    width, height = actor_geometry()
    start = find_tile(grid, "S") or (len(grid) - 3, 1)
    return {
        "x": start[1] * tile_size,
        "y": start[0] * tile_size - tile_size * 0.8,
        "vx": 0.0,
        "vy": 0.0,
        "width": width,
        "height": height,
        "on_ground": False,
    }


def step_physics_actor(grid: list[list[str]], actor: dict[str, float], input_flags: dict[str, bool]) -> dict[str, float]:
    next_actor = dict(actor)
    next_actor["vx"] = 0.0

    if input_flags["move_left"]:
        next_actor["vx"] = -PHYSICS_SPEC["run_speed"]
    if input_flags["move_right"]:
        next_actor["vx"] = PHYSICS_SPEC["run_speed"]

    if input_flags["jump"] and next_actor["on_ground"]:
        next_actor["vy"] = PHYSICS_SPEC["jump_velocity"]
        next_actor["on_ground"] = False

    next_actor["vy"] = min(
        next_actor["vy"] + PHYSICS_SPEC["gravity"] * PHYSICS_SPEC["frame_dt"],
        PHYSICS_SPEC["max_fall_speed"],
    )

    tile_size = PHYSICS_SPEC["tile_size"]
    next_x = next_actor["x"] + next_actor["vx"] * PHYSICS_SPEC["frame_dt"]
    hit = intersects_solid(grid, next_actor, next_x, next_actor["y"])
    if hit:
        _, hit_col = hit
        if next_actor["vx"] > 0:
            next_x = hit_col * tile_size - next_actor["width"]
        elif next_actor["vx"] < 0:
            next_x = (hit_col + 1) * tile_size
        next_actor["vx"] = 0.0
    next_actor["x"] = max(0.0, next_x)

    next_y = next_actor["y"] + next_actor["vy"] * PHYSICS_SPEC["frame_dt"]
    hit = intersects_solid(grid, next_actor, next_actor["x"], next_y)
    next_actor["on_ground"] = False
    if hit:
        hit_row, _ = hit
        if next_actor["vy"] > 0:
            next_y = hit_row * tile_size - next_actor["height"]
            next_actor["on_ground"] = True
        else:
            next_y = (hit_row + 1) * tile_size
        next_actor["vy"] = 0.0
    next_actor["y"] = next_y
    return next_actor


def settle_physics_actor(grid: list[list[str]], actor: dict[str, float]) -> dict[str, float]:
    current = dict(actor)
    for _ in range(40):
        current = step_physics_actor(grid, current, {"move_left": False, "move_right": False, "jump": False})
        if current["on_ground"]:
            break
    return current


def physics_state_key(actor: dict[str, float]) -> str:
    return "|".join(
        [
            str(js_round(actor["x"] / 6)),
            str(js_round(actor["y"] / 6)),
            str(js_round(actor["vx"] / 60)),
            str(js_round(actor["vy"] / 60)),
            "1" if actor["on_ground"] else "0",
        ]
    )


def build_lite_physics_plan(ascii_text: str) -> list[str]:
    grid = parse_ascii_grid(ascii_text)
    goal = find_tile(grid, "G")
    if goal is None:
        return []

    goal_x = goal[1] * PHYSICS_SPEC["tile_size"]
    start_actor = settle_physics_actor(grid, spawn_physics_actor(grid))
    open_nodes = [
        {
            "priority": 0.0,
            "cost": 0,
            "actor": start_actor,
            "parent": None,
            "action": None,
        }
    ]
    seen = {physics_state_key(start_actor): 0}
    expansions = 0

    while open_nodes and expansions < PHYSICS_SPEC["max_expansions"]:
        best_index = min(range(len(open_nodes)), key=lambda index: open_nodes[index]["priority"])
        current = open_nodes.pop(best_index)

        if current["actor"]["x"] >= goal_x - PHYSICS_SPEC["goal_tolerance_px"]:
            actions: list[str] = []
            cursor = current
            while cursor and cursor["parent"] is not None:
                actions.append(cursor["action"])
                cursor = cursor["parent"]
            return list(reversed(actions))

        for action_label in PHYSICS_ACTIONS:
            actor = current["actor"]
            for frame_index in range(physics_action_frame_limit(action_label)):
                actor = step_physics_actor(grid, actor, physics_action_input(action_label, frame_index))

            if actor["x"] < current["actor"]["x"] - 10:
                continue

            cost = current["cost"] + 1
            key = physics_state_key(actor)
            if seen.get(key, float("inf")) <= cost:
                continue

            seen[key] = cost
            heuristic = max(0.0, (goal_x - actor["x"]) / 80)
            open_nodes.append(
                {
                    "priority": cost + heuristic,
                    "cost": cost,
                    "actor": actor,
                    "parent": current,
                    "action": action_label,
                }
            )

        expansions += 1

    return []


def plan_record(case_id: str, case_title: str, candidate_id: str, candidate_label: str, ascii_text: str) -> dict:
    actions = build_lite_physics_plan(ascii_text)
    action_counts = dict(Counter(actions))
    total_frames = sum(physics_action_frame_limit(action) for action in actions)
    return {
        "key": f"{case_id}::{candidate_id}",
        "case_id": case_id,
        "case_title": case_title,
        "candidate_id": candidate_id,
        "candidate_label": candidate_label,
        "plan_found": bool(actions),
        "action_count": len(actions),
        "action_counts": action_counts,
        "actions": actions,
        "estimated_frames": total_frames,
        "estimated_seconds": round(total_frames * PHYSICS_SPEC["frame_dt"], 3),
    }


def build_lite_physics_exports(cases: list[dict]) -> tuple[dict, str]:
    items = []
    text_lines = [
        "Lite Physics Replay Export",
        "",
        "This artifact records collision-aware action plans under the browser replay physics.",
        "Constraint-level reachable replay and lite-physics replay are intentionally different evidence layers.",
        "",
        "Physics spec:",
    ]
    text_lines.extend(f"- {key}: {value}" for key, value in PHYSICS_SPEC.items())

    for case in cases:
        case_id = case["id"]
        case_title = case["title"]
        case_records = [
            plan_record(case_id, case_title, "best", "Best Level", case["best_level"]["ascii_text"] or "")
        ]
        case_records.extend(
            plan_record(
                case_id,
                case_title,
                f"frontier_{item['rank']}",
                f"Frontier Rank {item['rank']}",
                item["ascii_text"] or "",
            )
            for item in case["frontier"]
        )
        items.extend(case_records)

        text_lines.extend(
            [
                "",
                f"[{case_id}] {case_title}",
            ]
        )
        for record in case_records:
            status = "OK" if record["plan_found"] else "FAIL"
            text_lines.append(
                f"- {record['candidate_id']}: {status}, actions={record['action_count']}, seconds={record['estimated_seconds']}"
            )
            if record["plan_found"]:
                text_lines.append("  actions: " + " ".join(record["actions"]))

    payload = {
        "spec": PHYSICS_SPEC,
        "items": items,
    }
    return payload, "\n".join(text_lines) + "\n"


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

    physics_payload, physics_text = build_lite_physics_exports(cases)
    physics_payload_text = json.dumps(physics_payload, indent=2)
    (BROWSER_ROOT / "lite_physics_plans.json").write_text(physics_payload_text + "\n", encoding="utf-8")
    (BROWSER_ROOT / "lite_physics_plans.js").write_text(
        "window.LITE_PHYSICS_PLANS = " + physics_payload_text + ";\n",
        encoding="utf-8",
    )
    (BROWSER_ROOT / "lite_physics_plans.txt").write_text(physics_text, encoding="utf-8")
    print("Browser data:", BROWSER_ROOT / "browser_data.json")


if __name__ == "__main__":
    main()
