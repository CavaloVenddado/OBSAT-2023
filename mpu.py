import time
import board
import adafruit_mpu6050

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    print("Temperatura: %.2f" % mpu.temperature, "°C")
    print("Giro X: %.2f, Y: %.2f, Z: %.2f" %mpu.gyro)
    time.sleep(1)