import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import plotly.graph_objs as go
import pandas as pd
import psycopg2 as pg
import numpy as np
import colors_and_fonts as color
import App_sql_queries as sql
import plotly as pt


dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = '3334'
conn = pg.connect(dbname=dbname, host=host, user=user, password=password)  # рисоединение к базе данных

deals_query = sql.deals_query
tenant_rep_query = sql.tenant_rep_query
llr_query = sql.llr_query

sale_lease_query = sql.sale_lease_query
sale_lease_query_sale = sql.sale_lease_query_sale
sale_lease_query_lease = sql.sale_lease_query_lease


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

    #cur.execute(select_all)  # выполнение SQL запроса по типу сделок Sale/Lease по lease
    #select_all_data = cur.fetchall()
    #select_all_df = pd.DataFrame(select_all_data)

    deals_df.columns = ['Agency', 'SQM', 'Year']
    tenant_df.columns = ['Agency', 'SQM', 'Year']
    llr_df.columns = ['Agency', 'SQM', 'Year']

    sale_lease_df.columns = ['Agency', 'SQM', 'Year', 'Type_of_deal']
    sale_lease_lease_df.columns = ['Agency', 'SQM', 'Year', 'Type_of_deal']
    sale_lease_sale_df.columns = ['Agency', 'SQM', 'Year', 'Type_of_deal']

    #select_all_df.columns = ['Include_in_Market_Share','Agency','Country','City','Property_Name','Address', 'Submarket_Large', 'Owner', 'Date_of_acquiring', 'Class',  ]


# print(deals_df)
# print(tenant_df)
# print(llr_df)
# print(sale_lease_df)
# print(sale_lease_sale_df)
# print(sale_lease_lease_df)


years = ("All years", "2013", "2014", "2015", "2016", "2017")

app = dash.Dash()

#app.css.config.serve_locally = True  # css с локалки, не работает
#app.css.append_css({'external_url': 'C:\\Users\\Yury.Festa\\PycharmProjects\\WEB_APP_FOR_INTEGIS\\style.css'})    # пока не работает
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})   # что-то абстрактное из сети

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})    # то, что предлагают плотли


app.layout = html.Div(
    [
          html.Div(
              children="Market Share (localhost)",
              className='row',
              style={'textAlign': 'center',
                     'color': color.colliers_pale_blue
                     }
          ),

          html.Div(
              [
                  dcc.Dropdown(
                      id="Year",
                      options=[
                          {
                              'label': i,
                              'value': i
                          }
                          for i in years
                      ],
                      value='All years'
                  )
              ],
              className='row',
              style={'width': '25%',
              #       'display': 'inline-block'
                    }
          ),

          html.Div(
              [
                  html.Div(
                      [
                          dcc.Graph(id='market-graph'),
                          dcc.Graph(id='market-graph-horizontal'),
                          dcc.Graph(id='market-pie-graph'),
                          dcc.Graph(id='llr-representation-pie'),
                          dcc.Graph(id='llr-representation-bar'),
                          dt.DataTable(
                              rows=sale_lease_df.to_dict('records'),
                              #row_selectable=True,
                              filterable=True,
                              sortable=True,
                          )
                      ],
                      className='six columns',
                      #style={'width': '46.75%',
                      #       #'margin-left': '0',
                      #       'display': 'inline-block',
                      #       'float': 'left'
                      #       }
                  ),

                  html.Div(
                       [
                           dcc.Graph(id='market-graph-percent'),
                           dcc.Graph(id='market-graph-horizontal-total'),
                           dcc.Graph(id='tenant-representation-pie'),
                           dcc.Graph(id='tenant-representation-bar'),
                           dcc.Graph(id='sale-lease-horizontal'),
                          #dcc.Graph(id='sale-lease-vertical')
                       ],
                       className='six columns',
                       #style={
                       #    'width': '46.75%',
                       #    'padding-left': '10',
                       #     #'margin-left': '3%',
                       #     'display': 'inline-block',
                       #     'float': 'right'
                       #     }

                  )
              ],
              className='row',
              #style={
              #       'display': 'inline-block '
              #       }
          ),
    ],
    style={'backgroundColor': color.colliers_dark_blue}
)


@app.callback(
    dash.dependencies.Output('market-graph', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_graph(Year):
    if Year == "All years":
        df_plot = deals_df.copy()
    else:
        df_plot = deals_df[deals_df['Year'] == Year]

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
                width=750,
                height=550,
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
    [dash.dependencies.Input('Year', 'value')])
def update_pie_graph(Year):
    if Year == "All years":
        df_plot2 = deals_df.copy()
    else:
        df_plot2 = deals_df[deals_df['Year'] == Year]

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
            width=750,
            height=550,
        )
    }


@app.callback(
    dash.dependencies.Output('market-graph-horizontal', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_graph_horizontal(Year):
    if Year == "All years":
        df_plot = deals_df.copy()
    else:
        df_plot = deals_df[deals_df['Year'] == Year]

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
                    text='1000000000000000000000000 %',
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

                width=750,
                height=550,
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
    dash.dependencies.Output('market-graph-percent', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_graph_percent(Year):
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
                    width=750,
                    height=550,
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
                width=750,
                height=550,
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
    [dash.dependencies.Input('Year', 'value')])
def update_graph_horizontal_total(Year):
    if Year == "All years":
        df_plot = deals_df.copy()
    else:
        df_plot = deals_df[deals_df['Year'] == Year]

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

                width=750,
                height=550,
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


@app.callback(
    dash.dependencies.Output('tenant-representation-pie', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_tenant_representation(Year):
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
            width=750,
            height=550,
        )
    }


@app.callback(
    dash.dependencies.Output('llr-representation-pie', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_llr_representation(Year):
    if Year == "All years":
        df_plot2 = llr_df.copy()
    else:
        df_plot2 = llr_df[tenant_df['Year'] == Year]

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
            width=750,
            height=550,
        )
    }


@app.callback(
    dash.dependencies.Output('tenant-representation-bar', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_tenant_representation_bar(Year):
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
                width=750,
                height=550,
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
    dash.dependencies.Output('llr-representation-bar', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_llr_representation_bar(Year):
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
                    width=750,
                    height=550,
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
                width=750,
                height=550,
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
    dash.dependencies.Output('sale-lease-horizontal', 'figure'),
    [dash.dependencies.Input('Year', 'value')])
def update_sale_lease_horizontal(Year):
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

                width=750,
                height=550,
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


# @app.callback(
#    dash.dependencies.Output('sale-lease-vertical', 'figure'),
#    [dash.dependencies.Input('Year', 'value')])

def update_sale_lease_vertical(Year):
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

    # print('=-=-=-=-=-=-=-=-=-=-=-=-=-')
    # print(pv1)
    # print(pv2)
    # newdf = pd.DataFrame(pv1)

    # print(agency_list)

    trace1 = go.Bar(y=pv1[("SQM")], x=pv1.index, marker=dict(
        color=color.colliers_light_blue), width=0.2, orientation='v', name='Lease')
    trace2 = go.Bar(y=pv2[("SQM")], x=pv1.index, marker=dict(
        color=color.colliers_dark_blue), width=0.2, orientation='v', name='Sale')

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

                width=750,
                height=550,
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
                           showticklabels=True),
                barmode='stack'
            ),

    }


# print(sorted(df['Agency'].unique())

if __name__ == '__main__':
    app.run_server(debug=True)