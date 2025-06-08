import pygame
import numpy as np
from typing import Tuple, Optional
from .ball import Ball
import settings

class Cue:
    def __init__(self, cue_ball: Ball):
        self.cue_ball = cue_ball
        self.angle = 0.0
        self.power = 0.0
        self.max_power = settings.MAX_POWER
        self.is_aiming = False
        self.is_shooting = False
        self.power_direction = 1
        self.min_distance = settings.BALL_RADIUS * 2
        self.trajectory_mode = 'solid'

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                self.trajectory_mode = 'dashed' if self.trajectory_mode == 'solid' else 'solid'

    def update(self, mouse_pos: Tuple[int, int], mouse_buttons: Tuple[bool, bool, bool]) -> None:
        """Update cue state."""
        if self.cue_ball.is_moving():
            self.is_aiming = False
            self.is_shooting = False
            return

        dx = mouse_pos[0] - self.cue_ball.pos[0]
        dy = mouse_pos[1] - self.cue_ball.pos[1]
        self.angle = np.arctan2(dy, dx)

        if mouse_buttons[0]:
            if not self.is_shooting:
                self.is_shooting = True
                self.power = 0
            else:
                self.power += settings.POWER_SCALE * self.max_power / 7
                if self.power > self.max_power:
                    self.power = self.max_power
        else:
            if self.is_shooting:
                self.shoot()
            self.is_shooting = False
            self.is_aiming = True

    def shoot(self) -> None:
        """Apply force to cue ball."""
        if not self.is_shooting or self.cue_ball.is_moving():
            return

        force = np.array([
            -np.cos(self.angle),
            -np.sin(self.angle)
        ]) * self.power

        self.cue_ball.apply_impulse(force)

    def draw(self, screen: pygame.Surface) -> None:
        if not self.is_aiming and not self.is_shooting:
            return
        start_pos = self.cue_ball.pos
        direction = np.array([np.cos(self.angle), np.sin(self.angle)])
        cue_length = settings.CUE_LENGTH + (self.power / self.max_power) * 100
        cue_end = start_pos + direction * cue_length
        pygame.draw.line(screen, settings.CUE_COLOR,
                        (int(start_pos[0]), int(start_pos[1])),
                        (int(cue_end[0]), int(cue_end[1])),
                        settings.CUE_WIDTH)
        traj_start = start_pos - direction * (settings.BALL_RADIUS + 10)
        traj_end = traj_start - direction * 300
        if self.trajectory_mode == 'solid':
            pygame.draw.line(screen, (0, 255, 255),
                             (int(traj_start[0]), int(traj_start[1])),
                             (int(traj_end[0]), int(traj_end[1])), 3)
        else:
            self._draw_dashed_line(screen, (0, 255, 255), traj_start, traj_end, dash_length=20, gap_length=15, width=3)
        if self.is_shooting:
            self._draw_power_meter(screen)

    def _draw_dashed_line(self, screen, color, start, end, dash_length=10, gap_length=10, width=1):
        start = np.array(start)
        end = np.array(end)
        direction = end - start
        length = np.linalg.norm(direction)
        if length == 0:
            return
        direction = direction / length
        num_dashes = int(length // (dash_length + gap_length))
        for i in range(num_dashes + 1):
            seg_start = start + direction * (i * (dash_length + gap_length))
            seg_end = seg_start + direction * dash_length
            if np.linalg.norm(seg_end - start) > length:
                seg_end = end
            pygame.draw.line(screen, color, seg_start, seg_end, width)

    def _draw_power_meter(self, screen: pygame.Surface) -> None:
        """Draw power meter."""
        power_height = 30
        power_width = 200
        power_x = 20
        power_y = settings.WINDOW_HEIGHT - power_height - 20
        
        pygame.draw.rect(screen, (50, 50, 50),
                        (power_x, power_y, power_width, power_height))
        
        power_level = (self.power / self.max_power) * power_width
        for i in range(int(power_level)):
            alpha = int(255 * (i / power_level))
            color = (255, int(255 * (1 - i / power_level)), 0, alpha)
            pygame.draw.line(screen, color,
                           (power_x + i, power_y),
                           (power_x + i, power_y + power_height),
                           1)
        
        pygame.draw.rect(screen, (200, 200, 200),
                        (power_x, power_y, power_width, power_height),
                        2) 