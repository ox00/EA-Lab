#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

OUTPUT_ROOT="${OUTPUT_ROOT:-output/pcg/baseline_compare}"
SEEDS="${SEEDS:-7 17 27 37 47}"
ALGORITHMS="${ALGORITHMS:-ea nsga2}"
GENERATIONS="${GENERATIONS:-20}"
POPULATION_SIZE="${POPULATION_SIZE:-30}"
RENDER_BACKEND="${RENDER_BACKEND:-ascii}"

mkdir -p "$OUTPUT_ROOT"

echo "Running baseline compare..."
echo "Output root: $OUTPUT_ROOT"
echo "Algorithms: $ALGORITHMS"
echo "Seeds: $SEEDS"
echo "Generations: $GENERATIONS, Population size: $POPULATION_SIZE"

for algorithm in $ALGORITHMS; do
  for seed in $SEEDS; do
    run_dir="$OUTPUT_ROOT/${algorithm}_seed${seed}"
    echo "-> $algorithm seed=$seed"
    PYTHONPATH=src python3 -m ea_lab.pcg.demo \
      --algorithm "$algorithm" \
      --seed "$seed" \
      --generations "$GENERATIONS" \
      --population-size "$POPULATION_SIZE" \
      --render-backend "$RENDER_BACKEND" \
      --output-dir "$run_dir"
  done
done

python3 scripts/summarize-baseline.py \
  --base-dir "$OUTPUT_ROOT" \
  --algorithms $ALGORITHMS \
  --output-prefix compare_summary

echo "Baseline compare completed."
