#include <Arduino.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/queue.h>

// Pins FIX ME match actual pins
const int BUTTONS[] = {4, 5, 6, 7};
const int numberOfButtons = 4;
const int LED = 15;
const int BUZZER = 17;

// data to travel through queue: which event, and when it happened
typedef struct {
  uint8_t eventType;
  uint32_t timestamp;
} ButtonEvent;

QueueHandle_t eventQueue;


// check if all 4 pressed
volatile bool allFourHeld = false;

// task 1: watches buttons only
void buttonTask(void *param) {
  int lastState[] = {HIGH, HIGH, HIGH, HIGH};

  while (true) {
    int states[numberOfButtons];
    int pressedCount = 0;

    for (int i = 0; i < numberOfButtons; i++) {
      states[i] = digitalRead(BUTTONS[i]);
      if (states[i] == LOW) pressedCount++;
    }

    // update the shared flag every poll
    allFourHeld = (pressedCount == 4);

    if (!allFourHeld) {
      // only check individual buttons when not all 4 are down
      for (int i = 0; i < numberOfButtons; i++) {
        if (states[i] == LOW && lastState[i] == HIGH) {
          ButtonEvent evt = {(uint8_t)i, millis()};
          xQueueSend(eventQueue, &evt, 0);
        }
        lastState[i] = states[i];
      }
    }

    vTaskDelay(pdMS_TO_TICKS(20));
  }
}

// task 2: waits for events, drives LED/buzzer/serial
void alertTask(void *parameter) {
  ButtonEvent received;
  const char* MESSAGE[] = {"TEMP_HIGH", "HUMIDITY_HIGH", "AIR_QUALITY_ALERT", "SYSTEM_FAULT"};

  while (true) {
    // check the shared flag first, this is the continuous-alarm path
    if (allFourHeld) {
      digitalWrite(BUZZER, HIGH);
      digitalWrite(LED, HIGH);
      Serial.println("SYSTEM_FAILURE_CHECK_ALL");
      vTaskDelay(pdMS_TO_TICKS(200));
      digitalWrite(BUZZER, LOW);
      digitalWrite(LED, LOW);
      vTaskDelay(pdMS_TO_TICKS(200)); // brief pause between flashes
    }
    // otherwise, handle single-button events same as before, non-blocking check
    else if (xQueueReceive(eventQueue, &received, pdMS_TO_TICKS(50))) {
      digitalWrite(LED, HIGH);
      Serial.println(MESSAGE[received.eventType]);
      vTaskDelay(pdMS_TO_TICKS(200));
      digitalWrite(LED, LOW);
    }
  }
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < numberOfButtons; i++) pinMode(BUTTONS[i], INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  eventQueue = xQueueCreate(10, sizeof(ButtonEvent));

  xTaskCreate(buttonTask, "ButtonTask", 2048, NULL, 2, NULL);
  xTaskCreate(alertTask, "AlertTask", 2048, NULL, 1, NULL);
}

void loop() {
  // empty, FreeRTOS scheduler runs the tasks, not this loop
}