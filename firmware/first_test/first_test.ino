#define VERTICAL_CH_PIN A0

int vertical_reading = 0;

void setup() {
  Serial.begin(9600);
  pinMode(VERTICAL_CH_PIN, INPUT);
}

void loop() {
  vertical_reading = analogRead(VERTICAL_CH_PIN);
  Serial.println(vertical_reading);
  delay(3);
}
