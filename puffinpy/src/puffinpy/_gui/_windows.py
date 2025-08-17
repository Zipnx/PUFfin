
import dearpygui.dearpygui as dpg
from puffinpy._gui._structures import WinType

def wininit_stats():
    with dpg.window(label = 'Device Statistics', tag = WinType.STATS.value, 
                    no_title_bar = True, width = 200, height = 200):
        
        with dpg.group(horizontal = True):
            dpg.add_text('Temperature:')
            dpg.add_input_text(tag = "stats_temp_readout", 
                               readonly = True, width = -1)

        with dpg.group(horizontal = True):
            dpg.add_text("TX:")
            dpg.add_input_text(tag = "stats_rx_readout",
                               readonly = True, width = -1)

        with dpg.group(horizontal = True):
            dpg.add_text("RX:")
            dpg.add_input_text(tag = "stats_tx_readout",
                               readonly = True, width = -1)

        with dpg.group(horizontal = True):
            dpg.add_text("Status:")
            with dpg.drawlist(width = 30, height = 30):
                dpg.draw_rectangle((0, 0), (20, 20), fill = (255, 0, 0, 255), tag = "stats_status_display")

def wininit_apufinteract():
    with dpg.window(label = "Direct APUF", tag = WinType.APUF_INTERACT.value):
        dpg.add_text("Enter Challenge:")
        dpg.add_input_text(tag = "apufinteract_chall")
        dpg.add_button(label = "Execute")
        dpg.add_spacer(height = 3)

        with dpg.group(horizontal = True):
            dpg.add_text('Resp:')
            dpg.add_input_text(tag = "apufinteract_resp", 
                               readonly = True, width = -1)

def wininit_apufsampler():
    with dpg.window(label = "APUF Sampler", tag = WinType.APUF_SAMPLER.value,
                    width = 900, height = 400):
        dpg.add_text('Sampler options:')
        
        with dpg.group(horizontal = True):
            dpg.add_text("Sample Count: ")
            dpg.add_input_int(tag = 'apufsampler_count', width = 120,
                              default_value = 8192,
                              min_value = 128, max_value = 65536)

        with dpg.group(horizontal = True):
            dpg.add_text("Sampling Method: ")
            dpg.add_combo(
                width = 100,
                items = ['Sequential', 'Random'],
                default_value = 'Random',
                tag = 'apufsampler_method'
            )

        dpg.add_text('Sampler Seed (optional for random sampler):')
        dpg.add_input_text(tag = 'apufsampler_seed')
        dpg.add_spacer(height = 2)
        dpg.add_button(label = 'Start Sampler')
        dpg.add_spacer(height = 4)

def wininit_keygen():
    with dpg.window(label = "Key Generation", tag = WinType.KEYGEN.value):
        dpg.add_text("Secret Key:")
        dpg.add_input_text(tag = "keygen_readout", readonly = True)
        dpg.add_spacer(height = 3)
        dpg.add_button(label = "Generate")


def wininit_console():

    with dpg.window(label="Console Log", pos=(0, 310), width=980, height=300):
        with dpg.child_window(tag="console_output", width=-1, height=-1, autosize_x=True, autosize_y=True):
            dpg.add_text("[Console Initialized]")

def wininit_debugcon():

    with dpg.window(label="Debug Console", pos=(0, 310), width=980, height=300):
        with dpg.child_window(tag="debugcon_output", width=-1, height=-1, autosize_x=True, autosize_y=True):
            pass
