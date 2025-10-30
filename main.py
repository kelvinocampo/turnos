from persistencia import guardar_info

recargo = 0

recargo_dominicales = 0
recargo_nocturnas = 0
recargo_dominicales_nocturnas = 0

extras = 0

extras_dominicales = 0
extras_nocturnas = 0
extras_dominicales_nocturnas = 0

turnos = []
dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def ingresar_turno(dia):
    while True:
        turno = input(
            f"\nIngrese el turno a registrar dia {dia}: 1 - Diurno, 2 - Nocturno, no - No registra, exit - Detener registro: "
        )

        if not turno in ["1", "2", "no", "exit"]:
            print("\nEntrada no valida.")
            continue

        if turno == "no":
            return turno, False

        if turno == "exit":
            return turno, True

        turno = "dia" if turno == "1" else "nocturno"
        break
    return turno, False


def registar_turno(dias):
    global recargo, extras
    for dia in dias:
        recargo_inicial = recargo
        extras_inicial = extras

        turno, salir = ingresar_turno(dia)
        if turno == "no":
            continue
        if salir:
            break

        recargo += 12
        aplica_extras = recargo > 44
        if aplica_extras:
            extras_sumar = recargo - 44
            extras += extras_sumar
            recargo -= extras_sumar

        if aplica_extras:
            extras_registrar = extras - extras_inicial

            if recargo - recargo_inicial > 0:
                hora_inicio = 6 if turno == "dia" else 18
                hora_fin = (
                    18 - extras_registrar if turno == "dia" else 30 - extras_registrar
                )
                turno_registrar = {
                    "dia": dia,
                    "hora_inicio": hora_inicio,
                    "hora_fin": hora_fin,
                    "turno": turno,
                    "extra": False,
                    "horas": (recargo - recargo_inicial),
                }
                turnos.append(turno_registrar)

            hora_inicio = (
                6 + (12 - extras_registrar)
                if turno == "dia"
                else 18 + (12 - extras_registrar)
            )

            hora_fin = 18 if turno == "dia" else 30
            turno_registrar = {
                "dia": dia,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "turno": turno,
                "extra": aplica_extras,
                "horas": extras_registrar,
            }
        else:
            hora_inicio = 6 if turno == "dia" else 18
            hora_fin = 18 if turno == "dia" else 30
            turno_registrar = {
                "dia": dia,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "turno": turno,
                "extra": aplica_extras,
                "horas": (recargo - recargo_inicial),
            }

        turnos.append(turno_registrar)
registar_turno(dias)


def calcular_recargos_extras(turnos):
    global recargo_dominicales, recargo_nocturnas, recargo_dominicales_nocturnas
    global extras_dominicales, extras_nocturnas, extras_dominicales_nocturnas
    for turno in turnos:
        horas_nocturnas = turno["hora_fin"] - turno["hora_inicio"]
        horas_nocturnas -= 3 if turno["hora_inicio"] < 21 else 0

        # Extra
        if turno["hora_fin"] > 21 and turno["dia"] == "domingo" and turno["extra"]:
            extras_dominicales_nocturnas += horas_nocturnas
        elif turno["hora_fin"] > 21 and turno["dia"] != "domingo" and turno["extra"]:
            extras_nocturnas += horas_nocturnas
        elif turno["turno"] == "dia" and turno["dia"] == "domingo" and turno["extra"]:
            extras_dominicales += turno["horas"]

        # Recargo
        if turno["hora_fin"] > 21 and turno["dia"] == "domingo" and not turno["extra"]:
            recargo_dominicales_nocturnas += horas_nocturnas
        elif (
            turno["hora_fin"] > 21 and turno["dia"] != "domingo" and not turno["extra"]
        ):
            recargo_nocturnas += horas_nocturnas
        elif (
            turno["turno"] == "dia" and turno["dia"] == "domingo" and not turno["extra"]
        ):
            recargo_dominicales += turno["horas"]
calcular_recargos_extras(turnos)


def printar_resumen():
    resumen = "----- Resumen -----\n"
    resumen += "Turnos registrados:\n"
    resumen += "-" * 10 + "\n"

    for turno in turnos:
        # Ajuste de formato de horas
        def formato_hora(hora):
            hora = hora % 24  # Normaliza si pasa de 24
            sufijo = "AM" if 0 <= hora < 12 else "PM"
            hora_12 = hora if 1 <= hora <= 12 else abs(hora - 12)
            if hora_12 == 0:
                hora_12 = 12
            return f"{hora_12} {sufijo}"

        hora_inicio_formato = formato_hora(turno["hora_inicio"])
        hora_fin_formato = formato_hora(turno["hora_fin"])

        resumen += (
            f"Dia: {turno['dia']}, "
            f"Hora inicio: {hora_inicio_formato}, "
            f"Hora fin: {hora_fin_formato}, "
            f"Turno: {turno['turno']}, "
            f"Extra: {turno['extra']}, "
            f"Horas: {turno['horas']}\n"
        )
        resumen += "-" * 10 + "\n"

    resumen += f"Recargo total horas: {recargo}\n"
    resumen += f"Extras total horas: {extras}\n\n"

    resumen += "Detalle recargos:\n"
    resumen += f"Recargo nocturnas: {recargo_nocturnas}\n"
    resumen += f"Recargo dominicales: {recargo_dominicales}\n"
    resumen += f"Recargo dominicales nocturnas: {recargo_dominicales_nocturnas}\n\n"

    resumen += "Detalle extras:\n"
    resumen += f"Extras nocturnas: {extras_nocturnas}\n"
    resumen += f"Extras dominicales: {extras_dominicales}\n"
    resumen += f"Extras dominicales nocturnas: {extras_dominicales_nocturnas}\n"

    print(resumen)
    return resumen
resumen = printar_resumen()

guardar_info(resumen.splitlines(), "resumen_turnos.txt")
