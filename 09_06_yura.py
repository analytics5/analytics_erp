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
# import Passwords_and_Usernames as users
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from itertools import chain

#py.sign_in('Wittgensteen', 'D9dEx9VG7SfqBlkoDvRl')  # вход в аккаунт на plotly Юра
py.sign_in('Barbrady', 'V11sgDqsmE4XpTsVGoFJ')  # вход в аккаунт на plotly Дима


dbname = 'postgres'  # название базы данных
host = 'localhost'  # IP адрес хоста, если сервер локальный, "localhost"
user = 'postgres'  # имя учетной записи в БД
password = '3334'  # пароль для подключения к БД
port = '5432'  # порт для подключения к БД
conn = pg.connect(dbname=dbname, host=host, user=user,
                  password=password)  # подключение к базе данных с помощью psycopg2

url = 'postgresql://{}:{}@{}:{}/{}'  # подключение к базе данных с помощью sqlalchemy
url = url.format(user, password, host, port, dbname)
con = sqlalchemy.create_engine(url, client_encoding='utf8')
meta = sqlalchemy.MetaData(bind=con, reflect=True)

all_deals_query = sql.table_query_new_all  # датафрейм с дампом всей базы по сделкам
suspicious_deals = sql.table_query  # датафрейм с дампом базы по сомнительным сделкам, возможно, стоит убрать

country = ("All countries", "Russia", "Ukraine", "Belarus", "Kazakhstan ",
           "Azerbaijan")  # кортеж со списком стран доля выпадающего списка
country_ind = ("All countries", "RU", "UA", "BY", "KZ", "AZ")  # кортеж со списком стран доля выпадающего списка
years = ("All years", "2013", "2014", "2015", "2016", "2017", "2018")  # кортеж со списком годов доля выпадающего списка
Agency = (
    "All agency", "Colliers", "KF", "JLL", "CW", "SAR", "CBRE")  # кортеж со списком компаний доля выпадающего списка
Agency_tab = ("Colliers", "KF", "JLL", "CW", "SAR", "CBRE")  # кортеж со списком компаний доля выпадающего списка
list_of_columns = [
    "Include_in_Market_Share", "Agency", "Country", "City",  # список заголовков таблицы по всем сделкам
    "Property_Name", "Address", "Submarket_Large", "Owner",
    "Date_of_acquiring", "Class", "Class_Colliers", "Floor",
    "SQM", "Deal_Size", "Company", "Business_Sector", "Sublease_Agent",
    "Type_of_Deal", "Type_of_Consultancy", "LLR_TR", "LLR_Only",
    "E_TR_Only", "LLR/E_TR", "Month", "Year", "Quarter"]

list_of_columns_suspicious = [
    'Agency', 'Country', 'City', 'Property Name',  # список заголовков таблицы по сомнительным сделкам
    'Class', 'SQM', 'Company', 'Type_of_Consultancy',
    'Year', 'Quarter']

list_of_columns_for_gui = [
    "Include in market share", "Agency", "Country", "City",  # список чеклиста для выбора столбцов таблицы из дерева
    "Property name", "Address", "Submarket large", "Owner",
    "Date of acquiring", "Class", "Class Colliers", "Floor",
    "SQM", "Size of deal", "Company", "Business sector", "Sublease agent",
    "Type of deal", "Type of consultancy", "LLR/TR", "LLR only",
    "(E)TR only", "LLR/(E)TR", "Month", "Year", "Quarter"]

with conn:
    cur = conn.cursor()           # запорос к БД через psycopg2
    cur.execute(all_deals_query)  # исполнение SQL команды по дампу всей базы
    all_deals_query_data = cur.fetchall()  # запись данных во временную переменную
    all_deals_query_df = pd.DataFrame(all_deals_query_data)  # запись данных в pandas data frame
    all_deals_query_df.columns = list_of_columns  # имена столбцов датафрейма по сделкам
    all_deals_query_df["LLR_Only"] = all_deals_query_df["LLR_Only"].replace(
        {True: 'Yes', False: 'No'})  # замена булевых значений на yes и no
    all_deals_query_df["E_TR_Only"] = all_deals_query_df["E_TR_Only"].replace(
        {True: 'Yes', False: 'No'})  # замена булевых значений на yes и no
    all_deals_query_df["LLR/E_TR"] = all_deals_query_df["LLR/E_TR"].replace(
        {True: 'Yes', False: 'No'})  # замена булевых значений на yes и no

    cur.execute(suspicious_deals)  # выполнение SQL запроса по сделкам
    suspicious_deals_data = cur.fetchall()  # данные по сделкам
    suspicious_deals_df = pd.DataFrame(suspicious_deals_data)  # Запись в датафрейм
    suspicious_deals_df.columns = list_of_columns_suspicious  # имена столбцов датафрейма по сомнительным сделкам


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


# '''
#     Начало основного блока приложения
#
#                                          '''

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
app.css.append_css({  # Мой файл с гитхаба на rawgit с измененной разметкой
    'external_url': 'https://rawgit.com/Wittgensteen/work_stuff/master/new_buttons.css'})

# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})    # CSS разметка. Та, что предлагают plotly
# app.css.append_css({'external_url': 'https://raw.githubusercontent.com/Wittgensteen/work_stuff/master/base_style.css'})    # Мой файл с разметкой
# auth = dash_auth.BasicAuth(app, users.VALID_USERNAME_PASSWORD_PAIRS)     #авторизация пользователя, скорее всего не будет использоваться, но оставить всё-таки надо, на случай


# '''
#     Инициализация основного окна приложения, без этой страницы не работают остальные
#
#'''


def serve_layout():

    return html.Div(
        [
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content'),
            html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}
                     ),
        ],
        # style={'backgroundColor': color.colliers_dark_blue}            #цвет фона всех страниц, в текущий момент - белый
    )

app.layout = serve_layout

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
                       # 'width': '15%',
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
        dcc.Interval(                    # таймер обновления компонентов
            id='interval-component',
            interval=1*5000,             # таймер отсчитывает миллисекунды
            n_intervals=0
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Checklist(  # чеклист с одним значением для имитации дерева параметров
                            id='tree-checklist',  # при выборе параметра, открывается список для отображения столбцов
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
                        dcc.Checklist(  # чеклист для выбора столбцов в таблице
                            id='interface',
                            options=[{'label': i, 'value': j} for i, j in  # все возможные значения
                                     zip(list_of_columns_for_gui, list_of_columns)],
                            values=['Agency', 'Country', 'City', 'Property_Name',
                                    # значения по умолчанию при первй загрузке страницы
                                    'Class', 'SQM', "Company", "Business_Sector",
                                    'Type_of_Deal', 'Type_of_Consultancy', 'LLR_TR', 'Year', 'Quarter'],
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
            id='interface-bar',
            className='one column',
            style={'backgroundColor': color.colliers_pale_blue,  # цвет фона за блоком с ссылками
                   'width': '192px',
                   'margin-top': '0px',
                   # 'max-height': '100vh',
                   'min-height': '220vh',
                   # 'position': 'absolute',
                   'display': 'block',
                   }
        ),
        html.Div(
            [
                html.Button('<<',
                            id='interface-arrow-left',
                            # className='button-primary',
                            style={
                                'position': 'fixed',
                                # элемент зафиксирован на странице и при прокрутке не меняет своё положение
                                'left': '194px',
                                'box-shadow': '0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19',
                                'display': 'inline-block',
                                'max-height': '100vh',
                                'min-height': '100vh',
                                'width': '15px',
                                # 'float': 'right',
                                # 'height': '46px',
                                'padding': '0 0px',
                                'color': '#FFF',
                                'text-align': '100vh',
                                'font-size': '12px',
                                'font-weight': '500',
                                'line-height': '38px',
                                'letter-spacing': '.001rem',
                                'text-transform': 'uppercase',
                                'text-decoration': 'none',
                                'white-space': 'nowrap',
                                'background-color': color.colliers_yellow,
                                'color': color.colliers_grey_80,
                                'border-radius': '0px',
                                'border': '1px solid #bbb',
                                'cursor': 'pointer',
                                'box-sizing': 'border-box'
                            }
                            )

            ]
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
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
                                       href='/main'),

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
                                        html.Div(
                                            ['Агентство'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Страна'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Город'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Объект'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Класс'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Площадь'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Компания'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Сектор'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Тип сделки'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
                                        dcc.Dropdown(
                                            id="Type_of_Deal",
                                            # value='All agency',
                                            placeholder="Тип сделки",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Type_of_Deal"].unique()
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
                                        html.Div(
                                            ['Тип услуг'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['LLR/TR'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Год'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Квартал'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['В Market Share'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
                                        dcc.Dropdown(
                                            id="Include_in_Market_Share",
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
                                    id='Include_in_Market_Share_Div',
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
                                        html.Div(
                                            ['Адрес'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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
                                        html.Div(
                                            ['Субрынок'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
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

                                html.Div(
                                    [
                                        html.Div(
                                            ['Собственник'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
                                        dcc.Dropdown(
                                            id="Owner",
                                            # value='All agency',
                                            placeholder="Собственник",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Owner"].unique()

                                            ],
                                        )
                                    ],
                                    id='Owner_Div',
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
                                        html.Div(
                                            ['Дата приобретения'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
                                        dcc.Dropdown(
                                            id="Date_of_acquiring",
                                            # value='All agency',
                                            placeholder="Дата приобретения",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Date_of_acquiring"].unique()

                                            ],
                                        )
                                    ],
                                    id='Date_of_acquiring_Div',
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
                                        html.Div(
                                            ['Класс Colliers'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
                                        dcc.Dropdown(
                                            id="Class_Colliers",
                                            # value='All agency',
                                            placeholder="Класс Colliers",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Class_Colliers"].unique()

                                            ],
                                        )
                                    ],
                                    id='Class_Colliers_Div',
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

                                        html.Div(
                                            ['Этаж'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
                                        dcc.Dropdown(
                                            id="Floor",
                                            # value='All agency',
                                            placeholder="Этаж",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Floor"].unique()

                                            ],
                                        )
                                    ],
                                    id='Floor_Div',
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
                                        html.Div(
                                            ['Размер сделки'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),
                                        dcc.Dropdown(
                                            id="Deal_Size",
                                            # value='All agency',
                                            placeholder="Размер сделки",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Deal_Size"].unique()

                                            ],
                                        )
                                    ],
                                    id='Deal_Size_Div',
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
                                        html.Div(
                                            ['Sublease Agent'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),

                                        dcc.Dropdown(
                                            id="Sublease_Agent",
                                            # value='All agency',
                                            placeholder="Sublease Agent",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Sublease_Agent"].unique()

                                            ],
                                        )
                                    ],
                                    id='Sublease_Agent_Div',
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
                                        html.Div(
                                            ['LLR'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),

                                        dcc.Dropdown(
                                            id="LLR_Only",
                                            # value='All agency',
                                            placeholder="LLR",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["LLR_Only"].unique()

                                            ],
                                        )
                                    ],
                                    id='LLR_Only_Div',
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
                                        html.Div(
                                            ['(E)TR'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),

                                        dcc.Dropdown(
                                            id="E_TR_Only",
                                            # value='All agency',
                                            placeholder="(E)TR",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["E_TR_Only"].unique()

                                            ],
                                        )
                                    ],
                                    id='E_TR_Only_Div',
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
                                        html.Div(
                                            ['LLR/(E)TR'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),

                                        dcc.Dropdown(
                                            id="LLR/E_TR",
                                            # value='All agency',
                                            placeholder="LLR/(E)TR",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["LLR/E_TR"].unique()

                                            ],
                                        )
                                    ],
                                    id='LLR/E_TR_Div',
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
                                        html.Div(
                                            ['Месяц'],
                                            style={'color': color.colliers_grey_10,
                                                   'textAlign': 'center',
                                                   'fontSize': 14,
                                                   'backgroundColor': color.colliers_dark_blue}
                                        ),

                                        dcc.Dropdown(
                                            id="Month",
                                            # value='All agency',
                                            placeholder="Месяц",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Month"].unique()

                                            ],
                                        )
                                    ],
                                    id='Month_Div',
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
                                    min_width=1695,
                                    resizable=True,
                                    id='datatable'
                                )
                            ],
                            style={
                                'width': '100wh'
                            },
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
                                        #html.Img(id='market-graph-tab-png'),
                                        # dcc.Graph(id='all-years-horizontal'),
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
            # className='ten columns',
            id='main-div',
            style={
                'padding-left': '15px',
                'float': 'left',
                'box - sizing': 'border - box',
                'width': '88.6666666667%'
            },

        )

    ],
    style={'backgroundColor': color.colliers_grey_10,
           'margin-top': '0px'},

)

#   '''
#      Функция кнопки скрытия элементов интерфейса
#      Эта функция введена искуственно для возможности скрыть блок кода
#                                                                      '''


def interface_button():
    @app.callback(dash.dependencies.Output('interface-bar', 'style'),  # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks') # если кнопка нажата, то скрывается элемент настройки интерфейса
                   ])
    def show_bar(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            style = {
                'backgroundColor': color.colliers_pale_blue,  # цвет фона за блоком с ссылками
                'transition': 'right 0.1s',
                '-webkit-transition': 'right 0.1s',
                'width': '192px',
                # 'margin': '20 0 100 0px',
                # 'max-height': '100vh',
                'min-height': '220vh',
                # 'position': 'absolute',
                'display': 'block',
            }
        if n_clicks is not None and n_clicks % 2 != 0:
            style = {
                'transition': 'left 0.1s',
                '-webkit-transition': 'left 0.1s',
                'display': 'none'
            }
        return style

    @app.callback(dash.dependencies.Output('interface-arrow-left', 'style'), # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks') # если кнопка нажата, то элемент перемещается влево
                   ])
    def move_button(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            style = {
                'position': 'fixed',
                # элемент зафиксирован на странице и при прокрутке не меняет своё положение
                'transition': 'right 0.1s',
                '-webkit-transition': 'right 0.1s',
                'left': '194px',
                'box-shadow': '0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19',
                'display': 'inline-block',
                'max-height': '100vh',
                'min-height': '100vh',
                'width': '15px',
                # 'float': 'right',
                # 'height': '46px',
                'padding': '0 0px',
                'color': '#FFF',
                'text-align': '100vh',
                'font-size': '12px',
                'font-weight': '500',
                'line-height': '38px',
                'letter-spacing': '.001rem',
                'text-transform': 'uppercase',
                'text-decoration': 'none',
                'white-space': 'nowrap',
                'background-color': color.colliers_yellow,
                'color': color.colliers_grey_80,
                'border-radius': '0px',
                'border': '1px solid #bbb',
                'cursor': 'pointer',
                'box-sizing': 'border-box'
            }
        if n_clicks is not None and n_clicks % 2 != 0:
            style = {
                'position': 'fixed',
                # элемент зафиксирован на странице и при прокрутке не меняет своё положение
                'transition': 'left 0.1s',
                '-webkit-transition': '0.1s',
                'left': '0px',
                'box-shadow': '0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19',
                'display': 'inline-block',
                'max-height': '100vh',
                'min-height': '100vh',
                'width': '15px',
                # 'float': 'right',
                # 'height': '46px',
                'padding': '0 0px',
                'color': '#FFF',
                'text-align': '100vh',
                'font-size': '12px',
                'font-weight': '500',
                'line-height': '38px',
                'letter-spacing': '.001rem',
                'text-transform': 'uppercase',
                'text-decoration': 'none',
                'white-space': 'nowrap',
                'background-color': color.colliers_yellow,
                'color': color.colliers_grey_80,
                'border-radius': '0px',
                'border': '1px solid #bbb',
                'cursor': 'pointer',
                'box-sizing': 'border-box'
            }
        return style

    @app.callback(dash.dependencies.Output('interface-arrow-left', 'children'), # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks')  # если кнопка нажата, то '<<' сменяется на '>>'
                   ])
    def move_button(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            children = '<<'
        if n_clicks is not None and n_clicks % 2 != 0:
            children = '>>'
        return children

    @app.callback(dash.dependencies.Output('main-div', 'style'),  # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks') # если кнопка нажата, то элемент перемещается влево
                   ])
    def move_button(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            style = {
                'transition': 'right 0.2s',
                '-webkit-transition': 'right 0.2s',
                'padding-left': '15px',
                'float': 'left',
                'box - sizing': 'border - box',
                'width': '88.6666666667%'
            }
        if n_clicks is not None and n_clicks % 2 != 0:
            style = {
                'transition': 'left 0.2s',
                '-webkit-transition': 'left 0.2s',
                'padding-left': '15px',
                'float': 'left',
                'box - sizing': 'border - box',
                'width': '100%'
            }
        return style

    @app.callback(dash.dependencies.Output('datatable', 'min_width'),  # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks') # если кнопка нажата, то ширина таблицы меняется
                   ])
    def move_button(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            style = 1695
        if n_clicks is not None and n_clicks % 2 != 0:
            style = 1905
        return style


interface_button()


#   '''
#      Отображение tree-like блока со списком
#      На вход принимается значение чеклиста 'colums'
#      Если значение выбрано, то отрисовывается новый блок со списком, как в дереве
#                                                                                      '''
@app.callback(dash.dependencies.Output('interface', 'labelStyle'),  # на вход принимается значение чеклиста 'colums'
              [dash.dependencies.Input('tree-checklist', 'values') # если значение выбрано, то отрисовывается новый блок со списком, как в дереве
               ])
def show_tree(val):
    if 'Show' in val:
        children = {'display': 'block',
                    'width': '192px',
                    'margin': '0 0 0 10px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children


#   '''
#      Функция отображение выпадающих списков по значению checklist`а
#      Эта функция введена искуственно для возможности скрыть блок кода
#                                                                        '''


def select_drop_from_check():
    @app.callback(dash.dependencies.Output('Include_in_Market_Share_Div', 'style'),
                  # проверка checklist со значениями выбранных столбов в таблице
                  [dash.dependencies.Input('interface', 'values')  # при выборе столбца добавляется выпадающий список
                   ])
    def update_drop_include(val):
        try:
            if 'Include_in_Market_Share' in val:
                style_include = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }

            if 'Include_in_Market_Share' not in val:
                style_include = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_include

    @app.callback(dash.dependencies.Output('Agency_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_agency(val):
        try:
            if 'Agency' in val:
                style_agency = {'display': 'inline-block',
                                'width': '7.69%'
                                }

            if 'Agency' not in val:
                style_agency = {'display': 'none',
                                'width': '7.69%'
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_agency

    @app.callback(dash.dependencies.Output('Country_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_country(val):
        try:
            if 'Country' in val:
                style_country = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }

            if 'Country' not in val:
                style_country = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_country

    @app.callback(dash.dependencies.Output('City_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_city(val):
        try:
            if 'City' in val:
                style_city = {'display': 'inline-block',
                              'width': '7.69%'
                              }

            if 'City' not in val:
                style_city = {'display': 'none',
                              'width': '7.69%'
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_city

    @app.callback(dash.dependencies.Output('Property_name_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_property_name(val):
        try:
            if 'Property_Name' in val:
                style_property_name = {'display': 'inline-block',
                                       'width': '7.69%'
                                       }

            if 'Property_Name' not in val:
                style_property_name = {'display': 'none',
                                       'width': '7.69%'
                                       }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_property_name

    @app.callback(dash.dependencies.Output('Class_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_class(val):
        try:
            if 'Class' in val:
                style_class = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Class' not in val:
                style_class = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_class

    @app.callback(dash.dependencies.Output('SQM_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_SQM(val):
        try:
            if 'SQM' in val:
                style_SQM = {'display': 'inline-block',
                             'width': '7.69%'
                             }

            if 'SQM' not in val:
                style_SQM = {'display': 'none',
                             'width': '7.69%'
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_SQM

    @app.callback(dash.dependencies.Output('Company_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Company(val):
        try:
            if 'SQM' in val:
                style_Company = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }

            if 'SQM' not in val:
                style_Company = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Company

    @app.callback(dash.dependencies.Output('Business_Sector_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Business_Sector(val):
        try:
            if 'Business_Sector' in val:
                style_Business_Sector = {'display': 'inline-block',
                                         'width': '7.69%'
                                         }

            if 'Business_Sector' not in val:
                style_Business_Sector = {'display': 'none',
                                         'width': '7.69%'
                                         }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Business_Sector

    @app.callback(dash.dependencies.Output('Type_of_Deal_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Type_of_Deal(val):
        try:
            if 'Type_of_Deal' in val:
                style_Type_of_Deal = {'display': 'inline-block',
                                      'width': '7.69%'
                                      }

            if 'Type_of_Deal' not in val:
                style_Type_of_Deal = {'display': 'none',
                                      'width': '7.69%'
                                      }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Type_of_Deal

    @app.callback(dash.dependencies.Output('Type_of_Consultancy_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Type_of_Consultancy(val):
        try:
            if 'Type_of_Consultancy' in val:
                style_Type_of_Consultancy = {'display': 'inline-block',
                                             'width': '7.69%'
                                             }

            if 'Type_of_Consultancy' not in val:
                style_Type_of_Consultancy = {'display': 'none',
                                             'width': '7.69%'
                                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Type_of_Consultancy

    @app.callback(dash.dependencies.Output('LLR/TR_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Type_of_Consultancy(val):
        try:
            if 'LLR_TR' in val:
                style_LLR_TR = {'display': 'inline-block',
                                'width': '7.69%'
                                }

            if 'LLR_TR' not in val:
                style_LLR_TR = {'display': 'none',
                                'width': '7.69%'
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_LLR_TR

    @app.callback(dash.dependencies.Output('Year_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Year(val):
        try:
            if 'Year' in val:
                style_Year = {'display': 'inline-block',
                              'width': '7.69%'
                              }

            if 'Year' not in val:
                style_Year = {'display': 'none',
                              'width': '7.69%'
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Year

    @app.callback(dash.dependencies.Output('Quarter_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Quarter(val):
        try:
            if 'Quarter' in val:
                style_Quarter = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }
            if 'Quarter' not in val:
                style_Quarter = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Quarter

    @app.callback(dash.dependencies.Output('Address_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Address(val):
        try:
            if 'Address' in val:
                style_Addres = {'display': 'inline-block',
                                'width': '7.69%'
                                }

            if 'Address' not in val:
                style_Addres = {'display': 'none',
                                'width': '7.69%'
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Addres

    @app.callback(dash.dependencies.Output('Submarket_Large_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Submarket_large(val):
        try:
            if 'Submarket_Large' in val:
                style_Submarket_Large = {'display': 'inline-block',
                                         'width': '7.69%'
                                         }

            if 'Submarket_Large' not in val:
                style_Submarket_Large = {'display': 'none',
                                         'width': '7.69%'
                                         }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Submarket_Large

    @app.callback(dash.dependencies.Output('Owner_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Owner(val):
        try:
            if 'Owner' in val:
                style_Owner = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Owner' not in val:
                style_Owner = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Owner

    @app.callback(dash.dependencies.Output('Date_of_acquiring_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Date_of_acquiring(val):
        try:
            if 'Date_of_acquiring' in val:
                style_Date_of_acquiring = {'display': 'inline-block',
                                           'width': '7.69%'
                                           }

            if 'Date_of_acquiring' not in val:
                style_Date_of_acquiring = {'display': 'none',
                                           'width': '7.69%'
                                           }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Date_of_acquiring

    @app.callback(dash.dependencies.Output('Class_Colliers_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Class_Colliers(val):
        try:
            if 'Class_Colliers' in val:
                style_Class_Colliers = {'display': 'inline-block',
                                        'width': '7.69%'
                                        }

            if 'Class_Colliers' not in val:
                style_Class_Colliers = {'display': 'none',
                                        'width': '7.69%'
                                        }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Class_Colliers

    @app.callback(dash.dependencies.Output('Floor_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Floor(val):
        try:
            if 'Floor' in val:
                style_Floor = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Floor' not in val:
                style_Floor = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Floor

    @app.callback(dash.dependencies.Output('Deal_Size_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Deal_Size(val):
        try:
            if 'Deal_Size' in val:
                style_Deal_Size = {'display': 'inline-block',
                                   'width': '7.69%'
                                   }

            if 'Deal_Size' not in val:
                style_Deal_Size = {'display': 'none',
                                   'width': '7.69%'
                                   }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Deal_Size

    @app.callback(dash.dependencies.Output('Sublease_Agent_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Sublease_Agent(val):
        try:
            if 'Sublease_Agent' in val:
                style_Sublease_Agent = {'display': 'inline-block',
                                        'width': '7.69%'
                                        }

            if 'Sublease_Agent' not in val:
                style_Sublease_Agent = {'display': 'none',
                                        'width': '7.69%'
                                        }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Sublease_Agent

    @app.callback(dash.dependencies.Output('LLR_Only_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_LLR_Only(val):
        try:
            if 'LLR_Only' in val:
                style_LLR_Only = {'display': 'inline-block',
                                  'width': '7.69%'
                                  }

            if 'LLR_Only' not in val:
                style_LLR_Only = {'display': 'none',
                                  'width': '7.69%'
                                  }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_LLR_Only

    @app.callback(dash.dependencies.Output('E_TR_Only_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_E_TR_Only(val):
        try:
            if 'E_TR_Only' in val:
                style_E_TR_Only = {'display': 'inline-block',
                                   'width': '7.69%'
                                   }

            if 'E_TR_Only' not in val:
                style_E_TR_Only = {'display': 'none',
                                   'width': '7.69%'
                                   }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_E_TR_Only

    @app.callback(dash.dependencies.Output('LLR/E_TR_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_LLR_E_TR(val):
        try:
            if 'LLR/E_TR' in val:
                style_LLR_E_TR = {'display': 'inline-block',
                                  'width': '7.69%'
                                  }

            if 'LLR/E_TR' not in val:
                style_LLR_E_TR = {'display': 'none',
                                  'width': '7.69%'
                                  }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_LLR_E_TR

    @app.callback(dash.dependencies.Output('Month_Div', 'style'),
                  [dash.dependencies.Input('interface', 'values')
                   ])
    def update_drop_Month(val):
        try:
            if 'Month' in val:
                style_Month = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Month' not in val:
                style_Month = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Month


select_drop_from_check()  # вызов функции с отображением выпадающих списков


#   '''
#      Вывод строк таблицы
#      На вход принимается значение выпадающих списков и выбрвнных элементов в списке слева
#      На основе этих значение формируется dataframe, поещаемый в таблицу
#                                                                                      '''
@app.callback(dash.dependencies.Output('datatable', 'rows'),# здесь на вход принимается значение значение выпадающих списков и на основе этих значение формируется dataframe, поещаемый в таблицу
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
               dash.dependencies.Input('Include_in_Market_Share', 'value'),
               dash.dependencies.Input('Address', 'value'),
               dash.dependencies.Input('Submarket_Large', 'value'),
               dash.dependencies.Input('Owner', 'value'),
               dash.dependencies.Input('Date_of_acquiring', 'value'),
               dash.dependencies.Input('Class_Colliers', 'value'),
               dash.dependencies.Input('Floor', 'value'),
               dash.dependencies.Input('Deal_Size', 'value'),
               dash.dependencies.Input('Sublease_Agent', 'value'),
               dash.dependencies.Input('LLR_Only', 'value'),
               dash.dependencies.Input('E_TR_Only', 'value'),
               dash.dependencies.Input('LLR/E_TR', 'value'),
               dash.dependencies.Input('Month', 'value'),
               dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
               ])
def update_datatable(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                     Owner,
                     Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only, LLR_E_TR,
                     Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency], # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()  # копия словаря
    list_of_values_copy = list(filter(None,
                                      list_of_values))  # очистка кортежа от пустых элементов (при не выбранном значении value, значение по умолчанию = None

    if len(list_of_values_copy) == 0 or (Year is not None and Year[0] == 'All years'):
        return all_deals_query_df[col].to_dict('records')
    # ____________________________________________________________#

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
        return data[col].to_dict('records')

#   '''
#      подсчёт суммы по отфильтрованным данным
#                                              '''

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
               dash.dependencies.Input('Company', 'value'),
               dash.dependencies.Input('Include_in_Market_Share', 'value'),
               dash.dependencies.Input('Address', 'value'),
               dash.dependencies.Input('Submarket_Large', 'value'),
               dash.dependencies.Input('Owner', 'value'),
               dash.dependencies.Input('Date_of_acquiring', 'value'),
               dash.dependencies.Input('Class_Colliers', 'value'),
               dash.dependencies.Input('Floor', 'value'),
               dash.dependencies.Input('Deal_Size', 'value'),
               dash.dependencies.Input('Sublease_Agent', 'value'),
               dash.dependencies.Input('LLR_Only', 'value'),
               dash.dependencies.Input('E_TR_Only', 'value'),
               dash.dependencies.Input('LLR/E_TR', 'value'),
               dash.dependencies.Input('Month', 'value'),
               dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
               ])
def update_sum(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
               Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large, Owner,
               Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only, LLR_E_TR,
               Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])
    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()

    list_of_values_copy = list(filter(None, list_of_values))

    if len(list_of_values_copy) == 0 or (Year is not None and Year[0] == 'All years'):
        data_sum = int(round(all_deals_query_df["SQM"].sum()))
        sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')    # форматирование отображения разрядов числа, на место запятой ставится пробел
        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'

    # ____________________________________________________________#

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
                data_sum = int(round(data["SQM"].sum()))
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
                data_sum = int(round(data["SQM"].sum()))
            sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')    # форматирование отображения разрядов числа, на место запятой ставится пробел
        return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м'


#   '''
#      скачивание csv файла с дампом всей базы данных по сделкам
#                                                                 '''
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
               ]
              )
def update_download_all_link(Year, Country, Agency, City, Property_name, Class, SQM, Business_Sector, Type_of_Deal,
                             Type_of_Consultancy, Quarter, Company):
    csv_string = all_deals_query_df.to_csv(index=False, encoding='utf-8', sep=';')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string


#   '''
#      скачивание csv файла с выбранными даннымы
#                                                 '''


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
     dash.dependencies.Input('Company', 'value'),
     dash.dependencies.Input('Include_in_Market_Share', 'value'),
     dash.dependencies.Input('Address', 'value'),
     dash.dependencies.Input('Submarket_Large', 'value'),
     dash.dependencies.Input('Owner', 'value'),
     dash.dependencies.Input('Date_of_acquiring', 'value'),
     dash.dependencies.Input('Class_Colliers', 'value'),
     dash.dependencies.Input('Floor', 'value'),
     dash.dependencies.Input('Deal_Size', 'value'),
     dash.dependencies.Input('Sublease_Agent', 'value'),
     dash.dependencies.Input('LLR_Only', 'value'),
     dash.dependencies.Input('E_TR_Only', 'value'),
     dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_download_link(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                         Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address,
                         Submarket_Large, Owner,
                         Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                         LLR_E_TR,
                         Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()

    list_of_values_copy = list(filter(None, list_of_values))

    if len(list_of_values_copy) == 0:
        return all_deals_query_df.to_dict('records')

    # ____________________________________________________________#

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
        csv_string = data.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string


# '''
#     Начало блока по отрисовке графиков
#     Callback`и, отрисовывающие графики, принимают на вход данные выпающих списков.
#     График принимает те же переменные, как и таблица, сначала фильтруется датафрейм по выбранным данным,
#     после этот датафрейм переводится в сводную таблицу в pandas и по значениям сводной таблицы строится график.
#                                                                                                                 '''


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
     dash.dependencies.Input('Company', 'value'),
     dash.dependencies.Input('Include_in_Market_Share', 'value'),
     dash.dependencies.Input('Address', 'value'),
     dash.dependencies.Input('Submarket_Large', 'value'),
     dash.dependencies.Input('Owner', 'value'),
     dash.dependencies.Input('Date_of_acquiring', 'value'),
     dash.dependencies.Input('Class_Colliers', 'value'),
     dash.dependencies.Input('Floor', 'value'),
     dash.dependencies.Input('Deal_Size', 'value'),
     dash.dependencies.Input('Sublease_Agent', 'value'),
     dash.dependencies.Input('LLR_Only', 'value'),
     dash.dependencies.Input('E_TR_Only', 'value'),
     dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_graph_tab(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                     Owner,
                     Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only, LLR_E_TR,
                     Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = all_deals_query_df.copy()
    except TypeError:
        df_plot = all_deals_query_df.copy()
    except IndexError:
        df_plot = all_deals_query_df.copy()
    # __________________________________________________________________________________________________ #

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            df_plot = data

    pv = pd.pivot_table(         # создание сводной таблицы из текущего датафрейма
        df_plot,                 # выбор текущего датафрейма
        index=['Year'],          # выбор индекса ("строки" в Excel Pivot Tables)
        columns=['Agency'],      # выбор столбцов ("столбцы" в Excel Pivot Tables)
        values=["SQM"],          # выбор подсчитываемого значения ("значения" в Excel Pivot Tables)
        aggfunc=sum,             # параметр поля значения (суммаб кол-влб среднее итд)
        fill_value=0)            # заполнение пустых ячеек

    width = 700
    height = 500

    if len(df_plot['Agency'].unique()) == 6:
        data = []

        trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
                        name='Colliers',
                        marker=dict(
                            color=color.colliers_dark_blue),
                        width=0.4,
                        text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
                        textposition='inside',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                        name='CW',
                        marker=dict(
                            color=color.colliers_extra_light_blue),
                        width=0.4,
                        text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
                        textposition='inside',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
                        name='CBRE',
                        marker=dict(
                            color=color.colliers_grey_40),
                        width=0.4,
                        text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
                        textposition='inside',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
                        name='JLL',
                        marker=dict(
                            color=color.colliers_yellow),
                        width=0.4,
                        text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
                        textposition='inside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12))

        trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
                        name='KF',
                        marker=dict(
                            color=color.colliers_red),
                        width=0.4,
                        text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
                        textposition='inside',
                        textfont=dict(
                            color=color.white,
                            size=12))

        trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
                        name='SAR',
                        marker=dict(
                            color=color.colliers_light_blue),
                        width=0.4,
                        text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
                        textposition='inside',
                        textfont=dict(
                            color=color.white,
                            size=12))


        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])

    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        list_of_unique = df_plot['Agency'].unique()
        if 'Colliers' in list_of_unique:
            trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
                            name='Colliers',
                            marker=dict(
                                color=color.colliers_dark_blue),
                            width=0.4,
                            text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace1)



        if 'CW' in list_of_unique:
            trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                            name='CW',
                            marker=dict(
                                color=color.colliers_extra_light_blue),
                            width=0.4,
                            text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace2)

        if 'CBRE' in list_of_unique:
            trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
                            name='CBRE',
                            marker=dict(
                                color=color.colliers_grey_40),
                            width=0.4,
                            text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace3)

        if 'JLL' in list_of_unique:
            trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
                            name='JLL',
                            marker=dict(
                                color=color.colliers_yellow),
                            width=0.4,
                            text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.colliers_grey_80,
                                size=12))
            data.append(trace4)

        if 'KF' in list_of_unique:
            trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
                            name='KF',
                            marker=dict(
                                color=color.colliers_red),
                            width=0.4,
                            text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
                            textposition='inside',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace5)

            if 'SAR' in list_of_unique:
                trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
                                name='SAR',
                                marker=dict(
                                    color=color.colliers_light_blue),
                                width=0.4,
                                text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
                                textposition='inside',
                                textfont=dict(
                                    color=color.white,
                                    size=12))

            data.append(trace6)

    # '''
    #     Формирование строки для подписи графика
    #     Сначала создаётся лист со значениями выбранных индексов для фильтрации
    #     Если парметры не выбраны, то выводится 'All deals' и 'All years'
    #     Если парметры выбраны, и не указан год, то выводятся элементы списка значений
    #     выбранных параметров и 'All years'
    #     Если парметры выбраны и указан год, то выводятся элементы списка значений
    #     выбранных параметров и элементы списка 'Year'
    #                                                                                    '''

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = 'All years'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = 'all years'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    return {
        'data': data,
        'layout':
            go.Layout(
                title='{}<br>'
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
                    #title='Years'
                ),
                yaxis={'title': 'Area in sq.m'},
                legend=dict(orientation="h",
                            traceorder="normal"),
                barmode='stack')
    }


'''
    Начало блока по отрисовке статических изображений
    Код закомментирован до обсуждения
                                                       '''
# @app.callback(
#     dash.dependencies.Output('market-graph-tab-png', 'src'),
#     [dash.dependencies.Input('Year', 'value'),
#      dash.dependencies.Input('Country', 'value'),
#      dash.dependencies.Input('Agency', 'value'),
#      dash.dependencies.Input('City', 'value'),
#      dash.dependencies.Input('Property_name', 'value'),
#      dash.dependencies.Input('Class', 'value'),
#      dash.dependencies.Input('SQM', 'value'),
#      dash.dependencies.Input('Business_Sector', 'value'),
#      dash.dependencies.Input('Type_of_Deal', 'value'),
#      dash.dependencies.Input('Type_of_Consultancy', 'value'),
#      dash.dependencies.Input('LLR/TR', 'value'),
#      dash.dependencies.Input('Quarter', 'value'),
#      dash.dependencies.Input('Company', 'value'),
#      dash.dependencies.Input('Include_in_Market_Share', 'value'),
#      dash.dependencies.Input('Address', 'value'),
#      dash.dependencies.Input('Submarket_Large', 'value'),
#      dash.dependencies.Input('Owner', 'value'),
#      dash.dependencies.Input('Date_of_acquiring', 'value'),
#      dash.dependencies.Input('Class_Colliers', 'value'),
#      dash.dependencies.Input('Floor', 'value'),
#      dash.dependencies.Input('Deal_Size', 'value'),
#      dash.dependencies.Input('Sublease_Agent', 'value'),
#      dash.dependencies.Input('LLR_Only', 'value'),
#      dash.dependencies.Input('E_TR_Only', 'value'),
#      dash.dependencies.Input('LLR/E_TR', 'value'),
#      dash.dependencies.Input('Month', 'value'),
#      dash.dependencies.Input('interface', 'values'),  # значение чеклиста из дерева с выбором столбцов
#      #dash.dependencies.Input('interval-component', 'n_intervals')
#      ])
# def update_graph_tab_pic(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
#                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large, Owner,
#                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only, LLR_E_TR,
#                      Month, col):
#     cond = dict(Year=[Year], Country=[Country], Agency=[Agency],                  # создание словаря с ключом - названием столбца, значением - выбранным параметрам
#                 City=[City], Property_Name=[Property_Name], Class=[Class],
#                 SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
#                 Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
#                 Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
#                 Submarket_Large=[Submarket_Large],
#                 Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
#                 Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
#                 LLR_E_TR=[LLR_E_TR], Month=[Month])
#
#     list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
#                       Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large, Owner,
#                       Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
#                       LLR_E_TR,
#                       Month)
#     cond_1 = cond.copy()
#     list_of_values_copy = list(filter(None, list_of_values))
#
#     try:
#         if len(list_of_values_copy) == 0:
#             df_plot = all_deals_query_df.copy()
#     except TypeError:
#         df_plot = all_deals_query_df.copy()
#     except IndexError:
#         df_plot = all_deals_query_df.copy()
#     # __________________________________________________________________________________________________ #
#
#     if len(list_of_values_copy) != 0:
#         for i in range(len(list_of_values_copy)):
#             ind = get_key(cond_1, [list_of_values_copy[i]])
#             if i == 0:
#                 data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
#             else:
#                 data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
#             df_plot = data
#
#     pv = pd.pivot_table(  # создание сводной таблицы из текущего датафрейма
#         df_plot,  # выбор текущего датафрейма
#         index=['Year'],  # выбор индекса ("строки" в Excel Pivot Tables)
#         columns=['Agency'],  # выбор столбцов ("столбцы" в Excel Pivot Tables)
#         values=["SQM"],  # выбор подсчитываемого значения ("значения" в Excel Pivot Tables)
#         aggfunc=sum,  # параметр поля значения (суммаб кол-влб среднее итд)
#         fill_value=0)  # заполнение пустых ячеек
#
#     width = 650
#     height = 450
#
#     if len(df_plot['Agency'].unique()) == 6:
#         data = []
#
#         trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
#                         name='Colliers',
#                         marker=dict(
#                             color=color.colliers_dark_blue),
#                         width=0.4,
#                         text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
#                         textposition='inside',
#                         textfont=dict(
#                             color=color.white,
#                             size=12))
#         trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
#                         name='CW',
#                         marker=dict(
#                             color=color.colliers_extra_light_blue),
#                         width=0.4,
#                         text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
#                         textposition='inside',
#                         textfont=dict(
#                             color=color.white,
#                             size=12))
#         trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
#                         name='CBRE',
#                         marker=dict(
#                             color=color.colliers_grey_40),
#                         width=0.4,
#                         text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
#                         textposition='inside',
#                         textfont=dict(
#                             color=color.white,
#                             size=12))
#         trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
#                         name='JLL',
#                         marker=dict(
#                             color=color.colliers_yellow),
#                         width=0.4,
#                         text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
#                         textposition='inside',
#                         textfont=dict(
#                             color=color.colliers_grey_80,
#                             size=12))
#
#         trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
#                         name='KF',
#                         marker=dict(
#                             color=color.colliers_red),
#                         width=0.4,
#                         text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
#                         textposition='inside',
#                         textfont=dict(
#                             color=color.white,
#                             size=12))
#
#         trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
#                         name='SAR',
#                         marker=dict(
#                             color=color.colliers_light_blue),
#                         width=0.4,
#                         text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
#                         textposition='inside',
#                         textfont=dict(
#                             color=color.white,
#                             size=12))
#
#         data.extend([trace1, trace2, trace3, trace4, trace5, trace6])
#
#     elif len(df_plot['Agency'].unique()) < 6:
#         data = []
#         list_of_unique = df_plot['Agency'].unique()
#         if 'Colliers' in list_of_unique:
#             trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
#                             name='Colliers',
#                             marker=dict(
#                                 color=color.colliers_dark_blue),
#                             width=0.4,
#                             text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
#                             textposition='inside',
#                             textfont=dict(
#                                 color=color.white,
#                                 size=12))
#             data.append(trace1)
#
#         if 'CW' in list_of_unique:
#             trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
#                             name='CW',
#                             marker=dict(
#                                 color=color.colliers_extra_light_blue),
#                             width=0.4,
#                             text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
#                             textposition='inside',
#                             textfont=dict(
#                                 color=color.white,
#                                 size=12))
#             data.append(trace2)
#
#         if 'CBRE' in list_of_unique:
#             trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
#                             name='CBRE',
#                             marker=dict(
#                                 color=color.colliers_grey_40),
#                             width=0.4,
#                             text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
#                             textposition='inside',
#                             textfont=dict(
#                                 color=color.white,
#                                 size=12))
#             data.append(trace3)
#
#         if 'JLL' in list_of_unique:
#             trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
#                             name='JLL',
#                             marker=dict(
#                                 color=color.colliers_yellow),
#                             width=0.4,
#                             text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
#                             textposition='inside',
#                             textfont=dict(
#                                 color=color.colliers_grey_80,
#                                 size=12))
#             data.append(trace4)
#
#         if 'KF' in list_of_unique:
#             trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
#                             name='KF',
#                             marker=dict(
#                                 color=color.colliers_red),
#                             width=0.4,
#                             text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
#                             textposition='inside',
#                             textfont=dict(
#                                 color=color.white,
#                                 size=12))
#             data.append(trace5)
#
#             if 'SAR' in list_of_unique:
#                 trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
#                                 name='SAR',
#                                 marker=dict(
#                                     color=color.colliers_light_blue),
#                                 width=0.4,
#                                 text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
#                                 textposition='inside',
#                                 textfont=dict(
#                                     color=color.white,
#                                     size=12))
#
#             data.append(trace6)
#
#     # '''
#     #     Формирование строки для подписи графика
#     #     Сначала создаётся лист со значениями выбранных индексов для фильтрации
#     #     Если парметры не выбраны, то выводится 'All deals' и 'All years'
#     #     Если парметры выбраны, и не указан год, то выводятся элементы списка значений
#     #     выбранных параметров и 'All years'
#     #     Если парметры выбраны и указан год, то выводятся элементы списка значений
#     #     выбранных параметров и элементы списка 'Year'
#     #                                                                                    '''
#
#     list_of_ind = []
#     for i in range(len(list_of_values_copy)):
#         ind = get_key(cond_1, [list_of_values_copy[i]])
#         list_of_ind.append(ind)
#
#     if len(list_of_values_copy) == 0:
#         format_data = 'All deals'
#         format_year = 'All years'
#
#     if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
#         list_of_values_copy_chain = list(chain(*list_of_values_copy))
#         format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
#         format_year = 'all years'
#
#     if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
#         list_of_values_copy_chain = list(chain(*list_of_values_copy))
#         for i in Year:
#             list_of_values_copy_chain.remove('{}'.format(i))
#         format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
#         format_year = ', '.join(Year)
#
#     image_data = {
#         'data': data,
#         'layout':
#             go.Layout(
#                 title='{}<br>'
#                       'in {}'.format(format_data, format_year),
#                 autosize=False,
#                 bargap=0.3,
#                 bargroupgap=0,
#                 font=dict(
#                     color=color.colliers_grey_80,
#                     family='Arial',
#                     size=12),
#                 width=width,
#                 height=height,
#                 margin=dict(pad=0),
#                 titlefont=dict(
#                     color=color.colliers_grey_80,
#                     family='Arial',
#                     size=18),
#                 xaxis=dict(
#                     exponentformat=False,
#                     autorange=True,
#                     showgrid=True,
#                     zeroline=True,
#                     showline=True,
#                     autotick=False,
#                     ticks='',
#                     showticklabels=True,
#                     #title='Years'
#                 ),
#                 yaxis={'title': 'Area in sq.m'},
#                 legend=dict(orientation="h",
#                             traceorder="normal"),
#                 barmode='stack')
#     }
#
#     img = py.image.get(image_data, format='png')
#     #print('Data loaded from Plotly')
#     #plot_url = py.plot(image_data, filename='my plot', auto_open=False)
#     #print(plot_url)
#     #plot_url_png = plot_url + '.png'
#     #print(plot_url_png)
#
#     plot_bytes_encode = str(base64.b64encode(img))
#     plot_bytes_encode = plot_bytes_encode[0:-1]
#     plot_bytes_encode_fin = plot_bytes_encode[2:]
#     stringpic = "data:image/png;base64," + plot_bytes_encode_fin   # строчка с байткодом картинки
#     #stringpic = plot_url_png                # строчка с сылкой на файл картинки на сайте плотли
#
#     return stringpic


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
     dash.dependencies.Input('Company', 'value'),
     dash.dependencies.Input('Include_in_Market_Share', 'value'),
     dash.dependencies.Input('Address', 'value'),
     dash.dependencies.Input('Submarket_Large', 'value'),
     dash.dependencies.Input('Owner', 'value'),
     dash.dependencies.Input('Date_of_acquiring', 'value'),
     dash.dependencies.Input('Class_Colliers', 'value'),
     dash.dependencies.Input('Floor', 'value'),
     dash.dependencies.Input('Deal_Size', 'value'),
     dash.dependencies.Input('Sublease_Agent', 'value'),
     dash.dependencies.Input('LLR_Only', 'value'),
     dash.dependencies.Input('E_TR_Only', 'value'),
     dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_graph_tab_none_stack(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                                Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address,
                                Submarket_Large, Owner,
                                Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only,
                                E_TR_Only, LLR_E_TR,
                                Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = all_deals_query_df.copy()
    except TypeError:
        df_plot = all_deals_query_df.copy()
    except IndexError:
        df_plot = all_deals_query_df.copy()

    # __________________________________________________________________________________________________ #

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            df_plot = data

    pv = pd.pivot_table(
        df_plot,
        index=['Year'],
        columns=['Agency'],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    width = 700
    height = 500

    if len(df_plot['Agency'].unique()) == 6:
        data = []

        trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
                        name='Colliers',
                        marker=dict(
                            color=color.colliers_dark_blue),
                        width=0.4,
                        #text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
                        textposition='outside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12))

        trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                        name='CW',
                        marker=dict(
                            color=color.colliers_extra_light_blue),
                        width=0.4,
                        #text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
                        textposition='outside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12)
                        )
        trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
                        name='CBRE',
                        marker=dict(
                            color=color.colliers_grey_40),
                        width=0.4,
                        #text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
                        textposition='outside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12)
                        )
        trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
                        name='JLL',
                        marker=dict(
                            color=color.colliers_yellow),
                        width=0.4,
                        #text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
                        textposition='outside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12)
                        )
        trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
                        name='KF',
                        marker=dict(
                            color=color.colliers_red),
                        width=0.4,
                        #text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
                        textposition='outside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12)
                        )
        trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
                        name='SAR',
                        marker=dict(
                            color=color.colliers_light_blue),
                        width=0.4,
                        #text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
                        textposition='outside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12)
                        )

        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])

    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        list_of_unique = df_plot['Agency'].unique()
        if 'Colliers' in list_of_unique:
            trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
                            name='Colliers',
                            marker=dict(
                                color=color.colliers_dark_blue),
                            width=0.4,
                            text=pv[("SQM", 'Colliers')])
            data.append(trace1)


        if 'CW' in list_of_unique:
            trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                            name='CW',
                            marker=dict(
                                color=color.colliers_extra_light_blue),
                            width=0.4)
            data.append(trace2)

        if 'CBRE' in list_of_unique:
            trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
                            name='CBRE',
                            marker=dict(
                                color=color.colliers_grey_40),
                            width=0.4)
            data.append(trace3)

        if 'JLL' in list_of_unique:
            trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
                            name='JLL',
                            marker=dict(
                                color=color.colliers_yellow),
                            width=0.4)
            data.append(trace4)

        if 'KF' in list_of_unique:
            trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
                            name='KF',
                            marker=dict(
                                color=color.colliers_red),
                            width=0.4)
            data.append(trace5)

        if 'SAR' in list_of_unique:
            trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
                            name='SAR',
                            marker=dict(
                                color=color.colliers_light_blue),
                            width=0.4)
            data.append(trace6)

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = 'All years'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = 'all years'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    return {
        'data': data,
        'layout':
            go.Layout(
                title='{}<br>'
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
                    #title='Years'
                ),
                yaxis={'title': 'Area in sq.m'},
                legend=dict(orientation="h",
                            traceorder="normal"),
                # barmode='stack'
            )
    }


@app.callback(
    dash.dependencies.Output('market-graph-horizontal-tab', 'figure'),
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
     dash.dependencies.Input('Include_in_Market_Share', 'value'),
     dash.dependencies.Input('Address', 'value'),
     dash.dependencies.Input('Submarket_Large', 'value'),
     dash.dependencies.Input('Owner', 'value'),
     dash.dependencies.Input('Date_of_acquiring', 'value'),
     dash.dependencies.Input('Class_Colliers', 'value'),
     dash.dependencies.Input('Floor', 'value'),
     dash.dependencies.Input('Deal_Size', 'value'),
     dash.dependencies.Input('Sublease_Agent', 'value'),
     dash.dependencies.Input('LLR_Only', 'value'),
     dash.dependencies.Input('E_TR_Only', 'value'),
     dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_graph_horizontal(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                            Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address,
                            Submarket_Large, Owner,
                            Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                            LLR_E_TR,
                            Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = all_deals_query_df.copy()
    except TypeError:
        df_plot = all_deals_query_df.copy()
    except IndexError:
        df_plot = all_deals_query_df.copy()
    # __________________________________________________________________________________________________ #

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            df_plot = data

    width = 700
    height = 500

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    if len(df_plot['Agency'].unique()) == 6:
        data = []

        trace1 = go.Bar(y=pv.index, x=pv[("SQM", 'Colliers')],
                        name='Colliers',
                        marker=dict(
                            color=color.colliers_dark_blue),
                        width=0.45,
                        orientation='h',
                        text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
                        textposition='auto',
                        textfont=dict(
                            color=color.white,
                            size=14))
        trace2 = go.Bar(y=pv.index, x=pv[("SQM", 'SAR')],
                        name='SAR',
                        marker=dict(
                            color=color.colliers_light_blue),
                        width=0.45,
                        orientation='h',
                        text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
                        textposition='auto',
                        textfont=dict(
                            color=color.white,
                            size=14))
        trace3 = go.Bar(y=pv.index, x=pv[("SQM", 'CW')],
                        name='CW',
                        marker=dict(
                            color=color.colliers_extra_light_blue),
                        width=0.45, orientation='h',
                        text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
                        textposition='auto',
                        textfont=dict(
                            color=color.white,
                            size=14))
        trace4 = go.Bar(y=pv.index, x=pv[("SQM", 'CBRE')],
                        name='CBRE',
                        marker=dict(
                            color=color.colliers_grey_40),
                        width=0.45,
                        orientation='h',
                        text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
                        textposition='auto',
                        textfont=dict(
                            color=color.white,
                            size=14))
        trace5 = go.Bar(y=pv.index, x=pv[("SQM", 'JLL')],
                        name='JLL',
                        marker=dict(
                            color=color.colliers_yellow),
                        width=0.45,
                        orientation='h',
                        text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
                        textposition='auto',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=14))
        trace6 = go.Bar(y=pv.index, x=pv[("SQM", 'KF')],
                        name='KF',
                        marker=dict(
                            color=color.colliers_red),
                        width=0.45,
                        orientation='h',
                        text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
                        textposition='auto',
                        textfont=dict(
                            color=color.white,
                            size=14))

        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])

    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        list_of_unique = df_plot['Agency'].unique()
        if 'Colliers' in list_of_unique:
            trace1 = go.Bar(y=pv.index, x=pv[("SQM", 'Colliers')],
                            name='Colliers',
                            marker=dict(
                                color=color.colliers_dark_blue),
                            width=0.4,
                            orientation='h',
                            text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace1)

        if 'SAR' in list_of_unique:
            trace2 = go.Bar(y=pv.index, x=pv[("SQM", 'SAR')],
                            name='SAR',
                            marker=dict(
                                color=color.colliers_light_blue),
                            width=0.4,
                            orientation='h',
                            text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace2)

        if 'CW' in list_of_unique:
            trace3 = go.Bar(y=pv.index, x=pv[("SQM", 'CW')],
                            name='CW',
                            marker=dict(
                                color=color.colliers_extra_light_blue),
                            width=0.4,
                            orientation='h',
                            text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace3)

        if 'CBRE' in list_of_unique:
            trace4 = go.Bar(y=pv.index, x=pv[("SQM", 'CBRE')],
                            name='CBRE',
                            marker=dict(
                                color=color.colliers_grey_40),
                            width=0.4,
                            orientation='h',
                            text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
                            textposition='auto',
                            textfont=dict(color=color.white,
                                          size=12))
            data.append(trace4)

        if 'JLL' in list_of_unique:
            trace5 = go.Bar(y=pv.index, x=pv[("SQM", 'JLL')],
                            name='JLL',
                            marker=dict(
                                color=color.colliers_yellow),
                            width=0.4,
                            orientation='h',
                            text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
                            textposition='auto',
                            textfont=dict(
                                color=color.colliers_grey_80,
                                size=12))
            data.append(trace5)

        if 'KF' in list_of_unique:
            trace6 = go.Bar(y=pv.index, x=pv[("SQM", 'KF')],
                            name='KF',
                            marker=dict(
                                color=color.colliers_red),
                            width=0.4,
                            orientation='h',
                            text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12,
                                autosize=False))
            data.append(trace6)

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = 'All years'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = 'all years'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    return {
        'data': data,
        'layout':

            go.Layout(
                annotations=[dict(
                    x=pv["SQM"].sum(),
                    y=pv.index,
                    showarrow=False,
                    text=' ',
                    xref="x",
                    yref="y")],
                title='{}<br>'
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
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=True,
                    ticks='',
                    showticklabels=True,
                    #title='Area in sq.m'
                ),
                yaxis=dict(autorange=True,
                           showgrid=True,
                           zeroline=True,
                           showline=True,
                           autotick=False,
                           ticks='',
                           showticklabels=True,
                           #title='Year'
                           ),
                legend=dict(orientation="h",
                            traceorder='normal'),

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
     dash.dependencies.Input('Company', 'value'),
     dash.dependencies.Input('Include_in_Market_Share', 'value'),
     dash.dependencies.Input('Address', 'value'),
     dash.dependencies.Input('Submarket_Large', 'value'),
     dash.dependencies.Input('Owner', 'value'),
     dash.dependencies.Input('Date_of_acquiring', 'value'),
     dash.dependencies.Input('Class_Colliers', 'value'),
     dash.dependencies.Input('Floor', 'value'),
     dash.dependencies.Input('Deal_Size', 'value'),
     dash.dependencies.Input('Sublease_Agent', 'value'),
     dash.dependencies.Input('LLR_Only', 'value'),
     dash.dependencies.Input('E_TR_Only', 'value'),
     dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_pie_graph(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                     Owner,
                     Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only, LLR_E_TR,
                     Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = all_deals_query_df.copy()
    except TypeError:
        df_plot = all_deals_query_df.copy()
    except IndexError:
        df_plot = all_deals_query_df.copy()
    # __________________________________________________________________________________________________ #

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            df_plot = data

    width = 700
    height = 500

    pv = pd.pivot_table(
        df_plot,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    colors_pie = [ color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_grey_40,
                  color.colliers_yellow, color.colliers_red, color.colliers_light_blue]
    pie1 = go.Pie(values=pv["SQM"],
                  labels=['Colliers', 'CW', 'CBRE', 'JLL', 'KF', 'SAR'],
                  hoverinfo='label+value+percent',
                  textinfo='label+percent',
                  textposition='outside',
                  textfont=dict(
                      color=colors_pie,
                      size=12),
                  marker=dict(colors=colors_pie,
                              line=dict(
                                  color=color.white,
                                  width=1
                              )
                              )
                  )

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = 'All years'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = 'all years'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    return {
        'data': [pie1],
        'layout': go.Layout(
            title='{}<br>'
                  'in {}'.format(format_data, format_year),
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


@app.callback(
    dash.dependencies.Output('market-graph-percent-tab', 'figure'),
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
     dash.dependencies.Input('Include_in_Market_Share', 'value'),
     dash.dependencies.Input('Address', 'value'),
     dash.dependencies.Input('Submarket_Large', 'value'),
     dash.dependencies.Input('Owner', 'value'),
     dash.dependencies.Input('Date_of_acquiring', 'value'),
     dash.dependencies.Input('Class_Colliers', 'value'),
     dash.dependencies.Input('Floor', 'value'),
     dash.dependencies.Input('Deal_Size', 'value'),
     dash.dependencies.Input('Sublease_Agent', 'value'),
     dash.dependencies.Input('LLR_Only', 'value'),
     dash.dependencies.Input('E_TR_Only', 'value'),
     dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_graph_percent(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                         Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address,
                         Submarket_Large, Owner,
                         Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                         LLR_E_TR,
                         Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = all_deals_query_df.copy()
    except TypeError:
        df_plot = all_deals_query_df.copy()
    except IndexError:
        df_plot = all_deals_query_df.copy()
    # __________________________________________________________________________________________________ #

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            df_plot = data

    width = 700
    height = 500

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

    # из исходного датафрейма с real получить список из str, причем каждыому элементу добавить знак процента
    # чтобы отбросить 0 перевожу в интеджер, потом в строку, к строке + %, эту историю из строки обратно в список
    trace1 = go.Bar(x=pv1.index, y=pv1[("SQM", 'Colliers')] * 100 / pv2["SQM"].sum(),
                    name='Colliers',
                    marker=dict(
                        color=color.colliers_dark_blue),
                    width=0.4,
                    text=(
                        list(map(lambda x: str(x) + "%",
                                 list(((pv1[("SQM", 'Colliers')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(np.int64))))),
                    textposition='auto',
                    textfont=dict(
                        color=color.white,
                        size=12))

    trace2 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum(),
                    name='CW',
                    marker=dict(
                        color=color.colliers_extra_light_blue),
                    width=0.4,
                    text=(
                        list(map(lambda x: str(x) + "%",
                                 list(((pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(np.int64))))),
                    textposition='auto',
                    textfont=dict(
                        color=color.white,
                        size=12))
    trace3 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum(),
                    name='CBRE',
                    marker=dict(
                        color=color.colliers_grey_40),
                    width=0.4,
                    text=(
                        list(map(lambda x: str(x) + "%",
                                 list(((pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(np.int64))))),
                    textposition='auto',
                    textfont=dict(
                        color=color.white,
                        size=12))
    trace4 = go.Bar(x=pv1.index, y=pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum(),
                    name='JLL',
                    marker=dict(
                        color=color.colliers_yellow),
                    width=0.4,
                    text=(
                        list(map(lambda x: str(x) + "%",
                                 list(((pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(np.int64))))),
                    textposition='auto',
                    textfont=dict(
                        color=color.colliers_grey_80,
                        size=12))
    trace5 = go.Bar(x=pv1.index, y=pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum(),
                    name='KF',
                    marker=dict(
                        color=color.colliers_red),
                    width=0.4,
                    text=(
                        list(map(lambda x: str(x) + "%",
                                 list(((pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(np.int64))))),
                    textposition='auto',
                    textfont=dict(
                        color=color.white,
                        size=12))

    trace6 = go.Bar(x=pv1.index, y=pv1[("SQM", 'SAR')] * 100 / pv2["SQM"].sum(),
                    name='SAR',
                    marker=dict(
                        color=color.colliers_light_blue),
                    width=0.4,
                    text=(
                        list(map(lambda x: str(x) + "%",
                                 list(((pv1[("SQM", 'SAR')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(np.int64))))),
                    textposition='auto',
                    textfont=dict(
                        color=color.white,
                        size=12))

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = 'All years'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = 'all years'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)



    annotations = []





    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='{}<br>'
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
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=False,
                    ticks='',
                    showticklabels=True,
                    #title='Years'
                ),
                yaxis=dict(ticksuffix='%',
                          ),
                barmode='stack',
                legend=dict(orientation="h",
                            traceorder='normal')
            )
    }


@app.callback(
    dash.dependencies.Output('market-graph-horizontal-total-tab', 'figure'),
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
     dash.dependencies.Input('Include_in_Market_Share', 'value'),
     dash.dependencies.Input('Address', 'value'),
     dash.dependencies.Input('Submarket_Large', 'value'),
     dash.dependencies.Input('Owner', 'value'),
     dash.dependencies.Input('Date_of_acquiring', 'value'),
     dash.dependencies.Input('Class_Colliers', 'value'),
     dash.dependencies.Input('Floor', 'value'),
     dash.dependencies.Input('Deal_Size', 'value'),
     dash.dependencies.Input('Sublease_Agent', 'value'),
     dash.dependencies.Input('LLR_Only', 'value'),
     dash.dependencies.Input('E_TR_Only', 'value'),
     dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface', 'values')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_graph_horizontal_total(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                                  Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address,
                                  Submarket_Large, Owner,
                                  Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only,
                                  E_TR_Only, LLR_E_TR,
                                  Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    try:
        if len(list_of_values_copy) == 0:
            df_plot = all_deals_query_df.copy()
    except TypeError:
        df_plot = all_deals_query_df.copy()
    except IndexError:
        df_plot = all_deals_query_df.copy()
    # __________________________________________________________________________________________________ #

    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = all_deals_query_df[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            else:
                data = data[(all_deals_query_df[ind].isin(list_of_values_copy[i]))]
            df_plot = data

    width = 700
    height = 500

    pv = pd.pivot_table(
        df_plot,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    print(pv['SQM'].sum())
    pv_sorted = pv.sort_values(by='SQM', ascending=True)
    print((list(map(lambda x: x, list((pv_sorted[("SQM")] / 1000).apply(np.int64))))))
    trace2 = go.Bar(x=pv_sorted["SQM"] / 100000,
                    y=pv_sorted.index,
                    marker=dict(
                        color=[color.sar_color, color.colliers_color, color.kf_color, color.cw_color, color.cbre_color,
                               color.jll_color]),
                    width=0.45,
                    orientation='h',
                    text=(list(map(lambda x: x, list((pv_sorted[("SQM")] / 1000).apply(np.int64))))),
                    textposition='none',
                    textfont=dict(
                        color=[color.white, color.white, color.white, color.white, color.white, color.colliers_grey_80],
                        size=12))

    trace1 = go.Bar(x=pv_sorted["SQM"] / 1000,
                    y=pv_sorted.index,
                    marker=dict(
                        color=[color.sar_color, color.colliers_color, color.kf_color, color.cw_color, color.cbre_color,
                               color.jll_color]),
                    width=0.45,
                    orientation='h',
                    text=(list(map(lambda x: x, list((pv_sorted[("SQM")] / 1000).apply(np.int64))))),
                    textposition='none',
                    textfont=dict(
                        color=[color.white, color.white, color.white, color.white, color.white, color.colliers_grey_80],
                        size=12))

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = 'All years'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = 'all years'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    annotations = []

    for agency, value in zip(pv_sorted.index, pv_sorted["SQM"] / 1000):
        print('value=',value)
        print('PV SQM SUM', pv['SQM'].sum() /1000)
        print(str(((value / pv['SQM'].sum())) * 100) + '%'),
        annotations.append(dict(
                        x=value + 100,
                        y=agency,
                        #xref='x',
                        #yref='y',
                        text='<b>'+ str(int(round(((value / (pv['SQM'].sum() / 1000))*100)))) + '%'+'</b>',
                        showarrow=False,
                        font=dict(family='Arial',
                                  size=12,
                                  color=color.colliers_color),
                    )
        )

    annotations.append(dict(
                        x=1100,
                        y=0.01,
                        xref='x',
                        yref='paper',
                        text='тыс. м²',
                        showarrow=False,
                        font=dict(family='Arial',
                                  size=14,
                                  color=color.black),
                    ))

    for agency, value, text,color_1 in zip(pv_sorted.index, pv_sorted["SQM"] / 1000, list(map(lambda x: x, list((pv_sorted[("SQM")] / 1000).apply(np.int64)))),[color.white, color.white, color.white, color.white, color.white, color.colliers_grey_80]):
        annotations.append(dict(
                        x=0.015,
                        y=agency,
                        xref='paper',
                        #yref='y',
                        text= text,
                        showarrow=False,
                        font=dict(family='Arial',
                                  size=12,
                                  color=color_1),
                    )
        )

    return {
        'data': [trace1],
        'layout':
            go.Layout(
                title='{}<br>'
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
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=True,
                    ticks='',
                    showticklabels=True,
                    #title='Area in sq.m'
                ),
                yaxis=dict(autorange=True,
                           showgrid=True,
                           zeroline=True,
                           showline=True,
                           autotick=False,
                           ticks='',
                           showticklabels=True,
                           ),
                legend=dict(orientation="h",
                            traceorder='normal'),
                # legend=dict(
                #     x=100,
                #     y=1,
                #     font=dict(
                #         size=10,
                #     )
                # ),
                #showlegend=False,
                barmode='stack',
                annotations=annotations,

            )
    }


# РАЗМЕТКА СТРАНИЦЫ 'СОМНИТЕЛЬНЫЕ СДЕЛКИ'

suspicious_deals_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Checklist(  # чеклист с одним значением для имитации дерева параметров
                            id='tree-checklist_susp',
                            # при выборе параметра, открывается список для отображения столбцов
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
                        dcc.Checklist(  # чеклист для выбора столбцов в таблице
                            id='interface_susp',
                            options=[{'label': i, 'value': j} for i, j in  # все возможные значения
                                     zip(list_of_columns_for_gui, list_of_columns)],
                            values=['Agency', 'Country', 'City', 'Property_Name',
                                    # значения по умолчанию при первй загрузке страницы
                                    'Class', 'SQM', "Company", "Business_Sector",
                                    'Type_of_Deal', 'Type_of_Consultancy', 'LLR_TR', 'Year', 'Quarter'],
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
                                       href='/main'),

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
                                            id="Agency_susp",
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
                                    id='Agency_Div_susp',
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
                                            id="Country_susp",
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
                                    id='Country_Div_susp',
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
                                            id="City_susp",
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
                                    id='City_Div_susp',
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
                                            id="Property_name_susp",
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
                                    id='Property_name_Div_susp',
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
                                            id="Class_susp",
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
                                    id='Class_Div_susp',

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
                                            id="SQM_susp",
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
                                            id="Company_susp",
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
                                    id='Company_Div_susp',

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
                                            id="Business_Sector_susp",
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
                                            id="Type_of_Deal_susp",
                                            # value='All agency',
                                            placeholder="Тип сделки",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Type_of_Deal"].unique()
                                            ],

                                        )],
                                    id='Type_of_Deal_Div_susp',
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
                                            id="Type_of_Consultancy_susp",
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
                                    id='Type_of_Consultancy_Div_susp',
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
                                            id="LLR/TR_susp",
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
                                    id='LLR/TR_Div_susp',
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
                                            id="Year_susp",
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
                                    id='Year_Div_susp',
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
                                            id="Quarter_susp",
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
                                    id='Quarter_susp',
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
                                            id="Include_in_Market_Share_susp",
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
                                    id='Include_in_Market_Share_Div_susp',
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
                                            id="Address_susp",
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
                                    id='Address_Div_susp',
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
                                            id="Submarket_Large_susp",
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
                                    id='Submarket_Large_Div_susp',
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
                                            id="Owner_susp",
                                            # value='All agency',
                                            placeholder="Собственник",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Owner"].unique()

                                            ],
                                        )
                                    ],
                                    id='Owner_Div_susp',
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
                                            id="Date_of_acquiring_susp",
                                            # value='All agency',
                                            placeholder="Субрынок",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Date_of_acquiring"].unique()

                                            ],
                                        )
                                    ],
                                    id='Date_of_acquiring_Div_susp',
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
                                            id="Class_Colliers_susp",
                                            # value='All agency',
                                            placeholder="Класс Colliers",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Class_Colliers"].unique()

                                            ],
                                        )
                                    ],
                                    id='Class_Colliers_Div_susp',
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
                                            id="Floor_susp",
                                            # value='All agency',
                                            placeholder="Этаж",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Floor"].unique()

                                            ],
                                        )
                                    ],
                                    id='Floor_Div_susp',
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
                                            id="Deal_Size_susp",
                                            # value='All agency',
                                            placeholder="Размер сделки",
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Deal_Size"].unique()

                                            ],
                                        )
                                    ],
                                    id='Deal_Size_Div_susp',
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
                                            id="Sublease_Agent_susp",
                                            # value='All agency',
                                            placeholder="Sublease_Agent",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Sublease_Agent"].unique()

                                            ],
                                        )
                                    ],
                                    id='Sublease_Agent_Div_susp',
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
                                            id="LLR_Only_susp",
                                            # value='All agency',
                                            placeholder="LLR",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["LLR_Only"].unique()

                                            ],
                                        )
                                    ],
                                    id='LLR_Only_Div_susp',
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
                                            id="E_TR_Only_susp",
                                            # value='All agency',
                                            placeholder="(E)TR",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["E_TR_Only"].unique()

                                            ],
                                        )
                                    ],
                                    id='E_TR_Only_Div_susp',
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
                                            id="LLR/E_TR_susp",
                                            # value='All agency',
                                            placeholder="LLR/(E)TR",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["LLR/E_TR"].unique()

                                            ],
                                        )
                                    ],
                                    id='LLR/E_TR_Div_susp',
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
                                            id="Month_susp",
                                            # value='All agency',
                                            placeholder="Месяц",  # ИЗМЕНИТЬ
                                            multi=True,
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in all_deals_query_df["Month"].unique()

                                            ],
                                        )
                                    ],
                                    id='Month_Div_susp',
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
                                    id='datatable-suspicious'
                                )
                            ]
                        ),
                        html.Div([
                            html.A(
                                'Download All Data',
                                id='download-all-link_susp',
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
                                id='download-selected-link_susp',
                                download="selected_data.csv",
                                href="",
                                target="_blank",
                            )
                        ],
                            style={'background-color': color.colliers_dark_blue}
                        ),
                    ],
                    className='row',
                )
            ],
            className='ten columns',
            # style={
            #     'width': '91.3 %'
            # },

        )

    ],
    style={'backgroundColor': color.colliers_grey_10},

)


@app.callback(dash.dependencies.Output('interface_susp', 'labelStyle'),
              # на вход принимается значение чеклиста 'colums'
              [dash.dependencies.Input('tree-checklist_susp', 'values')
               # если значение выбрано, то отрисовывается новый блок со списком, как в дереве
               ])
def show_tree(val):
    if 'Show' in val:
        children = {'display': 'block',
                    'width': '192px',
                    'margin': '0 0 0 10px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children


def select_drop_from_check_susp():
    @app.callback(dash.dependencies.Output('Include_in_Market_Share_Div_susp', 'style'),
                  # проверка checklist со значениями выбранных столбов в таблице
                  [dash.dependencies.Input('interface_susp', 'values')
                   # при выборе столбца добавляется выпадающий список
                   ])
    def update_drop_include(val):
        try:
            if 'Include_in_Market_Share' in val:
                style_include = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }

            if 'Include_in_Market_Share' not in val:
                style_include = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_include

    @app.callback(dash.dependencies.Output('Agency_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_agency(val):
        try:
            if 'Agency' in val:
                style_agency = {'display': 'inline-block',
                                'width': '7.69%'
                                }

            if 'Agency' not in val:
                style_agency = {'display': 'none',
                                'width': '7.69%'
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_agency

    @app.callback(dash.dependencies.Output('Country_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_country(val):
        try:
            if 'Country' in val:
                style_country = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }

            if 'Country' not in val:
                style_country = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_country

    @app.callback(dash.dependencies.Output('City_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_city(val):
        try:
            if 'City' in val:
                style_city = {'display': 'inline-block',
                              'width': '7.69%'
                              }

            if 'City' not in val:
                style_city = {'display': 'none',
                              'width': '7.69%'
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_city

    @app.callback(dash.dependencies.Output('Property_name_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_property_name(val):
        try:
            if 'Property_Name' in val:
                style_property_name = {'display': 'inline-block',
                                       'width': '7.69%'
                                       }

            if 'Property_Name' not in val:
                style_property_name = {'display': 'none',
                                       'width': '7.69%'
                                       }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_property_name

    @app.callback(dash.dependencies.Output('Class_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_class(val):
        try:
            if 'Class' in val:
                style_class = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Class' not in val:
                style_class = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_class

    @app.callback(dash.dependencies.Output('SQM_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_SQM(val):
        try:
            if 'SQM' in val:
                style_SQM = {'display': 'inline-block',
                             'width': '7.69%'
                             }

            if 'SQM' not in val:
                style_SQM = {'display': 'none',
                             'width': '7.69%'
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_SQM

    @app.callback(dash.dependencies.Output('Company_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Company(val):
        try:
            if 'SQM' in val:
                style_Company = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }

            if 'SQM' not in val:
                style_Company = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Company

    @app.callback(dash.dependencies.Output('Business_Sector_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Business_Sector(val):
        try:
            if 'Business_Sector' in val:
                style_Business_Sector = {'display': 'inline-block',
                                         'width': '7.69%'
                                         }

            if 'Business_Sector' not in val:
                style_Business_Sector = {'display': 'none',
                                         'width': '7.69%'
                                         }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Business_Sector

    @app.callback(dash.dependencies.Output('Type_of_Deal_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Type_of_Deal(val):
        try:
            if 'Type_of_Deal' in val:
                style_Type_of_Deal = {'display': 'inline-block',
                                      'width': '7.69%'
                                      }

            if 'Type_of_Deal' not in val:
                style_Type_of_Deal = {'display': 'none',
                                      'width': '7.69%'
                                      }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Type_of_Deal

    @app.callback(dash.dependencies.Output('Type_of_Consultancy_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Type_of_Consultancy(val):
        try:
            if 'Type_of_Consultancy' in val:
                style_Type_of_Consultancy = {'display': 'inline-block',
                                             'width': '7.69%'
                                             }

            if 'Type_of_Consultancy' not in val:
                style_Type_of_Consultancy = {'display': 'none',
                                             'width': '7.69%'
                                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Type_of_Consultancy

    @app.callback(dash.dependencies.Output('LLR/TR_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Type_of_Consultancy(val):
        try:
            if 'LLR_TR' in val:
                style_LLR_TR = {'display': 'inline-block',
                                'width': '7.69%'
                                }

            if 'LLR_TR' not in val:
                style_LLR_TR = {'display': 'none',
                                'width': '7.69%'
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_LLR_TR

    @app.callback(dash.dependencies.Output('Year_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Year(val):
        try:
            if 'Year' in val:
                style_Year = {'display': 'inline-block',
                              'width': '7.69%'
                              }

            if 'Year' not in val:
                style_Year = {'display': 'none',
                              'width': '7.69%'
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Year

    @app.callback(dash.dependencies.Output('Quarter_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Quarter(val):
        try:
            if 'Quarter' in val:
                style_Quarter = {'display': 'inline-block',
                                 'width': '7.69%'
                                 }
            if 'Quarter' not in val:
                style_Quarter = {'display': 'none',
                                 'width': '7.69%'
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Quarter

    @app.callback(dash.dependencies.Output('Address_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Address(val):
        try:
            if 'Address' in val:
                style_Addres = {'display': 'inline-block',
                                'width': '7.69%'
                                }

            if 'Address' not in val:
                style_Addres = {'display': 'none',
                                'width': '7.69%'
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Addres

    @app.callback(dash.dependencies.Output('Submarket_Large_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Submarket_large(val):
        try:
            if 'Submarket_Large' in val:
                style_Submarket_Large = {'display': 'inline-block',
                                         'width': '7.69%'
                                         }

            if 'Submarket_Large' not in val:
                style_Submarket_Large = {'display': 'none',
                                         'width': '7.69%'
                                         }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Submarket_Large

    @app.callback(dash.dependencies.Output('Owner_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Owner(val):
        try:
            if 'Owner' in val:
                style_Owner = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Owner' not in val:
                style_Owner = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Owner

    @app.callback(dash.dependencies.Output('Date_of_acquiring_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Date_of_acquiring(val):
        try:
            if 'Date_of_acquiring' in val:
                style_Date_of_acquiring = {'display': 'inline-block',
                                           'width': '7.69%'
                                           }

            if 'Date_of_acquiring' not in val:
                style_Date_of_acquiring = {'display': 'none',
                                           'width': '7.69%'
                                           }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Date_of_acquiring

    @app.callback(dash.dependencies.Output('Class_Colliers_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Class_Colliers(val):
        try:
            if 'Class_Colliers' in val:
                style_Class_Colliers = {'display': 'inline-block',
                                        'width': '7.69%'
                                        }

            if 'Class_Colliers' not in val:
                style_Class_Colliers = {'display': 'none',
                                        'width': '7.69%'
                                        }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Class_Colliers

    @app.callback(dash.dependencies.Output('Floor_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Floor(val):
        try:
            if 'Floor' in val:
                style_Floor = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Floor' not in val:
                style_Floor = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Floor

    @app.callback(dash.dependencies.Output('Deal_Size_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Deal_Size(val):
        try:
            if 'Deal_Size' in val:
                style_Deal_Size = {'display': 'inline-block',
                                   'width': '7.69%'
                                   }

            if 'Deal_Size' not in val:
                style_Deal_Size = {'display': 'none',
                                   'width': '7.69%'
                                   }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Deal_Size

    @app.callback(dash.dependencies.Output('Sublease_Agent_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Sublease_Agent(val):
        try:
            if 'Sublease_Agent' in val:
                style_Sublease_Agent = {'display': 'inline-block',
                                        'width': '7.69%'
                                        }

            if 'Sublease_Agent' not in val:
                style_Sublease_Agent = {'display': 'none',
                                        'width': '7.69%'
                                        }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Sublease_Agent

    @app.callback(dash.dependencies.Output('LLR_Only_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_LLR_Only(val):
        try:
            if 'LLR_Only' in val:
                style_LLR_Only = {'display': 'inline-block',
                                  'width': '7.69%'
                                  }

            if 'LLR_Only' not in val:
                style_LLR_Only = {'display': 'none',
                                  'width': '7.69%'
                                  }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_LLR_Only

    @app.callback(dash.dependencies.Output('E_TR_Only_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_E_TR_Only(val):
        try:
            if 'E_TR_Only' in val:
                style_E_TR_Only = {'display': 'inline-block',
                                   'width': '7.69%'
                                   }

            if 'E_TR_Only' not in val:
                style_E_TR_Only = {'display': 'none',
                                   'width': '7.69%'
                                   }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_E_TR_Only

    @app.callback(dash.dependencies.Output('LLR/E_TR_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_LLR_E_TR(val):
        try:
            if 'LLR/E_TR' in val:
                style_LLR_E_TR = {'display': 'inline-block',
                                  'width': '7.69%'
                                  }

            if 'LLR/E_TR' not in val:
                style_LLR_E_TR = {'display': 'none',
                                  'width': '7.69%'
                                  }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_LLR_E_TR

    @app.callback(dash.dependencies.Output('Month_Div_susp', 'style'),
                  [dash.dependencies.Input('interface_susp', 'values')
                   ])
    def update_drop_Month(val):
        try:
            if 'Month' in val:
                style_Month = {'display': 'inline-block',
                               'width': '7.69%'
                               }

            if 'Month' not in val:
                style_Month = {'display': 'none',
                               'width': '7.69%'
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Month


select_drop_from_check_susp()  # вызов функции с отображением выпадающих списков


@app.callback(dash.dependencies.Output('datatable-suspicious', 'rows'),
              [dash.dependencies.Input('Year_susp', 'value'),
               dash.dependencies.Input('Country_susp', 'value'),
               dash.dependencies.Input('Agency_susp', 'value'),
               dash.dependencies.Input('City_susp', 'value'),
               dash.dependencies.Input('Property_name_susp', 'value'),
               dash.dependencies.Input('Class_susp', 'value'),
               dash.dependencies.Input('SQM_susp', 'value'),
               dash.dependencies.Input('Business_Sector_susp', 'value'),
               dash.dependencies.Input('Type_of_Deal_susp', 'value'),
               dash.dependencies.Input('Type_of_Consultancy_susp', 'value'),
               dash.dependencies.Input('LLR/TR_susp', 'value'),
               dash.dependencies.Input('Quarter_susp', 'value'),
               dash.dependencies.Input('Company_susp', 'value'),
               dash.dependencies.Input('Include_in_Market_Share_susp', 'value'),
               dash.dependencies.Input('Address_susp', 'value'),
               dash.dependencies.Input('Submarket_Large_susp', 'value'),
               dash.dependencies.Input('Owner_susp', 'value'),
               dash.dependencies.Input('Date_of_acquiring_susp', 'value'),
               dash.dependencies.Input('Class_Colliers_susp', 'value'),
               dash.dependencies.Input('Floor_susp', 'value'),
               dash.dependencies.Input('Deal_Size_susp', 'value'),
               dash.dependencies.Input('Sublease_Agent_susp', 'value'),
               dash.dependencies.Input('LLR_Only_susp', 'value'),
               dash.dependencies.Input('E_TR_Only_susp', 'value'),
               dash.dependencies.Input('LLR/E_TR_susp', 'value'),
               dash.dependencies.Input('Month_susp', 'value'),
               dash.dependencies.Input('interface_susp', 'values')  # значение чеклиста из дерева с выбором столбцов
               ])
def update_datatable_susp(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                          Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address,
                          Submarket_Large, Owner,
                          Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                          LLR_E_TR,
                          Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy], LLR_TR=[LLR_TR],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], LLR_Only=[LLR_Only], E_TR_Only=[E_TR_Only],
                LLR_E_TR=[LLR_E_TR], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, LLR_TR, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, LLR_Only, E_TR_Only,
                      LLR_E_TR,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    suspecious_deals_df_equal_sqm = all_deals_query_df[all_deals_query_df.duplicated(['SQM'], keep=False)].sort_values(
        'SQM', ascending=False)
    print('equal SQM')
    print(suspecious_deals_df_equal_sqm['SQM'])

    sort_for_dif = all_deals_query_df.sort_values('SQM', ascending=False)
    suspecious_deals_df_sqm_diff_less_five = sort_for_dif[sort_for_dif['SQM'].diff() < 5]
    print('difference between SQM')
    print(suspecious_deals_df_sqm_diff_less_five)

    suspecious_deals_df_merged_by_equal_and_diff = pd.merge(suspecious_deals_df_equal_sqm,
                                                            suspecious_deals_df_sqm_diff_less_five, how='inner')
    print('merged')
    print(suspecious_deals_df_merged_by_equal_and_diff)

    # suspecious_deals_df_sqm_diff_year = sort_for_dif[sort_for_dif['Year'].diff() <= 1]
    # suspecious_deals_df_sqm_diff_year_sorted = suspecious_deals_df_sqm_diff_year.sort_values('Year', ascending=False)
    # print('suspecious_deals_df_sqm_diff_year_sorted')
    # print(suspecious_deals_df_sqm_diff_year_sorted)

    sort_for_dif = all_deals_query_df.sort_values('Quarter', ascending=False)
    suspecious_deals_df_quar_diff = sort_for_dif[sort_for_dif['Quarter'].diff() <= 2]

    suspecious_deals_df_merged_by_equal_year_qurter_diff = pd.merge(suspecious_deals_df_merged_by_equal_and_diff,
                                                                    suspecious_deals_df_quar_diff, how='inner')

    suspecious_deals_total = suspecious_deals_df_merged_by_equal_year_qurter_diff

    if len(list_of_values_copy) == 0:
        return suspecious_deals_total[col].to_dict('records')
    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = suspecious_deals_total[(suspecious_deals_total[ind].isin(list_of_values_copy[i]))]
            else:
                data = suspecious_deals_total[(suspecious_deals_total[ind].isin(list_of_values_copy[i]))]
        return data[col].to_dict('records')


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
    # формирования файла-шаблона с первой строкой - названием столбцов таблицы
    [dash.dependencies.Input('download-example-button', 'n_clicks')]
)
def example_button(n_clicks):
    data = pd.DataFrame.from_records([list_of_columns])  # создание датафрейма из списка заголовков столбца
    csv_string = data.to_csv(header=False, index=False, encoding='utf-8',
                             sep=',')  # формирование csv файла выбранной кодировкой и знаком разделения
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(
        csv_string)  # декодирование csv файла в байткод и запись в ссылку байткода для скачивания
    return csv_string  # возвращает сформированный байткод в строку-ссылку


def parse_contents(contents, filename):  # чтение загруженного файла, определение расширения,
    content_type, content_string = contents.split(',')  # разделителя и декодирование из байткода
    decoded = base64.b64decode(content_string + "==")

    try:
        if 'csv' in filename:
            df = pd.read_csv((io.StringIO(decoded.decode('utf-8'))), header=None)
            df.columns = list_of_columns
        elif 'xls' in filename:  # проверка, является ли загруженный файл xls, не всегда работает корректно, так что пока лучше остановиться на csv
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
            df.columns = list_of_columns
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


@app.callback(dash.dependencies.Output('output-data-upload', 'children'),  # отображение в таблице загруженных данных
              [dash.dependencies.Input('upload-data', 'contents'),
               dash.dependencies.Input('upload-data', 'filename'),
               ])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


def save_contents(contents_save, filename_save):  # данные, загруженные в скрипт сохраняются в скрытом элементе страницы
    content_type, content_string = contents_save.split(
        ',')  # в json массиве, это необходимо для передачи данных между callback`ами
    decoded = base64.b64decode(
        content_string + "==")  # это решение - единственный способ передать данные без использования глобальных переменных
    try:
        if 'csv' in filename_save:  # проверка, является ли загруженный файл csv
            df = pd.read_csv((io.StringIO(decoded.decode('utf-8'))), header=None)
            json = df.to_json(date_format='iso', orient='split')
        elif 'xls' in filename_save:  # проверка, является ли загруженный файл xls
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
            json = df.to_json(date_format='iso', orient='split')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return json


@app.callback(dash.dependencies.Output('intermediate-value', 'children'),
              # callback, выполняющий функцию "save_contents"
              [dash.dependencies.Input('upload-data', 'contents'),
               dash.dependencies.Input('upload-data', 'filename'),
               ])
def save_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            save_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children


@app.callback(dash.dependencies.Output('table', 'children'),  # сохранение данных из загруженного файла в БД
              [dash.dependencies.Input('intermediate-value', 'children')]
              )
def update_table(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        dff = pd.read_json(jsonified_cleaned_data[0], orient='split')
        dff.columns = list_of_columns
        dff.to_sql('Market_Share', con, if_exists='append', index=None, index_label=list_of_columns)
        return print('База обновлена')
    else:
        print('empty json')


# '''
#     обновление страницы: если параметра pathname совпадает с ссылкой страницы, то отрисовывается
#     выбранная страница
#                                                                                                    '''

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
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


if __name__ == '__main__':
    app.run_server(debug=True, host='10.168.207.102')
