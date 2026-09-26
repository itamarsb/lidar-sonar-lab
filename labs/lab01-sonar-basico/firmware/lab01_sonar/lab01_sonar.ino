/*
 * Lab 01 - Sonar HC-SR04 com compensação de temperatura (Arduino Mega 2560)
 * Projeto: lidar-sonar-lab  |  Autor: Itamar de Sá Britto Júnior
 *
 * Ligações no Mega 2560:
 *   HC-SR04  VCC  -> 5V
 *   HC-SR04  GND  -> GND
 *   HC-SR04  TRIG -> D22
 *   HC-SR04  ECHO -> D49   (pino ICP4 do Timer4, reservado para input capture no Lab 02)
 *   LM35     +Vs  -> 5V
 *   LM35     Vout -> A0
 *   LM35     GND  -> GND
 *
 * Saída serial (USB, 115200 baud), uma linha CSV por medição:
 *   ms,echo_us,temp_c,c_ms,dist_fixa_cm,dist_comp_cm
 *
 *   dist_fixa_cm -> assume 343 m/s (o que a maioria dos tutoriais faz)
 *   dist_comp_cm -> usa c = 331,3 + 0,606*T (compensado pela temperatura)
 */

#if !defined(__AVR_ATmega2560__)
  #error "Este firmware foi feito para o Arduino Mega 2560. Selecione a placa 'Arduino Mega or Mega 2560'."
#endif

const uint8_t PIN_TRIG = 22;
const uint8_t PIN_ECHO = 49;   // ICP4: mesmo pino servirá para input capture por hardware
const uint8_t PIN_LM35 = A0;

const uint8_t  AMOSTRAS         = 5;      // mediana de N ecos por medição
const uint16_t INTERVALO_ECO_MS = 60;     // datasheet: >= 60 ms entre disparos
const uint32_t TIMEOUT_ECO_US   = 30000;  // ~5 m ida e volta; acima disso = sem eco
const uint32_t PERIODO_MS       = 500;    // uma linha CSV a cada 0,5 s

// Referência interna de 1,1 V do Mega: ~0,1 °C de resolução com o LM35 (10 mV/°C),
// contra ~0,5 °C usando a referência padrão de 5 V.
float lerTemperaturaC() {
  analogRead(PIN_LM35);                 // descarta a 1ª leitura após trocar a referência
  uint32_t soma = 0;
  for (uint8_t i = 0; i < 16; i++) soma += analogRead(PIN_LM35);
  float adc = soma / 16.0;
  return adc * 110.0 / 1023.0;          // 1,1 V / 10 mV por °C = 110 °C de fundo de escala
}

uint32_t dispararEco() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);                // pulso de trigger de 10 us (confira no osciloscópio)
  digitalWrite(PIN_TRIG, LOW);
  return pulseIn(PIN_ECHO, HIGH, TIMEOUT_ECO_US);  // 0 = timeout
}

uint32_t medianaEco() {
  uint32_t v[AMOSTRAS];
  for (uint8_t i = 0; i < AMOSTRAS; i++) {
    v[i] = dispararEco();
    delay(INTERVALO_ECO_MS);
  }
  // insertion sort (N pequeno)
  for (uint8_t i = 1; i < AMOSTRAS; i++) {
    uint32_t x = v[i];
    int8_t j = i - 1;
    while (j >= 0 && v[j] > x) { v[j + 1] = v[j]; j--; }
    v[j + 1] = x;
  }
  return v[AMOSTRAS / 2];
}

void setup() {
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  analogReference(INTERNAL1V1);
  Serial.begin(115200);
  delay(200);
  Serial.println(F("# lab01_sonar v1.1 (Mega 2560)"));
  Serial.println(F("ms,echo_us,temp_c,c_ms,dist_fixa_cm,dist_comp_cm"));
}

void loop() {
  static uint32_t ultimo = 0;
  if (millis() - ultimo < PERIODO_MS) return;
  ultimo = millis();

  float    t    = lerTemperaturaC();
  uint32_t echo = medianaEco();
  float    c    = 331.3 + 0.606 * t;               // m/s

  // distância = tempo * velocidade / 2 (ida e volta). us * m/s -> cm: fator 1e-4
  float dFixa = (echo > 0) ? echo * 343.0 * 1e-4 / 2.0 : NAN;
  float dComp = (echo > 0) ? echo * c     * 1e-4 / 2.0 : NAN;

  Serial.print(ultimo);    Serial.print(',');
  Serial.print(echo);      Serial.print(',');
  Serial.print(t, 2);      Serial.print(',');
  Serial.print(c, 2);      Serial.print(',');
  Serial.print(dFixa, 2);  Serial.print(',');
  Serial.println(dComp, 2);
}
