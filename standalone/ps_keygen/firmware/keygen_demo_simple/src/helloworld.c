/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */

#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "ropuf.h"
#include "sha256.h"

int main()
{
    init_platform();
    uint32_t key[4];
    char keybytes[32];
    BYTE hash[SHA256_BLOCK_SIZE];

    memset(keybytes, 0, 32);

    ropuf_execute(2, key);

    for (int i = 3; i >= 0; i--) {
    	//printf("%08x", (unsigned int)key[i]);
    	keybytes[i*4] 		= (key[i] >> 24) & 0xff;
    	keybytes[i*4 + 1]	= (key[i] >> 16) & 0xff;
    	keybytes[i*4 + 2]  	= (key[i] >> 8)  & 0xff;
    	keybytes[i*4 + 3] 	= (key[i] & 0xff);
    }
    //puts("\n");


    puts("====== RAW RESPONSE =======\n");
    for (int i = 0; i < 16; i++) {
    	printf("%02x", keybytes[i]);
    }
    puts("\n");

    SHA256_CTX ctx;
    sha256_init(&ctx);
    sha256_update(&ctx, (const BYTE*)keybytes, 32);
    sha256_final(&ctx, hash);

    for (int i = 0; i < 16; i++) {
    	hash[i] ^= hash[i + 16];
    }

    puts("====== HASHED RESPONSE =======\n");
        for (int i = 0; i < 16; i++) {
        	printf("%02x", hash[i]);
        }
        puts("\n");

    cleanup_platform();
    return 0;
}
