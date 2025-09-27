# ui_manager.py
import pygame
from config import Colors

# A simple base class for UI elements
class UIElement:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
    
    def handle_event(self, event):
        # To be implemented by subclasses
        pass
    
    def draw(self, surface):
        # To be implemented by subclasses
        pass

class DialogBox(UIElement):
    """
    A class to replicate the complex dialog boxes from the JS DOM.
    In a real project, this would be much more complex, with layouts,
    buttons, text inputs, etc. This is a simplified placeholder.
    """
    def __init__(self, rect, title, background_image=None):
        super().__init__(rect)
        self.title = title
        self.background_image = background_image
        self.font = pygame.font.SysFont("Tahoma", 14)
        self.is_active = False

    def draw(self, surface):
        if not self.is_active:
            return
        
        # Draw background
        if self.background_image:
            surface.blit(self.background_image, self.rect.topleft)
        else:
            pygame.draw.rect(surface, Colors.LIGHT_GREY, self.rect)
            pygame.draw.rect(surface, Colors.BLACK, self.rect, 2) # Border

        # Draw title
        title_surf = self.font.render(self.title, True, Colors.WHITE)
        # Simple title bar
        pygame.draw.rect(surface, Colors.BLUE, (self.rect.x, self.rect.y, self.rect.width, 25))
        surface.blit(title_surf, (self.rect.x + 5, self.rect.y + 5))

class UIManager:
    """
    Manages and draws all UI elements, such as menus and dialogs.
    Replaces the DOM manipulation parts of CLASS_visual.
    """
    def __init__(self):
        self.elements = []
        self.active_dialog = None
        
        # Example dialog - in a real game, you'd have one for each type
        # (save, load, charts, etc.)
        self.confirm_dialog = DialogBox((100, 100, 256, 154), "Confirm")
        # Add more dialogs here...
        
        # Menu state
        self.is_menu_open = False

    def open_dialog(self, dialog_id):
        """Opens a specific dialog box."""
        # This would be a lookup in a real system
        if dialog_id == "CONFIRM":
            self.active_dialog = self.confirm_dialog
            self.active_dialog.is_active = True
        print(f"Opening dialog: {dialog_id}")

    def close_active_dialog(self):
        if self.active_dialog:
            self.active_dialog.is_active = False
            self.active_dialog = None

    def handle_events(self, events):
        """
        Processes events for UI elements.
        Returns True if an event was consumed by the UI.
        """
        if self.active_dialog:
            for event in events:
                # Basic close functionality
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.close_active_dialog()
                    return True # Event was consumed
            # In a full implementation, you'd pass events to dialog buttons here
            return True # Assume dialogs consume all input while open
        return False

    def draw(self, surface):
        """Draws all active UI elements."""
        # 1. Draw the top menu bar (simplified)
        self.draw_menu_bar(surface)

        # 2. Draw any active dialog box on top
        if self.active_dialog:
            self.active_dialog.draw(surface)

    def draw_menu_bar(self, surface):
        """Replicates the render_menu logic."""
        bar_rect = pygame.Rect(0, 0, surface.get_width(), 20)
        pygame.draw.rect(surface, Colors.LIGHT_GREY, bar_rect)
        pygame.draw.rect(surface, Colors.WHITE, bar_rect, 2) # Border
        
        # Simplified: Just draw labels
        font = pygame.font.SysFont("Tahoma", 11)
        game_text = font.render("Game", True, Colors.BLACK)
        options_text = font.render("Options", True, Colors.BLACK)
        surface.blit(game_text, (10, 4))
        surface.blit(options_text, (60, 4))

    def draw_volume_bar(self, surface, volume, sound_enabled):
        """
        Replicates the render_vol_bar logic from JS.
        `volume` is a float from 0.0 to 1.0.
        """
        vb_rect = pygame.Rect(400, 2, 100, 17)
        
        for i in range(vb_rect.width):
            if i % 2 == 1: continue # Skip every other pixel for the "bar" effect
            
            ratio = i / vb_rect.width
            line_height = round(vb_rect.height * ratio)

            if i < volume * vb_rect.width:
                if sound_enabled:
                    # Interpolate color from green to red
                    color = (
                        int(Colors.GREEN[0] * (1 - ratio) + Colors.RED[0] * ratio),
                        int(Colors.GREEN[1] * (1 - ratio) + Colors.RED[1] * ratio),
                        int(Colors.GREEN[2] * (1 - ratio) + Colors.RED[2] * ratio)
                    )
                else:
                    color = Colors.DARK_GREY
            else:
                color = Colors.WHITE
            
            start_pos = (vb_rect.x + i, vb_rect.y + vb_rect.height - line_height)
            end_pos = (vb_rect.x + i, vb_rect.y + vb_rect.height)
            pygame.draw.line(surface, color, start_pos, end_pos)