def es_numero_entero_positivo(texto):
    return len(texto) > 0 and all(
        caracter in "0123456789" for caracter in texto
    )

def es_ruc_valido(ruc):
    # Validación básica: exactamente 11 dígitos.
    # No verifica el dígito de control del RUC.
    return len(ruc) == 11 and es_numero_entero_positivo(ruc)

def es_litros_valido(texto):
    return es_numero_entero_positivo(texto) and int(texto) > 0

def es_fecha_valida(fecha):
    # Validación básica: DD/MM/AAAA.
    # Admite días del 1 al 31; no distingue la duración de cada mes.
    if len(fecha) != 10:
        return False

    if fecha[2] != "/" or fecha[5] != "/":
        return False

    texto_dia = fecha[0:2]
    texto_mes = fecha[3:5]
    texto_año = fecha[6:10]

    if not all(
        es_numero_entero_positivo(parte)
        for parte in (texto_dia, texto_mes, texto_año)
    ):
        return False

    dia = int(texto_dia)
    mes = int(texto_mes)
    año = int(texto_año)

    return 1 <= dia <= 31 and 1 <= mes <= 12 and año >= 1
