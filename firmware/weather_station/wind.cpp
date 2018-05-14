#include "wind.h"
#include "Arduino.h"
#include "logging.h"
#include "FreqCounter.h"

/* N.B. Connect Sensor to Pin 5 */

/* Measure and Log Frequency */
void log_wind_reading(void) {
  
    uint16_t frq;
    uint8_t data[2] = {0,0};

    /* Start Counter with 1s Gate Time */
    FreqCounter::f_comp=100;
    FreqCounter::start(1000);  
  
    /* Wait for Measurement */
    while (FreqCounter::f_ready == 0) 
  
    frq=(uint16_t)FreqCounter::f_freq;
    
    /* Log Reading */
    data[0] = (uint8_t)(frq & 0xFF);
    data[1] = (uint8_t)((frq >> 8) & 0xFF);    
    log_data(ID_WIND, data, 2);
    
    /* Debug */
    Serial.print("Wind Freq: ");
    Serial.println(frq);

}
