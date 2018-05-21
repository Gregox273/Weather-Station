#ifndef COMMANDS_H
#define COMMANDS_H

/* Command Bytes */
#define CMD_SD_DUMP       0x11
#define CMD_TX_ENABLE     0x81
#define CMD_TX_DISABLE    0x18
#define CMD_RTC_UPDATE    0x88
#define CMD_IDLE_UPDATE   0x44

void check_commands(void);

extern uint32_t idle_time;

#endif
