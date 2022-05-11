import pandas as pd
from datetime import datetime, timedelta


DIAS = [
    'Segunda-feira',
    'Terça-Feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]


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


def calcularDias(inicio, qtd_hora, total, qtd_dia, setup=0):
    dias = cont = 0
    Total = int(total)
    inicio = inicio.replace(' ', '-')
    inicio = inicio.replace(':', '-')
    inicio = inicio.split('-')
    data = datetime(day=int(inicio[0]), month=int(inicio[1]), year=int(inicio[2]), hour=int(inicio[3]), minute=int(inicio[4]), second=int(inicio[5]))
    while Total > 0:
        Total -= int(qtd_dia)
        if cont != 0:
            dias += 1
        cont += 1
    data += timedelta(days=dias)
    indice_semana = data.weekday()
    dia_semana = DIAS[indice_semana]
    if str(dia_semana) == 'Sábado':
        data += timedelta(days=2)
    elif str(dia_semana) == 'Domingo':
        data += timedelta(days=1)
    indice_semana = data.weekday()
    dia_semana = DIAS[indice_semana]
    return data.strftime(f'{dia_semana}, %d-%m-%Y')


if __name__ == '__main__':
    dias = calcularDias('10-05-2022 07:10:00', 63, '2000', '504')
    print(dias)