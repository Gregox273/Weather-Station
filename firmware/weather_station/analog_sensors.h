#ifndef ANALOG_SENSORS_H
#define ANALOG_SENSORS_H

/* Analog Pin Mapping */
#define UV_PIN          0
#define TEMP_PIN        1
#define LIGHT_PIN       2
#define LOW_LIGHT_PIN   3
#define V_LOW_LIGHT_PIN 4

void log_Vcc(void); 
void log_analog_reading(uint8_t id, uint8_t pin);

#endif
