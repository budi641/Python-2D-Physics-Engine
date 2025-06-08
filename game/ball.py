import pygame
import numpy as np
from typing import Tuple, Optional
from physics.body import RigidBody
import settings

class Ball(RigidBody):
    def __init__(self, number: int, pos: Tuple[float, float], is_cue_ball: bool = False):
        super().__init__(
            pos=pos,
            radius=settings.BALL_RADIUS,
            mass=settings.BALL_MASS,
            restitution=settings.BALL_RESTITUTION,
            friction=settings.BALL_FRICTION
        )
        self.number = number
        self.is_cue_ball = is_cue_ball
        self.in_pocket = False
        self.color = settings.BALL_COLORS[number]
        
        size = settings.BALL_RADIUS * 2
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        self._draw_ball()

    def _draw_ball(self) -> None:
        """Draw ball on surface."""
        center = settings.BALL_RADIUS
        radius = settings.BALL_RADIUS

        pygame.draw.circle(self.surface, self.color, (center, center), radius)

        if not self.is_cue_ball:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.number), True, (255, 255, 255))
            text_rect = text.get_rect(center=(center, center))
            
            shadow = font.render(str(self.number), True, (0, 0, 0))
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            self.surface.blit(shadow, shadow_rect)
            self.surface.blit(text, text_rect)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw ball on screen."""
        if self.in_pocket:
            return
            
        screen_x = int(self.pos[0] - settings.BALL_RADIUS)
        screen_y = int(self.pos[1] - settings.BALL_RADIUS)
        screen.blit(self.surface, (screen_x, screen_y))

    def is_moving(self, threshold: float = 0.1) -> bool:
        """Check if ball is moving."""
        return np.linalg.norm(self.vel) > threshold

    def reset(self, pos: Optional[Tuple[float, float]] = None) -> None:
        """Reset ball state."""
        if pos is None:
            pos = (settings.CUE_BALL_POS if self.is_cue_ball
                  else settings.RACK_POS)
        self.pos = np.array(pos, dtype=float)
        self.prev_pos = self.pos.copy()
        self.vel = np.zeros(2, dtype=float)
        self.force = np.zeros(2, dtype=float)
        self.in_pocket = False 