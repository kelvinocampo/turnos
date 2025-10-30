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


def ingresar_turno():
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


for dia in dias:
    recargo_inicial = recargo
    extras_inicial = extras

    turno, salir = ingresar_turno()
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
    elif turno["hora_fin"] > 21 and turno["dia"] != "domingo" and not turno["extra"]:
        recargo_nocturnas += horas_nocturnas
    elif turno["turno"] == "dia" and turno["dia"] == "domingo" and not turno["extra"]:
        recargo_dominicales += turno["horas"]

print("----- Resumen -----")
print("Turnos registrados:")
for turno in turnos:
    hora_fin_formato = (
        str(turno["hora_fin"] - 24)
        if turno["hora_fin"] > 24
        else str(turno["hora_fin"])
    )
    hora_inicio_formato = (
        str(turno["hora_inicio"] - 24)
        if turno["hora_inicio"] > 24
        else str(turno["hora_inicio"])
    )
    print(
        f"""
        Dia: {turno['dia']}, 
        Hora inicio: {hora_inicio_formato}, 
        Hora fin: {hora_fin_formato}, 
        Turno: {turno['turno']}, 
        Extra: {turno['extra']}, 
        Horas: {turno['horas']}
          """
    )
    print("-" * 10)

print("Recargo total horas:", recargo)
print("Extras total horas:", extras)
print("\nDetalle recargos:")
print("Recargo nocturnas:", recargo_nocturnas)
print("Recargo dominicales:", recargo_dominicales)
print("Recargo dominicales nocturnas:", recargo_dominicales_nocturnas)
print("\nDetalle extras:")
print("Extras nocturnas:", extras_nocturnas)
print("Extras dominicales:", extras_dominicales)
print("Extras dominicales nocturnas:", extras_dominicales_nocturnas)
