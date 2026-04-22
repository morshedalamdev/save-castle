# save-castle

Python/JavaScript conversion of the **Typing Defense** game from Rust/JavaScript.

## Tech stack
- Python 3
- Pygame
- JavaScript/CSS web assets preserved from the original project (`web/`)

## Run locally
```bash
python -m pip install -r requirements.txt
python src/main.py
```

## Project structure
The project keeps the same high-level layout as the original Rust codebase:
- `assets/` (original sprites/background/ui/words)
- `src/main.py` (game entrypoint)
- `src/systems.py`
- `src/game/**` (castle, enemies, rounds_and_indicators, hud, effects, boss, decorations)
- `src/menu/**`
- `web/sound.js`, `web/styles.css`, `index.html`
