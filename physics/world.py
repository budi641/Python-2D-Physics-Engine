import numpy as np
import pygame
from typing import List, Tuple
from .body import RigidBody, SoftBody
from .collision import circle_vs_circle, circle_vs_line, resolve_collision
from .particles import ParticleSystem
import settings

SUBSTEPS = 4  # Number of sub-steps per frame for robust collision handling
CUSHION_DAMPING = 1.0  # No extra damping for cushion collisions

class PhysicsWorld:
    def __init__(self, gravity: Tuple[float, float] = (0, 0), dt: float = 1/60):
        self.gravity = np.array(gravity, dtype=float)
        self.dt = dt
        self.bodies: List[RigidBody] = []
        self.soft_bodies: List[SoftBody] = []
        self.static_lines: List[Tuple[np.ndarray, np.ndarray]] = []
        self.particle_system = ParticleSystem()
        self.iterations = 8  # Number of constraint solving iterations

    def add_body(self, body: RigidBody) -> None:
        """Add physics body."""
        self.bodies.append(body)

    def add_soft_body(self, soft_body: SoftBody) -> None:
        """Add soft body."""
        self.soft_bodies.append(soft_body)
        # Add all particles to the main body list
        self.bodies.extend(soft_body.particles)

    def add_static_line(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> None:
        """Add static line."""
        self.static_lines.append((np.array(p1), np.array(p2)))

    def step(self) -> None:
        """Perform physics step."""
        sub_dt = self.dt / SUBSTEPS
        for _ in range(SUBSTEPS):
            # Apply gravity to all bodies
            for body in self.bodies:
                if not body.is_static:
                    body.apply_force(self.gravity * body.mass)

            # Integrate velocities and positions (classic Newtonian)
            for body in self.bodies:
                body.vel += body.force * body.inv_mass * sub_dt
                body.vel *= (1.0 - body.friction)
                body.pos += body.vel * sub_dt
                body.force = np.zeros(2, dtype=float)
                # Clamp position to table bounds
                left = settings.TABLE_MARGIN + body.radius
                right = settings.WINDOW_WIDTH - settings.TABLE_MARGIN - body.radius
                top = settings.TABLE_MARGIN + body.radius
                bottom = settings.WINDOW_HEIGHT - settings.TABLE_MARGIN - body.radius
                body.pos[0] = np.clip(body.pos[0], left, right)
                body.pos[1] = np.clip(body.pos[1], top, bottom)

            # Solve soft body constraints (if any)
            for _ in range(self.iterations):
                for soft_body in self.soft_bodies:
                    soft_body.solve_constraints(sub_dt)

            # Detect and resolve collisions (impulse-based, one pass)
            self._resolve_collisions()

        # Update particle system
        self.particle_system.update(self.dt)

    def _resolve_collisions(self) -> None:
        """Resolve all collisions."""
        # Check ball-ball collisions
        for i, body_a in enumerate(self.bodies):
            for body_b in self.bodies[i+1:]:
                collision = circle_vs_circle(body_a, body_b)
                if collision:
                    resolve_collision(collision)

        # Check ball-line collisions
        for body in self.bodies:
            for p1, p2 in self.static_lines:
                collision = circle_vs_line(body, p1, p2)
                if collision:
                    resolve_collision(collision)
                    # Add additional velocity damping for cushion collisions
                    body.vel *= CUSHION_DAMPING  # More realistic cushion hit

    def draw(self, screen: pygame.Surface) -> None:
        """Draw physics objects."""
        # Draw bodies
        for body in self.bodies:
            body.draw(screen)

        # Draw soft bodies
        for soft_body in self.soft_bodies:
            soft_body.draw(screen)

        # Draw static lines
        for p1, p2 in self.static_lines:
            pygame.draw.line(screen, (0, 255, 0),
                           (int(p1[0]), int(p1[1])),
                           (int(p2[0]), int(p2[1])), 1)

        # Draw particles
        self.particle_system.draw(screen)

    def remove_body(self, body):
        """Remove body from world."""
        if body in self.bodies:
            self.bodies.remove(body) 