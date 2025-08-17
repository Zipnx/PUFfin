
import dearpygui.dearpygui as dpg

class PuffinGUI:
    def __init__(self, port: str, config):
        self.window_tag = "winmain"

    def setup(self):
        dpg.create_context()

        with dpg.window(label = "Test", tag=self.window_tag):
            dpg.add_text("The gui works somewhat")
        
        dpg.create_viewport(title = "PuffinPy GUI")
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def run(self):
        self.setup()
        dpg.start_dearpygui()
        dpg.destroy_context()

def main():
    app = PuffinGUI('COM4', None)
    app.run()
