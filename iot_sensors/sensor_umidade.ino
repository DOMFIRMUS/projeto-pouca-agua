#include <WiFi.h>
#include <HTTPClient.h>

// Configurações da rede Wi-Fi
const char* ssid = "MEU_SSID";
const char* password = "MINHA_SENHA";

// IP e porta do servidor Flask
const char* serverIP = "192.168.1.100";
const int serverPort = 5000;

// Pino analógico conectado ao sensor de umidade capacitivo
const int sensorPin = 34;

// Valores de calibração para o mapeamento (ajustar conforme o sensor)
// Exemplo:
// Ar (0% de umidade) pode ler próximo a 4095
// Água (100% de umidade) pode ler próximo a 1000
const int dryValue = 4095;
const int wetValue = 1000;

void setup() {
  // Inicia a comunicação serial
  Serial.begin(115200);

  // Conecta ao Wi-Fi
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado.");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // 4) Ler o sensor analógico de umidade capacitivo
    int rawValue = analogRead(sensorPin);

    // Mapear o valor bruto para uma porcentagem de 0% a 100%
    int umidade = map(rawValue, dryValue, wetValue, 0, 100);

    // Garantir que a porcentagem fique entre 0 e 100
    umidade = constrain(umidade, 0, 100);

    // Temperatura simulada
    float temperatura = 25.5;

    // 5) Montar o payload em JSON
    String jsonPayload = "{";
    jsonPayload += "\"umidade\": " + String(umidade) + ",";
    jsonPayload += "\"temperatura\": " + String(temperatura);
    jsonPayload += "}";

    // Montar a URL do servidor
    String serverUrl = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/sensor";

    // Fazer a requisição HTTP POST
    HTTPClient http;
    http.begin(serverUrl);

    // Adicionar cabeçalho para indicar conteúdo JSON
    http.addHeader("Content-Type", "application/json");

    // Enviar POST
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.print("Código de resposta HTTP: ");
      Serial.println(httpResponseCode);
      String resposta = http.getString();
      Serial.println(resposta);
    } else {
      Serial.print("Erro na requisição. Código: ");
      Serial.println(httpResponseCode);
    }

    // Liberar recursos
    http.end();
  } else {
    Serial.println("Wi-Fi desconectado. Tentando reconectar...");
    WiFi.begin(ssid, password);
  }

  // 6) Aguardar 10 minutos (600.000 milissegundos) antes da próxima leitura
  delay(600000);
}
