# input_handler.py
import pygame
from config import Direction

class InputHandler:
    """Manages all user input from keyboard and mouse."""
    def __init__(self):
        self.direction = Direction.NONE
        self.mouse_pos = (0, 0)
        self.mouse_pressed = [False, False, False] # Left, Middle, Right
        self.quit_requested = False
        
        # Mapping keyboard keys to directions
        self.key_map = {
            pygame.K_UP: Direction.UP,
            pygame.K_w: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_s: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_a: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_d: Direction.RIGHT,
        }

    def process_events(self, ui_manager):
        """
        Process the Pygame event queue.
        This should be called once per frame in the main game loop.
        """
        # Reset per-frame state
        self.direction = Direction.NONE
        
        events = pygame.event.get()

        # First, let the UI manager process events to see if it consumes them
        # (e.g., clicking a button in a dialog box)
        ui_consumed_event = ui_manager.handle_events(events)

        if ui_consumed_event:
            return

        # If UI didn't consume events, process them for gameplay
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_requested = True
            
            # --- Mouse Tracking ---
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = [False, False, False]

        # --- Keyboard (State-based for continuous movement) ---
        keys = pygame.key.get_pressed()
        
        # Check directions (add more keys as needed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = Direction.UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = Direction.DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = Direction.LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = Direction.RIGHT
            
    def get_direction(self):
        """Returns the current direction pressed by the player."""
        return self.direction