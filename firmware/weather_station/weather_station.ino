#include "RTC.h"
#include "wind.h"
#include "commands.h"
#include "logging.h"
#include "analog_sensors.h"

/* State Machine Definitions */
typedef enum {
    STATE_IDLE=0, STATE_TEMP, STATE_UV, STATE_LOW_LIGHT,
    STATE_LIGHT, STATE_WIND, NUM_STATES
} state_t;

typedef state_t state_func_t(void);

/* State Functions */
state_t run_state(state_t cur_state);
static state_t do_state_idle(void);
static state_t read_sensor_temp(void);
static state_t read_sensor_uv(void);
static state_t read_sensor_low_light(void);
static state_t read_sensor_light(void);
static state_t read_sensor_wind(void);

/* State Table */
state_func_t* const state_table[NUM_STATES] = {
    do_state_idle, read_sensor_temp, read_sensor_uv, read_sensor_low_light,
    read_sensor_light, read_sensor_wind
};

/* State Table Lookup */
state_t run_state(state_t cur_state){
    return state_table[cur_state]();
};

/* Global Variables */
uint32_t idle_time = 1000;
bool tx_flag = false;


/* Setup Function */
void setup() {
  
    /* Terminal Serial Port*/
    Serial.begin(115200);

    /* Setup SD Card */
    logging_setup(10);

    /* Enable Pullup on Hall Effect */
    pinMode(5, INPUT_PULLUP);

    /* Measure VCC */
    logVcc();

    /* Setup RTC */
    rtc_setup();
}


/* Main Loop */
void loop() {

    /* Initilise State Machine */
    state_t cur_state = STATE_IDLE;

    /* Tick State Machine */
    while(true){

      /* Run Current State */
      cur_state = run_state(cur_state);

      /* Check Serial Port for Commands */
      check_commands();
    }
}


/* IDLE State */
static state_t do_state_idle(void){

    /* Measure VCC */
    logVcc();
  
    /* Sleep */
    delay(idle_time);
    
    return STATE_TEMP;
}


/* Read Temperature Sensor State */
static state_t read_sensor_temp(void){
    
    /* Take Measurement */
    log_analog_reading(ID_TEMP, TEMP_PIN);
        
    return STATE_UV;
}


/* Read UV Sensor State */
static state_t read_sensor_uv(void){

    /* Take Measurement */
    log_analog_reading(ID_UV, UV_PIN);
    
    return STATE_LOW_LIGHT;
}


/* Read Low Light Sensor State */
static state_t read_sensor_low_light(void){

    /* Take Measurement */
    log_analog_reading(ID_LOW_LIGHT, LOW_LIGHT_PIN);
    
    return STATE_LIGHT;
}


/* Read Light Sensor State */
static state_t read_sensor_light(void){

    /* Take Measurement */
    log_analog_reading(ID_LIGHT, LIGHT_PIN);
    
    return STATE_WIND;
}


/* Read Wind Sensor State */
static state_t read_sensor_wind(void){
  
    /* Take Measurement */
    log_wind_reading();
    
    return STATE_IDLE;
}
