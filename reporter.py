import pandas as pd


def create_report_from_orders(orders_filepath: str):
    df = pd.read_excel(orders_filepath)

    df.rename({
        'Расстояние':'distance',
        'Время выполнения':'drive_time',
        'Стоимость':'ride_cost',
        'Платное ожидание':'waiting_time',
        'Телефон':'phone'
        }, axis=1, inplace=True)

    df = df.astype({'phone': str})
    df.info()
    time_to_wait = 20

    day_down_spread_limit = 35
    day_up_spread_limit = 40

    night_down_spread_limit = 30
    night_up_spread_limit = 50




    # correct_rides_df = df[df['Статус'] == 'Заказ завершен успешно']
    correct_rides_df = df


    correct_rides_df['avg_speed'] = correct_rides_df.distance / (correct_rides_df.drive_time*60)
    correct_rides_df = correct_rides_df[correct_rides_df.avg_speed > 0]
    correct_rides_df.info()
    correct_rides_df.head(5)
    
    

    # test = df[df['Стоимость'] > 2000]

    return correct_rides_df
        


