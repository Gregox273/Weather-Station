#ifndef LOGGING_H
#define LOGGING_H

/* Id Bytes */
#define ID_TEMP   0x01   
#define ID_UV     0x02
#define ID_LIGHT  0x04
#define ID_GAS    0x08
#define ID_WIND   0x18
#define ID_GPS    0x81

void logging_setup(uint8_t cs_pin);
void log_data(uint8_t id, uint8_t* buff, uint8_t len);
void dump_sd(void);

extern bool tx_flag;

#endif
