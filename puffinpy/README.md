
# Puffin Crypto Module Core

This module's purpose is to interact with the PUFort hardware over serial.
It will be used in the GUI application, as well as other benchmarking scripts,
therefore it was better for it to be a independent module

## Usage

To use this protocol in the other project, run:

```
This is for a complete install
pip install -e .[dev,cli,gui]
```

This assumes a virtualenv is already made and used. Afterwards the module can be used
as such:

```python
# [TODO WITH NEW FORMAT] 
```

When installed, you can also run the cli or gui app by running
```
# For the cli:
puffincli <SERIALPORT>
# For the gui:
puffingui
```

Note that the result varies depending on the opcode, and the data (if needed) that are passed
to the hardware

## Protocol

Unlike the previous ascii command-response system i'd made for quick PS testing,
this properly encodes, inorder to lower the data required for interaction.

Although a bit trickier than the pure ascii one, making it also harder to debug,
it is still really barebones and a C implementation is not that big a challenge.

If this was meant to be extremely future-proof a version field would be really 
needed, but this is not going to be deployed so no biggie.

### Command Packet

A command packet is formed as:

| Opcode | Payload Length (N) | Payload |
|--------|--------------------|---------|
| 1 byte | 2 bytes (uint16\_t) | N bytes | 

### Response Packet

| Length (N) | Flags  | Response |
|------------|--------|----------|
| 2 bytes    | 1 byte | N bytes  |

Rn only 1 of the flags is used, but since i needed it as a boolean
might as well make this into a bitfield and have room for expansion

| Bit  | Flag Name        | Use                                    |
|------|------------------|----------------------------------------|
| 0x01 | Error flag       | Indicate that the response is an error |
| 0x02 | Reserved         | To be established                      |
| 0x04 | Reserved         | To be established                      |
| 0x08 | Reserved         | To be established                      |
| 0x10 | Reserved         | To be established                      |
| 0x20 | Reserved         | To be established                      |
| 0x40 | Reserved         | To be established                      |
| 0x80 | Reserved         | To be established                      |
