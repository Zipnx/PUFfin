/*
 * aes_dec.h
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#ifndef SRC_AES_DEC_H_
#define SRC_AES_DEC_H_

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

#include "xil_io.h"
#include "xparameters.h"

#define AESDEC_TIMEOUT 512

void decrypt_aes(char* key, char* ciph, char* plain);

#endif /* SRC_AES_DEC_H_ */
