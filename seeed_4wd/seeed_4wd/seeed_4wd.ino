/*
 * Program as Tools->Board->Arduino Duemilanove w/ ATmega328.
 * 
 */

#include "motordriver_4wd.h"
#include "seeed_pwm.h"


const int DIO_ENCODER_LEFT_A = 2;
const int DIO_ENCODER_LEFT_B = A2;

const int DIO_ENCODER_RIGHT_A = 3;
const int DIO_ENCODER_RIGHT_B = A3;

volatile int left_ticks = 0;
volatile int right_ticks = 0;

void init_encoders() {
  pinMode(DIO_ENCODER_LEFT_A, INPUT_PULLUP);
  pinMode(DIO_ENCODER_LEFT_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(DIO_ENCODER_LEFT_A), on_left_tick, CHANGE);

  pinMode(DIO_ENCODER_RIGHT_A, INPUT_PULLUP);
  pinMode(DIO_ENCODER_RIGHT_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(DIO_ENCODER_RIGHT_A), on_right_tick, CHANGE);
}

void on_left_tick() {
  left_ticks += encoder_change(DIO_ENCODER_LEFT_A, DIO_ENCODER_LEFT_B);
}

void on_right_tick() {
  right_ticks += encoder_change(DIO_ENCODER_RIGHT_A, DIO_ENCODER_RIGHT_B);
}

int encoder_change(int pina, int pinb) {
  if (digitalRead(pina) == digitalRead(pinb)) {
    return 1;
  } else {
    return -1;
  }
}


int left_percent = 0;
int right_percent = 0;
int loops_since_command = 0;

const int WATCHDOG_CYCLES = 25;

const int COMMAND_BUFFER_LEN = 32;
int command_buffer_index = -1;
char command_buffer[COMMAND_BUFFER_LEN];

bool parse_command() {
  char* cur = command_buffer;
  if (*cur != 'M') {
    return false;
  }
  cur++;

  int left_dir = 1;
  if (*cur == '-') {
    left_dir = -1;
    cur++;
  }
  int left_abs = 0;
  for (int i = 0; i < 3; i++) {
    if (*cur < '0' || *cur > '9') {
      return false;
    }
    int new_digit = (int)(*cur) - (int)('0');
    left_abs = 10*left_abs + new_digit;
    cur++;
  }
  if (*cur != ' ') {
    return false;
  }
  cur++;
  
  int right_dir = 1;
  if (*cur == '-') {
    right_dir = -1;
    cur++;
  }
  int right_abs = 0;
  for (int i = 0; i < 3; i++) {
    if (*cur < '0' || *cur > '9') {
      return false;
    }
    int new_digit = (int)(*cur) - (int)('0');
    right_abs = 10*right_abs + new_digit;
    cur++;
  }

  if (*cur != '\0') {
    return false;
  }
  
  left_percent = left_dir * left_abs;
  right_percent = right_dir * right_abs;
  
  return true;
}

void consume_commands() {
  loops_since_command += 1;
  if (loops_since_command > WATCHDOG_CYCLES) {
    left_percent = 0;
    right_percent = 0;
  }
  
  int available_bytes = Serial.available();
  for (int i = 0; i < available_bytes; i++) {
    char new_byte = Serial.read();
    // Do I have no active command?
    if (command_buffer_index < 0) {
      // look for the start of a new command
      if (new_byte == 'C') {
        // Start the command
        command_buffer_index = 0;
        memset(command_buffer, 0, COMMAND_BUFFER_LEN);
      }
      continue;
    }
    // Is it the end of the command?
    if (new_byte == '\n' || new_byte == '\r') {
      /*
      Serial.print("received command:");
      Serial.print(command_buffer_index);
      Serial.write(command_buffer, command_buffer_index);
      Serial.print('\n');
      */
      if (!parse_command()) {
        Serial.print("Invalid command\n");
      } else {
        /*
        Serial.print("Message accepted\n");
        Serial.print(left_percent);
        Serial.print(' ');
        Serial.print(right_percent);
        Serial.print('\n');
        */
        loops_since_command = 0;
      }
      command_buffer_index = -1;
      
      continue;
    }

    // Is the buffer overflowing?
    if (command_buffer_index >= COMMAND_BUFFER_LEN) {
      // Drop the message
      Serial.print("dropped incomplete message\n");
      command_buffer_index = -1;
      continue;
    }

    // Add the byte to the command
    command_buffer[command_buffer_index] = new_byte;
    command_buffer_index++;
  }
  
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  MOTOR.init();

  init_encoders();
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("E");
  Serial.print(left_ticks);
  Serial.print(' ');
  Serial.println(right_ticks);

  consume_commands(); 

  unsigned char ldir = left_percent < 0 ? DIRF : DIRR;
  unsigned char rdir = right_percent < 0 ? DIRF : DIRR;
  
  MOTOR.setSpeedDir1(abs(left_percent), ldir);
  MOTOR.setSpeedDir2(abs(right_percent), rdir);
  
  delay(20);
}
