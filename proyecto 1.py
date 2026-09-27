from datetime import datetime
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

RUTA_ARCHIVO = "expedientes.txt"
SEPARADOR = "|"

ESTADOS_VALIDOS = (
    "PENDIENTE",
    "EN PROCESO",
    "ATENDIDO"
)


# ============================================================
# VALIDACIONES
# ============================================================

def validar_dni(dni):
    """
    Valida que el DNI tenga exactamente 8 dígitos numéricos.
    """
    dni = dni.strip()

    return dni.isdigit() and len(dni) == 8


def validar_nombre(nombre):
    """
    Valida que el nombre no esté vacío y contenga
    solamente letras, espacios, tildes, ñ y ü.
    """
    nombre = nombre.strip()

    if not nombre:
        return False

    letras_validas = "abcdefghijklmnopqrstuvwxyzáéíóúñü"

    for caracter in nombre.lower():
        if caracter != " " and caracter not in letras_validas:
            return False

    return True


def validar_asunto(asunto):
    """
    Valida que el asunto tenga entre 5 y 200 caracteres.
    """
    asunto = asunto.strip()

    return 5 <= len(asunto) <= 200


def normalizar_nombre(nombre):
    """
    Convierte el nombre a formato título.
    Ejemplo: juan perez -> Juan Perez
    """
    palabras = nombre.strip().split()

    return " ".join(
        palabra.capitalize()
        for palabra in palabras
    )


def normalizar_texto(texto):
    """
    Elimina espacios innecesarios al inicio y al final.
    """
    return texto.strip()


# ============================================================
# PERSISTENCIA DE DATOS
# ============================================================

def cargar_expedientes(ruta=RUTA_ARCHIVO):
    """
    Lee el archivo de expedientes y devuelve una lista
    de diccionarios.
    """
    expedientes = []

    if not os.path.exists(ruta):
        return expedientes

    with open(ruta, "r", encoding="utf-8") as archivo:

        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            campos = linea.split(SEPARADOR)

            # Una línea válida debe tener 6 campos
            if len(campos) != 6:
                continue

            expediente = {
                "codigo": campos[0],
                "dni": campos[1],
                "nombre": campos[2],
                "asunto": campos[3],
                "fecha": campos[4],
                "estado": campos[5]
            }

            expedientes.append(expediente)

    return expedientes


def guardar_expedientes(expedientes, ruta=RUTA_ARCHIVO):
    """
    Guarda todos los expedientes en el archivo de texto.
    """
    with open(ruta, "w", encoding="utf-8") as archivo:

        for exp in expedientes:

            linea = SEPARADOR.join([
                exp["codigo"],
                exp["dni"],
                exp["nombre"],
                exp["asunto"],
                exp["fecha"],
                exp["estado"]
            ])

            archivo.write(linea + "\n")


# ============================================================
# BÚSQUEDA
# ============================================================

def buscar_por_codigo(expedientes, codigo):
    """
    Busca un expediente por código mediante búsqueda lineal.
    """
    codigo = codigo.strip().upper()

    for exp in expedientes:

        if exp["codigo"].upper() == codigo:
            return exp

    return None


# ============================================================
# ORDENAMIENTO
# ============================================================

def ordenar_por_campo(expedientes, campo="codigo", ascendente=True):
    """
    Ordena una copia de la lista usando Bubble Sort.

    Campos permitidos:
    - codigo
    - nombre
    - fecha

    No modifica la lista original.
    """

    campos_validos = (
        "codigo",
        "nombre",
        "fecha"
    )

    if campo not in campos_validos:
        raise ValueError("Campo de ordenamiento inválido.")

    lista = expedientes.copy()
    n = len(lista)

    for i in range(n - 1):

        intercambio = False

        for j in range(n - 1 - i):

            valor_actual = lista[j][campo]
            valor_siguiente = lista[j + 1][campo]

            if ascendente:
                debe_intercambiar = (
                    valor_actual > valor_siguiente
                )
            else:
                debe_intercambiar = (
                    valor_actual < valor_siguiente
                )

            if debe_intercambiar:

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

                intercambio = True

        # Si no hubo intercambios,
        # la lista ya está ordenada.
        if not intercambio:
            break

    return lista


# ============================================================
# GENERAR CÓDIGO
# ============================================================

def generar_codigo(expedientes):
    """
    Genera un código único:
    EXP-0001, EXP-0002, EXP-0003, etc.
    """

    numero = len(expedientes) + 1

    codigos_existentes = {
        exp["codigo"]
        for exp in expedientes
    }

    codigo = f"EXP-{numero:04d}"

    while codigo in codigos_existentes:

        numero += 1
        codigo = f"EXP-{numero:04d}"

    return codigo


# ============================================================
# MOSTRAR EXPEDIENTE
# ============================================================

def mostrar_expediente(exp):
    """
    Muestra los datos de un expediente.
    """

    print("-" * 50)
    print(f"Código : {exp['codigo']}")
    print(f"DNI    : {exp['dni']}")
    print(f"Nombre : {exp['nombre']}")
    print(f"Asunto : {exp['asunto']}")
    print(f"Fecha  : {exp['fecha']}")
    print(f"Estado : {exp['estado']}")
    print("-" * 50)


# ============================================================
# REGISTRAR EXPEDIENTE
# ============================================================

def registrar_expediente(expedientes):
    """
    Solicita los datos del ciudadano,
    los valida y registra el expediente.
    """

    print("\n--- REGISTRO DE NUEVO EXPEDIENTE ---")

    # ----------------------------
    # DNI
    # ----------------------------

    dni = input(
        "DNI del ciudadano (8 dígitos): "
    ).strip()

    while not validar_dni(dni):

        print(
            "DNI inválido. "
            "Debe tener exactamente 8 dígitos."
        )

        dni = input(
            "DNI del ciudadano (8 dígitos): "
        ).strip()

    # ----------------------------
    # NOMBRE
    # ----------------------------

    nombre = input(
        "Nombre completo del ciudadano: "
    ).strip()

    while not validar_nombre(nombre):

        print(
            "Nombre inválido. "
            "Use solamente letras y espacios."
        )

        nombre = input(
            "Nombre completo del ciudadano: "
        ).strip()

    nombre = normalizar_nombre(nombre)

    # ----------------------------
    # ASUNTO
    # ----------------------------

    asunto = input(
        "Asunto del trámite: "
    ).strip()

    while not validar_asunto(asunto):

        print(
            "Asunto inválido. "
            "Debe tener entre 5 y 200 caracteres."
        )

        asunto = input(
            "Asunto del trámite: "
        ).strip()

    asunto = normalizar_texto(asunto)

    # ----------------------------
    # CREAR EXPEDIENTE
    # ----------------------------

    codigo = generar_codigo(expedientes)

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    estado = "PENDIENTE"

    expediente = {
        "codigo": codigo,
        "dni": dni,
        "nombre": nombre,
        "asunto": asunto,
        "fecha": fecha,
        "estado": estado
    }

    # Agregar a la lista
    expedientes.append(expediente)

    # Guardar en archivo
    guardar_expedientes(expedientes)

    print("\nExpediente registrado con éxito.")
    print(f"Código asignado: {codigo}")


# ============================================================
# BUSCAR EXPEDIENTE
# ============================================================

def buscar_expediente(expedientes):
    """
    Solicita un código y muestra el expediente encontrado.
    """

    print("\n--- BUSCAR EXPEDIENTE ---")

    codigo = input(
        "Ingrese el código del expediente: "
    )

    resultado = buscar_por_codigo(
        expedientes,
        codigo
    )

    if resultado is not None:

        mostrar_expediente(resultado)

    else:

        print(
            "No se encontró ningún expediente "
            "con ese código."
        )


# ============================================================
# LISTAR EXPEDIENTES
# ============================================================

def listar_expedientes(expedientes):
    """
    Muestra todos los expedientes ordenados.
    """

    print("\n--- LISTAR EXPEDIENTES ---")

    if not expedientes:

        print(
            "No hay expedientes registrados todavía."
        )

        return

    print("\n1. Ordenar por código")
    print("2. Ordenar por nombre")
    print("3. Ordenar por fecha")

    opcion = input(
        "Elija un criterio de orden: "
    ).strip()

    campo_map = {
        "1": "codigo",
        "2": "nombre",
        "3": "fecha"
    }

    campo = campo_map.get(opcion)

    if campo is None:

        print(
            "Opción de ordenamiento inválida."
        )

        return

    ordenados = ordenar_por_campo(
        expedientes,
        campo
    )

    print(
        f"\n--- EXPEDIENTES ORDENADOS POR {campo.upper()} ---"
    )

    for exp in ordenados:

        mostrar_expediente(exp)


# ============================================================
# ACTUALIZAR ESTADO
# ============================================================

def actualizar_estado(expedientes):
    """
    Permite cambiar el estado de un expediente.
    """

    print("\n--- ACTUALIZAR ESTADO ---")

    codigo = input(
        "Código del expediente: "
    )

    expediente = buscar_por_codigo(
        expedientes,
        codigo
    )

    if expediente is None:

        print("Expediente no encontrado.")

        return

    print("\nEstados disponibles:")

    for estado in ESTADOS_VALIDOS:

        print(f"- {estado}")

    nuevo_estado = input(
        "Nuevo estado: "
    ).strip().upper()

    if nuevo_estado not in ESTADOS_VALIDOS:

        print("Estado inválido.")

        return

    expediente["estado"] = nuevo_estado

    guardar_expedientes(expedientes)

    print(
        "Estado actualizado correctamente."
    )


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def mostrar_menu():
    """
    Muestra el menú principal.
    """

    print("\n")
    print("=" * 45)
    print("       MESA DE PARTES DIGITAL")
    print("=" * 45)
    print("1. Registrar expediente")
    print("2. Buscar expediente por código")
    print("3. Listar y ordenar expedientes")
    print("4. Actualizar estado de expediente")
    print("5. Salir")
    print("=" * 45)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    """
    Función principal del sistema.
    """

    # Cargar los expedientes existentes
    expedientes = cargar_expedientes()

    while True:

        mostrar_menu()

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion == "1":

            registrar_expediente(
                expedientes
            )

        elif opcion == "2":

            buscar_expediente(
                expedientes
            )

        elif opcion == "3":

            listar_expedientes(
                expedientes
            )

        elif opcion == "4":

            actualizar_estado(
                expedientes
            )

        elif opcion == "5":

            print(
                "\nSaliendo del sistema. "
                "¡Hasta pronto!"
            )

            break

        else:

            print(
                "\nOpción no válida. "
                "Intente nuevamente."
            )


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()
