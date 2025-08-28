/*
 * apuf.h
 *
 *  Created on: Aug 28, 2025
 *      Author: Zipnx
 */

#ifndef INCLUDE_PRIMITIVES_APUF_H_
#define INCLUDE_PRIMITIVES_APUF_H_

#include "globals.h"
#include "types.h"

#define MAX_APUF_TIMEOUT 128

HCMSTATUS APUF_execute(HCM* module, uint32_t challenge, uint32_t* response);

#endif /* INCLUDE_PRIMITIVES_APUF_H_ */
