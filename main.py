from loguru import logger

from settings import chmod_to_geckodriver

from downloader import download_orders_file

from reporter import create_report_from_orders

from gshetts import set_df_to_gsheet



if __name__ == "__main__":
    logger.info("application started...")
    if chmod_to_geckodriver('./utils/geckodriver'):
        logger.info("chmod +x for geckodriver")

    # orders_filepath = download_orders_file('2022-10-10', '2022-10-15')
    # print(orders_filepath)
    fraud_rides = create_report_from_orders('downloads/4010d385-41ba-4eb6-a73e-9639e9b3b2ee.xlsx')
    # print(fraud_rides.info())

    set_df_to_gsheet(fraud_rides)    



    # TODO create report
    # TODO import report to google sheets
    # TODO send gooogke_sheet link to emails


    # TODO download orders file - done
