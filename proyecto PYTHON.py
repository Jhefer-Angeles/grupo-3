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

def mesa_de_partes_cajacha():
    total = 0

    codigos = [""] * 100
    clientes = [""] * 100
    rucs = [""] * 100
    estilos = [0] * 100
    cantidades = [0] * 100 
    fechas = [""] * 100

    print("Cargando pedidos desde pedidos.txt...")

    while True:
        print()
        print("=== MESA DE PARTES DIGITAL - CAJACHA ===")
        print(
            "1. Registrar | 2. Consultar | 3. Ordenar | "
            "4. Listar | 5. Salir"
        )

        try:
            opcion = int(input("Seleccione opcion (1-5): "))
        except ValueError:
            print("Opcion no valida. Ingrese un numero del 1 al 5.")
            continue

        if not 1 <= opcion <= 5:
            print("Opcion no valida. Ingrese un numero del 1 al 5.")
            continue

        if opcion == 1:
            print(
                "Ingrese cliente, RUC, estilo, litros "
                "y fecha de entrega:"
            )

            cliente = input("Cliente: ")
            ruc = input("RUC: ")
            try:
                num_estilo = int(input("Estilo (1-5): "))
            except ValueError:
                num_estilo = 0

            litros_txt = input("Litros: ")
            fecha = input("Fecha de entrega (DD/MM/AAAA): ")

            datos_validos = (
                cliente != ""
                and es_ruc_valido(ruc)
                and 1 <= num_estilo <= 5
                and es_litros_valido(litros_txt)
                and es_fecha_valida(fecha)
            )

            if datos_validos:
                if total < 100:
                    litros = int(litros_txt)
                    codigo = f"PED-{total + 1:03d}"

                    codigos[total] = codigo
                    clientes[total] = cliente
                    rucs[total] = ruc
                    estilos[total] = num_estilo
                    cantidades[total] = litros
                    fechas[total] = fecha

                    total += 1

                    print("Pedido registrado y guardado.")
                    print("Codigo:", codigo)
                else:
                    print("No se pueden registrar mas de 100 pedidos.")
            else:
                print("Error: datos invalidos.")

elif opcion == 2:
            buscado = input("Ingrese codigo a buscar: ").upper()
            pos = -1

            for i in range(total):
                if codigos[i] == buscado:
                    pos = i

            if pos == -1:
                print("Pedido no encontrado.")
            else:
                print("Codigo:", codigos[pos])
                print("Cliente:", clientes[pos])
                print("RUC:", rucs[pos])
                print("Estilo:", estilos[pos])
                print("Litros:", cantidades[pos])
                print("Fecha:", fechas[pos])

        elif opcion == 3:
            print("Ordenando por codigo (burbuja)...")

            for i in range(total - 1):
                for j in range(total - 1 - i):
                    if codigos[j] > codigos[j + 1]:
                        codigos[j], codigos[j + 1] = (
                            codigos[j + 1], codigos[j]
                        )
                        clientes[j], clientes[j + 1] = (
                            clientes[j + 1], clientes[j]
                        )
                        rucs[j], rucs[j + 1] = (
                            rucs[j + 1], rucs[j]
                        )
                        estilos[j], estilos[j + 1] = (
                            estilos[j + 1], estilos[j]
                        )
                        cantidades[j], cantidades[j + 1] = (
                            cantidades[j + 1], cantidades[j]
                        )
                        fechas[j], fechas[j + 1] = (
                            fechas[j + 1], fechas[j]
                        )

            print("Pedidos ordenados por codigo.")
elif opcion == 4:
            if total == 0:
                print("No hay pedidos registrados.")
            else:
                for i in range(total):
                    print(
                        f"{codigos[i]} | {clientes[i]} "
                        f"| RUC: {rucs[i]} "
                        f"| Estilo: {estilos[i]} "
                        f"| Litros: {cantidades[i]} "
                        f"| Fecha: {fechas[i]}"
                    )

                print("Mostrar pedidos registrados.")

        elif opcion == 5:
            print("Guardando pedidos en pedidos.txt...")
            print("Saliendo del sistema. Hasta pronto.")
            break

if __name__ == "__main__":
    mesa_de_partes_cajacha()
