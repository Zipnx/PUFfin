/*
 * apuf.c
 *
 *  Created on: Aug 19, 2025
 *      Author: Zipnx
 */

#include "apuf.h"

#define APUF_BASE 	XPAR_APUF_RAW_MULTI_AXI_V_0_BASEADDR
#define APUF_CTRL 	APUF_BASE			// slv_reg0
#define APUF_CHALL	APUF_BASE + 0x04	// slv_reg1
#define APUF_RESP0  APUF_BASE + 0x08	// slv_reg2
#define APUF_RESP1  APUF_BASE + 0x0C	// slv_reg3
#define APUF_RESP2  APUF_BASE + 0x10 	// slv_reg4
#define APUF_STAT   APUF_BASE + 0x14	// slv_reg5

#define EXEC_TIMEOUT 128

static inline
uint32_t ctrl_get() {
	return Xil_In32(APUF_CTRL);
}

static inline
void ctrl_set(uint32_t ctrl) {
	Xil_Out32(APUF_CTRL, ctrl);
}

static inline
void chall_set(uint32_t chall) {
	Xil_Out32(APUF_CHALL, chall);
}

uint64_t resp_get() {
	uint64_t lsbs = (uint64_t)Xil_In32(APUF_RESP0);
	uint64_t msbs = (uint64_t)Xil_In32(APUF_RESP1);
	msbs &= 0xfff;
	// If need be the 3rd slv_reg can be used too

	// You wont believe how much a stupid bug here cost.
	// and i bet, if you are reading this, you can guess what i messed up
	return (msbs << 32) | lsbs;
}

static inline
uint32_t stat_get() {
	return Xil_In32(APUF_STAT);
}

static inline
bool is_busy() {
	return (stat_get() & 0x1) != 0;
}

void set_trigger(bool state) {
	// normally i would read in ctrl and modify it, but i
	// forgot this doesnt have any other controls other than
	// the trigger
	Xil_Out32(APUF_CTRL, (state) ? 0x1 : 0x0);
}

uint64_t execute(uint32_t challenge) {

	// just to be sure
	set_trigger(false);
	chall_set(challenge);
	set_trigger(true);

	int timeout = EXEC_TIMEOUT;

	while (is_busy() && --timeout > 0);

	set_trigger(false);

	if (timeout <= 0) return (1ll << 63);

	return resp_get();
}


