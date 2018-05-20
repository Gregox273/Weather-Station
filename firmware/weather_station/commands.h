#ifndef COMMANDS_H
#define COMMANDS_H

/* Command Bytes */
#define SD_DUMP       0x11
#define TX_ENABLE     0x81
#define TX_DISABLE    0x18
#define RTC_UPDATE    0x88
#define IDLE_UPDATE   0x44

void check_commands(void);

extern uint32_t idle_time;

#endif
