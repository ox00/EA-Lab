from dataclasses import dataclass
from dataclasses import asdict
from typing import Dict, Union


@dataclass(frozen=True)
class MarioConfig:
    height: int = 16
    segment_width: int = 14
    num_segments: int = 8
    max_jumpable_gap: int = 3
    target_difficulty: float = 0.55
    target_emptiness: float = 0.45
    population_size: int = 20
    crossover_rate: float = 0.9
    mutation_rate: float = 0.2
    generations: int = 10
    seed: int = 7
    nsga2_objective_mode: str = "core_3obj"
    init_mode: str = "random"
    ai_seed_ratio: float = 0.5
    ai_seed_temperature: float = 0.9
    ai_seed_start_length: int = 3
    ai_seed_repair: bool = False

    @property
    def width(self) -> int:
        return self.segment_width * self.num_segments

    def as_dict(self) -> Dict[str, Union[int, float]]:
        data = asdict(self)
        data["width"] = self.width
        return data
