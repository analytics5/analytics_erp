import dash
import base64
import io
import itertools
import urllib
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
import project_sql as sql
import Passwords_and_Usernames as users
import plotly as pt



app = dash.Dash(__name__)
server = app.server
auth = dash_auth.BasicAuth(app, users.VALID_USERNAME_PASSWORD_PAIRS)
app.config.suppress_callback_exceptions = True
# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})    # то, что предлагают плотли
# app.css.append_css({'external_url': 'https://raw.githubusercontent.com/Wittgensteen/work_stuff/master/base_style.css'})    # мой файл на гитхабе
app.css.append_css({'external_url': 'https://rawgit.com/Wittgensteen/work_stuff/master/new_buttons.css'})  # мой файл с гитхаба на rawgit




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

all_deals_query = sql.table_query

suspicious_deals = sql.suspicious_deals

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

    all_deals_query_df.columns = ['Agency', 'Country', 'City', 'Property_name', 'Class', 'SQM',         # ИЗМЕНЕНО ВРЕМЕННО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                  'Type_of_Consultancy', 'Year', 'Quarter']

    suspicious_deals_df.columns = ['Agency', 'Country', 'City', 'Property Name', 'Class', 'SQM', 'Company',
                                   'Type_of_Consultancy', 'Year', 'Quarter']

country = ("All countries", "Russia", "Ukraine", "Belarus", "Kazakhstan ", "Azerbaijan")
country_ind = ("All countries", "RU", "UA", "BY", "KZ", "AZ")
years = ("All years", "2013", "2014", "2015", "2016", "2017", "2018")
Agency = ("All agency", "Colliers", "KF", "JLL", "CW", "SAR", "CBRE")




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

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}
                 ),

    ],
    # style={'backgroundColor': color.colliers_dark_blue}
)

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
* Здесь будет располагаться руководство пользователя
  * С гиперссылками
    ''')
],
    style={'backgroundColor': color.colliers_pale_blue}
)

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
    style={'backgroundColor': color.colliers_pale_blue}
)

page_1_layout = html.Div(
    [
        html.Div([
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                children="Позиции на рынке России",
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
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Year",
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in years
                                            ],
                                            value='All years'
                                        ),

                                    ],
                                    # className='row',
                                    style={'width': '25%',
                                           'display': 'inline-block'}
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Size",
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in ['Default', '1/2', '1/3']
                                            ],
                                            value='Default'
                                        ),

                                    ],
                                    style={'width': '25%',
                                           'display': 'inline-block'}
                                ),
                            ]
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='market-graph'),
                                        dcc.Graph(id='market-graph-non-stack'),
                                        dcc.Graph(id='market-graph-horizontal'),
                                    ],
                                    className='six columns',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(id='market-pie-graph'),
                                        dcc.Graph(id='market-graph-percent'),
                                        dcc.Graph(id='market-graph-horizontal-total')
                                    ],
                                    className='six columns  ',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                )
                            ],
                            className='row',

                        )

                    ],
                    className='ten columns',
                    style={'display': 'inline'}
                    # style={'display': 'inline-block'}
                )

            ],
            style={'backgroundColor': color.colliers_grey_10}

        )
    ],
    style={'backgroundColor': color.colliers_pale_blue}
)


@app.callback(
    dash.dependencies.Output('market-graph', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_graph(Year, Size):
    if Year == "All years":
        df_plot = deals_df.copy()
    else:
        df_plot = deals_df[deals_df['Year'] == Year]

    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    # if Size == "1/4":
    #     width = 370
    #     height = 180

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

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

    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='Deals in {}<br>'
                      'Deals in Russia'.format(Year),
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
    dash.dependencies.Output('market-graph-non-stack', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_graph_not_stack(Year, Size):
    if Year == "All years":
        df_plot = deals_df.copy()
    else:
        df_plot = deals_df[deals_df['Year'] == Year]
    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
        color=color.colliers_dark_blue), width=0.2, )
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

    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='Deals in {}<br>'
                      'Deals in Russia'.format(Year),
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

                yaxis=dict(
                    exponentformat=False,
                    title='Area in sq.m'
                ),
                # barmode='stack'
            )
    }


@app.callback(
    dash.dependencies.Output('market-graph-horizontal', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_graph_horizontal(Year, Size):
    if Year == "All years":
        df_plot = deals_df.copy()
    else:
        df_plot = deals_df[deals_df['Year'] == Year]

    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    print(pv[("SQM")].sum())

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
                title='Market Share in {}, %'.format(Year),
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
    dash.dependencies.Output('market-pie-graph', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_pie_graph(Year, Size):
    if Year == "All years":
        df_plot2 = deals_df.copy()
    else:
        df_plot2 = deals_df[deals_df['Year'] == Year]

    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    pv = pd.pivot_table(
        df_plot2,
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
    return {
        'data': [pie1],
        'layout': go.Layout(
            title='Deals in {}<br>'
                  'Deals in Russia'.format(Year),
            width=width,
            height=height,
        )
    }


@app.callback(
    dash.dependencies.Output('market-graph-percent', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_graph_percent(Year, Size):
    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    if Year == "All years":
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
        y1 = pv1[("SQM"), 'Colliers'] * 100 / pv2["SQM"].sum()
        print(y1['2013'])
        print(round((y1['2013'])))
        trace1 = go.Bar(x=pv1.index, y=y1, name='Colliers', marker=dict(
            color=color.colliers_dark_blue), width=0.25, textposition='auto')
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
        return {
            'data': [trace1, trace2, trace3, trace4, trace5, trace6],
            'layout':
                go.Layout(
                    title='Percent in {}'.format(Year),
                    autosize=False,
                    bargap=0.3,
                    bargroupgap=0,
                    font=dict(
                        color=color.colliers_grey_80_60,
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
        df_plot = deals_df[deals_df['Year'] == Year]

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

    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='Percent in {}'.format(Year),
                autosize=False,
                bargap=0.3,
                bargroupgap=0,
                font=dict(
                    color=color.colliers_grey_10,
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
    dash.dependencies.Output('market-graph-horizontal-total', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_graph_horizontal_total(Year, Size):
    if Year == "All years":
        df_plot = deals_df.copy()
    else:
        df_plot = deals_df[deals_df['Year'] == Year]

    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

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
    return {
        'data': [trace1],
        'layout':
            go.Layout(
                title='Deals in {}'.format(Year),
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


page_2_layout = html.Div(
    [
        html.Div([
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                children="Позиции на рынке Москвы",
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
                                   'height': '900px',
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
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Year",
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in years
                                            ],
                                            value='All years'
                                        ),

                                    ],
                                    # className='row',
                                    style={'width': '25%',
                                           'display': 'inline-block'}
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Size",
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in ['Default', '1/2', '1/3']
                                            ],
                                            value='Default'
                                        ),

                                    ],
                                    style={'width': '25%',
                                           'display': 'inline-block'}
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='llr-representation-pie'),
                                        dcc.Graph(id='llr-representation-bar'),
                                    ],
                                    className='six columns',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(id='tenant-representation-pie'),
                                        dcc.Graph(id='tenant-representation-bar')
                                    ],
                                    className='six columns  ',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                )
                            ],
                            className='row',

                        )

                    ],
                    className='ten columns',
                    style={'display': 'inline'}
                    # style={'display': 'inline-block'}
                )

            ],
            style={'backgroundColor': color.colliers_grey_10}

        )
    ],
    style={'backgroundColor': color.colliers_pale_blue}
)


@app.callback(
    dash.dependencies.Output('llr-representation-pie', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_llr_representation(Year, Size):
    if Year == "All years":
        df_plot2 = llr_df.copy()
    else:
        df_plot2 = llr_df[llr_df['Year'] == Year]

    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    pv = pd.pivot_table(
        df_plot2,
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
    return {
        'data': [pie1],
        'layout': go.Layout(
            title='Landlord representation in {}'.format(Year),
            width=width,
            height=height,
        )
    }


@app.callback(
    dash.dependencies.Output('tenant-representation-bar', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_tenant_representation_bar(Year, Size):
    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    if Year == "All years":
        df_plot = tenant_df.copy()
    else:
        df_plot = tenant_df[tenant_df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    print('__-__--__--____')
    print(tenant_df)
    print('__-__--__--____')

    trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
        color=color.colliers_dark_blue), width=0.2)
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

    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='Tenant representation in {}'.format(Year),
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
                yaxis={'title': 'Area in sq.m'},
                barmode='stack')
    }


@app.callback(
    dash.dependencies.Output('tenant-representation-pie', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_tenant_representation(Year, Size):
    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    if Year == "All years":
        df_plot2 = tenant_df.copy()
    else:
        df_plot2 = tenant_df[tenant_df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot2,
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
    return {
        'data': [pie1],
        'layout': go.Layout(
            title='Tenant representation in {}'.format(Year),
            width=width,
            height=height,
        )
    }


@app.callback(
    dash.dependencies.Output('llr-representation-bar', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_llr_representation_bar(Year, Size):
    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    if Year == "All years":
        df_plot = llr_df.copy()
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
            color=color.colliers_dark_blue), width=0.2, text='%')
        trace2 = go.Bar(x=pv1.index, y=pv1[("SQM", 'SAR')] * 100 / pv2["SQM"].sum(), name='SAR', marker=dict(
            color=color.colliers_light_blue), width=0.2, text='%')
        trace3 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum(), name='CW', marker=dict(
            color=color.colliers_extra_light_blue), width=0.2, text='%')
        trace4 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum(), name='CBRE', marker=dict(
            color=color.colliers_grey_40), width=0.2, text='%')
        trace5 = go.Bar(x=pv1.index, y=pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum(), name='JLL', marker=dict(
            color=color.colliers_yellow), width=0.2, text='%')
        trace6 = go.Bar(x=pv1.index, y=pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum(), name='KF', marker=dict(
            color=color.colliers_red), width=0.2, text='%')
        return {
            'data': [trace1, trace2, trace3, trace4, trace5, trace6],
            'layout':
                go.Layout(
                    title='Landlord Represenation in {}'.format(Year),
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
        df_plot = llr_df[llr_df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    print('0000000000000000000000000000000000000000000000')
    print(pv)
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

    return {
        'data': [trace1, trace2, trace3, trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='Percent in {}'.format(Year),
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


page_3_layout = html.Div(
    [
        html.Div([
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                children="Доля сделок SALE vs LEASE (Москва)",
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
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Year",
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in years
                                            ],
                                            value='All years'
                                        ),

                                    ],
                                    # className='row',
                                    style={'width': '25%',
                                           'display': 'inline-block'}
                                ),

                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="Size",
                                            options=[{
                                                'label': i,
                                                'value': i
                                            }
                                                for i in ['Default', '1/2', '1/3']
                                            ],
                                            value='Default'
                                        ),

                                    ],
                                    style={'width': '25%',
                                           'display': 'inline-block'}
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='sale-lease-horizontal'),

                                    ],
                                    className='six columns',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(id='sale-lease-horizontal')

                                    ],
                                    className='six columns  ',
                                    # style={'backgroundColor': color.colliers_pale_blue,
                                    #       'display': 'inline-block'
                                    #       }
                                )
                            ],
                            className='row',

                        )

                    ],
                    className='ten columns',
                    style={'display': 'inline'}
                    # style={'display': 'inline-block'}
                )

            ],
            style={'backgroundColor': color.colliers_grey_10}

        )
    ],
    style={'backgroundColor': color.colliers_pale_blue}
)


@app.callback(
    dash.dependencies.Output('sale-lease-horizontal', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     dash.dependencies.Input('Size', 'value')])
def update_sale_lease_horizontal(Year, Size):
    if Size == "Default":
        width = 650
        height = 450

    if Size == "1/2":
        width = 740
        height = 360

    if Size == "1/3":
        width = 426
        height = 240

    if Year == "All years":
        df_plot1 = sale_lease_sale_df.copy()
        df_plot2 = sale_lease_lease_df.copy()

    else:
        df_plot1 = sale_lease_df[sale_lease_df['Year'] == Year]
        df_plot2 = sale_lease_lease_df[sale_lease_lease_df['Year'] == Year]

    pv1 = pd.pivot_table(
        df_plot1,
        index=["Agency"],
        # columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    # df_plot1 = df_plot1.reindex(pv1["SQM"].sort_values(by=2015, ascending=False).index)
    # print(pv1)
    # print('=-=-=-=-=-=-=-=-=-=-=-=-=-')
    # print(df_plot1)
    # print('=-=-=-=-=-=-=-=-=-=-=-=-=-')

    pv2 = pd.pivot_table(
        df_plot2,
        index=["Agency"],
        # columns=['Agency'],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    print('=-=-=-=-=-=-=-=-=-=-=-=-=-')
    pv1.reset_index(inplace=True)  # объединение датафреймов в один для адекватного построения графиков
    pv2.reset_index(inplace=True)
    pv12 = pd.merge(pv1, pv2, 'left', on=["Agency"])
    pv12.columns = ['Agency', 'Sale', 'Lease']

    print(pv12)
    pv3 = pd.pivot_table(
        pv12,
        index=["Agency"],
        # columns=['Sale','Lease'],
        values=["Sale", "Lease"],
        aggfunc=sum,
        fill_value=0
    )

    # print(pv1)
    # print('____________')
    # print(pv2)
    # print('_____________')
    # print(pv12)
    # print(pv3)

    trace1 = go.Bar(x=pv12['Sale'], y=pv12['Agency'], marker=dict(
        color=color.colliers_light_blue), width=0.2, orientation='h', name='Sale')
    trace2 = go.Bar(x=pv12['Lease'], y=pv12['Agency'], marker=dict(
        color=color.colliers_dark_blue), width=0.2, orientation='h', name='Lease')

    return {
        'data': [trace1, trace2],
        'layout':
            go.Layout(
                title='Deals in {}'.format(Year),
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


page_4_layout = html.Div(
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
                                        for i in all_deals_query_df["Property_name"].unique()
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
                                # html.Div([dcc.Dropdown(
                                #     id="Company",
                                #     # value='All agency',
                                #     placeholder="Компания",
                                #     multi=True,
                                #     options=[{
                                #         'label': i,
                                #         'value': i
                                #     }
                                #         for i in all_deals_query_df["Company"].unique()
                                #     ],
                                #
                                # )],
                                #     # className='one columns',
                                #     style={
                                #         'width': '10%',
                                #         #    'padding-left': '10',
                                #         #     #'margin-left': '3%',
                                #         'display': 'inline-block',
                                #         #     'float': 'right'
                                #     }
                                # ),

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
                                    filterable=True,
                                    sortable=True,
                                    selected_row_indices=[],
                                    min_height=600,
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
                                'Download Data',
                                id='download-link',
                                download="rawdata.csv",
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


@app.callback(dash.dependencies.Output('datatable', 'rows'),
              [dash.dependencies.Input('Year', 'value'),
               dash.dependencies.Input('Country', 'value'),
               dash.dependencies.Input('Agency', 'value'),
               dash.dependencies.Input('City', 'value'),
               dash.dependencies.Input('Property_name', 'value'),
               dash.dependencies.Input('Class', 'value'),
               dash.dependencies.Input('SQM', 'value'),
               dash.dependencies.Input('Type_of_Consultancy', 'value'),
               dash.dependencies.Input('Quarter', 'value')
               ])
def update_datatable(Year, Country, Agency, City, Property_name, Class, SQM, Type_of_Consultancy, Quarter):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                City=[City],Property_name=[Property_name],Class=[Class],
                SQM=[SQM],Type_of_Consultancy=[Type_of_Consultancy], Quarter=[Quarter])
    q = ' and '.join(['{} in @cond.get("{}")'.format(k, k) for k in cond.keys()])
    #print(cond)
    #print(cond.keys())
    #print(q)
    print('New iteration')
    print(Year, 'Year')
    print(Country, 'Country')
    print(Agency, 'Agency')
    print(City, 'City')
    print(Property_name, 'Property_name')
    print(Class, 'Class')
    print(SQM, 'SQM')
    print(Type_of_Consultancy, 'Type_of_deal')
    print(Quarter, 'Quarter')
    list_of_values = (Year, Country, Agency, City, Property_name, Class, SQM, Type_of_Consultancy, Quarter)
    list_of_index = ('Year', 'Country', 'Agency', 'City', 'Property_name', 'Class', 'SQM', 'Type_of_Consultancy', 'Quarter')
    list1 = list(itertools.combinations(list_of_index, 1))
    list2 = list(itertools.combinations(list_of_index, 2))
    list3 = list(itertools.combinations(list_of_index, 3))
    list4 = list(itertools.combinations(list_of_index, 4))
    list5 = list(itertools.combinations(list_of_index, 5))
    list6 = list(itertools.combinations(list_of_index, 6))
    list7 = list(itertools.combinations(list_of_index, 7))
    list8 = list(itertools.combinations(list_of_index, 8))
    list9 = list(itertools.combinations(list_of_index, 9))


    #d = {a: a for a in list_of_index}
    #print(d)
    #print(cond.keys())

    print(cond.keys())
    print(cond.values())


    for c in cond.keys():
        if c is None or (cond[c][0] is None or len(cond[c][0]) == 0):
            print(c, cond[c][0], 'первое условие')
            print(cond.get(c))
            print(print(cond.keys()))
            return all_deals_query_df.to_dict('records')


        if c is not None and len(cond[c][0]) != 0:
            print(c, cond[c][0], 'второе условие')
            data = all_deals_query_df[(all_deals_query_df[c].isin(cond[c][0]))]
            del cond[c]
            return data.to_dict('records')






#_________________________________________________________________
#     if (Country == Country) and \
#             (Agency == Agency) and \
#             (Year is None or len(Year) == 0 or Year[0] == "All years")and \
#             (City is None or len(City) == 0)and \
#             (Property_name is None or len(Property_name) == 0)and \
#             (Class is None or len(Class) == 0)and \
#             ((SQM is None or len(str(SQM)) == 0) or \
#                      (SQM is None or len(SQM) == 0))and \
#             (Type_of_Consultancy is None or len(Type_of_Consultancy) == 0)and \
#             (Quarter is None or len(Quarter) == 0):
#         return all_deals_query_df[(all_deals_query_df['Agency'].isin(Agency)) &
#                                   (all_deals_query_df['Country'].isin(Country))].to_dict('records')
#
#
#
#
#
#
#
#
# #_____________________________________________________________________________________________________
#
#
#     if (Country == Country) and \
#             (City == City) and \
#             (Agency == Agency) and \
#             (Year is None or len(Year) == 0) and \
#             (Property_name is None or len(Property_name) == 0)and \
#             (Class is None or len(Class) == 0)and \
#             ((SQM is None or len(str(SQM)) == 0) or \
#                      (SQM is None or len(SQM) == 0))and \
#             (Type_of_Consultancy is None or len(Type_of_Consultancy) == 0)and \
#             (Quarter is None or len(Quarter) == 0):
#         return all_deals_query_df[(all_deals_query_df['Agency'].isin(Agency)) &
#                                   (all_deals_query_df['Country'].isin(Country)) &
#                                   (all_deals_query_df['City'].isin(City))].to_dict('records')
#
#
#
#
#
# #_____________________________________________________________________
#
#     if (Country == Country) and \
#             (Property_name == Property_name) and \
#             (Agency == Agency) and \
#             (City == City) and \
#             (Year is None or len(Year) == 0 or Year == "All years")and \
#             (Class is None or len(Class) == 0)and \
#             ((SQM is None or len(str(SQM)) == 0) or \
#                      (SQM is None or len(SQM) == 0))and \
#             (Type_of_Consultancy is None or len(Type_of_Consultancy) == 0)and \
#             (Quarter is None or len(Quarter) == 0):
#         return all_deals_query_df[(all_deals_query_df['Agency'].isin(Agency)) &
#                                   (all_deals_query_df['Country'].isin(Country)) &
#                                   (all_deals_query_df['City'].isin(City)) &
#                                   (all_deals_query_df['Property Name'].isin(Property_name))].to_dict('records')
#
#
# #_______________________________________________
#     if (Country == Country) and \
#             (Property_name == Property_name) and \
#             (Agency == Agency) and \
#             (City == City) and \
#             (Year is None or len(Year) == 0 or Year == "All years")and \
#             (Class == Class)and \
#             ((SQM is None or len(str(SQM)) == 0) or \
#                      (SQM is None or len(SQM) == 0))and \
#             (Type_of_Consultancy is None or len(Type_of_Consultancy) == 0)and \
#             (Quarter is None or len(Quarter) == 0):
#         return all_deals_query_df[(all_deals_query_df['Agency'].isin(Agency)) &
#                                   (all_deals_query_df['Country'].isin(Country)) &
#                                   (all_deals_query_df['City'].isin(City)) &
#                                   (all_deals_query_df['Property Name'].isin(Property_name)) &
#                                   (all_deals_query_df['Class'].isin(Class))].to_dict('records')
#
#
#
#
#
# #______________________________________________
#     if (Year is None or len(Year) == 0 or Year == "All years") and \
#             (Property_name == Property_name) and \
#             (Agency == Agency) and \
#             (City == City) and \
#             (Country == Country) and \
#             (Class == Class) and \
#             (SQM == SQM)and \
#             (Type_of_Consultancy is None or len(Type_of_Consultancy) == 0)and \
#             (Quarter is None or len(Quarter) == 0):
#         return all_deals_query_df[(all_deals_query_df['Agency'].isin(Agency)) &
#                                   (all_deals_query_df['Country'].isin(Country)) &
#                                   (all_deals_query_df['City'].isin(City)) &
#                                   (all_deals_query_df['Property Name'].isin(Property_name)) &
#                                   (all_deals_query_df['Class'].isin(Class)) &
#                                   (all_deals_query_df['SQM'].isin(SQM))].to_dict('records')
#
#
#
#
#     #______________________________________________
#
#     if (Year == Year) and\
#             (Country == Country) and\
#             (Agency is None or len(Agency) == 0 or Agency == "All agency") and\
#             (City == City) and\
#             (Property_name == Property_name and
#              Class == Class) and\
#             (SQM == SQM) and\
#             (Type_of_Consultancy == Type_of_Consultancy)and \
#             (Quarter is None or len(Quarter) == 0):
#         return all_deals_query_df[(all_deals_query_df['Year'].isin(Year)) &
#                                   (all_deals_query_df['Country'].isin(Country))&
#                                   (all_deals_query_df['City'].isin(City))&
#                                   (all_deals_query_df['Property Name'].isin(Property_name)) &
#                                   (all_deals_query_df['Class'].isin(Class))&
#                                   (all_deals_query_df['SQM'].isin(SQM))&
#                                   (all_deals_query_df['Type_of_Consultancy'].isin(Type_of_Consultancy))].to_dict('records')
#
#
#     #______________________________________________
#
#     if (Year == Year) and (Country == Country) and (Agency == Agency) and (City == City) and\
#             (Property_name == Property_name) and (Class == Class) and (SQM == SQM) and (Type_of_Consultancy == Type_of_Consultancy)and (Quarter == Quarter):
#         return all_deals_query_df[(all_deals_query_df['Year'].isin(Year)) &
#                                   (all_deals_query_df['Agency'].isin(Agency)) &
#                                   (all_deals_query_df['Country'].isin(Country))&
#                                   (all_deals_query_df['City'].isin(City))&
#                                   (all_deals_query_df['Property Name'].isin(Property_name)) &
#                                   (all_deals_query_df['Class'].isin(Class))&
#                                   (all_deals_query_df['SQM'].isin(SQM))&
#                                   (all_deals_query_df['Type_of_Consultancy'].isin(Type_of_Consultancy))&
#                                   (all_deals_query_df['Quarter'].isin(Quarter))].to_dict('records')







# @app.callback(dash.dependencies.Output('sum', 'children'),
#               [dash.dependencies.Input('Year', 'value'),
#                dash.dependencies.Input('Country', 'value'),
#                dash.dependencies.Input('Agency', 'value')
#                ])
# def update_sum(Year, Country, Agency):
#     if (Year is None or len(Year) == 0 or Year[0] == "All years") and \
#             (Country is None or len(Country) == 0 or Country[0] == "All countries") and \
#             (Agency is None or len(Agency) == 0 or Agency[0] == "All agency"):
#         data_sum = all_deals_query_df["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Country is None or len(Country) == 0 or Country[0] == "All countries") and \
#             (Year is None or len(Year) == 0) and \
#             (Agency is None or len(Agency) == 0):
#         data_sum = all_deals_query_df["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Agency is None or len(Agency) == 0 or Agency[0] == "All agency") and \
#             (Year is None or len(Year) == 0) and \
#             (Country is None or len(Country) == 0):
#         data_sum = all_deals_query_df["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Year == Year) and \
#             (Country is None or len(Country) == 0 or Country[0] == "All countries") and \
#             (Agency is None or len(Agency) == 0 or Agency[0] == "All agency"):
#         data = all_deals_query_df[(all_deals_query_df['Year'].isin(Year))]
#         data_sum = data["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Country == Country) and \
#             (Year is None or len(Year) == 0 or Year[0] == "All years") and \
#             (Agency is None or len(Agency) == 0 or Agency[0] == "All agency"):
#         data = all_deals_query_df[(all_deals_query_df['Country'].isin(Country))]
#         data_sum = data["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Agency == Agency) and \
#             (Year is None or len(Year) == 0 or Year[0] == "All years") and \
#             (Country is None or len(Country) == 0 or Country[0] == "All countries"):
#         data = all_deals_query_df[(all_deals_query_df['Agency'].isin(Agency))]
#         data_sum = data["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Year == Year) and \
#             (Country == Country) and \
#             (Agency is None or len(Agency) == 0 or Agency[0] == "All agency"):
#         data = all_deals_query_df[(all_deals_query_df['Year'].isin(Year)) &
#                                   (all_deals_query_df['Country'].isin(Country))]
#         data_sum = data["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Year == Year) and \
#             (Agency == Agency) and \
#             (Country is None or len(Country) == 0 or Country[0] == "All countries"):
#         data = all_deals_query_df[(all_deals_query_df['Year'].isin(Year)) &
#                                   (all_deals_query_df['Agency'].isin(Agency))]
#         data_sum = data["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Country == Country) and \
#             (Agency == Agency) and \
#             (Year is None or len(Year) == 0 or Year[0] == "All years"):
#         data = all_deals_query_df[(all_deals_query_df['Country'].isin(Country)) &
#                                   (all_deals_query_df['Agency'].isin(Agency))]
#         data_sum = data["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     if (Year == Year) and (Country == Country) and (Agency == Agency):
#         data = all_deals_query_df[(all_deals_query_df['Year'].isin(Year)) &
#                                   (all_deals_query_df['Agency'].isin(Agency)) &
#                                   (all_deals_query_df['Country'].isin(Country))].to_dict('records')
#         data_sum = data["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'
#
#     else:
#         data_sum = all_deals_query_df["SQM"].sum()
#         return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'


@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('Year', 'value'),
     # dash.dependencies.Input('Country', 'value'),
     # dash.dependencies.Input('Agency', 'value')
     ])
def update_download_link(Year):
    if (Year is None or len(Year) == 0 or Year[0] == "All years"):
        csv_string = all_deals_query_df.to_csv(index=False, encoding='utf-8', sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

    if (Year == Year):
        csv_string = all_deals_query_df[(all_deals_query_df['Year'].isin(Year))].to_csv(index=False, encoding='utf-8',
                                                                                        sep=';')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string


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
                                html.Div([dcc.Dropdown(
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

                                )],
                                    # className='two columns',
                                    style={
                                        'width': '10%',
                                        #    'padding-left': '10',
                                        #     #'margin-left': '3%',
                                        'display': 'inline-block',
                                        #     'float': 'right'
                                    }
                                ),
                                html.Div([dcc.Dropdown(
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
                                        for i in all_deals_query_df["Property_name"].unique()
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
                                # html.Div([dcc.Dropdown(
                                #     id="Company",
                                #     # value='All agency',
                                #     placeholder="Компания",
                                #     multi=True,
                                #     options=[{
                                #         'label': i,
                                #         'value': i
                                #     }
                                #         for i in all_deals_query_df["Company"].unique()
                                #     ],
                                #
                                # )],
                                #     # className='one columns',
                                #     style={
                                #         'width': '10%',
                                #         #    'padding-left': '10',
                                #         #     #'margin-left': '3%',
                                #         'display': 'inline-block',
                                #         #     'float': 'right'
                                #     }
                                # ),
                                html.Div([dcc.Dropdown(
                                    id="Type_of_deal",
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

                            ],
                            className='row'
                        ),

                        html.Div(
                            [
                                dt.DataTable(
                                    rows=suspicious_deals_df.to_dict('records'),
                                    editable=False,
                                    row_selectable=False,
                                    # filterable=True,
                                    sortable=True,
                                    selected_row_indices=[],
                                    min_height=600,
                                )
                            ]
                        ),
                        # html.Div(id='sum',
                        #          style={'color': color.colliers_grey_10,
                        #         'background-color': color.colliers_dark_blue,
                        #         'fontSize': 14,
                        #         'border': 'solid 1px black',
                        #                 }
                        #          )
                    ],
                    className='ten columns',

                )

            ],
            style={'backgroundColor': color.colliers_grey_10}

        )
    ],
    style={'backgroundColor': color.colliers_pale_blue}
)

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
                        html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
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
                            html.Div(id='output-data-upload'),
                            # Hidden div inside the app that stores the intermediate value
                            html.Div(id='intermediate-value', style={'display': 'none'}
                                     ),
                            html.Table(id='table',style={'display': 'none'}),
                            html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
                        ]
                        )

                    ],
                    className='ten columns',
                    style={'display': 'inline'}
                    # style={'display': 'inline-block'}
                )

            ],
            style={'backgroundColor': color.colliers_grey_10}

        )
    ],
    style={'backgroundColor': color.colliers_pale_blue}
)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string + "==")

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv((io.StringIO(decoded.decode('utf-8'))), header=None)
            # df.columns = ['ID', 'Name', 'Info']
            # df.to_sql('update_test', con, if_exists='append', index=False)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
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
            json = df.to_json(date_format='iso', orient='records')
            #print(type(json))
                # df.columns = ['ID', 'Name', 'Info']
                # df.to_sql('update_test', con, if_exists='append', index=False)

        elif 'xls' in filename_save:
                # Assume that the user uploaded an excel file
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
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
        #print(type(children))
        return children


@app.callback(dash.dependencies.Output('table', 'children'),
              [dash.dependencies.Input('intermediate-value', 'children')]
              )
def update_table(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        print(type(jsonified_cleaned_data))
        print(jsonified_cleaned_data)
        dff = pd.read_json(jsonified_cleaned_data[0], orient='records')
        dff.columns = ['ID', 'Name', 'Info']
        print(dff)
        #print(dff.DataFrme(index=False))
        dff.to_sql('update_test', con, if_exists='append', index=False)
        return print('База обновлена')
    else:
        print('empty json')





# Обновление страницы
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
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


#help(dt.DataTable)

if __name__ == '__main__':
    app.run_server(debug=True)
