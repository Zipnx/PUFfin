/*
 * aes_dec.h
 *
 *  Created on: 31 Aug 2025
 *      Author: Zipnx
 */

#ifndef INCLUDE_PRIMITIVES_AES_DEC_H_
#define INCLUDE_PRIMITIVES_AES_DEC_H_

#include <stdint.h>
#include <stdbool.h>

#include "types.h"
#include "xil_io.h"

#define AESDEC_TIMEOUT 512

HCMSTATUS aes_decrypt(HCM* module, uint8_t* key, uint8_t* ciph, uint8_t* out_plain);

#endif /* INCLUDE_PRIMITIVES_AES_DEC_H_ */
