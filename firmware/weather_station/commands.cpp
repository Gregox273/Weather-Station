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
  
    //Serial.println("Checking Serial...");

    if(Serial.available()>0) {
      
      wkup = Serial.read();
      cmd = Serial.read();

      switch(cmd) {
        
         case SD_DUMP:
            
            Serial.println("Dumping SD...");
            dump_sd();
            break;
        
         case TX_ENABLE:
         
            Serial.println("Enabling TX...");
            tx_flag = true;
            break;

         case TX_DISABLE:
         
            Serial.println("Disabling TX...");
            tx_flag = false;
            break;

         case RTC_UPDATE:
         
            Serial.println("Updating RTC...");            
            rtc_update();            
            break;

         case IDLE_UPDATE:
         
            Serial.println("Updating IDLE Time...");           
            idle_update();
            break;

         default:
            Serial.println("Command Not Recognised");            
      }
            
    } else {
      
      //Serial.println("No Commands Found");
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
        Serial.println("Command Payload Read Error");
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
        Serial.print("RTC Time ");
        Serial.println(rtc_time);

        /* TODO: Update RTC Here */
    }

}


/* Update Idle Time */
void idle_update(void) {
    
    /* Read Update Period */
    uint32_t idle_data[4];
    if(extract_payload(idle_data, 4)) {
      
        /* Set Idle Time */
        idle_time = (uint32_t)(idle_data[0] | idle_data[1]<<8 | idle_data[2]<<16 | idle_data[3]<<24);
        Serial.print("Idle period set to ");
        Serial.println(idle_time);
    }
}
