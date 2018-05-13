#include"Arduino.h"
#include "commands.h"

bool extract_payload(uint8_t* data, uint8_t num_bytes);


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
            break;
        
         case TX_ENABLE:
            Serial.println("Enabling TX...");
            break;

         case TX_DISABLE:
            Serial.println("Disabling TX...");
            break;

         case RTC_UPDATE:
            Serial.println("Updating RTC...");
            
            /* Read Time */
            uint8_t time_data[4];
            if(extract_payload(time_data, 4)){
              
                /*Set RTC Time*/
                Serial.println(time_data[0]);
                Serial.println(time_data[1]);
                Serial.println(time_data[2]);
                Serial.println(time_data[3]);  
            }
            
            break;

         case IDLE_UPDATE:
            Serial.println("Updating IDLE Time...");
            break;

         default:
            Serial.println("Command Not Recognised");            
        }
      
    } else {
      
      //Serial.println("No Commands Found");
    }
}


/* Extract Payload */
bool extract_payload(uint8_t* data, uint8_t num_bytes) {

    /* Read Payload */
    uint8_t i=0;
    while(Serial.available()&& i<num_bytes){

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
