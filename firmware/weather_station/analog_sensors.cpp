#include "Arduino.h"
#include "logging.h"
#include "analog_sensors.h"


/* Logs Raw ADC Reading */
void log_analog_reading(uint8_t id, uint8_t pin) {
  
    int i = 0;
    long result = 0;
    const int num_avg = 20;
    long adc_res[num_avg];  
    uint8_t reading[2] = {0,0};

    for(i=0; i<num_avg; i++) {
        
        /* Read Voltage */
        adc_res[i] = analogRead(pin);
        result += adc_res[i];
    }

    result = result/num_avg;

    /* Log Voltage */
    reading[0] = (uint8_t)(result & 0xFF);
    reading[1] = (uint8_t)((result >> 8) & 0xFF);    
    log_data(id, reading, 2);

    /* Debug */
    //Serial.print("adc ");
    //Serial.print(pin);
    //Serial.print(" = ");
    //Serial.println(result);
} 


/* Logs Supply Voltage in mV */
void log_Vcc() {
  
    const int num_avg = 20;
    long result[num_avg];
    uint8_t data[2];
    long supply = 0;
    long sum = 0;
    int i = 0;
    
    /* Set ADMUX to 1.1v Band Gap with AVREF */
    ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
    delay(2);
  
    /* Average Measurements */
    for(i=0; i<num_avg; i++) {
  
      /* Initiate Conversion */
      ADCSRA |= _BV(ADSC); 
  
      /* Wait for Conversion to Complete */
      while (bit_is_set(ADCSRA,ADSC));
  
      /* Read Conversion Result */
      result[i] = ADCL;
      result[i] |= ADCH<<8;
  
      /* Back Calculate AVREF - 1024 x 1108.9mV = 1135514 */
      result[i] = 1135514L / result[i];
      sum += result[i];
    }
    
    /* Log Reading */
    supply = sum/num_avg;
    data[0] = (uint8_t)(supply & 0xFF);
    data[1] = (uint8_t)((supply >> 8) & 0xFF);    
    log_data(ID_VCC, data, 2);
}
