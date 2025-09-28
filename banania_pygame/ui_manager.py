# ui_manager.py
import pygame
from config import ImageID, DialogBox as DialogBoxType, RenderMode, KeyCode, Direction, Entity, ErrorCode

# This module handles UI elements like menus and dialog boxes. It's designed to be
# the Python/Pygame equivalent of the UI management parts of the original JavaScript code.
#
# NOTE: Enums like `Entity`, `Direction`, and `RenderMode` are intentionally not used here.
# They relate to the core game logic and level rendering, which are managed by other
# parts of the application, not the high-level UI manager.

# --- UI Colors ---
class Colors:
    """Defines colors used in the UI, matching the JS version."""
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
        """Handles mouse events. Expects event.pos to be relative to the parent container."""
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
    def __init__(self, text, pos, font, color=Colors.BLACK, align="left"):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color
        self.align = align
        self.surface = self.font.render(self.text, True, self.color)

    def draw(self, surface):
        if self.align == "left":
            surface.blit(self.surface, self.pos)
        elif self.align == "right":
            surface.blit(self.surface, (self.pos[0] - self.surface.get_width(), self.pos[1]))


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

    def handle_event(self, event):
        """Handles events. Expects mouse event.pos to be relative to the parent container."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                 self.active = False # Or could trigger a submit action
            else:
                self.text += event.unicode
            return True
        return False

    def update(self, dt):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 500: # Blink every 500ms
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible

    def draw(self, surface):
        pygame.draw.rect(surface, Colors.INPUT_BG, self.rect)
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
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.center = screen_rect.center

        self.title = title
        self.res = resource_manager
        self.ui_manager = uimanager
        self.bg_image = self.res.get_image(bg_image_id) if bg_image_id is not None else None

        self.title_font = pygame.font.SysFont("Tahoma", 14, bold=True)
        self.font = pygame.font.SysFont("Tahoma", 12)

        self.components = []

    def handle_event(self, event):
        """Handles and consumes events for the modal dialog."""
        is_mouse_event = event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION)

        # Consume mouse events outside the dialog to enforce modality
        if is_mouse_event and not self.rect.collidepoint(event.pos):
            return True

        # Create a copy of the event with position relative to the dialog for components
        relative_event = pygame.event.Event(event.type, event.dict)
        if is_mouse_event:
            relative_event.pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)

        for component in self.components:
            if hasattr(component, 'handle_event'):
                if component.handle_event(relative_event):
                    break # Stop after one component handles it
        return True # Always consume events when dialog is active

    def update(self, dt):
        for component in self.components:
            if hasattr(component, 'update'):
                component.update(dt)

    def draw(self, surface):
        # Draw background
        if self.bg_image:
            surface.blit(self.bg_image, self.rect.topleft)
        else: # Fallback
            pygame.draw.rect(surface, Colors.LIGHT_GREY, self.rect)
            pygame.draw.rect(surface, Colors.DARK_GREY, self.rect, 2)

        # Draw Title (JS style, slightly outside the top of the box)
        title_surf = self.title_font.render(self.title, True, Colors.TITLE_TEXT)
        surface.blit(title_surf, (self.rect.x + 5, self.rect.y - 13))

        # Draw components on a subsurface relative to the dialog's position
        dialog_surface = surface.subsurface(self.rect)
        for component in self.components:
            component.draw(dialog_surface)

    def close(self):
        self.ui_manager.active_dialog = None

# --- Specific Dialog Box Implementations ---

class ConfirmDialog(DialogBox):
    """Asks a confirmation question."""
    def __init__(self, resource_manager, uimanager, yes_callback, no_callback):
        super().__init__((0, 0, 256, 154), "Confirm", ImageID.DIALOGBOX_CONFIRM, resource_manager, uimanager)

        self.components.append(Label("Do you want to save the game?", (40, 35), self.font))

        self.components.extend([
            Button((20, 100, 65, 25), ImageID.BTN_YES_UP, ImageID.BTN_YES_DOWN, yes_callback, self.res),
            Button((100, 100, 65, 25), ImageID.BTN_NO_UP, ImageID.BTN_NO_DOWN, no_callback, self.res),
            Button((180, 100, 65, 25), ImageID.BTN_CANCEL_UP, ImageID.BTN_CANCEL_DOWN, self.close, self.res)
        ])

class SaveLoadDialog(DialogBox):
    """Dialog for saving or loading, with name, password, and error fields."""
    def __init__(self, resource_manager, uimanager, title, ok_callback):
        super().__init__((0, 0, 256, 213), title, ImageID.DIALOGBOX_SAVELOAD, resource_manager, uimanager)

        self.ok_callback = ok_callback
        self.components.append(Label("Player name:", (20, 35), self.font))
        self.components.append(Label("Password:", (20, 60), self.font))

        self.name_input = InputField((100, 35, 120, 22), self.font)
        self.pass_input = InputField((100, 60, 120, 22), self.font, is_password=True)
        self.error_label = Label("", (20, 85), self.font, color=Colors.RED)
        self.components.extend([self.name_input, self.pass_input, self.error_label])

        self.components.extend([
            Button((40, 160, 65, 25), ImageID.BTN_OK_UP, ImageID.BTN_OK_DOWN, self._on_ok, self.res),
            Button((160, 160, 65, 25), ImageID.BTN_CANCEL_UP, ImageID.BTN_CANCEL_DOWN, self.close, self.res)
        ])

    def _on_ok(self):
        result = self.ok_callback(self.name_input.get_value(), self.pass_input.get_value())
        if result == ErrorCode.SUCCESS:
            self.close()
        else:
            self.set_error(result)

    def set_error(self, code):
        error_messages = {
            ErrorCode.EXISTS: "Error - the account already exists.",
            ErrorCode.NOSAVE: "Error - there are no savegames to load!",
            ErrorCode.WRONGPW: "Error - you used the wrong password.",
            ErrorCode.NOTFOUND: "Error - this username couldn't be found.",
            ErrorCode.EMPTYNAME: "Error - please fill in your name."
        }
        self.error_label.text = error_messages.get(code, "Unknown error")
        self.error_label.surface = self.font.render(self.error_label.text, True, self.error_label.color)

class ChangePasswordDialog(SaveLoadDialog):
    """Dialog for changing a password. Inherits from SaveLoadDialog."""
    def __init__(self, resource_manager, uimanager, ok_callback):
        super().__init__(resource_manager, uimanager, "Change password", ok_callback)
        # Override labels from parent
        self.components[0] = Label("Old password:", (20, 35), self.font)
        self.components[1] = Label("New password:", (20, 60), self.font)

class LoadLevelDialog(DialogBox):
    """Dialog for loading a specific level."""
    def __init__(self, resource_manager, uimanager, game_state_accessor):
        super().__init__((0, 0, 197, 273), "Load level", ImageID.DIALOGBOX_LOADLVL, resource_manager, uimanager)
        
        username = game_state_accessor('username') or "- none -"
        self.components.append(Label("Player name:", (20, 30), self.font))
        self.components.append(Label(username, (100, 30), self.font))
        self.components.append(Label("Level, steps:", (20, 50), self.font))
        
        # In a real implementation, this would be a scrollable list component.
        # For this example, we'll just add a placeholder label.
        self.components.append(Label("Level list component\nnot yet implemented.", (20, 80), self.font))
        
        self.components.extend([
            Button((25, 220, 65, 25), ImageID.BTN_OK_UP, ImageID.BTN_OK_DOWN, self.close, self.res), # Placeholder action
            Button((105, 220, 65, 25), ImageID.BTN_CANCEL_UP, ImageID.BTN_CANCEL_DOWN, self.close, self.res)
        ])

class ChartsDialog(DialogBox):
    """Dialog for displaying high scores (charts)."""
    def __init__(self, resource_manager, uimanager, chart_data):
        super().__init__((0, 0, 322, 346), "Charts", ImageID.DIALOGBOX_CHARTS, resource_manager, uimanager)

        headers = [("rank", 21), ("level", 57), ("steps", 100), ("name", 150)]
        for text, x_pos in headers:
            self.components.append(Label(text, (x_pos, 37), self.font))
        
        # Display chart data (e.g., top 10 players)
        for i, entry in enumerate(chart_data[:10]):
            y_pos = 65 + 18 * i
            self.components.extend([
                Label(str(i+1), (41, y_pos), self.font, align="right"),
                Label(str(entry['level']), (87, y_pos), self.font, align="right"),
                Label(str(entry['steps']), (140, y_pos), self.font, align="right"),
                Label(entry['name'], (155, y_pos), self.font)
            ])

        self.components.append(Button((125, 300, 65, 25), ImageID.BTN_OK_UP, ImageID.BTN_OK_DOWN, self.close, self.res))


# --- Menu Data Structures ---

class SubMenu:
    """Stores data for a dropdown menu."""
    def __init__(self, width, dd_width, name, options):
        self.width = width
        self.offset_line = 9
        self.offset_text = 17
        self.dd_width = dd_width
        self.dd_height = 6 + sum(self.offset_line if opt['line'] else self.offset_text for opt in options)
        self.name = name
        self.options = options

class Menu:
    """Stores data for the main menu bar."""
    def __init__(self, offset_x, offset_y, height, submenus):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.height = height
        self.width = sum(sm.width for sm in submenus)
        self.submenus = submenus

# --- Main UI Manager Class ---

class UIManager:
    """Manages and draws all UI elements, such as menus and dialogs."""
    def __init__(self, resource_manager, game_logic_callbacks):
        self.res = resource_manager
        self.game_callbacks = game_logic_callbacks # For actions and getting state
        self.active_dialog = None
        
        self.main_buttons_pressed = [False, False, False]
        self.berti_blink_time = 103

        self.menu_font = pygame.font.SysFont("Tahoma", 11)
        self.selected_menu_item = -1
        self._init_menus()
        
        self.hotkey_map = {
            pygame.K_F2: 0, # New
            pygame.K_F5: 4  # Single steps
        }

    def _init_menus(self):
        """Initializes the menu structure based on the JS logic."""
        # Lambdas to check game state. These should be connected to the actual game.
        can_always = lambda: True
        has_storage = lambda: self.game_callbacks['get_state']('has_storage')
        can_save = lambda: self.game_callbacks['get_state']('can_save')
        is_logged_in = lambda: self.game_callbacks['get_state']('is_logged_in')

        arr_options1 = [
            {'name': "New", 'effect_id': 0, 'on': can_always, 'hotkey': "F2", 'check': 0, 'line': False},
            {'name': "Load Game...", 'effect_id': 1, 'on': has_storage, 'hotkey': "", 'check': 0, 'line': False},
            {'name': "Save", 'effect_id': 2, 'on': can_save, 'hotkey': "", 'check': 0, 'line': False},
            {'name': "Pause", 'effect_id': 3, 'on': can_always, 'hotkey': "", 'check': 1, 'line': False}
        ]
        arr_options2 = [
            {'name': "Single steps", 'effect_id': 4, 'on': can_always, 'hotkey': "F5", 'check': 1, 'line': False},
            {'name': "Sound", 'effect_id': 5, 'on': can_always, 'hotkey': "", 'check': 1, 'line': False},
            {'name': "", 'effect_id': -1, 'on': can_always, 'hotkey': "", 'check': 0, 'line': True},
            {'name': "Load Level", 'effect_id': 6, 'on': has_storage, 'hotkey': "", 'check': 0, 'line': False},
            {'name': "Change Password", 'effect_id': 7, 'on': is_logged_in, 'hotkey': "", 'check': 0, 'line': False},
            {'name': "", 'effect_id': -1, 'on': can_always, 'hotkey': "", 'check': 0, 'line': True},
            {'name': "Charts", 'effect_id': 8, 'on': has_storage, 'hotkey': "", 'check': 0, 'line': False}
        ]
        
        self.main_menu = Menu(1, 2, 17, [SubMenu(43, 100, "Game", arr_options1), SubMenu(55, 150, "Options", arr_options2)])

    def _trigger_menu_effect(self, effect_id):
        """Performs an action based on a menu item's effect_id."""
        print(f"Triggering effect_id: {effect_id}")
        if effect_id == 0: # New
            self.game_callbacks['new']()
        elif effect_id == 1: # Load Game
            self.show_dialog(DialogBoxType.LOAD)
        elif effect_id == 2: # Save Game
            self.show_dialog(DialogBoxType.SAVE)
        elif effect_id == 3: # Pause
            self.game_callbacks['toggle_pause']()
        elif effect_id == 4: # Single steps <--- ADD THIS CASE
            self.game_callbacks['toggle_single_steps']()
        elif effect_id == 5: # Sound
            self.game_callbacks['toggle_sound']()
        elif effect_id == 6: # Load Level
             self.show_dialog(DialogBoxType.LOADLVL)
        elif effect_id == 7: # Change Password
            self.show_dialog(DialogBoxType.CHPASS)
        elif effect_id == 8: # Charts
            self.show_dialog(DialogBoxType.CHARTS)
        
        self.selected_menu_item = -1 # Close menu after action

    def handle_event(self, event):
        """Handles user input for all UI elements."""
        if self.active_dialog:
            self.active_dialog.handle_event(event)
            return

        # Handle Hotkeys
        if event.type == pygame.KEYDOWN and event.key in self.hotkey_map:
            self._trigger_menu_effect(self.hotkey_map[event.key])
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_menu_click(event.pos)
            self._handle_main_buttons_click(event.pos)
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
             self.main_buttons_pressed = [False, False, False]

    def update(self, dt):
        """Updates UI components, like blinking cursors in input fields."""
        if self.active_dialog:
            self.active_dialog.update(dt)

    def _handle_main_buttons_click(self, mouse_pos):
        button_rects = [pygame.Rect(219, 35, 30, 30), pygame.Rect(253, 35, 30, 30), pygame.Rect(287, 35, 30, 30)]
        for i, rect in enumerate(button_rects):
            if rect.collidepoint(mouse_pos):
                self.main_buttons_pressed[i] = True
                # Here you would call the callback for the main button
                print(f"Main button {i} clicked")
                break
    
    def _handle_menu_click(self, mouse_pos):
        menu = self.main_menu
        x_offset = menu.offset_x
        
        # Check for click on main menu bar to open/close a submenu
        for i, submenu in enumerate(menu.submenus):
            if pygame.Rect(x_offset, menu.offset_y, submenu.width, menu.height).collidepoint(mouse_pos):
                self.selected_menu_item = -1 if self.selected_menu_item == i else i
                return
            x_offset += submenu.width
        
        # Check for click inside an open submenu
        if self.selected_menu_item != -1:
            submenu = menu.submenus[self.selected_menu_item]
            x_offset = menu.offset_x + sum(sm.width for sm in menu.submenus[:self.selected_menu_item])
            dd_rect = pygame.Rect(x_offset, menu.offset_y + menu.height, submenu.dd_width, submenu.dd_height)

            if not dd_rect.collidepoint(mouse_pos):
                self.selected_menu_item = -1 # Clicked outside, close menu
                return
            
            # Find which option was clicked
            y_offset = menu.offset_y + menu.height + 4
            for option in submenu.options:
                item_height = submenu.offset_line if option['line'] else submenu.offset_text
                if not option['line']:
                    opt_rect = pygame.Rect(x_offset, y_offset, submenu.dd_width, item_height)
                    if opt_rect.collidepoint(mouse_pos) and option['on']():
                        self._trigger_menu_effect(option['effect_id'])
                        return
                y_offset += item_height
        
    def show_dialog(self, dialog_type, **kwargs):
        """Creates and shows a dialog box based on its type."""
        if dialog_type == DialogBoxType.CONFIRM:
            self.active_dialog = ConfirmDialog(self.res, self, kwargs['yes_callback'], kwargs['no_callback'])
        elif dialog_type == DialogBoxType.SAVE:
            self.active_dialog = SaveLoadDialog(self.res, self, "Save game", self.game_callbacks['save'])
        elif dialog_type == DialogBoxType.LOAD:
            self.active_dialog = SaveLoadDialog(self.res, self, "Load game", self.game_callbacks['load'])
        elif dialog_type == DialogBoxType.CHPASS:
            self.active_dialog = ChangePasswordDialog(self.res, self, self.game_callbacks['change_password'])
        elif dialog_type == DialogBoxType.LOADLVL:
            self.active_dialog = LoadLevelDialog(self.res, self, self.game_callbacks['get_state'])
        elif dialog_type == DialogBoxType.CHARTS:
            chart_data = self.game_callbacks['get_charts_data']()
            self.active_dialog = ChartsDialog(self.res, self, chart_data)
        
        self.selected_menu_item = -1 # Ensure menu is closed when dialog opens

    def draw_all(self, surface):
        """Draws all managed UI elements."""
        game_state = self.game_callbacks['get_full_state']()
        
        self.draw_volume_bar(surface, game_state['volume'], game_state['sound_on'])
        self.draw_main_buttons(surface, game_state['buttons_activated'])
        self.draw_menu(surface, game_state)

        if self.active_dialog:
            self.active_dialog.draw(surface)

    def draw_main_buttons(self, surface, activated_buttons):
        # Previous Button
        if not activated_buttons[0]:
            surface.blit(self.res.get_image(ImageID.BTN_PREV_DISABLED), (219, 35))
        else:
            img = ImageID.BTN_PREV_DOWN if self.main_buttons_pressed[0] else ImageID.BTN_PREV_UP
            surface.blit(self.res.get_image(img), (219, 35))
        
        # Berti Button (Blinking logic from JS)
        if self.main_buttons_pressed[1]:
            surface.blit(self.res.get_image(ImageID.BTN_BERTI_DOWN), (253, 35))
        else:
            if self.berti_blink_time >= 100:
                surface.blit(self.res.get_image(ImageID.BTN_BERTI_BLINK_UP), (253, 35))
                self.berti_blink_time -= 1
                if self.berti_blink_time < 100: self.berti_blink_time = 95 
            else:
                surface.blit(self.res.get_image(ImageID.BTN_BERTI_UP), (253, 35))
                self.berti_blink_time -= 1
                if self.berti_blink_time < 0: self.berti_blink_time = 103

        # Next Button
        if not activated_buttons[2]:
            surface.blit(self.res.get_image(ImageID.BTN_NEXT_DISABLED), (287, 35))
        else:
            img = ImageID.BTN_NEXT_DOWN if self.main_buttons_pressed[2] else ImageID.BTN_NEXT_UP
            surface.blit(self.res.get_image(img), (287, 35))

    def draw_menu(self, surface, game_state):
        menu = self.main_menu
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw main menu bar text
        submenu_offset = 0
        for sm in menu.submenus:
            text_surf = self.menu_font.render(sm.name, True, Colors.BLACK)
            surface.blit(text_surf, (menu.offset_x + submenu_offset + 6, menu.offset_y + 3))
            submenu_offset += sm.width
            
        # Draw open dropdown menu
        if self.selected_menu_item != -1:
            submenu = menu.submenus[self.selected_menu_item]
            x_pos = menu.offset_x + sum(sm.width for sm in menu.submenus[:self.selected_menu_item])
            dd_rect = pygame.Rect(x_pos, menu.offset_y + menu.height + 1, submenu.dd_width, submenu.dd_height)
            
            # Draw dropdown background and border
            pygame.draw.rect(surface, Colors.LIGHT_GREY, dd_rect)
            pygame.draw.line(surface, Colors.WHITE, dd_rect.topleft, dd_rect.topright)
            pygame.draw.line(surface, Colors.WHITE, dd_rect.topleft, dd_rect.bottomleft)
            pygame.draw.line(surface, Colors.DARK_GREY, (dd_rect.right - 1, dd_rect.top), (dd_rect.right - 1, dd_rect.bottom))
            pygame.draw.line(surface, Colors.DARK_GREY, (dd_rect.left, dd_rect.bottom - 1), (dd_rect.right, dd_rect.bottom - 1))

            # Draw menu options
            y_offset = dd_rect.top + 4
            for option in submenu.options:
                if option['line']:
                    pygame.draw.line(surface, Colors.MED_GREY, (dd_rect.left + 3, y_offset + 3), (dd_rect.right - 3, y_offset + 3))
                    pygame.draw.line(surface, Colors.WHITE, (dd_rect.left + 3, y_offset + 4), (dd_rect.right - 3, y_offset + 4))
                    y_offset += submenu.offset_line
                else:
                    opt_rect = pygame.Rect(dd_rect.left, y_offset, submenu.dd_width, submenu.offset_text)
                    is_hovered = opt_rect.collidepoint(mouse_pos)
                    is_enabled = option['on']()

                    if is_hovered and is_enabled:
                        pygame.draw.rect(surface, Colors.BLUE, (dd_rect.left + 3, y_offset, submenu.dd_width - 6, submenu.offset_text))
                    
                    text_color = Colors.MED_GREY if not is_enabled else (Colors.WHITE if is_hovered else Colors.BLACK)
                    text_surf = self.menu_font.render(option['name'], True, text_color)
                    surface.blit(text_surf, (dd_rect.left + 20, y_offset + 1))
                    
                    is_checked = (option['effect_id'] == 3 and game_state['paused']) or \
                                 (option['effect_id'] == 5 and game_state['sound_on'])
                                 
                    if option['check'] != 0 and is_checked:
                        check_img_id = ImageID.CHECKBOX_UNCHECKED if is_hovered and is_enabled else ImageID.CHECKBOX_CHECKED
                        surface.blit(self.res.get_image(check_img_id), (dd_rect.left + 6, y_offset + 4))

                    y_offset += submenu.offset_text
            
    def draw_volume_bar(self, surface, volume, sound_enabled):
        vb_rect = pygame.Rect(400, 2, 100, 17)
        for i in range(0, vb_rect.width, 2):
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
            
            pygame.draw.line(surface, color, (vb_rect.x + i, vb_rect.bottom), 
                             (vb_rect.x + i, vb_rect.bottom - line_height))