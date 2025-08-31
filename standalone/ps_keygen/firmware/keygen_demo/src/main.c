/*
 * main.c
 *
 *  Created on: 30 Aug 2025
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
	HCM_EnableROPUF(module, XPAR_SYSKEYGEN_AXI_V1_0_0_BASEADDR);

	// TODO: Make an error for this, if a read happens with rx disabled
	HCM_SetRxEnabled(module, true);
	HCM_UnlockAll(module);

	Command cmd;
	Response resp;

	while (1) {
		INFO("Receiving...");
		result = HCM_CommandReceive(module, &cmd);

		if (result != HCMPASS) continue;

		INFO("Recv result: 0x%08x", result);

		HCM_ResponseMake(module, &resp);
		resp.size = 16;
		HCM_ResponseSend(module, &resp);

		OKAY("Sent response.");
		break;
	}
}
