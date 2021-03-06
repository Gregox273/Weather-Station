#include "RTC.h"
#include "wind.h"
#include "commands.h"
#include "logging.h"
#include "LowPower.h"
#include "analog_sensors.h"

/* Sleep Function */
void go_to_sleep(uint32_t sleep_time);

/* State Machine Definitions */
typedef enum {
    STATE_IDLE=0, STATE_TEMP, STATE_UV, STATE_LIGHT,
    STATE_LOW_LIGHT, STATE_V_LOW_LIGHT, STATE_WIND, NUM_STATES
} state_t;

typedef state_t state_func_t(void);

/* State Functions */
state_t run_state(state_t cur_state);
static state_t do_state_idle(void);
static state_t read_sensor_temp(void);
static state_t read_sensor_uv(void);
static state_t read_sensor_light(void);
static state_t read_sensor_low_light(void);
static state_t read_sensor_v_low_light(void);
static state_t read_sensor_wind(void);

/* State Table */
state_func_t* const state_table[NUM_STATES] = {
    do_state_idle, read_sensor_temp, read_sensor_uv, read_sensor_light,
    read_sensor_low_light, read_sensor_v_low_light, read_sensor_wind
};

/* State Table Lookup */
state_t run_state(state_t cur_state){
    return state_table[cur_state]();
};

/* Global Variables */
uint32_t idle_time = 1;
bool tx_flag = false;


/* Setup Function */
void setup() {
  
    /* Terminal Serial Port*/
    Serial.begin(115200);

    /* Setup LED Pin */
    pinMode(LED_PIN, OUTPUT);

    /* Setup SD Card */
    logging_setup(10);

    /* Enable Pullup on Hall Effect */
    pinMode(5, INPUT_PULLUP);
   
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

    /* Dim Activity LED */
    digitalWrite(LED_PIN, HIGH);

    /* Measure VCC */
    log_Vcc();
  
    /* Sleep - Time in Seconds */
    go_to_sleep(idle_time);

    /* Light Activity LED */
    digitalWrite(LED_PIN, LOW);
    
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
    
    return STATE_LIGHT;
}


/* Read Light Sensor State */
static state_t read_sensor_light(void){

    /* Take Measurement */
    log_analog_reading(ID_LIGHT, LIGHT_PIN);
    
    return STATE_LOW_LIGHT;
}


/* Read Low Light Sensor State */
static state_t read_sensor_low_light(void){

    /* Take Measurement */
    log_analog_reading(ID_LOW_LIGHT, LOW_LIGHT_PIN);
    
    return STATE_V_LOW_LIGHT;
}


/* Read Very Low Light Sensor State */
static state_t read_sensor_v_low_light(void){

    /* Take Measurement */
    log_analog_reading(ID_V_LOW_LIGHT, V_LOW_LIGHT_PIN);
    
    return STATE_WIND;
}


/* Read Wind Sensor State */
static state_t read_sensor_wind(void){
  
    /* Take Measurement */
    log_wind_reading();
    
    return STATE_IDLE;
}


/* Go to Sleep */
void go_to_sleep(uint32_t sleep_time){

    uint32_t num_secs = 0;

    while(num_secs<sleep_time){

        /* Check Serial Port for Commands */
        check_commands();

        /* Power Down */
        LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
        num_secs += 1;
    }
}
