/*
 * globals.h
 *
 *  Created on: 2 Aug 2025
 *      Author: Zipnx
 *
 *  Note: I got into some win32 api trickerly recently
 *        and decided to see how the NTSTATUS is implemented
 *        A simpler status spec would work way better here.
 */

#ifndef INCLUDE_GLOBALS_H_
#define INCLUDE_GLOBALS_H_

#define DEBUG_ENABLED
#ifdef DEBUG_ENABLED

/*
#define DEBUG(fmt, ...) 	HCM_DebugPrint("[%s:%d] " fmt "\n\r", __FILE__, __LINE__, ##__VA_ARGS__)
#define INFO(fmt, ...)  	HCM_DebugPrint("[*] " fmt "\n\r", ##__VA_ARGS__)
#define OKAY(fmt, ...)  	HCM_DebugPrint("[+] " fmt "\n\r", ##__VA_ARGS__)
#define ERROR(fmt, ...)  	HCM_DebugPrint("[+] " fmt "\n\r", ##__VA_ARGS__)
#define WARN(fmt, ...)  	HCM_DebugPrint("[!] " fmt "\n\r", ##__VA_ARGS__)
*/


#define DEBUG(fmt, ...) 	xil_printf("[%s:%d] " fmt "\n\r", __FILE__, __LINE__, ##__VA_ARGS__)
#define INFO(fmt, ...)  	xil_printf("[*] " fmt "\n\r", ##__VA_ARGS__)
#define OKAY(fmt, ...)  	xil_printf("[+] " fmt "\n\r", ##__VA_ARGS__)
#define ERROR(fmt, ...)  	xil_printf("[+] " fmt "\n\r", ##__VA_ARGS__)
#define WARN(fmt, ...)  	xil_printf("[!] " fmt "\n\r", ##__VA_ARGS__)


#else

#define DEBUG(fmt, ...) ((void)0);
#define OKAY(fmt, ...)  ((void)0);
#define INFO(fmt, ...)  ((void)0);
#define ERROR(fmt, ...) ((void)0);
#define WARN(fmt, ...)  ((void)0);

#endif

/* =============== HCM VERSION SETUP ===================*/
#define HCM_MJ_VERSION 0
#define HCM_MN_VERSION 2
#define HCM_PATCH_VERSION 1

#define HCM_VERSION \
	((HCM_MJ_VERSION & 0xf) << 12) |\
	((HCM_MN_VERSION & 0xf) << 8) |\
	(HCM_PATCH_VERSION & 0xff)

/* ============= COM PARAMETERS, CAN BE OVERRIDEN =============== */
#ifndef HCM_COMS_RX_BUFLEN
#define HCM_COMS_RX_BUFLEN 0x10000
#endif

#ifndef HCM_COMS_TX_BUFLEN
#define HCM_COMS_TX_BUFLEN 0x10000
#endif

#ifndef UART_DEVICE_ID
#define UART_DEVICE_ID XPAR_PS7_UART_1_DEVICE_ID
#endif

// So far this is unused
#ifndef HCM_RECV_TIMEOUT
#define HCM_RECV_TIMEOUT -1
#endif

#define SYSMON_CONVERSION_WAIT_TIMEOUT 16

/* ================= HCM Status Codes ================== */

// I decided to use a system pretty much exactly the same
// as on windows NTSTATUS
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

typedef uint32_t HCMSTATUS;

#define HCMSTATUS_SEVERITY_SUCCESS 	0x0
#define HCMSTATUS_SEVERITY_INFO    	0x1
#define HCMSTATUS_SEVERITY_DEBUG   	0x2
#define HCMSTATUS_SEVERITY_ERROR   	0x3

#define HCMSTATUS_FACILITY_GENERIC  0x001
#define HCMSTATUS_FACILITY_COMS		0x002
#define HCMSTATUS_FACILITY_APUF		0x003
#define HCMSTATUS_FACILITY_ROPUF    0x004
#define HCMSTATUS_FACILITY_XADC		0x005

#define HCMSTATUS_SEVERITY_SHFT 	30
#define HCMSTATUS_FACILITY_SHFT		16
#define HCMSTATUS_CODE_MASK 		0xFFFF
#define HCMSTATUS_FACILITY_MASK		0x3FFF

#define HCM_MAKE_STATUS(sev, fac, code) \
    (((sev) << HCMSTATUS_SEVERITY_SHFT) | \
     (((fac) & HCMSTATUS_FACILITY_MASK) << HCMSTATUS_FACILITY_SHFT) | \
     ((code) & HCMSTATUS_CODE_MASK))

#define HCMSTATUS_GET_SEVERITY(status) 	((status >> HCMSTATUS_SEVERITY_SHFT) & 0x3)
#define HCMSTATUS_GET_FACILITY(status) 	((status >> HCMSTATUS_FACILITY_SHFT) & HCMSTATUS_FACILITY_MASK)
#define HCMSTATUS_GET_CODE(status)		(status & HCMSTATUS_CODE_MASK)

#define HCM_IS_SUCCESS(status) 	(HCMSTATUS_GET_SEVERITY(status) == HCMSTATUS_SEVERITY_SUCCESS)
#define HCM_IS_ERROR(status)	(HCMSTATUS_GET_SEVERITY(status) == HCMSTATUS_SEVERITY_ERROR)

#define HCMSUCCESS 		HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_SUCCESS, HCMSTATUS_FACILITY_GENERIC, 0x0000)
#define HCMFAILURE 		HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR,   HCMSTATUS_FACILITY_GENERIC, 0x0001)
#define HCMDENIED		HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR,   HCMSTATUS_FACILITY_GENERIC, 0x0002)
#define HCMALLOCFAIL	HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR, 	HCMSTATUS_FACILITY_GENERIC, 0x0004)
#define HCMOVERFLOW 	HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR,   HCMSTATUS_FACILITY_GENERIC, 0x0005)
#define HCMCAPFAIL		HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR,   HCMSTATUS_FACILITY_GENERIC, 0x0006)

#define HCMUNAVAIL		HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR,   HCMSTATUS_FACILITY_COMS,	0x0001)
#define HCMUARTFAIL		HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR,   HCMSTATUS_FACILITY_COMS,    0x0002)
#define HCMTIMEOUT		HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_INFO,    HCMSTATUS_FACILITY_COMS,    0x0003)
#define HCMMALFORMED	HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR,   HCMSTATUS_FACILITY_COMS, 	0x0004)
// used for when the packet received had an opcode that was not processed by the HCM automatically,
// in that case the application handles the request
#define HCMPASS			HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_INFO,	HCMSTATUS_FACILITY_COMS, 	0x0005)

#define HCMSYSMON_CFG_FAIL 	HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR, HCMSTATUS_FACILITY_XADC, 0x0001)
#define HCMSYSMON_INIT_FAIL HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR, HCMSTATUS_FACILITY_XADC, 0x0002)
#define HCMSYSMON_CONV_FAIL HCM_MAKE_STATUS(HCMSTATUS_SEVERITY_ERROR, HCMSTATUS_FACILITY_XADC, 0x0003)

#endif /* INCLUDE_GLOBALS_H_ */
