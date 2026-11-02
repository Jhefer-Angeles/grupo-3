import base64
import os

PNG_LOGO = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAOElEQVR42mP4"
    "f5CdJMQAxCISGkQiOmtgOFGBB1FPA9x2CBekgiQNcD1EOQluPFX9QEsNgypp"
    "kIQAxUrwwgzJRdUAAAAASUVORK5CYII="
)

ROLES_VALIDOS = ("PRO", "ART", "DIS", "SON") 

try:
    if not os.path.isfile("estudio_gamer.txt"):
        estudio = input("Nombre de tu estudio: ").strip()

        if not estudio:
            raise ValueError("El estudio necesita un nombre.")

        with open("estudio_gamer.txt", "w", encoding="utf-8") as archivo:
            archivo.write(f"{estudio}\n100\n")

        print(f"¡Bienvenido a {estudio}! Presupuesto inicial: 100 mil dólares.")

    if not os.path.isfile("logo_estudio.png"):
        with open("logo_estudio.png", "wb") as archivo:
            archivo.write(base64.b64decode(PNG_LOGO))

        print("Logo de tu estudio creado.")

    with open("logo_estudio.png", "rb") as archivo:
        logo = archivo.read()

    if not logo.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("El logo no tiene una firma PNG válida.")

    print(f"Logo recuperado: {len(logo)} bytes.")

    with open("estudio_gamer.txt", "r", encoding="utf-8") as archivo:
        registros = archivo.read().splitlines()

    estudio = registros[0]
    presupuesto = int(registros[1])
    empleados = [registro.split("|") for registro in registros[2:]]

    saldo = presupuesto - sum(int(e[2]) for e in empleados)

    print(f"Presupuesto disponible: {saldo} mil dólares.")

    empleado = input("Desarrollador a contratar: ").strip()
    rol = input("Rol (PRO/ART/DIS/SON): ").strip().upper()
    salario = int(input("Salario (miles de dólares): "))

    if (
        not empleado
        or "|" in empleado
        or rol not in ROLES_VALIDOS
        or salario <= 0
    ):
        print("Datos de la contratación inválidos.")

    elif any(empleado.casefold() == e[0].casefold() for e in empleados):
        print("El desarrollador ya trabaja en tu estudio.")

    elif salario > saldo:
        print("Presupuesto insuficiente.")

    else:
        with open("estudio_gamer.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{empleado}|{rol}|{salario}\n")

        print("Contratación registrada.")

    with open("estudio_gamer.txt", "r", encoding="utf-8") as archivo:
        registros = archivo.read().splitlines()

    saldo = int(registros[1])
    print(f"\nESTUDIO: {registros[0]}")

    for registro in registros[2:]:
        nombre, rol_emp, pago = registro.split("|")
        saldo -= int(pago)
        print(f"- {nombre} | {rol_emp} | {pago} mil dólares")

    print(f"Saldo restante: {saldo} mil dólares.")

except (OSError, ValueError, IndexError) as error:
    print(f"Operación interrumpida: {error}")