// C++ code
//

// variables
const int LED = 6;
const int BUZZER = 10;
bool allFourPressed = false;

// arrays 
const int BUTTONS[] = {2, 3, 4, 5};
int numberOfButtons = sizeof(BUTTONS) / sizeof(BUTTONS[0]);
// strings use heap mem may crash 2KB RAM, const char* stores on flash storage
const char* MESSAGE[] = {"TEMP_HIGH", "HUMIDITY_HIGH", "AIR_QUALITY_ALERT", "SYSTEM_FAULT"};
int lastState[] = {HIGH, HIGH, HIGH, HIGH};

// function to sound alarm  and flash led
void beep() {
  digitalWrite(BUZZER, HIGH);
  digitalWrite(LED, HIGH);
  delay(200);
  digitalWrite(LED, LOW);
  delay(200);
}

void setup(){
  // init buttons by default they read high (INPUT_PULLUP)
  for (int i = 0; i < numberOfButtons; i ++) {
  	pinMode(BUTTONS[i], INPUT_PULLUP); 
  }
  
  // init led buzzer and serial output
  pinMode(LED,OUTPUT);
  pinMode(BUZZER,OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  // init button state and number of presses
  int states[numberOfButtons];
  int pressedCount = 0;
  
  // when button state low (pressed) update count and change state on press
  for(int i = 0; i < numberOfButtons; i ++) {
  	states[i] = digitalRead(BUTTONS[i]);
    if (states[i] == LOW) {
    	pressedCount++; 
    }
  }
  
  // when all four buttins pressed flash led and sound alarm
  // write error message
  if(pressedCount == 4) {
    beep();
    if (allFourPressed == false && pressedCount == 4) {
      Serial.println("SYSTEM_FAILURE_CHECK_ALL");
      allFourPressed = true;
    }
 
  }
  // when one one button pressed light comes on and no buzzer
  // write error meesage
  else if (pressedCount > 0) {
    allFourPressed = false;
    digitalWrite(LED, HIGH);
    digitalWrite(BUZZER, LOW);
    
    // handles state so messge only prints once or on changes
    // change state outside curly braces so button push updates on release            
    for(int i = 0; i < numberOfButtons; i++) {
       if (states[i] == LOW && lastState[i] == HIGH) {
         Serial.println(MESSAGE[i]);
       }
       lastState[i] = states[i];
     }
   }
  // all eslse no message led or buzzer
  else {
    allFourPressed = false;
    digitalWrite(LED, LOW);
    digitalWrite(BUZZER, LOW);
  }
}