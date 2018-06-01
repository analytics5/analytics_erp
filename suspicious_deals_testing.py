import dash
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


suspicious_deals = """SELECT "Agency":: text, "Country":: text, "City":: text, "Property_Name", "SQM"::real, "Company"::text, "Type_of_Consultancy","Year"::text, "Quarter"::text
                      FROM "Market_Share"
                      
                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'
                      AND "SQM"::real IN (SELECT "SQM"::real
                      FROM "Market_Share"
                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'
                      
                      GROUP BY "Year", "Agency", "SQM"
                      HAVING count(*)>1)
                      ORDER BY "SQM" DESC """

suspicious_deals_1 = """SELECT "Agency":: text, "Country":: text, "City":: text, "Property_Name", "Class"::text,"SQM"::real, "Company"::text,"Year"::text, "Quarter"::text
                      FROM "Market_Share"
                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' 
                      AND "SQM"::real IN ( SELECT "SQM"::real
                      FROM "Market_Share"
                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'
                      GROUP BY "Agency","SQM"
                      HAVING count(*)>1)
                      ORDER BY "SQM" """



dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = '3334'
conn = pg.connect(dbname=dbname, host=host, user=user, password=password)  # рисоединение к базе данных

with conn:

    cur = conn.cursor()
    all_deals_query = sql.table_query
    cur.execute(all_deals_query)  # выполнение SQL запроса по сделкам
    all_deals_data = cur.fetchall()  # данные по сделкам

    all_deals_query_df = pd.DataFrame(all_deals_data)



    print('TEST DEALS')

    cur.execute(suspicious_deals)  # выполнение SQL запроса по сделкам
    suspicious_deals_data = cur.fetchall()  # данные по сделкам
    suspicious_deals_df = pd.DataFrame(suspicious_deals_data)  # Запись в датафрейм
    suspicious_deals_df.columns = ['Agency', 'Country', 'City', 'Property Name', 'SQM', 'Company','Type_of_Consultancy', 'Year',
                              'Quarter']
    all_deals_query_df.columns = ['Agency', 'Country', 'City', 'Property Name', 'Class', 'SQM', 'Company',
                                  'Type_of_Consultancy', 'Year', 'Quarter']


app = dash.Dash()

app.config.suppress_callback_exceptions = True
app.css.append_css({'external_url': 'https://cdn.rawgit.com/Wittgensteen/work_stuff/master/base_style.css'})    # мой файл с гитхаба на rawgit

years = ("All years", "2013", "2014", "2015", "2016", "2017", "2018")
Agency = ("All agency","Colliers", "KF", "JLL", "CW", "SAR", "CBRE")

country = ("All countries","Russia", "Ukraine", "Belarus","Kazakhstan ","Azerbaijan")
country_ind = ("All countries", "RU", "UA", "BY", "KZ", "AZ")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
],
    style={'backgroundColor': color.colliers_dark_blue,}
)


deals_content = html.Div(
    [
        html.H3(children="База данных по сделкам 1",
                className='row',
                style={'textAlign': 'center','color': color.colliers_pale_blue
                       }
                ),


        html.Div(
            [
                html.A(html.Button('Показать все сделки',className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }),
                       href='/all_deals_1'
                       ),
                html.A(html.Button('Показать спорные сделки', className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }
                            ), href='/all_deals_2'),


                html.A(html.Button('Дропдаун', className='button-primary', style={
                    'display': 'inline',
                    'height': '38px',
                    'padding': '0 15px',
                    # 'color': '#FFF',
                    # 'text-align': 'center',
                    # 'font-size': '11px',
                    # 'font-weight': '600',
                    # 'line-height': '38px',
                    # 'letter-spacing': '.1rem',
                    # 'text-transform': 'uppercase',
                    # 'text-decoration': 'none',
                    # 'white-space': 'nowrap',
                    # 'background-color': '#33C3F0',
                    # 'border-radius': '4px',
                    'border': '1px solid #ffc425',
                    # 'cursor': 'pointer',
                    # 'box-sizing': 'border-box'
                }),
                       href='/all_deals_drop'
                       ),

            ]
        ),

        html.Br(),

        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    ],
    style={'backgroundColor': color.colliers_dark_blue}
)


suspicious_deals_layout = html.Div(
    [
        html.H3(children="База данных по сделкам 1",
                className='row',
                style={'textAlign': 'center','color': color.colliers_pale_blue
                       }
                ),


        html.Div(
            [
                html.A(html.Button('Показать все сделки', n_clicks=0,className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }), href='/all_deals_1'),
                html.A(html.Button('Показать спорные сделки', className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }
                            ), href='/all_deals_2')

            ]
        ),

        html.Br(),

        html.Div(
            [
                dt.DataTable(
                    rows=suspicious_deals_df.to_dict('records'),
                    # row_selectable=True,
                    filterable=True,
                    sortable=True,
                    editable=False,
                )
            ]
        ),
    ],
    style={'backgroundColor': color.colliers_dark_blue}
)


all_deals_layout = html.Div(
    [
        html.H3(children="База данных по сделкам 2",
                className='row',
                style={'textAlign': 'center','color': color.colliers_pale_blue
                       }
                ),


        html.Div(
            [
                html.A(html.Button('Показать все сделки', n_clicks=0, id='all_deals_button',className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }), href='/all_deals_1'),
                html.A(html.Button('Показать спорные сделки', n_clicks=0, id='suspicious_deals_button', className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }
                            ), href='/all_deals_2')

            ]
        ),

        html.Br(),

        html.Div(
            [
                dt.DataTable(
                    rows=all_deals_query_df.to_dict('records'),
                    # row_selectable=True,
                    filterable=True,
                    sortable=True,
                    editable=False,
                )
            ]
        ),
    ],
    style={'backgroundColor': color.colliers_dark_blue}
)


all_deals_drop_layout = html.Div(
    [
        html.H3(children="База данных по сделкам 2",
                className='row',
                style={'textAlign': 'center','color': color.colliers_pale_blue
                       }
                ),


        html.Div(
            [
                html.A(html.Button('Показать все сделки', n_clicks=0, id='all_deals_button',className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }), href='/all_deals_1'),
                html.A(html.Button('Показать спорные сделки', n_clicks=0, id='suspicious_deals_button', className='button-primary',style={
                                'display': 'inline',
                               'height': '38px',
                               'padding': '0 15px',
                               # 'color': '#FFF',
                               # 'text-align': 'center',
                               # 'font-size': '11px',
                               # 'font-weight': '600',
                               # 'line-height': '38px',
                               # 'letter-spacing': '.1rem',
                               # 'text-transform': 'uppercase',
                               # 'text-decoration': 'none',
                               # 'white-space': 'nowrap',
                               # 'background-color': '#33C3F0',
                               # 'border-radius': '4px',
                               'border': '1px solid #ffc425',
                               # 'cursor': 'pointer',
                               # 'box-sizing': 'border-box'
                               }
                            ), href='/all_deals_2'),
            ]
        ),

        html.Div(
            [
                html.Div([dcc.Dropdown(
                    id="Year",
                    # multi=True,
                    #value='All years',
                    placeholder="Год",
                    options=[{
                        'label': i,
                        'value': i
                    }
                        for i in years
                    ],

                )],
                    #className='two columns',
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
                    #value='All countries',
                    placeholder="Страна",
                    # multi=True,
                    options=[{
                        'label': j,
                        'value': j
                    }
                        for j in country_ind

                    ],

                )],
                    #className='two columns',
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
                    #value='All agency',
                    placeholder="Агентство",
                    # multi=True,
                    options=[{
                        'label': i,
                        'value': i
                    }
                        for i in Agency
                    ],

                )],
                    #className='one columns',
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

        html.Div(id='sum',
                 style={'color': color.colliers_grey_10, 'fontSize': 14}),

        html.Br(),

        html.Div(
            [
                dt.DataTable(
                    rows=[{}],  # initialise the row
                    editable=False,
                    row_selectable=False,
                    #filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    min_height=800,
                    id='datatable'
                )
            ]
        ),




    ],
    style={'backgroundColor': color.colliers_dark_blue}
)


@app.callback(dash.dependencies.Output('datatable', 'rows'),
              [dash.dependencies.Input('Year', 'value'),
               dash.dependencies.Input('Country', 'value'),
               dash.dependencies.Input('Agency', 'value')
               ])
def update_datatable (Year, Country, Agency):

    if Year == None and Country == None and Agency == None:
        return all_deals_query_df.to_dict('records')

    elif Year == "All years" and Country == "All countries" and Agency == "All agency":
        #pd.DataFrame([],[]).to_dict('records')
        return all_deals_query_df.to_dict('records')

    elif Year == "All years"  and Country == Country and Agency == "All agency":
        #pd.DataFrame.to_dict('records')
        return all_deals_query_df[all_deals_query_df['Country'].isin([Country])].to_dict('records')

    elif Year == "All years"  and Country == Country and Agency == Agency:
        #pd.DataFrame.to_dict('records')
        return all_deals_query_df[all_deals_query_df['Agency'].isin([Agency]) & (all_deals_query_df['Country'].isin([Country]))].to_dict('records')

    elif Year == Year and Country == "All countries" and Agency == "All agency":
        #pd.DataFrame.to_dict('records')
        return all_deals_query_df[(all_deals_query_df['Year'].isin([Year]))].to_dict('records')

    elif Year == Year and Country == Country and Agency == "All agency":
        #pd.DataFrame.to_dict('records')
        #print(type(Year))
        return all_deals_query_df[(all_deals_query_df['Year'].isin([Year])) & (all_deals_query_df['Country'].isin([Country]))].to_dict('records')

    elif Year == Year and Country == "All countries" and Agency == Agency:
        #pd.DataFrame.to_dict('records')
        return all_deals_query_df[(all_deals_query_df['Year'].isin([Year])) & (all_deals_query_df['Agency'].isin([Agency]))].to_dict('records')

    elif Year == "All years" and Country == "All countries" and Agency == Agency:                   #не работает!!!!!!!!!!!
        #pd.DataFrame.to_dict('records')
        return all_deals_query_df[(all_deals_query_df['Agency'].isin([Agency]))].to_dict('records')

    elif Year == Year and Country == Country and Agency == Agency:
        #pd.DataFrame.to_dict('records')
        return all_deals_query_df[(all_deals_query_df['Year'].isin([Year])) & (all_deals_query_df['Agency'].isin([Agency]))& (all_deals_query_df['Country'].isin([Country]))].to_dict('records')

    else:
        return all_deals_query_df.to_dict('records')


@app.callback(dash.dependencies.Output('sum', 'children'),
              [dash.dependencies.Input('Year', 'value'),
               dash.dependencies.Input('Country', 'value'),
               dash.dependencies.Input('Agency', 'value')
               ])
def update_datatable(Year, Country, Agency):


    if Year == None and Country == None and Agency == None:
        data_sum = all_deals_query_df["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    if Year == "All years" and Country == "All countries" and Agency == "All agency":
        data_sum = all_deals_query_df["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    elif Year == "All years" and Country == Country and Agency == "All agency":
        data = all_deals_query_df[all_deals_query_df['Country'].isin([Country])]
        data_sum = data["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    elif Year == "All years" and Country == Country and Agency == Agency:

        data = all_deals_query_df[all_deals_query_df['Agency'].isin([Agency]) & (all_deals_query_df['Country'].isin([Country]))]
        data_sum = data["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    elif Year == Year and Country == "All countries" and Agency == "All agency":

        data = all_deals_query_df[(all_deals_query_df['Year'].isin([Year]))]
        data_sum = data["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    elif Year == Year and Country == Country and Agency == "All agency":

        data = all_deals_query_df[(all_deals_query_df['Year'].isin([Year])) & (all_deals_query_df['Country'].isin([Country]))]
        data_sum = data["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    elif Year == Year and Country == "All countries" and Agency == Agency:

        data = all_deals_query_df[(all_deals_query_df['Year'].isin([Year])) & (all_deals_query_df['Agency'].isin([Agency]))]
        data_sum = data["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    elif Year == "All years" and Country == "All countries" and Agency == Agency:                   #не работает!!!!!!!!!!!
        return all_deals_query_df[(all_deals_query_df['Agency'].isin([Agency]))]

    elif Year == Year and Country == Country and Agency == Agency:

        data = all_deals_query_df[(all_deals_query_df['Year'].isin([Year])) & (all_deals_query_df['Agency'].isin([Agency]))& (all_deals_query_df['Country'].isin([Country]))]
        data_sum = data["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

    else:
        data = all_deals_query_df[all_deals_query_df['Year'].isin([Year])]
        data_sum = data["SQM"].sum()
        return 'Суммарная площадь составляет ', round(data_sum), ' кв.м'

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [
                  dash.dependencies.Input('url', 'pathname'),
                  #dash.dependencies.Input('all_deals_button', 'pathname'),
                  #dash.dependencies.Input('suspicious_deals_button', 'pathname')
              ]
)
def display_page(pathname):
    if pathname == '/all_deals_1':
        return suspicious_deals_layout
    elif pathname == '/all_deals_2':
        return all_deals_layout
    elif pathname == '/all_deals_drop':
        return all_deals_drop_layout
    else:
        return deals_content
    # You could also return a 404 "URL not found" page here  all_deals_drop


if __name__ == '__main__':
    app.run_server(debug=True)
