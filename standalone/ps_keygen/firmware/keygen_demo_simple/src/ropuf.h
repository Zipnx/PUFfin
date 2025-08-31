/*
 * ropuf.h
 *
 *  Created on: 30 Aug 2025
 *      Author: Zipnx
 */

#ifndef SRC_ROPUF_H_
#define SRC_ROPUF_H_

#include <stdint.h>
#include <stdbool.h>
#include "xparameters.h"
#include "xil_io.h"

void ropuf_execute(uint32_t select, uint32_t* outputs);

#endif /* SRC_ROPUF_H_ */
