import pandas as pd


def create_report_from_orders(orders_filepath: str):
    df = pd.read_excel(orders_filepath)


    time_to_wait = 20

    day_down_spread_limit = 35
    day_up_spread_limit = 40

    night_down_spread_limit = 30
    night_up_spread_limit = 50


    correct_rides_df = df[df['Статус'] == 'Заказ завершен успешно']


    test = df[df['Стоимость'] > 2000]
    test.info()
    return test
        


