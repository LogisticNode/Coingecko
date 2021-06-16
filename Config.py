#DataBase
import sqlite3
from DataBase import Sqlighter

db = Sqlighter('DataBase.db')

#Requests
from bs4 import BeautifulSoup
from lxml import html
import requests
import fake_useragent
import random

#Data
url = 'https://www.coingecko.com/account/sign_in?locale=ru'
candy_url = 'https://www.coingecko.com/account/candy/daily_check_in?locale=ru'
id = 1

#Beautiful
import datetime
import time