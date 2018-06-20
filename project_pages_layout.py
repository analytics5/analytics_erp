import colors_and_fonts as color
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import project_static as static


# ОСНОВНАЯ СТРАНИЦА ПРИЛОЖЕНИЯ

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


# РАЗМЕТКА СТРАНИЦЫ 'MAIN'

def index_page():
    return html.Div([
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

def help_page():
    return html.Div([
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


# РАЗМЕТКА СТРАНИЦЫ 'ABOUT'

def about_page():
    return html.Div([
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


# РАЗМЕТКА СТРАНИЦЫ 'DEALS'

def deals_page():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Checklist(  # чеклист с одним значением для имитации дерева параметров
                                id='tree-checklist-columns',
                                # при выборе параметра, открывается список для отображения столбцов
                                options=[
                                    {'label': 'Select columns', 'value': 'Show'}
                                ],
                                values=[],
                                labelStyle={'display': 'block',
                                            'width': '192px',
                                            }
                            )
                        ],
                        style={
                            'display': 'inline',
                            'font-weight': 'bold'
                        }
                    ),

                    html.Div(
                        [
                            dcc.Checklist(  # чеклист для выбора столбцов в таблице
                                id='interface-columns',
                                options=[{'label': i, 'value': j} for i, j in  # все возможные значения
                                         zip(static.list_of_columns_for_gui, static.list_of_columns)],
                                values=['Agency', 'Country', 'City', 'Property_Name',
                                        # значения по умолчанию при первй загрузке страницы
                                        'Class', 'SQM', "Company", "Business_Sector",
                                        'Type_of_Deal', 'Type_of_Consultancy', 'Year', 'Quarter'],
                                labelStyle={
                                    'display': 'none',
                                    'padding-left:': '90px'
                                }
                            )
                        ],
                        style={
                            'display': 'inline'

                        }
                    ),

                    html.Div(
                        [
                            dcc.Checklist(  # чеклист с одним значением для дерева выбора графиков
                                id='tree-checklist-graphics',
                                # при выборе параметра, открывается список для отрисовки графиков
                                options=[
                                    {'label': 'Select graphics', 'value': 'Show'}
                                ],
                                values=[],
                                labelStyle={'display': 'block',
                                            'width': '192px',
                                            'font-weight': '300'
                                            }
                            )
                        ],
                        style={
                            'display': 'inline',
                            'font-weight': 'bold'
                        }
                    ),

                    html.Div(
                        [
                            dcc.Checklist(  # чеклист для выбора графиков на странице
                                id='interface-graphics',
                                options=[{'label': i, 'value': i} for i in  # все возможные значения из списка грфиков
                                         static.list_of_graphics_for_gui],
                                values=["Bar-stacked", "Bar-stacked-percent", "LLR,(E)TR, LLR/(E)TR-pie-2017-RU",
                                        'LLR,(E)TR, LLR/(E)TR-pie-1Q2018-RU', "LLR,(E)TR, LLR/(E)TR-pie-five-years-RU"],
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

                    html.Div(
                        [
                            dcc.Checklist(  # чеклист с одним значением для раскрытия дерева по типам сделок
                                id='tree-checklist-data',
                                # при выборе параметра, открывается список для выбора данных
                                options=[
                                    {'label': 'Select data', 'value': 'Show'}
                                ],
                                values=[],
                                labelStyle={'display': 'block',
                                            'width': '192px',
                                            'font-weight': '300'
                                            }
                            )
                        ],
                        style={
                            'display': 'inline',
                            'font-weight': 'bold'
                        }
                    ),

                    html.Div(
                        [
                            dcc.RadioItems(  # чеклист для выбора типов сделок
                                id='interface-data',
                                options=[{'label': i, 'value': i} for i in  # все возможные значения из списка типов сделок
                                         static.list_of_deals_type],
                                value="All deals",
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
                                                    for i in static.Agency_tab
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
                                                    for j in static.country_ind
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
                                                    for i in static.all_deals_query_df["City"].unique()
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
                                                    for i in static.all_deals_query_df["Property_Name"].unique()
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
                                                    for i in static.all_deals_query_df["Class"].unique()
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
                                                    for i in static.all_deals_query_df["SQM"].unique()
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
                                                    for i in static.all_deals_query_df["Company"].unique()
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
                                                    for i in static.all_deals_query_df["Business_Sector"].unique()
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
                                                    for i in static.all_deals_query_df["Type_of_Deal"].unique()
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
                                                    for i in static.all_deals_query_df["Type_of_Consultancy"].unique()
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
                                                    for i in static.all_deals_query_df["LLR_TR"].unique()
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
                                                    for i in static.years
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
                                                    for i in static.all_deals_query_df["Quarter"].unique()
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
                                                    for i in
                                                    static.all_deals_query_df["Include_in_Market_Share"].unique()

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
                                                    for i in static.all_deals_query_df["Address"].unique()

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
                                                    for i in static.all_deals_query_df["Submarket_Large"].unique()

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
                                                    for i in static.all_deals_query_df["Owner"].unique()

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
                                                    for i in static.all_deals_query_df["Date_of_acquiring"].unique()

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
                                                    for i in static.all_deals_query_df["Class_Colliers"].unique()

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
                                                    for i in static.all_deals_query_df["Floor"].unique()

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
                                                    for i in static.all_deals_query_df["Deal_Size"].unique()

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
                                                    for i in static.all_deals_query_df["Sublease_Agent"].unique()

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
                                                    for i in static.all_deals_query_df["LLR_Only"].unique()

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
                                                    for i in static.all_deals_query_df["E_TR_Only"].unique()

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
                                                    for i in static.all_deals_query_df["LLR/E_TR"].unique()

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
                                                    for i in static.all_deals_query_df["Month"].unique()

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
                            html.Div(id='sum-string',
                                     style={'color': color.colliers_grey_10,
                                            'background-color': color.colliers_dark_blue,
                                            'fontSize': 14,
                                            #'border': 'solid 1px black',
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

                            #  _____________________________________________________________________________________________________________#

                            html.Div(                           # pie 2017 по России + таблицы
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id='LLR,(E)TR, LLR/(E)TR-pie-2017-RU',
                                                      style={'display': 'none',
                                                             'padding': '40px 0px 0px 0px'}),
                                            html.Div(id='pie-4-text',
                                                     children='LLR,(E)TR and LLR/(E)TR deals in Russia in 2017',
                                                     style={'padding-left': '50px',
                                                            'display': 'none'}
                                                     ),
                                        ],
                                        className='four columns',

                                    ),

                                    html.Div(                        # div с таблицей по ключевым сделкам 2017 Россия
                                        [
                                            html.H4(
                                                children='Ключевые сделки, 2017',
                                                style={
                                                    'padding-left': '670px',
                                                    #'textAlign': 'left',
                                                    'color': color.colliers_color
                                                }
                                            ),
                                            html.H6(
                                                children='Россия',
                                                style={
                                                     'padding-left': '670px',
                                                    #'textAlign': 'center',
                                                    'color': color.colliers_light_blue
                                                }
                                            ),
                                            html.Div(id='html-tab-RU-2017',
                                                     style={
                                                         # 'width': '30.3%',
                                                         #        'display': 'row',
                                                         'float': 'right'}
                                                     ),
                                        ],
                                        #className='six columns',
                                    ),
                                ],
                                className='twelve columns'
                            ),

                            #  _______________________________________________________________________________________#

                            html.Div(  # pie 1q2018 по России + таблицы
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id='LLR,(E)TR, LLR/(E)TR-pie-1Q2018-RU',
                                                      style={'display': 'none'}),
                                            html.Div(id='pie-5-text',
                                                     children='LLR,(E)TR and LLR/(E)TR deals in Russia in 1Q 2018',
                                                     style={'padding-left': '50px',
                                                            'display': 'none'}
                                                     ),
                                        ],
                                        className='four columns',

                                    ),

                                    html.Div(  # div с таблицей по ключевым сделкам 1q2018 Россия
                                        [
                                            html.H4(
                                                children='Ключевые сделки, I кв. 2018',
                                                style={
                                                     'padding-left': '670px',
                                                    #'textAlign': 'center',
                                                    'color': color.colliers_color
                                                }
                                            ),
                                            html.H6(
                                                children='Россия',
                                                style={
                                                     'padding-left': '670px',
                                                    #'textAlign': 'center',
                                                    'color': color.colliers_light_blue
                                                }
                                            ),
                                            html.Div(id='html-tab-RU-1q2018',
                                                     style={
                                                         # 'width': '30.3%',
                                                         #        'display': 'row',
                                                         'float': 'right'}
                                                     ),
                                        ],
                                        # className='six columns',
                                    ),
                                ],
                                className='twelve columns'
                            ),

                            #  _______________________________________________________________________________________#

                            html.Div(  # pie 2013-2018 по России + таблицы
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id='LLR,(E)TR, LLR/(E)TR-pie-five-years-RU',
                                                      style={'display': 'none'}),
                                            html.Div(id='pie-6-text',
                                                     children='LLR,(E)TR and LLR/(E)TR deals in Russia in 2013-2018 years',
                                                     style={'padding-left': '50px',
                                                            'display': 'none'}
                                                     ),
                                        ],
                                        className='four columns',

                                    ),

                                    html.Div(  # div с таблицей по ключевым сделкам 1q2018 Россия
                                        [
                                            html.H4(
                                                children='Ключевые сделки, 2013-2018',
                                                style={
                                                     'padding-left': '670px',
                                                    #'textAlign': 'center',
                                                    'color': color.colliers_color
                                                }
                                            ),
                                            html.H6(
                                                children='Россия',
                                                style={
                                                     'padding-left': '670px',
                                                    #'textAlign': 'center',
                                                    'color': color.colliers_light_blue
                                                }
                                            ),
                                            html.Div(id='html-tab-RU-five-years',
                                                     style={
                                                         # 'width': '30.3%',
                                                         #        'display': 'row',
                                                         'float': 'right'}
                                                     ),
                                        ],
                                        # className='six columns',
                                    ),
                                ],
                                className='twelve columns'
                            ),


#  _______________________________________________________________________________________________________________#

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Graph(id='LLR,(E)TR, LLR/(E)TR-pie-2017-MOS',
                                                      style={'display': 'none'}),
                                            html.Div(id='pie-7-text',
                                                     children='LLR,(E)TR and LLR/(E)TR deals in Moscow in 2017',
                                                     style={'padding-left': '50px',
                                                            'display': 'none'}
                                                     )
                                        ],
                                        className='four columns',
                                        # style={'width': '30.3%',
                                        #        'display': 'row',
                                        #        'float': 'left'}
                                    ),
                                    html.Div(
                                        [
                                            dcc.Graph(id='LLR,(E)TR, LLR/(E)TR-pie-1Q2018-MOS',
                                                      style={'display': 'none'}),
                                            html.Div(id='pie-8-text',
                                                     children='LLR,(E)TR and LLR/(E)TR deals in Moscow in 1Q 2018',
                                                     style={'padding-left': '50px',
                                                            'display': 'none'}
                                                     )

                                        ],
                                        className='four columns',
                                        # style={'width': '30.3%',
                                        #        'display': 'row',
                                        #        'float': 'left'}
                                    ),
                                    html.Div(
                                        [
                                            dcc.Graph(id='LLR,(E)TR, LLR/(E)TR-pie-five-years-MOS',
                                                      style={'display': 'none'}),
                                            html.Div(id='pie-9-text',
                                                     children='LLR,(E)TR and LLR/(E)TR deals in Moscow in 2013-2018 years',
                                                     style={'padding-left': '50px',
                                                            'display': 'none'}
                                                     )
                                        ],
                                        className='four columns',
                                        # style={'width': '30.3%',
                                        #        'display': 'row',
                                        #        'float': 'left'}
                                    ),
                                ],
                                className='twelve columns'
                            ),


                            html.Div(
                                [
                                    dcc.Graph(id='biggest-deal-tab-2017',
                                           style={'display': 'none'})
                                 ],
                                className='four columns'),




                            html.Div(
                                [
                                    html.Div(
                                        [
                                            # dcc.Slider(  # настройка ширины графика
                                            #     id='market-graph-tab-slider-width',
                                            #     min=1,
                                            #     max=1000,
                                            #     step=5,
                                            #     value=700,
                                            #     marks={
                                            #         700: {'label': '700px', 'style': {'color': color.colliers_color}},
                                            #     },
                                            #
                                            # ),
                                            # html.Br(),
                                            # dcc.Slider(  # настройка высоты графика
                                            #     id='market-graph-tab-slider-height',
                                            #     min=1,
                                            #     max=1000,
                                            #     step=5,
                                            #     value=500,
                                            #     marks={
                                            #         500: {'label': '500px', 'style': {'color': color.colliers_color}},
                                            #     }
                                            # ),
                                            html.Br(),
                                            dcc.Graph(id='market-graph-tab', style={'display': 'inline-block'}),
                                            html.H6(id='market-graph-tab-string', style={'display': 'none'}),
                                            dcc.Graph(id='market-graph-non-stack-tab', style={'display': 'none'}),
                                            dcc.Graph(id='market-graph-horizontal-tab', style={'display': 'none'}),
                                        ],
                                        className='six columns',
                                        # style={'backgroundColor': color.colliers_pale_blue,
                                        #       'display': 'inline-block'
                                        #       }
                                    ),
                                    html.Div(
                                        [
                                            # html.Img(id='market-graph-tab-png'),
                                            # dcc.Graph(id='all-years-horizontal'),
                                            dcc.Graph(id='market-pie-graph-tab', style={'display': 'none'}),
                                            dcc.Graph(id='market-graph-percent-tab', style={'inline-block': 'none'}),
                                            dcc.Graph(id='market-graph-horizontal-total-tab', style={'display': 'none'})
                                        ],
                                        className='six columns',
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


# РАЗМЕТКА СТРАНИЦЫ 'SUSPICIOUS_DEALS'

def suspicious_deals_page():
    return html.Div(
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
                                         zip(static.list_of_columns_for_gui, static.list_of_columns)],
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
                                                    for i in static.Agency_tab
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
                                                    for j in static.country_ind
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
                                                    for i in static.all_deals_query_df["City"].unique()
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
                                                    for i in static.all_deals_query_df["Property_Name"].unique()
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
                                                    for i in static.all_deals_query_df["Class"].unique()
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
                                                    for i in static.all_deals_query_df["SQM"].unique()
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
                                                    for i in static.all_deals_query_df["Company"].unique()
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
                                                    for i in static.all_deals_query_df["Business_Sector"].unique()
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
                                                    for i in static.all_deals_query_df["Type_of_Deal"].unique()
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
                                                    for i in static.all_deals_query_df["Type_of_Consultancy"].unique()
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
                                                    for i in static.all_deals_query_df["LLR_TR"].unique()
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
                                                    for i in static.years
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
                                                    for i in static.all_deals_query_df["Quarter"].unique()
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
                                                    for i in
                                                    static.all_deals_query_df["Include_in_Market_Share"].unique()

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
                                                    for i in static.all_deals_query_df["Address"].unique()

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
                                                    for i in static.all_deals_query_df["Submarket_Large"].unique()

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
                                                    for i in static.all_deals_query_df["Owner"].unique()

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
                                                    for i in static.all_deals_query_df["Date_of_acquiring"].unique()

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
                                                    for i in static.all_deals_query_df["Class_Colliers"].unique()

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
                                                    for i in static.all_deals_query_df["Floor"].unique()

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
                                                    for i in static.all_deals_query_df["Deal_Size"].unique()

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
                                                    for i in static.all_deals_query_df["Sublease_Agent"].unique()

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
                                                    for i in static.all_deals_query_df["LLR_Only"].unique()

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
                                                    for i in static.all_deals_query_df["E_TR_Only"].unique()

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
                                                    for i in static.all_deals_query_df["LLR/E_TR"].unique()

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
                                                    for i in static.all_deals_query_df["Month"].unique()

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


# РАЗМЕТКА СТРАНИЦЫ 'ОБНОВИТЬ БАЗУ'

def update_database():
    return html.Div(
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
