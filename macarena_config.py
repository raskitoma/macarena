#############################################
# Macarena - DB
# (c)2022, Raskitoma.com
#--------------------------------------------
# Master DB utility functions for bot
#-------------------------------------------- 
# TODO
#-------------------------------------------- 
import os, sys
import requests
import json
import pandas as pd
import configparser
from datetime import datetime
import time
from flask import Flask
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tqdm import tqdm

if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS".
    APPLICATION_PATH = sys._MEIPASS # pylint: disable=no-member
else:
    APPLICATION_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = APPLICATION_PATH + '/csv/'

global config, my_wallets, null_wallet, my_api_key

config = configparser.ConfigParser()
config.read(APPLICATION_PATH + "/settings.ini")
null_wallet = "0x0000000000000000000000000000000000000000"
try:
    my_wallets = config["GENERAL"]["my_wallets"].split(",")
except:
    print("No wallets configured")
    sys.exit(1)
try:
    my_api_key = config["GENERAL"]["etherscan_api"]
except:
    print("No API key configured")
    sys.exit(1)
try:
    DATABASE_CONN = config["GENERAL"]["DATABASE_URI"]
except:
    DATABASE_CONN = 'sqlite:///' + os.path.join(DATA_FOLDER, 'macarena.db')

# Create the application instance
app = Flask(__name__)
# Extra configs to secure app
app.config['SECRET_KEY'] = 'b012345678901234567890123456789a'
# csrf = CSRFProtect()
# csrf.init_app(app)
# Setting app upload folder
app.config['UPLOAD_FOLDER'] = DATA_FOLDER
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setting Database Connection URI
app.config['SQLALCHEMY_DATABASE_URI'] =  DATABASE_CONN

# Some usefull functions
def get_timestamp():
    '''
    Just a simple function to retrieve a formatted timestamp.
    '''
    return datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))

def dump_datetime(value):
    '''
    Deserialize datetime object into string form for JSON processing
    '''
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")

# request year and month
def get_year_month():
    year = input("Enter year (Enter null for all history): ")
    # if year is empty, return None
    if year == "":
        return None
    # if year is not a number, and has a length of 4, ask again
    elif not year.isdigit() and len(year) == 4:
        print("Year must be a 4 digit number")
        return get_year_month()
    # get month until it has 2 digits and is a number
    month = input("Enter month: ")
    while not month.isdigit() or len(month) != 2:
        print("Month must be a number with 2 digits")
        month = input("Enter month: ")
    return year, month

# clear screen
def clear_screen():
    '''
    Clears the screen
        Parameters: None
        Returns: None
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

# delete previous csv files in csv folder
def delete_csv_files():
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            os.remove(DATA_FOLDER + file)

def selenium_create_browser():
    '''
    Creates a selenium browser object using gecko driver
        Parameters: None
        Returns: selenium browser object (object)
    '''
    pseudodisplay = None
    # Setting virtual display, if needed
    try:
        pseudodisplay = Display(visible=0, size=(2560, 1440))
        pseudodisplay.start()
    except Exception as e:
        print ('Virtual display not initialized: {}'.format(e))
        pass
    # Setting up Firefox/gecko
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('browser.download.folderList', 2)
    firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
    firefox_profile.set_preference('browser.download.dir', DATA_FOLDER)
    firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')
#    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference("http.response.timeout", 5)
    firefox_profile.set_preference("dom.max_script_run_time", 5)
    firefox_profile.update_preferences()
    # creating Selenium browser object
    browser = webdriver.Firefox(firefox_profile=firefox_profile)
    return browser

#############################################
# EoF    
