#include <SD.h>
#include <SPI.h>
#include "Arduino.h"
#include "logging.h"

File logFile;

void logging_setup(uint8_t cs_pin) {

    tx_flag = false;
  
    /* SD Card Init - Blocking */
    while(!SD.begin(cs_pin)) {
        Serial.println("SD Card Not Found!");
    } 
    return;
}



void log_data(uint8_t id, uint8_t* buff, uint8_t len){
  
    uint8_t timestamp;
    
    /* TODO: Timestamp packet here */
    timestamp = 100;
    
    /* Write Data to Log File */
    logFile = SD.open("log.bin", FILE_WRITE);
    if (logFile) {
      logFile.write(timestamp);
      logFile.write(id);
      logFile.write(buff, len);
      logFile.close();
    } else {
      Serial.println("Error Writing to File");
    }

    /* Vomit Over USB */
    if(tx_flag) {
      Serial.write(timestamp);
      Serial.write(id);
      Serial.write(buff, len);
    }
}

void dump_sd(void) {
  
    logFile = SD.open("log.bin", FILE_READ);
    if (logFile) {
      /* Dump Until EOF */
      while (logFile.available()) {
        Serial.write(logFile.read());
      }
      logFile.close();
    } else {
      Serial.println("Error Dumping File");
    }
}
