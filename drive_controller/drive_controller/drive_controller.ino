const int DIO_ENCODER_LEFT_A = 2;
const int DIO_ENCODER_LEFT_B = 8;

const int DIO_ENCODER_RIGHT_A = 3;
const int DIO_ENCODER_RIGHT_B = 4;

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


const int DIO_MOTOR_LEFT_A = 5;
const int DIO_MOTOR_LEFT_B = 9;
const int DIO_MOTOR_RIGHT_A = 10;
const int DIO_MOTOR_RIGHT_B = 11;

// Can go up to 1023
const int MAX_MOTOR_OUTPUT = 200;

void write_motor(int pina, int pinb, int percent) {
  int out_a = 0;
  int out_b = 0;
  if (percent > 0) {
    out_a = MAX_MOTOR_OUTPUT * percent / 100;
  } else {
    out_b = -1 * MAX_MOTOR_OUTPUT * percent / 100;
  }
  analogWrite(pina, out_a);
  analogWrite(pinb, out_b);
}

void write_left_motor(int percent) {
  write_motor(DIO_MOTOR_LEFT_A, DIO_MOTOR_LEFT_B, percent);
}
void write_right_motor(int percent) {
  write_motor(DIO_MOTOR_RIGHT_A, DIO_MOTOR_RIGHT_B, percent);
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  Serial.println("Initializing"); 

  pinMode(DIO_MOTOR_LEFT_A, OUTPUT);
  pinMode(DIO_MOTOR_LEFT_B, OUTPUT);
  pinMode(DIO_MOTOR_RIGHT_A, OUTPUT);
  pinMode(DIO_MOTOR_RIGHT_B, OUTPUT);

  write_left_motor(0);
  write_right_motor(0);
  

  init_encoders();
}

void loop() {  
  Serial.print(left_ticks);
  Serial.print(' ');
  Serial.print(right_ticks);
  Serial.print('\n');

  write_left_motor(0);
  write_right_motor(0);
  
  delay(500);
}
