
import dearpygui.dearpygui as dpg
from puffinpy._gui._windows import (wininit_aes, wininit_stats, wininit_apufinteract, wininit_apufsampler, 
                                    wininit_keygen, wininit_console,
                                    wininit_debugcon)

from importlib.resources import files as pkg_files
from pathlib import Path
import time, argparse

from puffinpy import HCMCommander
from puffinpy._utils import bytecount_shorten

LAYOUTS = pkg_files("puffinpy._gui._layouts")
DEFAULT_LAYOUT = LAYOUTS / "default.dpg"
LOGO = LAYOUTS / "logo.png"

last_poll_time = 0

class PuffinGUI:
    def __init__(self, port: str, simulate: bool = False):
        self.window_tag = "winmain"
        self.hcm = HCMCommander(port = port, simulate = simulate)

    def setup(self):
        dpg.create_context()
        dpg.configure_app(docking = True, docking_space = True)
        
        self.setup_menubar() 

        # Will make the docking preset later, rn just doin quick dev
        wininit_stats()
        self.setup_heartbeat()

        wininit_apufinteract(self.hcm)
        wininit_apufsampler()
        wininit_keygen(self.hcm)
        wininit_console()
        wininit_debugcon()
        wininit_aes(self.hcm)
         
        with dpg.texture_registry():
            width, height, _, data = dpg.load_image(str(LOGO))
            texture_id = dpg.add_static_texture(width, height, data)

        with dpg.window(label = "", no_title_bar = True, tag = "win_logo", width = 200, height = 200):
            dpg.add_image(texture_id, width = 150, height = 150)

        self.load_default_layout()
        dpg.create_viewport(title = "PuffinPy GUI")
        dpg.setup_dearpygui()
        dpg.show_viewport()
    
    @staticmethod
    def load_default_layout():
        dpg.configure_app(init_file = str(DEFAULT_LAYOUT), load_init_file = True)


    def setup_menubar(self):

        with dpg.viewport_menu_bar():
            with dpg.menu(label = 'Layout'):
                dpg.add_menu_item(label = 'Save layout', callback = lambda e: dpg.save_init_file('layout.dpg'))
                dpg.add_menu_item(label = 'Load layout')
                dpg.add_menu_item(label = 'Reset to Default', callback = self.load_default_layout)
            
    def setup_heartbeat(self):
        def poll_temp(sender, app_data):
            global last_poll_time
            now = time.time()
            
            if now - last_poll_time >= 2:
                last_poll_time = now
                temp = self.hcm.get_temperature()
                dpg.set_value('stats_temp_readout', format(temp, '.2f'))
                dpg.configure_item("stats_status_display", fill = (0, 255, 0, 255))

                rx_rate  = self.hcm.traffic.rx_get_rate()
                rx_total = self.hcm.traffic.rx_total

                tx_rate  = self.hcm.traffic.tx_get_rate()
                tx_total = self.hcm.traffic.tx_total

                dpg.set_value('stats_rx_readout', f'{bytecount_shorten(rx_total)} ({bytecount_shorten(rx_rate)}/s)') 
                dpg.set_value('stats_tx_readout', f'{bytecount_shorten(tx_total)} ({bytecount_shorten(tx_rate)}/s)') 


            dpg.set_frame_callback(dpg.get_frame_count() + 32, poll_temp)

        poll_temp(None, None)

    def run(self):
        self.setup()
        dpg.start_dearpygui()
        dpg.destroy_context()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('serial', type=str, help = 'Serial port to connect to')
    parser.add_argument('--sim', action = 'store_true', help = "Run in simulation mode")
    args = parser.parse_args()

    app = PuffinGUI(args.serial, args.sim)
    app.run()
