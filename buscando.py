import cv2#Libreria OpenCV para procesamiento de imagenes(Visión artificial)
import serial,time#Librerias para comunicacion serial Arduino-Python
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient#Libreria de Azure para Custom Vision service
from msrest.authentication import ApiKeyCredentials#Libreria de Azure para autenticar credenciales de servicio

credentials = ApiKeyCredentials(in_headers={"Prediction-key": "Aquí la key del proyecto"})#La clave para hacer uso del servicio de custom vision desplegado
predictor = CustomVisionPredictionClient("Aquí el endpoint", credentials)#Endpoint donde se encuentra nuestro servicio de custom vision desplegado

def ArduinoMessage(data):
    arduino.write(data.encode())
    arduino.close()

def main():
    message='0'
    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)#abrir la cámara y completar la inicialización de la cámara
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)#Cambiamos el ancho de la imagen 
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)#Cambiamos la altura de la imagen
    while (camera.isOpened()):#detectar si la inicialización se realizó correctamente
        ret, image = camera.read() #capturar fotogramas, image devuelve el fotograma capturado, ret true si es éxitoso la captura
        if ret== True:#Si se ha capturado correctamente el fotograma
            cv2.imshow('video',image)#Mostrar la serie de fotogramas que se están tomando
            if cv2.waitKey(1) & 0xFF == ord('t'):#Si se preciona la tecla: t , entra al condicional
                cv2.imwrite('capture.png', image)#Se guarda el fotograma cuando se presiono la tecla
                camera.release()#Apaga la camara
                cv2.destroyAllWindows()#Destruir todas las ventanas que se hayan mostrado anteriormente con cv2
                break#Sale del ciclo while
        else: #En caso de no poder capturar un fotograma
            print('Error al intentar ingresar a la camara')#Mostrar posible error de pq no se capturo fotograma
    with open("capture.png", mode="rb") as captured_image: #Abre la imagen guardada en formato de lectura
        results = predictor.detect_image("ID del proyecto","Aquí el nombre con el que el proyecto fue desplegado",captured_image)#Se envia la imagen tomada con el id y el nombre del proyecto
    for prediction in results.predictions:#Se miran todas las predicciones hechas por Azure almacenadas en results cuando enviamos la imagen
        if prediction.probability > 0.5:#Para todas las predicciones que se hayan tenido que sean mayores a un 50% de seguridad
            print(prediction)
            bbox = prediction.bounding_box#Cuadros delimetadores que se obtienen de la predicción
            #Para los cuadros delimitadores, hacemos un cálculo simple basado en el tamaño de la imagen, establecemos el color del cuadro delimitador y el grosor del borde. 
            #Dibujamos estos cuadros delimetadores en la imagen
            result_image = cv2.rectangle(image, (int(bbox.left * 640), int(bbox.top * 480)), (int((bbox.left + bbox.width) * 640), int((bbox.top + bbox.height) * 480)),(137,87,35), 3)
            cv2.putText(image,f"Spider ({round(prediction.probability*100,2)})",(int(bbox.left * 630)+60, int(bbox.top * 470)-25),1, 1,(22,37,33),2)
            cv2.imwrite('capture.png', result_image)#Se guarda la imagen que se mando al servicio de custom vision
            message='1'
    ArduinoMessage(message)
    imagen = cv2.imread('capture.png') 
    cv2.imshow('Object detection',imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    """El objeto serial recibe por lo menos dos parametros, primero el puerto donde se conecta
    el arduino y como segundo la velocidad a la cual se inicia la comunicacion serial (la misma que en Arduino)"""
    arduino=serial.Serial('COM5',9600)
    time.sleep(2)#La documentación oficial indica que se debe dar esos 2segundos como minimo
    main()