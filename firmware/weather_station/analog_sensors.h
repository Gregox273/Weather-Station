#ifndef ANALOG_SENSORS_H
#define ANALOG_SENSORS_H

/* Analog Pin Mapping */
#define TEMP_PIN      1
#define UV_PIN        0
#define LIGHT_PIN     3
#define LOW_LIGHT_PIN 2


void logVcc(void); 
void log_analog_reading(uint8_t id, uint8_t pin);

#endif
