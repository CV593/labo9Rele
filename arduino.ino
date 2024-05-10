const int pinRelay = 7;
const int leds[] = {2, 3, 4};
const int tiempos[] = {6000, 3000, 5000};
boolean semaforoActivo = false;

void setup() {
  pinMode(pinRelay, OUTPUT);
  for (int i = 0; i < sizeof(leds) / sizeof(leds[0]); i++) {
    pinMode(leds[i], OUTPUT);
  }
  Serial.begin(9600);
}

void encenderLed(int led, int duracion) {
  digitalWrite(pinRelay, HIGH);
  digitalWrite(led, HIGH);
  delay(duracion);
  digitalWrite(led, LOW);
  digitalWrite(pinRelay, LOW);
}

void apagarLed(int led) {
  digitalWrite(led, LOW);
}

void parpadearAmarillo(int led, int repeticiones, int duracion) {
  for (int i = 0; i < repeticiones; i++) {
    digitalWrite(led, HIGH);
    digitalWrite(pinRelay, HIGH);
    delay(duracion);
    digitalWrite(led, LOW);
    digitalWrite(pinRelay, LOW);
    delay(duracion);
  }
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();
    if (comando == '1') {
      semaforoActivo = true;
      for (int i = 0; i < sizeof(leds) / sizeof(leds[0]); i++) {
        if (i == 1) {
          parpadearAmarillo(leds[i], 4, 200);
        } else {
          encenderLed(leds[i], tiempos[i]);
        }
        apagarLed(leds[i]);
      }
    } else if (comando == '5') {
      semaforoActivo = false;
    }
  }
}
