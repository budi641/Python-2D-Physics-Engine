import pygame
import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class Constraint:
    """Base class for position-based constraints."""
    stiffness: float = 1.0
    iterations: int = 1

    def solve(self, dt: float) -> None:
        """Solve constraint."""
        pass

class RigidBody:
    def __init__(self,
                 pos: Tuple[float, float],
                 radius: float,
                 mass: float,
                 restitution: float = 0.8,
                 friction: float = 0.1):
        self.pos = np.array(pos, dtype=float)
        self.prev_pos = self.pos.copy()
        self.vel = np.zeros(2, dtype=float)
        self.force = np.zeros(2, dtype=float)
        self.radius = radius
        self.mass = mass
        self.inv_mass = 1.0 / mass if mass > 0 else 0
        self.restitution = restitution
        self.friction = friction
        self.is_static = mass == 0
        self.constraints: List[Constraint] = []
        self.pinned = False

    def apply_force(self, force: np.ndarray) -> None:
        """Apply force to body."""
        self.force += force

    def apply_impulse(self, impulse: np.ndarray) -> None:
        """Apply impulse to body."""
        if not self.is_static:
            self.vel += impulse * self.inv_mass

    def integrate(self, dt: float) -> None:
        """Integrate physics using Verlet."""
        if self.is_static or self.pinned:
            return

        self.prev_pos = self.pos.copy()
        self.vel += self.force * self.inv_mass * dt
        self.vel *= (1.0 - self.friction)
        self.pos += self.vel * dt + 0.5 * self.force * self.inv_mass * dt * dt
        self.force = np.zeros(2, dtype=float)

    def solve_constraints(self, dt: float) -> None:
        """Solve all constraints."""
        for constraint in self.constraints:
            for _ in range(constraint.iterations):
                constraint.solve(dt)

    def get_velocity_at_point(self, point: np.ndarray) -> np.ndarray:
        """Get velocity at point."""
        return self.vel.copy()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw body for debug."""
        pygame.draw.circle(screen, (255, 0, 0), 
                         (int(self.pos[0]), int(self.pos[1])), 
                         int(self.radius), 1)

class SoftBody:
    """Collection of particles with constraints."""
    def __init__(self):
        self.particles: List[RigidBody] = []
        self.constraints: List[Constraint] = []

    def add_particle(self, particle: RigidBody) -> None:
        """Add particle."""
        self.particles.append(particle)

    def add_constraint(self, constraint: Constraint) -> None:
        """Add constraint."""
        self.constraints.append(constraint)

    def solve_constraints(self, dt: float) -> None:
        """Solve all constraints."""
        for constraint in self.constraints:
            for _ in range(constraint.iterations):
                constraint.solve(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw soft body."""
        for particle in self.particles:
            particle.draw(screen)

class DistanceConstraint(Constraint):
    """Maintains fixed distance between particles."""
    def __init__(self, p1: RigidBody, p2: RigidBody, distance: float):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.distance = distance

    def solve(self, dt: float) -> None:
        if self.p1.is_static and self.p2.is_static:
            return

        delta = self.p2.pos - self.p1.pos
        dist = np.linalg.norm(delta)
        if dist == 0:
            return

        diff = (dist - self.distance) / dist
        correction = delta * diff * self.stiffness

        if not self.p1.is_static:
            self.p1.pos += correction * self.p1.inv_mass / (self.p1.inv_mass + self.p2.inv_mass)
        if not self.p2.is_static:
            self.p2.pos -= correction * self.p2.inv_mass / (self.p1.inv_mass + self.p2.inv_mass) 