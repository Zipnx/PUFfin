/*
 * apuf.c
 *
 *  Created on: Aug 28, 2025
 *      Author: Zipnx
 */

#include "primitives/apuf.h"

/*
 * Yes, this is pretty much the same as the raw apuf.
 * I wish to forget i had to do this
 */

/* APUF FUNCTIONALITY
 * ======================
 * TRIGGER 		=> slv_reg0(0)
 * RO_XCHG_TRIG => slv_reg0(1)
 * RESET 		=> slv_reg0(31)
 * CHALLENGE  	=> slv_reg1
 * RESPONSE   	=> slv_reg2
 * BUSY		 	=> slv_reg3(0)
 * RO_LOADED 	=> slv_reg3(1)
 */

inline static uint32_t _APUF_ctrl_get(HCM* module) {
	return Xil_In32(module->hw_addrs.apuf);
}

inline static void _APUF_ctrl_set(HCM* module, uint32_t flags) {
	Xil_Out32(module->hw_addrs.apuf, flags);
}

inline static uint32_t _APUF_chall_get(HCM* module) {
	return Xil_In32(module->hw_addrs.apuf + 0x4);
}

inline static void _APUF_chall_set(HCM* module, uint32_t challenge) {
	Xil_Out32(module->hw_addrs.apuf + 0x4, challenge);
}

inline static uint32_t _APUF_resp_get(HCM* module) {
	return Xil_In32(module->hw_addrs.apuf + 0x8);
}

inline static uint32_t _APUF_status_get(HCM* module) {
	return Xil_In32(module->hw_addrs.apuf + 0x0C);
}

inline static bool _APUF_is_busy(HCM* module) {
	return (_APUF_status_get(module) & 0x1) != 0;
}

void _APUF_toggle_trig(HCM* module, bool enable) {
	uint32_t flags = _APUF_ctrl_get(module);

	if (enable) {
		_APUF_ctrl_set(module, flags | 0x1);
	} else {
		_APUF_ctrl_set(module, flags & 0xfffffffe);
	}
}

HCMSTATUS APUF_execute(HCM* module, uint32_t challenge, uint32_t* response) {

	if (!HCMCAP_CHECK(module->capabilities, HCMCAP_APUF)) {
		return HCMCAPFAIL;
	}

	_APUF_chall_set(module, challenge);
	_APUF_toggle_trig(module, true);

	int timeout = MAX_APUF_TIMEOUT;

	while (_APUF_is_busy(module) && --timeout > 0);

	_APUF_toggle_trig(module, false);

	if (timeout <= 0) return HCMTIMEOUT;

	*response = _APUF_resp_get(module);

	return HCMSUCCESS;
}



