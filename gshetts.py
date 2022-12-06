import pygsheets
import pandas as pd

from settings import G_SETTINGS_FILEPATH

def set_df_to_gsheet(data: pd.DataFrame):
    service_file = G_SETTINGS_FILEPATH
    gs = pygsheets.authorize(service_file=service_file)
    sh = gs.open('swift_fraud')
    g_worksheet = sh.worksheet_by_title('rides')

    exist_sheet = g_worksheet.get_as_df(include_tailing_empty=False)
    start_row = len(exist_sheet) + 2

    g_worksheet.set_dataframe(data, (start_row ,1), extend=True)
    