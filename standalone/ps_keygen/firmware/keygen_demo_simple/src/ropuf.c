/*
 * ropuf.c
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#include "ropuf.h"

/*
 * # Format:
 * rst :    slv_reg0(31)
 * trigger: slv_reg0(0)
 * sel:     slv_reg0(3 downto 1)
 * key: 	slv_reg1, slv_reg2, slv_reg3, slv_reg4
 * busy:    slv_reg5(0)
 *
 */

#define KEYGEN_BASE XPAR_SYSKEYGEN_AXI_V1_0_0_BASEADDR
#define KEYGEN_CTRL KEYGEN_BASE
#define KEYGEN_KEY0 KEYGEN_BASE + 0x04
#define KEYGEN_KEY1 KEYGEN_BASE + 0x08
#define KEYGEN_KEY2 KEYGEN_BASE + 0x0C
#define KEYGEN_KEY3 KEYGEN_BASE + 0x10
#define KEYGEN_STAT KEYGEN_BASE + 0x14

static inline
uint32_t ctrl_get() {
	return Xil_In32(KEYGEN_CTRL);
}

static inline
void ctrl_set(uint32_t ctrl) {
	Xil_Out32(KEYGEN_CTRL, ctrl);
}

static inline
uint32_t stat_get() {
	return Xil_In32(KEYGEN_STAT);
}

static inline
bool is_busy() {
	return (stat_get() & 0x1) != 0;
}

void select_set(uint32_t select) {
	uint32_t ctrl = ctrl_get() & 0xfffffff1;
	ctrl_set(ctrl | ((select & 0x7) << 1));
}

void trigger_set(bool state) {
	uint32_t ctrl = ctrl_get();

	if (state) {
		ctrl_set(ctrl |= 0x1);
	} else {
		ctrl_set(ctrl &= 0xfffffffe);
	}
}

void resp_get(uint32_t* outputs) {

	outputs[0] = Xil_In32(KEYGEN_KEY0);
	outputs[1] = Xil_In32(KEYGEN_KEY1);
	outputs[2] = Xil_In32(KEYGEN_KEY2);
	outputs[3] = Xil_In32(KEYGEN_KEY3);

}

void ropuf_execute(uint32_t select, uint32_t* outputs) {
	trigger_set(false);
	select_set(select);
	trigger_set(true);

	while (is_busy());

	trigger_set(false);
	resp_get(outputs);
}
