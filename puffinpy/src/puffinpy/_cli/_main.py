
import sys, cmd, argparse
from puffinpy import HCMCommander

class PuffinShell(cmd.Cmd):
    intro = '''\nWelcome to the PuffinPy Interactive shell
=============================================
From here you can query and execute available
functionalities on any device that implements
the libhcm firmware.
'''
    prompt = "puffin> "
    
    def __init__(self, cliargs: argparse.Namespace):
        if not cliargs.port and not cliargs.sim:
            print('If simulation is not selected, a serial port is required (-p)')
            sys.exit(-1)

        super().__init__()
        self.cliargs = cliargs

        self.hcm = HCMCommander(
            port = cliargs.port if cliargs.port is not None else '',
            debug = True,
            simulate = cliargs.sim
        ) 
    
    def do_query(self, arg):
        '''
        Usage: query

        Query the capabilities of the device.
        IE: Whether it has enabled APUF, ROPUF, AES, etc...
        '''
        print('UNIMPLEMENTED')
        print('Query available capabilities of the device')

    def do_temperature(self, arg):
        '''
        Usage: temperature

        Get the temperature of the board from the XADC
        '''
        try:
            temp = self.hcm.get_temperature()
        except ValueError:
            print('[!] Error retrieving temperature')
            return

        print('Temperature:', temp)
    
    def do_apuf(self, arg):
        '''
        Usage: apuf <CHALLENGE>

        Send a challenge to the Arbiter PUF and get back a response.
        '''
        try:
            chall = int(arg)
        except ValueError:
            print('[!] Invalid int')
            return

        if chall.bit_length() > 32:
            print('[!] Challenge must be a uint32')
            return 

        try:
            response = self.hcm.apuf_single(chall)
        except ValueError as e:
            print('[!] Error:', str(e))
            return

        print(f'Response: {hex(response)}')

    def do_rawapuf(self, arg):
        '''
        Usage: rawapuf <CHALLENGE>

        DEV: Used mostly for testing the raw apuf, this is pretty much
        always disabled.
        '''
        try:
            chall = int(arg)
        except ValueError:
            print('[!] Invalid int')
            return

        if chall.bit_length() > 32:
            print('[!] Challenge must be a uint32')
            return 

        try:
            response = self.hcm.rawapuf_single(chall)
        except ValueError as e:
            print('[!] Error:', str(e))
            return

        print(f'Response: {hex(response)}')
    
    def do_pufky(self, arg):
        '''
        Usage: pufky <SELECT>

        Get back a generated key from the pufky system
        '''
        
        pshash = False

        if ' ' in arg:
            arg = arg.split(' ')
            if len(arg) > 1:
                pshash = 'pshash' in arg[1]

            sel = arg[0]
        else:
            sel = arg

        try:
            sel = int(sel)
            if pshash:
                sel |= 0x80000000
        except ValueError:
            print('[!] Invalid select')
            return
        
        if sel.bit_length() > 32:
            print('[!] Select must be a uint32')
            return
        
        try:
            response = self.hcm.ropuf(sel)
        except BaseException as e:
            print('[!] Error:', str(e))
            return

        print(f'Key: {response.hex()}')
    
    def do_aesenc(self, arg):
        '''
        Usage: aesenc <KEY> <PLAIN>

        Encrypt the plaintext with the given AES 128 bit key
        '''

        args = arg.split(' ')
        if len(args) < 2:
            print('[!] Usage: <KEY> <PLAIN>')
            return

        try:
            key = bytes.fromhex(args[0])
            plain = bytes.fromhex(args[1])
        except:
            print('[!] Invalid hex inputs')
            return
        
        if len(key) != 16 or len(plain) != 16:
            print('[!] Key/Plain must be 16 bytes')
            return

        result = self.hcm.aes_encrypt(key, plain)
        
        print(f'Encrypted: {result.hex()}')
    
    def do_aesdec(self, arg):
        '''
        Usage: aesdec <KEY (*)> <CIPHERTEXT>

        Decrypt the ciphertext with the given key
        (*): The key required in the last round key
             from the aes key expansion.
        '''
        args = arg.split(' ')
        if len(args) < 2:
            print('[!] Usage: <KEY> <CIPHERTEXT>')
            return

        try:
            key = bytes.fromhex(args[0])
            ciph = bytes.fromhex(args[1])
        except:
            print('[!] Invalid hex inputs')
            return
        
        if len(key) != 16 or len(ciph) != 16:
            print('[!] Key/Plain must be 16 bytes')
            return

        result = self.hcm.aes_decrypt(key, ciph)

        print(f'Decrypted: {result.hex()}')

    def do_reconnect(self, arg):
        '''
        Usage: reconnect

        Used to reconnect to the board, needed after a board restarts/is reflashed
        '''
        res = self.hcm.connect()

        if res:
            print('Connected to board.')
        else:
            print('Failure connecting.')

    def do_exit(self, arg):
        '''
        Just exiting
        '''
        print('Exiting...')
        return True

def main():
    parser = argparse.ArgumentParser(description = "Puffin CLI application")
    parser.add_argument('-p', '--port', type = str, 
                        help = 'Serial port where the hardware is connected (com/tty), not required if sim is selected')
    parser.add_argument('--sim', action = 'store_true',
                        help = 'Simulate hardware instead (helpful for dev)')
    
    args = parser.parse_args()

    PuffinShell(args).cmdloop()
