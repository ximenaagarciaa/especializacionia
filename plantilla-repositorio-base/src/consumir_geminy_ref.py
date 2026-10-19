#para obtener variables de configuración
import os
import requests
from dotenv import load_dotenv
load_dotenv()
#constantes
MODELO = "gemini-flash-latest"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")


# función para crear la solicitud
def armar_peticion(pregunta):  # pregunta = "Confirma la conexion"
     if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
     url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
     body = {
        "contents": [
            {"parts": [{"text": pregunta}]} ]
          }
     return url, body


# armar_peticion_openai -> url, body


# función envía la petición
def enviar_peticion(url, body):
    try:        
       respuesta = requests.post(url, json=body, timeout=30)
    except respuesta.exceptions.ConnectionError:
        raise RuntimeError("No se pude realizar la conexión")
    except respuesta.exceptions.Timeout:
        raise RuntimeError("Se agoto el tiempo")
    if respuesta.status_code!= 200:
       raise RuntimeError(f"Error en la petición, Status Code: {respuesta.status_code}")  

    try:
       return respuesta.json()
    except respuesta.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servidor, no llego en el formato correcto")
    


# función procesa y extrae dato
def extraer_texto(datos):  # Gemini
    try:
       return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError , IndexError):
       raise RuntimeError("La respueta no recibe  el texto generado en el lugar definido")

     

def obtener_dato_de_prueba(pregunta):  # pregunta = "Confirma la conexion"
    url, body = armar_peticion(pregunta)  # obtiene url y body

    # url = resultado de armar_peticion
    # body = resultado de armar_peticion

    datos = enviar_peticion(url, body)
    return extraer_texto(datos)

try:
   print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión funciona"))
except (ValueError, RuntimeError) as error:
    print ("No se pudo concretar la operación, el error es:", error)  