import os
import stat
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")

DOWNLOAD_PATH  = os.environ.get("PWD") + os.environ.get("DOWNLOAD_PATH")
FILEPATH = os.environ.get("PWD") + os.environ.get("DOWNLOAD_PATH") + os.environ.get("FILENAME")

MAIL_EMAIL=os.environ.get("MAIL_EMAIL")
MAIL_PASS=os.environ.get("MAIL_PASS")

PWD = os.environ.get("PWD")
HOME = os.environ.get("HOME")

G_SETTINGS_FILEPATH = 'google_sheet_settings.json'

RECIPIENT_EMAILS = []


# fraud analyze variables
time_to_wait = 30

day_down_spread_limit = 30
day_up_spread_limit = 45

night_down_spread_limit = 30
night_up_spread_limit = 50



def chmod_to_geckodriver(geckodriver_filepath) -> bool:
    try:
        st = os.stat(geckodriver_filepath)
        os.chmod(geckodriver_filepath, st.st_mode | stat.S_IEXEC)
        return True
    except:
        return False