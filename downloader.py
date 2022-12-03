from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions, FirefoxProfile
from selenium.webdriver.firefox.options import Options

from settings import PASSWORD, DOWNLOAD_PATH, LOGIN, FILEPATH, PWD
import time
import os
import glob

from loguru import logger



def download_orders_file(start_date:str, end_date:str) -> str:
    """
    start_date example: '2022-03-23'
    return filepath to downloaded file
    """
    opts = FirefoxOptions()
    opts.add_argument("--headless")


    opts.set_preference("browser.download.folderList", 2)
    opts.set_preference("browser.download.manager.showWhenStarting", False)
    opts.set_preference("browser.download.dir", DOWNLOAD_PATH)
    opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")


    old_list_of_files = glob.glob(f'{DOWNLOAD_PATH}*.xlsx') # * means all if need specific format then *.csv
    # driver = webdriver.Firefox(executable_path = './utils/geckodriver', options=opts, firefox_profile=profile)
    driver = webdriver.Firefox(executable_path = './utils/geckodriver', options=opts)

    driver.get('https://swiftdrive.ru/auth/signin')

    logger.info("start auth")
    time.sleep(5)

    email = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div/div[2]/form/fieldset/div[1]/div/div/input")

    password = driver.find_element(By.XPATH,
                                    "/html/body/div/div/div[1]/div/div/div[2]/form/fieldset/div[2]/div/div/input")

    email.send_keys(LOGIN)
    password.send_keys(PASSWORD)

    button = driver.find_element(By.XPATH, '//*[@id="app-site"]/div/div[1]/div/div/div[2]/form/fieldset/div[3]/button')
    button.click()

    logger.info("auth complete")


    
    driver.get('https://swiftdrive.ru/app/reports')
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[contains(text(), "Диапазон")]').click()


    time.sleep(1)
    start_date_webelement = driver.find_element(
        By.XPATH, 
        '//*[@id="body"]/div[2]/div[3]/div/div[2]/div[1]/div/div/input')
    start_date_webelement.send_keys(start_date)

    end_date_webelement = driver.find_element(By.XPATH, '//*[@id="body"]/div[2]/div[3]/div/div[2]/div[2]/div/div/input')
    end_date_webelement.send_keys(end_date)

    driver.find_element(By.XPATH, '//*[contains(text(), "Применить")]').click()


    driver.find_element(By.XPATH, '//*[contains(text(), "Экспорт")]').click()
    driver.find_element(By.XPATH, '//*[contains(text(), "Экспортировать")]').click()


    new_list_of_files = glob.glob(f'{DOWNLOAD_PATH}*.xlsx') # * means all if need specific format then *.csv
    


    while len(old_list_of_files) == len(new_list_of_files):
        new_list_of_files = glob.glob(f'{DOWNLOAD_PATH}*.xlsx')
        


    new_file = (set(new_list_of_files) - set(old_list_of_files)).pop()

    logger.info("file downloaded")

    time.sleep(1)

    driver.quit()
    
    return new_file


def delete_file(path: str = FILEPATH) -> bool:
    try:
        os.remove(path)
    except:
        pass
    if os.path.isfile(path):
        return False
    return True