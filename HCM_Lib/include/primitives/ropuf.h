/*
 * ropuf.h
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#ifndef INCLUDE_PRIMITIVES_ROPUF_H_
#define INCLUDE_PRIMITIVES_ROPUF_H_

#include <stdint.h>
#include <stdbool.h>
#include "types.h"
#include "xparameters.h"
#include "xil_io.h"

HCMSTATUS ropuf_execute(HCM* module, uint32_t select, uint8_t* out_keybytes, bool pshash);

#endif /* INCLUDE_PRIMITIVES_ROPUF_H_ */
