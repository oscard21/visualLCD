import logging
import flet as ft

from exchanges.binance import Binance as Exchange

logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    exchange = Exchange()

    def ui_limpiar():
        # Coloca el count en los titulos
        count_positivos = 0
        ui_titulo_positivo.value = f'Positivos ({count_positivos})'

        count_negativos = 0
        ui_titulo_negativo.value = f'Negativos ({count_negativos})'

        ui_lista_positivos.clean()
        ui_lista_negativos.clean()

    def ui_buscar_click(e):
        logging.info(f'Días a buscar: {ui_dias.value}')
        ui_buscar.disabled = True
        ui_buscar_progreso.visible = True
        ui_limpiar()
        page.update()

        # Trae la información del exchange
        logging.info('Trayendo la información del exchange...')
        negativos, positivos = exchange.get_result(ui_dias.value)

        # Coloca el count en los titulos
        count_positivos = len(positivos)
        ui_titulo_positivo.value = f'Positivos ({count_positivos})'

        count_negativos = len(negativos)
        ui_titulo_negativo.value = f'Negativos ({count_negativos})'

        # recorre los positivos
        for item in positivos:
            texto = ft.Text(
                f"{item['symbol']}: OLD: {item['old']}, NEW: {item['new']}, PERCENT: {item['percent']}%", color=ft.colors.GREEN)
            ui_lista_positivos.controls.append(texto)
            page.update()

        # recorre los negativos
        for item in negativos:
            texto = ft.Text(
                f"{item['symbol']}: OLD: {item['old']}, NEW: {item['new']}, PERCENT: {item['percent']}%", color=ft.colors.RED)
            ui_lista_negativos.controls.append(texto)
            page.update()

        ui_buscar.disabled = False
        ui_buscar_progreso.visible = False
        page.update()

    page.title = 'Visual LCD'
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    ui_dias = ft.TextField(label='Días', autofocus=True, value=7,
                           keyboard_type=ft.KeyboardType.NUMBER, width=100)
    ui_buscar = ft.FloatingActionButton(
        icon=ft.icons.SEARCH, on_click=ui_buscar_click)

    ui_buscar_progreso = ft.ProgressBar(
        width=400, color=ft.colors.BLUE, bgcolor=ft.colors.GREY, expand=1)
    ui_buscar_progreso.visible = False

    ui_view_header = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ui_dias,
                    ui_buscar
                ]
            ),
            ft.Row(
                controls=[
                    ui_buscar_progreso
                ]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER

    )
    page.add(ui_view_header)

    ui_titulo_positivo = ft.Text(
        'Positivos (0)', size=20, color=ft.colors.GREEN, text_align=ft.TextAlign.CENTER, expand=1)
    ui_titulo_negativo = ft.Text(
        'Negativos (0)', size=20, color=ft.colors.RED, text_align=ft.TextAlign.CENTER, expand=1)

    ui_lista_positivos = ft.ListView(
        expand=1, spacing=10, padding=20)
    ui_lista_negativos = ft.ListView(
        expand=1, spacing=10, padding=20)

    ui_view_content = ft.Column(
        [
            ft.Row(
                [
                    ui_titulo_positivo,
                    ui_titulo_negativo
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            ft.Row(
                [
                    ui_lista_positivos,
                    ui_lista_negativos
                ],
                expand=1,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ],
        expand=1,
    )
    page.add(ui_view_content)


ft.app(target=main)
