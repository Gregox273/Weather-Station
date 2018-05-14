#ifndef ANALOG_SENSORS_H
#define ANALOG_SENSORS_H

/* Analog Pin Mapping */
#define TEMP_PIN    0
#define UV_PIN      1
#define LIGHT_PIN   2

void log_analog_reading(uint8_t id, uint8_t pin);

#endif
