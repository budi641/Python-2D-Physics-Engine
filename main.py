import pygame
import sys
from physics.world import PhysicsWorld
from game.table import Table
from game.cue import Cue
import settings

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption("8-Ball Pool")
        self.clock = pygame.time.Clock()
        
        self.world = PhysicsWorld(gravity=settings.GRAVITY, dt=settings.TIME_STEP)
        self.table = Table(self.world)
        self.cue = Cue(self.table.balls[0])
        
        self.running = True
        self.paused = False

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset_game()

    def reset_game(self):
        """Reset game state."""
        self.world.bodies.clear()
        self.world.static_lines.clear()
        self.table = Table(self.world)
        self.cue = Cue(self.table.balls[0])

    def update(self):
        """Update game state."""
        if self.paused:
            return

        self.world.step()
        pocketed_balls = self.table.check_pockets()
        if pocketed_balls:
            pass

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        self.cue.update(mouse_pos, mouse_buttons)

    def draw(self):
        """Draw game state."""
        self.screen.fill(settings.BLACK)
        
        self.table.draw(self.screen)
        self.cue.draw(self.screen)
        self.world.particle_system.draw(self.screen)
        
        if self.paused:
            font = pygame.font.Font(None, 74)
            text = font.render('PAUSED', True, settings.WHITE)
            text_rect = text.get_rect(center=(settings.WINDOW_WIDTH/2, settings.WINDOW_HEIGHT/2))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 