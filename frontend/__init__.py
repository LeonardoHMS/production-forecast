import PySimpleGUI as sg
import functions
import webbrowser


class ProgramPainel:
    def __init__(self):
        # Parameters
        FONT_STR = 'Arial, 12'
        SIZE_INPUT = (12, 1)
        sg.theme('DarkGrey')
        #Layout
        layout = [
            [
                sg.Text('Cod. Material'), 
                sg.Input(key='material', size=SIZE_INPUT), 
                sg.Text('Linha'),  
                sg.Combo(functions.LINHA, key='linha'),
                sg.Text(f'{"":^14}'),
                sg.Image('static/githublogo.png', enable_events=True, key='link', tooltip='acessar')
            ],
            [sg.Text('Qtd P/ Produzir'), sg.Input(key='produzir', size=SIZE_INPUT),
             sg.Text(f'{"By: LEONARDOHMS":>40}',enable_events=True, text_color=('black'), font='Arial, 12')
            ],
            [   
                sg.Text('Setup'),
                sg.Input(key='setup', size=SIZE_INPUT), 
                sg.Text('Data início'), 
                sg.Input(key='dia', size=SIZE_INPUT), 
                sg.CalendarButton('Calendário', format='%d-%m-%Y', month_names=functions.MES, day_abbreviations=functions.ABV_DIAS)
            ],
            [
                sg.Button('Confirmar'),
                sg.Text(f'{"Hora início":>29}'),
                sg.Combo(functions.HORAS, key='horas', default_value='07'),
                sg.Text(':'),
                sg.Combo(functions.MINUTOS, key='minutos', default_value='10')
            ],
            [sg.Multiline(size=(50,18), key='__OUTPUT__', font=FONT_STR, do_not_clear=False)],
            [sg.Text('--Tempo Aproximado--')]
        ]
        # Window
        self.window = sg.Window('Tempo de produção - v1.0', icon='static/work.ico').layout(layout)
        sg.cprint_set_output_destination(multiline_key='__OUTPUT__', window=self.window)

    def startProgram(self):
        while True:
            event, self.values = self.window.Read()
            if event == sg.WIN_CLOSED:
                break
            try:
                if event == 'Confirmar':
                    hora = f'{self.values["horas"]}:{self.values["minutos"]}:00'
                    qtd_hora = functions.qtdHora(self.values["material"].strip(),
                                self.values["linha"].strip())
                    if qtd_hora == 'NP':
                        sg.cprint('Material não é produzido nesta linha!')
                    else:
                        if self.values['setup'] == '':
                            self.values['setup'] = '0'
                        qtd_dia = qtd_hora * (8 - int(self.values["setup"]))
                        demanda = int(self.values["produzir"]) - qtd_dia
                        if demanda < 0:
                            print(demanda)
                            demanda = 'Demanda Atingida'
                            fim_producao = 'Concluído no mesmo dia'
                        else:
                            fim_producao = functions.calcularDias(
                                self.values["dia"],
                                hora,
                                self.values["produzir"],
                                qtd_hora,
                                self.values["setup"])
                        sg.cprint(f'Material: {functions.nomeMaterial(self.values["material"].strip())}')
                        sg.cprint(f'Qtd. Hora: {qtd_hora} Minutos')
                        sg.cprint(f'Qtd. Dia: {qtd_dia} Minutos')
                        sg.cprint(f'Demanda prox. Dias: {demanda}')
                        sg.cprint(f'Acabará em(Estimativa): {fim_producao}')
                elif event == 'link':
                        webbrowser.open('https://github.com/LeonardoHMS')
            except:
                sg.cprint('Informações inválidas!')


def main():
    program = ProgramPainel()
    program.startProgram()

if __name__ == '__main__':
    main()