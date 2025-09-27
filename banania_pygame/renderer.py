# renderer.py
import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LEV_OFFSET_X, LEV_OFFSET_Y, 
    LEV_DIMENSION_X, LEV_DIMENSION_Y, TILE_SIZE, Colors, Entity
)

class Renderer:
    """
    Handles all drawing to the screen. This is the Python/Pygame equivalent
    of the CLASS_visual and the global render_* functions in JavaScript.
    """
    def __init__(self):
        # A dictionary to hold all loaded images (Pygame surfaces)
        self.images = {}
        self.font_big = pygame.font.SysFont("Helvetica", 36)
        self.font_small = pygame.font.SysFont("Helvetica", 12)
        self.load_assets()

    def load_assets(self):
        """Load all game images into memory."""
        # This is a placeholder. You would load all your game sprites here.
        # Example: self.images['background'] = pygame.image.load('assets/background.png').convert()
        # For now, we'll create placeholder surfaces.
        try:
            self.images['background'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.images['background'].fill(Colors.DARK_GREY)
            
            self.images[Entity.PLAYER_BERTI] = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.images[Entity.PLAYER_BERTI].fill(Colors.BLUE)
            
            self.images[Entity.PURPLE_MONSTER] = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.images[Entity.PURPLE_MONSTER].fill((128, 0, 128)) # Purple
            
            self.images[Entity.BANANA_PEEL] = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.images[Entity.BANANA_PEEL].fill((255, 255, 0)) # Yellow
            
            print("Assets loaded.")
        except Exception as e:
            print(f"Error loading assets: {e}. Placeholders will be used.")

    def render(self, surface, game, ui_manager):
        """The main drawing function, called every frame."""
        
        # 1. Draw background
        surface.blit(self.images.get('background', pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))), (0, 0))
        
        # 2. Draw game state
        if not game.is_initialized:
            self.draw_loading_screen(surface)
        elif game.mode == 'entry':
            self.draw_title_screen(surface)
        elif game.mode == 'play':
            self.draw_game_field(surface, game.level_array)
            self.draw_hud(surface, game)
        elif game.mode == 'won':
            self.draw_end_screen(surface)
        
        # 3. Draw UI on top of everything
        ui_manager.draw_volume_bar(surface, 0.7, True) # Example call
        ui_manager.draw(surface)

    def draw_loading_screen(self, surface):
        surface.fill(Colors.LIGHT_GREY)
        text_surf = self.font_big.render("Loading...", True, Colors.BLACK)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        surface.blit(text_surf, text_rect)
        
    def draw_title_screen(self, surface):
        # In a real game, you'd blit a title image
        surface.fill(Colors.BLACK)
        text_surf = self.font_big.render("Berti the Banana Collector", True, Colors.YELLOW)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        surface.blit(text_surf, text_rect)

    def draw_end_screen(self, surface):
        surface.fill(Colors.BLUE)
        text_surf = self.font_big.render("You Won!", True, Colors.WHITE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        surface.blit(text_surf, text_rect)

    def draw_hud(self, surface, game):
        """Draws the Head-Up Display (steps, level number, etc.)."""
        # This function replicates render_displays from the JS code
        steps_text = self.font_small.render(f"Steps: {game.steps_taken}", True, Colors.WHITE)
        level_text = self.font_small.render(f"Level: {game.level_number}", True, Colors.WHITE)
        surface.blit(steps_text, (30, 45))
        surface.blit(level_text, (450, 45))

    def draw_game_field(self, surface, level_array):
        """
        Renders the entire grid of entities.
        This function replaces the complex `render_field` and `render_block` from JS.
        """
        for y in range(LEV_DIMENSION_Y):
            for x in range(LEV_DIMENSION_X):
                entity = level_array[x][y]
                if entity.id == Entity.EMPTY:
                    continue

                # Calculate the final draw position including the tweening offset
                draw_x = LEV_OFFSET_X + x * TILE_SIZE + entity.moving_offset.x
                draw_y = LEV_OFFSET_Y + y * TILE_SIZE + entity.moving_offset.y
                
                # Get the correct image for the entity
                # The animation logic from render_block would go here, selecting the
                # correct sprite from a spritesheet based on `entity.animation_frame`
                entity_image = self.images.get(entity.id)
                
                if entity_image:
                    surface.blit(entity_image, (draw_x, draw_y))
                else: # Fallback for unloaded images
                    pygame.draw.rect(surface, Colors.RED, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))