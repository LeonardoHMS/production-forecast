import pandas as pd
from datetime import datetime, timedelta

def loadingDataBase():
    dataframe = pd.read_excel(r'C:\Users\Leonardo Mantovani\Documents\Github\production-forecast\database\database.xlsx')
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


def calcularDias(inicio, codigo, total, setup, linha):
    dias = cont = horas = 0
    Total = int(total)
    inicio = inicio.replace(' ', '-')
    inicio = inicio.replace(':', '-')
    inicio = inicio.split('-')
    tempo_prd = datetime(day=int(inicio[0]), month=int(inicio[1]), year=int(inicio[2]), hour=int(inicio[3]), minute=int(inicio[4]), second=int(inicio[5]))
    qtd_hora = qtdHora(codigo, linha)
    one_day = qtd_hora * (8 - int(setup))
    while Total >0:
        Total -= qtd_hora
        horas += 1
        cont += 1
        if Total > 0:
            if horas == 8:
                dias += 1
                horas = 0
    tempo_prd += timedelta(days=dias, hours=horas)
    return tempo_prd


if __name__ == '__main__':
    dias = calcularDias('09-05-2022 07:10:00', '30000161', '1200', '7', 'A1')
    print(dias)