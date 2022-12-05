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

print(os.environ['DB_USERNAME'])

conn = psycopg2.connect(
        host=os.environ['DB_ADDRESS'],
        database="fragment",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations

ton_auctions = 'https://tonapi.io/v1/auction/getCurrent?tld=t.me'
response = requests.get(ton_auctions)
data_json = json.loads(response.text)

for item in data_json['data']:
    if(int(item['bids']) > 1):
        print(item['domain'],item['date'],item['bids'],item['price'])
# print(data_json)


utc=pytz.UTC

app = Flask(__name__,template_folder='./')

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    cur = conn.cursor()

    cur.execute('INSERT INTO public.auction('+
	'username, id)'+
	'VALUES (%s, %s)',('ali',10))

    conn.commit()

    cur.close()

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
atexit.register(lambda: conn.close())


class fragment:
    def __init__(self, id, price, time,time_to_end):
        self.id = id
        self.price = price
        self.time = time
        self.time_to_end = time_to_end
    def url(self):
        return "https://fragment.com/username/"+re.sub(",","",self.id)
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



@app.route('/')
def index():
    response = requests.get("https://fragment.com/?filter=auction")

    today = utc.localize(datetime.utcnow())


    soup = BeautifulSoup(response.text,"html.parser")

    print(soup)

    table = soup.find_all('table',attrs={'class':'table tm-table tm-table-fixed'})

    print(table)

    trs = table[0].find_all('tr')

    fragments = []

    for tr in trs:
            ids = tr.find_all('div',attrs={'class':'table-cell-value tm-value'})
            price = tr.find_all('div',attrs={'class':'icon-ton'})
            time = tr.find_all('time')

            if(len(ids) != 0):
                    # print(ids[0].text,price[0].text,time[0]['datetime'])

                    # datetime_object = datetime.strptime(time[0]['datetime'], '%y-%m-%dT%H:%M:%S%z')
                    datetime_object = dt.parse(time[0]['datetime'])
                    delta =  relativedelta(datetime_object, today)
                    print(ids[0].text,delta.days,delta.hours,delta.minutes,delta.seconds)
                    print(datetime_object)


                    price = price[0].text
                    fragments.append(fragment(ids[0].text,int(re.sub(",","",price)),time[0]['datetime'],str(delta.days)+
                    'd'+str(delta.hours)+'h'+str(delta.minutes)+'m'+str(delta.seconds)+'s'))
    # print(table)

    fragments.sort(key=lambda x: x.time, reverse=False)

    for item in fragments:
        print(item.id,item.price,item.time,item.time_to_end)

    print(len(fragments))

    print(response)
    print("OK")
    print(today)
    # return  Response(json.dumps(fragments, default=vars),  mimetype='application/json')
    try:
        return render_template('index.html', fragments=fragments)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

