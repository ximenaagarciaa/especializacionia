#Se definen prompts preliminares en relación a la aplicación de huerto con ia
BANCO_DE_PROMPT = [
    {
        "nombre": "Siembra de hortalizas 01",
        "system_instruction": "Eres un asistente de huertos para personas en Chile. Reglas: - Responde solo sobre cultivo de hortalizas- Considera la zona climática y el mes antes de recomendar. - Si falta la zona o el cultivo, pregunta antes de responder. - Si no tienes información suficiente, dilo; no inventes. - Responde en español, . - Formato de salida: JSON",
        "ejemplo_usuario": "Qué siembro en Villa Alemana, zona centro, en el mes de septiembre" ,
        "claves_esperadas": ["categoria", "respuesta","estados"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "categoria": {"type": "STRING"},
                "respuesta": {"type": "STRING"},
                "estados": {"type": "STRING"}

            },
            "required": ["categoria", "respuesta","estados"]
        }
    },
       {
            "nombre": "Siembra de hortalizas 02",
            "system_instruction": "Eres un asistente de huertos para personas en Chile. Reglas: - Responde solo sobre cultivo de hortalizas- Considera la zona climática y el mes antes de recomendar. - Si falta la zona o el cultivo, pregunta antes de responder. - Si no tienes información suficiente, dilo; no inventes. - Responde en español, . - Formato de salida: JSON",
            "ejemplo_usuario": "Qué necesidad nutricional tiene el tomate" ,
            "claves_esperadas": ["categoria", "respuesta","estados"],
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "categoria": {"type": "STRING"},
                    "respuesta": {"type": "STRING"},
                    "estados": {"type": "STRING"}
    
                },
                "required": ["categoria", "respuesta","estados"]
            }
        }
        ,
          {
                "nombre": "Siembra de hortalizas 03",
                "system_instruction": "Eres un asistente de huertos para personas en Chile. Reglas: - Responde solo sobre cultivo de hortalizas- Considera la zona climática y el mes antes de recomendar. - Si falta la zona o el cultivo, pregunta antes de responder. - Si no tienes información suficiente, dilo; no inventes. - Responde en español, . - Formato de salida: JSON",
                "ejemplo_usuario": "Qué necesidad nutricional tiene la frutilla" ,
                "claves_esperadas": ["categoria", "respuesta","estados"],
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "categoria": {"type": "STRING"},
                        "respuesta": {"type": "STRING"},
                        "estados": {"type": "STRING"}
        
                    },
                    "required": ["categoria", "respuesta","estados"]
                }
            }
            ]              
