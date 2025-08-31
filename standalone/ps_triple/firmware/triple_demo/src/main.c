/*
 * main.c
 *
 *  Created on: 31 Aug 2025
 *      Author: Zipnx
 */

#include "hcm.h"
#include "xparameters.h"

int main(void) {
	HCM* module;
	HCMSTATUS result;

	// idc about the result
	result = HCM_EnableDebugCon(XPAR_PS7_UART_0_DEVICE_ID);
	result = HCM_Init(&module, XPAR_PS7_UART_1_DEVICE_ID);

	INFO("Init Result: %08x", result);

	if (result != HCMSUCCESS)
		return XST_FAILURE;

	INFO("Init complete");

	HCM_EnableXSysmon(module, XPAR_SYSMON_0_DEVICE_ID);

	HCM_EnableAPUF(module, XPAR_SYSAUTH_AXI_V1_0_0_BASEADDR);
	HCM_EnableROPUF(module, XPAR_SYSKEYGEN_AXI_V1_0_0_BASEADDR);
	HCM_EnableAESEnc(module, XPAR_AES_ENC_AXI_V1_0_0_BASEADDR);
	HCM_EnableAESDec(module, XPAR_AES_DEC_AXI_V1_0_0_BASEADDR);

	HCM_SetRxEnabled(module, true);
	HCM_UnlockAll(module);

	Command cmd;

	while (1) {
		result = HCM_CommandReceive(module, &cmd);

		if (result != HCMPASS) continue;

		break;
	}
}
