/*
 * rocount.c
 *
 *  Created on: Aug 25, 2025
 *      Author: Zipnx
 */

#include "rocount.h"

#define ROCOUNT_BASE XPAR_ROCOUNT_AXI_V1_0_0_BASEADDR
#define ROCOUNT_CTRL ROCOUNT_BASE
#define ROCOUNT_COUNT_BASE ROCOUNT_BASE + 0x4
#define ROCOUNT_COUNT_LEN  12
#define ROCOUNT_STAT ROCOUNT_BASE + 0x34 // this might be wrong off the top of my head

static inline
void ctrl_set(uint32_t ctrl) {
	Xil_Out32(ROCOUNT_CTRL, ctrl);
}

static inline
uint32_t ctrl_get() {
	return Xil_In32(ROCOUNT_CTRL);
}

static inline
uint32_t stat_get() {
	return Xil_In32(ROCOUNT_STAT);
}

static inline
bool is_busy() {
	return (stat_get() & 0x1) != 0;
}

void trigger_set(bool enable) {
	uint32_t ctrl = ctrl_get();

	if (enable) {
		ctrl |= 0x1;
	} else {
		ctrl &= 0xfffffffe;
	}

	ctrl_set(ctrl);
}

void select_set(uint32_t select) {
	uint32_t ctrl = ctrl_get() & 0xfffffff1; // gon also zero out the 3 prev sel bits
	ctrl |= (select & 0x7) << 1;

	ctrl_set(ctrl);
}

void counts_get(uint32_t* result){

	for (int i = 0; i < ROCOUNT_COUNT_LEN; i++) {
		result[i] = Xil_In32(ROCOUNT_COUNT_BASE + i * 4);
	}

}

void execute(uint32_t sel, uint32_t* results) {
	trigger_set(false);
	select_set(sel);
	trigger_set(true);

	while(is_busy());

	trigger_set(false);
	counts_get(results);
}
