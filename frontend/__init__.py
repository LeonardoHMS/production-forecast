import traceback
import webbrowser

import PySimpleGUI as sg

import functions


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
                sg.Combo(functions.PRODUCTION_LINE, key='linha'),
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
                sg.Combo(functions.HOURS, key='set_hora', default_value='00'),
                sg.Combo(functions.MINUTOS, key='set_min', default_value='00'),
                sg.Text('Data início'),
                sg.Input(key='dia', size=SIZE_INPUT),
                sg.CalendarButton(
                    'Calendário', format='%d-%m-%Y',
                    month_names=functions.MONTHS,
                    day_abbreviations=functions.ACRON_DAYS,
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
                sg.Text(f'{"Hora início":>29}'),
                sg.Combo(functions.HOURS, key='horas', default_value='07'),
                sg.Text(':'),
                sg.Combo(functions.MINUTOS, key='minutos', default_value='10'),
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
            'Tempo de produção - v1.5', icon='static/work.ico').layout(layout)
        sg.cprint_set_output_destination(
            multiline_key='__OUTPUT__', window=self.window)

    def startProgram(self):
        while True:
            event, self.values = self.window.Read()
            if event == sg.WIN_CLOSED:
                break
            try:
                if event == 'Confirmar':
                    set_horas = f'{self.values["set_hora"]}:{self.values["set_min"]}:00'
                    hora = f'{self.values["horas"]}:{self.values["minutos"]}:00'
                    qtd_hora = functions.qtdHora(
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
                        qtd_dia = (qtd_hora/60) * ((minutos_dia - 48) -
                                                   (int(self.values["set_hora"])*60))
                        demanda = int(self.values["produzir"]) - int(qtd_dia)
                        if demanda < 0:
                            demanda = 'Demanda Atingida'
                            fim_producao = 'Concluído no mesmo dia'
                        else:
                            fim_producao = functions.calcularDias(
                                self.values["dia"],
                                hora,
                                self.values["produzir"],
                                qtd_hora,
                                set_horas,
                                self.values['extra'],
                                self.values['noturno'])
                        sg.cprint(
                            f'Material: {functions.nomeMaterial(self.values["material"].strip())}')
                        sg.cprint(f'Qtd. Hora: {qtd_hora} Unidades')
                        sg.cprint(
                            f'Qtd. Aproximada 1º dia: {int(qtd_dia)} Unidades')
                        sg.cprint(f'Demanda prox. Dias: {int(demanda)}')
                        sg.cprint(f'Acabará em(Estimativa): {fim_producao}')
                elif event == 'link':
                    webbrowser.open('https://github.com/LeonardoHMS')
            except Exception:
                sg.cprint('Informações inválidas!')
                sg.popup(traceback.format_exc(), title='Erro',
                         icon=r'static/work.ico')


def main():
    program = ProgramPainel()
    program.startProgram()


if __name__ == '__main__':
    main()
