// Simple demo of three threads.
// LED blink thread, count thread, and main thread.
#include "ChRt.h"
#include <WS2812Serial.h>
#include <Trill.h>

//------------------------------------------------------------------------------
// NeoPixels

const int numled = 24;
const int pin = 1;
const int pin8 = 8;

//Memory for neopixel 1:
byte drawingMemory[numled*3];         //  3 bytes per LED
DMAMEM byte displayMemory[numled*12]; // 12 bytes per LED

//Memory for neopixel 2:
byte drawingMemory2[numled*3];         //  3 bytes per LED
DMAMEM byte displayMemory2[numled*12]; // 12 bytes per LED

WS2812Serial leds(numled, displayMemory, drawingMemory, pin, WS2812_GRB);
WS2812Serial leds2(numled, displayMemory2, drawingMemory2, pin8, WS2812_GRB);

#define RED    0xFF0000
#define GREEN  0x00FF00
#define BLUE   0x0000FF
#define YELLOW 0xFFFF00
#define PINK   0xFF1088
#define ORANGE 0xE05800
#define WHITE  0xFFFFFF

//------------------------------------------------------------------------------
// Trills
Trill trillSensor;
boolean touchActive = false;
int prevButtonState[2] = { 0 , 0 };

//------------------------------------------------------------------------------
// count gives a sense of free time?

volatile uint32_t count = 0;
//------------------------------------------------------------------------------
// thread 1 - high priority for blinking LED.
// 64 byte stack beyond task switch and interrupt needs.
static THD_WORKING_AREA(waThread1, 140);


static THD_FUNCTION(Thread1 , arg) {
  (void)arg;

  int microsec = 150 / leds.numPixels();
  while(1) {
  for (int i=0; i < leds.numPixels(); i++) {
    noInterrupts();
    leds.setPixel(i, BLUE);
    leds.show();
    interrupts();
    chThdSleepMilliseconds(microsec);
   }

   for (int i=0; i < leds.numPixels(); i++) {
    leds.setPixel(i, ORANGE);
    leds.show();
    chThdSleepMilliseconds(microsec);
   }

   for (int i=0; i < leds.numPixels(); i++) {
    leds.setPixel(i, GREEN);
    leds.show();
    chThdSleepMilliseconds(microsec);
   }
   
   for (int i=0; i < leds.numPixels(); i++) {
    leds.setPixel(i, WHITE);
    leds.show();
    chThdSleepMilliseconds(microsec);
   }
  }
}

//------------------------------------------------------------------------------
// thread 2 - high priority for blinking LED.
// 64 byte stack beyond task switch and interrupt needs.
static THD_WORKING_AREA(waThread2, 140);


static THD_FUNCTION(Thread2, arg) {
  (void)arg;

  int microsec = 150 / leds2.numPixels();
  while(1) {
  for (int i=0; i < leds2.numPixels(); i++) {
    noInterrupts();
    leds2.setPixel(i, BLUE);
    leds2.show();
    interrupts();
    chThdSleepMilliseconds(microsec);
   }

   for (int i=0; i < leds2.numPixels(); i++) {
    leds2.setPixel(i, ORANGE);
    leds2.show();
    chThdSleepMilliseconds(microsec);
   }

   for (int i=0; i < leds2.numPixels(); i++) {
    leds2.setPixel(i, BLUE);
    leds2.show();
    chThdSleepMilliseconds(microsec);
   }
   
   for (int i=0; i < leds2.numPixels(); i++) {
    leds2.setPixel(i, WHITE);
    leds2.show();
    chThdSleepMilliseconds(microsec);
   }
  }
}


//------------------------------------------------------------------------------
// thread 3 - count when higher priority threads sleep.
// 64 byte stack beyond task switch and interrupt needs.
static THD_WORKING_AREA(waThread3, 64);

static THD_FUNCTION(Thread3, arg) {
  (void)arg;

  while (true) {
    noInterrupts();
    count++;
    interrupts();
  }
}
//------------------------------------------------------------------------------
// Name chSetup is not special - must be same as used in chBegin() call.
void chSetup() {
  // Start blink thread. Priority one more than loop().
  chThdCreateStatic(waThread1, sizeof(waThread1),
                    NORMALPRIO + 1, Thread1, NULL);
  // Start blink thread. Priority one more than loop().
  chThdCreateStatic(waThread2, sizeof(waThread2),
                    NORMALPRIO + 1, Thread2, NULL);
  // Start count thread.  Priority one less than loop().
  chThdCreateStatic(waThread3, sizeof(waThread3),
                    NORMALPRIO - 1, Thread3, NULL);
}
//------------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  // Wait for USB Serial.
  while (!Serial) {}
  leds.begin();
  leds2.begin();

  int ret = trillSensor.setup(Trill::TRILL_RING);
  if(ret != 0) {
    Serial.println("failed to initialise trillSensor");
    Serial.print("Error code: ");
    Serial.println(ret);
  }
  
  chBegin(chSetup);
  // chBegin() resets stacks and should never return.
  while (true) {}

}
//------------------------------------------------------------------------------
// Runs at NORMALPRIO.
void loop() {
  // Sleep for one second.

  
  
  chThdSleepMilliseconds(50);
  
  // Print count for previous second.
  Serial.print(F("Count: "));
  Serial.print(count);
  
  // Zero count.
  count = 0;

  // Print unused stack space in bytes.
  Serial.print(F(", Unused Stack: "));
  Serial.print(chUnusedThreadStack(waThread1, sizeof(waThread1)));
  Serial.print(' ');
  Serial.print(chUnusedThreadStack(waThread3, sizeof(waThread3)));
  Serial.print(' ');
  Serial.print(chUnusedMainStack());
#ifdef __arm__
  // ARM has separate stack for ISR interrupts. 
  Serial.print(' ');
  Serial.print(chUnusedHandlerStack());
#endif  // __arm__
  Serial.println();

  
  trillSensor.read();

  if(trillSensor.getNumTouches() > 0) {
    Serial.print("T");
    Serial.print(" ");
    for(int i = 0; i < trillSensor.getNumTouches(); i++) {
        Serial.print(trillSensor.touchLocation(i));
        Serial.print(" ");
        Serial.print(trillSensor.touchSize(i));
        Serial.print(" ");
    }
    Serial.println("");
    touchActive = true;
  }
  else if(touchActive) {
    // Print a single line when touch goes off
    Serial.print("T");
    Serial.print(" ");
    Serial.println("0 0");
    touchActive = false;
  }

  for(int b = 0; b < trillSensor.getNumButtons(); b++) {
  int buttonState = trillSensor.getButtonValue(b);
  if(buttonState != prevButtonState[b]) {
            Serial.print("B");
            Serial.print(" ");
            Serial.print(b);
            Serial.print(" ");
            Serial.print(buttonState);
            Serial.print(" ");
            Serial.println("");
            prevButtonState[b] = buttonState;
        }
  }
}
