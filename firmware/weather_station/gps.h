#ifndef GPS_H
#define GPS_H

/* UART Pin Mapping */
#define RX_PIN    4

void gps_setup(void);
void log_gps_reading(void);

#endif
