from dataclasses import dataclass


@dataclass
class CollidingWith:
    entity_id: int | None = None
