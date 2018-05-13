#include "commands.h"

/* State Machine Definitions */
typedef enum {
    STATE_IDLE=0, STATE_TEMP, STATE_UV, STATE_LIGHT, STATE_GAS,
    STATE_WIND, STATE_GPS, NUM_STATES
} state_t;

typedef state_t state_func_t(void);

/* State Functions */
state_t run_state(state_t cur_state);
static state_t do_state_idle(void);
static state_t read_sensor_temp(void);
static state_t read_sensor_uv(void);
static state_t read_sensor_light(void);
static state_t read_sensor_gas(void);
static state_t read_sensor_wind(void);
static state_t read_sensor_gps(void);

/* State Table */
state_func_t* const state_table[NUM_STATES] = {
    do_state_idle, read_sensor_temp, read_sensor_uv, read_sensor_light,
    read_sensor_gas, read_sensor_wind, read_sensor_gps
};

/* State Table Lookup */
state_t run_state(state_t cur_state){
    return state_table[cur_state]();
};


/* Setup Function */
void setup() {
  
    /* Terminal Serial Port*/
    Serial.begin(115200);
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
  
    //Serial.println("Entering IDLE State");
    
    delay(1000);
    return STATE_TEMP;
}


/* Read Temperature Sensor State */
static state_t read_sensor_temp(void){
  
    //Serial.println("Entering TEMP State");
    
    return STATE_UV;
}


/* Read UV Sensor State */
static state_t read_sensor_uv(void){
  
    //Serial.println("Entering UV State");
    
    return STATE_LIGHT;
}


/* Read Light Sensor State */
static state_t read_sensor_light(void){
  
    //Serial.println("Entering LIGHT State");
    
    return STATE_GAS;
}


/* Read Gas Sensor State */
static state_t read_sensor_gas(void){
  
    //Serial.println("Entering GAS State");
    
    return STATE_WIND;
}


/* Read Wind Sensor State */
static state_t read_sensor_wind(void){
  
    //Serial.println("Entering WIND State");
    
    return STATE_GPS;
}


/* Read GPS State */
static state_t read_sensor_gps(void){
  
    //Serial.println("Entering GPS State");
    
    return STATE_IDLE;
}
