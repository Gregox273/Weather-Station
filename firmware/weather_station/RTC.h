#ifndef RTC_H
#define RTC_H

#include "Arduino.h"

void rtc_setup(void);
void set_time(uint32_t current_time);
uint32_t get_timestamp(void);

#endif
