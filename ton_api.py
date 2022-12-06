import atexit
# from urllib.request import urlopen
import json
import os
import re
import time
from datetime import date, datetime

import dateutil.parser as dt
import psycopg2
import pytz
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from flask import Flask, Response, render_template, request


def get_all_auctions():
    ton_auctions = 'https://tonapi.io/v1/auction/getCurrent?tld=t.me'
    response = requests.get(ton_auctions)
    json_response = json.loads(response.text)
    return json_response['data']
