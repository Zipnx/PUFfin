/*
 * aes_enc.c
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#include "aes_enc.h"

#define AESENC_BASE XPAR_AES_ENC_AXI_V1_0_0_BASEADDR
#define AESENC_CTRL 		AESENC_BASE
#define AESENC_KEY_BASE 	AESENC_BASE + 0x4
#define AESENC_PLAIN_BASE 	AESENC_BASE + 0x14
#define AESENC_CIPH_BASE 	AESENC_BASE + 0x24
#define AESENC_STAT 		AESENC_BASE + 0x34

static inline void trigger_set(bool state) {
	// remember, its active low
	Xil_Out32(AESENC_CTRL, (state) ? 0x80000000 : 0);
}

static inline bool is_busy() {
	return (Xil_In32(AESENC_STAT) & 0x1) != 0;
}

void key_set(const char* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESENC_KEY_BASE + (i*4), words[i]);
	}
}

void plain_set(const char* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESENC_PLAIN_BASE + (i*4), words[i]);
	}
}

void ciph_get(char* output) {
	uint32_t* words = (uint32_t*)output;

	for (int i = 0; i < 4; i++) {
		words[i] = Xil_In32(AESENC_CIPH_BASE + (i*4));
	}

}

void encrypt_aes(char* key, char* plain, char* out_ciph) {

	trigger_set(false);
	key_set(key);
	plain_set(plain);
	trigger_set(true);

	uint32_t timeout = AESENC_TIMEOUT;

	while(is_busy() && timeout-- > 0);

	if (timeout <= 0)
		puts("Timeout detected");

	trigger_set(false);
	ciph_get(out_ciph);

}
