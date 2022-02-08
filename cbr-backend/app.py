import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__)

metrics = PrometheusMetrics(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('database_url')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class cbr(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    ValuteID = db.Column(db.String(16))
    NumCode = db.Column(db.Numeric(8))
    CharCode = db.Column(db.String(8))
    Nominal = db.Column(db.Integer())
    Name = db.Column(db.String(300))
    Value = db.Column(db.Float(12,4))
    db.UniqueConstraint(date, ValuteID)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def parse(url):

    response = requests.get(url)

    inserts = []

    myroot = ET.fromstring(response.content)

    for valute in myroot.findall('Valute'):
       insert = {}
       cont = 0
       for element in valute.iter():
           if list(element) == []:
              insert[element.tag] = element.text
              insert['ValuteID'] = valute.attrib['ID']
              insert['Date'] = datetime.strptime(myroot.attrib['Date'], "%d.%m.%Y").strftime('%Y-%m-%d')
              element.text=element.text.replace(",",".")
              cont = 1
       if cont:
          inserts.append(insert)
    return inserts

def mysql(url):
   import os
   import mysql.connector
   connection = mysql.connector.connect(user=os.getenv('mysql_user'),
   password = os.getenv('mysql_password'),
   host=os.getenv('mysql_host'),
   database=os.getenv('mysql_db'))

   values = [list(x.values()) for x in parse(url)]

   columns = [list(x.keys()) for x in parse(url)][0]

   values_str = ""

   for i, record in enumerate(values):

       val_list = []
       for v, val in enumerate(record):
           if type(val) == str:
               val = "'{}'".format(val.replace(",", "."))
           val_list += [ str(val) ]

       values_str += "(" + ', '.join( val_list ) + "),\n"
   values_str = values_str[:-2] + ";"
   table_name = "cbr"
   sql_string = "INSERT IGNORE INTO %s (%s)\nVALUES\n%s" % (
       table_name,
       ', '.join(columns),
       values_str
   )
   with connection.cursor() as cursor:
       cursor.execute(sql_string)
       connection.commit()

def refresh():

 for i in range(1, datetime.today().day + 1):
     i = ('{:02d}'.format(i))
     now = datetime.now()
     url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req='+str(i)+'/'+now.strftime("%m")+'/'+now.strftime("%Y")
     mysql(url)


@app.route('/api/refresh', methods=['GET'])
def get_tasks():
    refresh()
    return "ok"
