import pandas as pd
import numpy as np
import datetime

from settings import time_to_wait
from settings import day_down_spread_limit, day_up_spread_limit
from settings import night_down_spread_limit, night_up_spread_limit 



def is_in_day(hour: int):
    if 6 < hour < 22:
        return True
    return False


def create_report_from_orders(orders_filepath: str):
    df = pd.read_excel(orders_filepath)

    # delete summary row
    df = df[:-1]



    # rename needed columns
    df.rename({
        'Статус':'state',
        'Расстояние':'distance',
        'Время выполнения':'drive_time',
        'Стоимость':'ride_cost',
        'Платное ожидание':'waiting_time',
        'Телефон':'phone',
        'Дата начала следования':'start_ride_date',
        'Время начала следования':'start_ride_time',
        'Дата завершения':'end_ride_date',
        'Время завершения':'end_ride_time',
        'Дата прибытия автомобиля':'car_come_date',
        'Время прибытия автомобиля':'car_come_time',
        'Прибыль (руб)':'profit',
        'Маржа (%)': 'margin',
        'Стоимость':'cost',
        'Платное ожидание':'payed_wait',
        'Время выполнения':'execute_time_delete'

        }, axis=1, inplace=True)

    df = df.astype({
        'phone': str,
        'profit': int,
        'margin': int,



        })

    
    df.phone = df.phone.str.replace('.0', '')



    # select only completed rides

    correct_rides_df = df[df.state == 'Заказ завершен успешно']


    correct_rides_df['start_ride_datetime'] = correct_rides_df.start_ride_date +  ' ' + correct_rides_df.start_ride_time
    correct_rides_df['start_ride_datetime'] = pd.to_datetime(
        correct_rides_df['start_ride_datetime'], format='%d.%m.%Y %H:%M:%S'
        )

    correct_rides_df['end_ride_datetime']=correct_rides_df.end_ride_date + ' ' + correct_rides_df.end_ride_time
    correct_rides_df['end_ride_datetime'] = pd.to_datetime(
        correct_rides_df['end_ride_datetime'], format='%d.%m.%Y %H:%M:%S'
    )


    correct_rides_df['car_come_datetime']=correct_rides_df.car_come_date + ' ' + correct_rides_df.car_come_time
    correct_rides_df['car_come_datetime'] = pd.to_datetime(
        correct_rides_df['car_come_datetime'], format='%d.%m.%Y %H:%M:%S'
    )

    # calculate car wait time and convert to minutes

    correct_rides_df['correct_wait_time'] = correct_rides_df['start_ride_datetime']-correct_rides_df['car_come_datetime']
    correct_rides_df['correct_wait_time'] = correct_rides_df['correct_wait_time'] / pd.Timedelta(minutes=1)


    # calculate correct ride time and convert to minutes

    correct_rides_df['correct_time_ride']=correct_rides_df['end_ride_datetime']-correct_rides_df['start_ride_datetime']
    correct_rides_df.correct_time_ride = correct_rides_df.correct_time_ride / pd.Timedelta(minutes=1)
    

    correct_rides_df['avg_speed'] = correct_rides_df.distance / (correct_rides_df.correct_time_ride/60)


    # get avg speed for all rides

    avg_speed_total = correct_rides_df.avg_speed.mean()
    
    correct_rides_df['is_day'] = correct_rides_df.apply(lambda row: is_in_day(row.start_ride_datetime.hour), axis=1)

    fraud_avg_speed_df = correct_rides_df[
        (
            (correct_rides_df.is_day==True) & 
            (
                (correct_rides_df.avg_speed > avg_speed_total+day_up_spread_limit)|(correct_rides_df.avg_speed < avg_speed_total-day_down_spread_limit)
            )
        )

        |

        (
            (correct_rides_df.is_day==False) & 
            (
                (correct_rides_df.avg_speed > avg_speed_total+night_up_spread_limit)|(correct_rides_df.avg_speed < avg_speed_total-night_down_spread_limit)
            )
        )
    ]
    fraud_avg_speed_df['fraud_type'] = 'средняя скорость'

    fraud_big_wait_time_df = correct_rides_df[correct_rides_df.correct_wait_time > time_to_wait]
    fraud_big_wait_time_df['fraud_type'] = 'время ожидания'
   
    nan_info_fraud_df = correct_rides_df[
        (correct_rides_df.avg_speed.isna()) 
        & 
        (correct_rides_df.distance.isna())
        &
        (correct_rides_df.correct_wait_time.isna())
        ]
    nan_info_fraud_df['fraud_type'] = 'Недостаточно данных'

    frauds = [fraud_avg_speed_df, fraud_big_wait_time_df, nan_info_fraud_df]

    all_fraud_df = pd.concat(frauds)
    all_fraud_df = all_fraud_df.fillna(0)

    all_fraud_df.avg_speed = all_fraud_df.avg_speed.astype(int)
    all_fraud_df.correct_time_ride = all_fraud_df.correct_time_ride.astype(int)
    all_fraud_df.correct_wait_time = all_fraud_df.correct_wait_time.astype(int)
    all_fraud_df.payed_wait = all_fraud_df.payed_wait.astype(int)
    all_fraud_df.distance = all_fraud_df.distance.astype(int)
    all_fraud_df.cost = all_fraud_df.cost.astype(int)




    





    # set column names as it was
    all_fraud_df.rename({
        'state':'Статус',
        'distance':'Расстояние',
        'drive_time':'Время выполнения',
        'ride_cost':'Стоимость',
        'waiting_time':'Платное ожидание',
        'phone':'Телефон',
        'start_ride_date':'Дата начала следования',
        'start_ride_time':'Время начала следования',
        'end_ride_date':'Дата завершения',
        'end_ride_time':'Время завершения',
        'car_come_date':'Дата прибытия автомобиля',
        'car_come_time':'Время прибытия автомобиля',
        'correct_time_ride':'Время в пути мин',
        'avg_speed':'Средняя скорость км/ч',
        'correct_wait_time':'Общее время ожидания мин',
        'fraud_type':'Тип Фрода',
        'profit':'Прибыль руб',
        'margin': 'Маржа (%)',
        'cost':'Стоимость'


    }, axis=1, inplace=True)


    all_fraud_df.drop(columns=[
        'is_day', 
        'start_ride_datetime',
        'end_ride_datetime',
        'car_come_datetime',
        'Код сотрудника',
        'Код филиала',
        'Код затрат (номер проекта)',
        'Вид поездки',
        'CC name',
        'Центры затрат',
        'Комментарий',
        'Юр Лицо',
        'Цель поездки',
        'Номер рабочего рейса',
        'Дата рабочего рейса',
        'Тип  рабочего рейса',
        'Пункт отправления рабочего рейса',
        'Пункт прибытия рабочего рейса',
        'Тип ВС рабочего рейса',
        'Тип экипажа',
        'Комментарии для  отдела командировок',
        'ДУЭиИ',
        'Цель поездок',
        'Case Code',
        'Цель  поездки',
        'Дата (рейс?)',
        'КЦ тип строка',
        'Название проекта',
        'КЦ тип дата',
        'Номер проекта',
        'Номер сделки/проекта',
        'поле тип дата 78',
        'Цель поездки (тип строка) 78',
        'Развоз сотрудников в ночное время',
        'execute_time_delete'
        ],  inplace=True)

    




    return all_fraud_df
        


