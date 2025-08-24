/*
 * types.h
 *
 *  Created on: Aug 18, 2025
 *      Author: Zipnx
 */

#include <stdint.h>
#include <stdbool.h>

#include "globals.h"
#include "xuartps.h"
#include "xsysmon.h"

#ifndef INCLUDE_TYPES_H_
#define INCLUDE_TYPES_H_

typedef struct _HW_ADDRS {
	uint32_t raw_apuf;
	uint32_t apuf;
	uint32_t ropuf;
	uint32_t aes;
} HW_ADDRS;

typedef struct _HCM {
	uint16_t version;
	uint16_t capabilities;
	uint16_t permissions;

	XUartPs uart_ps;

	uint8_t* rx_buffer;
	uint8_t* tx_buffer;

	XSysMon sysmon_inst;

	union {
		char flags;
		struct {
			bool initialized	  : 1;
			bool uart_initialized : 1;
			bool rx_paused        : 1;
			bool reserved1        : 1;
			bool reserved2		  : 1;
			bool reserved3		  : 1;
			bool reserved4		  : 1;
			bool reserved5		  : 1;
		};
	} init_flags;

	HW_ADDRS hw_addrs;
} HCM;

// 1 byte is prob fine
typedef enum {
	OP_INFO   		= 0x00,
	OP_QUERY    	= 0x01,
	OP_APUF_SINGLE	= 0x02,
	OP_RDTEMP 		= 0x03,
	OP_RDPUFKY		= 0x04,
	OP_APUF_BATCH   = 0x05,
	OP_AES_ENC		= 0x06,
	OP_AES_DEC		= 0x07,

	// debugs:
	OP_ROCOUNTS_RD 		= 0xfd,
	OP_RAWAPUF_BATCH 	= 0xfe,
	OP_RAWAPUF_SINGLE  	= 0xff,
} opcode_t;

/* ================ HCM Capabilities ================= */
#define HCMCAP_XADC 		0x0001
#define HCMCAP_RAW_APUF 	0x0002
#define HCMCAP_RAW_ROPUF	0x0004
#define HCMCAP_APUF			0x0008
#define HCMCAP_ROPUF		0x0010
#define HCMCAP_AES_ENC		0x0020
#define HCMCAP_PRNG			0x0040
#define HCMCAP_PHYS_UAC		0x0080
#define HCMCAP_DEBUG_CON	0x0100
#define HCMCAP_AES_DEC		0x0200
#define HCMCAP_RESERVED6	0x0400
#define HCMCAP_RESERVED5	0x0800
#define HCMCAP_RESERVED4	0x1000
#define HCMCAP_RESERVED3	0x2000
#define HCMCAP_RESERVED2	0x4000
#define HCMCAP_RESERVED1	0x8000

#define HCMCAP_CHECK(cap, flag) ((cap & flag) != 0)
#define HCMCAP_SET(cap, flag) (cap | flag);


#endif /* INCLUDE_TYPES_H_ */


