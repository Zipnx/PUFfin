/*
 * utils.h
 *
 *  Created on: 28 Jul 2025
 *      Author: Zipnx
 */

#include "serialcom/utils.h"

uint16_t read_size(void) {
	char msb = getchar();
	char lsb = getchar();

	if (msb == EOF || lsb == EOF) return 0;

	return ((uint16_t)msb << 8) | (uint16_t) lsb;
}

uint32_t unpack_int(uint8_t* data) {
	return (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3];
}

void pack_int(uint32_t value, uint8_t* buffer) {
	buffer[0] = (value >> 24) & 0xff;
	buffer[1] = (value >> 16) & 0xff;
	buffer[2] = (value >>  8) & 0xff;
	buffer[3] = value & 0xff;
}

uint16_t unpack_short(uint8_t* data) {
	return (data[0] << 8) | data[1];
}

void pack_short(uint16_t value, uint8_t* buffer) {
	buffer[0] = (value >> 8) & 0xff;
	buffer[1] = value & 0xff;
}
