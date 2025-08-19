/*
 * coms.h
 *
 *  Created on: 28 Jul 2025
 *      Author: Zipnx
 */

// this was originally a static library, but because vivado sdk was misbehaving with updating the build
// the source files where moved manually, this is ugly but it works.

#ifndef INCLUDE_COMS_H_
#define INCLUDE_COMS_H_

#include "types.h"
#include "utils.h"

typedef struct _Command {
	uint8_t 	opcode;
	uint16_t 	size;
	uint8_t* 	data;
} Command;

typedef struct _Response {
	uint16_t 	size;
	uint8_t  	flags;
	uint8_t* 	data;
} Response;


HCMSTATUS HCM_CommandReceiveDirect(HCM* module, Command* out_command);
HCMSTATUS HCM_CommandReceive(HCM* module, Command* out_command);

HCMSTATUS HCM_ResponseMake(HCM* module, Response* out_resp);
HCMSTATUS HCM_ResponseSend(HCM* module, Response* resp);




#endif /* INCLUDE_COMS_H_ */
