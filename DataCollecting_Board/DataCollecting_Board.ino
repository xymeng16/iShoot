/*
   iShoot code: Data collecting program for Curie.
   Interaction with mobile phone via BLE
   Receive value, function
   -1, initial value
   0, start capturing data
   1, stop capturing data and upload it to the phone
   The SRAM of the 101 is 24K, so we can save the data during the runtime in the SRAM.
   Notice that for each second, the loop function will be invoked for more than 96700 times.
*/
// 2048 byte in the Radon board.
#include <EEPROM.h>
#include <CurieBLE.h>
#include "CurieIMU.h"
#include <cstring>
extern int DEBUG(char *, ...);
const int N = 475;
//byte data[2048];
struct transData
{
  short sampleNo;
  short segNo;
  short data[6];
} datas[N];
int ax, ay, az;
int gx, gy, gz;

#define WirelessMode
BLEPeripheral blePeripheral;
BLEService iShootService("c73966de-d25f-4150-abe4-cd6daa414532");
BLECharacteristic dataCarrier("d43eef85-1db5-42df-9d98-ee38f4d96e62", BLERead |  BLENotify, sizeof(transData)); // 4Byte - #data, 4Byte - #seg, (12 * N)Byte - data segment
BLECharCharacteristic controller("d0f6928a-d1c2-4898-a6ef-6383f83130eb", BLERead | BLEWrite);

int calibrateOffsets = 1; // int to determine whether calibration takes place or not

int length = 0, sampleCount = 0, sampleNo = 1, segNo = 1;
int gyroRange, acceRange;
// start reading from the first byte (address 0) of the EEPROM
int address = 0;
//byte value;

void sendBackToPhone()
{
  DEBUG("Send the #%d segment of the #%d sample back to phone", segNo, sampleNo);
  for (int i = 0; i < segNo % N; i++)
    dataCarrier.setValue((unsigned char *)&datas[i], sizeof(transData));
}

void BLEInitialize()
{
  // initialize serial and wait for port to open:
  DEBUG("TEST BLEInitializing... %d\n", 1);
  blePeripheral.setLocalName("iShoot");
  blePeripheral.setLocalName(iShootService.uuid());
  blePeripheral.addAttribute(iShootService);
  blePeripheral.addAttribute(controller);
  blePeripheral.addAttribute(dataCarrier);
  controller.setValue(-1);
  blePeripheral.begin();
}
void IMUInitialize(int accRate, int gyroRate)
{
  Serial.println("Radon is initializing its IMU sensor...");
  CurieIMU.begin();
  CurieIMU.autoCalibrateGyroOffset();
  CurieIMU.autoCalibrateAccelerometerOffset(X_AXIS, 0);
  CurieIMU.autoCalibrateAccelerometerOffset(Y_AXIS, 0);
  CurieIMU.autoCalibrateAccelerometerOffset(Z_AXIS, 1);

  CurieIMU.setAccelerometerRate(accRate);
  CurieIMU.setGyroRate(gyroRate);

  gyroRange = CurieIMU.getGyroRange();
  acceRange = CurieIMU.getAccelerometerRange();
}
void setup() {
  // clear the EEPROM
  for (int i = 0 ; i < EEPROM.length() ; i++)
  {
    EEPROM.write(i, 0);
  }
  Serial.begin(9600);
  //    while (!Serial);
  Serial.println("Radon is now online...");
  // Data = new shortWithByte[2048];
  BLEInitialize();
  IMUInitialize(1600, 3200);

}

void loop() {
  bool isFirst = true, isFinished = true, isSent = false;
  int ctrlValue;
  // listen for BLE peripherals to connect:
  BLECentral central = blePeripheral.central();

  if (central)
  {
    Serial.print("Connected from central: ");
    // print the central's MAC address:central.address();
    Serial.println(central.address());
    while (central.connected())
    {
      ctrlValue = (int) controller.value();
      //      Serial.print("Current control value is:");
      //      Serial.println(ctrlValue);
      //      DEBUG("Current finish flag is: %b", isFinished);
      if ((ctrlValue != 0 && ctrlValue != 1))
      {
        //        Serial.println("Continue");
        continue;
      }
      switch (ctrlValue)
      {
        case 0:
          {
            if (isFirst)
            {
              Serial.println("Radon's first time getting a '0', beginning to record sensor data after 1 second!");
              delay(1000); // Considering that the launching of the camera is a little time-consuming.
              isFirst = false;
            }
            CurieIMU.readMotionSensor(ax, ay, az, gx, gy, gz); // Read the sensor and save into those 6 variables.
            //          Serial.print("Sample data:");
            //          Serial.print(ax);
            //          Serial.println();
            short data[6] = {ax, ay, az, gx, gy, gz};
            datas[segNo % N].sampleNo = sampleNo;
            datas[segNo % N].segNo = segNo;
            memcpy(datas[segNo % N].data, data, 6 * sizeof(short));
            segNo++;
            //            DEBUG("Current seg No.: %d", segNo);
            Serial.print("Current seg No.:");
            Serial.println(segNo);
            isSent = false;
            if (segNo % N == 0)
            {
              sendBackToPhone();
              isSent = true;
            }
            // Save into the EEPROM, 12 bytes taken.
            //        for(int i = 0; i <12; i++)
            //        {
            //          EEPROM.write(length++, Data.datas[i]);
            //        }
            break;
          }
        case 1:
          {
            //          if (!isFinished)
            {
              Serial.println("Radon's first time getting a '1', stopping to record sensor data.");
              isFinished = true;
              if (!isSent)
                sendBackToPhone();
              sampleNo++;
              segNo = 1;
              while (ctrlValue != 0)
                ctrlValue = (int) controller.value();
              break;
            }
          }
      }
    }
    // when the central disconnects, print it out:
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());

  }
  /***
    As the EEPROM sizes are powers of two, wrapping (preventing overflow) of an
    EEPROM address is also doable by a bitwise and of the length - 1.

    ++address &= EEPROM.length() - 1;
  ***/

}
