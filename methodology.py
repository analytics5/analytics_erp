import dash
import base64
import io
import itertools
import urllib
from operator import itemgetter
import decimal
import sqlalchemy
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
import psycopg2 as pg
import numpy as np
import colors_and_fonts as color
import App_sql_queries as sql
import Passwords_and_Usernames as users
import plotly as pt


dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = '3334'
port = '5432'
conn = pg.connect(dbname=dbname, host=host, user=user, password=password)  # рисоединение к базе данных

url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, dbname)
con = sqlalchemy.create_engine(url, client_encoding='utf8')
meta = sqlalchemy.MetaData(bind=con, reflect=True)


all_val_query = """SELECT "Office_Area_SQM"::real
            FROM "Existing"
            """
delivery_vol_query = """SELECT "Office_Area_SQM"::real, "Year_Built", "Quarter_Build"
            FROM "Existing"
            """

take_up_query = """SELECT "Block"::real, "Deal_Type"::text, "Owner_Occupation"::text, "Year"::text, "Quarter"::text
            FROM "Deals"
            WHERE "Block" NOT LIKE '%w/s' AND "Block" NOT LIKE '%offices'  AND "Block" NOT LIKE 'Confi'  AND "Block" NOT LIKE 'n/a'
            """

vacancy_rate_query = """SELECT "Office_Area_SQM"::real, "Vacant_SQM"::real
            FROM "Existing"
            """


with conn:
    cur = conn.cursor()

    cur.execute(all_val_query)  # выполнение SQL запроса по сухествующим объектам
    vol_data = cur.fetchall()  # данные по сделкам
    vol_df = pd.DataFrame(vol_data)  # Запись в датафрейм
    vol_df.columns = ['SQM']

    cur.execute(delivery_vol_query)  # выполнение SQL запроса по введенным объектам
    delivery_vol_data = cur.fetchall()  # данные по сделкам
    delivery_vol_df = pd.DataFrame(delivery_vol_data)  # Запись в датафрейм
    delivery_vol_df.columns = ['SQM', 'Year_Built', 'Quarter_Build']


    cur.execute(take_up_query)  # выполнение SQL запроса по купленным и арендованным
    take_up_data = cur.fetchall()  # данные по сделкам
    take_up_df = pd.DataFrame(take_up_data)  # Запись в датафрейм
    take_up_df.columns = ['Block', 'Deal_Type', 'Owner_Occupation','Year', 'Quarter']


    cur.execute(vacancy_rate_query)  # выполнение SQL запроса по введенным объектам
    vacancy_rate_data = cur.fetchall()  # данные по сделкам
    vacancy_rate_df = pd.DataFrame(vacancy_rate_data)  # Запись в датафрейм
    vacancy_rate_df.columns = ['SQM', 'Vacant_SQM']


print(vol_df)
print('Объем предлжения')
print(vol_df['SQM'].sum())




delivery_vol_data = delivery_vol_df[(delivery_vol_df['Year_Built'].isin(['2016'])) &
                                  (delivery_vol_df['Quarter_Build'].isin(['Q3']))]

delivery_vol_sum = (delivery_vol_data["SQM"].sum())
print(delivery_vol_data)
print('Объём ввода')
print(delivery_vol_sum)



take_up_data = take_up_df[(take_up_df['Deal_Type'].isin(['New occupation'])) &
                          (take_up_df['Owner_Occupation'].isin(['Y'])) &
                          (take_up_df['Year'].isin(['2017']))
                          #(take_up_df['Quarter'].isin(['Q2']))
]
take_up_sum = (take_up_data["Block"].sum())
print(take_up_data)
print('Объём арендованных площадей')
print(take_up_sum)




vacancy_rate_sum = round(((vacancy_rate_df["Vacant_SQM"].sum())/(vacancy_rate_df["SQM"].sum()))*100, 2)
print('Вакансия')
print(vacancy_rate_sum, '%')



