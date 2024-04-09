// GSM pin connecton
// Arduino - Gsm
// Tx - 9
// Rx - 10

// GPS pin Connection
// Arduino - GPS
// RX - 3;
// TX - 2;


#include <TinyGPS++.h>
#include<SoftwareSerial.h>

SoftwareSerial mySerial(9,10);


SoftwareSerial gpsSerial(2, 3);
TinyGPSPlus gps;


//Gas
#define SmokeThreshold 800
#define MQ2pin 0 //A0 - Analog pin
float SmokeValue;  //variable to store sensor value

//vibration
int vib_pin=7;


void setup() {
  //Gas
	Serial.begin(9600); 
	Serial.println("MQ2 warming up!");
	delay(1000); 

  //GSM
  mySerial.begin(9600);

  //vibration
  pinMode(vib_pin,INPUT);

  //GPS
  gpsSerial.begin(9600);

}

void loop() {

  //Gas
  SmokeValue = analogRead(MQ2pin); //A0
  
  Serial.print("Sensor Value: ");
  Serial.print(SmokeValue);

  if(SmokeValue > SmokeThreshold)
    {
        Serial.print(" Smoke/Alcohol detected"); //Smoke or Alcohol, depending on Threshold
        SendMessage(2);

    }
  
  Serial.println("");
  delay(1000); 

  //Vibration

  int val;
  val=digitalRead(vib_pin);

  if(val==1)
  {
      Serial.println(" Vibration detected!"); //Vibration implies collision
      SendMessage(1);

      //Serial.println("Location: lattitude-xxx , Longitude-xxx");
      
      while (gpsSerial.available() > 0)
        if (gps.encode(gpsSerial.read()))
          displayInfo();


        if (millis() > 5000 && gps.charsProcessed() < 10)
        {
          Serial.println("No GPS detected");
        }

  }


}


void SendMessage(int status)
{

  mySerial.println("AT+CMGF=1");
  delay(1000);

  mySerial.println("AT+CMGS=\"+91xxxxxxxxxx\"\r"); // Replace xxxxxxxxxx with receiver mobile number
  delay(1000);

  if(status==1){
  mySerial.println(" Collision detected: lattitude-xxx , longitude-xxx");
  delay(100);
  }

  if(status==2){
  mySerial.println(" Smoke/Alcohol alert ");
  delay(100);
  }

  mySerial.println((char)26);
  delay(1000);

}



void displayInfo()
{
  if (gps.location.isValid())
  {
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
    Serial.print("Altitude: ");
    Serial.println(gps.altitude.meters());
  }
  else
  {
    Serial.println("Location: Not Available");
  }
  
  Serial.print("Date: ");
  if (gps.date.isValid())
  {
    Serial.print(gps.date.month());
    Serial.print("/");
    Serial.print(gps.date.day());
    Serial.print("/");
    Serial.println(gps.date.year());
  }
  else
  {
    Serial.println("Not Available");
  }

  Serial.print("Time: ");
  if (gps.time.isValid())
  {
    if (gps.time.hour() < 10) Serial.print(F("0"));
    Serial.print(gps.time.hour());
    Serial.print(":");
    if (gps.time.minute() < 10) Serial.print(F("0"));
    Serial.print(gps.time.minute());
    Serial.print(":");
    if (gps.time.second() < 10) Serial.print(F("0"));
    Serial.print(gps.time.second());
    Serial.print(".");
    if (gps.time.centisecond() < 10) Serial.print(F("0"));
    Serial.println(gps.time.centisecond());
  }
  else
  {
    Serial.println("Not Available");
  }

  Serial.println();
  Serial.println();
  delay(1000);
}