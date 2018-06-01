#ifndef LOGGING_H
#define LOGGING_H

/* Data Packet Id Bytes */
#define ID_TEMP         0x01   
#define ID_UV           0x02
#define ID_LIGHT        0x04
#define ID_LOW_LIGHT    0x08
#define ID_V_LOW_LIGHT  0x10
#define ID_WIND         0x20
#define ID_VCC          0x40

/* Event Id Bytes */
#define RTC_ERROR       0x80
#define RTC_UPDATE      0x81
#define IDLE_UPDATE     0x82
#define PAYLOAD_ERROR   0x83
#define UNKNOWN_COMMAND 0x84
#define TX_ENABLE       0x85
#define TX_DISABLE      0x86
#define SD_DUMP         0x87
#define SD_WIPE         0x88

/* End of Dump */
#define DUMP_END        0x90

/* LED Pin */
#define LED_PIN   2

void logging_setup(uint8_t cs_pin);
void log_event(uint8_t event);
void log_data(uint8_t id, uint8_t* buff, uint8_t len);
void dump_sd(void);
void wipe_sd(void);

extern bool tx_flag;

#endif
