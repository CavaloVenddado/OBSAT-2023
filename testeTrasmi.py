import requests
def transmit():
    data = {
            "equipe": 0,
            "bateria": humidity,
            "temperatura": mpu.temperature,
            "giroscopio": mpu.gyro,
            "acelerometro": mpu.accel,
            payload:{
                "desmatado":output_data[0][1],
                "preservado":output_data[0][0]
            }
        }

        # Send the data to the server
        response = requests.post('http://localhost:5000/data', json=data)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print("Failed to send data.")