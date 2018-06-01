import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import psycopg2 as pg
import numpy as np
import colors_and_fonts as color

dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = '3334'
conn = pg.connect(dbname=dbname, host=host, user=user, password=password)   #рисоединение к базе данных

query = """SELECT "Agency"::text, "SQM"::real, "Year"::text 
            FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Country"='RU' AND "Include_in_Market_Share"='Y'"""
with conn:
    cur = conn.cursor()
    cur.execute(query)  # выполнение SQL запроса
    colnames = [column[0] for column in cur.description]
    rows3 = cur.fetchall()  # чтение данных, полученных при запросе к базе
    #rows3.insert(0,colnames)
    df = pd.DataFrame(rows3)
    #df.columns = [colnames]
    df.columns = ['Agency', 'SQM','Year']

print(df)

#df1 = pd.read_excel('C:\\Users\\Public\\tms.xlsx')

years = ("All years","2013","2014","2015","2016","2017")

app = dash.Dash()

app.layout = html.Div(style={'backgroundColor': color.colliers_dark_blue, 'display': 'inline-block'}, children=

    [html.H2(children="Market Share",
            style={'textAlign': 'center',
            'color': color.colliers_pale_blue}),
    html.Div(
        [
            dcc.Dropdown(
                id="Year",
                options=[{
                    'label': i,
                    'value': i
                } for i in years],
                #multi=True,
                value='All years'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),

            html.Div([
                dcc.Graph(
                    id='market-graph')],
                    style={'width': '100%'}),

           html.Div([dcc.Graph(id='market-graph-horizontal'),
                     dcc.Graph(id='market-pie-graph'),
                     dcc.Graph(id='market-graph-percent'),
                     dcc.Graph(id='market-graph-horizontal-total')],
                style={'display': 'inline-block', 'width': '50%'})
])

@app.callback(
    dash.dependencies.Output('market-graph', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
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
        aggfunc=sum,
        fill_value=0)

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
        'data': [trace1, trace2, trace3, trace4,trace5, trace6],
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
            width=800,
            height=600,
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
    dash.dependencies.Output('market-pie-graph', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
     ]
)
def update_pie_graph(Year):
    if Year == "All years":
        df_plot2 = df.copy()
    else:
        df_plot2 = df[df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot2,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    colors = [color.colliers_grey_40,color.colliers_extra_light_blue, color.colliers_dark_blue,color.colliers_yellow,
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
    'data':[pie1],
    'layout':go.Layout(
            title='Deals in {}'.format(Year),
            width=800,
            height=600,
        )
    }



@app.callback(
    dash.dependencies.Output('market-graph-horizontal', 'figure'),
    [dash.dependencies.Input('Year', 'value'),
 ])
def update_graph_horizontal(Year):
    if Year == "All years":
        df_plot = df.copy()
    else:
        df_plot = df[df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    trace1 = go.Bar(y=pv.index, x=pv[("SQM", 'Colliers')], name='Colliers', marker=dict(
        color=color.colliers_dark_blue), width=0.2, orientation = 'h')
    trace2 = go.Bar(y=pv.index, x=pv[("SQM", 'SAR')], name='SAR', marker=dict(
        color=color.colliers_light_blue), width=0.2, orientation = 'h')
    trace3 = go.Bar(y=pv.index, x=pv[("SQM", 'CW')], name='CW', marker=dict(
        color=color.colliers_extra_light_blue), width=0.2, orientation = 'h')
    trace4 = go.Bar(y=pv.index, x=pv[("SQM", 'CBRE')], name='CBRE', marker=dict(
        color=color.colliers_grey_40), width=0.2, orientation = 'h')
    trace5 = go.Bar(y=pv.index, x=pv[("SQM", 'JLL')], name='JLL', marker=dict(
        color=color.colliers_yellow), width=0.2, orientation = 'h')
    trace6 = go.Bar(y=pv.index, x=pv[("SQM", 'KF')], name='KF', marker=dict(
        color=color.colliers_red), width=0.2, orientation = 'h')
    return {
        'data': [trace1, trace2, trace3, trace4,trace5, trace6],
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

            width=800,
            height=600,
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

            barmode='stack')
    }




@app.callback(
    dash.dependencies.Output('market-graph-percent', 'figure'),
    [dash.dependencies.Input('Year','value'),
     ]
)
def update_graph_percent(Year):
    if Year == "All years":
        df_plot = df.copy()

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
            color=color.colliers_light_blue), width=0.2,text='%')
        trace3 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum(), name='CW', marker=dict(
            color=color.colliers_extra_light_blue), width=0.2,text='%')
        trace4 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum(), name='CBRE', marker=dict(
            color=color.colliers_grey_40), width=0.2,text='%')
        trace5 = go.Bar(x=pv1.index, y=pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum(), name='JLL', marker=dict(
            color=color.colliers_yellow), width=0.2,text='%')
        trace6 = go.Bar(x=pv1.index, y=pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum(), name='KF', marker=dict(
            color=color.colliers_red), width=0.2,text='%')
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
                    width=800,
                    height=600,
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
        df_plot = df[df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    #print(pv("SQM").sum())
    trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')]*100/pv.values.sum(), name='Colliers', marker=dict(
        color=color.colliers_dark_blue), width=0.2,text='%')
    trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')]*100/pv.values.sum(), name='SAR', marker=dict(
        color=color.colliers_light_blue), width=0.2,text='%')
    trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')]*100/pv.values.sum(), name='CW', marker=dict(
        color=color.colliers_extra_light_blue), width=0.2,text='%')
    trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')]*100/pv.values.sum(), name='CBRE', marker=dict(
        color=color.colliers_grey_40), width=0.2,text='%')
    trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')]*100/pv.values.sum(), name='JLL', marker=dict(
        color=color.colliers_yellow), width=0.2,text='%')
    trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')]*100/pv.values.sum(), name='KF', marker=dict(
        color=color.colliers_red), width=0.2,text='%')

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
                    width=800,
                    height=600,
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
 ])
def update_graph_horizontal_total(Year):
    if Year == "All years":
        df_plot = df.copy()
    else:
        df_plot = df[df['Year'] == Year]

    pv = pd.pivot_table(
        df_plot,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    trace1 = go.Bar(y=pv.index, x=pv[("SQM")], marker=dict(
        color=color.colliers_dark_blue), width=0.2, orientation = 'h')
    return {
        'data': [trace1],
        'layout':
        go.Layout(
            title='Deals in 2013-2017',
            autosize=False,
            bargap=0.3,
            bargroupgap=0,
            font=dict(
                color=color.colliers_grey_80,
                family='Arial',
                size=12),

            width=800,
            height=600,
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

#print(sorted(df['Agency'].unique()))



if __name__ == '__main__':
    app.run_server(debug=True)