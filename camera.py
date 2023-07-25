import cv2
import time

def capture_image():
    # Inicializar o objeto de captura de vídeo
    cap = cv2.VideoCapture(0)

    # Verificar se a câmera está aberta corretamente
    if not cap.isOpened():
        print("Erro ao abrir a câmera")
        return

    # Ler a primeira imagem para descartar (algumas câmeras podem fornecer a primeira imagem em branco)
    ret, frame = cap.read()

    # Exibir a imagem em um visualizador
    cv2.imshow("Visualizador da Câmera", frame)
    cv2.waitKey(5000)  # Aguardar 5 segundos (5000 ms)

    # Capturar uma imagem após 5 segundos
    ret, frame = cap.read()

    # Verificar se a captura foi bem-sucedida
    if ret:
        # Salvar a imagem no desktop
        cv2.imwrite("/home/cavalovendado/Imagens/testes/foto.jpg", frame)
        print("Foto salva com sucesso!")
    else:
        print("Erro ao capturar a imagem")

    # Liberar o objeto de captura e fechar o visualizador
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_image()
