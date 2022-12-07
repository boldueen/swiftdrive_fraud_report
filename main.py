from loguru import logger

from settings import chmod_to_geckodriver, RECIPIENT_EMAILS

from downloader import download_orders_file

from reporter import create_report_from_orders

from gshetts import set_df_to_gsheet

from mailer import send_fraud_report_on_mail

import datetime



if __name__ == "__main__":
    
    today_date = datetime.date.today()
    start_date = str(today_date - datetime.timedelta(days=14))
    today_date = str(today_date)

    logger.info("application started...")
    chmod_to_geckodriver('./utils/geckodriver')

    orders_filepath = download_orders_file(start_date, today_date)
    fraud_rides = create_report_from_orders(orders_filepath)
    url = set_df_to_gsheet(fraud_rides)  
    
    for recipient_email in RECIPIENT_EMAILS:
        send_fraud_report_on_mail(recipient_email, url)

    


    # TODO correct create report

