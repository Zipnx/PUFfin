/*
 * aes_dec.c
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */


#include "aes_dec.h"

#define AESDEC_BASE XPAR_AES_DEC_AXI_V1_0_0_BASEADDR
#define AESDEC_CTRL 		AESDEC_BASE
#define AESDEC_KEY_BASE 	AESDEC_BASE + 0x4
#define AESDEC_CIPH_BASE 	AESDEC_BASE + 0x14
#define AESDEC_PLAIN_BASE 	AESDEC_BASE + 0x24
#define AESDEC_STAT 		AESDEC_BASE + 0x34

static inline void dec_trigger_set(bool state) {
	// remember, its active low
	Xil_Out32(AESDEC_CTRL, (state) ? 0x80000000 : 0);
}

static inline bool dec_is_busy() {
	return (Xil_In32(AESDEC_STAT) & 0x1) != 0;
}

void dec_key_set(const char* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESDEC_KEY_BASE + (i*4), words[i]);
	}
}

void dec_ciph_set(const char* key) {
	const uint32_t* words = (const uint32_t*) key;

	for (int i = 0; i < 4; i++) {
		Xil_Out32(AESDEC_CIPH_BASE + (i*4), words[i]);
	}
}

void dec_plain_get(char* output) {
	uint32_t* words = (uint32_t*)output;

	for (int i = 0; i < 4; i++) {
		words[i] = Xil_In32(AESDEC_PLAIN_BASE + (i*4));
	}

}

void decrypt_aes(char* key, char* ciph, char* plain) {

	dec_trigger_set(false);
	dec_key_set(key);
	dec_ciph_set(ciph);
	dec_trigger_set(true);

	uint32_t timeout = AESDEC_TIMEOUT;

	while(dec_is_busy() && timeout-- > 0);

	if (timeout <= 0)
		puts("Timeout detected");

	dec_trigger_set(false);
	dec_plain_get(plain);

}


