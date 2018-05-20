#include <Wire.h>
#include "RTC.h"
#include "RTClib.h"
#include "Arduino.h"
#include "logging.h"

RTC_DS1307 rtc;


/* Setup RTC */
void rtc_setup(void) {

  /* Init RTC */
  if (! rtc.begin()) {
    Serial.println("RTC Not Found!");
    while (1);
  }

  /* Update RTC with Compile Time */
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
}


/* Get UNIX Time */
uint32_t get_timestamp(void) {
  
    DateTime now = rtc.now();
  
    /* Debug */
    Serial.println(now.unixtime());
    
    return now.unixtime();
}


/* Update RTC */
void set_time(uint32_t current_time) {

    /* Set Time from UNIX Timestamp */
    rtc.adjust(DateTime(current_time));  
}
