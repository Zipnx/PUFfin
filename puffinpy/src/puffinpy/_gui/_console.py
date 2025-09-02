
import dearpygui.dearpygui as dpg

MAX_LOG_BUFFER = 512

logs = []

def console_print(s: str):
    global logs

    log_id = dpg.add_text(s, parent = "console_output")
    logs.append(log_id)

    while len(logs) > MAX_LOG_BUFFER:
        dpg.delete_item(logs[0])
        logs.pop(0)

    dpg.set_y_scroll("console_output", -1)

def info(s):  console_print(f'[*] {s}')
def good(s):  console_print(f'[+] {s}')
def error(s): console_print(f'[!] {s}')
