# Mandir Jumper

A vertical scrolling game where you control a Nepali warrior jumping between temple walls (mandirs).

## Features

- **Automatic Climbing**: The warrior automatically climbs upward
- **Wall Jumping**: Press SPACE or click to jump between temple walls
- **Enemies**: 
  - Flying crows that move horizontally
  - Spinning khukuris (traditional Nepali curved knives)
- **Power-ups**:
  - **Chiyaa** (tea): Increases climbing speed temporarily
  - **Prayer Wheel**: Grants temporary invincibility
- **Session Highscore**: Your best score is tracked during the current game session
- **Score System**: Score increases as you climb higher
- **Portrait Layout**: Mobile-style vertical screen

## Installation

1. Install Python 3.7 or higher
2. Install pygame:
   ```bash
   pip install pygame
   ```
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python mandir_jumper.py
   ```

2. **Controls**:
   - **SPACE** or **Mouse Click**: Jump between walls
   - **R**: Restart game (when game over)

3. **Objective**:
   - Climb as high as possible between the temple walls
   - Avoid enemies (crows and spinning khukuris)
   - Collect power-ups for advantages
   - Beat your highscore!

## Game Mechanics

- The warrior automatically climbs between two temple walls
- Jump timing is crucial to avoid enemies
- Power-ups spawn every 10 seconds
- Enemies spawn every 1.5 seconds (gets faster as score increases)
- Score = Height climbed / 10
- Session highscore resets when you restart the game

## UI Elements

- **High Score**: Displayed at the top, resets when you restart the game
- **Current Score**: Shows your current climbing progress
- **Power-up Status**: Visual indicators for active power-ups
- **Game Over Screen**: Shows final score and highscore

## Code Structure

The game is modular and easy to expand:

- `Player`: Warrior character with power-up states
- `Enemy`: Crows and khukuris with different behaviors
- `PowerUp`: Collectible items with visual effects
- `Game`: Main game loop, state management, and highscore system

## Files

- `mandir_jumper.py`: Main game file
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Expansion Ideas

- Add more enemy types (temple guards, flying daggers)
- New power-ups (double jump, shield, slow motion)
- Different temple themes (mountain, valley, city)
- Achievements system
- Multiplayer support
- Mobile touch controls
- Better graphics and animations
- Sound track and ambient temple sounds

## Technical Notes

- Built with Pygame
- 60 FPS gameplay
- Portrait orientation (400x700 pixels)
- Collision detection using pygame rectangles
- Session-based highscore tracking
- Cross-platform compatibility

## Cultural Elements

- **Mandir**: Hindi/Nepali word for temple
- **Khukuri**: Traditional curved Nepali knife
- **Chiyaa**: Nepali word for tea
- **Prayer Wheel**: Buddhist/Hindu spiritual element

Enjoy your temple-jumping adventure!
