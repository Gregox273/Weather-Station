#include "Arduino.h"
#include "logging.h"
#include "analog_sensors.h"

void log_analog_reading(uint8_t id, uint8_t pin) {
  
    int adc_res;
    uint8_t reading[2] = {0,0};

    /* Read Voltage */
    adc_res = analogRead(pin);

    /* Log Voltage */
    reading[0] = (uint8_t)(adc_res & 0xFF);
    reading[1] = (uint8_t)((adc_res >> 8) & 0xFF);    
    log_data(id, reading, 2);
}
