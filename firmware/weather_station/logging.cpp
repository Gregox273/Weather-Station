#include <SD.h>
#include <SPI.h>
#include "RTC.h"
#include "Arduino.h"
#include "logging.h"

File logFile;

/* Setup SD Card */
void logging_setup(uint8_t cs_pin) {

    tx_flag = false;
  
    /* SD Card Init - Blocking */
    while(!SD.begin(cs_pin)) {
        Serial.println("SD Card Not Found!");
    } 
    return;
}


/* Log Data Packet */
void log_data(uint8_t id, uint8_t* buff, uint8_t len){
     
    /* Timestamp Packet */
    uint32_t timestamp = get_timestamp();
    uint8_t time_data[4];

    time_data[0] = (uint8_t)(timestamp & 0xFF);
    time_data[1] = (uint8_t)((timestamp >> 8) & 0xFF);
    time_data[2] = (uint8_t)((timestamp >> 16) & 0xFF);
    time_data[3] = (uint8_t)((timestamp >> 24) & 0xFF);
    
    
    /* Write Data to Log File */
    logFile = SD.open("log.bin", FILE_WRITE);
    if (logFile) {
      logFile.write(time_data, 4);
      logFile.write(id);
      logFile.write(buff, len);
      logFile.close();
    } else {
      Serial.println("Error Writing to File");
    }

    /* Vomit Over USB */
    if(tx_flag) {
      Serial.write(time_data, 4);
      Serial.write(id);
      Serial.write(buff, len);
    }
}


/* Log Event */
void log_event(uint8_t event){
     
    /* Timestamp Packet */
    uint32_t timestamp = get_timestamp();
    uint8_t time_data[4];

    time_data[0] = (uint8_t)(timestamp & 0xFF);
    time_data[1] = (uint8_t)((timestamp >> 8) & 0xFF);
    time_data[2] = (uint8_t)((timestamp >> 16) & 0xFF);
    time_data[3] = (uint8_t)((timestamp >> 24) & 0xFF);
    
    
    /* Write Data to Log File */
    logFile = SD.open("log.bin", FILE_WRITE);
    if (logFile) {
      logFile.write(time_data, 4);
      logFile.write(event);
      logFile.close();
    } else {
      Serial.println("Error Writing to File");
    }

    /* Vomit Over USB */
    if(tx_flag) {
      Serial.write(time_data, 4);
      Serial.write(event);
    }
}


/* Dump SD Card */
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
