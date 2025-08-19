
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
        print('UNIMPLEMENTED')
        print('Query available capabilities of the device')

    def do_temperature(self, arg):
        try:
            temp = self.hcm.get_temperature()
        except ValueError:
            print('[!] Error retrieving temperature')

        print('Temperature:', temp)
    
    def do_apuf(self, arg):
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

        print(f'Response: 0x{hex(response)}')

    def do_rawapuf(self, arg):
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

        print(f'Response: 0x{hex(response)}')


    def do_test(self, arg):
        print('Just checkin:', arg)


    def do_exit(self, arg):
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
