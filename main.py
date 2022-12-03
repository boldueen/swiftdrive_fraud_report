from loguru import logger

from settings import chmod_to_geckodriver

from downloader import download_orders_file



if __name__ == "__main__":
    logger.info("application started...")
    if chmod_to_geckodriver('./utils/geckodriver'):
        logger.info("chmod +x for geckodriver")

    orders_filepath = download_orders_file('2022-01-01', '2022-01-07')
    # TODO create report
    # TODO import report to google sheets
    # TODO send gooogke_sheet link to emails


    # TODO download orders file - done
