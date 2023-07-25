import Adafruit_DHT
import time
import board
import adafruit_mpu6050

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

def read_sensor_data():
    # Definir o tipo de sensor (DHT11)
    sensor = Adafruit_DHT.DHT11

    # Definir o pino GPIO conectado ao sensor
    pin = 4

    while True:
        # Tentar ler os valores de temperatura e umidade
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Verificar se a leitura foi bem-sucedida
        if humidity is not None and temperature is not None:
            
            print(f"Umidade: {humidity:.1f}%")
        else:
            print("Falha ao ler os dados do sensor")
            
        print("Temperatura: %.2f" % mpu.temperature, "°C")
        print("Giro X: %.2f, Y: %.2f, Z: %.2f" %mpu.gyro)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("________________________________________________________")

        # Aguardar 2 segundos antes de fazer a próxima leitura
        time.sleep(2)

if __name__ == "__main__":
    read_sensor_data()
