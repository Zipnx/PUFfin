/*
 * aes_dec.c
 *
 *  Created on: 31 Aug 2025
 *      Author: Zipnx
 */

#include "primitives/aes_dec.h"

#define AESDEC_CTRL(module) 		module->hw_addrs.aes_dec
#define AESDEC_KEY_BASE(module) 	module->hw_addrs.aes_dec + 0x4
#define AESDEC_CIPH_BASE(module) 	module->hw_addrs.aes_dec + 0x14
#define AESDEC_PLAIN_BASE(module) 	module->hw_addrs.aes_dec + 0x24
#define AESDEC_STAT(module) 		module->hw_addrs.aes_dec + 0x34

static inline void dec_trigger_set(HCM* module, bool state) {
	// remember, its active low
	Xil_Out32(AESDEC_CTRL(module), (state) ? 0x80000000 : 0);
}

static inline bool dec_is_busy(HCM* module) {
	return (Xil_In32(AESDEC_STAT(module)) & 0x1) != 0;
}

void dec_key_set(HCM* module, const uint8_t* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESDEC_KEY_BASE(module) + (i*4), words[i]);
	}
}

void dec_ciph_set(HCM* module, const uint8_t* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESDEC_CIPH_BASE(module) + (i*4), words[i]);
	}
}

void dec_plain_get(HCM* module, uint8_t* output) {
	uint32_t* words = (uint32_t*)output;

	for (int i = 0; i < 4; i++) {
		words[i] = Xil_In32(AESDEC_PLAIN_BASE(module) + (i*4));
	}

}

HCMSTATUS aes_decrypt(HCM* module, uint8_t* key, uint8_t* ciph, uint8_t* out_plain) {

	dec_trigger_set(module, false);
	dec_key_set(module, key);
	dec_ciph_set(module, ciph);
	dec_trigger_set(module, true);

	uint32_t timeout = AESDEC_TIMEOUT;

	while(dec_is_busy(module) && timeout-- > 0);

	if (timeout <= 0)
		return HCMTIMEOUT;

	dec_trigger_set(module, false);
	dec_plain_get(module, out_plain);

	return HCMSUCCESS;
}
