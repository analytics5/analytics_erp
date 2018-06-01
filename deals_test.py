import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import psycopg2 as pg
import numpy as np

dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = 'ZpZh2rgH'
conn = pg.connect(dbname=dbname, host=host, user=user, password=password)   #рисоединение к базе данных

query = """SELECT "Agency", "SQM"::numeric, "Year" 
            FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' """
with conn:
    cur = conn.cursor()
    cur.execute(query)  # выполнение SQL запроса
    colnames = [column[0] for column in cur.description]
    rows3 = cur.fetchall()  # чтение данных, полученных при запросе к базе
    #rows3.insert(0,colnames)
    df = pd.DataFrame(rows3)
    df.columns = [colnames]

#df1 = pd.read_excel('C:\\Users\\Public\\tms.xlsx')


years = ['2013', '2014', '2015', '2016', '2017']
app = dash.Dash()

app.layout = html.Div([
    html.H2("Market Share sat"),
    html.Div(
        [
            dcc.Dropdown(
                id="Year",
                options=[{
                    'label': i,
                    'value': i
                } for i in years],
                value='All years'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),

    dcc.Graph(id='funnel-graph'),


    #dcc.Slider(
        #id='year--slider',
        #min=years.min(),
        #max=years.max(),
        #value=df['Year'].max(),
        #step=None,
        #marks={str(year): str(year) for year in df['Year']})

])


@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     #dash.dependencies.Input('year--slider','value')
     ])
def update_graph(Year):
    if Year == "All years":
        df_plot = df.copy()
    else:
        df_plot = df[df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=len,
        fill_value=0)

    trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')], name='Colliers')
    trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')], name='SAR')
    trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')], name='JLL')
    trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')], name='CW')
    trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')], name='KF')
    trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')], name='CBRE')

    return {
        'data': [trace1, trace2, trace3, trace4,trace5, trace6],
        'layout':
        go.Layout(
            title='Deals in {}'.format(Year),
            barmode='stack')
    }

if __name__ == '__main__':
    app.run_server(debug=True)