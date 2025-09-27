# main.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_engine import Game
from renderer import Renderer
from input_handler import InputHandler
from audio_manager import AudioManager
from ui_manager import UIManager

def main():
    """The main function to run the game."""
    pygame.init()
    
    # Setup the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Berti - Python Edition")
    clock = pygame.time.Clock()

    # --- Initialize all game components ---
    # Placeholder for external level data. You would load your levels here.
    # For now, a simple empty level.
    mock_level_data = {
        0: [[0 for _ in range(13)] for _ in range(21)]
    }
    
    game = Game(mock_level_data)
    renderer = Renderer()
    input_handler = InputHandler()
    audio_manager = AudioManager()
    ui_manager = UIManager()
    
    # Mark the game as initialized to move past the loading screen
    game.is_initialized = True

    # --- Main Game Loop ---
    is_running = True
    while is_running:
        # 1. Process Input
        input_handler.process_events(ui_manager)
        if input_handler.quit_requested:
            is_running = False

        # 2. Update Game Logic
        game.update(input_handler)
        
        # 3. Render Graphics
        renderer.render(screen, game, ui_manager)

        # 4. Update the display and control framerate
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()