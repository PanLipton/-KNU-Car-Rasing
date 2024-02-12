# MenuManager.py

class MenuManager:
    def __init__(self, screen, gui_manager):
        self.screen = screen
        self.gui_manager = gui_manager
        self.current_menu = None

    def set_menu(self, menu_class, background_image_path):
        self.current_menu = menu_class(self.screen, self.gui_manager, self, background_image_path)

    def change_menu(self, menu_class):
        self.gui_manager.clear_and_reset()  # Очищення усіх існуючих елементів інтерфейсу
        self.set_menu(menu_class)

    def draw(self):
        if self.current_menu:
            self.current_menu.draw()

    def handle_event(self, event):
        if self.current_menu:
            self.current_menu.handle_event(event)
