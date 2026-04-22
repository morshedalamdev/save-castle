from __future__ import annotations


def reset_typing(enemies, typing_ids: set[int]) -> None:
    for enemy in enemies:
        enemy.typing_index = -1
    typing_ids.clear()


def on_letter_pressed(letter: str, enemies, typing_ids: set[int], indicators) -> int:
    killed = 0
    made_mistake = False
    active = [e for e in enemies if id(e) in typing_ids]
    if not active:
        for enemy in enemies:
            if enemy.word and enemy.word[0] == letter:
                enemy.typing_index = 0
                typing_ids.add(id(enemy))
                indicators.streak += 1
                if len(enemy.word) == 1:
                    killed += 1
        return killed

    for enemy in active:
        next_index = enemy.typing_index + 1
        if next_index < len(enemy.word) and enemy.word[next_index] == letter:
            enemy.typing_index = next_index
            indicators.streak += 1
            if next_index == len(enemy.word) - 1:
                killed += 1
        else:
            enemy.typing_index = -1
            typing_ids.discard(id(enemy))
            made_mistake = True

    if made_mistake and not typing_ids:
        indicators.streak = 0
    return killed
