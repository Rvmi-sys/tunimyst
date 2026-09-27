# Tunimyst

An educational trivia game about Tunisian culture, built as a four-person university project at MedTech / South Mediterranean University in 2025. Players answer questions about history, geography, sports and culture across increasingly difficult levels. Correct answers gradually reveal a Tunisian public figure, followed by a bonus guessing question.

## Features

- Multiple quiz levels and timed questions
- Score tracking, results and a scoreboard
- Progressive image reveal and bonus rounds
- Pygame interface with menus, buttons and sound controls

## Run locally

Install Python 3 and Pygame, then run from the repository root:

```bash
python -m pip install -r requirements.txt
python Tunimyst.py
```

The original `Sound_Effect.mp3` and `Nidhal_Saadi1.png` were unavailable in this export. Sound is optional; the first Nidhal image falls back to the base background. Some image assets depict public figures and may require separate rights clearance for reuse outside this educational project.

## Team and contributions

- **Rami Ben Moallem:** interface visuals, backgrounds, text and button rendering, score-box animation and correct-answer effects; wrote the project report.
- **Mohamed Hachem Bouguerra:** game structure, question loading and game-state flow.
- **Khadija Triki:** answer logic, scoring and result display.
- **Taoufik Elloumi:** scoring system and score animations.

Contributions are based on the team's project report. This is a collaborative university project, not a solo work.

## Tech stack

Python, Pygame.
