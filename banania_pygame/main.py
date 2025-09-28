# main.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, UPS, Entity # Added Entity for mock level
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

    # CHANGED: Initialization order is important. Managers that provide resources
    # (Renderer, AudioManager) should be created before managers that use them (Game, UIManager).
    
    renderer = Renderer()
    audio_manager = AudioManager()
    
    # ADDED: Pass the renderer as the resource manager for the UI
    ui_manager = UIManager(renderer) 
    
    # Placeholder for external level data. You would load your levels here.
    # ADDED: A slightly more interesting mock level with a player character.
    mock_level_data = {
        1: [[Entity.EMPTY for _ in range(13)] for _ in range(21)]
    }
    # Place a player character for testing
    mock_level_data[1][10][6] = Entity.PLAYER_BERTI

    # CHANGED: Pass the audio_manager instance to the Game object.
    game = Game(mock_level_data, audio_manager)
    game.load_level(1) # Load the initial level

    input_handler = InputHandler()
    
    # Mark the game as initialized to move past any potential loading screen logic
    game.is_initialized = True

    # --- Main Game Loop ---
    is_running = True
    while is_running:
        # 1. Process Input
        # ADDED: The game state dictionary required by the UI Manager
        game_state = {
            'paused': game.is_paused,
            'sound_on': audio_manager.sound_enabled,
            'volume': audio_manager.volume,
            # Placeholder for button activation logic (e.g., can go to prev/next level)
            'buttons_activated': [game.level_number > 1, True, game.level_number < 50] 
        }
        
        # CHANGED: Pass the game_state to the input handler for context
        input_handler.process_events(ui_manager, game_state)
        if input_handler.quit_requested:
            is_running = False

        # 2. Update Game Logic
        game.update(input_handler)
        
        # ADDED: Animation state should be updated with game logic, not rendering.
        renderer.update_all_animations(game)
        
        # ADDED: Update UI components (e.g., for blinking cursors in text fields)
        # We pass clock.get_time() which is the delta time in milliseconds
        ui_manager.update(clock.get_time(), game_state)

        # 3. Render Graphics
        # CHANGED: The rendering call now correctly uses the 'draw' method
        # and separates game rendering from UI rendering.
        
        # Step 3a: Draw the game world (background, characters, items)
        renderer.draw(screen, game)
        
        # Step 3b: Draw the UI elements on top of the game world
        ui_manager.draw_all(screen, game_state)

        # 4. Update the display and control framerate
        pygame.display.flip()
        clock.tick(UPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()