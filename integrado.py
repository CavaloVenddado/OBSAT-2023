import Adafruit_DHT
import time
import board
import adafruit_mpu6050
import numpy as np
import cv2
import tflite_runtime.interpreter as tflite
import requests

tempo_de_ligamento = time.time()

# Initialize MPU6050
i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

# Definir o tipo de sensor (DHT11)
sensor = Adafruit_DHT.DHT11

# Definir o pino GPIO conectado ao sensor
pin = 4

# Carregar o modelo TFLite
interpreter = tflite.Interpreter(model_path='model_unquant.tflite')
interpreter.allocate_tensors()

# Obter informações dos tensores de entrada e saída
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']

print(input_shape)

#id da imagem
num = 0

# Inicializar o objeto de captura de vídeo
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a câmera")
    exit()

print("+======================================+")
print("|IA e câmera inicializadas com sucesso!|")
print("+======================================+")


def main():
    while True:
        """
            cálculo da bateria
        """
        tempo_ligado = time.time() - tempo_de_ligamento
        bat = 100 - tempo_ligado * (100/9504)
        print("bateria", bat, "%")

        """
            Sensores
        """
        # Tentar ler os valores de temperatura e umidade
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Verificar se a leitura foi bem-sucedida
        if humidity is not None and temperature is not None:
            print(f"Umidade: {humidity:.1f}%")
        else:
            print("Falha ao ler os dados do sensor")

        print("Temperatura: %.2f" % temperature, "°C")
        print("Giro  X: %.2f, Y: %.2f, Z: %.2f" % (mpu.gyro))
        print("Accel X: %.2f, Y: %.2f, Z: %.2f" % (mpu.acceleration))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("________________________________________________________")

        """
            Imagem
        """

        # Ler a imagem (jogar 10 fora antes (baita gambiarra lol))
        for i in range(0, 10):
            ret, frame = cap.read()
            

        # Exibir a imagem em um visualizador
        # cv2.imshow("Visualizador da Câmera", frame)
        # botar do tamanho certo
        new_frame = cv2.resize(frame, (input_shape[1], input_shape[2]))
        cv2.imshow("Visao IA", new_frame)
        cv2.waitKey(100)
        
        #salva a imagem no catrão SD
        cv2.imwrite(("img_"+ time.strftime("%H_%M_%S", time.localtime()) + ".jpg"), new_frame)
        # tela preta:
        # input_data = np.zeros((1, 224, 224, 3)).astype(np.float32)

        # deixar a imagem do jeito necessário
        # o tf precisa do batch_size tmb (dim0)
        # e trocar de uint8 para float32
        input_data = np.expand_dims(new_frame, axis=0).astype(np.float32)

        # Definir os dados de entrada
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # Executar a inferência
        interpreter.invoke()

        # Obter os resultados da saída
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Imprimir os resultados
        print("preservado: ", output_data[0][0], " desmatado: ", output_data[0][1])

        """
            Transmissão
        """

        data = {
            "equipe": 0,
            "bateria": humidity,
            "temperatura": temperature,
            "giroscopio": mpu.gyro,
            "acelerometro": mpu.acceleration,
            "payload":{
                "desmatado":str(output_data[0][1]),
                "preservado":str(output_data[0][0])
            }
        }
        # Send the data to the server
        response = requests.post('https://obsat.org.br/teste_post/envio.php', json=data)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print("Failed to send data.")

        time.sleep(10)
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
