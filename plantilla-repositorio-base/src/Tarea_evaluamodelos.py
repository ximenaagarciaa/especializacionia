#para obtener variables de configuración
import os
import requests
from dotenv import load_dotenv
import time
load_dotenv()
#constantes

pregunta = "Eres un experto en horticultura en Chile. Indica los requisitos para sembrar tomates en Villa Alemana, Región de Valparaíso, considerando su clima mediterráneo.Incluye: época de siembra, temperatura, horas de sol, suelo, riego, nutrientes y distancia de plantaciónComo agricultor dime el cultivo de hortaliza mas productivo para la v region de chile"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#Valores referenciales obtenidos desde https://ai.google.dev/gemini-api/docs/pricing?hl=es-419, con fecha 24-10-2026
modelos = [
    {
        "nombre": "gemini-3.5-flash-lite",
        "precio_entrada": 0.0000003,  
        "precio_salida": 0.0000025    
    },
    {
        "nombre": "gemini-3.6-flash",
        "precio_entrada": 0.00000075,
        "precio_salida":  0.00000375
    },
    {  "nombre": "gemini-3.8-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    }
]


# función para crear la solicitud
def armar_peticion(MODELO,pregunta):  # pregunta , se define en constantes
   if not pregunta:
      raise ValueError("La pregunta no puede estar vacía")
   url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
   body = {
      "contents": [
            {"parts": [{"text": pregunta}]} ]
         }
   return url, body



# función envía la petición
def enviar_peticion(url, body):
   try:        
      respuesta = requests.post(url, json=body, timeout=120)
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



#calcular_costo(datos:dict,precio_entrada:float, precio_salida:float) ->float
def calcular_costo(datos, precio_entrada, precio_salida):
   
   uso= datos["usageMetadata"]
   token_entrada =uso["promptTokenCount"]
   token_salida= uso["candidatesTokenCount"]
   #  token_razonamiento= uso["thoughtsTokenCount"]
   token_razonamiento = uso.get("thoughtsTokenCount", 0)
   costo_total = token_entrada* precio_entrada + (token_razonamiento + token_salida)* precio_salida
   return costo_total

# función que invoca la evaluación de un modelo específico varias veces y calcula latencia y costo
def evaluar_modelo(MODELO, pregunta, precio_entrada, precio_salida, repeticiones=4):
    """
    Ejecuta 'repeticiones' veces la misma petición para un modelo específico.
    Calcula e imprime Latencia, Costo y Respuesta de cada intento,
    además del promedio de latencia al final.
    """
    print("=" * 70)
    print(f" EVALUANDO MODELO: {MODELO}")
    print("=" * 70)
    
    latencias = []
    costos = []

    for i in range(1, repeticiones + 1):
        print(f"\n--- Intento {i} de {repeticiones} ({MODELO}) ---")
        time.sleep(3)  # Espera de 3 segundos entre intentos
        # 1. Armar petición (puedes pasar el modelo si tu función lo requiere)
        url, body = armar_peticion(MODELO,pregunta) 

        # 2. Medir latencia
        inicio = time.perf_counter()  # tiempo de inicio para calcular latencia
        datos = enviar_peticion(url, body)
        fin = time.perf_counter()  # tiempo de fin de recepción de datos, para calcular latencia  
        latencia = fin - inicio
        latencias.append(latencia)
        
        # 3. Calcular costo
        costo = calcular_costo(datos, precio_entrada, precio_salida) # función para calcular costo de la petición      
        costos.append(costo)
        
        # 4. Extraer respuesta
        respuesta = extraer_texto(datos)
        
        # 5. Imprimir resultados de la petición actual
        print(f"Tiempo de latencia:  {latencia:.2f} segundos")
        print(f"Costo de la petición:    ${costo:.6f} USD")
        print(f"Respuesta: {respuesta}")

    # Resumen acumulado del modelo
    latencia_promedio = sum(latencias) / len(latencias)
    costo_total = sum(costos)
    
    print("\n" + "-" * 40)
    print(f" RESUMEN {MODELO}:")
    print(f" Latencia promedio: {latencia_promedio:.2f} segundos")
    print(f" Costo acumulado ({repeticiones} peticiones): ${costo_total:.6f} USD")
    print("-" * 40 + "\n")





# Procesar los 3 modelos consecutivamente
for iteramodelo in modelos:

    nombre_modelo=iteramodelo["nombre"]
    precio_entrada=iteramodelo["precio_entrada"]
    precio_salida=iteramodelo["precio_salida"]
    evaluar_modelo(nombre_modelo, pregunta, precio_entrada, precio_salida, repeticiones=4)