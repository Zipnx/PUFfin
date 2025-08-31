/*
 * aes_enc.h
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#ifndef SRC_AES_ENC_H_
#define SRC_AES_ENC_H_

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

#include "xil_io.h"
#include "xparameters.h"

#define AESENC_TIMEOUT 512

void encrypt_aes(char* key, char* plain, char* out_ciph);

#endif /* SRC_AES_ENC_H_ */
