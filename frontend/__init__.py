import traceback
import webbrowser

import PySimpleGUI as sg

from functions import functions as fc
from functions import parameters


class ProgramPainel:
    def __init__(self):
        # Parameters
        FONT_STR = 'Arial, 12'
        SIZE_INPUT = (12, 1)
        sg.theme('DarkGrey')
        # Layout
        layout = [
            [
                sg.Text('Cod. Material'),
                sg.Input(key='material', size=SIZE_INPUT),
                sg.Text('Linha'),
                sg.Combo(parameters.PRODUCTION_LINE, key='linha'),
                sg.Text(f'{"":^14}'),
                sg.Image(
                    'static/githublogo.png',
                    enable_events=True,
                    key='link',
                    tooltip='acessar',
                )
            ],
            [
                sg.Text('Qtd P/ Produzir'),
                sg.Input(
                    key='produzir',
                    size=SIZE_INPUT,
                ),
                sg.Text(
                    f'{"By: LEONARDOHMS":>40}',
                    enable_events=True,
                    text_color=('black'),
                    font='Arial, 12',
                ),
            ],
            [
                sg.Text('Setup'),
                sg.Combo(fc.HOURS, key='set_hora', default_value='00'),
                sg.Combo(fc.MINUTES, key='set_min',
                         default_value='00'),
                sg.Text('Data início'),
                sg.Input(key='dia', size=SIZE_INPUT),
                sg.CalendarButton(
                    'Calendário', format='%d-%m-%Y',
                    month_names=parameters.MONTHS,
                    day_abbreviations=parameters.ACRON_DAYS,
                ),
            ],
            [
                sg.Radio(
                    'diurno',
                    group_id='radio_periodo',
                    default=True,
                    key='diurno'
                ),
                sg.Radio(
                    'noturno',
                    group_id='radio_periodo',
                    key='noturno'
                ),
            ],
            [
                sg.Button('Confirmar'),
                sg.Button('24 Horas'),
                sg.Text(f'{"Hora início":>29}'),
                sg.Combo(fc.HOURS, key='horas', default_value='07'),
                sg.Text(':'),
                sg.Combo(fc.MINUTES, key='minutos',
                         default_value='10'),
                sg.Text('H. Extra:'),
                sg.Checkbox('', default=False, key='extra')
            ],
            [sg.Multiline(
                size=(50, 18),
                key='__OUTPUT__',
                font=FONT_STR,
                do_not_clear=False
            )],
            [sg.Text('--Tempo Aproximado--')]
        ]

        # Window
        self.window = sg.Window(
            'Tempo de produção',
            icon='static/python.ico'
        ).layout(layout)
        sg.cprint_set_output_destination(
            multiline_key='__OUTPUT__', window=self.window)

    def startProgram(self):
        while True:
            event, self.values = self.window.Read()
            if event == sg.WIN_CLOSED:
                break
            try:
                if event == 'Confirmar':
                    set_horas = f'{self.values["set_hora"]}:'\
                        f'{self.values["set_min"]}:00'
                    hora = f'{self.values["horas"]}:'\
                        f'{self.values["minutos"]}:00'
                    qtd_hora = fc.get_qty_hour(
                        self.values["material"].strip(),
                        self.values["linha"].strip()
                    )
                    if qtd_hora == 'NP':
                        sg.cprint('Material não é produzido nesta linha!')
                    else:
                        if self.values['extra']:
                            minutos_dia = 648
                        else:
                            minutos_dia = 528
                        # 48 seria tempo parado, para dados mais reais
                        qtd_dia = (int(qtd_hora)/60) *\
                            ((int(minutos_dia) - 48) -
                             (int(self.values["set_hora"])*60))
                        demanda = int(self.values["produzir"]) - int(qtd_dia)
                        if demanda < 0:
                            demanda = 'Demanda Atingida'
                            fim_producao = 'Concluído no mesmo dia'
                        else:
                            fim_producao = fc.calculate_production(
                                self.values["dia"],
                                hora,
                                self.values["produzir"],
                                qtd_hora,
                                set_horas,
                                self.values['extra'],
                                self.values['noturno'])
                        sg.cprint(
                            f'Material:'
                            f'{fc.get_material_name(self.values["material"])}')
                        sg.cprint(f'Qtd. Hora: {qtd_hora} Unidades')
                        sg.cprint(
                            f'Qtd. Aproximada 1º dia: {int(qtd_dia)} Unidades')
                        sg.cprint(f'Demanda prox. Dias: {demanda}')
                        sg.cprint(f'Acabará em(Estimativa): {fim_producao}')
                elif event == '24 Horas':
                    set_horas = f'{self.values["set_hora"]}:'\
                        f'{self.values["set_min"]}:00'
                    hora = f'{self.values["horas"]}:'\
                        f'{self.values["minutos"]}:00'
                    qtd_hora = fc.get_qty_hour(
                        self.values["material"].strip(),
                        self.values["linha"].strip()
                    )
                    fim_producao = fc.calculate_production_in_24_hours(
                        self.values.get('dia'),
                        hora,
                        self.values.get('produzir'),
                        qtd_hora,
                        set_horas
                    )
                    sg.cprint(
                        f'Material:'
                        f'{fc.get_material_name(self.values["material"])}'
                    )
                    sg.cprint(f'Qtd. Hora: {qtd_hora} Unidades')
                    sg.cprint(f'Acabará em(Estimativa): {fim_producao}')
                elif event == 'link':
                    webbrowser.open('https://github.com/LeonardoHMS')
            except Exception:
                sg.cprint('Informações inválidas!')
                sg.popup(traceback.format_exc(), title='Erro',
                         icon=r'static/python.ico')


def main():
    program = ProgramPainel()
    program.startProgram()


if __name__ == '__main__':
    main()
