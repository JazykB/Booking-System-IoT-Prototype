#include <SPI.h>
#include <MFRC522.h>
#include <DHT.h>
#include <Servo.h> // Include the Servo library

#define SS_PIN 10
#define RST_PIN 9
#define LED_PIN 4 // Relay channel 2 connected to LED
#define LOCK_PIN 8 // Relay channel 1 connected to Lock
#define DHTPIN 2 // DHT11 data pin connected to Arduino Digital Pin 2
#define DHTTYPE DHT11 // DHT 11
#define IR_BLASTER_PIN A0 // IR Blaster analog input pin
#define NOISE_SENSOR_PIN A1 // Noise sensor analog input pin
#define RED_LED_PIN 5 // Red LED pin
#define BLUE_LED_PIN 6 // Blue LED pin
#define SERVO_PIN 7 // Servo motor control pin
#define BUZZER_PIN 3 // Buzzer control pin
#define BUZZER_SHORT_DELAY 200 // Buzzer short beep duration
#define BUZZER_LONG_DELAY 500 // Buzzer long beep duration
#define BUZZER_REPEAT_DELAY 300 // Delay between buzzer beeps
#define BUZZER_MATCH_REPETITIONS 1 // Number of buzzer beeps on successful RFID match
#define BUZZER_MISMATCH_REPETITIONS 2 // Number of buzzer beeps on unsuccessful RFID match
#define BUZZER_EXCEED_PEOPLE_REPETITIONS 5 // Number of buzzer beeps when people count exceeds limit
#define BUZZER_NOISE_THRESHOLD 300 // Noise sensor threshold for buzzer activation
#define BUZZER_NOISE_REPETITIONS 3 // Number of buzzer beeps on noise detection
#define MAX_PEOPLE_COUNT 6 // Maximum number of people allowed in the meeting room

DHT dht(DHTPIN, DHTTYPE);
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create instance
Servo servoMotor; // Create servo motor object

bool isRFIDDetected = false;
bool isIRBlasterActive = false;
bool isNoiseDetected = false;
bool isSystemOn = false;
bool cardPreviouslyPresent = false;



int peopleCount = 0;
int buzzerRepetitions = 0;
bool isDoorOpen = false;
unsigned long doorOpenTime = 0;
String lastCardID = "";
// RFID Reader
String incomingRFID = "";


void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init(); // Initialize MFRC522
  pinMode(LED_PIN, OUTPUT);
  pinMode(LOCK_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);  // Initialize Buzzer
  digitalWrite(LED_PIN, HIGH); // Normally close condition for Relay module
  digitalWrite(LOCK_PIN, HIGH); // Normally close condition for Relay module
  digitalWrite(BUZZER_PIN, LOW); // Normally silent condition for Buzzer
  dht.begin();
  servoMotor.attach(SERVO_PIN); // Attach servo motor to the designated pin
}

bool firstRFIDDetected = false; // added this new variable

void loop() {
  // RFID Reader
  if (Serial.available()) {
    incomingRFID = Serial.readStringUntil('\n'); // Read the incoming RFID number up to the newline
  }

  // Compare the detected RFID with the incomingRFID
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String detectedRFID = printCardID();
    if(detectedRFID.equalsIgnoreCase(incomingRFID)) { // changed this line
      // The detected RFID matches the incoming RFID
      handleCardPresent();
    } else {
      // The detected RFID does not match the incoming RFID
      handleCardNotPresent();
    }
  } else {
    handleCardNotPresent();
  }

  

  

  // Print sensor readings when the system is on
  if (isSystemOn) {
    // DHT11 Sensor
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    // IR Blaster
    int irValue = analogRead(IR_BLASTER_PIN);
    Serial.print("IR Blaster Value: ");
    Serial.println(irValue);

    if (irValue > 0) {
      isIRBlasterActive = true;
      adjustAC(irValue);
    } else {
      isIRBlasterActive = false;
    }

    // Noise Sensor
    int noiseValue = analogRead(NOISE_SENSOR_PIN);
    Serial.print("Noise Sensor Value: ");
    Serial.println(noiseValue);

    if (noiseValue > BUZZER_NOISE_THRESHOLD) {
      if (!isNoiseDetected) {
        isNoiseDetected = true;
        // Buzzer - Noise Detection
        activateBuzzer(BUZZER_NOISE_REPETITIONS);
      }
    } else {
      isNoiseDetected = false;
    }

    // People Counting
    int currentPeopleCount = countPeople();
    Serial.print("People Count: ");
    Serial.println(currentPeopleCount);

    if (currentPeopleCount > MAX_PEOPLE_COUNT) {
      // Buzzer - Exceed People Limit
      activateBuzzer(BUZZER_EXCEED_PEOPLE_REPETITIONS);
    }

    // Door Status
  bool isDoorOpened = (digitalRead(LOCK_PIN) == LOW);
  if (isDoorOpened) {
    Serial.println("Door is: opened");
  } else {
    Serial.println("Door is: closed");
  }
  }
}

void handleCardPresent() {
  if (!isRFIDDetected) {
    isRFIDDetected = true;
    // Turn the system on the first time an RFID card is detected
    isSystemOn = true;
    cardPreviouslyPresent = true;
    digitalWrite(RED_LED_PIN, HIGH); // LED ON
    Serial.print("RFID card detected:");
    lastCardID = printCardID();


    if (!isDoorOpen){
      // Open the door when the card is detected
      digitalWrite(LOCK_PIN, LOW); // Lock OPEN
      isDoorOpen = true;
      doorOpenTime = millis();
    }
    else {
      if (millis() - doorOpenTime >= 10000) {
        // Close the door after 10 seconds when the card is detected again
        digitalWrite(LOCK_PIN, HIGH); // Lock CLOSE
        isDoorOpen = false;
        doorOpenTime = 0;
      }
    }
  }
}

void handleCardNotPresent() {
  
  if (isRFIDDetected) {
    // Close the door when the card is not present
    digitalWrite(RED_LED_PIN, LOW); // LED OFF
    digitalWrite(LOCK_PIN, HIGH); // Lock CLOSE
    isDoorOpen = false;
    isRFIDDetected = false;
    

  }
  Serial.println("RFID card detected: " +lastCardID);
  
}


String printCardID() {
  // Print the RFID card ID
  String cardID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    // Convert each byte of the UID to hexadecimal
    // and add leading zeroes when necessary
    if (mfrc522.uid.uidByte[i] < 0x10) {
      cardID += '0';
    }
    cardID += String(mfrc522.uid.uidByte[i], HEX);
  }
  cardID.toUpperCase(); // Convert the card ID to upper case to ensure consistency
  Serial.println(cardID);
  return cardID;
}

void activateBuzzer(int repetitions) {
  if (buzzerRepetitions == 0) {
    buzzerRepetitions = repetitions; // Set the buzzer repetition count

    for (int i = 0; i < repetitions; i++) {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(BUZZER_SHORT_DELAY);
      digitalWrite(BUZZER_PIN, LOW);
      delay(BUZZER_REPEAT_DELAY);
    }

    buzzerRepetitions = 0; // Reset the buzzer repetition count
  }
}

int countPeople() {
  int sensorValue = analogRead(IR_BLASTER_PIN);
  if (sensorValue > 400) {
    // Sensor triggered, increment people count
    peopleCount++;
    delay(1000); // Delay to avoid multiple counts from a single trigger
  }
  return peopleCount;
}

void adjustAC(int irValue) {
  // Desired temperature and airflow levels based on current levels
  float desiredTemperature = 0.0;
  float desiredAirflow = 0.0;

  if (isSystemOn) { // Check if system is ON
    // Determine desired temperature and airflow level based on current levels
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    Serial.print("Temperature: ");
    Serial.println(t);

    Serial.print("Humidity: ");
    Serial.println(h);
    
    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    
    if (t >= 25.0 && h <= 70.0) {
      desiredTemperature = 21.0;
      desiredAirflow = 30.0;
      Serial.println("desiredTemperature: 21.0");
      Serial.println("desiredAirflow: 30.0");
    } else if (t >= 25.0 && h > 70.0) {
      desiredTemperature = 20.0;
      desiredAirflow = 40.0;
      Serial.println("desiredTemperature: 20.0");
      Serial.println("desiredAirflow: 40.0");
    } else if (t < 25.0 && h <= 70.0) {
      desiredTemperature = 21.5;
      desiredAirflow = 20.0;
      Serial.println("desiredTemperature: 21.5");
      Serial.println("desiredAirflow: 20.0");
    } else if (t < 25.0 && h > 70.0) {
      desiredTemperature = 21.0;
      desiredAirflow = 30.0;
      Serial.println("desiredTemperature: 21.0");
      Serial.println("desiredAirflow: 30.0");
    } else {
      desiredTemperature = 23.0;
      desiredAirflow = 20.0;
      Serial.println("desiredTemperature: 23.0");
      Serial.println("desiredAirflow: 20.0");
    }
  }

  // Adjust LED lights intensity based on desired temperature
  if (desiredTemperature >= 15.0 && desiredTemperature < 20.0) {
    analogWrite(BLUE_LED_PIN, 255);
  } else if (desiredTemperature >= 20.0 && desiredTemperature < 25.0) {
    analogWrite(BLUE_LED_PIN, 160);
  } else if (desiredTemperature >= 25.0 && desiredTemperature < 30.0) {
    analogWrite(BLUE_LED_PIN, 100);
  } else if (desiredTemperature >= 30.0 && desiredTemperature <= 35.0) {
    analogWrite(BLUE_LED_PIN, 1);
  } else {
    analogWrite(BLUE_LED_PIN, 0);
  }

  // Adjust servo motor level
  if (desiredAirflow >= 10 && desiredAirflow < 20) {
    servoMotor.write(45);
  } else if (desiredAirflow >= 20 && desiredAirflow < 30) {
    servoMotor.write(90);
  } else if (desiredAirflow >= 30 && desiredAirflow < 40) {
    servoMotor.write(135);
  } else if (desiredAirflow >= 40 && desiredAirflow <= 50) {
    servoMotor.write(180);
  } else {
    servoMotor.write(0);
  }
  delay(1000);
}