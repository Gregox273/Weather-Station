#include "RTC.h"
#include "Arduino.h"
#include "commands.h"
#include "logging.h"

void rtc_update(void);
void idle_update(void);
bool extract_payload(uint32_t* data, uint8_t num_bytes);


/* Check Serial Buffer for Commands */
void check_commands(void) {

    uint8_t wkup;
    uint8_t cmd;

    if(Serial.available()>0) {
      
        wkup = Serial.read();
        cmd = Serial.read();
  
        switch(cmd) {
          
           case SD_DUMP:
              
              log_event(SD_DUMP);
              dump_sd();
              break;
          
           case TX_ENABLE:
           
              log_event(TX_ENABLE);  
              tx_flag = true;
              break;
  
           case TX_DISABLE:
           
              log_event(TX_DISABLE);  
              tx_flag = false;
              break;
  
           case RTC_UPDATE:
         
              rtc_update();            
              break;
  
           case IDLE_UPDATE:
           
              idle_update();
              break;
  
           default:
              log_event(UNKNOWN_COMMAND);         
        }    
    }
}


/* Extract Payload */
bool extract_payload(uint32_t* data, uint8_t num_bytes) {

    /* Read Payload */
    uint8_t i=0;
    while(Serial.available() && i<num_bytes){

        data[i] = Serial.read();
        i+=1;
    }

    /* Check Bytes Read */
    if(i==(num_bytes)) {
        return true;  
    } else {
        log_event(PAYLOAD_ERROR);
        return false;  
    }
}


/* Update RTC */
void rtc_update(void) {
    
    /* Read Time */
    uint32_t rtc_time;
    uint32_t time_data[4];
    if(extract_payload(time_data, 4)) {
      
        /* Set RTC Time */
        rtc_time = (uint32_t)(time_data[0] | time_data[1]<<8 | time_data[2]<<16 | time_data[3]<<24);
        set_time(rtc_time);
    }
}


/* Update Idle Time */
void idle_update(void) {
    
    /* Read Update Period */
    uint32_t idle_data[4];
    if(extract_payload(idle_data, 4)) {
      
        /* Set Idle Time */
        idle_time = (uint32_t)(idle_data[0] | idle_data[1]<<8 | idle_data[2]<<16 | idle_data[3]<<24);
        log_event(IDLE_UPDATE);
    }
}
