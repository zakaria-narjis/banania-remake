# game_engine.py
import random
import config
from entities import (
    Entity, Player, PurpleMonster, GreenMonster, LightBlock, HeavyBlock, 
    PinnedBlock, Banana, Key, Door, Empty, Dummy, Vec
)
from config import ErrorCode, ImageID # Import ErrorCode and ImageID

# You'll likely want a dedicated class to handle saving/loading.
# For now, we can stub it out.
class SaveGameManager:
    def __init__(self):
        # In a real implementation, you would load user data here,
        # perhaps from a JSON file.
        self.username = None
        self.reached_level = 1
        self.arr_steps = {i: 0 for i in range(1, 51)}
        self.progressed = False

    def save_game(self):
        print("Saving game...")
        self.progressed = False
    
    def load_game(self, username, password):
        print(f"Loading game for {username}...")
        return True # Placeholder for success

class Game:
    """
    Manages the core game logic, state, and entity interactions.
    This is the Python equivalent of the JavaScript `CLASS_game`.
    """
    def __init__(self, level_data, audio_manager):
        # --- Game State ---
        self.is_paused = False
        self.is_initialized = False
        self.wait_timer = config.INTRO_DURATION * config.UPS
        self.mode = 0 # CHANGED: Was 'entry'. 0=Title, 1=Game, 2=End
        self.level_ended = 0 # 0: ongoing, 1: won, 2: lost
 
        # --- Level Data ---
        self.external_level_data = level_data # From EXTERNAL_LEVELS
        self.level_number = 0
        self.level_array = [] # The 2D grid of entity objects
        self.berti_positions = [] # Quick access to player objects
        
        # --- Player & Level Stats ---
        self.steps_taken = 0
        self.num_bananas = 0
        self.bananas_remaining = 0

        # --- Input & Timing ---
        self.single_steps = True
        self.last_dir_pressed = config.Direction.NONE
        self.update_tick = 0
        self.move_speed = round(1 * 60 / config.UPS)
        self.door_removal_delay = round(8 * config.UPS / 60)

        # --- Systems ---
        self.audio_manager = audio_manager
        self.save_manager = SaveGameManager()
        self.completed_moves = []
    ## 1. Main Game Loop Method
    # =================================================================================
    
    def update(self, input_handler):
        """
        The main logic update, called once per frame from your main game loop.
        Equivalent to the global `update` and `update_entities` functions in JS.
        """
        if self.is_paused:
            return

        if self.wait_timer > 0:
            self.wait_timer -= 1
            return
            
        if self.level_ended != 0:
            if self.level_ended == 1: # Won
                self.next_level()
            elif self.level_ended == 2: # Lost
                self.reset_level()
            return

        self.update_tick += 1
        
        synced_move = (self.update_tick * 60 / config.UPS) % (12 / self.move_speed) == 0

        # --- Handle Inputs and AI Decisions FIRST ---
        # Player input
        for berti_pos in self.berti_positions:
            player = self.level_array[berti_pos.x][berti_pos.y]
            player.handle_input(self, input_handler, self.single_steps)
        
        # AI decisions
        for y in range(config.LEV_DIMENSION_Y):
            for x in range(config.LEV_DIMENSION_X):
                entity = self.level_array[x][y]
                if synced_move and isinstance(entity, (PurpleMonster, GreenMonster)):
                    entity.update_ai(self)
                
        # --- THEN, update ALL entity states and COLLECT completed moves ---
        self.completed_moves.clear() # Clear the list from the previous frame
        for y in range(config.LEV_DIMENSION_Y):
            for x in range(config.LEV_DIMENSION_X):
                entity = self.level_array[x][y]
                entity.update(self)

        # --- NOW, process all collected moves at once ---
        if self.completed_moves:
            self._process_completed_moves(self.completed_moves)

        # --- FINALLY, check for game over conditions ---
        for berti_pos in self.berti_positions:
            player = self.level_array[berti_pos.x][berti_pos.y]
            player.check_enemy_proximity(self)

    ## 2. Level Handling Methods
    # =================================================================================
    def load_level(self, level_num):
        """
        Initializes the game board from level data.
        Equivalent to `load_level` in JS.
        """
        self.level_number = level_num
        self.mode = 1
        self.level_array = [[Empty(x, y) for y in range(config.LEV_DIMENSION_Y)] for x in range(config.LEV_DIMENSION_X)]
        self.berti_positions = []
        self.steps_taken = 0
        self.num_bananas = 0
        self.level_ended = 0
        self.wait_timer = config.LEV_START_DELAY * config.UPS
        
        berti_counter = 0
        # Ensure level exists, otherwise load an empty one to prevent crashes
        if level_num >= len(self.external_level_data):
            print(f"Warning: Level {level_num} not found. Loading empty level.")
            level_map = [[config.Entity.EMPTY for _ in range(config.LEV_DIMENSION_Y)] for _ in range(config.LEV_DIMENSION_X)]
        else:
            level_map = self.external_level_data[level_num]

        for y in range(config.LEV_DIMENSION_Y):
            for x in range(config.LEV_DIMENSION_X):
                entity_id = level_map[x][y]

                if entity_id == config.Entity.PLAYER_BERTI:
                    self.level_array[x][y] = Player(x, y, berti_counter)
                    self.berti_positions.append(Vec(x, y))
                    berti_counter += 1
                elif entity_id == config.Entity.AUTO_BERTI:
                    self.level_array[x][y] = PurpleMonster(x, y)
                elif entity_id == config.Entity.BANANA_PEEL:
                    self.level_array[x][y] = Banana(x, y)
                    self.num_bananas += 1
                elif entity_id == config.Entity.PURPLE_MONSTER:
                    self.level_array[x][y] = PurpleMonster(x, y)
                elif entity_id == config.Entity.GREEN_MONSTER:
                    self.level_array[x][y] = GreenMonster(x, y)
                elif entity_id == config.Entity.PINNED_BLOCK:
                    self.level_array[x][y] = PinnedBlock(x, y)
                elif entity_id == config.Entity.LIGHT_BLOCK:
                    self.level_array[x][y] = LightBlock(x, y)
                elif entity_id == config.Entity.HEAVY_BLOCK:
                    self.level_array[x][y] = HeavyBlock(x, y)
                elif config.Entity.KEY_1 <= entity_id <= config.Entity.KEY_6:
                    key_type = entity_id - config.Entity.KEY_1 + 1
                    self.level_array[x][y] = Key(x, y, key_type)
                elif config.Entity.DOOR_1 <= entity_id <= config.Entity.DOOR_6:
                    door_type = entity_id - config.Entity.DOOR_1 + 1
                    self.level_array[x][y] = Door(x, y, door_type)
                else:
                    self.level_array[x][y] = Empty(x, y)
        
        self.bananas_remaining = self.num_bananas
        
        # *** ADD THIS CALL TO THE NEW METHOD ***
        self._initialize_entity_animations()

        print(f"Level {level_num} loaded. Bananas to collect: {self.bananas_remaining}")
    
    def _initialize_entity_animations(self):
        """
        Sets the initial animation_frame for all entities after level load.
        This is the Python port of the 'init_animation' function from the JS source.
        """
        # Offsets are from the JS 'visual' class
        offset_key_x, offset_key_y = 3, 4
        offset_banana_x, offset_banana_y = 4, 4
        
        for y in range(config.LEV_DIMENSION_Y):
            for x in range(config.LEV_DIMENSION_X):
                entity = self.level_array[x][y]
                
                # Using isinstance is more Pythonic and robust than checking entity.id
                if isinstance(entity, Player):
                    entity.animation_frame = ImageID.BERTI_IDLE
                elif isinstance(entity, PinnedBlock):
                    entity.animation_frame = ImageID.BLOCK_PINNED
                elif isinstance(entity, Banana):
                    entity.animation_frame = ImageID.BANANA_PEEL
                    entity.fine_offset_x = offset_banana_x
                    entity.fine_offset_y = offset_banana_y
                elif isinstance(entity, LightBlock):
                    entity.animation_frame = ImageID.BLOCK_LIGHT
                elif isinstance(entity, HeavyBlock):
                    entity.animation_frame = ImageID.BLOCK_HEAVY
                elif isinstance(entity, PurpleMonster):
                    entity.animation_frame = ImageID.PURPMON_STUCK_0
                elif isinstance(entity, GreenMonster):
                    entity.animation_frame = ImageID.GREENMON_STUCK_0
                elif isinstance(entity, Key):
                    # Key image IDs are sequential in the ImageID enum
                    entity.animation_frame = ImageID.KEY_1 + entity.key_type - 1
                    entity.fine_offset_x = offset_key_x
                    entity.fine_offset_y = offset_key_y
                elif isinstance(entity, Door):
                    # Door image IDs are sequential and grouped (closed, opening, fading)
                    entity.animation_frame = ImageID.DOOR_1_CLOSED + (entity.door_type - 1) * 3

    def next_level(self):
        if self.level_number >= 50:
            self.mode = 2 # Use 2 for won screen, as defined in __init__
            return
        self.load_level(self.level_number + 1)
    
    def reset_level(self):
        self.load_level(self.level_number)

    def end_level(self, won=False, caught=False):
        """Ends the current level with a win or loss condition."""
        if won:
            self.level_ended = 1
            self.audio_manager.play_sound('level_win')
        elif caught:
            self.level_ended = 2
            self.audio_manager.play_sound('player_caught')
        self.wait_timer = config.LEV_STOP_DELAY * config.UPS


    ## 3. Movement and Interaction Logic
    # =================================================================================

    def is_walkable(self, x, y, direction):
        """
        Checks if an entity at (x, y) can move in a given direction.
        This is the most complex and important rule function.
        Equivalent to `walkable` in JS.
        """
        dest = self.dir_to_coords(x, y, direction)
        
        if not self.is_in_bounds(dest.x, dest.y):
            return False

        entity_at_src = self.level_array[x][y]
        entity_at_dest = self.level_array[dest.x][dest.y]
        
        # Case 1: Destination is empty
        if isinstance(entity_at_dest, Empty):
            return True

        # Case 2: Destination is not empty but not moving
        if not entity_at_dest.is_moving:
            # Can consume items?
            if isinstance(entity_at_src, Player) and entity_at_dest.consumable:
                return True
            # Can push blocks?
            if entity_at_src.can_push and entity_at_dest.pushable:
                # Recursively check if the block can be pushed
                return self.is_walkable(dest.x, dest.y, direction)
        
        # Case 3: Destination is occupied by a moving entity
        else:
            # Complex logic from JS about two small entities moving past each other
            if (entity_at_dest.face_dir == direction) or \
               (entity_at_src.is_small and entity_at_dest.is_small):
                # Check if another entity is already targeting this destination tile
                # (This prevents multiple entities from moving to the same tile)
                # ...
                return True

        return False

    def start_move(self, x, y, direction):
        """
        Initiates the visual movement of an entity.
        Equivalent to `start_move` in JS.
        """
        entity = self.level_array[x][y]
        dest = self.dir_to_coords(x, y, direction)

        entity.is_moving = True
        entity.face_dir = direction
        
        if isinstance(entity, Player):
            self.steps_taken += 1

        dest_entity = self.level_array[dest.x][dest.y]
        
        # --- REVISED LOGIC ---
        # If the destination is empty, we mark it as a Dummy to reserve the spot.
        if isinstance(dest_entity, Empty):
             self.level_array[dest.x][dest.y] = Dummy(dest.x, dest.y)
        # If the destination is a consumable item (like a banana), do nothing.
        # The player will simply move onto it. The consumption logic is handled
        # in _process_completed_moves.
        elif dest_entity.consumable:
            pass # Allow movement onto the item
        # If the destination is not empty and not consumable, THEN try to push it.
        elif not dest_entity.is_moving:
             entity.is_pushing = True
             self.start_move(dest.x, dest.y, direction)


    def move(self, x, y, direction):
        """
        Finalizes a move action, updating the logical positions in the grid.
        Equivalent to `move` in JS.
        """
        src_entity = self.level_array[x][y]
        dest_pos = self.dir_to_coords(x, y, direction)

        # Reset source entity state
        src_entity.is_moving = False
        src_entity.moving_offset = Vec(0, 0)
        src_entity.is_pushing = False

        dest_entity = self.level_array[dest_pos.x][dest_pos.y]
        
        # Handle item consumption
        if isinstance(src_entity, Player) and dest_entity.consumable:
            if isinstance(dest_entity, Banana):
                self.bananas_remaining -= 1
                if self.bananas_remaining <= 0:
                    self.end_level(won=True)
            # ... handle keys and doors
        
        # Swap entities in the grid
        self.level_array[dest_pos.x][dest_pos.y] = src_entity
        self.level_array[x][y] = Empty(x, y) # The old spot is now empty

        # Update the entity's own internal coordinates to match its new grid position.
        src_entity.x, src_entity.y = dest_pos.x, dest_pos.y
        
        # Update Berti's position tracker if it was a player
        if isinstance(src_entity, Player):
            self.berti_positions[src_entity.berti_id] = dest_pos
    
    ## 4. AI and Utility Methods
    # =================================================================================
    def is_in_bounds(self, x, y):
        """Checks if coordinates are within the level grid."""
        return 0 <= x < config.LEV_DIMENSION_X and 0 <= y < config.LEV_DIMENSION_Y

    def dir_to_coords(self, x, y, direction):
        """Converts a position and direction into a new coordinate Vec."""
        if direction == config.Direction.UP: return Vec(x, y - 1)
        if direction == config.Direction.DOWN: return Vec(x, y + 1)
        if direction == config.Direction.LEFT: return Vec(x - 1, y)
        if direction == config.Direction.RIGHT: return Vec(x + 1, y)
        return Vec(x, y)

    def can_see_tile(self, eye_x, eye_y, tile_x, tile_y):
            """
            Line-of-sight algorithm for monster AI, ported from the original JS.
            Determines if there is a clear path between two tiles, ignoring small entities.
            """
            diff_x = tile_x - eye_x
            diff_y = tile_y - eye_y

            if diff_x == 0 and diff_y == 0:
                return True

            walk1_x, walk1_y, walk2_x, walk2_y = 0, 0, 0, 0
            
            if diff_x == 0:
                walk1_x, walk2_x = 0, 0
                walk1_y, walk2_y = 1 if diff_y > 0 else -1, 1 if diff_y > 0 else -1
            elif diff_x > 0:
                if diff_y == 0:
                    walk1_x, walk2_x = 1, 1
                    walk1_y, walk2_y = 0, 0
                elif diff_y > 0:
                    if diff_y > diff_x: walk1_x, walk1_y, walk2_x, walk2_y = 0, 1, 1, 1
                    elif diff_y == diff_x: walk1_x, walk1_y, walk2_x, walk2_y = 1, 1, 1, 1
                    else: walk1_x, walk1_y, walk2_x, walk2_y = 1, 0, 1, 1
                else: 
                    if abs(diff_y) > diff_x: walk1_x, walk1_y, walk2_x, walk2_y = 0, -1, 1, -1
                    elif abs(diff_y) == diff_x: walk1_x, walk1_y, walk2_x, walk2_y = 1, -1, 1, -1
                    else: walk1_x, walk1_y, walk2_x, walk2_y = 1, 0, 1, -1
            else: 
                if diff_y == 0:
                    walk1_x, walk1_y, walk2_x, walk2_y = -1, 0, -1, 0
                elif diff_y > 0:
                    if diff_y > abs(diff_x): walk1_x, walk1_y, walk2_x, walk2_y = 0, 1, -1, 1
                    elif diff_y == abs(diff_x): walk1_x, walk1_y, walk2_x, walk2_y = -1, 1, -1, 1
                    else: walk1_x, walk1_y, walk2_x, walk2_y = -1, 0, -1, 1
                else: 
                    if diff_y > diff_x: walk1_x, walk1_y, walk2_x, walk2_y = -1, 0, -1, -1
                    elif diff_y == diff_x: walk1_x, walk1_y, walk2_x, walk2_y = -1, -1, -1, -1
                    else: walk1_x, walk1_y, walk2_x, walk2_y = 0, -1, -1, -1

            x_offset, y_offset = 0, 0
            
            while True:
                x_ratio1 = (x_offset + walk1_x) / diff_x if diff_x != 0 else 1
                x_ratio2 = (x_offset + walk2_x) / diff_x if diff_x != 0 else 1
                y_ratio1 = (y_offset + walk1_y) / diff_y if diff_y != 0 else 1
                y_ratio2 = (y_offset + walk2_y) / diff_y if diff_y != 0 else 1

                if abs(x_ratio1 - y_ratio1) <= abs(x_ratio2 - y_ratio2):
                    x_offset, y_offset = x_offset + walk1_x, y_offset + walk1_y
                else:
                    x_offset, y_offset = x_offset + walk2_x, y_offset + walk2_y

                if x_offset == diff_x and y_offset == diff_y: return True
                
                current_entity = self.level_array[eye_x + x_offset][eye_y + y_offset]
                if not isinstance(current_entity, (Empty, Dummy)) and not current_entity.is_small: return False

    def get_adjacent_tiles(self, x, y, include_diagonals=False):
        """Returns a list of valid adjacent coordinate Vecs."""
        adj = []
        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 and j == 0: continue
                if not include_diagonals and i != 0 and j != 0: continue
                
                check_x, check_y = x + i, y + j
                if self.is_in_bounds(check_x, check_y):
                    adj.append(Vec(check_x, check_y))
        return adj
        
    ## 5. UI Callback Methods
    # =================================================================================
    def get_state(self, key):
        """Provides specific game state information to the UI."""
        if key == 'has_storage': return True
        if key == 'can_save': return self.save_manager.progressed
        if key == 'is_logged_in': return self.save_manager.username is not None
        if key == 'username': return self.save_manager.username
        return None

    def get_full_state(self):
        """Provides a dictionary of the full game state for the UI to render."""
        return {
            'paused': self.is_paused,
            'sound_on': self.audio_manager.sound_enabled,
            'volume': self.audio_manager.volume,
            'buttons_activated': [self.level_number > 1, True, self.level_number < 50]
        }

    def get_charts_data(self):
        """Returns placeholder chart data for the UI."""
        return [
            {'name': 'Player1', 'level': 10, 'steps': 1234},
            {'name': 'ProGamer', 'level': 8, 'steps': 987},
            {'name': 'BertiFan', 'level': 5, 'steps': 750},
        ]

    def save_game_action(self, username, password):
        """UI callback for saving the game. Returns an ErrorCode."""
        print(f"UI Action: Save for '{username}'")
        if not username: return ErrorCode.EMPTYNAME
        self.save_manager.username = username
        self.save_manager.save_game()
        return ErrorCode.SUCCESS

    def load_game_action(self, username, password):
        """UI callback for loading a game. Returns an ErrorCode."""
        print(f"UI Action: Load for '{username}'")
        if not username: return ErrorCode.EMPTYNAME
        return ErrorCode.SUCCESS if self.save_manager.load_game(username, password) else ErrorCode.NOTFOUND

    def change_password_action(self, old_pass, new_pass):
        """UI callback for changing password. Returns an ErrorCode."""
        print("UI Action: Change password")
        if not new_pass: return ErrorCode.EMPTYNAME
        return ErrorCode.SUCCESS

    def new_game_action(self):
        """UI callback for starting a new game without saving."""
        print("UI Action: New game")
        self.save_manager = SaveGameManager()
        self.load_level(1)

    def save_and_new_game_action(self):
        """UI callback for the 'Yes' button in the 'New Game' confirmation."""
        print("UI Action: Save and New. Triggering Save dialog.")
        pass
    
    def toggle_single_steps(self):
        """Toggles between single-step and continuous movement."""
        self.single_steps = not self.single_steps
        print(f"Single step mode: {self.single_steps}")

    def toggle_pause(self):
        """Toggles the game's paused state."""
        self.is_paused = not self.is_paused
        print(f"Game paused: {self.is_paused}")

    def toggle_sound(self):
        """Toggles sound on and off via the audio manager."""
        self.audio_manager.toggle_sound()

    def _process_completed_moves(self, moves_to_process):
        """
        Handles the final logic for all entities that finished moving in a tick.
        Uses a two-pass system to prevent entities from overwriting each other.
        """
        # Pass 1: Clear all moving entities from their old positions in the grid.
        for entity in moves_to_process:
            if self.level_array[entity.x][entity.y] == entity:
                self.level_array[entity.x][entity.y] = Empty(entity.x, entity.y)

        # Pass 2: Place entities in their new positions and handle interactions.
        for entity in moves_to_process:
            dest_pos = self.dir_to_coords(entity.x, entity.y, entity.face_dir)
            
            target_tile_entity = self.level_array[dest_pos.x][dest_pos.y]

            # Handle player-specific interactions (like consuming items)
            if isinstance(entity, Player) and target_tile_entity.consumable:
                if isinstance(target_tile_entity, Banana):
                    self.bananas_remaining -= 1
                
                target_tile_entity.consume(self) # The item handles its own removal
                
                # --- MOVED WIN CONDITION CHECK HERE ---
                # Check for win immediately after banana count is updated.
                if self.bananas_remaining <= 0:
                    self.end_level(won=True)
            
            # Place the moving entity into its new final position.
            # This check prevents placing an entity if the item consumption already handled the tile.
            if isinstance(self.level_array[dest_pos.x][dest_pos.y], (Empty, Dummy)):
                 self.level_array[dest_pos.x][dest_pos.y] = entity

            entity.x, entity.y = dest_pos.x, dest_pos.y
            
            # Reset the entity's state now that the move is complete.
            entity.is_moving = False
            entity.moving_offset = Vec(0, 0)
            entity.is_pushing = False

            # Update the game's quick-access list for the player's position.
            if isinstance(entity, Player):
                self.berti_positions[entity.berti_id] = dest_pos

    def remove_entity(self, entity_to_remove):
        """Replaces the specified entity with an Empty tile."""
        if self.level_array[entity_to_remove.x][entity_to_remove.y] == entity_to_remove:
            self.level_array[entity_to_remove.x][entity_to_remove.y] = Empty(entity_to_remove.x, entity_to_remove.y)