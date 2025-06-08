import numpy as np
import pygame
from typing import List, Tuple, Optional, Callable
from .body import RigidBody

class Particle(RigidBody):
    """Particle with lifetime and visual properties."""
    def __init__(self,
                 pos: Tuple[float, float],
                 vel: Tuple[float, float],
                 radius: float,
                 color: Tuple[int, int, int],
                 lifetime: float):
        super().__init__(pos, radius, 1.0)
        self.vel = np.array(vel, dtype=float)
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.alpha = 255

    def update(self, dt: float) -> bool:
        """Update particle state."""
        self.age += dt
        if self.age >= self.lifetime:
            return True

        self.alpha = int(255 * (1.0 - self.age / self.lifetime))
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw particle with alpha."""
        if self.alpha <= 0:
            return

        surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, self.alpha),
                         (self.radius, self.radius), self.radius)
        
        screen.blit(surf, (int(self.pos[0] - self.radius),
                          int(self.pos[1] - self.radius)))

class ParticleEmitter:
    """Base particle emitter."""
    def __init__(self,
                 pos: Tuple[float, float],
                 rate: float,
                 particle_lifetime: float,
                 particle_radius: float,
                 color: Tuple[int, int, int]):
        self.pos = np.array(pos, dtype=float)
        self.rate = rate
        self.particle_lifetime = particle_lifetime
        self.particle_radius = particle_radius
        self.color = color
        self.accumulator = 0.0
        self.active = True

    def emit(self, dt: float) -> List[Particle]:
        """Emit new particles."""
        if not self.active:
            return []
        if self.rate == 0:
            self.active = False
            return self._create_particles(1)
        self.accumulator += dt
        num_particles = int(self.rate * self.accumulator)
        self.accumulator -= num_particles / self.rate
        return self._create_particles(num_particles)

    def _create_particles(self, count: int) -> List[Particle]:
        """Create particles."""
        return []

class PointEmitter(ParticleEmitter):
    """Point emitter with random velocity."""
    def __init__(self,
                 pos: Tuple[float, float],
                 rate: float,
                 particle_lifetime: float,
                 particle_radius: float,
                 color: Tuple[int, int, int],
                 speed_range: Tuple[float, float],
                 angle_range: Tuple[float, float]):
        super().__init__(pos, rate, particle_lifetime, particle_radius, color)
        self.speed_range = speed_range
        self.angle_range = angle_range

    def _create_particles(self, count: int) -> List[Particle]:
        particles = []
        for _ in range(count):
            angle = np.random.uniform(*self.angle_range)
            speed = np.random.uniform(*self.speed_range)
            vel = (speed * np.cos(angle), speed * np.sin(angle))
            particle = Particle(self.pos, vel, self.particle_radius,
                              self.color, self.particle_lifetime)
            particles.append(particle)
        return particles

class ConfettiEmitter(PointEmitter):
    """Confetti burst emitter."""
    def __init__(self, pos, count=40):
        super().__init__(
            pos=pos,
            rate=0,
            particle_lifetime=0.4,
            particle_radius=4,
            color=(255,255,255),
            speed_range=(700, 1200),
            angle_range=(0, 2 * np.pi)
        )
        self.count = count

    def _create_particles(self, count):
        particles = []
        for _ in range(self.count):
            angle = np.random.uniform(*self.angle_range)
            speed = np.random.uniform(*self.speed_range)
            vel = (speed * np.cos(angle), speed * np.sin(angle))
            color = tuple(np.random.randint(0, 256, 3))
            particle = Particle(self.pos, vel, self.particle_radius, color, self.particle_lifetime)
            particles.append(particle)
        return particles

class ParticleSystem:
    """Particle system manager."""
    def __init__(self):
        self.emitters: List[ParticleEmitter] = []
        self.particles: List[Particle] = []

    def add_emitter(self, emitter: ParticleEmitter) -> None:
        """Add emitter."""
        self.emitters.append(emitter)

    def update(self, dt: float) -> None:
        """Update particles and emitters."""
        self.particles = [p for p in self.particles if not p.update(dt)]

        for emitter in self.emitters:
            new_particles = emitter.emit(dt)
            self.particles.extend(new_particles)

        for particle in self.particles:
            particle.integrate(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(screen) 