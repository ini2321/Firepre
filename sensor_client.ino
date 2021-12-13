#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <MHZ19.h>
#include <time.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>
Adafruit_ADS1115 ads1015;

//wifi, mqtt server 설정
const char* ssid = "firepre";
const char* password = "00000000";
const char* mqtt_server = "192.168.0.36";

//DS18B20 방수 온도 센서
const int oneWireBus = 14;
OneWire oneWire(oneWireBus);
DallasTemperature DS18(&oneWire);

//MQ2 가스 센서
#define MQ2PIN A0

//DHT22 온습도 센서
#define DHTPIN 12
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

//MH-Z19B CO2 센서
const int rx_pin = 13; //Serial rx pin no
const int tx_pin = 15; //Serial tx pin no
MHZ19 *mhz19_uart = new MHZ19(rx_pin, tx_pin);

int analog_Current = 0;
float current = 0;

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define DATA_BUFFER_SIZE  (50)
char data[DATA_BUFFER_SIZE];
int value = 0;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);
  } else {
    digitalWrite(BUILTIN_LED, HIGH);
  }

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

//////센서값 반환 함수들///////
float ds18b20() {
  DS18.requestTemperatures();
  float temperatureC = DS18.getTempCByIndex(0);
  float temperatureF = DS18.getTempFByIndex(0);

  return temperatureC;
}

float dht22(String a) {
  // Reading temperature or humidity
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  if (a == "Hum") {
    return h;
  }
  else if (a == "Temp") {
    return t;
  }
  else {
    return 0;
  }
}

float mhz19(String b)
{
  measurement_t m = mhz19_uart->getMeasurement();

  float c = m.co2_ppm;
  float t = m.temperature;

  if (b == "Co2") {
    return c;
  }
  else if (b == "Temp") {
    return t;
  }
  else {
    return 0;
  }
}

float gas() {
  float g = analogRead(MQ2PIN);
  return g;
}

float Current() {
  int16_t adc0, adc1;
  
  adc0 = ads1015.readADC_SingleEnded(0);
  adc1 = ads1015.readADC_SingleEnded(1);
  
  float res = map(adc0, 0, 26255, 1, 10);
  analog_Current = adc1;
  // 측정된 analog 값을 계산식을 이용해 디지털 전류 값으로 변경
  current = (0.0264 * adc1 /16 -19.64)*res;
  return current;
}
//////함수 끝////////////

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(MQ2PIN, INPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  DS18.begin();
  dht.begin();
  mhz19_uart->begin(rx_pin, tx_pin);
  mhz19_uart->setAutoCalibration(false);
  ads1015.begin();
  delay(3000);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;

  //센서 데이터 전송
  snprintf (data, DATA_BUFFER_SIZE, "%g, %g, %g, %g, %g, %g, %g", 
             ds18b20(), dht22("Temp"), dht22("Hum"), mhz19("Co2"), mhz19("Temp"), gas(), Current());
  Serial.print("Publish Data: ");
  Serial.println(data);
  client.publish("outTopic", data);
  }
}
