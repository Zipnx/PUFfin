/*
 * rawapuf.h
 *
 *  Created on: 4 Aug 2025
 *      Author: Zipnx
 */

#ifndef INCLUDE_PRIMITIVES_RAWAPUF_H_
#define INCLUDE_PRIMITIVES_RAWAPUF_H_

#include "types.h"

#define MAX_RAW_APUF_TIMEOUT 2048

HCMSTATUS RawAPUF_execute(HCM* module, uint32_t challenge, uint32_t* response);

#endif /* INCLUDE_PRIMITIVES_RAWAPUF_H_ */
