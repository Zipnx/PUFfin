/*
 * aes_enc.c
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#include "primitives/aes_enc.h"

#define AESENC_CTRL(module) 		module->hw_addrs.aes_enc
#define AESENC_KEY_BASE(module) 	module->hw_addrs.aes_enc + 0x4
#define AESENC_PLAIN_BASE(module) 	module->hw_addrs.aes_enc + 0x14
#define AESENC_CIPH_BASE(module) 	module->hw_addrs.aes_enc + 0x24
#define AESENC_STAT(module) 		module->hw_addrs.aes_enc + 0x34

static inline void enc_trigger_set(HCM* module, bool state) {
	// remember, its active low
	Xil_Out32(AESENC_CTRL(module), (state) ? 0x80000000 : 0);
}

static inline bool enc_is_busy(HCM* module) {
	return (Xil_In32(AESENC_STAT(module)) & 0x1) != 0;
}

void enc_key_set(HCM* module, const uint8_t* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESENC_KEY_BASE(module) + (i*4), words[i]);
	}
}

void enc_plain_set(HCM* module, const uint8_t* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESENC_PLAIN_BASE(module) + (i*4), words[i]);
	}
}

void enc_ciph_get(HCM* module, uint8_t* output) {
	uint32_t* words = (uint32_t*)output;

	for (int i = 0; i < 4; i++) {
		words[i] = Xil_In32(AESENC_CIPH_BASE(module) + (i*4));
	}

}

HCMSTATUS aes_encrypt(HCM* module, uint8_t* key, uint8_t* plain, uint8_t* out_ciph) {
	enc_trigger_set(module, false);
	enc_key_set(module, key);
	enc_plain_set(module, plain);
	enc_trigger_set(module, true);

	uint32_t timeout = AESENC_TIMEOUT;

	while(enc_is_busy(module) && timeout-- > 0);
	enc_trigger_set(module, false);

	if (timeout <= 0)
		return HCMTIMEOUT;

	enc_ciph_get(module, out_ciph);

	return HCMSUCCESS;
}
