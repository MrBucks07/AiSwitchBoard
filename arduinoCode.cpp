//string coming from python.
String pyInput;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  if(Serial.available() > 0){
      pyInput = Serial.readString();
      //if input is on turn on led
      if(pyInput == "on"){
        digitalWrite(13, HIGH);
      }
      //if input is off turn off led
      else if(pyInput == "off"){
        digitalWrite(13, LOW);
      }
  }
  delay(100);
}