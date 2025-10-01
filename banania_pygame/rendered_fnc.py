    def draw_level_entities(self, surface, game):
        """Draws the game entities, with clipping to keep them within the game board area."""
        
        # 1. Define the clipping rectangle for the game board.
        clip_rect = pygame.Rect(
            LEV_OFFSET_X,
            LEV_OFFSET_Y,
            LEV_DIMENSION_X * TILE_SIZE,
            LEV_DIMENSION_Y * TILE_SIZE
        )
        
        # --- Draw the game board entities with clipping enabled ---
        try:
            # 2. Apply the clipping rectangle.
            surface.set_clip(clip_rect)

            # To achieve the correct 2.5D perspective, we collect all drawable objects
            # and sort them in every frame based on their visual position.
            
            # Step A: Collect all drawable entities into a single list.
            drawable_entities = []
            for y in range(LEV_DIMENSION_Y):
                for x in range(LEV_DIMENSION_X):
                    block = game.level_array[x][y]
                    # A block is drawable if it has a valid image assigned.
                    if hasattr(block, 'animation_frame') and block.animation_frame != -1:
                         drawable_entities.append(block)

            # Step B: Define the sorting key for column-by-column rendering.
            # TODO : YOU HAVE TO SORT THE drawable_entities by x 
            # WE WOULD GET A LIST SORTED BY x
            # THEN IF A BLOCK IS MOVING (eg: LIGHTBLOCK, PURPLEMONSTER, GREENMONSTER, PLAYER_BERTI,HeAVY_BLOCK) YOU CHANGE IT ORDER OF RENDERING
            # FOR EACH MOVING ENTITY YOU HAVE TO CHECK THE DIRECTION OF MOVEMENT FIRST
            # IF THE ENTITY IS MOVING UP OR DOWN YOU HAVE TO RENDER IT AFTER THE 3 BLOCKS  on its right (y-1,y,y+1) in x-1 and before the 3 blocks in x+1 (y-1,y,y+1).
            # IF THE ENTITY IS MOVING LEFT OR RIGHT YOU HAVE TO RENDER IT AFTER THE 3 BLOCKS above it in y-1 (x-1,x,x+1) and before the blocks in y+1 (x-1,x,x+1).
            # AND YOU CAN DO THAT BY JUST THE ORDER OF THE LIST.
            # Step C: Sort the list of entities using our final key.
            drawable_entities.sort(key=sort_key)

            # Step D: Draw the entities in their newly sorted back-to-front order.
            for block in drawable_entities:
                self.draw_block(surface, block, block.x, block.y)

        finally:
            # 3. IMPORTANT: Reset the clip so popups and UI can draw outside the board.
            surface.set_clip(None)
        
        # --- Draw Popups on top (e.g., "WOW!", "ARGL!") without clipping ---
        if game.level_ended > 0 and game.berti_positions:
            for p_pos in game.berti_positions:
                player_block = game.level_array[p_pos.x][p_pos.y]
                x_pos = LEV_OFFSET_X + p_pos.x * TILE_SIZE + player_block.moving_offset.x
                y_pos = LEV_OFFSET_Y + p_pos.y * TILE_SIZE + player_block.moving_offset.y
                
                popup_img, offset_x, offset_y = None, 0, 0

                if game.level_ended == 1: # Won
                    if game.win_type == 'wow':
                        popup_id = ImageID.WOW
                        offset_x, offset_y = self.offset_wow_x, self.offset_wow_y
                    else: 
                        popup_id = ImageID.YEAH
                        offset_x, offset_y = self.offset_yeah_x, self.offset_yeah_y
                    popup_img = self.images.get(popup_id)
                
                elif game.level_ended == 2: # Died
                    popup_img = self.images.get(ImageID.ARGL)
                    offset_x, offset_y = self.offset_argl_x, self.offset_argl_y

                if popup_img:
                    surface.blit(popup_img, (x_pos + offset_x, y_pos + offset_y))