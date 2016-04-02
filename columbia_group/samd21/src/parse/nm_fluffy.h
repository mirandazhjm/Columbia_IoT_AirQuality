/*
 * nm_fluffy.h
 *
 * Created: 2014-11-05 오후 5:25:24
 *  Author: jini
 */ 

#include "nm_bsp.h"
#include "m2m_types.h"
#ifndef NM_FLUFFY_H_
#define NM_FLUFFY_H_

#define MAIN_M2M_AP_SEC                  M2M_WIFI_SEC_OPEN
#define MAIN_M2M_AP_WEP_KEY              "1234567890"
#define MAIN_M2M_AP_SSID_MODE            SSID_MODE_VISIBLE

#define MAIN_HTTP_PROV_SERVER_DOMAIN_NAME    "atmelconfig.com"

#define MAIN_M2M_DEVICE_NAME                 "FutureAir_"//"WINC1500_00:00"
#define MAIN_MAC_ADDRESS                     {0xf8, 0xf0, 0x05, 0x45, 0xD4, 0x84}

static tstrM2MAPConfig gstrM2MAPConfig = {
	MAIN_M2M_DEVICE_NAME, 1, 0, WEP_40_KEY_STRING_SIZE, MAIN_M2M_AP_WEP_KEY, (uint8)MAIN_M2M_AP_SEC, MAIN_M2M_AP_SSID_MODE
};

static CONST char gacHttpProvDomainName[] = MAIN_HTTP_PROV_SERVER_DOMAIN_NAME;

static uint8 gau8MacAddr[] = MAIN_MAC_ADDRESS;
static sint8 gacDeviceName[] = MAIN_M2M_DEVICE_NAME;

uint8_t provisioning;
uint8_t wifiConnected(void);
void fluffy_wifi_noti_cb(uint8_t u8MsgType, void * pvMsg);

uint8_t fluffy_check_home_ap(char* ssid, char* pw, uint8_t secType);

void fluffy_set_home_ap_info(char* ssid, char* pw, uint8_t secType, uint8_t fileWrite);
int fluffy_remove_home_ap_info(void);

uint8_t fluffy_load_fluffy_info(void);
void fluffy_set_fluffy_info(uint8_t fileWrite);
int fluffy_remove_fluffy_info(void);

int fluffy_device_config_add_key( const char* key, const char* label, const char* value );
const char * fluffy_device_config_get_value( const char *key );
const char * fluffy_device_config_get_value_by_index( int index );
void fluffy_device_config_set_value( int index, char* value );
const char * fluffy_device_config_get_key( int index );
const char * fluffy_device_config_get_label( int index );
int fluffy_device_config_get_count( void );
	
void fluffy_wifi_ap_mode(int8_t isAPEnable, uint8_t* macAddr);

uint8_t fluffy_get_ap_mode_completed(void);

void fluffy_wifi_stat_mode(int8_t isStaEnable);

uint8_t fluffy_get_wifi_connected(void);

#endif /* NM_FLUFFY_H_ */