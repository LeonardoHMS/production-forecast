from datetime import datetime, timedelta

import pandas as pd

from .parameters import DAYS

HOURS = []
for hour in range(24):
    if hour < 10:
        hourN = f'0{hour}'
        HOURS.append(int(hourN))
    else:
        HOURS.append(hour)

MINUTES = []
for minute in range(60):
    if minute < 10:
        minuteN = f'0{minute}'
        MINUTES.append(int(minuteN))
    else:
        MINUTES.append(minute)


def load_dataBase():
    dataframe = pd.read_excel(r'database\database.xlsx')
    return dataframe


def get_material_name(material_id):
    material_id = int(material_id)
    dataframe = load_dataBase()
    dataframe = dataframe.set_index('codigo')
    material = dataframe.loc[material_id, 'nome_material']
    return material


def get_qty_hour(material_id, linha):
    material_id = int(material_id)
    dataframe = load_dataBase()
    dataframe = dataframe.set_index('codigo')
    hour = dataframe.loc[material_id, linha]
    return hour


def calculate_production(day, hours, total, qty_hours, setup, extra, period):
    daytime_hours = [11, 35, 17, 28, 48, 90, 822]
    night_hours = [22, 0, 2, 48, 20, 60, 880]
    if period:
        schedules = night_hours
    else:
        schedules = daytime_hours
    total = int(total)
    qty_min = qty_hours/60
    setup = setup.split(':')
    set_hours = int(timedelta(hours=int(setup[0]), minutes=int(
        setup[1]), seconds=int(setup[2])).seconds / 60)
    day = day.split('-')
    hours = hours.split(':')
    data = datetime(
        day=int(day[0]),
        month=int(day[1]),
        year=int(day[2]),
        hour=int(hours[0]),
        minute=int(hours[1]),
        second=int(hours[2])
    )
    while set_hours > 0:
        data += timedelta(minutes=1)
        set_hours -= 1
        if data.hour == schedules[0] and data.minute == schedules[1]:
            # Acrescenta 48 para correção, tempo de parada
            data += timedelta(minutes=schedules[5]+schedules[4])
            print(data)
        if extra:
            if data.hour == 19 and data.minute > 28:
                data += timedelta(minutes=702)
        else:
            if data.hour == schedules[2] and data.minute > schedules[3]:
                data += timedelta(minutes=schedules[6])
    while total > 0:
        total -= qty_min
        data += timedelta(minutes=1)
        if data.hour == schedules[0] and data.minute == schedules[1]:
            # Acrescenta 48 para correção, tempo de parada
            data += timedelta(minutes=schedules[5]+schedules[4])
        if extra:
            if data.hour == 19 and data.minute > 28:
                data += timedelta(minutes=702)
        else:
            if data.hour == schedules[2] and data.minute > schedules[3]:
                data += timedelta(minutes=schedules[6])
        week_index = data.weekday()
        dia_semana = DAYS[week_index]
        if dia_semana == 'Sábado':
            data += timedelta(days=2)
        if dia_semana == 'Domingo':
            data += timedelta(days=1)
    return data.strftime(f'{dia_semana}, %d-%m-%Y as %H:%M:%S')


def calculate_production_in_24_hours(day, hours, total, qty_hours, setup):
    total = int(total)
    qty_min = qty_hours/60
    setup = setup.split(':')
    set_hours = int(timedelta(hours=int(setup[0]), minutes=int(
        setup[1]), seconds=int(setup[2])).seconds / 60)
    day = day.split('-')
    hours = hours.split(':')
    data = datetime(
        day=int(day[0]),
        month=int(day[1]),
        year=int(day[2]),
        hour=int(hours[0]),
        minute=int(hours[1]),
        second=int(hours[2])
    )

    while set_hours > 0:
        data += timedelta(minutes=1)
        set_hours -= 1

    while total > 0:
        total -= qty_min
        data += timedelta(minutes=1)
        week_index = data.weekday()
        dia_semana = DAYS[week_index]
        if dia_semana == 'Sábado' and data.hour == 6:
            data += timedelta(hours=48)
    return data.strftime(f'{dia_semana}, %d-%m-%Y as %H:%M:%S')


if __name__ == '__main__':
    ...
