import pandas as pd
from datetime import datetime, timedelta

LINHA = ['A1','A2','A3','A4','A5','M1','M2','M3']

DIAS = [
    'Segunda-feira',
    'Terça-Feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]

ABV_DIAS = [
    'Dom',
    'Seg',
    'Ter',
    'Qua',
    'Qui',
    'Sex',
    'Sab'
]

MES = [
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
]

HORAS = []
for hour in range(24):
    if hour < 10:
        hourN = f'0{hour}'
        HORAS.append(hourN)
    else:
        HORAS.append(hour)

MINUTOS = []
for minute in range(60):
    if minute < 10:
        minuteN = f'0{minute}'
        MINUTOS.append(minuteN)
    else:
        MINUTOS.append(minute)


def loadingDataBase():
    dataframe = pd.read_excel(r'database\database.xlsx')
    return dataframe


def nomeMaterial(codigo):
    codigo = int(codigo)
    dataframe = loadingDataBase()
    dataframe = dataframe.set_index('codigo')
    material = dataframe.loc[codigo, 'nome_material']
    return material


def qtdHora(codigo, linha):
    codigo = int(codigo)
    dataframe = loadingDataBase()
    dataframe = dataframe.set_index('codigo')
    hora = dataframe.loc[codigo, linha]
    return hora


def calcularDias(dia, hora, total, qtd_hora, setup):
    Total = int(total)
    qtd_min = qtd_hora/60
    setup = setup.split(':')
    set_horas = int(timedelta(hours=int(setup[0]), minutes=int(setup[1]), seconds=int(setup[2])).seconds / 60)
    dia = dia.split('-')
    hora = hora.split(':')
    data = datetime(
        day=int(dia[0]),
        month=int(dia[1]),
        year=int(dia[2]),
        hour=int(hora[0]),
        minute=int(hora[1]),
        second=int(hora[2])
        )
    while set_horas > 0:
        data += timedelta(minutes=1)
        set_horas -= 1
        if data.hour == 11 and data.minute == 35:
            data += timedelta(minutes=90)
        if data.hour == 17 and data.minute > 28:
            data += timedelta(minutes=822)
    while Total > 0:
        Total -= qtd_min
        data += timedelta(minutes=1)
        if data.hour == 11 and data.minute == 35:
            data += timedelta(minutes=90)
        if data.hour == 17 and data.minute > 28:
            data += timedelta(minutes=822)
        indice_semana = data.weekday()
        dia_semana = DIAS[indice_semana]
        if dia_semana == 'Sábado':
            data += timedelta(days=2)
        if dia_semana == 'Domingo':
            data += timedelta(days=1)
    return data.strftime(f'{dia_semana}, %d-%m-%Y as %H:%M:%S')


if __name__ == '__main__':
    dias = calcularDias('12-05-2022', '07:10:00', '500', 109, '05:00:00')
    print(dias)