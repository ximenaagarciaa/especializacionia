import time
from typing import Any, Callable
from src.consumir_gemini_ref    import armar_peticion, enviar_peticion, extraer_texto
 #función, intentos, espera_segundos. Valor retorno :Cualquiera
def con_reintento(
        funcion: Callable[[], Any],
        intentos: int = 3, 
        espera_segundos: int = 2
) -> Any:
    """
    Decorador para reintentar la ejecución de una función en caso de error.
    
    Args:
        funcion (Callable): La función a ejecutar.
        intentos (int): Número de intentos antes de fallar.
        espera_segundos (int): Tiempo de espera entre intentos en segundos.
    
    Returns:
        Any: El resultado de la función si tiene éxito.
    
    Raises:
        Exception: La última excepción lanzada si todos los intentos fallan.
    """
    for intento in range(intentos):
        try:
            return funcion() #detiene en este momento elp proceso y espera que se ejecute la funcion
        except TimeoutError as e:
               if intento == intentos - 1:
                     raise
               print(f"Intento {intento + 1} de {intento} segundos..."   )
               time.sleep(espera_segundos)
       