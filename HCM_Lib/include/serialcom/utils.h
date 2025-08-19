/*
 * utils.h
 *
 *  Created on: 28 Jul 2025
 *      Author: Zipnx
 */

#ifndef INCLUDE_UTILS_H_
#define INCLUDE_UTILS_H_

#include <stdio.h>
#include <stdint.h>

uint16_t read_size(void);

uint32_t unpack_int(uint8_t* data);
void pack_int(uint32_t value, uint8_t* buffer);

uint16_t unpack_short(uint8_t* data);
void pack_short(uint16_t value, uint8_t* buffer);

#endif /* INCLUDE_UTILS_H_ */
