# ui_manager.py
import pygame
from config import ImageID, DialogBox as DialogBoxType, RenderMode, KeyCode, Direction, Entity, ErrorCode

# Define colors used in the UI, matching the JS version
class Colors:
    BLACK = (0, 0, 0)
    DARK_GREY = (64, 64, 64)
    MED_GREY = (128, 128, 128)
    LIGHT_GREY = (212, 208, 200)
    WHITE = (255, 255, 255)
    BLUE = (10, 36, 106)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DISABLED_GREY = (50, 50, 50)
    INPUT_BG = (255, 255, 255)
    INPUT_BORDER = (128, 128, 128)
    TITLE_TEXT = (255, 255, 255)

# --- UI Component Helper Classes ---

class Button:
    """A simple UI button that uses images for its states."""
    def __init__(self, rect, img_up_id, img_down_id, callback, resource_manager):
        self.rect = pygame.Rect(rect)
        self.img_up = resource_manager.get_image(img_up_id)
        self.img_down = resource_manager.get_image(img_down_id)
        self.image = self.img_up
        self.callback = callback
        self.pressed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                self.image = self.img_down
                return True # Event handled
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed:
                if self.rect.collidepoint(event.pos) and self.callback:
                    self.callback()
                self.pressed = False
                self.image = self.img_up
                return True # Event handled
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Label:
    """A simple text label."""
    def __init__(self, text, pos, font, color=Colors.BLACK):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)

class InputField:
    """A text input field for dialog boxes."""
    def __init__(self, rect, font, is_password=False):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.is_password = is_password
        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event, dialog_rect):
        # Check for activation
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Adjust position to be absolute on screen
            absolute_rect = self.rect.move(dialog_rect.topleft)
            if absolute_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        
        # Handle key presses if active
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                 self.active = False # Or trigger a submit action
            else:
                self.text += event.unicode
    
    def update(self, dt):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 500: # Blink every 500ms
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible

    def draw(self, surface):
        pygame.draw.rect(surface, Colors.WHITE, self.rect)
        pygame.draw.rect(surface, Colors.INPUT_BORDER, self.rect, 1)

        display_text = "*" * len(self.text) if self.is_password else self.text
        text_surf = self.font.render(display_text, True, Colors.BLACK)
        surface.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

        if self.active and self.cursor_visible:
            cursor_pos = self.rect.x + 5 + text_surf.get_width()
            pygame.draw.line(surface, Colors.BLACK, (cursor_pos, self.rect.y + 5), (cursor_pos, self.rect.y + self.rect.height - 5))
            
    def get_value(self):
        return self.text

# --- Base Dialog Box Class ---

class DialogBox:
    """Base class for all modal dialog boxes."""
    def __init__(self, rect, title, bg_image_id, resource_manager, uimanager):
        self.rect = pygame.Rect(rect)
        # Center the dialog on the screen
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.center = screen_rect.center
        
        self.title = title
        self.res = resource_manager
        self.ui_manager = uimanager # To close itself
        self.bg_image = self.res.get_image(bg_image_id) if bg_image_id is not None else None
        
        self.title_font = pygame.font.SysFont("Tahoma", 14, bold=True)
        self.font = pygame.font.SysFont("Tahoma", 12)
        
        self.components = [] # Holds buttons, labels, input fields, etc.

    def handle_event(self, event):
        # Dialogs are modal, so they consume all events
        for component in self.components:
            if hasattr(component, 'handle_event'):
                 # Pass the dialog's rect for coordinate calculations
                if isinstance(component, InputField):
                    component.handle_event(event, self.rect)
                else: # Buttons need absolute coordinates
                    component_rect_abs = component.rect.copy()
                    component_rect_abs.topleft = (component.rect.left + self.rect.left, component.rect.top + self.rect.top)
                    
                    original_event_pos = event.pos
                    event.pos = (original_event_pos[0] - self.rect.left, original_event_pos[1] - self.rect.top)
                    
                    if component.handle_event(event):
                        event.pos = original_event_pos # Restore event pos
                        return
                    event.pos = original_event_pos # Restore event pos


    def update(self, dt):
        for component in self.components:
            if hasattr(component, 'update'):
                component.update(dt)

    def draw(self, surface):
        # Draw background
        if self.bg_image:
            surface.blit(self.bg_image, self.rect.topleft)
        else: # Fallback for missing images
            pygame.draw.rect(surface, Colors.LIGHT_GREY, self.rect)
            pygame.draw.rect(surface, Colors.DARK_GREY, self.rect, 2)
            
        # Draw Title
        title_surf = self.title_font.render(self.title, True, Colors.TITLE_TEXT)
        surface.blit(title_surf, (self.rect.x + 5, self.rect.y - 13)) # JS style title

        # Draw components relative to the dialog's surface
        dialog_surface = surface.subsurface(self.rect)
        for component in self.components:
            component.draw(dialog_surface)
            
    def close(self):
        self.ui_manager.active_dialog = None

# --- Specific Dialog Box Implementations ---

class ConfirmDialog(DialogBox):
    """Asks the user 'Do you want to save the game?'."""
    def __init__(self, resource_manager, uimanager, yes_callback, no_callback):
        super().__init__((0, 0, 256, 154), "Confirm", ImageID.DBX_CONFIRM, resource_manager, uimanager)
        
        self.components.append(Label("Do you want to save the game?", (40, 35), self.font))
        
        # Buttons
        yes_btn = Button((20, 100, 65, 25), ImageID.BTN_YES_UP, ImageID.BTN_YES_DOWN, yes_callback, self.res)
        no_btn = Button((100, 100, 65, 25), ImageID.BTN_NO_UP, ImageID.BTN_NO_DOWN, no_callback, self.res)
        cancel_btn = Button((180, 100, 65, 25), ImageID.BTN_CANCEL_UP, ImageID.BTN_CANCEL_DOWN, self.close, self.res)
        self.components.extend([yes_btn, no_btn, cancel_btn])

class SaveLoadDialog(DialogBox):
    """Dialog for saving or loading a game, with name and password fields."""
    def __init__(self, resource_manager, uimanager, title, ok_callback):
        super().__init__((0, 0, 256, 213), title, ImageID.DBX_SAVELOAD, resource_manager, uimanager)
        
        # Labels
        self.components.append(Label("Player name:", (20, 35), self.font))
        self.components.append(Label("Password:", (20, 60), self.font))

        # Input Fields
        self.name_input = InputField((100, 35, 120, 22), self.font)
        self.pass_input = InputField((100, 60, 120, 22), self.font, is_password=True)
        self.components.extend([self.name_input, self.pass_input])

        # Buttons
        # The callback needs to fetch data from the input fields
        ok_action = lambda: ok_callback(self.name_input.get_value(), self.pass_input.get_value())
        ok_btn = Button((40, 160, 65, 25), ImageID.BTN_OK_UP, ImageID.BTN_OK_DOWN, ok_action, self.res)
        cancel_btn = Button((160, 160, 65, 25), ImageID.BTN_CANCEL_UP, ImageID.BTN_CANCEL_DOWN, self.close, self.res)
        self.components.extend([ok_btn, cancel_btn])
        
# --- Menu Data Structures ---

class SubMenu:
    """Stores data for a dropdown menu, mirroring the JS CLASS_submenu."""
    def __init__(self, width, dd_width, name, options):
        self.width = width
        self.offset_line = 9
        self.offset_text = 17
        self.dd_width = dd_width
        self.dd_height = 6 + sum(self.offset_line if opt['line'] else self.offset_text for opt in options)
        self.name = name
        self.options = options

class Menu:
    """Stores data for the main menu bar, mirroring the JS CLASS_menu."""
    def __init__(self, offset_x, offset_y, height, submenus):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.height = height
        self.width = sum(sm.width for sm in submenus)
        self.submenus = submenus

# --- Main UI Manager Class ---

class UIManager:
    """
    Manages and draws all UI elements, such as menus and dialogs.
    This class is the direct Python/Pygame equivalent of the UI
    management and rendering parts of the JavaScript `CLASS_visual`.
    """
    def __init__(self, resource_manager):
        self.res = resource_manager
        self.active_dialog = None
        
        # Main UI buttons state
        self.main_buttons_pressed = [False, False, False]
        self.berti_blink_time = 103 # Start with a random-like value

        # Menu state
        self.menu_font = pygame.font.SysFont("Tahoma", 11)
        self.selected_menu_item = -1 # -1 means no submenu is open
        self._init_menus()

    def _init_menus(self):
        """Initializes the menu structure based on the JS logic."""
        tautology = lambda: True
        
        # These would check actual game state
        has_storage = lambda: True 
        can_save = lambda: True
        is_logged_in = lambda: True

        arr_options1 = [
            {'line': False, 'check': 0, 'name': "New", 'hotkey': "F2", 'effect_id': 0, 'on': tautology},
            {'line': False, 'check': 0, 'name': "Load Game...", 'hotkey': "", 'effect_id': 1, 'on': has_storage},
            {'line': False, 'check': 0, 'name': "Save", 'hotkey': "", 'effect_id': 2, 'on': can_save},
            {'line': False, 'check': 1, 'name': "Pause", 'hotkey': "", 'effect_id': 3, 'on': tautology}
        ]
        
        arr_options2 = [
            {'line': False, 'check': 1, 'name': "Single steps", 'hotkey': "F5", 'effect_id': 4, 'on': tautology},
            {'line': False, 'check': 1, 'name': "Sound", 'hotkey': "", 'effect_id': 5, 'on': tautology},
            {'line': True, 'check': 0, 'name': "", 'hotkey': "", 'effect_id': -1, 'on': tautology},
            {'line': False, 'check': 0, 'name': "Load Level", 'hotkey': "", 'effect_id': 6, 'on': has_storage},
            {'line': False, 'check': 0, 'name': "Change Password", 'hotkey': "", 'effect_id': 7, 'on': is_logged_in},
            {'line': True, 'check': 0, 'name': "", 'hotkey': "", 'effect_id': -1, 'on': tautology},
            {'line': False, 'check': 0, 'name': "Charts", 'hotkey': "", 'effect_id': 8, 'on': has_storage}
        ]
        
        sub_m1 = SubMenu(43, 100, "Game", arr_options1)
        sub_m2 = SubMenu(55, 150, "Options", arr_options2)
        self.main_menu = Menu(1, 2, 17, [sub_m1, sub_m2])

    def handle_event(self, event, game_state):
        """Handles user input for all UI elements."""
        # Prioritize dialogs if one is open
        if self.active_dialog:
            self.active_dialog.handle_event(event)
            return

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_menu_click(mouse_pos)
            self._handle_main_buttons_click(event.pos)
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
             self.main_buttons_pressed = [False, False, False]
             
    def update(self, dt, game_state):
        """Updates all UI components that need it (e.g., blinking cursors)."""
        if self.active_dialog:
            self.active_dialog.update(dt)

    def _handle_main_buttons_click(self, mouse_pos):
        button_rects = [
            pygame.Rect(219, 35, 30, 30),
            pygame.Rect(253, 35, 30, 30),
            pygame.Rect(287, 35, 30, 30)
        ]
        for i, rect in enumerate(button_rects):
            if rect.collidepoint(mouse_pos):
                self.main_buttons_pressed[i] = True
                print(f"Main button {i} clicked")
                break
    
    def _handle_menu_click(self, mouse_pos):
        menu = self.main_menu
        x_offset = menu.offset_x
        
        for i, submenu in enumerate(menu.submenus):
            rect = pygame.Rect(x_offset, menu.offset_y, submenu.width, menu.height)
            if rect.collidepoint(mouse_pos):
                self.selected_menu_item = -1 if self.selected_menu_item == i else i
                return
            x_offset += submenu.width
        
        if self.selected_menu_item != -1:
            submenu = menu.submenus[self.selected_menu_item]
            x_offset = menu.offset_x + sum(sm.width for sm in menu.submenus[:self.selected_menu_item])
            
            dd_rect = pygame.Rect(x_offset, menu.offset_y + menu.height, submenu.dd_width, submenu.dd_height)
            if dd_rect.collidepoint(mouse_pos):
                y_offset = menu.offset_y + menu.height + 4
                for option in submenu.options:
                    if not option['line']:
                        item_height = submenu.offset_text
                        opt_rect = pygame.Rect(x_offset, y_offset, submenu.dd_width, item_height)
                        if opt_rect.collidepoint(mouse_pos) and option['on']():
                            print(f"Clicked menu option: {option['name']}")
                            # --- This is where you would trigger dialogs ---
                            if option['effect_id'] == 0: # New Game
                                yes_cb = lambda: self.show_save_load_dialog("Save game", self._placeholder_save_and_new)
                                no_cb = self._placeholder_new_game
                                self.show_confirm_dialog(yes_cb, no_cb)

                            if option['effect_id'] == 1: # Load Game
                                self.show_save_load_dialog("Load game", self._placeholder_load)

                            if option['effect_id'] == 2: # Save Game
                                self.show_save_load_dialog("Save game", self._placeholder_save)

                            self.selected_menu_item = -1
                            return
                        y_offset += item_height
                    else:
                        y_offset += submenu.offset_line
            else:
                 self.selected_menu_item = -1

    # --- Dialog Management Methods ---
    def show_confirm_dialog(self, yes_callback, no_callback):
        self.active_dialog = ConfirmDialog(self.res, self, yes_callback, no_callback)
        self.selected_menu_item = -1 # Ensure menu is closed

    def show_save_load_dialog(self, title, ok_callback):
        self.active_dialog = SaveLoadDialog(self.res, self, title, ok_callback)
        self.selected_menu_item = -1 # Ensure menu is closed

    # --- Placeholder Callbacks for Dialogs ---
    def _placeholder_save(self, username, password):
        print(f"ACTION: Save game for user '{username}' with password '{password}'")
        if self.active_dialog: self.active_dialog.close()
    
    def _placeholder_save_and_new(self, username, password):
        print(f"ACTION: Save game for user '{username}' then start a new game.")
        if self.active_dialog: self.active_dialog.close()

    def _placeholder_load(self, username, password):
        print(f"ACTION: Load game for user '{username}' with password '{password}'")
        if self.active_dialog: self.active_dialog.close()

    def _placeholder_new_game(self):
        print("ACTION: Start new game without saving.")
        if self.active_dialog: self.active_dialog.close()


    def draw_all(self, surface, game_state):
        """Draws all managed UI elements."""
        self.draw_volume_bar(surface, game_state['volume'], game_state['sound_on'])
        self.draw_main_buttons(surface, game_state['buttons_activated'])
        self.draw_menu(surface, game_state)

        if self.active_dialog:
            self.active_dialog.draw(surface)

    def draw_main_buttons(self, surface, activated_buttons):
        if not activated_buttons[0]:
            surface.blit(self.res.get_image(ImageID.BTN_PREV_DISABLED), (219, 35))
        else:
            img = ImageID.BTN_PREV_DOWN if self.main_buttons_pressed[0] else ImageID.BTN_PREV_UP
            surface.blit(self.res.get_image(img), (219, 35))
        
        if self.main_buttons_pressed[1]:
            surface.blit(self.res.get_image(ImageID.BTN_BERTI_DOWN), (253, 35))
        else:
            if self.berti_blink_time >= 100:
                surface.blit(self.res.get_image(ImageID.BTN_BERTI_BLINK_UP), (253, 35))
                self.berti_blink_time -= 1
                if self.berti_blink_time < 100:
                     self.berti_blink_time = 95 
            else:
                surface.blit(self.res.get_image(ImageID.BTN_BERTI_UP), (253, 35))
                self.berti_blink_time -= 1
                if self.berti_blink_time < 0:
                     self.berti_blink_time = 103

        if not activated_buttons[2]:
            surface.blit(self.res.get_image(ImageID.BTN_NEXT_DISABLED), (287, 35))
        else:
            img = ImageID.BTN_NEXT_DOWN if self.main_buttons_pressed[2] else ImageID.BTN_NEXT_UP
            surface.blit(self.res.get_image(img), (287, 35))


    def draw_menu(self, surface, game_state):
        menu = self.main_menu
        mouse_pos = pygame.mouse.get_pos()
        
        submenu_offset = 0
        for i, sm in enumerate(menu.submenus):
            text_surf = self.menu_font.render(sm.name, True, Colors.BLACK)
            surface.blit(text_surf, (menu.offset_x + submenu_offset + 6, menu.offset_y + 3))
            submenu_offset += sm.width
            
        if self.selected_menu_item != -1:
            submenu = menu.submenus[self.selected_menu_item]
            x_pos = menu.offset_x + sum(sm.width for sm in menu.submenus[:self.selected_menu_item])
            
            dd_rect = pygame.Rect(x_pos, menu.offset_y + menu.height + 1, submenu.dd_width, submenu.dd_height)
            pygame.draw.rect(surface, Colors.LIGHT_GREY, dd_rect)
            
            pygame.draw.line(surface, Colors.WHITE, dd_rect.topleft, dd_rect.topright, 1)
            pygame.draw.line(surface, Colors.WHITE, dd_rect.topleft, dd_rect.bottomleft, 1)
            pygame.draw.line(surface, Colors.DARK_GREY, (dd_rect.right -1, dd_rect.top), (dd_rect.right -1, dd_rect.bottom), 1)
            pygame.draw.line(surface, Colors.DARK_GREY, (dd_rect.left, dd_rect.bottom -1), (dd_rect.right, dd_rect.bottom -1), 1)

            y_offset = dd_rect.top + 4
            for option in submenu.options:
                if option['line']:
                    pygame.draw.line(surface, Colors.MED_GREY, (dd_rect.left + 3, y_offset + 3), (dd_rect.right - 3, y_offset + 3), 1)
                    pygame.draw.line(surface, Colors.WHITE, (dd_rect.left + 3, y_offset + 4), (dd_rect.right - 3, y_offset + 4), 1)
                    y_offset += submenu.offset_line
                else:
                    opt_rect = pygame.Rect(dd_rect.left, y_offset, submenu.dd_width, submenu.offset_text)
                    is_hovered = opt_rect.collidepoint(mouse_pos)
                    is_enabled = option['on']()

                    if is_hovered and is_enabled:
                        pygame.draw.rect(surface, Colors.BLUE, (dd_rect.left + 3, y_offset, submenu.dd_width - 6, submenu.offset_text))
                    
                    if not is_enabled:
                        text_color = Colors.MED_GREY
                    elif is_hovered:
                        text_color = Colors.WHITE
                    else:
                        text_color = Colors.BLACK
                        
                    text_surf = self.menu_font.render(option['name'], True, text_color)
                    surface.blit(text_surf, (dd_rect.left + 20, y_offset + 1))
                    
                    is_checked = (option['effect_id'] == 3 and game_state['paused']) or \
                                 (option['effect_id'] == 5 and game_state['sound_on'])
                    if option['check'] != 0 and is_checked:
                        check_img_id = ImageID.CHECKBOX_UNCHECKED if is_hovered else ImageID.CHECKBOX_CHECKED
                        surface.blit(self.res.get_image(check_img_id), (dd_rect.left + 6, y_offset + 4))

                    y_offset += submenu.offset_text
            
    def draw_volume_bar(self, surface, volume, sound_enabled):
        vb_rect = pygame.Rect(400, 2, 100, 17)
        
        for i in range(vb_rect.width):
            if i % 2 == 1: continue
            
            ratio = i / vb_rect.width
            line_height = round(vb_rect.height * ratio)

            if i < volume * vb_rect.width:
                if sound_enabled:
                    color = (
                        int(Colors.GREEN[0] * (1 - ratio) + Colors.RED[0] * ratio),
                        int(Colors.GREEN[1] * (1 - ratio) + Colors.RED[1] * ratio),
                        int(Colors.GREEN[2] * (1 - ratio) + Colors.RED[2] * ratio)
                    )
                else:
                    color = Colors.DISABLED_GREY
            else:
                color = Colors.WHITE
            
            pygame.draw.line(surface, color, (vb_rect.x + i, vb_rect.y + vb_rect.height), 
                             (vb_rect.x + i, vb_rect.y + vb_rect.height - line_height))