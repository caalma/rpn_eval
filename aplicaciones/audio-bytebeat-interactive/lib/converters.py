def seconds_to_texttime(segundos):
    """
    Convierte un valor decimal de segundos en el formato hh horas mm minutos ss segundos.

    :param segundos: float - Valor en segundos.
    :return: str - Cadena formateada como 'hh horas mm minutos ss segundos'.
    """
    # Convertir a entero si es necesario
    segundos = int(segundos)

    # Calcular horas, minutos y segundos
    horas = segundos // 3600  # División entera para obtener las horas
    resto = segundos % 3600   # Resto después de extraer las horas
    minutos = resto // 60     # División entera para obtener los minutos
    segundos_finales = resto % 60  # Resto después de extraer los minutos

    # Formatear la salida
    return f"{horas} horas {minutos} minutos {segundos_finales} segundos"


async def async_print(t):
    print(t)
