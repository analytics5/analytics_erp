
import psycopg2 as pg
from tkinter import ttk
import pyexcel
import os
import pandas as pd
from pandas._libs.tslibs import timedeltas
import matplotlib
from matplotlib import *
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import pandas as pd
from tkinter import messagebox


dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = 'ZpZh2rgH'

conn = pg.connect(dbname=dbname, host=host, user=user, password=password)   #рисоединение к базе данных
query = """SELECT "Property_Name", "Class"
                     FROM "Market_Share"
                     WHERE "Agency"= 'Colliers' ;"""
with conn:
    cur = conn.cursor()
    cur.execute(query)  # выполнение SQL запроса
    colnames = [column[0] for column in cur.description]
    rows1 = cur.fetchall()  # чтение данных, полученных при запросе к базе
    #rows1.insert(0,colnames)
df = pd.DataFrame(rows1)
#print(df)

query2 = """SELECT "Property_Name", "Class"
                     FROM "Market_Share"
                     WHERE "Owner"= 'O1 Properties' ;"""
with conn:
    cur = conn.cursor()
    cur.execute(query2)  # выполнение SQL запроса
    colnames = [column[0] for column in cur.description]
    rows2 = cur.fetchall()  # чтение данных, полученных при запросе к базе
#print(rows2)


query3 = """SELECT "Agency", "Class", "Property_Name", "SQM"::real, "Year"
            FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' """   #"SQM" ~ E'^\\d+$' AND   #AND "SQM"::numeric


query4 = """SELECT "Property_Name", "SQM", "Year", "Quarter" 
            FROM "Market_Share"
            WHERE "SQM" LIKE '%w/s'"""
with conn:
    cur = conn.cursor()
    cur.execute(query4)  # выполнение SQL запроса
    colnames = [column[0] for column in cur.description]
    rows3 = cur.fetchall()  # чтение данных, полученных при запросе к базе
    #rows3.insert(0,colnames)
    df3 = pd.DataFrame(rows3)
    df3.columns = [colnames]

print(df3)



#query5 = """SELECT "Agency","City", "Property_Name", "SQM"::real, "Year", "Quarter"
            #FROM "Market_Share"
            #WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Agency" LIKE 'KF' AND "City" LIKE 'Moscow' AND "SQM" IN
            #(SELECT "SQM" FROM "Market_Share" GROUP BY "SQM" HAVING count(*)>0)"""  #LIKE (SELECT `column` FROM `table` GROUP BY `column` HAVING count(*)>1);


#with conn:
    #cur = conn.cursor()
    #cur.execute(query5)  # выполнение SQL запроса
    #colnames = [column[0] for column in cur.description]
    #rows3 = cur.fetchall()  # чтение данных, полученных при запросе к базе
    #rows3.insert(0,colnames)
    #df5 = pd.DataFrame(rows3)
    #df5.columns = [colnames]

#print(df5)


df1 = pd.read_excel('C:\\Users\\Public\\Перспектиные города.xlsx')
df1.plot(x='SAL', y='Sec', style='o')
plt.show()
