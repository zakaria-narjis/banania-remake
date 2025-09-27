# entities.py
import random
import config # Assuming your constants are in config.py

# A simple class for 2D vectors/coordinates could be useful
class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ===================================================================================
# BASE ENTITY CLASS
# ===================================================================================

class Entity:
    """The base class for all objects in the game world."""
    def __init__(self, x, y, entity_id):
        self.x = x
        self.y = y
        self.id = entity_id

        # --- State Properties ---
        self.is_moving = False
        self.moving_offset = Vec(0, 0) # Visual offset while moving
        self.is_pushing = False
        self.face_dir = config.Direction.DOWN
        self.just_moved = False
        self.removal_timer = -1 # Corresponds to gets_removed_in

        # --- Gameplay Attributes ---
        self.can_push = False
        self.pushable = False
        self.consumable = False
        self.is_small = False # Affects movement and visibility rules

        # --- Visuals ---
        self.animation_frame = -1
        self.animation_delay = 0

    def update(self, game):
        """
        Handles the continuous logic for an entity, like visual movement and timers.
        This is called every game tick.
        """
        self.animation_delay += 1
        
        # 1. Handle visual movement tweening
        if self.is_moving:
            if self.face_dir == config.Direction.UP:
                self.moving_offset.y -= game.move_speed
            elif self.face_dir == config.Direction.DOWN:
                self.moving_offset.y += game.move_speed
            elif self.face_dir == config.Direction.LEFT:
                self.moving_offset.x -= game.move_speed
            elif self.face_dir == config.Direction.RIGHT:
                self.moving_offset.x += game.move_speed

            # Check if movement to the next tile is complete
            if abs(self.moving_offset.x) >= config.TILE_SIZE or abs(self.moving_offset.y) >= config.TILE_SIZE:
                game.move(self.x, self.y, self.face_dir)
                self.just_moved = True

        # 2. Handle entity removal timer (for doors)
        if self.removal_timer == 0:
            if self.is_moving:
                # If the door is moving when it gets removed
                dest_pos = game.dir_to_coords(self.x, self.y, self.face_dir)
                game.level_array[dest_pos.x][dest_pos.y] = Empty(dest_pos.x, dest_pos.y)
            game.level_array[self.x][self.y] = Empty(self.x, self.y)
        
        elif self.removal_timer > 0:
            self.removal_timer -= 1
            # You might want to trigger an animation update here
            # vis.update_animation(self.x, self.y)

# ===================================================================================
# CHARACTER SUBCLASSES (PLAYER AND MONSTERS)
# ===================================================================================

class Character(Entity):
    """A base class for movable characters like the player and monsters."""
    def __init__(self, x, y, entity_id):
        super().__init__(x, y, entity_id)
        self.is_small = True # Players and monsters are "small" entities

class Player(Character):
    """The player-controlled character."""
    def __init__(self, x, y, berti_id):
        super().__init__(x, y, config.Entity.PLAYER_BERTI)
        self.berti_id = berti_id
        self.can_push = True

    def handle_input(self, game, input_handler):
        """
        Checks for keyboard/touch input and initiates movement.
        Corresponds to the `register_input` function.
        """
        if self.is_moving:
            return

        # Determine direction from input (this part depends on your input_handler)
        # For simplicity, we'll just check for a pressed direction
        pressed_dir = input_handler.get_direction() # You'll need to implement this

        if pressed_dir != config.Direction.NONE and game.is_walkable(self.x, self.y, pressed_dir):
            game.start_move(self.x, self.y, pressed_dir)

    def check_enemy_proximity(self, game):
        """
        Checks adjacent and diagonal tiles for monsters to see if the player was caught.
        """
        if self.moving_offset.x != 0 or self.moving_offset.y != 0:
            return

        for tile_pos in game.get_adjacent_tiles(self.x, self.y, include_diagonals=True):
            entity = game.level_array[tile_pos.x][tile_pos.y]
            
            # Check if the entity is a monster and is not moving
            if isinstance(entity, Monster) and not entity.is_moving:
                # Check for diagonal obstruction
                is_diagonal = abs(self.x - tile_pos.x) == 1 and abs(self.y - tile_pos.y) == 1
                if is_diagonal:
                    # If there's an obstacle in the way, the player is safe
                    obstacle1 = not isinstance(game.level_array[tile_pos.x][self.y], (Empty, Dummy))
                    obstacle2 = not isinstance(game.level_array[self.x][tile_pos.y], (Empty, Dummy))
                    if obstacle1 or obstacle2:
                        continue # Skip to the next adjacent tile

                # If we reach here, the player is caught!
                game.end_level(caught=True)
                return

class Monster(Character):
    """A base class for enemy AI characters."""
    def __init__(self, x, y, entity_id):
        super().__init__(x, y, entity_id)
        self.sees_berti = False
        self.time_since_noise = 100

    def update_ai(self, game):
        """The main AI logic loop for the monster."""
        if not self.is_moving:
            self.chase_berti(game)

    def move_randomly(self, game):
        """Makes the monster wander aimlessly if it cannot see the player."""
        if self.is_moving:
            return
        
        possibilities = [config.Direction.UP, config.Direction.DOWN, config.Direction.LEFT, config.Direction._RIGHT]
        random.shuffle(possibilities) # Shuffle to make it random

        # Prefer moving forward, but try other directions too
        if random.random() < 0.80 and game.is_walkable(self.x, self.y, self.face_dir):
            game.start_move(self.x, self.y, self.face_dir)
            return

        # Try all other random directions
        for direction in possibilities:
            if game.is_walkable(self.x, self.y, direction):
                game.start_move(self.x, self.y, direction)
                return

    def chase_berti(self, game):
        """Finds and moves towards the player if visible."""
        if self.is_moving:
            return

        self.time_since_noise += 1
        closest_berti_pos = None
        min_dist = float('inf')

        # 1. Find the closest, visible Berti
        for berti_pos in game.berti_positions:
            # Check if Berti is generally in the direction the monster is facing
            is_in_front = (
                (self.face_dir == config.Direction.DOWN and berti_pos.y >= self.y) or
                (self.face_dir == config.Direction.UP and berti_pos.y <= self.y) or
                (self.face_dir == config.Direction.LEFT and berti_pos.x <= self.x) or
                (self.face_dir == config.Direction.RIGHT and berti_pos.x >= self.x)
            )
            
            if is_in_front and game.can_see_tile(self.x, self.y, berti_pos.x, berti_pos.y):
                dist = abs(berti_pos.x - self.x) + abs(berti_pos.y - self.y)
                if dist < min_dist:
                    min_dist = dist
                    closest_berti_pos = berti_pos

        # 2. Decide whether to chase or move randomly
        if closest_berti_pos is None or random.random() < 0.02:
            self.sees_berti = False
            self.move_randomly(game)
            return

        # 3. If chasing, determine the best direction to move
        if not self.sees_berti:
            self.sees_berti = True
            # Play a sound when first spotting the player
            if self.time_since_noise > random.randint(3, 13):
                self.time_since_noise = 0
                if self.id == config.Entity.PURPLE_MONSTER:
                    game.play_sound('monster_spot_purple')
                elif self.id == config.Entity.GREEN_MONSTER:
                    game.play_sound('monster_spot_green')

        diff_x = closest_berti_pos.x - self.x
        diff_y = closest_berti_pos.y - self.y

        # Determine preferred directions based on player position
        dir1, dir2 = None, None
        if abs(diff_x) > abs(diff_y):
            dir1 = config.Direction.RIGHT if diff_x > 0 else config.Direction.LEFT
            dir2 = config.Direction.DOWN if diff_y > 0 else config.Direction.UP
        else:
            dir1 = config.Direction.DOWN if diff_y > 0 else config.Direction.UP
            dir2 = config.Direction.RIGHT if diff_x > 0 else config.Direction.LEFT
        
        if diff_y == 0: dir2 = None
        if diff_x == 0: dir2 = None

        # Try to move in the primary direction, then secondary, otherwise move randomly
        if game.is_walkable(self.x, self.y, dir1):
            game.start_move(self.x, self.y, dir1)
        elif dir2 and game.is_walkable(self.x, self.y, dir2):
            game.start_move(self.x, self.y, dir2)
        else:
            self.move_randomly(game)


class PurpleMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.PURPLE_MONSTER)
        self.can_push = True

class GreenMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.GREEN_MONSTER)
        # Green monsters cannot push according to the JS logic


# ===================================================================================
# OBJECT SUBCLASSES (BLOCKS, ITEMS, ETC.)
# ===================================================================================

class Block(Entity):
    """Base class for pushable blocks."""
    def __init__(self, x, y, entity_id):
        super().__init__(x, y, entity_id)
        self.pushable = True

class LightBlock(Block):
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.LIGHT_BLOCK)
        self.can_push = True # Can push other blocks

class HeavyBlock(Block):
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.HEAVY_BLOCK)

class PinnedBlock(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.PINNED_BLOCK)

class Item(Entity):
    """Base class for consumable items like keys and bananas."""
    def __init__(self, x, y, entity_id):
        super().__init__(x, y, entity_id)
        self.consumable = True
    def consume(self, game):
        """
        Handles the logic when the item is consumed.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclass must implement abstract method")
class Banana(Item):
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.BANANA_PEEL)
    def consume(self, game):
        game.bananas_collected += 1
        game.play_sound('collect_banana')
        game.remove_entity(self)
class Key(Item):
    """A key that opens a corresponding door."""
    def __init__(self, x, y, entity_id, door_id):
        super().__init__(x, y, entity_id)
        self.door_id = door_id # The ID of the door this key opens
    def consume(self, game):
        game.add_key(self.door_id) # The game adds the key to the player's inventory
        game.play_sound('pickup_key')
        game.remove_entity(self)
class Door(Entity):
    """A door that can be removed by a key."""
    def __init__(self, x, y, entity_id):
        super().__init__(x, y, entity_id)

# ===================================================================================
# SPECIAL/SYSTEM ENTITIES
# ===================================================================================

class Empty(Entity):
    """Represents an empty tile."""
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.EMPTY)

class Dummy(Entity):
    """A temporary placeholder for a tile that an entity is moving into."""
    def __init__(self, x, y):
        super().__init__(x, y, config.Entity.DUMMY)