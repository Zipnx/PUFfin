/*
 * hcm.c
 *
 *  Created on: 2 Aug 2025
 *      Author: Zipnx
 */

#include "hcm.h"
#include "primitives/rawapuf.h"

XUartPs debug_uart;
static bool debug_uart_enabled = false;

HCMSTATUS HCM_Init(HCM** module, uint32_t uart_devid) {

	INFO("\n\r=========================================================\n\r");
	INFO("Initializing HCM...");

	HCM* hcm = (HCM*)malloc(sizeof(HCM));

	if (module == NULL) return HCMALLOCFAIL;

	hcm->rx_buffer = (uint8_t*)malloc(HCM_COMS_RX_BUFLEN);

	if (hcm->rx_buffer == NULL) {
		ERROR("Unable to allocate rx buffer");
		free(hcm);
		return HCMALLOCFAIL;
	}
	OKAY("[0x%p] RX Buffer Allocated (%d bytes)", hcm->rx_buffer, HCM_COMS_RX_BUFLEN);

	hcm->tx_buffer = (uint8_t*)malloc(HCM_COMS_TX_BUFLEN);

	if (hcm->tx_buffer == NULL) {
		ERROR("Unable to allocate tx buffer");
		free(hcm->rx_buffer);
		free(hcm);
		return HCMALLOCFAIL;
	}
	OKAY("[0x%p] TX Buffer Allocated (%d bytes)", hcm->tx_buffer, HCM_COMS_TX_BUFLEN);

	hcm->version = HCM_VERSION;
	hcm->capabilities = 0x0000; // TODO: Evaluate capabilities
	hcm->permissions  = 0xFFFF; // Default direct access to all capabilities
	hcm->init_flags.initialized = true;
	hcm->init_flags.uart_initialized = false;
	hcm->init_flags.rx_paused = true;

	*module = hcm;

	HCMSTATUS result = UART_Init(hcm, uart_devid);

	if (result != HCMSUCCESS) {
		ERROR("Unable to initialize main uart coms");
		free(hcm->rx_buffer);
		free(hcm);
	}

	return result;
}

HCMSTATUS UART_Init(HCM* module, uint32_t uart_devid) {

	XUartPs_Config* config = XUartPs_LookupConfig(uart_devid);

	if (!config) {
		ERROR("Unable to evaluate config of main uart");
		return HCMUARTFAIL;
	}

	int status = XUartPs_CfgInitialize(&module->uart_ps, config, config->BaseAddress);

	if (status != XST_SUCCESS) {
		ERROR("Unable to initialize config of main uart");
		return HCMUARTFAIL;
	}

	XUartPs_SetBaudRate(&module->uart_ps, 115200);

	module->init_flags.uart_initialized = true;

	OKAY("Main UART coms setup complete");

	return HCMSUCCESS;
}

HCMSTATUS HCM_DeInit(HCM* module) {
	module->init_flags.rx_paused = true;
	if (UART_DeInit(module) != HCMSUCCESS) return HCMFAILURE;

	free(module->rx_buffer);
	free(module->tx_buffer);

	OKAY("HCM Cleanup complete");

	memset(module, 0, sizeof(HCM));
	free(module);

	return HCMSUCCESS;
}

HCMSTATUS UART_DeInit(HCM* module) {
	if (!module->init_flags.uart_initialized) return HCMFAILURE;

	XUartPs_ResetHw(module->uart_ps.Config.BaseAddress);
	module->init_flags.uart_initialized = false;

	WARN("Main UART coms cleanup complete");

	return HCMSUCCESS;
}

HCMSTATUS HCM_SetRxEnabled(HCM* module, bool enabled) {
	if (!module->init_flags.uart_initialized) return HCMUARTFAIL;

	OKAY("Set RX state to %d\n", enabled);

	module->init_flags.rx_paused = !enabled;
	return HCMSUCCESS;
}

int sysmon_await_conversion(XSysMon* inst) {
	int timeout = SYSMON_CONVERSION_WAIT_TIMEOUT;
	uint32_t status;

	DEBUG("[SYSMON] Doing XSysMon conversion");

	do {
		DEBUG("[SYSMON] Conversion attempt #%d...", SYSMON_CONVERSION_WAIT_TIMEOUT - timeout);
		status = XSysMon_GetStatus(inst);
	} while (((status & XSM_SR_EOC_MASK) == 0) && --timeout > 0);

	if (timeout <= 0) {
		ERROR("[SYSMON] Conversion timed out");
		return XST_FAILURE;
	}

	OKAY("[SYSMON] Conversion success");

	return XST_SUCCESS;
}

HCMSTATUS HCM_EnableDebugCon(uint32_t debug_uart_dev_id) {

	debug_uart_enabled = false;

	XUartPs_Config *config;
	config = XUartPs_LookupConfig(debug_uart_dev_id);

	if (!config) return HCMFAILURE;

	int status = XUartPs_CfgInitialize(&debug_uart, config, config->BaseAddress);

	if (status != XST_SUCCESS) return HCMFAILURE;

	XUartPs_SetBaudRate(&debug_uart, 115200);
	debug_uart_enabled = true;

	return HCMSUCCESS;
}

void HCM_DebugPrint(const char* fmt, ...) {

	if (fmt == NULL) return;
	if (!debug_uart_enabled) return;

	char buffer[256];
	va_list args;
	va_start(args, fmt);

	vsnprintf(buffer, sizeof(buffer), fmt, args);
	va_end(args);

	XUartPs_Send(&debug_uart, (uint8_t*)buffer, strlen(buffer));
}

HCMSTATUS HCM_EnableXSysmon(HCM* module, uint32_t sysmon_dev_id) {

	INFO("[SYSMON] Initializing XSysmon...");

	XSysMon_Config* sysmon_config;
	sysmon_config = XSysMon_LookupConfig(sysmon_dev_id);

	if (sysmon_config == NULL) {
		ERROR("[SYSMON] Unable to lookup config");
		return HCMSYSMON_CFG_FAIL;
	}

	OKAY("[SYSMON] Sysmon config lookup success");

	int status = XSysMon_CfgInitialize(
		&module->sysmon_inst,
		sysmon_config,
		sysmon_config->BaseAddress
	);

	if (status != XST_SUCCESS) {
		ERROR("[SYSMON] Unable to initialize config");
		return HCMSYSMON_INIT_FAIL;
	}

	OKAY("[SYSMON] Sysmon config initialization complete");

	status = sysmon_await_conversion(&module->sysmon_inst);

	if (status != XST_SUCCESS) return HCMSYSMON_CONV_FAIL;

	module->capabilities |= HCMCAP_XADC;

	return HCMSUCCESS;
}

HCMSTATUS HCM_Sysmon_temperature(HCM* module, float* out_temperature) {

	if (!HCMCAP_CHECK(module->capabilities, HCMCAP_XADC)) return HCMUNAVAIL;

	//INFO("[SYSMON] Getting ADC data");
	uint16_t raw_temp = XSysMon_GetAdcData(&module->sysmon_inst, XSM_CH_TEMP);
	//OKAY("[SYSMON] Got raw temp: %d", raw_temp);
	//INFO("[SYSMON] Parsing to float...");
	*out_temperature = XSysMon_RawToTemperature(raw_temp);
	//OKAY("[SYSMON] Got float temp: %.2f", *out_temperature);
	//xil_printf doesnt support %f :P
	return HCMSUCCESS;
}

HCMSTATUS HCM_EnableRawAPUF(HCM* module, uint32_t raw_apuf_base) {

	module->hw_addrs.raw_apuf = raw_apuf_base;
	module->capabilities |= HCMCAP_RAW_APUF;

	OKAY("[0x%p] Raw APUF enabled.", raw_apuf_base);

	return HCMSUCCESS;
}

HCMSTATUS HCM_EnableAPUF(HCM* module, uint32_t apuf_base) {

	module->hw_addrs.apuf = apuf_base;
	module->capabilities |= HCMCAP_APUF;

	OKAY("[0x%p] Arbiter PUF enabled.", apuf_base);

	return HCMSUCCESS;
}

HCMSTATUS HCM_EnableROPUF(HCM* module, uint32_t ropuf_base) {

	module->hw_addrs.ropuf = ropuf_base;
	module->capabilities |= HCMCAP_ROPUF;

	OKAY("[0x%p] RingOscillator PUF enabled.", ropuf_base);

	return HCMSUCCESS;
}

HCMSTATUS HCM_EnableAES(HCM* module, uint32_t aes_base) {

	module->hw_addrs.aes = aes_base;
	module->capabilities |= HCMCAP_AES;

	OKAY("[0x%p] AES Core enabled.", aes_base);

	return HCMSUCCESS;
}

// FAR TODO: This is horrific, but it has to be done right now.
//           Needs better error handling, feedback to peer
//			 and prob a goto error handler to avoid repeating the
//           same stuff over and over.
//           In general this library is a mess
HCMSTATUS HCM_CommandReceive(HCM* module, Command* out_command) {
	// this ideally shouldnt be done in coms, but i just want to get this over with

	HCMSTATUS status = HCM_CommandReceiveDirect(module, out_command);

	if (status != HCMSUCCESS) return status;

	// handle the possible commands to be executed directly from the HCM,
	// no dev outside the lib required, can be blocked by permissions

	Response resp;
	float temp;
	HCM_ResponseMake(module, &resp);

	INFO("Checking for builtin command");

	switch (out_command->opcode) {
	case OP_INFO:
		// Return hcm information
		INFO("Got INFO request from peer");
		pack_short(module->version, resp.data);
		resp.size = 2;
		status = HCM_ResponseSend(module, &resp);

		if (status != HCMSUCCESS) {
			ERROR("Error sending response to peer");
			return HCMFAILURE;
		}

		return HCMSUCCESS;

	case OP_QUERY:
		// Return available capabilities & perms
		pack_short(module->capabilities, resp.data);
		pack_short(module->permissions, resp.data + 4);
		resp.size = 4;
		status = HCM_ResponseSend(module, &resp);

		if (status != HCMSUCCESS) {
			ERROR("Error sending response to peer");
			return HCMFAILURE;
		}

		return HCMSUCCESS;

	case OP_APUF_SINGLE:
		// TODO: Execute 1 challenge on the APUF
		return HCMSUCCESS;

	case OP_APUF_BATCH:
		// TODO: Execute a variable number of challenges
		return HCMSUCCESS;

	case OP_RDTEMP:
		status = HCM_Sysmon_temperature(module, &temp);

		if (status != HCMSUCCESS) {
			pack_int(status, resp.data);

			return HCMFAILURE;
		}

		memcpy(resp.data, &temp, 4);
		resp.size = 4;
		status = HCM_ResponseSend(module, &resp);

		if (status != HCMSUCCESS) {
			return HCMFAILURE;
		}

		return HCMSUCCESS;

	case OP_RDPUFKY:
		// TODO: Read the generated key from the ROPUF
		return HCMSUCCESS;

	case OP_RAWAPUF_SINGLE:
		INFO("Executing raw apuf builtin");
		pack_int(0x41414141, resp.data);
		resp.size = 5;
		HCM_ResponseSend(module, &resp);

		return HCMSUCCESS;

		if (out_command->size != 4) {
			// TODO: Return error to user
			return HCMFAILURE;
		}

		uint32_t challenge = unpack_int(out_command->data);
		uint32_t response;

		status = RawAPUF_execute(module, challenge, &response);

		if (status != HCMSUCCESS) {
			// TODO: Again return an error to user
			return HCMFAILURE;
		}

		pack_int(response, resp.data);
		resp.size = 2;

		status = HCM_ResponseSend(module, &resp);

		if (status != HCMSUCCESS) return status;

		return HCMSUCCESS;

	}

	// Indicate that the packet should be processed by non-lib processes
	return HCMPASS;
}
