// Example code copied from https://github.com/espressif/arduino-esp32/blob/master/libraries/BluetoothSerial/examples/SerialToSerialBT/SerialToSerialBT.ino

// This code creates a bridge between Serial and Bluetooth (SPP)

#include "BluetoothSerial.h"
//ALSO INCLUDE HERE WHATEVER SENSORS WE HAVE

// REMOVE THE SUBSEQUENT TWO IFDEF BLOCKS IF THIS IS TROLLING
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED) 
#error BLUETOOTH NOT ENABLED, RUN `make menuconfig` TO ENABLE 
#endif

//#if ~defined(CONFIG_BT_SPP_ENABLED)
//#error SERIAL BLUETOOTH NOT AVAILABLE OR ENABLED 
//#endif 

BluetoothSerial = SerialBT;

void setup() {
    Serial.begin(115200); // Baud Rate
    SerialBT.begin("ESP32"); // DEVICE NAME
    Serial.printf("Device started.\n Please pair with the Bluetooth now");
    SerialBT.println("Starting, from SerialBT");
    delay(500);
}

void loop() {
    String inputFromOtherSide;
    if (SerialBT.available()) {
        inputFromOtherSide = SerialBT.readString();
        SerialBT.write("Hello from the Bluetooth module");
        SerialBT.write(inputFromOtherSide);
    } else {
        SerialBT.write("ERROR, SerialBT UNAVAILABLE")
    }
    //if (Serial.available()) {
    //    SerialBT.write(Serial.read());
    //}
    delay(20);
}