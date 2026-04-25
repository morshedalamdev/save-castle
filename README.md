# save-castle

Python/JavaScript conversion of the **Typing Defense** game from Rust/JavaScript.

## Tech stack
- Python 3.10 (recommended)
- Pygame
- Pytest (test runner)
- HTML/CSS/JavaScript web assets preserved from the original project (`web/`, `index.html`)

## Local setup

### 1) Create and activate a virtual environment

macOS/Linux:
```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
```

If `python3.10` is not available, use your installed Python 3 interpreter.

### 2) Install dependencies
```bash
python -m pip install -r requirements.txt
```

## Run locally

### Run the game (Python + Pygame)
```bash
python src/main.py
```

## How to play

### Objective
- Defend the castle by typing enemy words before they reach it.
- You lose lives when enemies collide with the castle.
- The game ends when lives reach `0`.

### Controls
- `SPACE`: Start game / start next round / restart after game over.
- `ESC`: Pause/resume during a started game.
- `BACKSPACE`: Cancel current typing target.
- `1`, `2`, `3`: Set difficulty (`EASY`, `MEDIUM`, `HARD`).
- `A-Z`: Type letters to target and eliminate enemies.

### Gameplay loop
- Each round spawns a limited number of enemies.
- Type the letters of an enemy's word in order to defeat it.
- Your HUD tracks round, WPM, score, streak, lives, and difficulty.
- When a round completes, press `SPACE` to begin the next round.
- Faster and more accurate typing improves streak and score.

### Run tests (Pytest)
```bash
python -m pytest -q
```

### Open web assets (HTML/CSS/JavaScript)
The repository includes browser assets in `index.html` and `web/`.

Open `index.html` directly in your browser, or serve the project root with a simple local server:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`.

## Project structure
The project keeps the same high-level layout as the original Rust codebase:
- `assets/` (original sprites/background/ui/words)
- `src/main.py` (game entrypoint)
- `src/systems.py`
- `src/game/**` (castle, enemies, rounds_and_indicators, hud, effects, boss, decorations)
- `src/menu/**`
- `web/sound.js`, `web/styles.css`, `index.html`
