/*
 * coms.c
 *
 *  Created on: 28 Jul 2025
 *      Author: Zipnx
 */

#include "serialcom/com.h"

HCMSTATUS HCM_CommandReceiveDirect(HCM* module, Command* out_command) {

	if (!module || module->init_flags.rx_paused || !module->init_flags.uart_initialized)
		return HCMFAILURE;

	uint8_t opcode;
	int bytes_recv = 0;

	// TODO: Will add a timeout
	//int timeout = 0;

	do {
		bytes_recv = XUartPs_Recv(&module->uart_ps, &opcode, 1);
	} while (bytes_recv != 1);

	//printf("Opcodes: %c\n", opcode);

	uint8_t raw_pckt_size[2];
	size_t total_recv = 0;

	while (total_recv < 2) {
		bytes_recv = XUartPs_Recv(&module->uart_ps, raw_pckt_size+total_recv, 2 - total_recv);
		total_recv += bytes_recv;
	}

	if (total_recv != 2) return HCMFAILURE;

	uint16_t packet_size = unpack_short(raw_pckt_size);

	//printf("Size: %hi\n", packet_size);

	if (packet_size >= HCM_COMS_RX_BUFLEN) {
		// TODO: Return a size error to the peer
		return HCMFAILURE;
	}

	total_recv = 0;

	while (total_recv < packet_size) {
		bytes_recv = XUartPs_Recv(&module->uart_ps, module->rx_buffer + total_recv, packet_size - total_recv);
		total_recv += bytes_recv;
	}

	if (total_recv != packet_size) return HCMMALFORMED;

	out_command->opcode = opcode;
	out_command->size   = packet_size;
	out_command->data   = module->rx_buffer;


	return HCMSUCCESS;
}

HCMSTATUS HCM_ResponseMake(HCM* module, Response* out_resp) {
	out_resp->data = module->tx_buffer + 3;
	out_resp->size = 0;
	out_resp->flags = 0;

	return HCMSUCCESS;
}

HCMSTATUS HCM_ResponseSend(HCM* module, Response* resp) {
	uint32_t total_size = resp->size + 3;

	if (total_size > HCM_COMS_TX_BUFLEN) {
		return HCMOVERFLOW;
	}

	pack_short(resp->size, module->tx_buffer);
	module->tx_buffer[2] = resp->flags;

	uint32_t bytes_sent = 0;

	do {
		uint32_t sent = XUartPs_Send(
			&module->uart_ps,
			module->tx_buffer + bytes_sent,
			total_size - bytes_sent
		);

		if (sent <= 0){
			return HCMFAILURE;
		}

		bytes_sent += sent;
	} while (bytes_sent < total_size);

	return HCMSUCCESS;
}

