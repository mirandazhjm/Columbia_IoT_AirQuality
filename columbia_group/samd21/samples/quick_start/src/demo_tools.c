/*
 * Copyright (c) 2014, Sensirion AG
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * * Redistributions of source code must retain the above copyright notice, this
 *   list of conditions and the following disclaimer.
 *
 * * Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 * * Neither the name of Sensirion AG nor the names of its
 *   contributors may be used to endorse or promote products derived from
 *   this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * \file
 *
 * \brief Sensirion SHTC1 demo helper functions.
 *
 * The demo_tools contains helper functions needed by the example. Delay
 * functions, port pins (used for LED/button), usart communication and
 * i2c communication initialization are here.
 *
 * There is also a function provided to the main application which allows to
 * directly send a string (printf-style) over the serial connection to
 * the terminal on host PC.
 */

#include <asf.h>
#include <stdarg.h>
#include "demo_tools.h"
#include "i2c_master.h"

/* used to init usart communication to host PC */
struct usart_module usart_instance;

/* used to init I2C software module. */
struct i2c_master_module i2c_master_instance;

void configure_i2c_master(void)
{
    /* initialize config structure and software module */
    struct i2c_master_config config_i2c_master;
    i2c_master_get_config_defaults(&config_i2c_master);

    /* change buffer timeout to something longer */
    config_i2c_master.buffer_timeout = 10000;

    /* initialize and enable device with config. */
    i2c_master_init(&i2c_master_instance, SERCOM2, &config_i2c_master);
    i2c_master_enable(&i2c_master_instance);
}

void configure_usart(void)
{
    struct usart_config config_usart;
    usart_get_config_defaults(&config_usart);

    config_usart.baudrate = 9600;
    config_usart.mux_setting = EDBG_CDC_SERCOM_MUX_SETTING;
    config_usart.pinmux_pad0 = EDBG_CDC_SERCOM_PINMUX_PAD0;
    config_usart.pinmux_pad1 = EDBG_CDC_SERCOM_PINMUX_PAD1;
    config_usart.pinmux_pad2 = EDBG_CDC_SERCOM_PINMUX_PAD2;
    config_usart.pinmux_pad3 = EDBG_CDC_SERCOM_PINMUX_PAD3;

    while (usart_init(&usart_instance, EDBG_CDC_MODULE, &config_usart)
            != STATUS_OK){
    }

    usart_enable(&usart_instance);
}

void usart_i2c_init()
{
    delay_init();
    configure_usart();
    configure_i2c_master();
}

void print_to_terminal(const char* format, ...)
{
    va_list a_list;
    char serial_message[100];
    uint8_t length = 0;

    va_start(a_list, format);
    vsnprintf(serial_message, sizeof(serial_message), format, a_list);
    va_end(a_list);
    while (serial_message[length++]);
    usart_write_buffer_wait(&usart_instance, (uint8_t*) serial_message, length);
}

inline int ishex(int x)
{
	return	(x >= '0' && x <= '9')	||
	(x >= 'a' && x <= 'f')	||
	(x >= 'A' && x <= 'F');
}

int decode(const char *s, char *dec)
{
	char *o;
	const char *end = s + strlen(s);
	int c;
	
	for (o = dec; s <= end; o++) {
		c = *s++;
		if (c == '+') c = ' ';
		else if (c == '%' && (	!ishex(*s++)	||
		!ishex(*s++)	||
		!sscanf(s - 2, "%2x", &c)))
		return -1;
		
		if (dec) *o = c;
	}
	
	return o - dec;
}