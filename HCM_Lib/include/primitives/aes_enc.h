/*
 * aes_enc.h
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#ifndef INCLUDE_PRIMITIVES_AES_ENC_H_
#define INCLUDE_PRIMITIVES_AES_ENC_H_

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

#include "types.h"
#include "xil_io.h"

#define AESENC_TIMEOUT 512

HCMSTATUS aes_encrypt(HCM* module, uint8_t* key, uint8_t* plain, uint8_t* out_ciph);

#endif /* INCLUDE_PRIMITIVES_AES_ENC_H_ */
