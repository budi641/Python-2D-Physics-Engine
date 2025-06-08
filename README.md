# 8-Ball Pool Physics Simulation

A realistic 8-ball pool game implementation using Python and Pygame, featuring accurate physics simulation and particle effects.

## Project Structure

```
├── main.py              # Main game loop and initialization
├── settings.py          # Game configuration and constants
├── requirements.txt     # Python dependencies
├── game/               # Game-specific components
│   ├── ball.py         # Ball class and rendering
│   ├── cue.py          # Cue stick mechanics
│   └── table.py        # Pool table setup and management
└── physics/            # Physics engine components
    ├── body.py         # Rigid body and constraint system
    ├── collision.py    # Collision detection and response
    ├── particles.py    # Particle system for effects
    └── world.py        # Physics world management
```

## Core Components

### Physics Engine

The game uses a custom physics engine with the following features:

1. **Rigid Body System**
   - Position-based dynamics
   - Verlet integration for stable simulation
   - Mass and inertia properties
   - Friction and restitution coefficients

2. **Collision System**
   - Circle-circle collision detection
   - Circle-line collision detection
   - Impulse-based collision response
   - Penetration resolution

3. **Constraint System**
   - Distance constraints for soft bodies
   - Position-based constraint solving
   - Iterative constraint satisfaction

4. **Particle System**
   - Particle emitters
   - Lifetime management
   - Visual effects (confetti, impacts)

### Game Components

1. **Pool Table**
   - Customizable dimensions
   - Pocket detection
   - Cushion physics
   - Ball racking system

2. **Balls**
   - Realistic ball physics
   - Customizable properties
   - Visual rendering
   - Numbered design

3. **Cue Stick**
   - Power-based shooting
   - Angle control
   - Visual feedback
   - Collision detection

## Physics Implementation

### Core Equations

1. **Verlet Integration**
   ```
   x(t + Δt) = 2x(t) - x(t - Δt) + a(t)Δt²
   ```

2. **Collision Response**
   ```
   j = -(1 + e) * (v₁ - v₂) · n / (1/m₁ + 1/m₂)
   v₁' = v₁ + j/m₁ * n
   v₂' = v₂ - j/m₂ * n
   ```
   where:
   - j = impulse
   - e = coefficient of restitution
   - v = velocity
   - m = mass
   - n = collision normal

3. **Friction**
   ```
   F = -μN * v/|v|
   ```
   where:
   - μ = friction coefficient
   - N = normal force
   - v = velocity

## Setup and Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Controls

- **Mouse**: Aim and shoot
- **Left Click**: Set power
- **Right Click**: Shoot
- **R**: Reset game
- **ESC**: Pause/Resume

## Configuration

Game parameters can be adjusted in `settings.py`:
- Physics constants
- Visual properties
- Game dimensions
- Ball properties
- Table settings

## Dependencies

- Python 3.8+
- Pygame
- NumPy

## Future Improvements

1. Multiplayer support
2. Advanced game rules
3. AI opponents
4. Tournament mode
5. Custom table skins
6. Replay system 