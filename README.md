# NEON RUNNER

A cyberpunk-themed platformer game built with Pygame.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

NEON RUNNER is a fast-paced cyberpunk platformer where players control a neon warrior battling through waves of enemies in a digital void. Features include double-jump mechanics, projectile attacks, particle effects, and a synthwave-inspired visual style.

## Features

- **Cyberpunk Aesthetics**: Neon color palette with glowing effects, scanlines, and grid backgrounds
- **Smooth Controls**: Responsive movement with double-jump capability
- **Combat System**: Mouse-click projectile attacks with screen shake feedback
- **Dynamic Difficulty**: Enemy spawn rate increases as your score rises
- **Particle Effects**: Explosions, trails, and ambient floating particles
- **Visual Polish**: Pulsing glows, glitch effects on title, and corner frame UI

## Controls

| Key | Action |
|-----|--------|
| `←` `→` or `A` `D` | Move left/right |
| `SPACE` | Jump / Double Jump |
| `Mouse Click` | Attack (shoot projectile) |
| `ESC` | Quit game |

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/theanswer910725/-NEON-PULSE.git
cd -NEON-PULSE
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
cd game
python main.py
```

## Project Structure

```
├── game/
│   ├── main.py          # Main game loop and logic
│   ├── player.py        # Player class with movement and combat
│   ├── enemy.py         # Enemy AI and behavior
│   ├── platform.py      # Platform rendering
│   ├── projectile.py    # Projectile class
│   ├── particles.py     # Particle system for effects
│   ├── constants.py     # Game constants and color palette
│   └── levels/          # Level data (reserved)
├── docs/                # Design documents and test plans
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Gameplay

- **Objective**: Survive as long as possible while defeating enemies to earn points
- **Scoring**: +100 points per enemy defeated
- **Health**: Player has 3 health points, displayed as a shield bar
- **Difficulty Scaling**: Enemy spawn interval decreases as score increases

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Cyan | `#00FFFF` | Player glow, UI borders |
| Magenta | `#FF00FF` | Score display, explosions |
| Neon Purple | `#B400FF` | Grid lines, ambient particles |
| Danger Red | `#FF003C` | Damage indicators |

## Development

### Running Tests

```bash
cd game
python -m pytest test_functional_verification.py
python -m pytest test_experience_verification.py
```

## License

This project is licensed under the MIT License.
