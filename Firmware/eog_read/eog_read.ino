/*
 * This code is for reading analog signals coming from EOG recording 
board.
 * Currently, it detects (by thresholding) player's eye movements and 
sends 
 * a corresponding keystroke via USB
 */

#include "PluggableUSBHID.h"
#include "USBKeyboard.h"

#define VERTICAL_CH_PIN A0
#define HORIZONTAL_CH_PIN A1

/*
 * CONFIG VARIABLES, FEEL FREE TO CHANGE
 */
int sampling_period = 5; // how many times do we sample per second

int window_width_ms = 1000; // in milliseconds, for moving average
int window_width_samples_num = window_width_ms / sampling_period;
int window_array[200]; // defining window for moving average

int baseline_duration_ms = 5000; // in milliseconds, recording the 
baseline average voltage when steady
int baseline_duration_samples_num = baseline_duration_ms / 
sampling_period;
int baseline_array[1000]; // defining array for storing baseline readings

unsigned long current_time;
int vertical_reading = 0;
int horizontal_reading = 0;

unsigned long start_time;
int i = 0;
int running_sum = 0;
int baseline = 0;

bool calibrating = true;//  

USBKeyboard Keyboard;

void setup() {
  Serial.begin(115200);
  pinMode(VERTICAL_CH_PIN, INPUT);
  pinMode(HORIZONTAL_CH_PIN, INPUT);

  delay(3000);  
  start_time = millis();
}

void loop() {  
  if (calibrating) {
    if (millis() < start_time + baseline_duration_ms) {
      vertical_reading = analogRead(VERTICAL_CH_PIN);
      baseline_array[i] = vertical_reading;
      running_sum += vertical_reading;
      i += 1;
    }
    else {
      calibrating = false;
      baseline = running_sum / baseline_duration_samples_num; // computing 
the baseline
      Serial.println("baseline:");
      Serial.println(baseline);
    }
  } 
  else {
    vertical_reading = analogRead(VERTICAL_CH_PIN);
    Serial.println(vertical_reading);
    if (vertical_reading > 1000) {
      Serial.println("up");  
      Keyboard.printf(" ");
      delay(50);
    }
  }
  delay(3);
}
