#para obtener variables de configuración
import os
import requests
from dotenv import load_dotenv
import time
import re
import json



load_dotenv()
#constantes
#MODELO = "gemini-flash-latest"

MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

precio_entrada= 0.00000075
precio_salida=0.00000375
pregunta = "que cultivos se deben sembrar en primavera"


# función para crear la solicitud
def armar_peticion(MODELO, pregunta, systeminstruction, response_schema=None): 
    if not pregunta:
       raise ValueError("La pregunta no puede estar vacía")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
    body = {
      "systemInstruction": {

        "parts": [{"text": systeminstruction}]

      },

      "contents": [{

         "parts": [{"text": pregunta}]

      }]

    }
    if response_schema is not None:
            body["generationConfig"] = {
               "responseMimeType": "application/json",
               "responseSchema": response_schema
            }
           
    return url, body



# función envía la petición
def enviar_peticion(url, body):
    try:    

       
       respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pude realizar la conexión")
    except requests.exceptions.Timeout:
        raise RuntimeError("Se agoto el tiempo")
    if respuesta.status_code!= 200:
       raise RuntimeError(f"Error en la petición, Status Code: {respuesta.status_code}")  

    try:
       return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servidor, no llego en el formato correcto")
  

    


# función procesa y extrae dato
def extraer_texto(datos):  # Gemini
    try:
       return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError , IndexError):
       raise RuntimeError("La respuesta no contiene  el texto generado en el lugar definido")

     

def obtener_respuesta_final(pregunta):  # pregunta, corresponde al tema que se desea saber
    systeminstruction = "Como agricultor de huerto hurbano,en chile, zona centro,v REGION,NO INCLUYAS TOMATES, Responde con un objeto de json:" \
    " 'Nombre hortaliza' y 'recomendacion de cultivo', NO INCLUYAS EXPLICACIONES, NI SALUDOS, NI DESPEDIDAS, NI FRASES DE CIERRE, NI FRASES DE INTRODUCCION, SOLO EL OBJETO JSON"
    
    response_schema = {
      "type": "OBJECT",
      "properties": {
         "Nombre hortaliza": { "type": "STRING" },
         "recomendacion de cultivo": { "type": "STRING" }
      },
      "required": ["Nombre hortaliza", "recomendacion de cultivo"]
      }
   
    url, body = armar_peticion(MODELO, pregunta, systeminstruction, response_schema)  # obtiene url y body

    # url = resultado de armar_peticion
    # body = resultado de armar_peticion
   
    inicio = time.perf_counter() #Empezar el contador
    datos = enviar_peticion(url, body)
    fin = time.perf_counter() #Termina el contador
    latencia = fin - inicio
    print(f"Latencia: {latencia:.2f} segundos")
    costo = calcular_costo(datos, precio_entrada, precio_salida)
    print(f"Costo de la petición: ${costo:.6f} USD")  
    texto = extraer_texto(datos)
    datos_formateados = parsear_respuesta_json(texto, claves_requeridas=["Nombre hortaliza", "recomendacion de cultivo"])
    return datos_formateados

#calcular_costo(datos:dict,precio_entrada:float, precio_salida:float) ->float
def calcular_costo(datos, precio_entrada, precio_salida):
   
    uso= datos["usageMetadata"]
    token_entrada =uso["promptTokenCount"]
    token_salida= uso["candidatesTokenCount"]
    token_razonamiento= uso["thoughtsTokenCount"]
    costo_total = token_entrada* precio_entrada + (token_razonamiento + token_salida)* precio_salida
    return costo_total

def parsear_respuesta_json(texto, claves_requeridas=None):
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    try:
      datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
            raise ValueError("La respuesta del modelo no es JSON válido.")
    if claves_requeridas:
       faltantes = [clave for clave in claves_requeridas if clave not in datos]
       if faltantes:
          raise ValueError("La respuesta no tiene la estructura esperada.")
    return datos
if __name__ == "__main__": #solo ejecuta si este archivo es ejecuto directamnete      
   try:
  # obtener_dato_de_prueba
  # print(obtener_dato_de_prueba(pregunta))
     pregunta_f = obtener_respuesta_final(pregunta)
     print(f"Resultado: {pregunta_f}")
     print("Resultado:")
     print(json.dumps(pregunta_f, indent=2, ensure_ascii=False))  
      
   except (ValueError, RuntimeError) as error:
      print ("No se pudo concretar la operación, el error es:", error)  