# main.py
import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, UPS, Entity, ErrorCode, DialogBox as DialogBoxType
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

    # CORRECTED ORDER: Game logic must be created before the UI that needs to call it.
    
    renderer = Renderer()
    audio_manager = AudioManager()
    
    # Create mock level data
    mock_level_data = {
        1: [[Entity.EMPTY for _ in range(13)] for _ in range(21)]
    }
    mock_level_data[1][10][6] = Entity.PLAYER_BERTI

    # 1. Create the Game instance FIRST
    game = Game(mock_level_data, audio_manager)

    # 2. Create the dictionary of callbacks for the UI Manager
    # This acts as a bridge, allowing the UI to safely interact with the game engine.
    game_logic_callbacks = {
        # State getters
        'get_state': game.get_state,
        'get_full_state': game.get_full_state,
        'get_charts_data': game.get_charts_data,
        
        # Action performers
        'new': game.new_game_action,
        'save': game.save_game_action,
        'load': game.load_game_action,
        'change_password': game.change_password_action,
        'toggle_pause': game.toggle_pause,
        'toggle_sound': game.toggle_sound,
        'toggle_single_steps': game.toggle_single_steps,
        # This special callback tells the UI to open the save dialog first,
        # and if that save is successful, to then trigger a new game.
        # We define a small helper function here to orchestrate this.
        'save_and_new': None # This will be set after ui_manager is created.
    }

    # 3. Create the UI Manager, passing in the callbacks
    ui_manager = UIManager(renderer, game_logic_callbacks)
    
    # Now, define the save_and_new callback which needs a reference to ui_manager
    def save_and_new_flow():
        # Define what happens when the save dialog's "OK" is successful
        def on_save_success(username, password):
            result = game.save_game_action(username, password)
            if result == ErrorCode.SUCCESS:
                game.new_game_action() # Trigger new game after successful save
            return result
        # Show the save dialog and pass our custom success handler to it
        ui_manager.active_dialog = UIManager.SaveLoadDialog(
            renderer, ui_manager, "Save game", on_save_success
        )
    # Assign the fully defined flow to the callback dictionary
    game_logic_callbacks['save_and_new'] = save_and_new_flow


    # Load initial level and create input handler
    game.load_level(1)
    input_handler = InputHandler()
    game.is_initialized = True

    # --- Main Game Loop ---
    is_running = True
    while is_running:
        # 1. Process Input
        # We now get the state directly from the game object via the callback
        game_state = game.get_full_state()
        
        input_handler.process_events(ui_manager)
        if input_handler.quit_requested:
            is_running = False

        # 2. Update Game Logic
        game.update(input_handler)
        renderer.update_all_animations(game)
        
        # Pass delta time (in ms) to UI for animations like blinking cursors
        ui_manager.update(clock.get_time())

        # 3. Render Graphics
        renderer.draw(screen, game)
        ui_manager.draw_all(screen)

        # 4. Update display and control framerate
        pygame.display.flip()
        clock.tick(UPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()