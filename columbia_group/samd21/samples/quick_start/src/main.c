/**
 *
 * \file
 *
 * \brief WINC1500 Example.
 *
 * Copyright (c) 2015 Atmel Corporation. All rights reserved.
 *
 * \asf_license_start
 *
 * \page License
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. The name of Atmel may not be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY ATMEL "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT ARE
 * EXPRESSLY AND SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * \asf_license_stop
 *
 */

/** \mainpage
 * \section intro Introduction
 * This example demonstrates how to connect to the Parse server
 * using the WINC1500 Wi-Fi module.<br>
 * It uses the following hardware:
 * - the SAMD21 Xplained Pro.
 * - the WINC1500 on EXT1.
 *
 * \section files Main Files
 * - main.c : Initialize the WINC1500 Wi-Fi module and connect to the Parse server.
 *
 * \section usage Usage
 * -# Configure below code in this file for AP and the Parse information to be connected.
 * \code
 *    char ssid[] = "YOUR_NETWORK_ID";
 *    char pw[] = "YOUR_NETWORK_PASS";
 *    int secType = 2;
 *    parseClient = parseInitialize(YOUR_APP_ID, YOUR_CLIENT_ID);
 * \endcode
 * -# Build the program and download it into the board.
 * -# On the computer, open and configure a terminal application as following.
 * \code
 *    Baud Rate : 115200
 *    Data : 8bit
 *    Parity bit : none
 *    Stop bit : 1bit
 *    Flow control : none
 * \endcode
 *
 * \section compinfo Compilation Information
 * This software was written for the GNU GCC compiler using Atmel Studio 6.2
 * Other compilers may or may not work.
 *
 * \section contactinfo Contact Information
 * For further information, visit
 * <A href="http://www.atmel.com">Atmel</A>.\n
 */

#include "asf.h"
#include <math.h>
#include "parse.h"
#include "parse/parse_impl.h"
#include "parse/nm_fluffy.h"
#include "driver/include/m2m_wifi.h"
#include "socket/include/socket.h"
#include "conf_nvm.h"

#include <stdio.h>

#include "demo_tools.h"
#include "shtc1.h"
#include "ams_voc.h"

#define STRING_EOL    "\r\n"
#define STRING_HEADER "-- Atmel WINC1500 : Fluffy --"STRING_EOL	\
	"-- "BOARD_NAME " --"STRING_EOL	\
	"-- Compiled: "__DATE__ " "__TIME__ " --"STRING_EOL
	
/* Parse instance */
ParseClient parseClient = NULL;

static void requestCallback(ParseClient client, int error, int httpStatus, const char *httpResponseBody)
{
	if (0 != error) {
		print_to_terminal("requestCallback / error code %d / Error !!!!!\r\n", error);
		return;
	}

	print_to_terminal("requestCallback : 0x%x, %d, %d, %s\r\n\r\n", client, error, httpStatus, httpResponseBody);
}

void pushCallback(ParseClient client, int error, const char *data)
{
	if (0 != error) {
		print_to_terminal("pushCallback / error code %d / Error !!!!!\r\n", error);
		return;
	}

	print_to_terminal("pushCallback : 0x%x, %s\r\n", client, data);
}

/**
 * \brief Main application function.
 *
 * Application entry point.
 *
 * \return program return value.
 */
int main(void)
{	
	int bart_cc = 0;
	
	
	//char ssid[] = "Michael_iPhone";
	//char pw[] = "tigerwang";

	//char ssid[] = "Civic_Hall_Annex";
	//char pw[] = "156lafayette";

	char ssid[] = "Civic Hall";
	char pw[] = "156lafayette";

	//char ssid[] = "asaaa";
	//char pw[] = "ahsan100";
	
	//char ssid[] = "FiOS-DNB09";
	//char pw[] = "lash44pod7642mice";
	
	/* 0 - no security, 1 - WEP, 2 - WPA */
	int secType = M2M_WIFI_SEC_OPEN;
	//if pw is not empty change to secure mode!
	if(strlen(pw)){
		print_to_terminal("WPA is used\n");
		secType = M2M_WIFI_SEC_WPA_PSK;
	}
	
	
	/* Initialize the board. */
	system_init();

	/* initialize temperature sensor */
	//at30tse_init();
	//int temp_reading = at30tse_read_temperature() * 100;
	
	// initializes USART and I2C communication 
    usart_i2c_init();
	
	print_to_terminal(STRING_HEADER);
	//uint32 systemfreq =system_cpu_clock_get_hz();
	//print_to_terminal("the cpu clock is: %d",systemfreq);

	/* rest api */
	char timestamp[] = "\"2015-12-17\"";
	int id = 0;
	
	/* values read from sensor, encoded as integer numbers */
    int temp, rh, dew;
	int co2, voc;

    // temperature (°C), dew point (°C), and relative humidity (%RH)
    double temp_f, rh_f, dew_f, k_f;
	
    /* statuses of I2C communication */
    enum status_code shtc1_connected;
    enum status_code shtc1_read_status;
	enum status_code voc_read_status;



    /* test if sensor is connected */
	shtc1_connected = shtc1_probe(&i2c_master_instance);
	printf(" shtc1 sensor is %s\r\n\n",
	shtc1_connected ? "present" : "not present");

	/* Configure Non-Volatile Memory */
	configure_nvm();

	/* InItialize WiFI Connection via WINC1500 */
	if (LOCAL_PARSE_SUCCESS != initWifiModule()) {
		print_to_terminal("main / initWifiModule Error !!!!!\r\n");
		return -1;
	}

	/* Load or Provision WiFi Settings */
	int debug_2 = loadSettingsOrProvisionBoard(ssid, pw, secType);
	print_to_terminal("debug_2: loadSettingsOrProvisionBoard return value = %d\r\n\n", debug_2);
	
	/* Connect to WiFi Station */
	while (1) {
		if (M2M_WIFI_MODE_STA == localParseEventLoop(NULL)) {
			print_to_terminal("main / WiFi connection is done\r\n");
			break;
		}
	}
	
	/* obtain MAC address */
	uint8 pu8MacAddr[6]; 
	if (M2M_SUCCESS != m2m_wifi_get_mac_address(pu8MacAddr)) {
		print_to_terminal("Unable to read MAC address!\r\n");
		return -1;
	}	
	for(int i=0; i<6; i++)
	{
		print_to_terminal("mac address [%d] = 0x%x\n", i, pu8MacAddr[i]);	
	}	
	char macAddr[16] = "";
	sprintf(macAddr, "0x%02x%02x%02x%02x%02x%02x\0", pu8MacAddr[0], pu8MacAddr[1], pu8MacAddr[2], pu8MacAddr[3], pu8MacAddr[4], pu8MacAddr[5]);
	print_to_terminal("mac address = %s\n", macAddr);
	
	parseClient = parseInitialize("6ImqHzoPTWbZPTx8ePUMJxpywRqSqc6leMOZp8MJ", "kjQ27Hqm2H97fBXbUmYbGCbnedeH3WZtX2GvU2Cj");	
	
	delay_s(3);
	print_to_terminal("delayed 3 sec\n");
		
	while(1)
	{
		/************** Get VOC and CO2 equivalent reading *************************/
		voc_read_status = ams_sensor_read(&i2c_master_instance, &voc, &co2);
		//print_to_terminal("voc_read_status = 0x%x\n", voc_read_status);
		
		if (voc_read_status == STATUS_OK)
		{
			print_to_terminal("voc = %d ppb\t", voc);
			print_to_terminal("co2 = %d ppm\n", co2);
		}
		else
		{
			print_to_terminal("AMS Measurement failed. Extension-Board disconnected?\n");
		}
		
		/**************** Get temp + humidity CLOCK STRETCHING *********************/
		shtc1_read_status = shtc1_read_hpm_sync(&i2c_master_instance, &temp, &rh);
		//print_to_terminal("shtc1_read_status = 0x%x\n", shtc1_read_status);
		
		if (shtc1_read_status == STATUS_OK)
		{
			print_to_terminal("temp = %d\t", temp);
			print_to_terminal("rh = %d\t", rh);
			
			temp_f = temp / 1000.0f;
			rh_f = rh / 1000.0f;
			
			k_f = (log10(rh_f) - 2) / 0.4343 + (17.62 * temp_f) / (243.12 + temp_f);
			dew_f = 243.12 * k_f / (17.62 - k_f);
			dew = dew_f * 1000;
			print_to_terminal("dew = %d\n\n", dew);
		}
		else
		{
			print_to_terminal("SHTC1 Measurement failed. Extension-Board disconnected?\n");
		}
		/**********************get the dust sensor reading**********************************/

		/* POST to REST API Server */
		// create air quality POST command body
		
		temp = temp_f; rh = rh_f;
		
		char httpRequestBody[256] = "";
		sprintf(httpRequestBody, "{\"temperature\": %d,\"humidity\": %d,\"dewpoint\": %d, \"co2\": %d, \"voc\": %d, \"device\": \"%s\"}", temp, rh, dew, co2, voc, macAddr);
		print_to_terminal("*** POST COMMAND *** \n%s", httpRequestBody);
		
		// send temp POST command to REST API server
		parseSendRequest(parseClient, "POST", "/1/test1data", httpRequestBody, requestCallback);
		
		// add delay
		print_to_terminal("RUN COUNTER => %d\n", ++bart_cc);
		delay_s(9);
	}

	return 0;
}
