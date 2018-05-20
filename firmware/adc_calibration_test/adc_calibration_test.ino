/* Returns Supply Voltage in mV */
long readVcc() {
  
  const int num_avg = 20;
  long result[num_avg];
  long sum;
  int i=0;
  
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
  return sum/num_avg;
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println( readVcc(), DEC );
  delay(1000);
}
