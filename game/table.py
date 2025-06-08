import pygame
import numpy as np
from typing import List, Optional
from physics.world import PhysicsWorld
from .ball import Ball
import settings
from physics.particles import ConfettiEmitter

class Table:
    def __init__(self, world: PhysicsWorld):
        self.world = world
        self.balls: List[Ball] = []
        self.pockets: List[tuple] = []
        self._setup_table()
        self._setup_balls()

    def _setup_table(self) -> None:
        """Setup table and pockets."""
        left = settings.TABLE_MARGIN
        right = settings.WINDOW_WIDTH - settings.TABLE_MARGIN
        top = settings.TABLE_MARGIN
        bottom = settings.WINDOW_HEIGHT - settings.TABLE_MARGIN

        self.world.add_static_line((left, top), (right, top))
        self.world.add_static_line((right, top), (right, bottom))
        self.world.add_static_line((right, bottom), (left, bottom))
        self.world.add_static_line((left, bottom), (left, top))

        pocket_offset = settings.POCKET_RADIUS
        self.pockets = [
            (left, top),
            (right // 2, top),
            (right, top),
            (right, bottom),
            (right // 2, bottom),
            (left, bottom),
        ]

        if hasattr(self.world, 'particle_system'):
            for pocket in self.pockets:
                self.world.particle_system.add_emitter(ConfettiEmitter(pocket))

    def _setup_balls(self) -> None:
        """Setup initial ball positions."""
        cue_ball = Ball(0, settings.CUE_BALL_POS)
        self.balls.append(cue_ball)
        self.world.add_body(cue_ball)

        ball_order = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        start_x, start_y = settings.RACK_POS
        idx = 0
        for row in range(5):
            y = start_y + (row - 2) * settings.BALL_RADIUS * np.sqrt(3)
            for col in range(row+1):
                if idx >= len(ball_order):
                    break
                x = start_x + (col - row/2) * settings.BALL_RADIUS * 2
                ball = Ball(ball_order[idx], (x, y))
                self.balls.append(ball)
                self.world.add_body(ball)
                idx += 1

    def check_pockets(self) -> List[Ball]:
        """Check for pocketed balls."""
        pocketed_balls = []
        for ball in self.balls[:]:
            for pocket in self.pockets:
                distance = np.linalg.norm(np.array(ball.pos) - np.array(pocket))
                if distance < settings.POCKET_RADIUS:
                    if ball.number == 0:
                        ball.reset()
                    else:
                        pocketed_balls.append(ball)
                        self.balls.remove(ball)
                        self.world.remove_body(ball)
                        if hasattr(self.world, 'particle_system'):
                            self.world.particle_system.add_emitter(ConfettiEmitter(pocket))
        return pocketed_balls

    def is_ball_moving(self) -> bool:
        """Check if any ball is moving."""
        return any(ball.is_moving() for ball in self.balls)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw table and components."""
        pygame.draw.rect(screen, settings.TABLE_FELT,
                        (settings.TABLE_MARGIN, settings.TABLE_MARGIN,
                         settings.TABLE_WIDTH, settings.TABLE_HEIGHT))

        pygame.draw.rect(screen, settings.TABLE_WOOD,
                        (settings.TABLE_MARGIN - 10, settings.TABLE_MARGIN - 10,
                         settings.TABLE_WIDTH + 20, settings.TABLE_HEIGHT + 20),
                        10)

        for pocket in self.pockets:
            pygame.draw.circle(screen, (0, 0, 0), pocket, settings.POCKET_RADIUS)

        for ball in self.balls:
            ball.draw(screen) 