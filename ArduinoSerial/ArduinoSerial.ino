int PinLuz=13;//Pin donde conectaremos la salida al relevador

void setup() {
  Serial.begin(9600);//bits x segundo estandar de arduino uno
  pinMode(PinLuz,OUTPUT);//Configuramos como salida al bit al rele
  digitalWrite(PinLuz, HIGH);//Ponemos en alto la salida 
  //Con releveador de 2 o mas canales trabaja con logica inversa
}

void loop() {
  if (Serial.available()>0){//Saber si nos han mandado datos //entra al buffer donde esta la memoria de los datos almacenados que nos estan enviando
  char mensaje=Serial.read();// Se lee lo que exista en el puerto serial y se almacena
  if(mensaje=='1'){
    digitalWrite(PinLuz,LOW);
  }
  if(mensaje=='0'){
    digitalWrite(PinLuz,HIGH);
    }
  }
  delay(100);
}
