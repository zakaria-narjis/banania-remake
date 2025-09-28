# renderer.py
import pygame
import os
import math # Needed for floor

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, LEV_OFFSET_X, LEV_OFFSET_Y,
    LEV_DIMENSION_X, LEV_DIMENSION_Y, Entity, ImageID, IMAGE_DIR, Direction
)

# Constants for rendering logic, mirroring the JS implementation
TILE_SIZE = 24 # The JS version uses 24x24 tiles
ANIMATION_DURATION_MS = 100 # Time in ms for one animation frame

class Renderer:
    """
    Handles all drawing to the screen. This class is a Python/Pygame port
    of the rendering logic found in the original rendering_and_others.js,
    including CLASS_visual, render_field, and render_block functions.
    """
    def __init__(self):
        # A dictionary to hold all loaded images (Pygame surfaces)
        self.images = {}
        # Pygame fonts for any HUD/debug text
        self.font_big = pygame.font.SysFont("Tahoma", 24)
        self.font_small = pygame.font.SysFont("Tahoma", 12)

        # Animation sequence lengths (in frames)
        self.ANIM_LENGTH = 4

        # Offsets for pop-up images
        self.offset_wow_x = -20
        self.offset_wow_y = -44
        self.offset_yeah_x = -20
        self.offset_yeah_y = -44
        self.offset_argl_x = -20
        self.offset_argl_y = -44

        # --- Animation State Lookups ---
        # These lists map Direction enum to the starting ImageID for an animation.
        # This replaces the faulty logic in the original _get_animation_start_frame.
        # Order must match the Direction enum: UP(0), LEFT(1), DOWN(2), RIGHT(3)
        self.BERTI_WALK_STARTS = [
            ImageID.BERTI_WALK_UP_0, ImageID.BERTI_WALK_LEFT_0,
            ImageID.BERTI_WALK_DOWN_0, ImageID.BERTI_WALK_RIGHT_0
        ]
        self.BERTI_PUSH_STARTS = [
            ImageID.BERTI_PUSH_UP_0, ImageID.BERTI_PUSH_LEFT_0,
            ImageID.BERTI_PUSH_DOWN_0, ImageID.BERTI_PUSH_RIGHT_0
        ]
        self.PURPLE_MONSTER_WALK_STARTS = [
            ImageID.PURPMON_WALK_UP_0, ImageID.PURPMON_WALK_LEFT_0,
            ImageID.PURPMON_WALK_DOWN_0, ImageID.PURPMON_WALK_RIGHT_0
        ]
        self.PURPLE_MONSTER_PUSH_STARTS = [
            ImageID.PURPMON_PUSH_UP_0, ImageID.PURPMON_PUSH_LEFT_0,
            ImageID.PURPMON_PUSH_DOWN_0, ImageID.PURPMON_PUSH_RIGHT_0
        ]
        self.GREEN_MONSTER_WALK_STARTS = [
            ImageID.GREENMON_WALK_UP_0, ImageID.GREENMON_WALK_LEFT_0,
            ImageID.GREENMON_WALK_DOWN_0, ImageID.GREENMON_WALK_RIGHT_0
        ]

        # --- Asset Loading ---
        self.load_assets()


    def _load_image(self, filename):
        """Loads a single Pygame image surface, handling transparency."""
        try:
            path = os.path.join(IMAGE_DIR, filename)
            return pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image '{filename}': {e}")
            error_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            error_surface.fill((255, 0, 255)) # Magenta for missing textures
            return error_surface


    def load_assets(self):
        """
        Loads all game images, matching the complete asset list from the JS source.
        This includes game entities, UI elements, items, and dialog boxes.
        The ImageID enum in config.py must be updated to match these additions.
        """
        # --- Single-Frame and UI Assets ---
        # Corresponds to images[0], [1], [167-184] etc. in the JS
# renderer.py

# ... inside the Renderer class, in the load_assets method ...
        # --- Single-Frame and UI Assets ---
        # Corresponds to images[0], [1], [167-184] etc. in the JS
        simple_assets = {
            ImageID.BACKGROUND: "background.png",
            ImageID.TITLESCREEN: "entry.png",
            ImageID.ENDSCREEN: "exit.png",
            ImageID.FOOTSTEPS: "garbage_0.png", # Placeholder, assumes garbage_0 is footsteps
            ImageID.LADDER: "garbage_1.png", # Placeholder, assumes garbage_1 is ladder
            ImageID.ARGL: "argl.png",
            ImageID.WOW: "wow.png",
            ImageID.YEAH: "yeah.png",
            ImageID.CHECKBOX_CHECKED: "check_b.png", # Renamed from CHECK_B
            ImageID.CHECKBOX_UNCHECKED: "check_w.png", # Renamed from CHECK_W
            ImageID.DIALOGBOX_CONFIRM: "dbx_confirm.png",
            ImageID.DIALOGBOX_SAVELOAD: "dbx_saveload.png",
            ImageID.DIALOGBOX_LOADLVL: "dbx_loadlvl.png",
            ImageID.DIALOGBOX_CHARTS: "dbx_charts.png",
            ImageID.BTN_CANCEL_UP: "btn_c-up.png",
            ImageID.BTN_CANCEL_DOWN: "btn_c-down.png",
            ImageID.BTN_NO_UP: "btn_n-up.png",
            ImageID.BTN_NO_DOWN: "btn_n-down.png",
            ImageID.BTN_OK_UP: "btn_o-up.png",
            ImageID.BTN_OK_DOWN: "btn_o-down.png",
            ImageID.BTN_YES_UP: "btn_y-up.png",
            ImageID.BTN_YES_DOWN: "btn_y-down.png",
            
            # --- ADDED THIS BLOCK TO FIX THE CRASH ---
            ImageID.BTN_PREV_UP: "userbutton_0-1.png",
            ImageID.BTN_PREV_DOWN: "userbutton_1-1.png",
            ImageID.BTN_PREV_DISABLED: "userbutton_2-1.png",
            ImageID.BTN_BERTI_UP: "userbutton_0-0.png",
            ImageID.BTN_BERTI_DOWN: "userbutton_1-0.png",
            ImageID.BTN_BERTI_BLINK_UP: "userbutton_2-0.png",
            ImageID.BTN_NEXT_UP: "userbutton_0-2.png",
            ImageID.BTN_NEXT_DOWN: "userbutton_1-2.png",
            ImageID.BTN_NEXT_DISABLED: "userbutton_2-2.png",
            # -----------------------------------------
        }
        for img_id, filename in simple_assets.items():
            self.images[img_id] = self._load_image(filename)

        # --- Sequentially Named Assets ---
        # NOTE: JS starts garbage at index 2, but config.py doesn't have a start enum.
        # This assumes your final asset pack might differ slightly.
        # This code will correctly load garbage_0.png to garbage_8.png into sequential ImageIDs
        # You will need to add a GARBAGE_START enum to config.py for this to work.
        # For now, this is commented out to prevent errors.
        # for i in range(9): self.images[ImageID.GARBAGE_START + i] = self._load_image(f"garbage_{i}.png")
        
        for i in range(11): self.images[ImageID.DIGIT_0 + i] = self._load_image(f"digits_{i}.png")
        # Same as garbage, needs a STONE_START enum
        # for i in range(9): self.images[ImageID.STONE_START + i] = self._load_image(f"stone_{i}.png")

        # --- Multi-Indexed Assets (Loops) ---
        # This requires a USERBUTTON_START enum
        # for i in range(3):
        #     for j in range(3): self.images[ImageID.USERBUTTON_START + (3 * i) + j] = self._load_image(f"userbutton_{i}-{j}.png")
        
        door_types, door_frames = 6, 3
        for i in range(door_types):
            for j in range(door_frames): self.images[ImageID.DOOR_1_CLOSED + (i * door_frames) + j] = self._load_image(f"doors_{j}-{i}.png")

        # Corrected loading loops for animated characters
        # The logic relies on the enums in config.py being contiguous integers.
        player_anim_types, directions = 13, 4
        for i in range(player_anim_types):
            for j in range(directions):
                # The key is calculated from the base enum value plus an offset
                key = ImageID.BERTI_IDLE + (i * directions) + j
                self.images[key] = self._load_image(f"player_{j}-{i}.png")

        monster1_anim_types, directions = 9, 4
        for i in range(monster1_anim_types):
            for j in range(directions):
                key = ImageID.PURPMON_STUCK_0 + (i * directions) + j
                self.images[key] = self._load_image(f"monster1_{j}-{i}.png")

        monster2_anim_types, directions = 5, 4
        for i in range(monster2_anim_types):
            for j in range(directions):
                key = ImageID.GREENMON_STUCK_0 + (i * directions) + j
                self.images[key] = self._load_image(f"monster2_{j}-{i}.png")


    def _get_animation_start_frame(self, block):
        """Helper to determine the base frame ID for an entity's current state."""
        # Player Animation Logic
        if block.id == Entity.PLAYER_BERTI:
            if block.is_moving:
                base_list = self.BERTI_PUSH_STARTS if block.is_pushing else self.BERTI_WALK_STARTS
                return base_list[block.face_dir]
            else:
                # Player idle state is not animated
                return ImageID.BERTI_IDLE
        
        # Purple Monster Animation Logic
        elif block.id == Entity.PURPLE_MONSTER:
            if block.is_moving:
                base_list = self.PURPLE_MONSTER_PUSH_STARTS if block.is_pushing else self.PURPLE_MONSTER_WALK_STARTS
                return base_list[block.face_dir]
            else:
                # Monster idle ("stuck") state is a 4-frame animation
                return ImageID.PURPMON_STUCK_0

        # Green Monster Animation Logic
        elif block.id == Entity.GREEN_MONSTER:
            if block.is_moving:
                # Green monster does not have a push animation
                return self.GREEN_MONSTER_WALK_STARTS[block.face_dir]
            else:
                # Monster idle ("stuck") state is a 4-frame animation
                return ImageID.GREENMON_STUCK_0
        
        return -1

    def update_animation(self, game, x, y):
        """Updates the animation frame for a single entity based on its state."""
        block = game.level_array[x][y]
        
        # Handle static states (win/loss) first for the player
        if block.id == Entity.PLAYER_BERTI:
            if game.level_ended == 1:
                block.animation_frame = ImageID.BERTI_CELEBRATING
                return
            elif game.level_ended == 2:
                block.animation_frame = ImageID.BERTI_DEAD
                return
        
        # Determine the correct animation strip for the entity's current state
        start_id = self._get_animation_start_frame(block)
        
        # Exit if not an animated character or in a non-animated state (like Berti's idle)
        if start_id == -1 or (block.id == Entity.PLAYER_BERTI and not block.is_moving):
            block.animation_frame = start_id if start_id != -1 else block.animation_frame
            return

        # Determine if it's time to advance the animation frame
        advance_frame = False
        current_time_ms = pygame.time.get_ticks()
        if not hasattr(block, 'last_anim_time'):
            block.last_anim_time = 0
            
        if current_time_ms - block.last_anim_time > ANIMATION_DURATION_MS:
            advance_frame = True
            block.last_anim_time = current_time_ms
        
        # If the character's state has changed, reset the animation to the new strip
        if not hasattr(block, 'anim_index') or block.animation_frame < start_id or block.animation_frame >= start_id + self.ANIM_LENGTH:
            block.animation_frame = start_id
            block.anim_index = 0
        # Otherwise, advance the frame if it's time
        elif advance_frame:
            block.anim_index = (block.anim_index + 1) % self.ANIM_LENGTH
            block.animation_frame = start_id + block.anim_index

    def update_all_animations(self, game):
        """Iterates through all entities and updates their animations."""
        for y in range(LEV_DIMENSION_Y):
            for x in range(LEV_DIMENSION_X):
                # Ensure the block is an entity that needs animation updates
                if hasattr(game.level_array[x][y], 'id'):
                    self.update_animation(game, x, y)


    def draw_block(self, surface, block, x_grid, y_grid):
        """Draws a single game entity."""
        # Ensure block has an animation frame to draw
        if not hasattr(block, 'animation_frame'): return

        image = self.images.get(block.animation_frame)
        if not image: return

        # Get visual offsets for smooth movement and static adjustments
        offset_x = block.moving_offset.x + block.fine_offset_x
        offset_y = block.moving_offset.y + block.fine_offset_y
        x_pos = LEV_OFFSET_X + x_grid * TILE_SIZE + offset_x
        y_pos = LEV_OFFSET_Y + y_grid * TILE_SIZE + offset_y
        
        surface.blit(image, (x_pos, y_pos))

    def draw_level_entities(self, surface, game):
        """Draws the game entities, replicating the JS `render_field` Z-ordering logic."""
        # This layered rendering ensures characters appear behind objects when moving north
        for is_consumable_pass in [True, False]:
            for y in range(LEV_DIMENSION_Y):
                for x in range(LEV_DIMENSION_X):
                    block = game.level_array[x][y]
                    # Check if block has 'consumable' attr before accessing
                    if hasattr(block, 'consumable') and block.consumable == is_consumable_pass:
                        self.draw_block(surface, block, x, y)
        
        # Draw Popups on top (e.g., "WOW!", "ARGL!") after all entities
        if game.level_ended > 0 and hasattr(game, 'player_positions'):
            for p_pos in game.player_positions:
                player_block = game.level_array[p_pos['x']][p_pos['y']]
                x_pos = LEV_OFFSET_X + p_pos['x'] * TILE_SIZE + player_block.moving_offset.x
                y_pos = LEV_OFFSET_Y + p_pos['y'] * TILE_SIZE + player_block.moving_offset.y
                
                popup_img, offset_x, offset_y = None, 0, 0

                if game.level_ended == 1: # Won
                    popup_id = ImageID.WOW if hasattr(game, 'wow') and game.wow else ImageID.YEAH
                    popup_img = self.images.get(popup_id)
                    offset_x, offset_y = (self.offset_wow_x, self.offset_wow_y) if popup_id == ImageID.WOW else (self.offset_yeah_x, self.offset_yeah_y)
                
                elif game.level_ended == 2: # Died
                    popup_img = self.images.get(ImageID.ARGL)
                    offset_x, offset_y = self.offset_argl_x, self.offset_argl_y

                if popup_img:
                    surface.blit(popup_img, (x_pos + offset_x, y_pos + offset_y))

    def draw(self, surface, game):
        """The main drawing function, called every frame."""
        # Always draw the base background
        surface.blit(self.images.get(ImageID.BACKGROUND), (0, 0))

        # Mode 0: Title Screen
        if game.mode == 0:
            title_img = self.images.get(ImageID.TITLESCREEN)
            if title_img:
                # Center the title image within the level area
                x = LEV_OFFSET_X + (TILE_SIZE * LEV_DIMENSION_X - title_img.get_width()) / 2
                y = LEV_OFFSET_Y + (TILE_SIZE * LEV_DIMENSION_Y - title_img.get_height()) / 2
                surface.blit(title_img, (x, y))

        # Mode 1: Main Game
        elif game.mode == 1:
            # Draw static UI elements like footsteps and ladder
            surface.blit(self.images.get(ImageID.FOOTSTEPS), (22, 41))
            surface.blit(self.images.get(ImageID.LADDER), (427, 41))
            
            # Draw all the dynamic game entities
            self.draw_level_entities(surface, game)

            # NOTE: HUD elements like score, buttons, etc., would be drawn here
            
        # Mode 2: End Screen
        elif game.mode == 2:
            end_img = self.images.get(ImageID.ENDSCREEN)
            if end_img:
                x = LEV_OFFSET_X + (TILE_SIZE * LEV_DIMENSION_X - end_img.get_width()) / 2
                y = LEV_OFFSET_Y + (TILE_SIZE * LEV_DIMENSION_Y - end_img.get_height()) / 2
                surface.blit(end_img, (x, y))
                
    def get_image(self, image_id):
        """Helper to allow other managers to access loaded images."""
        return self.images.get(image_id)