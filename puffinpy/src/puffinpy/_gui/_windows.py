
import dearpygui.dearpygui as dpg
from puffinpy._commander import HCMCommander
from puffinpy._gui._structures import WinType

def wininit_stats():
    with dpg.window(label = 'Device Statistics', tag = WinType.STATS.value, 
                    no_title_bar = True, width = 200, height = 200):
        
        with dpg.group(horizontal = True):
            dpg.add_text('Temperature:')
            dpg.add_input_text(tag = "stats_temp_readout", 
                               readonly = True, width = -1)

        with dpg.group(horizontal = True):
            dpg.add_text("RX:")
            dpg.add_input_text(tag = "stats_rx_readout",
                               readonly = True, width = -1)

        with dpg.group(horizontal = True):
            dpg.add_text("TX:")
            dpg.add_input_text(tag = "stats_tx_readout",
                               readonly = True, width = -1)

        with dpg.group(horizontal = True):
            dpg.add_text("Status:")
            with dpg.drawlist(width = 30, height = 30):
                dpg.draw_rectangle((0, 0), (20, 20), fill = (255, 0, 0, 255), tag = "stats_status_display")

def wininit_apufinteract(hcm: HCMCommander):

    def apuf_callback(sender, app_data):
        challenge = dpg.get_value("apufinteract_chall")
        
        try:
            challenge = int(challenge)
        except ValueError:
            print('Invalid challenge (make proper error display at the console)')
            return

        if challenge.bit_length() > 32:
            print('Invalid challenge bit length')
            return

        resp = hcm.apuf_single(challenge)
        dpg.set_value('apufinteract_resp', hex(resp))


    with dpg.window(label = "Direct APUF", tag = WinType.APUF_INTERACT.value):
        dpg.add_text("Enter Challenge (dec/hex):")
        dpg.add_input_text(tag = "apufinteract_chall")
        dpg.add_button(label = "Execute", callback = apuf_callback)
        dpg.add_spacer(height = 8)
        dpg.add_input_text(tag = "apufinteract_resp", 
                           readonly = True, width = -1)

def wininit_aes(hcm: HCMCommander):
    def encrypt_callback():
        plain = dpg.get_value("aesenc_plain")
        key   = dpg.get_value("aesenc_key")

        cipher = hcm.aes_encrypt(bytes.fromhex(key), bytes.fromhex(plain))

        dpg.set_value("aesenc_ciph", cipher.hex())
    
    def decrypt_callback():
        ciph = dpg.get_value("aesdec_ciph")
        key  = dpg.get_value("aesdec_key")

        plain = hcm.aes_decrypt(bytes.fromhex(key), bytes.fromhex(ciph))

        dpg.set_value("aesdec_plain", plain.hex())

    with dpg.window(label = "AES Encrypt/Decrypt", width = 600, height = 400, tag = WinType.AES.value):
        with dpg.table(header_row = False, resizable = True, policy = dpg.mvTable_SizingStretchProp):
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row():
                with dpg.child_window(border = True):
                    dpg.add_text("Encrypt")
                    dpg.add_spacer(height = 4)

                    with dpg.group(horizontal = True):
                        dpg.add_text("Plain (hex):")
                        dpg.add_input_text(tag = "aesenc_plain", width = 270, 
                                           hexadecimal = True, no_spaces = True)

                    with dpg.group(horizontal = True):
                        dpg.add_text("Key   (hex):")
                        dpg.add_input_text(tag = "aesenc_key", width = 270, 
                                           hexadecimal = True, no_spaces = True)
                    
                    dpg.add_spacer(height = 4)
                    dpg.add_button(label = "Encrypt", callback = encrypt_callback)
                    dpg.add_spacer(height = 4)

                    with dpg.group(horizontal = True):
                        dpg.add_text('Ciphertext:')
                        dpg.add_input_text(tag = "aesenc_ciph", width = 270, readonly = True, 
                                           hexadecimal = True, no_spaces = True)

                with dpg.child_window(border = True):
                    dpg.add_text("Decrypt")
                    dpg.add_spacer(height = 4)

                    with dpg.group(horizontal = True):
                        dpg.add_text("Ciph (hex):")
                        dpg.add_input_text(tag = "aesdec_ciph", width = 270, 
                                           hexadecimal = True, no_spaces = True)

                    with dpg.group(horizontal = True):
                        dpg.add_text("Key  (hex):")
                        dpg.add_input_text(tag = "aesdec_key", width = 270, 
                                           hexadecimal = True, no_spaces = True)
                    
                    dpg.add_spacer(height = 4)
                    dpg.add_button(label = "Decrypt", callback = decrypt_callback)
                    dpg.add_spacer(height = 4)

                    with dpg.group(horizontal = True):
                        dpg.add_text('Plaintext:')
                        dpg.add_input_text(tag = "aesdec_plain", width = 270, readonly = True, 
                                           hexadecimal = True, no_spaces = True)
                    
                    dpg.add_spacer(height = 8)
                    dpg.add_text('''NOTE: Due to how the AES core works, the key used for decryption
must be the last round key from the aes key expansion.''')

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
            dpg.add_text('Repeat Count: ')
            dpg.add_input_int(tag = 'apufsampler_repcount', 
                              default_value = 1, width = 100, 
                              min_value = 1, max_value = 128)

        with dpg.group(horizontal = True):
            dpg.add_text("Chunk Size: ")
            dpg.add_input_int(tag = "apufsampler_chunksize", 
                              default_value = 64, width = 100,
                              min_value = 1, max_value = 1024) 
            # TODO: Make the chunk max be identified by the hcm rx buffer tize

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

def wininit_keygen(hcm: HCMCommander):
    KEYTYPES = ['Primary', 'Secondary', 'Tertiary']
    
    def callback_keygen(sender, app_data):
        keytype = dpg.get_value('keygen_keytype')
        select = KEYTYPES.index(keytype)
        pshash = not dpg.get_value('keygen_donthash')
        
        if pshash:
            select |= 0x80000000

        result = hcm.ropuf(select)
        dpg.set_value('keygen_readout', result.hex())

    with dpg.window(label = "Key Generation", tag = WinType.KEYGEN.value):
        dpg.add_text("Secret Key:")
        with dpg.group(horizontal = True):
            dpg.add_text('Key:')
            dpg.add_combo(
                width = 100,
                items = KEYTYPES,
                default_value = KEYTYPES[0],
                tag = "keygen_keytype"
            )

        with dpg.group(horizontal = True):
            dpg.add_text('Bypass Hash: ')
            dpg.add_checkbox(tag = "keygen_donthash")

        dpg.add_input_text(tag = "keygen_readout", readonly = True, width = -1)
        dpg.add_spacer(height = 3)
        dpg.add_button(label = "Generate", callback = callback_keygen)


def wininit_console():

    with dpg.window(label="Console Log", pos=(0, 310), width=980, height=300):
        with dpg.child_window(tag="console_output", width=-1, height=-1, autosize_x=True, autosize_y=True):
            dpg.add_text("[Console Initialized]")

def wininit_debugcon():

    with dpg.window(label="Debug Console", pos=(0, 310), width=980, height=300):
        with dpg.child_window(tag="debugcon_output", width=-1, height=-1, autosize_x=True, autosize_y=True):
            pass
