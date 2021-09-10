int buzzer = 46; // set the buzzer control digital IO pin

void setup() {
  pinMode(buzzer, OUTPUT); // set pin 8 as output
}

void loop() {
  for (int j = 0; j < 100; j++) { //make another sound
    digitalWrite(buzzer, HIGH);
    delay(1);
    digitalWrite(buzzer, LOW);
    delay(1);
  }
  delay(100);
}
