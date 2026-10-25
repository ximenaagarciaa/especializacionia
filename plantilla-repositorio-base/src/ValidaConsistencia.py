import json
import time
from prompts.banco import BANCO_DE_PROMPT
from consumir_gemini_ref import armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json
from pathlib import Path

RUTA_REGISTRO = Path(__file__).resolve().parent / "prompts" / "registro_resultados.json"




registro ={}
try:
    #Para cada prompt en el banco de prompts, se realizan 3 intentos de obtener una respuesta válida
    exitos_total = 0
    for prompt in BANCO_DE_PROMPT:
        exitos = 0
        intentos = 3
        for intento in range(intentos):
         
           # (MODELO, pregunta, systeminstruction, response_schema=None): 
            url, body = armar_peticion("gemini-3.5-flash-lite", pregunta=prompt["ejemplo_usuario"], systeminstruction=prompt["system_instruction"], response_schema=prompt["response_schema"])
            respuesta = enviar_peticion(url, body)
            texto = extraer_texto(respuesta)
            try:
                
                datos = parsear_respuesta_json(texto, prompt["claves_esperadas"])
                exitos += 1
            except ValueError as error:
                print(f"Error al parsear respuesta para {prompt['nombre']}: {error}")
            time.sleep(2)  # Espera de 1 segundo entre intentos
            print(f"{prompt['nombre']}: {exitos}/{intentos} respuestas válidas")
            registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}
            exitos_total += 1
    with open(RUTA_REGISTRO, "w", encoding="utf-8") as archivo:
         json.dump(registro, archivo, indent=2, ensure_ascii=False)

    print(f"Resumene Final, se procesaron {len(BANCO_DE_PROMPT)} prompts. Éxitos Totales: {exitos_total}/{len(BANCO_DE_PROMPT) * intentos}")
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación:", error)