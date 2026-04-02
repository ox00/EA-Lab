from dataclasses import dataclass
from dataclasses import asdict


@dataclass(frozen=True)
class MarioConfig:
    height: int = 16
    segment_width: int = 14
    num_segments: int = 8
    max_jumpable_gap: int = 3
    target_difficulty: float = 0.55
    population_size: int = 20
    crossover_rate: float = 0.9
    mutation_rate: float = 0.2
    generations: int = 10
    seed: int = 7

    @property
    def width(self) -> int:
        return self.segment_width * self.num_segments

    def as_dict(self) -> dict[str, int | float]:
        data = asdict(self)
        data["width"] = self.width
        return data
