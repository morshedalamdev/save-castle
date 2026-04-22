from dataclasses import dataclass, field


INITIAL_ENEMY_SPAWN_INTERVAL = 2.0


@dataclass
class EnemySpawnTimer:
    interval: float = INITIAL_ENEMY_SPAWN_INTERVAL
    elapsed: float = 0.0


@dataclass
class EnemiesBeingTyped:
    indicator: bool = False
    ids: set[int] = field(default_factory=set)
