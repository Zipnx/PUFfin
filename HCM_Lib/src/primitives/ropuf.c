/*
 * ropuf.c
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#include "primitives/ropuf.h"
#include "utils/sha256.h"

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
#define KEYGEN_CTRL(module) (module->hw_addrs.ropuf)
#define KEYGEN_KEY0(module) module->hw_addrs.ropuf + 0x04
#define KEYGEN_KEY1(module) module->hw_addrs.ropuf + 0x08
#define KEYGEN_KEY2(module) module->hw_addrs.ropuf + 0x0C
#define KEYGEN_KEY3(module) module->hw_addrs.ropuf + 0x10
#define KEYGEN_STAT(module) module->hw_addrs.ropuf + 0x14

static inline
uint32_t ctrl_get(HCM* module) {
	return Xil_In32(KEYGEN_CTRL(module));
}

static inline
void ctrl_set(HCM* module, uint32_t ctrl) {
	Xil_Out32(KEYGEN_CTRL(module), ctrl);
}

static inline
uint32_t stat_get(HCM* module) {
	return Xil_In32(KEYGEN_STAT(module));
}

static inline
bool is_busy(HCM* module) {
	return (stat_get(module) & 0x1) != 0;
}

void select_set(HCM* module, uint32_t select) {
	uint32_t ctrl = ctrl_get(module) & 0xfffffff1;
	ctrl_set(module, ctrl | ((select & 0x7) << 1));
}

void trigger_set(HCM* module, bool state) {
	uint32_t ctrl = ctrl_get(module);

	if (state) {
		ctrl_set(module, ctrl |= 0x1);
	} else {
		ctrl_set(module, ctrl &= 0xfffffffe);
	}
}

void resp_get(HCM* module, uint32_t* outputs) {

	outputs[0] = Xil_In32(KEYGEN_KEY0(module));
	outputs[1] = Xil_In32(KEYGEN_KEY1(module));
	outputs[2] = Xil_In32(KEYGEN_KEY2(module));
	outputs[3] = Xil_In32(KEYGEN_KEY3(module));

}

HCMSTATUS ropuf_execute(HCM* module, uint32_t select, uint8_t* out_keybytes, bool pshash) {
	if (!HCMCAP_CHECK(module->capabilities, HCMCAP_ROPUF)) {
		return HCMCAPFAIL;
	}


	trigger_set(module, false);
	select_set(module, select);
	trigger_set(module, true);

	while (is_busy(module));

	uint32_t registers[4];

	trigger_set(module, false);
	resp_get(module, registers);

    for (int i = 0; i < 4; i++) {
    	out_keybytes[i*4] 		= (registers[i] >> 24) & 0xff;
    	out_keybytes[i*4 + 1]	= (registers[i] >> 16) & 0xff;
    	out_keybytes[i*4 + 2]  	= (registers[i] >> 8)  & 0xff;
    	out_keybytes[i*4 + 3] 	= (registers[i] & 0xff);
    }

    if (!pshash) return HCMSUCCESS;

    BYTE plain[32];

    memset(plain, 0, 32);
    memcpy(plain, out_keybytes, 16);

    BYTE hash[SHA256_BLOCK_SIZE];
    SHA256_CTX ctx;

    sha256_init(&ctx);
    sha256_update(&ctx, (const BYTE*)plain, 32);
    sha256_final(&ctx, hash);

    for (int i = 0; i < 16; i++) {
    	out_keybytes[i] = hash[i] ^ hash[i + 16];
    }

    return HCMSUCCESS;
}
