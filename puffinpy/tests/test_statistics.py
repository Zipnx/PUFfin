
from puffinpy import Command, HCMCommander
from puffinpy._command import Opcode

# Made this just to test that pytest executes properly
def test_device():
    com = HCMCommander(port = 'COM4')
    cmd = Command(Opcode.READ_TEMP)

    result = com.push_command(cmd)
    print(result)

    assert True
     
