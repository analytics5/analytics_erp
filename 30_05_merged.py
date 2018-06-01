import dash
import base64
import io
import itertools
import urllib
from operator import itemgetter
# from PIL import ImageGrab
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
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('Wittgensteen', 'bl8Z5NQ1cMli9YmLhViF')  # Replace the username, and API key with your credentials.

app = dash.Dash(__name__)
server = app.server

# auth = dash_auth.BasicAuth(app, users.VALID_USERNAME_PASSWORD_PAIRS)
app.config.suppress_callback_exceptions = True
# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})    # то, что предлагают плотли
# app.css.append_css({'external_url': 'https://raw.githubusercontent.com/Wittgensteen/work_stuff/master/base_style.css'})    # мой файл на гитхабе
app.css.append_css({
    'external_url': 'https://rawgit.com/Wittgensteen/work_stuff/master/new_buttons.css'})  # мой файл с гитхаба на rawgit

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

deals_query = sql.deals_query
tenant_rep_query = sql.tenant_rep_query
llr_query = sql.llr_query

sale_lease_query = sql.sale_lease_query
sale_lease_query_sale = sql.sale_lease_query_sale
sale_lease_query_lease = sql.sale_lease_query_lease

all_deals_query = sql.table_query_new_all  # изменено на новый запрос

suspicious_deals = sql.table_query

with conn:
    cur = conn.cursor()

    cur.execute(deals_query)  # выполнение SQL запроса по сделкам
    deals_data = cur.fetchall()  # данные по сделкам
    deals_df = pd.DataFrame(deals_data)  # Запись в датафрейм

    cur.execute(tenant_rep_query)  # выполнение SQL запроса по типу сделок TR
    tenant_data = cur.fetchall()
    tenant_df = pd.DataFrame(tenant_data)

    cur.execute(llr_query)  # выполнение SQL запроса по типу сделок LLR
    llr_data = cur.fetchall()
    llr_df = pd.DataFrame(llr_data)

    cur.execute(sale_lease_query)  # выполнение SQL запроса по типу сделок Sale/Lease
    sale_lease_data = cur.fetchall()
    sale_lease_df = pd.DataFrame(sale_lease_data)

    cur.execute(sale_lease_query_sale)  # выполнение SQL запроса по типу сделок Sale/Lease по sale
    sale_lease_sale_data = cur.fetchall()
    sale_lease_sale_df = pd.DataFrame(sale_lease_sale_data)

    cur.execute(sale_lease_query_lease)  # выполнение SQL запроса по типу сделок Sale/Lease по lease
    sale_lease_lease_data = cur.fetchall()
    sale_lease_lease_df = pd.DataFrame(sale_lease_lease_data)

    cur.execute(all_deals_query)
    all_deals_query_data = cur.fetchall()
    all_deals_query_df = pd.DataFrame(all_deals_query_data)

    cur.execute(suspicious_deals)  # выполнение SQL запроса по сделкам
    suspicious_deals_data = cur.fetchall()  # данные по сделкам
    suspicious_deals_df = pd.DataFrame(suspicious_deals_data)  # Запись в датафрейм

    deals_df.columns = ['Agency', 'SQM', 'Year']
    tenant_df.columns = ['Agency', 'SQM', 'Year']
    llr_df.columns = ['Agency', 'SQM', 'Year']
    sale_lease_df.columns = ['Agency', 'SQM', 'Year', 'Type_of_deal']
    sale_lease_lease_df.columns = ['Agency', 'SQM', 'Year', 'Type_of_deal']
    sale_lease_sale_df.columns = ['Agency', 'SQM', 'Year', 'Type_of_deal']

    all_deals_query_df.columns = ["Include_in_Market_Share", "Agency", "Country", "City", "Property_Name", "Address",
                                  "Submarket_Large", "Owner", "Date_of_acquiring", "Class", "Class_Colliers",
                                  "Floor", "SQM", "Deal_Size", "Company", "Business_Sector", "Sublease_Agent",
                                  "Type_of_deal", "Type_of_Consultancy", "LLR_TR", "LLR_Only", "E_TR_Only",
                                  "LLR/E_TR", "Month", "Year", "Quarter"]
    all_deals_query_df["LLR_Only"] = all_deals_query_df["LLR_Only"].replace({True: 'Yes', False: 'No'})
    all_deals_query_df["E_TR_Only"] = all_deals_query_df["E_TR_Only"].replace({True: 'Yes', False: 'No'})
    all_deals_query_df["LLR/E_TR"] = all_deals_query_df["LLR/E_TR"].replace({True: 'Yes', False: 'No'})

    suspicious_deals_df.columns = ['Agency', 'Country', 'City', 'Property Name', 'Class', 'SQM', 'Company',
                                   'Type_of_Consultancy', 'Year', 'Quarter']

country = ("All countries", "Russia", "Ukraine", "Belarus", "Kazakhstan ", "Azerbaijan")
country_ind = ("All countries", "RU", "UA", "BY", "KZ", "AZ")
years = ("All years", "2013", "2014", "2015", "2016", "2017", "2018")
Agency = ("All agency", "Colliers", "KF", "JLL", "CW", "SAR", "CBRE")
Agency_tab = ("Colliers", "KF", "JLL", "CW", "SAR", "CBRE")
list_of_columns = ["Include_in_Market_Share", "Agency", "Country", "City", "Property_Name", "Address",
                   "Submarket_Large", "Owner", "Date_of_acquiring", "Class", "Class_Colliers",
                   "Floor", "SQM", "Deal_Size", "Company", "Business_Sector", "Sublease_Agent",
                   "Type_of_deal", "Type_of_Consultancy", "LLR_TR", "LLR_Only", "E_TR_Only",
                   "LLR/E_TR", "Month", "Year", "Quarter"]

list_of_columns_for_gui = ["Include in market share", "Agency", "Country", "City", "Property name", "Address",
                           "Submarket_Large", "Owner", "Date of acquiring", "Class", "Class Colliers",
                           "Floor", "SQM", "Size of deal", "Company", "Business sector", "Sublease agent",
                           "Type of deal", "Type of consultancy", "LLR/TR", "LLR only", "(E)TR only",
                           "LLR/(E)TR", "Month", "Year", "Quarter"]

to_main_page_button = html.A(html.Button('Вернуться на главную', className='button-primary',
                                         style={
                                             'display': 'inline',
                                             'height': '38px',
                                             'padding': '0 15px',
                                             # 'color': '#FFF',
                                             #  'text-align': 'center',
                                             #  'font-size': '11px',
                                             #  'font-weight': '600',
                                             #  'line-height': '38px',
                                             #  'letter-spacing': '.1rem',
                                             #  'text-transform': 'uppercase',
                                             #  'text-decoration': 'none',
                                             #  'white-space': 'nowrap',
                                             #  'background-color': '#33C3F0',
                                             #  'border-radius': '4px',
                                             'border': '1px solid #ffc425',
                                             #  'cursor': 'pointer',
                                             #  'box-sizing': 'border-box'
                                         }
                                         ), href='/main'
                             )

# '''
#     Начало основного блока приложения
#
#                                          '''

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}
                 ),

    ],
    # style={'backgroundColor': color.colliers_dark_blue}
)

# РАЗМЕТКА СТРАНИЦЫ 'MAIN'

index_page = html.Div([
    html.Div([
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            children="Office Market Share",
                            className='row',
                            style={'textAlign': 'center',
                                   'font-size': '16px',
                                   'margin': '20 0 0 15px',
                                   'color': color.colliers_grey_10,
                                   'display': 'inline-block',
                                   }
                        )
                    ],
                    style={'textAlign': 'left',
                           'margin': '0 0 0 10px',
                           'display': 'inline',
                           }
                ),

                html.A(html.Button('About Project',
                                   # className='button-primary',
                                   style={
                                       'display': 'inline-block',
                                       'float': 'right',
                                       'height': '40px',
                                       'padding': '0 0 10 5px',
                                       'color': '#FFF',
                                       'text-align': 'center',
                                       'font-size': '14px',
                                       'font-weight': '500',
                                       'line-height': '38px',
                                       'letter-spacing': '.001rem',
                                       'text-transform': 'uppercase',
                                       'text-decoration': 'none',
                                       'white-space': 'nowrap',
                                       'background-color': color.colliers_light_blue_20,
                                       'border-radius': '0px',
                                       'border': '1px solid #bbb',
                                       'cursor': 'pointer',
                                       'box-sizing': 'border-box'
                                   }
                                   ),
                       # className='row',
                       href='/page-about'),

                html.A(html.Button('Help',
                                   # className='button-primary',
                                   style={
                                       'display': 'inline-block',
                                       'float': 'right',
                                       'height': '40px',
                                       'padding': '5 15px',
                                       'color': '#FFF',
                                       'text-align': 'center',
                                       'font-size': '14px',
                                       'font-weight': '500',
                                       'line-height': '38px',
                                       'letter-spacing': '.001rem',
                                       'text-transform': 'uppercase',
                                       'text-decoration': 'none',
                                       'white-space': 'nowrap',
                                       'background-color': color.colliers_light_blue_20,
                                       'border-radius': '0px',
                                       'border': '1px solid #bbb',
                                       'cursor': 'pointer',
                                       'box-sizing': 'border-box'
                                   }
                                   ),
                       # className='row',
                       href='/page-help')
            ],
            # style={'display': 'inline-block'},
        ),
    ],
        className='banner',
        style={'backgroundColor': color.colliers_dark_blue,
               }
    ),

    html.Div(
        [
            html.Div(
                [
                    html.A(html.Button('База по сделкам',
                                       className='button-primary',
                                       style={
                                           # 'display': 'inline',
                                           'height': '38px',
                                           'width': '100%',
                                           'padding': '0 0 0 12px',
                                           'color': color.colliers_light_blue,
                                           'text-align': 'left',
                                           'font-size': '14px',
                                           'font-weight': '300',
                                           'line-height': '20px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'none',
                                           # 'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           # 'background-color': 'transparent',
                                           'border-radius': '0px',
                                           'border': '0px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           href='/page-4'),

                    html.A(html.Button('Обновить базу по сделкам',
                                       className='button-primary',
                                       style={
                                           # 'display': 'inline',
                                           'height': '38px',
                                           'width': '100%',
                                           'padding': '0 0 0 12px',
                                           'color': color.colliers_light_blue,
                                           'text-align': 'left',
                                           'font-size': '14px',
                                           'font-weight': '300',
                                           'line-height': '20px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'none',
                                           # 'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           # 'background-color': 'transparent',
                                           'border-radius': '0px',
                                           'border': '0px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           href='/page-5')
                ],
                className='two columns',
                style={'backgroundColor': color.colliers_pale_blue,  # цвет фона за блоком с ссылками
                       #'width': '15%',
                       # 'margin': '20 0 100 0px',
                       'height': '1080px'
                       }
            ),

        ],
    ),
],
    style={'backgroundColor': color.colliers_pale_blue}
)

# РАЗМЕТКА СТРАНИЦЫ 'HELP'

page_help_layout = html.Div([

    html.Div([
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            children="Руководство пользователя",
                            className='row',
                            style={'textAlign': 'center',
                                   # 'margin': '80 0 20 80px',
                                   'color': color.colliers_grey_10,
                                   'display': 'inline-block',
                                   }
                        )
                    ], style={'textAlign': 'left',
                              'margin': '0 0 0 25px',
                              'display': 'inline',
                              }
                ),

                html.A(html.Button('About Project',
                                   className='button-primary',
                                   style={
                                       'display': 'inline-block',
                                       'float': 'right',
                                       'height': '46px',
                                       'padding': '5 15px',
                                       'color': '#FFF',
                                       'text-align': 'center',
                                       'font-size': '14px',
                                       'font-weight': '500',
                                       'line-height': '38px',
                                       'letter-spacing': '.001rem',
                                       'text-transform': 'uppercase',
                                       'text-decoration': 'none',
                                       'white-space': 'nowrap',
                                       'background-color': color.colliers_light_blue_20,
                                       'border-radius': '0px',
                                       'border': '1px solid #bbb',
                                       'cursor': 'pointer',
                                       'box-sizing': 'border-box'
                                   }
                                   ),
                       # className='row',
                       href='/page-about'),

                html.A(html.Button('To main page',
                                   className='button-primary',
                                   style={
                                       'display': 'inline-block',
                                       'float': 'right',
                                       'height': '46px',
                                       'padding': '5 15px',
                                       'color': '#FFF',
                                       'text-align': 'center',
                                       'font-size': '14px',
                                       'font-weight': '500',
                                       'line-height': '38px',
                                       'letter-spacing': '.001rem',
                                       'text-transform': 'uppercase',
                                       'text-decoration': 'none',
                                       'white-space': 'nowrap',
                                       'background-color': color.colliers_light_blue_20,
                                       'border-radius': '0px',
                                       'border': '1px solid #bbb',
                                       'cursor': 'pointer',
                                       'box-sizing': 'border-box'
                                   }
                                   ),
                       # className='row',
                       href='/main')
            ],
            # style={'display': 'inline-block'},
        )
    ],
        className='banner',
        style={'backgroundColor': color.colliers_dark_blue,
               }
    ),

    dcc.Markdown('''
#### Справка по обновлению базы данных по сделкам
* Для обновления базы необходимо переместить мастер-файл формата ".csv" в поле "Drag and drop" или
  нажать на ссылку "Select Files" и выбрать мастер-файл из его текущей директории.
* Правила оформления мастер-файла:
  * Скачать шаблон файла, нажав на кнопку "Скачать шаблон"
  * При оформлении заполнения столбцов желательно избегать использования кириллицы
  * Ячейки со значением "SQM" желательно приводить к числовому формату
  * Для разделения дробной части использовать знак "." (точка), а не "," (запятая)
  * Столбец "Floor" желательно приводить к числовому формату
                                '''),
],
    style={'backgroundColor': color.colliers_pale_blue,
           'height': '340px'
           }
)

# РАЗМЕТКА СТРАНИЦЫ 'ABOUT PROJECT'

page_about_layout = html.Div([

    html.Div([
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            children="Информация о проекте",
                            className='row',
                            style={'textAlign': 'center',
                                   # 'margin': '80 0 20 80px',
                                   'color': color.colliers_grey_10,
                                   'display': 'inline-block',
                                   }
                        )
                    ],
                    style={'textAlign': 'left',
                           'margin': '0 0 0 25px',
                           'display': 'inline',
                           }

                ),
                html.A(html.Button('Help',
                                   className='button-primary',
                                   style={
                                       'display': 'inline-block',
                                       'float': 'right',
                                       'height': '46px',
                                       'padding': '5 15px',
                                       'color': '#FFF',
                                       'text-align': 'center',
                                       'font-size': '14px',
                                       'font-weight': '500',
                                       'line-height': '38px',
                                       'letter-spacing': '.001rem',
                                       'text-transform': 'uppercase',
                                       'text-decoration': 'none',
                                       'white-space': 'nowrap',
                                       'background-color': color.colliers_light_blue_20,
                                       'border-radius': '0px',
                                       'border': '1px solid #bbb',
                                       'cursor': 'pointer',
                                       'box-sizing': 'border-box'
                                   }
                                   ),
                       # className='row',
                       href='/page-help'),

                html.A(html.Button('To main page',
                                   className='button-primary',
                                   style={
                                       'display': 'inline-block',
                                       'float': 'right',
                                       'height': '46px',
                                       'padding': '5 15px',
                                       'color': '#FFF',
                                       'text-align': 'center',
                                       'font-size': '14px',
                                       'font-weight': '500',
                                       'line-height': '38px',
                                       'letter-spacing': '.001rem',
                                       'text-transform': 'uppercase',
                                       'text-decoration': 'none',
                                       'white-space': 'nowrap',
                                       'background-color': color.colliers_light_blue_20,
                                       'border-radius': '0px',
                                       'border': '1px solid #bbb',
                                       'cursor': 'pointer',
                                       'box-sizing': 'border-box'
                                   }
                                   ),
                       # className='row',
                       href='/main')
            ],
            # style={'display': 'inline-block'},
        )
    ],
        className='banner',
        style={'backgroundColor': color.colliers_dark_blue,
               }
    ),

    dcc.Markdown('''
###### Здесь будет информация о модуле
  * С ссылками на источники данных
  * И с текстом лицензии, так принято, почему-то
    ''')
],
    style={'backgroundColor': color.colliers_pale_blue,
           'height': '170px'
           }
)

# РАЗМЕТКА СТРАНИЦЫ 'БАЗА ПО СДЕЛКАМ'


page_4_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Checklist(
                            id='tree-checklist',
                            options=[
                                {'label': 'Columns', 'value': 'Show'}
                            ],
                            values=[],
                            labelStyle={'display': 'block',
                                        'width': '192px'
                                        }
                        )
                    ],
                    style={
                        'display': 'inline'
                    }
                ),

                html.Div(
                    [
                        dcc.Checklist(
                            id='interface',
                            options=[{'label': i, 'value': j} for i, j in
                                     zip(list_of_columns_for_gui, list_of_columns)],
                            values=['Agency', 'Country', 'City', 'Property_Name', 'Class', 'SQM', "Company",
                                    "Business_Sector",
                                    'Type_of_deal', 'Type_of_Consultancy', 'LLR_TR', 'Year', 'Quarter'],
                            labelStyle={
                                'display': 'none',
                                'padding-left:': '90px'
                            }
                        )
                    ],
                    style={
                        'display': 'inline',

                    }
                ),

            ],
            className='one column',
            style={'backgroundColor': color.colliers_pale_blue,  # цвет фона за блоком с ссылками
                   'width': '192px',
                   # 'margin': '20 0 100 0px',
                   'max-height': '200vh',
                   'min-height': '200vh',
                   # 'position': 'absolute',
                   'display': 'block',
                   }
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.A(html.Button('Показать все сделки',
                                                   className='button-primary',
                                                   style={
                                                       'display': 'inline',
                                                       'float': 'right',
                                                       'height': '46px',
                                                       'padding': '5 15px',
                                                       'color': '#FFF',
                                                       'text-align': 'center',
                                                       'font-size': '14px',
                                                       'font-weight': '500',
                                                       'line-height': '38px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'uppercase',
                                                       'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       'background-color': color.colliers_light_blue_20,
                                                       'border-radius': '0px',
                                                       'border': '1px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-4'
                                       ),
                                html.A(html.Button('Показать сомнительные сделки',
                                                   className='button-primary',
                                                   style={
                                                       'display': 'inline',
                                                       'float': 'right',
                                                       'height': '46px',
                                                       'padding': '5 15px',
                                                       'color': '#FFF',
                                                       'text-align': 'center',
                                                       'font-size': '14px',
                                                       'font-weight': '500',
                                                       'line-height': '38px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'uppercase',
                                                       'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       'background-color': color.colliers_light_blue_20,
                                                       'border-radius': '0px',
                                                       'border': '1px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/suspicious_deals'),
                            ]
                        ),
                        html.H5(children="Все сделки",
                                className='row',
                                style={'textAlign': 'center', 'color': color.colliers_grey_80
                                       }
                                ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Agency",
                                            # value='All agency',
                                            placeholder="Агентство",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in Agency_tab
                                            ],
                                        )
                                    ],
                                    id='Agency_Div',
                                    style={
                                        'width': '7.69%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'inline-block',
                                        # 'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Country",
                                            # value='All countries',
                                            placeholder="Страна",
                                            multi=True,
                                            options=[{
                                                'label': j,
                                                'value': j
                                            }
                                                for j in country_ind
                                            ],
                                        )
                                    ],
                                    id='Country_Div',
                                    style={
                                        'width': '7.69%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="City",
                                            # value='All agency',
                                            placeholder="Город",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["City"].unique()
                                            ],

                                        )],
                                    id='City_Div',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Property_name",
                                            # value='All agency',
                                            placeholder="Объект",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Property_Name"].unique()
                                            ],

                                        )],
                                    # className='one columns',
                                    id='Property_name_Div',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Class",
                                            # value='All agency',
                                            placeholder="Класс",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Class"].unique()
                                            ],

                                        )],
                                    id='Class_Div',

                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="SQM",
                                            # value='All agency',
                                            placeholder="Площадь",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["SQM"].unique()
                                            ],

                                        )],
                                    # className='one columns',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Company",
                                            # value='All agency',
                                            placeholder="Компания",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Company"].unique()
                                            ],

                                        )],
                                    id='Company_Div',

                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Business_Sector",
                                            # value='',
                                            placeholder="Сектор",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Business_Sector"].unique()
                                            ],

                                        )],
                                    id='Business_Sector_Div',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Type_of_Deal",
                                            # value='All agency',
                                            placeholder="Тип сделки",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Type_of_deal"].unique()
                                            ],

                                        )],
                                    id='Type_of_Deal_Div',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Type_of_Consultancy",
                                            # value='All agency',
                                            placeholder="Тип услуг",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Type_of_Consultancy"].unique()
                                            ],

                                        )],
                                    id='Type_of_Consultancy_Div',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="LLR/TR",
                                            # value='All agency',
                                            placeholder="LLR/TR",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["LLR_TR"].unique()
                                            ],

                                        )],
                                    id='LLR/TR_Div',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Year",
                                            multi=True,
                                            # value='All years',
                                            placeholder="Год",
                                            value=None,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in years
                                            ],
                                        )
                                    ],
                                    id='Year_Div',
                                    style={
                                        'width': '7.69%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'inline-block',
                                        # 'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Quarter",
                                            # value='All agency',
                                            placeholder="Квартал",

                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Quarter"].unique()
                                            ],

                                        )],
                                    id='Quarter',
                                    style={
                                        'width': '7.69%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Include_in_M_S",
                                            # value='All agency',
                                            placeholder="В Market Share",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Include_in_Market_Share"].unique()

                                            ],
                                        )
                                    ],
                                    id='Include_in_M_S_Div',
                                    style={
                                        'width': '7.69%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'none',
                                        # 'float': 'right'
                                    }
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Address",
                                            # value='All agency',
                                            placeholder="Адрес",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Address"].unique()

                                            ],
                                        )
                                    ],
                                    id='Address_Div',
                                    style={
                                        'width': '7.69%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'none',
                                        # 'float': 'right'
                                    }
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Submarket_Large",
                                            # value='All agency',
                                            placeholder="Субрынок",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Submarket_Large"].unique()

                                            ],
                                        )
                                    ],
                                    id='Submarket_Large_Div',
                                    style={
                                        'width': '7.69%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'none',
                                        # 'float': 'right'
                                    }
                                ),

                            ],
                            id='drop_testing',
                            className='row'
                        ),

                        html.Div(
                            [
                                dt.DataTable(
                                    rows=[{}],  # initialise the row
                                    editable=False,
                                    row_selectable=False,
                                    filterable=True,
                                    sortable=True,
                                    selected_row_indices=[],
                                    # filters=[list_of_columns],
                                    max_rows_in_viewport=10,
                                    min_height=600,
                                    resizable=True,
                                    id='datatable'
                                )
                            ]
                        ),
                        html.Div(id='sum',
                                 style={'color': color.colliers_grey_10,
                                        'background-color': color.colliers_dark_blue,
                                        'fontSize': 14,
                                        'border': 'solid 1px black',
                                        }
                                 ),
                        html.Div([
                            html.A(
                                'Download All Data',
                                id='download-all-link',
                                download="all_data.csv",
                                href="",
                                target="_blank",
                            ),
                        ],
                            style={'background-color': color.colliers_dark_blue}
                        ),
                        html.Div([
                            html.A(
                                'Download Selected Data',
                                id='download-selected-link',
                                download="selected_data.csv",
                                href="",
                                target="_blank",
                            )
                        ],
                            style={'background-color': color.colliers_dark_blue}
                        ),

                        html.Br(),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='market-graph-tab'),
                                        dcc.Graph(id='market-graph-non-stack-tab'),
                                        dcc.Graph(id='market-graph-horizontal-tab'),
                                    ],
                                    className='six columns',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(id='market-pie-graph-tab'),
                                        dcc.Graph(id='market-graph-percent-tab'),
                                        dcc.Graph(id='market-graph-horizontal-total-tab')
                                    ],
                                    className='six columns  ',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                )
                            ],
                            # className='ten columns',
                        )
                    ],
                    className='row',
                )
            ],
            className='ten columns',

        )

    ],
    style={'backgroundColor': color.colliers_grey_10},

)


# style = {'backgroundColor': color.colliers_pale_blue}
# )
#


@app.callback(dash.dependencies.Output('interface', 'labelStyle'),
              # здесь на вход пинимается значение чеклиста 'colums', если значение выбрано, то отрисовывается новый блок со списком,как в дереве
              [dash.dependencies.Input('tree-checklist', 'values')
               ])
def show_tree(val):
    print('значение кнопки дерева')
    print(val)
    if 'Show' in val:
        print(val)
        print('Вход в функцию')
        children = {'display': 'block',
                    'width': '192px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children


@app.callback(dash.dependencies.Output('datatable', 'rows'),                    # здесь на вход пинимается значение значение выпадающих списков и на основе этих значение формируется dataframe, поещаемый в таблицу
              [dash.dependencies.Input('Year', 'value'),
               dash.dependencies.Input('Country', 'value'),
               dash.dependencies.Input('Agency', 'value'),
               dash.dependencies.Input('City', 'value'),
               dash.dependencies.Input('Property_name', 'value'),
               dash.dependencies.Input('Class', 'value'),
               dash.dependencies.Input('SQM', 'value'),
               dash.dependencies.Input('Business_Sector', 'value'),
               dash.dependencies.Input('Type_of_Deal', 'value'),
               dash.dependencies.Input('Type_of_Consultancy', 'value'),
               dash.dependencies.Input('LLR/TR', 'value'),
               dash.dependencies.Input('Quarter', 'value'),
               dash.dependencies.Input('Company', 'value'),
               dash.dependencies.Input('interface', 'values')
               ])
def update_datatable(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, LLR_TR, Quarter, Company, val):
    print('значение чеклиста', val)
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_name=[Property_name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter])
    # print('New iteration')
    # print(all_deals_query_df["Type_of_Consultancy"].unique())
    list_of_values = (
        Year, Country, Agency, City, Property_name, Class, SQM, Company, Business_Sector, Type_of_Deal,
        Type_of_Consultancy, LLR_TR,
        Quarter)
    cond_1 = cond.copy()
    # print(cond_1.values())
    list_of_values_copy = list(filter(None, list_of_values))
    # print(len(list_of_values_copy))

    if len(list_of_values_copy) == 0 or (Year is not None and Year[0] == 'All years'):
        print(list_of_values_copy, 'первое условие')
        all_deals_query_df[val]
        return all_deals_query_df[val].to_dict('records')
    # ____________________________________________________________#

    if len(list_of_values_copy) == 1:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind = get_key(cond_1, list_of_values_copy)
        print(ind, list_of_values_copy[0], 'второе условие')
        data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[0]))]
        return data.to_dict('records')
    # _________________________________________________________________#

    if len(list_of_values_copy) == 2:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])

        print(ind_0)
        print(ind_1)

        print(list_of_values_copy[0], 'третье условие')

        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1]))]
        return data.to_dict('records')

    # __________________________________________________________________________#

    if len(list_of_values_copy) == 3:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])

        print(list_of_values_copy[0], 'четвертое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2]))]
        return data.to_dict('records')
    # _______________________________________________#
    if len(list_of_values_copy) == 4:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])

        print(list_of_values_copy[0], 'пятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3]))]
        return data.to_dict('records')

    # ____________________________
    if len(list_of_values_copy) == 5:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])

        print(list_of_values_copy[0], 'шестое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4]))]
        return data.to_dict('records')

    # _________________________________________________________________#

    if len(list_of_values_copy) == 6:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])

        print(list_of_values_copy[0], 'седьмое услови сумма')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5]))]
        return data.to_dict('records')

    # ______________________________________________________________________#

    if len(list_of_values_copy) == 7:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])

        print(list_of_values_copy[0], 'восьмое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6]))]
        return data.to_dict('records')

    # _________________________________________________________________

    if len(list_of_values_copy) == 8:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])

        print(list_of_values_copy[0], 'девятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7]))]
        return data.to_dict('records')

    # ________________________________________________________________________________________

    if len(list_of_values_copy) == 9:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8]))]
        return data.to_dict('records')

    # _____________________________________________________________--#

    if len(list_of_values_copy) == 10:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])

        print(list_of_values_copy[0], 'одинадцатое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9]))]
        return data.to_dict('records')

    # _____________________________________________________________--#

    if len(list_of_values_copy) == 11:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])

        print(list_of_values_copy[0], 'двенадцатое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9])) &
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10]))]
        return data.to_dict('records')

    # _____________________________________________________________--#

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])

        print(list_of_values_copy[0], 'тринадцатое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9])) &
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10])) &
                                  (all_deals_query_df[ind_11].isin(list_of_values_copy[11]))]
        return data.to_dict('records')

    if len(list_of_values_copy) == 13:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        ind_12 = get_key(cond_1, [list_of_values_copy[12]])

        print(list_of_values_copy[0], 'тринадцатое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9])) &
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10])) &
                                  (all_deals_query_df[ind_11].isin(list_of_values_copy[11])) &
                                  (all_deals_query_df[ind_12].isin(list_of_values_copy[12]))]
        return data.to_dict('records')


# _________________________________________#   добавление дропдаунов

@app.callback(dash.dependencies.Output('Include_in_M_S_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_include(val):
    # print('значение для отрисовки списка', val)
    try:
        if 'Include_in_Market_Share' in val:
            style_include = {'display': 'inline-block',
                             'width': '7.69%'
                             }

        if 'Include_in_Market_Share' not in val:
            style_include = {'display': 'none',
                             'width': '7.69%'
                             }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_include


@app.callback(dash.dependencies.Output('Agency_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_agency(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Agency' in val:
            style_agency = {'display': 'inline-block',
                            'width': '7.69%'
                            }

        if 'Agency' not in val:
            style_agency = {'display': 'none',
                            'width': '7.69%'
                            }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_agency


@app.callback(dash.dependencies.Output('Country_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_country(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Country' in val:
            style_country = {'display': 'inline-block',
                             'width': '7.69%'
                             }

        if 'Country' not in val:
            style_country = {'display': 'none',
                             'width': '7.69%'
                             }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_country


@app.callback(dash.dependencies.Output('City_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_city(val):
    print('значение для отрисовки списка', val)
    try:
        if 'City' in val:
            style_city = {'display': 'inline-block',
                          'width': '7.69%'
                          }

        if 'City' not in val:
            style_city = {'display': 'none',
                          'width': '7.69%'
                          }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_city


@app.callback(dash.dependencies.Output('Property_name_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_property_name(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Property_name' in val:
            style_property_name = {'display': 'inline-block',
                                   'width': '7.69%'
                                   }

        if 'Property_name' not in val:
            style_property_name = {'display': 'none',
                                   'width': '7.69%'
                                   }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_property_name


@app.callback(dash.dependencies.Output('Class_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_class(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Class' in val:
            style_class = {'display': 'inline-block',
                           'width': '7.69%'
                           }

        if 'Class' not in val:
            style_class = {'display': 'none',
                           'width': '7.69%'
                           }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_class


@app.callback(dash.dependencies.Output('SQM_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_SQM(val):
    print('значение для отрисовки списка', val)
    try:
        if 'SQM' in val:
            style_SQM = {'display': 'inline-block',
                         'width': '7.69%'
                         }

        if 'SQM' not in val:
            style_SQM = {'display': 'none',
                         'width': '7.69%'
                         }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_SQM


@app.callback(dash.dependencies.Output('Company_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Company(val):
    print('значение для отрисовки списка', val)
    try:
        if 'SQM' in val:
            style_Company = {'display': 'inline-block',
                             'width': '7.69%'
                             }

        if 'SQM' not in val:
            style_Company = {'display': 'none',
                             'width': '7.69%'
                             }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Company


@app.callback(dash.dependencies.Output('Business_Sector_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Business_Sector(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Business_Sector' in val:
            style_Business_Sector = {'display': 'inline-block',
                                     'width': '7.69%'
                                     }

        if 'Business_Sector' not in val:
            style_Business_Sector = {'display': 'none',
                                     'width': '7.69%'
                                     }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Business_Sector


@app.callback(dash.dependencies.Output('Type_of_Deal_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Type_of_Deal(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Type_of_deal' in val:
            style_Type_of_Deal = {'display': 'inline-block',
                                  'width': '7.69%'
                                  }

        if 'Type_of_deal' not in val:
            style_Type_of_Deal = {'display': 'none',
                                  'width': '7.69%'
                                  }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Type_of_Deal


@app.callback(dash.dependencies.Output('Type_of_Consultancy_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Type_of_Consultancy(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Type_of_Consultancy' in val:
            style_Type_of_Consultancy = {'display': 'inline-block',
                                         'width': '7.69%'
                                         }

        if 'Type_of_Consultancy' not in val:
            style_Type_of_Consultancy = {'display': 'none',
                                         'width': '7.69%'
                                         }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Type_of_Consultancy


@app.callback(dash.dependencies.Output('LLR/TR_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Type_of_Consultancy(val):
    print('значение для отрисовки списка', val)
    try:
        if 'LLR_TR' in val:
            style_LLR_TR = {'display': 'inline-block',
                            'width': '7.69%'
                            }

        if 'LLR_TR' not in val:
            style_LLR_TR = {'display': 'none',
                            'width': '7.69%'
                            }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_LLR_TR


@app.callback(dash.dependencies.Output('Year_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Year(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Year' in val:
            style_Year = {'display': 'inline-block',
                          'width': '7.69%'
                          }

        if 'Year' not in val:
            style_Year = {'display': 'none',
                          'width': '7.69%'
                          }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Year


@app.callback(dash.dependencies.Output('Quarter_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Quarter(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Quarter' in val:
            style_Quarter = {'display': 'inline-block',
                             'width': '7.69%'
                             }

        if 'Quarter' not in val:
            style_Quarter = {'display': 'none',
                             'width': '7.69%'
                             }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Quarter


@app.callback(dash.dependencies.Output('Address_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Address(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Address' in val:
            style_Addres = {'display': 'inline-block',
                             'width': '7.69%'
                             }

        if 'Address' not in val:
            style_Addres = {'display': 'none',
                             'width': '7.69%'
                             }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Addres

@app.callback(dash.dependencies.Output('Submarket_Large_Div', 'style'),
              [dash.dependencies.Input('interface', 'values')
               ])
def update_drop_Submarket_large(val):
    print('значение для отрисовки списка', val)
    try:
        if 'Submarket_Large' in val:
            style_Submarket_Large = {'display': 'inline-block',
                             'width': '7.69%'
                             }

        if 'Submarket_Large' not in val:
            style_Submarket_Large = {'display': 'none',
                             'width': '7.69%'
                             }

        # else:
        #     child = html.Div(style={'display': 'none'}),
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error'
        ])
    return style_Submarket_Large




# def add_dropdown_submarket_large(value):
#     try:
#         if 'Submarket_large' in value:
#             child_own =

# _________________________________________#


@app.callback(dash.dependencies.Output('sum', 'children'),
              [dash.dependencies.Input('Year', 'value'),
               dash.dependencies.Input('Country', 'value'),
               dash.dependencies.Input('Agency', 'value'),
               dash.dependencies.Input('City', 'value'),
               dash.dependencies.Input('Property_name', 'value'),
               dash.dependencies.Input('Class', 'value'),
               dash.dependencies.Input('SQM', 'value'),
               dash.dependencies.Input('Business_Sector', 'value'),
               dash.dependencies.Input('Type_of_Deal', 'value'),
               dash.dependencies.Input('Type_of_Consultancy', 'value'),
               dash.dependencies.Input('LLR/TR', 'value'),
               dash.dependencies.Input('Quarter', 'value'),
               dash.dependencies.Input('Company', 'value')
               ])
def update_sum(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal,
               Type_of_Consultancy, LLR_TR, Quarter, Company):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_name=[Property_name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter])
    # print('New iteration')
    list_of_values = (
        Year, Country, Agency, City, Property_name, Class, SQM, Company, Business_Sector, Type_of_Deal,
        Type_of_Consultancy, LLR_TR,
        Quarter)
    cond_1 = cond.copy()
    # print(cond_1)
    # print(cond_1.values())
    list_of_values_copy = list(filter(None, list_of_values))

    if len(list_of_values_copy) == 0 or (Year is not None and Year[0] == 'All years'):
        data_sum = int(round(all_deals_query_df["SQM"].sum()))

        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # ____________________________________________________________#

    if len(list_of_values_copy) == 1:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind = get_key(cond_1, list_of_values_copy)
        # print(list_of_values_copy[0], 'второе условие')
        data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[0]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'
        # _________________________________________________________________#

    if len(list_of_values_copy) == 2:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])

        # print(list_of_values_copy[0], 'третье условие')

        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # __________________________________________________________________________#

    if len(list_of_values_copy) == 3:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])

        # print(list_of_values_copy[0], 'четвертое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'
        # _______________________________________________#
    if len(list_of_values_copy) == 4:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])

        # print(list_of_values_copy[0], 'пятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # ____________________________
    if len(list_of_values_copy) == 5:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])

        # print(list_of_values_copy[0], 'шестое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # _________________________________________________________________#

    if len(list_of_values_copy) == 6:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])

        # print(list_of_values_copy[0], 'седьмое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # ______________________________________________________________________#

    if len(list_of_values_copy) == 7:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])

        # print(list_of_values_copy[0], 'восьмое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # _________________________________________________________________

    if len(list_of_values_copy) == 8:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])

        # print(list_of_values_copy[0], 'девятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # ________________________________________________________________________________________

    if len(list_of_values_copy) == 9:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])

        # print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

        # _____________________________________________________________--#

    if len(list_of_values_copy) == 10:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])

        # print(list_of_values_copy[0], '11 условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

    # _________________________________________________________
    if len(list_of_values_copy) == 11:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])

        # print(list_of_values_copy[0], '12 условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9]))
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

    # _________________________________________________________
    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])

        # print(list_of_values_copy[0], '13 условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9])) &
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10])) &
                                  (all_deals_query_df[ind_11].isin(list_of_values_copy[11]))]

        data_sum = int(round(data["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'


@app.callback(dash.dependencies.Output('download-all-link', 'href'),
              [dash.dependencies.Input('Year', 'value'),
               dash.dependencies.Input('Country', 'value'),
               dash.dependencies.Input('Agency', 'value'),
               dash.dependencies.Input('City', 'value'),
               dash.dependencies.Input('Property_name', 'value'),
               dash.dependencies.Input('Class', 'value'),
               dash.dependencies.Input('SQM', 'value'),
               dash.dependencies.Input('Business_Sector', 'value'),
               dash.dependencies.Input('Type_of_Deal', 'value'),
               dash.dependencies.Input('Type_of_Consultancy', 'value'),
               dash.dependencies.Input('Quarter', 'value'),
               dash.dependencies.Input('Company', 'value')
               ])
def update_download_all_link(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal,
                             Type_of_Consultancy, Quarter, Company):
    csv_string = all_deals_query_df.to_csv(index=False, encoding='utf-8', sep=';')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string


@app.callback(
    dash.dependencies.Output('download-selected-link', 'href'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Country', 'value'),
     dash.dependencies.Input('Agency', 'value'),
     dash.dependencies.Input('City', 'value'),
     dash.dependencies.Input('Property_name', 'value'),
     dash.dependencies.Input('Class', 'value'),
     dash.dependencies.Input('SQM', 'value'),
     dash.dependencies.Input('Business_Sector', 'value'),
     dash.dependencies.Input('Type_of_Deal', 'value'),
     dash.dependencies.Input('Type_of_Consultancy', 'value'),
     dash.dependencies.Input('LLR/TR', 'value'),
     dash.dependencies.Input('Quarter', 'value'),
     dash.dependencies.Input('Company', 'value')
     ])
def update_download_link(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal, LLR_TR,
                         Type_of_Consultancy, Quarter, Company):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_name=[Property_name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter])
    # print('New iteration')
    # print(Year)
    list_of_values = (
        Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal, Type_of_Consultancy,
        LLR_TR, Quarter,
        Company)
    cond_1 = cond.copy()
    # print(cond_1)
    # print(cond_1.values())
    list_of_values_copy = list(filter(None, list_of_values))

    if len(list_of_values_copy) == 0:
        # print(list_of_values_copy, 'первое условие')
        return all_deals_query_df.to_dict('records')

    # ____________________________________________________________#

    if len(list_of_values_copy) == 1:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind = get_key(cond_1, list_of_values_copy)
        # print(list_of_values_copy[0], 'второе условие')
        data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[0]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string
    # _________________________________________________________________#

    if len(list_of_values_copy) == 2:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])

        # print(list_of_values_copy[0], 'третье условие')

        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # __________________________________________________________________________#

    if len(list_of_values_copy) == 3:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])

        # print(list_of_values_copy[0], 'четвертое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string
    # _______________________________________________#
    if len(list_of_values_copy) == 4:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])

        print(list_of_values_copy[0], 'пятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # ____________________________
    if len(list_of_values_copy) == 5:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])

        print(list_of_values_copy[0], 'шестое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # _________________________________________________________________#

    if len(list_of_values_copy) == 6:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])

        print(list_of_values_copy[0], 'седьмое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # ______________________________________________________________________#

    if len(list_of_values_copy) == 7:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])

        print(list_of_values_copy[0], 'восьмое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # _________________________________________________________________

    if len(list_of_values_copy) == 8:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])

        print(list_of_values_copy[0], 'девятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # ________________________________________________________________________________________

    if len(list_of_values_copy) == 9:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # _____________________________________________________________--#

    if len(list_of_values_copy) == 10:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # _____________________________________________________________--#

    if len(list_of_values_copy) == 11:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9])) &
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    # _____________________________________________________________--#

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9])) &
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10])) &
                                  (all_deals_query_df[ind_11].isin(list_of_values_copy[11]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string
    # _____________________________________________________________--#

    if len(list_of_values_copy) == 13:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        ind_12 = get_key(cond_1, [list_of_values_copy[12]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9])) &
                                  (all_deals_query_df[ind_10].isin(list_of_values_copy[10])) &
                                  (all_deals_query_df[ind_11].isin(list_of_values_copy[11])) &
                                  (all_deals_query_df[ind_12].isin(list_of_values_copy[12]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string


# '''
#    Callback`и, отрисовывающие графики.
#    На вход принимают данные дропдаунов для таблицы, на выход - график
#                                                                        '''


# '''
#     Начало блока по отрисовке графиков
#
#                                          '''


# '''
#     График принимает те же переменные, как и таблица, сначала фильтруется датафрейм по выбранным данным,
#     после этот датафрейм переводится в сводную таблицу в pandas и по значениям сводной таблицы строится график.
#
#                                                                                                                    '''


@app.callback(
    dash.dependencies.Output('market-graph-tab', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Country', 'value'),
     dash.dependencies.Input('Agency', 'value'),
     dash.dependencies.Input('City', 'value'),
     dash.dependencies.Input('Property_name', 'value'),
     dash.dependencies.Input('Class', 'value'),
     dash.dependencies.Input('SQM', 'value'),
     dash.dependencies.Input('Business_Sector', 'value'),
     dash.dependencies.Input('Type_of_Deal', 'value'),
     dash.dependencies.Input('Type_of_Consultancy', 'value'),
     dash.dependencies.Input('LLR/TR', 'value'),
     dash.dependencies.Input('Quarter', 'value'),
     dash.dependencies.Input('Company', 'value')
     ])
def update_graph_tab(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, LLR_TR, Quarter, Company):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_name=[Property_name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter])

    list_of_values = (
        Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal, Type_of_Consultancy,
        LLR_TR,
        Quarter, Company)
    cond_1 = cond.copy()
    # print(cond_1.values())
    list_of_values_copy = list(filter(None, list_of_values))

    # print('tut grafic')
    # print(len(list_of_values_copy))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = deals_df.copy()
            format_data = 'all deals'
            format_year = 'all years'
        # print(len(list_of_values_copy))
    except TypeError:
        df_plot = deals_df.copy()
    except IndexError:
        df_plot = deals_df.copy()

    # print(len(list_of_values_copy))

    # _____________________________________

    if len(list_of_values_copy) == 1:
        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        # print('list_of_values_copy', list_of_values_copy[0])
        # print('я дошёл до цикла с условием == 1')
        # print(len(list_of_values_copy))

        ind_0 = get_key(cond_1, list_of_values_copy)
        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0])]
        # print(df_plot)

    # _____________________________________

    if len(list_of_values_copy) == 2:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])

        # print('list_of_values_copy', list_of_values_copy[0], list_of_values_copy[1])
        # print('я дошёл до цикла с условием == 2')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1])]

    # _____________________________________

    if len(list_of_values_copy) == 3:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])

        print('я дошёл до цикла с условием == 3')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2])]

    # _____________________________________

    if len(list_of_values_copy) == 4:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'
        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])

        print('я дошёл до цикла с условием == 4')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3])]

    # _____________________________________

    if len(list_of_values_copy) == 5:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])

        print('я дошёл до цикла с условием == 5')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4])]

    # _____________________________________

    if len(list_of_values_copy) == 6:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])

        print('я дошёл до цикла с условием == 6')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5])]

    # _____________________________________

    if len(list_of_values_copy) == 7:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])

        print('я дошёл до цикла с условием == 7')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6])]

        # _____________________________________

    if len(list_of_values_copy) == 8:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        print('я дошёл до цикла с условием == 8')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7])]

        # _____________________________________

    if len(list_of_values_copy) == 9:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        print('я дошёл до цикла с условием == 9')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8])]

        # _____________________________________

    if len(list_of_values_copy) == 10:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        print('я дошёл до цикла с условием == 10')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9])]

        # _____________________________________

    if len(list_of_values_copy) == 11:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        print('я дошёл до цикла с условием == 11')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10])]

        # _____________________________________

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        print('я дошёл до цикла с условием == 11')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10]) &
                                     all_deals_query_df[ind_11].isin(list_of_values_copy[11])]

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        ind_12 = get_key(cond_1, [list_of_values_copy[12]])
        print('я дошёл до цикла с условием == 12')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10]) &
                                     all_deals_query_df[ind_11].isin(list_of_values_copy[11]) &
                                     all_deals_query_df[ind_12].isin(list_of_values_copy[12])]

    pv = pd.pivot_table(
        df_plot,
        index=['Year'],
        columns=['Agency'],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    width = 650
    height = 450

    # print(len(df_plot['Agency'].unique()))
    if len(df_plot['Agency'].unique()) == 6:
        data = []
        # print(df_plot['Agency'].isin(['SAR']))
        # print('шесть трейсов')
        trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
            color=color.colliers_dark_blue), width=0.2, text=pv[("SQM", 'Colliers')])
        trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')], name='SAR', marker=dict(
            color=color.colliers_light_blue), width=0.2)
        trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')], name='CW', marker=dict(
            color=color.colliers_extra_light_blue), width=0.2)
        trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')], name='CBRE', marker=dict(
            color=color.colliers_grey_40), width=0.2)
        trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')], name='JLL', marker=dict(
            color=color.colliers_yellow), width=0.2)
        trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')], name='KF', marker=dict(
            color=color.colliers_red), width=0.2)

        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])



    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        # print('трейсов мньше шести')
        # print(len(df_plot['Agency'].unique()))
        # print(df_plot['Agency'].unique())
        list_of_unique = df_plot['Agency'].unique()
        if 'Colliers' in list_of_unique:
            trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
                color=color.colliers_dark_blue), width=0.2, text=pv[("SQM", 'Colliers')])
            data.append(trace1)

        if 'SAR' in list_of_unique:
            trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')], name='SAR', marker=dict(
                color=color.colliers_light_blue), width=0.2)
            data.append(trace2)
        # print(data)

        if 'CW' in list_of_unique:
            trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')], name='CW', marker=dict(
                color=color.colliers_extra_light_blue), width=0.2)
            data.append(trace3)
        # print(data)
        if 'CBRE' in list_of_unique:
            trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')], name='CBRE', marker=dict(
                color=color.colliers_grey_40), width=0.2)
            data.append(trace4)
        # print(data)
        if 'JLL' in list_of_unique:
            trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')], name='JLL', marker=dict(
                color=color.colliers_yellow), width=0.2)
            data.append(trace5)
        # print(data)
        if 'KF' in list_of_unique:
            trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')], name='KF', marker=dict(
                color=color.colliers_red), width=0.2)
            data.append(trace6)
        # print(data)

    if len(list_of_values_copy) > 0 and Year not in list_of_values_copy:
        # print(list_of_values_copy)
        format_data = str(list_of_values_copy[0])
        format_year = 'all years'
    elif len(list_of_values_copy) > 0 and Year in list_of_values_copy:
        # print(list_of_values_copy)
        del list_of_values_copy[Year]
        format_data = str(list_of_values_copy[0])

    if Year is not None:
        # print(Year)
        format_year = Year
    elif Year not in list_of_values_copy:
        format_year = 'all years'

    return {
        'data': data,
        'layout':
            go.Layout(
                title='Deals sorted by {}<br>'
                      'in {}'.format(format_data, format_year),
                autosize=False,
                bargap=0.3,
                bargroupgap=0,
                font=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=12),
                width=width,
                height=height,
                margin=dict(pad=0),
                titlefont=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=18),
                xaxis=dict(
                    exponentformat=False,
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=False,
                    ticks='',
                    showticklabels=True,
                    title='Years'
                ),
                yaxis={'title': 'Area in sq.m'},
                barmode='stack')
    }


@app.callback(
    dash.dependencies.Output('market-graph-non-stack-tab', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Country', 'value'),
     dash.dependencies.Input('Agency', 'value'),
     dash.dependencies.Input('City', 'value'),
     dash.dependencies.Input('Property_name', 'value'),
     dash.dependencies.Input('Class', 'value'),
     dash.dependencies.Input('SQM', 'value'),
     dash.dependencies.Input('Business_Sector', 'value'),
     dash.dependencies.Input('Type_of_Deal', 'value'),
     dash.dependencies.Input('Type_of_Consultancy', 'value'),
     dash.dependencies.Input('LLR/TR', 'value'),
     dash.dependencies.Input('Quarter', 'value'),
     dash.dependencies.Input('Company', 'value')
     ])
def update_graph_tab_none_stack(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal,
                                Type_of_Consultancy, LLR_TR, Quarter, Company):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_name=[Property_name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter])

    list_of_values = (
        Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal, Type_of_Consultancy,
        LLR_TR,
        Quarter, Company)
    cond_1 = cond.copy()
    # print(cond_1.values())
    list_of_values_copy = list(filter(None, list_of_values))

    # print('tut grafic')
    # print(len(list_of_values_copy))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = deals_df.copy()
            format_data = 'all deals'
            format_year = 'all years'
            # print(len(list_of_values_copy))
    except TypeError:
        df_plot = deals_df.copy()
    except IndexError:
        df_plot = deals_df.copy()

    print(len(list_of_values_copy))

    # _____________________________________

    if len(list_of_values_copy) == 1:
        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        # print('list_of_values_copy', list_of_values_copy[0])
        # print('я дошёл до цикла с условием == 1')
        # print(len(list_of_values_copy))

        ind_0 = get_key(cond_1, list_of_values_copy)
        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0])]
        # print(df_plot)

    # _____________________________________

    if len(list_of_values_copy) == 2:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])

        # print('list_of_values_copy', list_of_values_copy[0], list_of_values_copy[1])
        # print('я дошёл до цикла с условием == 2')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1])]

    # _____________________________________

    if len(list_of_values_copy) == 3:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])

        print('я дошёл до цикла с условием == 3')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2])]

    # _____________________________________

    if len(list_of_values_copy) == 4:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'
        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])

        print('я дошёл до цикла с условием == 4')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3])]

    # _____________________________________

    if len(list_of_values_copy) == 5:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])

        print('я дошёл до цикла с условием == 5')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4])]

    # _____________________________________

    if len(list_of_values_copy) == 6:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])

        print('я дошёл до цикла с условием == 6')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5])]

    # _____________________________________

    if len(list_of_values_copy) == 7:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])

        print('я дошёл до цикла с условием == 7')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6])]

        # _____________________________________

    if len(list_of_values_copy) == 8:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        print('я дошёл до цикла с условием == 8')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7])]

        # _____________________________________

    if len(list_of_values_copy) == 9:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        print('я дошёл до цикла с условием == 9')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8])]

        # _____________________________________

    if len(list_of_values_copy) == 10:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        print('я дошёл до цикла с условием == 10')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9])]

        # _____________________________________

    if len(list_of_values_copy) == 11:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        print('я дошёл до цикла с условием == 11')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10])]

        # _____________________________________

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        print('я дошёл до цикла с условием == 11')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10]) &
                                     all_deals_query_df[ind_11].isin(list_of_values_copy[11])]

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        ind_12 = get_key(cond_1, [list_of_values_copy[12]])
        print('я дошёл до цикла с условием == 12')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10]) &
                                     all_deals_query_df[ind_11].isin(list_of_values_copy[11]) &
                                     all_deals_query_df[ind_12].isin(list_of_values_copy[12])]

    pv = pd.pivot_table(
        df_plot,
        index=['Year'],
        columns=['Agency'],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    width = 650
    height = 450

    print(len(df_plot['Agency'].unique()))
    if len(df_plot['Agency'].unique()) == 6:
        data = []
        # print(df_plot['Agency'].isin(['SAR']))
        # print('шесть трейсов')
        trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
            color=color.colliers_dark_blue), width=0.2, text=pv[("SQM", 'Colliers')])
        trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')], name='SAR', marker=dict(
            color=color.colliers_light_blue), width=0.2)
        trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')], name='CW', marker=dict(
            color=color.colliers_extra_light_blue), width=0.2)
        trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')], name='CBRE', marker=dict(
            color=color.colliers_grey_40), width=0.2)
        trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')], name='JLL', marker=dict(
            color=color.colliers_yellow), width=0.2)
        trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')], name='KF', marker=dict(
            color=color.colliers_red), width=0.2)

        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])



    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        # print('трейсов мньше шести')
        # print(len(df_plot['Agency'].unique()))
        # print(df_plot['Agency'].unique())
        list_of_unique = df_plot['Agency'].unique()
        if 'Colliers' in list_of_unique:
            trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
                color=color.colliers_dark_blue), width=0.2, text=pv[("SQM", 'Colliers')])
            data.append(trace1)

        if 'SAR' in list_of_unique:
            trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')], name='SAR', marker=dict(
                color=color.colliers_light_blue), width=0.2)
            data.append(trace2)
            # print(data)

        if 'CW' in list_of_unique:
            trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')], name='CW', marker=dict(
                color=color.colliers_extra_light_blue), width=0.2)
            data.append(trace3)
            # print(data)
        if 'CBRE' in list_of_unique:
            trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')], name='CBRE', marker=dict(
                color=color.colliers_grey_40), width=0.2)
            data.append(trace4)
            # print(data)
        if 'JLL' in list_of_unique:
            trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')], name='JLL', marker=dict(
                color=color.colliers_yellow), width=0.2)
            data.append(trace5)
            # print(data)
        if 'KF' in list_of_unique:
            trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')], name='KF', marker=dict(
                color=color.colliers_red), width=0.2)
            data.append(trace6)
            # print(data)

    if len(list_of_values_copy) > 0 and Year not in list_of_values_copy:
        # print(list_of_values_copy)
        format_data = str(list_of_values_copy[0])
        format_year = 'all years'
    elif len(list_of_values_copy) > 0 and Year in list_of_values_copy:
        # print(list_of_values_copy)
        del list_of_values_copy[Year]
        format_data = str(list_of_values_copy[0])

    if Year is not None:
        # print(Year)
        format_year = Year
    elif Year not in list_of_values_copy:
        format_year = 'all years'

    return {
        'data': data,
        'layout':
            go.Layout(
                title='Deals sorted by {}<br>'
                      'in {}'.format(format_data, format_year),
                autosize=False,
                bargap=0.3,
                bargroupgap=0,
                font=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=12),
                width=width,
                height=height,
                margin=dict(pad=0),
                titlefont=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=18),
                xaxis=dict(
                    exponentformat=False,
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=False,
                    ticks='',
                    showticklabels=True,
                    title='Years'
                ),
                yaxis={'title': 'Area in sq.m'},
                # barmode='stack'
            )
    }


@app.callback(
    dash.dependencies.Output('market-graph-horizontal-tab', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     ])
def update_graph_horizontal(Year):
    width = 650
    height = 450

    try:
        if Year[0] == "All years" or len(Year) == 0:
            df_plot = deals_df.copy()
        else:
            df_plot = deals_df[deals_df['Year'].isin(Year)]
    except TypeError:
        df_plot = deals_df.copy()
    except IndexError:
        df_plot = deals_df.copy()

    # if Size == "Default size" or Size is None:
    #     width = 650
    #     height = 450
    #
    # if Size == "50%":
    #     width = 740
    #     height = 360
    #
    # if Size == "33%":
    #     width = 426
    #     height = 240

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    # print(pv[("SQM")].sum())

    trace1 = go.Bar(y=pv.index, x=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
        color=color.colliers_dark_blue), width=0.2, orientation='h')
    trace2 = go.Bar(y=pv.index, x=pv[("SQM", 'SAR')], name='SAR', marker=dict(
        color=color.colliers_light_blue), width=0.2, orientation='h')
    trace3 = go.Bar(y=pv.index, x=pv[("SQM", 'CW')], name='CW', marker=dict(
        color=color.colliers_extra_light_blue), width=0.2, orientation='h')
    trace4 = go.Bar(y=pv.index, x=pv[("SQM", 'CBRE')], name='CBRE', marker=dict(
        color=color.colliers_grey_40), width=0.2, orientation='h')
    trace5 = go.Bar(y=pv.index, x=pv[("SQM", 'JLL')], name='JLL', marker=dict(
        color=color.colliers_yellow), width=0.2, orientation='h')
    trace6 = go.Bar(y=pv.index, x=pv[("SQM", 'KF')], name='KF', marker=dict(
        color=color.colliers_red), width=0.2, orientation='h')

    try:
        if type(Year) == 'NoneType':
            format_data = 'All years'
        elif Year[0] == "All years" or len(Year) == 0 or Year is None:
            format_data = 'All years'
        else:
            format_data = ', '.join(Year)
    except TypeError:
        format_data = 'All years'
    except IndexError:
        format_data = 'All years'

    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':

            go.Layout(
                annotations=[dict(
                    x=pv[("SQM")].sum(),
                    y=trace1["y"],
                    showarrow=False,
                    text=' ',
                    xref="x",
                    yref="y")],
                title='Market Share in {}, %'.format(format_data),
                autosize=False,
                bargap=0.3,
                bargroupgap=0,
                font=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=12),

                width=width,
                height=height,
                margin=dict(pad=0),
                titlefont=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=18),
                xaxis=dict(
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=True,
                    ticks='',
                    showticklabels=True,
                    title='Area in sq.m'
                ),
                yaxis=dict(autorange=True,
                           showgrid=True,
                           zeroline=True,
                           showline=True,
                           autotick=False,
                           ticks='',
                           showticklabels=True,
                           title='Year'
                           ),

                barmode='stack'
            )
    }


@app.callback(
    dash.dependencies.Output('market-pie-graph-tab', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Country', 'value'),
     dash.dependencies.Input('Agency', 'value'),
     dash.dependencies.Input('City', 'value'),
     dash.dependencies.Input('Property_name', 'value'),
     dash.dependencies.Input('Class', 'value'),
     dash.dependencies.Input('SQM', 'value'),
     dash.dependencies.Input('Business_Sector', 'value'),
     dash.dependencies.Input('Type_of_Deal', 'value'),
     dash.dependencies.Input('Type_of_Consultancy', 'value'),
     dash.dependencies.Input('LLR/TR', 'value'),
     dash.dependencies.Input('Quarter', 'value'),
     dash.dependencies.Input('Company', 'value')
     ])
def update_pie_graph(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, LLR_TR, Quarter, Company):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_name=[Property_name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter])

    list_of_values = (
        Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal, Type_of_Consultancy,
        LLR_TR,
        Quarter, Company)
    cond_1 = cond.copy()
    print(cond_1.values())
    list_of_values_copy = list(filter(None, list_of_values))

    # print('tut grafic')
    # print(len(list_of_values_copy))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = deals_df.copy()
            format_data = 'all deals'
            format_year = 'all years'
            print(len(list_of_values_copy))
    except TypeError:
        df_plot = deals_df.copy()
    except IndexError:
        df_plot = deals_df.copy()

    print(len(list_of_values_copy))

    # _____________________________________

    if len(list_of_values_copy) == 1:
        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        print('list_of_values_copy', list_of_values_copy[0])
        print('я дошёл до цикла с условием == 1')
        print(len(list_of_values_copy))

        ind_0 = get_key(cond_1, list_of_values_copy)
        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0])]
        # print(df_plot)

    # _____________________________________

    if len(list_of_values_copy) == 2:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])

        print('list_of_values_copy', list_of_values_copy[0], list_of_values_copy[1])
        print('я дошёл до цикла с условием == 2')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1])]

    # _____________________________________

    if len(list_of_values_copy) == 3:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])

        print('я дошёл до цикла с условием == 3')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2])]

    # _____________________________________

    if len(list_of_values_copy) == 4:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'
        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])

        print('я дошёл до цикла с условием == 4')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3])]

    # _____________________________________

    if len(list_of_values_copy) == 5:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])

        print('я дошёл до цикла с условием == 5')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4])]

    # _____________________________________

    if len(list_of_values_copy) == 6:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        if Year is not None:
            format_year = Year[0]
        elif Year not in list_of_values_copy:
            format_year = 'all years'

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])

        print('я дошёл до цикла с условием == 6')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5])]

    # _____________________________________

    if len(list_of_values_copy) == 7:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])

        print('я дошёл до цикла с условием == 7')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6])]

        # _____________________________________

    if len(list_of_values_copy) == 8:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        print('я дошёл до цикла с условием == 8')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7])]

        # _____________________________________

    if len(list_of_values_copy) == 9:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        print('я дошёл до цикла с условием == 9')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8])]

        # _____________________________________

    if len(list_of_values_copy) == 10:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        print('я дошёл до цикла с условием == 10')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9])]

        # _____________________________________

    if len(list_of_values_copy) == 11:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        print('я дошёл до цикла с условием == 11')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10])]

        # _____________________________________

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        print('я дошёл до цикла с условием == 11')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10]) &
                                     all_deals_query_df[ind_11].isin(list_of_values_copy[11])]

    if len(list_of_values_copy) == 12:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])
        ind_10 = get_key(cond_1, [list_of_values_copy[10]])
        ind_11 = get_key(cond_1, [list_of_values_copy[11]])
        ind_12 = get_key(cond_1, [list_of_values_copy[12]])
        print('я дошёл до цикла с условием == 12')

        df_plot = all_deals_query_df[all_deals_query_df[ind_0].isin(list_of_values_copy[0]) &
                                     all_deals_query_df[ind_1].isin(list_of_values_copy[1]) &
                                     all_deals_query_df[ind_2].isin(list_of_values_copy[2]) &
                                     all_deals_query_df[ind_3].isin(list_of_values_copy[3]) &
                                     all_deals_query_df[ind_4].isin(list_of_values_copy[4]) &
                                     all_deals_query_df[ind_5].isin(list_of_values_copy[5]) &
                                     all_deals_query_df[ind_6].isin(list_of_values_copy[6]) &
                                     all_deals_query_df[ind_7].isin(list_of_values_copy[7]) &
                                     all_deals_query_df[ind_8].isin(list_of_values_copy[8]) &
                                     all_deals_query_df[ind_9].isin(list_of_values_copy[9]) &
                                     all_deals_query_df[ind_10].isin(list_of_values_copy[10]) &
                                     all_deals_query_df[ind_11].isin(list_of_values_copy[11]) &
                                     all_deals_query_df[ind_12].isin(list_of_values_copy[12])]

    pv = pd.pivot_table(
        df_plot,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    colors = [color.colliers_grey_40, color.colliers_extra_light_blue, color.colliers_dark_blue, color.colliers_yellow,
              color.colliers_red, color.colliers_light_blue]

    pie1 = go.Pie(values=pv["SQM"],
                  labels=sorted(pv.index),
                  hoverinfo='label+value+percent',
                  textfont=dict(
                      color=color.white,
                      size=12
                  ),
                  marker=dict(colors=colors,
                              line=dict(
                                  color=color.white,
                                  width=1
                              )
                              )
                  )

    try:
        if type(Year) == 'NoneType':
            format_data = 'All years'
        elif Year[0] == "All years" or len(Year) == 0 or Year is None:
            format_data = 'All years'
        else:
            format_data = ', '.join(Year)
    except TypeError:
        format_data = 'All years'
    except IndexError:
        format_data = 'All years'

    return {
        'data': [pie1],
        'layout': go.Layout(
            title='Deals in {}<br>'
                  'Deals in Russia'.format(format_data),
            width=650,
            height=450,
        )
    }


@app.callback(
    dash.dependencies.Output('market-graph-percent-tab', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     ])
def update_graph_percent(Year):
    width = 650
    height = 450

    # if Size == "Default size" or Size is None:
    #     width = 650
    #     height = 450
    #
    # if Size == "50%":
    #     width = 740
    #     height = 360
    #
    # if Size == "33%":
    #     width = 426
    #     height = 240

    try:
        if Year[0] == "All years" or len(Year) == 0:
            df_plot = deals_df.copy()
        else:
            df_plot = deals_df[deals_df['Year'].isin(Year)]
    except TypeError:
        df_plot = deals_df.copy()
    except IndexError:
        df_plot = deals_df.copy()

        pv1 = pd.pivot_table(
            df_plot,
            index=["Year"],
            columns=["Agency"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)
        pv2 = pd.pivot_table(
            df_plot,
            index=["Agency"],
            columns=["Year"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)

        trace1 = go.Bar(x=pv1.index, y=pv1[("SQM", 'Colliers')] * 100 / pv2["SQM"].sum(), name='Colliers', marker=dict(
            color=color.colliers_light_blue), width=0.25, text='%', textposition='auto')
        trace2 = go.Bar(x=pv1.index, y=pv1[("SQM", 'SAR')] * 100 / pv2["SQM"].sum(), name='SAR', marker=dict(
            color=color.colliers_light_blue), width=0.25, text='%', textposition='auto')
        trace3 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum(), name='CW', marker=dict(
            color=color.colliers_extra_light_blue), width=0.25, text='%', textposition='auto')
        trace4 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum(), name='CBRE', marker=dict(
            color=color.colliers_grey_40), width=0.25, text='%', textposition='auto')
        trace5 = go.Bar(x=pv1.index, y=pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum(), name='JLL', marker=dict(
            color=color.colliers_yellow), width=0.25, text='%', textposition='auto')
        trace6 = go.Bar(x=pv1.index, y=pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum(), name='KF', marker=dict(
            color=color.colliers_red), width=0.25, text='%', textposition='auto')

        try:
            if type(Year) == 'NoneType':
                format_data = 'All years'
            elif Year[0] == "All years" or len(Year) == 0 or Year is None:
                format_data = 'All years'
            else:
                format_data = ', '.join(Year)
        except TypeError:
            format_data = 'All years'
        except IndexError:
            format_data = 'All years'

        return {
            'data': [trace1, trace2, trace3, trace4, trace5, trace6],
            'layout':
                go.Layout(
                    title='Percent in {}'.format(format_data),
                    autosize=False,
                    bargap=0.3,
                    bargroupgap=0,
                    font=dict(
                        color=color.colliers_grey_80,
                        family='Arial',
                        size=12),
                    width=width,
                    height=height,
                    margin=dict(pad=0),
                    titlefont=dict(
                        color=color.colliers_grey_80,
                        family='Arial',
                        size=18),
                    xaxis=dict(
                        autorange=True,
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        autotick=False,
                        ticks='',
                        showticklabels=True,
                        title='Years'
                    ),
                    yaxis={'title': 'Percent'},
                    barmode='stack')
        }

    else:
        df_plot = deals_df[deals_df['Year'].isin(Year)]

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    # print(pv("SQM").sum())
    trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')] * 100 / pv.values.sum(), name='Colliers', marker=dict(
        color=color.colliers_dark_blue), width=0.2, text='%')
    trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')] * 100 / pv.values.sum(), name='SAR', marker=dict(
        color=color.colliers_light_blue), width=0.2, text='%')
    trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')] * 100 / pv.values.sum(), name='CW', marker=dict(
        color=color.colliers_extra_light_blue), width=0.2, text='%')
    trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')] * 100 / pv.values.sum(), name='CBRE', marker=dict(
        color=color.colliers_grey_40), width=0.2, text='%')
    trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')] * 100 / pv.values.sum(), name='JLL', marker=dict(
        color=color.colliers_yellow), width=0.2, text='%')
    trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')] * 100 / pv.values.sum(), name='KF', marker=dict(
        color=color.colliers_red), width=0.2, text='%')

    try:
        if type(Year) == 'NoneType':
            format_data = 'All years'
        elif Year[0] == "All years" or len(Year) == 0 or Year is None:
            format_data = 'All years'
        else:
            format_data = ', '.join(Year)
    except TypeError:
        format_data = 'All years'
    except IndexError:
        format_data = 'All years'

    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='Percent in {}'.format(format_data),
                autosize=False,
                bargap=0.3,
                bargroupgap=0,
                font=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=12),
                width=width,
                height=height,
                margin=dict(pad=0),
                titlefont=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=18),
                xaxis=dict(
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=False,
                    ticks='',
                    showticklabels=True,
                    title='Years'
                ),
                yaxis={'title': 'Percent'},
                barmode='stack')
    }


@app.callback(
    dash.dependencies.Output('market-graph-horizontal-total-tab', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     ])
def update_graph_horizontal_total(Year):
    width = 650
    height = 450

    try:
        if Year[0] == "All years" or len(Year) == 0:
            df_plot = deals_df.copy()
        else:
            df_plot = deals_df[deals_df['Year'].isin(Year)]
    except TypeError:
        df_plot = deals_df.copy()
    except IndexError:
        df_plot = deals_df.copy()

    # if Size == "Default size" or Size is None:
    #     width = 650
    #     height = 450
    #
    # if Size == "50%":
    #     width = 740
    #     height = 360
    #
    # if Size == "33%":
    #     width = 426
    #     height = 240

    pv = pd.pivot_table(
        df_plot,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    # print('___________++__________')
    # print(pv)

    trace1 = go.Bar(x=pv[("SQM")], y=pv.index, marker=dict(
        color=color.colliers_dark_blue), width=0.2, orientation='h')

    try:
        if type(Year) == 'NoneType':
            format_data = 'All years'
        elif Year[0] == "All years" or len(Year) == 0 or Year is None:
            format_data = 'All years'
        else:
            format_data = ', '.join(Year)
    except TypeError:
        format_data = 'All years'
    except IndexError:
        format_data = 'All years'

    return {
        'data': [trace1],
        'layout':
            go.Layout(
                title='Deals in {}'.format(format_data),
                autosize=False,
                bargap=0.3,
                bargroupgap=0,
                font=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=12),

                width=width,
                height=height,
                margin=dict(pad=0),
                titlefont=dict(
                    color=color.colliers_grey_80,
                    family='Arial',
                    size=18),
                xaxis=dict(
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=True,
                    ticks='',
                    showticklabels=True,
                    title='Area in sq.m'
                ),
                yaxis=dict(autorange=True,
                           showgrid=True,
                           zeroline=True,
                           showline=True,
                           autotick=False,
                           ticks='',
                           showticklabels=True,
                           ),
            )
    }


# '''
#     Конец блока по странице с таблицами
#
#                                          '''

suspicious_deals_layout = html.Div(
    [
        html.Div([
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                children="База данных по сделкам",
                                className='row',
                                style={'textAlign': 'center',
                                       'margin': '20 0 0 15px',
                                       'color': color.colliers_grey_10,
                                       'display': 'inline-block',
                                       }
                            ),
                        ],
                        style={'textAlign': 'left',
                               'margin': '0 0 0 25px',
                               'display': 'inline',
                               }
                    ),

                    html.A(html.Button('About Project',
                                       # className='button-primary',
                                       style={
                                           'display': 'inline-block',
                                           'float': 'right',
                                           'height': '46px',
                                           'padding': '0 0 10 5px',
                                           'color': '#FFF',
                                           'text-align': 'center',
                                           'font-size': '14px',
                                           'font-weight': '500',
                                           'line-height': '38px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'uppercase',
                                           'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           'background-color': color.colliers_light_blue_20,
                                           'border-radius': '0px',
                                           'border': '1px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           # className='row',
                           href='/page-about'),

                    html.A(html.Button('Help',
                                       # className='button-primary',
                                       style={
                                           'display': 'inline-block',
                                           'float': 'right',
                                           'height': '46px',
                                           'padding': '5 15px',
                                           'color': '#FFF',
                                           'text-align': 'center',
                                           'font-size': '14px',
                                           'font-weight': '500',
                                           'line-height': '38px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'uppercase',
                                           'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           'background-color': color.colliers_light_blue_20,
                                           'border-radius': '0px',
                                           'border': '1px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           # className='row',
                           href='/page-help'),

                    html.A(html.Button('To main page',
                                       className='button-primary',
                                       style={
                                           'display': 'inline-block',
                                           'float': 'right',
                                           'height': '46px',
                                           'padding': '5 15px',
                                           'color': '#FFF',
                                           'text-align': 'center',
                                           'font-size': '14px',
                                           'font-weight': '500',
                                           'line-height': '38px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'uppercase',
                                           'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           'background-color': color.colliers_light_blue_20,
                                           'border-radius': '0px',
                                           'border': '1px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           # className='row',
                           href='/main')
                ],
                # style={'display': 'inline-block'},
            ),
        ],
            className='banner',
            style={'backgroundColor': color.colliers_dark_blue,
                   }
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.A(html.Button('Позиции на рынке России',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': color.colliers_pale_blue,
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   },
                                                   # autoFocus={
                                                   #     'color': '#FFF',
                                                   #     'background-color': color.colliers_pale_blue,
                                                   #     'border-color': '#1EAEDB'
                                                   # }
                                                   ),
                                       href='/page-1'),
                                html.Br(),
                                html.A(html.Button('Позиции на рынке Москвы',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-2'
                                       ),
                                html.Br(),
                                html.A(html.Button('Доля сделок Sale vs Lease',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-3'),
                                html.Br(),
                                html.A(html.Button('База по сделкам',
                                                   className='button-active',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       # 'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-4'),
                                html.Br(),
                                html.A(html.Button('Обновить базу по сделкам',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-5')
                            ],
                            className='two columns',
                            style={'backgroundColor': color.colliers_pale_blue,  # цвет фона за блоком с ссылками
                                   # 'width': '15%',
                                   # 'margin': '20 0 100 0px',
                                   'height': '1350px',
                                   # 'display': 'inline-block'
                                   }
                        ),

                    ],
                    style={'backgroundColor': color.colliers_pale_blue,
                           }
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.A(html.Button('Показать все сделки',
                                                   className='button-primary',
                                                   style={
                                                       'display': 'inline',
                                                       'float': 'right',
                                                       'height': '46px',
                                                       'padding': '5 15px',
                                                       'color': '#FFF',
                                                       'text-align': 'center',
                                                       'font-size': '14px',
                                                       'font-weight': '500',
                                                       'line-height': '38px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'uppercase',
                                                       'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       'background-color': color.colliers_light_blue_20,
                                                       'border-radius': '0px',
                                                       'border': '1px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-4'
                                       ),
                                html.A(html.Button('Показать сомнительные сделки',
                                                   className='button-primary',
                                                   style={
                                                       'display': 'inline',
                                                       'float': 'right',
                                                       'height': '46px',
                                                       'padding': '5 15px',
                                                       'color': '#FFF',
                                                       'text-align': 'center',
                                                       'font-size': '14px',
                                                       'font-weight': '500',
                                                       'line-height': '38px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'uppercase',
                                                       'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       'background-color': color.colliers_light_blue_20,
                                                       'border-radius': '0px',
                                                       'border': '1px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/suspicious_deals'),
                            ]
                        ),
                        html.H5(children="Сомнительные сделки",
                                className='row',
                                style={'textAlign': 'center', 'color': color.colliers_grey_80
                                       }
                                ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Agency",
                                            # value='All agency',
                                            placeholder="Агентство",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in Agency
                                            ],
                                        )
                                    ],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'inline-block',
                                        # 'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [dcc.Dropdown(
                                        id="Country",
                                        # value='All countries',
                                        placeholder="Страна",
                                        multi=True,
                                        options=[{
                                            'label': j,
                                            'value': j
                                        }
                                            for j in country_ind
                                        ],
                                    )
                                    ],
                                    # className='two columns',
                                    style={
                                        'width': '10%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div(
                                    [dcc.Dropdown(
                                        id="City",
                                        # value='All agency',
                                        placeholder="Город",
                                        multi=True,
                                        options=[{
                                            'label': i,
                                            'value': i
                                        }
                                            for i in all_deals_query_df["City"].unique()
                                        ],

                                    )],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div([dcc.Dropdown(
                                    id="Property_name",
                                    # value='All agency',
                                    placeholder="Объект",
                                    multi=True,
                                    options=[{
                                        'label': i,
                                        'value': i
                                    }
                                        for i in all_deals_query_df["Property_Name"].unique()
                                    ],

                                )],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div([dcc.Dropdown(
                                    id="Class",
                                    # value='All agency',
                                    placeholder="Класс",
                                    multi=True,
                                    options=[{
                                        'label': i,
                                        'value': i
                                    }
                                        for i in all_deals_query_df["Class"].unique()
                                    ],

                                )],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div([dcc.Dropdown(
                                    id="SQM",
                                    # value='All agency',
                                    placeholder="Площадь",
                                    multi=True,
                                    options=[{
                                        'label': i,
                                        'value': i
                                    }
                                        for i in all_deals_query_df["SQM"].unique()
                                    ],

                                )],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div([dcc.Dropdown(
                                    id="Company",
                                    # value='All agency',
                                    placeholder="Компания",
                                    multi=True,
                                    options=[{
                                        'label': i,
                                        'value': i
                                    }
                                        for i in all_deals_query_df["Company"].unique()
                                    ],

                                )],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),

                                html.Div([dcc.Dropdown(
                                    id="Type_of_Consultancy",
                                    # value='All agency',
                                    placeholder="Тип сделки",
                                    multi=True,
                                    options=[{
                                        'label': i,
                                        'value': i
                                    }
                                        for i in all_deals_query_df["Type_of_Consultancy"].unique()
                                    ],

                                )],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Year",
                                            multi=True,
                                            # value='All years',
                                            placeholder="Год",
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in years
                                            ],
                                        )
                                    ],
                                    # className='two columns',
                                    style={
                                        'width': '10%',
                                        # 'padding-left': '10',
                                        # 'margin-left': '3%',
                                        'display': 'inline-block',
                                        # 'float': 'right'
                                    }
                                ),
                                html.Div([dcc.Dropdown(
                                    id="Quarter",
                                    # value='All agency',
                                    placeholder="Квартал",
                                    multi=True,
                                    options=[{
                                        'label': i,
                                        'value': i
                                    }
                                        for i in all_deals_query_df["Quarter"].unique()
                                    ],

                                )],
                                    # className='one columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                            ],
                            className='row'
                        ),

                        html.Div(
                            [
                                dt.DataTable(
                                    rows=[{}],  # initialise the row
                                    editable=False,
                                    row_selectable=False,
                                    filterable=False,
                                    sortable=True,
                                    selected_row_indices=[],
                                    min_height=600,
                                    id='datatable-suspicious'
                                )
                            ]
                        ),
                        html.Div(id='sum',
                                 style={'color': color.colliers_grey_10,
                                        'background-color': color.colliers_dark_blue,
                                        'fontSize': 14,
                                        'border': 'solid 1px black',
                                        }
                                 ),
                        html.Div([
                            html.A(
                                'Download All Data',
                                id='download-all-link',
                                download="all_data.csv",
                                href="",
                                target="_blank",
                            ),
                        ],
                            style={'background-color': color.colliers_dark_blue}
                        ),
                        html.Div([
                            html.A(
                                'Download Selected Data',
                                id='download-selected-link',
                                download="selected_data.csv",
                                href="",
                                target="_blank",
                            )
                        ],
                            style={'background-color': color.colliers_dark_blue}
                        ),

                    ],
                    className='ten columns',
                )

            ],
            style={'backgroundColor': color.colliers_grey_10}

        )
    ],
    style={'backgroundColor': color.colliers_pale_blue}
)


@app.callback(dash.dependencies.Output('datatable-suspicious', 'rows'),
              [dash.dependencies.Input('Year', 'value'),
               dash.dependencies.Input('Country', 'value'),
               dash.dependencies.Input('Agency', 'value'),
               dash.dependencies.Input('City', 'value'),
               dash.dependencies.Input('Property_name', 'value'),
               dash.dependencies.Input('Class', 'value'),
               dash.dependencies.Input('SQM', 'value'),
               dash.dependencies.Input('Type_of_Consultancy', 'value'),
               dash.dependencies.Input('Quarter', 'value'),
               dash.dependencies.Input('Company', 'value')
               ])
def update_datatable_susp(Year, Country, Agency, City, Property_name, Class, SQM, Type_of_Consultancy, Quarter,
                          Company):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_name=[Property_name], Class=[Class],
                SQM=[SQM], Company=[Company], Type_of_Consultancy=[Type_of_Consultancy], Quarter=[Quarter])
    print('New iteration')

    list_of_values = (Year, Country, Agency, City, Property_name, Class, SQM, Type_of_Consultancy, Quarter)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    suspecious_deals_df_equal_sqm = all_deals_query_df[all_deals_query_df.duplicated(['SQM'], keep=False)].sort_values(
        'SQM', ascending=False)

    suspecious_deals_df_equal_sqm_year = all_deals_query_df[
        all_deals_query_df.duplicated(['SQM', 'Year'], keep=False)].sort_values('SQM', ascending=False)

    sort_for_dif = all_deals_query_df.sort_values('SQM', ascending=False)

    dif = sort_for_dif[sort_for_dif['SQM'].diff() < 5]

    # sorted_dif = sorted_dif[sorted_dif['SQM'].diff() < 5]

    # print(all_deals_query_df['SQM'].diff() < 5)
    # print(dif)

    suspecious_deals_df = pd.merge(suspecious_deals_df_equal_sqm, suspecious_deals_df_equal_sqm_year, how='outer')

    print(suspecious_deals_df)

    suspecious_deals_df_no = pd.merge(suspecious_deals_df_equal_sqm, suspecious_deals_df_equal_sqm_year)

    print(suspecious_deals_df_no)

    # new_merge_deals = suspecious_deals_df_no.subtract(dif)

    # print(new_merge_deals)

    if len(list_of_values_copy) == 0:
        return suspecious_deals_df_no.to_dict('records')

    # ____________________________________________________________#

    if len(list_of_values_copy) == 1:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind = get_key(cond_1, list_of_values_copy)
        print(list_of_values_copy[0], 'второе условие')
        data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[0]))]
        return data.to_dict('records')
    # _________________________________________________________________#

    if len(list_of_values_copy) == 2:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])

        print(list_of_values_copy[0], 'третье условие')

        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1]))]
        return data.to_dict('records')

    # __________________________________________________________________________#

    if len(list_of_values_copy) == 3:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])

        print(list_of_values_copy[0], 'четвертое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2]))]
        return data.to_dict('records')
    # _______________________________________________#
    if len(list_of_values_copy) == 4:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])

        print(list_of_values_copy[0], 'пятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3]))]
        return data.to_dict('records')

    # ____________________________
    if len(list_of_values_copy) == 5:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])

        print(list_of_values_copy[0], 'шестое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4]))]
        return data.to_dict('records')

    # _________________________________________________________________#

    if len(list_of_values_copy) == 6:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])

        print(list_of_values_copy[0], 'седьмое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5]))]
        return data.to_dict('records')

    # ______________________________________________________________________#

    if len(list_of_values_copy) == 7:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])

        print(list_of_values_copy[0], 'восьмое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6]))]
        return data.to_dict('records')

    # _________________________________________________________________

    if len(list_of_values_copy) == 8:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])

        print(list_of_values_copy[0], 'девятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7]))]
        return data.to_dict('records')

    # ________________________________________________________________________________________

    if len(list_of_values_copy) == 9:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8]))]
        return data.to_dict('records')

    # _____________________________________________________________--#

    if len(list_of_values_copy) == 10:

        def get_key(d, value):
            for k, v in d.items():
                if v == value:
                    return k

        ind_0 = get_key(cond_1, [list_of_values_copy[0]])
        ind_1 = get_key(cond_1, [list_of_values_copy[1]])
        ind_2 = get_key(cond_1, [list_of_values_copy[2]])
        ind_3 = get_key(cond_1, [list_of_values_copy[3]])
        ind_4 = get_key(cond_1, [list_of_values_copy[4]])
        ind_5 = get_key(cond_1, [list_of_values_copy[5]])
        ind_6 = get_key(cond_1, [list_of_values_copy[6]])
        ind_7 = get_key(cond_1, [list_of_values_copy[7]])
        ind_8 = get_key(cond_1, [list_of_values_copy[8]])
        ind_9 = get_key(cond_1, [list_of_values_copy[9]])

        print(list_of_values_copy[0], 'десятое условие')
        data = all_deals_query_df[(all_deals_query_df[ind_0].isin(list_of_values_copy[0])) &
                                  (all_deals_query_df[ind_1].isin(list_of_values_copy[1])) &
                                  (all_deals_query_df[ind_2].isin(list_of_values_copy[2])) &
                                  (all_deals_query_df[ind_3].isin(list_of_values_copy[3])) &
                                  (all_deals_query_df[ind_4].isin(list_of_values_copy[4])) &
                                  (all_deals_query_df[ind_5].isin(list_of_values_copy[5])) &
                                  (all_deals_query_df[ind_6].isin(list_of_values_copy[6])) &
                                  (all_deals_query_df[ind_7].isin(list_of_values_copy[7])) &
                                  (all_deals_query_df[ind_8].isin(list_of_values_copy[8])) &
                                  (all_deals_query_df[ind_9].isin(list_of_values_copy[9]))]
        return data.to_dict('records')


# '''
#     Обновление базы данных по сделкам.
#
#                                          '''

page_5_layout = html.Div(
    [
        html.Div([
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                children="Обновление базы по сделкам",
                                className='row',
                                style={'textAlign': 'center',
                                       'margin': '20 0 0 15px',
                                       'color': color.colliers_grey_10,
                                       'display': 'inline-block',
                                       }
                            ),
                        ],
                        style={'textAlign': 'left',
                               'margin': '0 0 0 25px',
                               'display': 'inline',
                               }
                    ),

                    html.A(html.Button('About Project',
                                       # className='button-primary',
                                       style={
                                           'display': 'inline-block',
                                           'float': 'right',
                                           'height': '46px',
                                           'padding': '0 0 10 5px',
                                           'color': '#FFF',
                                           'text-align': 'center',
                                           'font-size': '14px',
                                           'font-weight': '500',
                                           'line-height': '38px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'uppercase',
                                           'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           'background-color': color.colliers_light_blue_20,
                                           'border-radius': '0px',
                                           'border': '1px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           # className='row',
                           href='/page-about'),

                    html.A(html.Button('Help',
                                       # className='button-primary',
                                       style={
                                           'display': 'inline-block',
                                           'float': 'right',
                                           'height': '46px',
                                           'padding': '5 15px',
                                           'color': '#FFF',
                                           'text-align': 'center',
                                           'font-size': '14px',
                                           'font-weight': '500',
                                           'line-height': '38px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'uppercase',
                                           'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           'background-color': color.colliers_light_blue_20,
                                           'border-radius': '0px',
                                           'border': '1px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           # className='row',
                           href='/page-help'),

                    html.A(html.Button('To main page',
                                       className='button-primary',
                                       style={
                                           'display': 'inline-block',
                                           'float': 'right',
                                           'height': '46px',
                                           'padding': '5 15px',
                                           'color': '#FFF',
                                           'text-align': 'center',
                                           'font-size': '14px',
                                           'font-weight': '500',
                                           'line-height': '38px',
                                           'letter-spacing': '.001rem',
                                           'text-transform': 'uppercase',
                                           'text-decoration': 'none',
                                           'white-space': 'nowrap',
                                           'background-color': color.colliers_light_blue_20,
                                           'border-radius': '0px',
                                           'border': '1px solid #bbb',
                                           'cursor': 'pointer',
                                           'box-sizing': 'border-box'
                                       }
                                       ),
                           # className='row',
                           href='/main')
                ],
                # style={'display': 'inline-block'},
            ),
        ],
            className='banner',
            style={'backgroundColor': color.colliers_dark_blue,
                   }
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.A(html.Button('Позиции на рынке России',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': color.colliers_pale_blue,
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   },
                                                   # autoFocus={
                                                   #     'color': '#FFF',
                                                   #     'background-color': color.colliers_pale_blue,
                                                   #     'border-color': '#1EAEDB'
                                                   # }
                                                   ),
                                       href='/page-1'),
                                html.Br(),
                                html.A(html.Button('Позиции на рынке Москвы',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-2'
                                       ),
                                html.Br(),
                                html.A(html.Button('Доля сделок Sale vs Lease',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-3'),
                                html.Br(),
                                html.A(html.Button('База по сделкам',
                                                   className='button-primary',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-4'),

                                html.Br(),
                                html.A(html.Button('Обновить базу по сделкам',
                                                   className='button-active',
                                                   style={
                                                       # 'display': 'inline',
                                                       'height': '38px',
                                                       'width': '100%',
                                                       'padding': '0 0 0 12px',
                                                       # 'color': color.colliers_light_blue,
                                                       'text-align': 'left',
                                                       'font-size': '14px',
                                                       'font-weight': '300',
                                                       'line-height': '20px',
                                                       'letter-spacing': '.001rem',
                                                       'text-transform': 'none',
                                                       # 'text-decoration': 'none',
                                                       'white-space': 'nowrap',
                                                       # 'background-color': 'transparent',
                                                       'border-radius': '0px',
                                                       'border': '0px solid #bbb',
                                                       'cursor': 'pointer',
                                                       'box-sizing': 'border-box'
                                                   }
                                                   ),
                                       href='/page-5'),

                            ],
                            className='two columns',
                            style={'backgroundColor': color.colliers_pale_blue,  # цвет фона за блоком с ссылками
                                   # 'width': '15%',
                                   # 'margin': '20 0 100 0px',
                                   'height': '1350px',
                                   # 'display': 'inline-block'
                                   }
                        ),

                    ],
                    style={'backgroundColor': color.colliers_pale_blue,
                           }
                ),

                html.Div(
                    [
                        html.Div([
                            html.A(html.Button('Скачать шабон', className='button',
                                               style={
                                                   'display': 'inline-block',
                                                   'height': '38px',
                                                   'padding': '0 15px',
                                                   'color': '#FFF',  # аоставить цвет как в интегисе
                                                   #  'text-align': 'center',
                                                   #  'font-size': '11px',
                                                   #  'font-weight': '600',
                                                   #  'line-height': '38px',
                                                   #  'letter-spacing': '.1rem',
                                                   #  'text-transform': 'uppercase',
                                                   #  'text-decoration': 'none',
                                                   #  'white-space': 'nowrap',
                                                   'background-color': '#81C784',
                                                   #  'border-radius': '4px',
                                                   'border': '1px solid',
                                                   #  'cursor': 'pointer',
                                                   #  'box-sizing': 'border-box'
                                               }
                                               ),
                                   id='download-example-button',
                                   download="update_example.csv",
                                   href="",
                                   target="_blank"
                                   ),
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'display': 'inline-block',
                                    'width': '50%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),
                            html.Div([
                                dcc.Markdown('''
[Справка по обновлению базы данных по сделкам](/page-help)
                            ''')], style={
                                'display': 'inline-block'}),

                            html.Div(id='output-data-upload'),
                            # Hidden div inside the app that stores the intermediate value
                            html.Div(id='intermediate-value', style={'display': 'none'}
                                     ),
                            html.Table(id='table', style={'display': 'none'}),
                            html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})

                        ]
                        ),

                    ],
                    className='ten columns',
                    style={'display': 'inline'}
                    # style={'display': 'inline-block'}
                ),

            ],
            style={'backgroundColor': color.colliers_grey_10}

        )
    ],
    style={'backgroundColor': color.colliers_pale_blue}
)


@app.callback(
    dash.dependencies.Output('download-example-button', 'href'),
    [dash.dependencies.Input('download-example-button', 'n_clicks')]
)
def example_button(n_clicks):
    data = pd.DataFrame.from_records([list_of_columns])

    # print(data)
    csv_string = data.to_csv(header=False, index=False, encoding='utf-8', sep=',')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string + "==")

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv((io.StringIO(decoded.decode('utf-8'))), header=None)
            df.columns = list_of_columns
            # df.columns = ['ID', 'Name', 'Info']
            # df.to_sql('update_test', con, if_exists='append', index=False)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
            df.columns = list_of_columns
            # df.columns = ['ID', 'Name', 'Info']
            # df.to_sql('update_test', con, if_exists='append', index=False)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div(
        [
            html.H5(filename),
            dt.DataTable(rows=df.to_dict('records')),
        ]
    )


@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              [dash.dependencies.Input('upload-data', 'contents'),
               dash.dependencies.Input('upload-data', 'filename'),
               ])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


def save_contents(contents_save, filename_save):
    content_type, content_string = contents_save.split(',')
    decoded = base64.b64decode(content_string + "==")

    try:
        if 'csv' in filename_save:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv((io.StringIO(decoded.decode('utf-8'))), header=None)
            json = df.to_json(date_format='iso', orient='split')
            # print(type(json))
            # df.columns = ['ID', 'Name', 'Info']
            # df.to_sql('update_test', con, if_exists='append', index=False)

        elif 'xls' in filename_save:
            # Assume that the user uploaded an excel file
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
            json = df.to_json(date_format='iso', orient='split')
            # df.columns = ['ID', 'Name', 'Info']
            # df.to_sql('update_test', con, if_exists='append', index=False)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return json


@app.callback(dash.dependencies.Output('intermediate-value', 'children'),
              [dash.dependencies.Input('upload-data', 'contents'),
               dash.dependencies.Input('upload-data', 'filename'),
               ])
def save_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            save_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        # print(type(children))
        return children


@app.callback(dash.dependencies.Output('table', 'children'),
              [dash.dependencies.Input('intermediate-value', 'children')]
              )
def update_table(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        print(type(jsonified_cleaned_data))
        print(jsonified_cleaned_data)
        dff = pd.read_json(jsonified_cleaned_data[0], orient='split')
        print(dff)
        dff.columns = list_of_columns
        print(dff)
        # print(dff.DataFrme(index=False))
        dff.to_sql('Market_Share', con, if_exists='append', index=None, index_label=list_of_columns)
        return print('База обновлена')
    else:
        print('empty json')


# Обновление страницы
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    # if pathname == '/page-1':
    #     return page_1_layout
    # elif pathname == '/page-2':
    #     return page_2_layout
    # elif pathname == '/page-3':
    #     return page_3_layout
    if pathname == '/page-4':
        return page_4_layout
    elif pathname == '/page-5':
        return page_5_layout
    elif pathname == '/suspicious_deals':
        return suspicious_deals_layout
    elif pathname == '/page-help':
        return page_help_layout
    elif pathname == '/page-about':
        return page_about_layout
    else:
        return index_page
        # You could also return a 404 "URL not found" page here


# help(dt.DataTable)

if __name__ == '__main__':
    app.run_server(debug=True, host='10.168.207.102')
