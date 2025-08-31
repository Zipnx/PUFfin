
# PUFfin

Git repo for the AMD OpenHardware Competition 2025

|Board|Zybo Z7-10|
|-----|----------|
|Vivado/SDK Version|2018.3|
|Python Version|3.12 (an earlier one can be used)|

[README WIP]

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
