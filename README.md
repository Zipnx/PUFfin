
# PUFfin

Git repo for the AMD OpenHardware Competition 2025
Team: AOHW25_255

Our project is a hardware security platform that can be used by developers to utilize outputs
from PUFs for cryptographic purposes. This repository includes:

 - PUFfin IP Cores for 2 PUFs (Ring Oscillator & Arbiter PUF), including AXI wrappers
 - Static Library for Xilinx SDK, which allows for easy use of the components
 - The PuffinPy python module, that can be used to interact with devices using the static library in firmware
 - PuffinPy also includes a CLI and a GUI application for easy testing
 - Projects in the ./standalone/ directory, which implement specific components, with 1, ps_triple enabling all of them

|Board|Zybo Z7-10|
|-----|----------|
|Vivado/SDK Version|2018.3|
|Python Version|3.12 (earlier is probably fine)|

## Made By (AOHW25_255)
 - Supervisor: Prof. Mihalis Psarakis
 - Sofianos Lymouris 
 - Nikos Pilichos
 - Vasilis Giannoulis

## Executing the Demo:
First download the .bit, .elf and .tcl files from the releases tab:
[Demo Files For ps_triple](https://github.com/Zipnx/PUFfin/releases/tag/demo)

Then run xsct and execute the following:

```tcl
connect
targets

# Pick one of the ARM cores
# Here we use the 2nd option

targets 2
source ps7_init.tcl
ps7_init
ps7_post_config
fpga -file ./ps_triple.bit
dow ./triple_demo.elf
con
```

After the bitstream and the elf are loaded, make sure you have created a 
virtual environment for python, in the root project directory and install the requirements as such:

```
python -m venv ./venv

# If using linux enter the venv with
source venv/bin/activate
# If using windows then enter the venv with
.\venv\Scripts\activate

pip install -r requirements.txt
```

Then you can test the board's capabilities by running either

```
puffincli -p <SERIALPORT>
or 
puffingui <SERIALPORT>
```

## Note On Packaging Issues

While developing, especially in the later stages we came a cross multiple problems
with the vivado 2018.3 packager. In many cases the packaging does not result in the files
in the iprepo directory to update.

As a result, we cannot ensure that the IP core project will work as expected, you might need
to wipe their respective iprepo entry and repackage, which might still not resolve the issue.

Unfortunatelly this is the reason why the RO normalization and a quick ECC module based on Hamming
codes, while implemented, is not used.

In future work we plan to move to a later and more stable version of Vivado

## Resources Used
 1. tobiasrj20 
    - Saved us lots of time: https://github.com/tobiasrj20/Vivado-Version-Control-Example
 2. B-Con
    - SHA 256 C Implementation: https://github.com/B-Con/crypto-algorithms/blob/master/sha256.h
 3. simoasnaghi
    - Used as a reference for designing the APUFs https://github.com/simoasnaghi/FPGA_PUF
 4. hadipurh
    - AES VHDL Ip cores for enc/dev: https://github.com/hadipourh/AES-VHDL
 5. Gabalo
    - Used as a reference for designing the ROs https://github.com/Gabalo/RO_PUF
 6. chaseruskin
    - Hamming Code VHDL project used for making the RO ECC (currently not in the design) https://github.com/chaseruskin/hamming
 7. dsaves
    - VHDL SHA-256 Implementation (currently not in the design) https://github.com/dsaves/SHA-256

## Papers Used

Maes, R., Van Herrewege, A., Verbauwhede, I. (2012). PUFKY: A Fully Functional PUF-Based Cryptographic Key Generator. In: Prouff, E., Schaumont, P. (eds) Cryptographic Hardware and Embedded Systems – CHES 2012. CHES 2012. Lecture Notes in Computer Science, vol 7428. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-33027-8_18
