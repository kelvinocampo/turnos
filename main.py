import flet as ft

dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def main(page: ft.Page):
    page.title = "Registro de Turnos"
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Variables globales de estado
    recargo = 0
    extras = 0
    turnos = []
    identificador = ft.TextField(label="Identificador del documento", width=300)

    # Elementos UI dinámicos
    salida_texto = ft.Text("", selectable=True)
    dropdown_turno = ft.Dropdown(
        label="Selecciona el tipo de turno",
        options=[
            ft.dropdown.Option("1 - Diurno"),
            ft.dropdown.Option("2 - Nocturno"),
            ft.dropdown.Option("3 - No registra"),
            ft.dropdown.Option("4 - Detener registro"),
        ],
        width=300,
    )

    # Estado de índice del día actual
    dia_index = {"value": 0}

    # -----------------------------------------------------
    # Funciones de lógica (idénticas a tu código base)
    # -----------------------------------------------------

    def registrar_turno(dias, recargo, extras, turnos, dia, turno):
        recargo_inicial = recargo
        extras_inicial = extras
        salir = False

        if turno == "1 - Diurno":
            turno = "dia"
        elif turno == "2 - Nocturno":
            turno = "nocturno"
        elif turno == "3 - No registra":
            return recargo, extras, turnos, salir
        elif turno == "4 - Detener registro":
            salir = True
            return recargo, extras, turnos, salir

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
                hora_fin = 18 - extras_registrar if turno == "dia" else 30 - extras_registrar
                turno_registrar = {
                    "dia": dia,
                    "hora_inicio": hora_inicio,
                    "hora_fin": hora_fin,
                    "turno": turno,
                    "extra": False,
                    "horas": (recargo - recargo_inicial),
                }
                turnos.append(turno_registrar)

            hora_inicio = 6 + (12 - extras_registrar) if turno == "dia" else 18 + (12 - extras_registrar)
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
        return recargo, extras, turnos, salir

    def formato_hora(hora):
        hora = hora % 24
        sufijo = "AM" if 0 <= hora < 12 else "PM"
        hora_12 = hora if 1 <= hora <= 12 else abs(hora - 12)
        if hora_12 == 0:
            hora_12 = 12
        return f"{hora_12} {sufijo}"

    def printar_resumen(turnos, recargo, extras):
        resumen = "----- Resumen -----\n"
        resumen += "Turnos registrados:\n"
        resumen += "-" * 10 + "\n"

        for turno in turnos:
            hora_inicio_formato = formato_hora(turno["hora_inicio"])
            hora_fin_formato = formato_hora(turno["hora_fin"])
            tipo_hora = "Extra" if turno["extra"] else "Recargo"

            resumen += (
                f"Dia: {turno['dia']}, "
                f"Hora inicio: {hora_inicio_formato}, "
                f"Hora fin: {hora_fin_formato}, "
                f"Turno: {turno['turno']}, "
                f"Tipo de hora: {tipo_hora}, "
                f"Horas: {turno['horas']}\n"
            )
            resumen += "-" * 10 + "\n"

        resumen += f"Recargo total horas: {recargo}\n"
        resumen += f"Extras total horas: {extras}\n"
        return resumen

    def guardar_info(data, filename):
        with open(filename, "w") as f:
            for entry in data.splitlines():
                f.write(f"{entry}\n")

    # -----------------------------------------------------
    # Función principal del flujo
    # -----------------------------------------------------

    def siguiente_turno(e):
        nonlocal recargo, extras, turnos

        if dia_index["value"] >= len(dias):
            salida_texto.value = "✅ Todos los días registrados."
            page.update()
            return

        dia = dias[dia_index["value"]]
        turno = dropdown_turno.value

        if not turno:
            salida_texto.value = "⚠️ Selecciona un tipo de turno antes de continuar."
            page.update()
            return

        recargo, extras, turnos, salir = registrar_turno(dias, recargo, extras, turnos, dia, turno)

        if salir:
            mostrar_resumen()
            return

        dia_index["value"] += 1

        if dia_index["value"] < len(dias):
            dropdown_turno.value = None
            titulo_dia.value = f"📅 Día actual: {dias[dia_index['value']]}"
        else:
            mostrar_resumen()

        page.update()

    def mostrar_resumen():
        resumen = printar_resumen(turnos, recargo, extras)
        salida_texto.value = resumen
        guardar_info(resumen, f"resumen_turnos_{identificador.value}.txt")
        page.update()

    def reiniciar_app(e):
        nonlocal recargo, extras, turnos
        recargo = 0
        extras = 0
        turnos = []
        dia_index["value"] = 0
        salida_texto.value = ""
        identificador.value = ""
        dropdown_turno.value = None
        titulo_dia.value = f"📅 Día actual: {dias[0]}"
        page.update()

    # -----------------------------------------------------
    # Interfaz
    # -----------------------------------------------------

    titulo_dia = ft.Text(f"📅 Día actual: {dias[0]}", size=20, weight=ft.FontWeight.BOLD)

    page.add(
        ft.Column(
            [
                ft.Text("Registro de Turnos", size=26, weight=ft.FontWeight.BOLD),
                identificador,
                titulo_dia,
                dropdown_turno,
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar turno", on_click=siguiente_turno),
                        ft.ElevatedButton("Reiniciar", on_click=reiniciar_app),
                    ]
                ),
                ft.Divider(),
                salida_texto,
            ]
        )
    )


ft.app(target=main)
