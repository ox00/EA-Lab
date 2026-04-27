# Mario Level Generation via Hard-Constrained Multi-Objective Evolutionary Search

[![Interactive Demo](https://img.shields.io/badge/Live-Interactive%20Demo-blue)](https://ox00.github.io/EA-Lab/)
[![Source Code](https://img.shields.io/badge/GitHub-Repository-green)](https://github.com/ox00/EA-Lab)

This project implements a robust Procedural Content Generation (PCG) pipeline for Mario level design. It combines an **explicit segment-based representation**, **hard feasibility constraints**, and **NSGA-II multi-objective optimization** to generate playable, diverse, and semantically controlled levels. The system also integrates an **AI-seeded initialization** path using an LSTM model trained on VGLC data.

---

## 🚀 Core Features

- **Explicit Genotype-Phenotype Mapping**: Levels are represented as chromosomes of segment identifiers, ensuring a transparent and deterministic decoding process.
- **Hard Feasibility Constraints**: A built-in reachability checker ensures every generated level is fully traversable from start to goal.
- **Multi-Objective Optimization (NSGA-II)**: Simultaneously optimizes for Difficulty Error, Structural Diversity, and Emptiness Error, preserving a Pareto frontier of trade-off solutions.
- **AI-Seeded Initialization**: Leverages an LSTM sequence model to seed the initial population with structures learned from original Mario levels.
- **Interactive Frontier Browser**: A web-based visualization tool to inspect the Pareto frontier, including lite-physics replays for traversal evidence.

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ox00/EA-Lab.git
   cd EA-Lab
   ```

2. **Set up the environment**:
   It is recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 Quick Start

To run the main evolutionary search experiment (NSGA-II with 3 objectives):

```bash
# Using the shell script wrapper
./scripts/run-mvp.sh --algorithm nsga2 --nsga2-objective-mode core_3obj --generations 20

# Or using Python directly
export PYTHONPATH=src
python -m ea_lab.pcg.demo --algorithm nsga2 --nsga2-objective-mode core_3obj --generations 20
```

### Key Arguments:
- `--algorithm`: `ea` (Single-objective) or `nsga2` (Multi-objective).
- `--init-mode`: `random` or `ai_seeded`.
- `--nsga2-objective-mode`: `core_3obj`, `family_4obj`, `curve_4obj`, or `semantic_5obj`.
- `--output-dir`: Where to save the results (default: `output/pcg/mvp`).

### AI-Seeded Assets
- The `ai_seeded` mode expects the processed chromosome data at `data/processed/vglc_chromosomes_approx.json`.
- The pre-trained LSTM checkpoint is stored at `models/lstm_generator.pt`.
- If the LSTM checkpoint is unavailable at runtime, the pipeline falls back to sampling from the processed chromosome distribution. The processed data file is still required for seeded initialization.

---

## 📊 Result Interpretation

After running an experiment, the results are saved in the `output/` directory.

### Browser/Replay Evidence
The project includes a specialized tool to view the Pareto frontier and traversal evidence:
1. Open `docs/index.html` or `docs/results/frontier-browser/index.html` in your browser.
2. This browser allows you to:
   - Visualize the Pareto frontier in 3D/2D metrics space.
   - Render the best levels from each front.
   - View **Lite-Physics Replays** showing the jumping and collision actions required to complete the level.

---

## 📂 Project Structure

- `src/`: Core source code (PCG engine and AI generator).
- `models/`: Pre-trained LSTM models for AI-seeded initialization.
- `output/`: Algorithm result data and experiment logs.
- `data/`: Generation seed library (processed VGLC data and segments).
- `scripts/`: Utility scripts for running batch experiments and generating figures.
- `docs/results/report/`: Formal project reports and analysis documents.

---

## 🔗 Project Availability
- **Live Demo**: [https://ox00.github.io/EA-Lab/](https://ox00.github.io/EA-Lab/)
- **Repository**: [https://github.com/ox00/EA-Lab](https://github.com/ox00/EA-Lab)

---
*Developed for CDS526: Evolutionary Computation Project.*
