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

/*
 * ================= README ==================
 * Since i dont have the time to make this use
 * the libhcm framework and pack the 44bit result
 * I'll just do this in the old ascii way, which will
 * be slower, by a fair bit, but it'll be functional.
 *
 * Maybe ill pack multiple responses in 1 exchange but
 * we'll see.
 *
 * Now another thing, the way i designed the rawapuf_multi
 * allows for up to 96 bits, just incase more slots need to be searched.
 * However, this will only use 44 of those. Could make it easily customizable
 * but that would prob be a waste of time for us rn.
 *
 * If I come to regret this, then cest la vie
 */

#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"

#include "apuf.h"

void display_result(uint32_t challenge) {
	uint64_t test = execute(challenge);

	if ((test & (1ll << 63)) != 0) {
		puts("ERROR Timeout");
		return;
	}

	uint32_t msb = (uint32_t)(test >> 32);
	uint32_t lsb = (uint32_t)(test & 0xffffffff);

	//printf("\nChallenge: 0x%08x\n", challenge);
	// Hardcoding stuff now for 44 bits. If we need more, god help us
	// All the todos on the PSs, the libhcm and the puffinpy module need
	// to be cleaned up post competition, this will be janky for now
	printf("0x%08x: 0x%03x%08x\n", (unsigned int)challenge, (unsigned int)msb, (unsigned int)lsb);
}

int main()
{
    init_platform();

    // i could bypass the xilio functions and do direct reads and writes, that way i'd also
    // avoid this conversion from bytes to int but tis what it is
    //char buffer[6];
    uint32_t chall;

    while (1) {
    	// Using raw bytes would require changing some settings,
    	// and rn my goal is to just make this work, even if its horribly slow
    	scanf("%08x", (unsigned int*)&chall);
    	// 6 for \n\r, which is annoying but im too lazy to change
    	//fgets(buffer, 6, stdin);

    	//if (buffer[4] != '\r') {
    	//	printf("ERROR Improper comms: %02x\n", buffer[4]);
    	//	continue;
    	//}

    	// makin sure big endian is how we roll
    	//chall = (buffer[0] << 24) | (buffer[1] << 16) | (buffer[2] << 8) | (buffer[3]);
    	display_result(chall);
    }

    cleanup_platform();
    return 0;
}
