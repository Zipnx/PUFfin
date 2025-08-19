/*
 * rawapuf.c
 *
 *  Created on: 4 Aug 2025
 *      Author: Zipnx
 */

#include "primitives/rawapuf.h"

/* RAW APUF FUNCTIONALITY
 * ======================
 * RESET 		=> slv_reg0(0)
 * CHALLENGE  	=> slv_reg1
 * RESPONSE   	=> slv_reg2
 * BUSY		 	=> slv_reg3(0)
 */

inline static uint32_t _RawAPUF_ctrl_get(HCM* module) {
	return Xil_In32(module->hw_addrs.raw_apuf);
}

inline static void _RawAPUF_ctrl_set(HCM* module, uint32_t flags) {
	Xil_Out32(module->hw_addrs.raw_apuf, flags);
}

inline static uint32_t _RawAPUF_chall_get(HCM* module) {
	return Xil_In32(module->hw_addrs.raw_apuf + 0x4);
}

inline static void _RawAPUF_chall_set(HCM* module, uint32_t challenge) {
	Xil_Out32(module->hw_addrs.raw_apuf + 0x4, challenge);
}

inline static uint32_t _RawAPUF_resp_get(HCM* module) {
	return Xil_In32(module->hw_addrs.raw_apuf + 0x8);
}

inline static uint32_t _RawAPUF_status_get(HCM* module) {
	return Xil_In32(module->hw_addrs.raw_apuf + 0x0C);
}

inline static bool _RawAPUF_is_busy(HCM* module) {
	return (_RawAPUF_status_get(module) & 0x1) != 0;
}

void _RawAPUF_toggle_trig(HCM* module, bool enable) {
	uint32_t flags = _RawAPUF_ctrl_get(module);

	if (enable) {
		_RawAPUF_ctrl_set(module, flags | 0x1);
	} else {
		_RawAPUF_ctrl_set(module, flags & 0xfffffffe);
	}
}

HCMSTATUS RawAPUF_execute(HCM* module, uint32_t challenge, uint32_t* response) {

	if (!HCMCAP_CHECK(module->capabilities, HCMCAP_RAW_APUF)) {
		return HCMCAPFAIL;
	}

	_RawAPUF_chall_set(module, challenge);
	_RawAPUF_toggle_trig(module, true);

	int timeout = MAX_RAW_APUF_TIMEOUT;

	while (_RawAPUF_is_busy(module) && --timeout > 0);

	_RawAPUF_toggle_trig(module, false);

	if (timeout <= 0) return HCMTIMEOUT;

	*response = _RawAPUF_resp_get(module);

	return HCMSUCCESS;
}











