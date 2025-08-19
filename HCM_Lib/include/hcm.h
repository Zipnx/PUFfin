/*
 * hcm.h
 *
 *  Created on: 2 Aug 2025
 *      Author: Zipnx
 */

#ifndef INCLUDE_HCM_H_
#define INCLUDE_HCM_H_

#include "globals.h"
#include "types.h"
#include "serialcom/com.h"

#include "xuartps.h"
#include "xsysmon.h"


HCMSTATUS HCM_Init(HCM** module, uint32_t uart_devid);
HCMSTATUS HCM_DeInit();

HCMSTATUS HCM_SetRxEnabled(HCM* module, bool enabled);

HCMSTATUS UART_Init(HCM* module, uint32_t uart_devid);
HCMSTATUS UART_DeInit(HCM* module);

HCMSTATUS HCM_EnableDebugCon(uint32_t debug_uart_dev_id);
void HCM_DebugPrint(const char* fmt, ...);

HCMSTATUS HCM_EnableXSysmon(HCM* module, uint32_t sysmon_dev_id);
HCMSTATUS HCM_Sysmon_temperature(HCM* module, float* out_temperature);
HCMSTATUS HCM_EnableRawAPUF(HCM* module, uint32_t raw_apuf_base);
HCMSTATUS HCM_EnableAPUF(HCM* module, uint32_t apuf_base);
HCMSTATUS HCM_EnableROPUF(HCM* module, uint32_t ropuf_base);
HCMSTATUS HCM_EnableAES(HCM* module, uint32_t aes_base);

static inline void HCM_LockAll(HCM* module) { module->permissions = 0x0000; }
static inline void HCM_Lock(HCM* module, uint16_t cap) { module->permissions &= (0xffff ^ cap); }
static inline void HCM_UnlockAll(HCM* module) { module->permissions = 0xffff; }
static inline void HCM_Unlock(HCM* module, uint16_t cap) { module->permissions |= cap; }

HCMSTATUS HCM_CommandReceive(HCM* module, Command* out_command);

#endif /* INCLUDE_HCM_H_ */
