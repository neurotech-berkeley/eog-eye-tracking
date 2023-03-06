#define VERTICAL_CH_PIN A0
#define HORIZONTAL_CH_PIN  A1
int vertical_reading = 0;
int horizontal_reading = 0;
//int time = 0;
void setup() {
  Serial.begin(9600);
}
void loop() {
  vertical_reading = analogRead(VERTICAL_CH_PIN);
  horizontal_reading = analogRead(HORIZONTAL_CH_PIN);
  
  Serial.print(vertical_reading);
  Serial.println(" ");
  Serial.print(-200);
  Serial.print(" ");
  Serial.print("1200");
  Serial.print(" ");
  delay(3);
}