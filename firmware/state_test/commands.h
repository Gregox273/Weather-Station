#ifndef COMMANDS_H
#define COMMANDS_H

/* Command Bytes */
#define SD_DUMP       'a'
#define TX_ENABLE     'b'
#define TX_DISABLE    'c'
#define RTC_UPDATE    'd'
#define IDLE_UPDATE   'e'

void check_commands(void);

#endif
