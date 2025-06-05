/*
  Alerta de Mancha de Óleo - ESP32
  Recebe alerta via HTTP e acende LED/buzzer
*/
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "SEU_WIFI";
const char* password = "SENHA_WIFI";
const int ledPin = 2; // GPIO2 (LED onboard)

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi conectado");
}

void loop() {
  // Exemplo: checa alerta a cada 10s
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://SEU_SERVIDOR/alerta");
    int httpCode = http.GET();
    if (httpCode == 200) {
      String payload = http.getString();
      if (payload == "1") {
        digitalWrite(ledPin, HIGH); // Alerta ON
      } else {
        digitalWrite(ledPin, LOW); // Alerta OFF
      }
    }
    http.end();
  }
  delay(10000);
}
