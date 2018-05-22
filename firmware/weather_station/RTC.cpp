#include "RTC.h"
#include "RTClib.h"
#include "Arduino.h"
#include "logging.h"

RTC_DS1307 rtc;

/* Setup RTC */
void rtc_setup(void) {

    /* Init RTC */
    if(!rtc.begin()) {
        
        /* RTC Communication Error */
        log_event(RTC_ERROR);
  
        /* Error Out */
        while(true) {
            digitalWrite(LED_PIN, LOW);
            delay(100);
            digitalWrite(LED_PIN, HIGH);
            delay(100); 
        }
    }
}


/* Get UNIX Time */
uint32_t get_timestamp(void) {
  
    DateTime now = rtc.now();
    return now.unixtime();
}


/* Update RTC */
void set_time(uint32_t current_time) {

    /* Set Time from UNIX Timestamp */
    rtc.adjust(DateTime(current_time)); 

    log_event(RTC_UPDATE);
}
