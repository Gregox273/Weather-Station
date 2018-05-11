#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <SPI.h>
#include <SD.h>

File logFile;
TinyGPS gps;
SoftwareSerial ss(4, 3);

/* Setup Function */ 
void setup() {
  
  /* Terminal Serial Port*/
  Serial.begin(115200);
  
  /* GPS Serial Port */
  ss.begin(9600);

  /* SD Card Init */
  if (!SD.begin(10)) {
    Serial.println("SD Card Not Found!");
    return;
  }  
}

void loop() {
  
  bool newGPSData = false;
  
  /* Listen to GPS Serial Port for 1 Second */
  for (unsigned long start = millis(); millis() - start < 1000;) {

    /* Check Buffer */
    while (ss.available()) {
      
      /* Parse NMEA from Buffer */
      char c = ss.read();
      if (gps.encode(c))
        newGPSData = true;
    }
  }

  /* Log Fresh GPS Data */
  if (newGPSData) {
    
    float flat, flon;
    uint8_t num_sat;
    unsigned long age;

    /* Get Data */
    gps.f_get_position(&flat, &flon, &age);
    num_sat = gps.satellites();

    /* Upload to PC */
    Serial.print("LAT=");
    Serial.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
    Serial.print(" LON=");
    Serial.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
    Serial.print(" SAT=");
    Serial.println(num_sat == TinyGPS::GPS_INVALID_SATELLITES ? 0 : num_sat);

    /* Write Data to Log File */
    logFile = SD.open("log.txt", FILE_WRITE);
    if (logFile) {
      logFile.print("LAT=");
      logFile.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
      logFile.print(" LON=");
      logFile.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
      logFile.print(" SAT=");
      logFile.println(num_sat == TinyGPS::GPS_INVALID_SATELLITES ? 0 : num_sat);
      logFile.close();
    } else {
      Serial.println("Error Writing to File!");
    }
  }
}
