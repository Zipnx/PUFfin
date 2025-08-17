
import cmd

class PuffinShell(cmd.Cmd):
    intro = '''Welcome to the PuffinPy Interactive shell
    ======================================
    From here you can query and execute available
    functionalities on any device that implements
    the libhcm firmware.
    '''
    prompt = "puffin> "
    
    def do_test(self, arg):
        print('Just checkin:', arg)


    def do_exit(self, arg):
        print('Exiting...')
        return True

def main():
    PuffinShell().cmdloop()
