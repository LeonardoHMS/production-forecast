import os
from datetime import datetime, timedelta

import pandas as pd

DAYS = os.environ.get('DAYS')
PRODUCTION_LINE = os.environ.get('PRODUCTION_LINE')

HORAS = []
for hour in range(24):
    if hour < 10:
        hourN = f'0{hour}'
        HORAS.append(int(hourN))
    else:
        HORAS.append(hour)

MINUTOS = []
for minute in range(60):
    if minute < 10:
        minuteN = f'0{minute}'
        MINUTOS.append(int(minuteN))
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


def calcularDias(dia, hora, total, qtd_hora, setup, extra, periodo):
    horarios_diurno = [11, 35, 17, 28, 48, 90, 822]
    horarios_noturno = [22, 0, 2, 48, 20, 60, 880]
    if periodo:
        horarios = horarios_noturno
    else:
        horarios = horarios_diurno
    Total = int(total)
    qtd_min = qtd_hora/60
    setup = setup.split(':')
    set_horas = int(timedelta(hours=int(setup[0]), minutes=int(
        setup[1]), seconds=int(setup[2])).seconds / 60)
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
        if data.hour == horarios[0] and data.minute == horarios[1]:
            # Acrescenta 48 para correção, tempo de parada
            data += timedelta(minutes=horarios[5]+horarios[4])
            print(data)
        if extra:
            if data.hour == 19 and data.minute > 28:
                data += timedelta(minutes=702)
        else:
            if data.hour == horarios[2] and data.minute > horarios[3]:
                data += timedelta(minutes=horarios[6])
    while Total > 0:
        Total -= qtd_min
        data += timedelta(minutes=1)
        if data.hour == horarios[0] and data.minute == horarios[1]:
            # Acrescenta 48 para correção, tempo de parada
            data += timedelta(minutes=horarios[5]+horarios[4])
        if extra:
            if data.hour == 19 and data.minute > 28:
                data += timedelta(minutes=702)
        else:
            if data.hour == horarios[2] and data.minute > horarios[3]:
                data += timedelta(minutes=horarios[6])
        indice_semana = data.weekday()
        dia_semana = DAYS[indice_semana]
        if dia_semana == 'Sábado':
            data += timedelta(days=2)
        if dia_semana == 'Domingo':
            data += timedelta(days=1)
    return data.strftime(f'{dia_semana}, %d-%m-%Y as %H:%M:%S')


if __name__ == '__main__':
    ...
