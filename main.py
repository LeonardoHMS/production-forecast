import PySimpleGUI as sg
import functions
import webbrowser

lista = ['A1','A2','A3','A4','A5','M1','M2','M3']

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
                sg.Combo(lista, key='linha'),
                sg.Text(f'{"By: Leonardo Mantovani":>35}',enable_events=True, key= 'link', text_color=('red'), tooltip='acessar')
            ],
            [sg.Text('Qtd P/ Produzir'), sg.Input(key='produzir', size=SIZE_INPUT)],
            [   
                sg.Text('Setup'),
                sg.Input(key='setup', size=SIZE_INPUT), 
                sg.Text('Data início'), 
                sg.Input(key='inicio', size=SIZE_INPUT), 
                sg.CalendarButton('Calendário', format='%d-%m-%Y %H:%M:%S')
            ],
            [sg.Button('Confirmar')],
            [sg.Multiline(size=(50,15), key='__OUTPUT__', font=FONT_STR, do_not_clear=False)]
        ]
        # Window
        self.window = sg.Window('Previsão de produção v0.1').layout(layout)
        sg.cprint_set_output_destination(multiline_key='__OUTPUT__', window=self.window)

    def startProgram(self):
        while True:
            event, self.values = self.window.Read()
            if event == sg.WIN_CLOSED:
                break
            try:
                if event == 'Confirmar':
                    if functions.qtdHora(self.values["material"].strip(), self.values["linha"].strip()) == 'NP':
                        sg.cprint('Material não é produzido nesta linha!')
                    else:
                        if self.values['setup'] == '':
                            self.values['setup'] = '0'
                        qtd_hora = functions.qtdHora(self.values["material"].strip(),
                                                    self.values["linha"].strip())
                        qtd_dia = qtd_hora * (8 - int(self.values["setup"]))
                        demanda = int(self.values["produzir"]) - qtd_dia
                        if demanda < 0:
                            demanda = 'Demanda Atingida'
                        fim_producao = functions.calcularDias(
                            self.values["inicio"], 
                            self.values["material"].strip(),
                            self.values["produzir"], 
                            self.values["setup"],
                            self.values["linha"])
                        sg.cprint(f'Material: {functions.nomeMaterial(self.values["material"].strip())}')
                        sg.cprint(f'Qtd. Hora: {qtd_hora} Minutos')
                        sg.cprint(f'Qtd. Dia: {qtd_dia} Minutos')
                        sg.cprint(f'Demanda prox. Dias: {demanda}')
                        sg.cprint(f'Acabará em(Estimativa): {fim_producao}')
                        sg.cprint('\n\n\n\n\n -- Tempo aproximado --')
                elif event == 'link':
                    webbrowser.open('https://github.com/LeonardoHMS')
            except:
                sg.cprint('Informações inválidas!')


def main():
    program = ProgramPainel()
    program.startProgram()

if __name__ == '__main__':
    main()