
import dearpygui.dearpygui as dpg
from puffinpy._gui._windows import (wininit_stats, wininit_apufinteract, wininit_apufsampler, 
                                    wininit_keygen, wininit_console,
                                    wininit_debugcon)

from importlib.resources import files as pkg_files
from pathlib import Path

LAYOUTS = pkg_files("puffinpy._gui._layouts")
DEFAULT_LAYOUT = LAYOUTS / "default.dpg"

class PuffinGUI:
    def __init__(self, port: str, config):
        self.window_tag = "winmain"

    def setup(self):
        dpg.create_context()
        dpg.configure_app(docking = True, docking_space = True)
        
        self.setup_menubar()
        
        # Will make the docking preset later, rn just doin quick dev
        #wininit_stats()
        #wininit_apufinteract()
        wininit_apufsampler()
        #wininit_keygen()
        #wininit_console()
        #wininit_debugcon()

        dpg.create_viewport(title = "PuffinPy GUI")
        dpg.setup_dearpygui()
        dpg.show_viewport()
    
    def setup_menubar(self):

        def load_default():
            dpg.configure_app(init_file = str(DEFAULT_LAYOUT), load_init_file = True)

        with dpg.viewport_menu_bar():
            with dpg.menu(label = 'Layout'):
                dpg.add_menu_item(label = 'Save layout')
                dpg.add_menu_item(label = 'Load layout')
                dpg.add_menu_item(label = 'Reset to Default', callback = load_default)
            

    def run(self):
        self.setup()
        dpg.start_dearpygui()
        dpg.destroy_context()

def main():
    app = PuffinGUI('COM4', None)
    app.run()
