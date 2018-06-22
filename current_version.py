import dash
import base64
import io
import urllib
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
import project_colors_and_fonts as color
import project_sql as sql
# import Passwords_and_Usernames as users
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
from itertools import chain
import project_static as static
import project_pages_layout as pages
import project_methods as my_method
import project_deals_graphics

#print(help(dt.DataTable))

''' НАЧАЛО ОСНОВНОГО БЛОКА ПРИЛОЖЕНИЯ '''

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
''' Мой файл с гитхаба на rawgit с измененной css разметкой'''
app.css.append_css({'external_url': 'https://rawgit.com/Wittgensteen/work_stuff/master/new_buttons.css'})

#py.sign_in('Wittgensteen', 'D9dEx9VG7SfqBlkoDvRl')  # вход в аккаунт на plotly Юра
py.sign_in('Barbrady', 'V11sgDqsmE4XpTsVGoFJ')  # вход в аккаунт на plotly Дима

app.layout = pages.serve_layout()  # ОСНОВНАЯ СТРАНИЦА ПРИЛОЖЕНИЯ

''' Разметка окон приложения. Функции с кодом разметки находится в файле project_pages_layout.py '''

index_page = pages.index_page()  # РАЗМЕТКА СТРАНИЦЫ 'MAIN'
page_help_layout = pages.help_page()  # РАЗМЕТКА СТРАНИЦЫ 'HELP'
page_about_layout = pages.about_page()  # РАЗМЕТКА СТРАНИЦЫ 'ABOUT PROJECT'
page_deals_layout = pages.deals_page()  # РАЗМЕТКА СТРАНИЦЫ 'БАЗА ПО СДЕЛКАМ'
page_update_database_layout = pages.update_database()  # РАЗМЕТКА СТРАНИЦЫ 'ОБНОВИТЬ БАЗУ'
page_default_graphs_and_tabs = pages.default_graphics_and_tables_page()
suspicious_deals_layout = pages.suspicious_deals_page()  # РАЗМЕТКА СТРАНИЦЫ 'БАЗА ПО СОМНИТЕЛЬНЫМ СДЕЛКАМ'

'''Функция кнопки скрытия элементов интерфейса'''


def interface_button():
    """ Эта функция введена искуственно для возможности скрыть блок кода """

    @app.callback(dash.dependencies.Output('interface-bar', 'style'),  # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks')
                   # если кнопка нажата, то скрывается элемент настройки интерфейса
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
            # ##print(n_clicks)
            style = {
                'transition': 'left 0.1s',
                '-webkit-transition': 'left 0.1s',
                'display': 'none'
            }
        return style

    @app.callback(dash.dependencies.Output('interface-arrow-left', 'style'),
                  # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks')
                   # если кнопка нажата, то элемент перемещается влево
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
                'box-shadow': '0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19)',
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

    @app.callback(dash.dependencies.Output('interface-arrow-left', 'children'),
                  # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks')
                   # если кнопка нажата, то '<<' сменяется на '>>'
                   ])
    def move_button(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            children = '<<'
        if n_clicks is not None and n_clicks % 2 != 0:
            children = '>>'
        return children

    @app.callback(dash.dependencies.Output('main-div', 'style'),  # на вход принимается событие нажатия кнопки <<
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks')
                   # если кнопка нажата, то элемент перемещается влево
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
                  [dash.dependencies.Input('interface-arrow-left', 'n_clicks')
                   # если кнопка нажата, то ширина таблицы меняется
                   ])
    def move_button(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            style = 1695
        if n_clicks is not None and n_clicks % 2 != 0:
            style = 1905
        return style


interface_button()


# БЛОК КОДА ПО ДЕФОЛТНЫМ ГРАФИКАМ

'''
Отображение tree-like блока со списком дефолтных графиков
'''


@app.callback(dash.dependencies.Output('interface-default-graphics', 'labelStyle'),
              # на вход принимается значение чеклиста 'colums'
              [dash.dependencies.Input('tree-checklist-default-graphics', 'values')   # 'tree-checklist-default-graphics'
               # если значение выбрано, то отрисовывается новый блок со списком, как в дереве
               ])
def show_default_graphics_tree(val):
    if 'Show' in val:
        children = {'display': 'block',
                    'width': '192px',
                    'margin': '0 0 0 10px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children


'''
Функция отображения дефолтных графиков по значению checklist`а
Эта функция введена искуственно для возможности скрыть блок кода
'''


def select_default_graph_from_check_graphics():
    @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-2017-RU', 'style'),
                  [dash.dependencies.Input('interface-default-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_graph_ru(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' in val:
                show_graph = {'display': 'inline-block',
                              'padding': '100px 0px 0px 50px'
                              }

            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('pie-4-text', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_text_ru(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' in val:
                show_text = {'display': 'inline-block',
                             'padding-left': '150px'
                             }

            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' not in val:
                show_text = {'display': 'none',
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_text

    @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_1q_2018_graph_ru(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' in val:
                show_graph = {'display': 'inline-block',
                              'padding': '100px 0px 0px 50px'
                              }

            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' not in val:
                show_graph = {'display': 'none'
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('pie-5-text', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_text_ru(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' in val:
                show_text = {'display': 'inline-block',
                             'padding-left': '150px'
                             }

            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' not in val:
                show_text = {'display': 'none',
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_text

    @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-five-years-RU', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_five_years_graph_ru(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' in val:
                show_graph = {'display': 'inline-block',
                              'padding': '100px 0px 0px 50px'
                              }

            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('pie-6-text', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_text_ru(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' in val:
                show_text = {'display': 'inline-block',
                             'padding-left': '90px'
                             }

            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' not in val:
                show_text = {'display': 'none',
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_text

    @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-2017-MOS', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_graph_mos(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('pie-7-text', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_text_mos(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' in val:
                show_text = {'display': 'inline-block',
                             'padding-left': '50px'
                             }

            if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' not in val:
                show_text = {'display': 'none',
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_text

    @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_1q_2018_graph_mos(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('pie-8-text', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_text_mos(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' in val:
                show_text = {'display': 'inline-block',
                             'padding-left': '50px'
                             }

            if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' not in val:
                show_text = {'display': 'none',
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_text

    @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_five_years_graph_mos(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('pie-9-text', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_llr_etr_pie_2017_text_mos(val):
        try:
            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' in val:
                show_text = {'display': 'inline-block',
                             'padding-left': '50px'
                             }

            if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' not in val:
                show_text = {'display': 'none',
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_text

    @app.callback(dash.dependencies.Output('html-tab-RU-2017-div', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_bigest_deal_table_2017(val):
        try:
            if 'biggest-deal-tab-2017' in val:
                show_tab = {'display': 'inline',
                            }

            if 'biggest-deal-tab-2017' not in val:
                show_tab = {'display': 'none',
                            }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_tab

    @app.callback(dash.dependencies.Output('html-tab-RU-1q2018-div', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_bigest_deal_table_1q2018(val):
        try:
            if 'biggest-deal-tab-1q2018' in val:
                show_tab = {'display': 'inline',
                            }

            if 'biggest-deal-tab-1q2018' not in val:
                show_tab = {'display': 'none',
                            }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_tab

    @app.callback(dash.dependencies.Output('html-tab-RU-five-years-div', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_bigest_deal_table_2013_2018(val):
        try:
            if 'biggest-deal-tab-2013-2018' in val:
                show_tab = {'display': 'inline',
                            }

            if 'biggest-deal-tab-2013-2018' not in val:
                show_tab = {'display': 'none',
                            }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_tab


select_default_graph_from_check_graphics()  # вызов функции с отображением дефолтных графиков и подписей к ним


'''Функция по отрисовке дефолтных графиков'''


def default_graphics():
    @app.callback(
        dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-2017-RU', 'figure'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ]
    )
    def update_pie_graph_4(values):

        df_plot = static.all_deals_query_df.copy()
        data = df_plot[(df_plot['Year'].isin(['2017'])) & (df_plot['Country'].isin(['RU']))]
        data_llr_only = data[(data['LLR_Only'].isin(['Yes']))]
        data_e_tr_only = data[(data['E_TR_Only'].isin(['Yes']))]
        data_llr_e_tr_only = data[(data['LLR/E_TR'].isin(['Yes']))]
        # ##print('data_llr_only_sum', data_llr_only["SQM"].sum())
        # ##print('data_e_tr_only', data_e_tr_only["SQM"].sum())
        # ##print('data_llr_e_tr_only', data_llr_e_tr_only["SQM"].sum())
        d = {'Type': ['LLR', '(E)TR', 'LLR/(E)TR'],
             'SQM': [data_llr_only["SQM"].sum(), data_e_tr_only["SQM"].sum(), data_llr_e_tr_only["SQM"].sum()]}
        df_graph = pd.DataFrame(data=d)

        width = 600
        height = 450

        pv = pd.pivot_table(
            df_graph,
            index=["Type"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)
        colors_pie = [color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_light_blue]
        pie1 = go.Pie(values=pv["SQM"],
                      labels=['LLR', '(E)TR', 'LLR/(E)TR'],
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
        return {
            'data': [pie1],
            'layout': go.Layout(
                title='2017',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

    @app.callback(
        dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU', 'figure'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_pie_graph_5(values):

        df_plot = static.all_deals_query_df.copy()
        data = df_plot[
            (df_plot['Year'].isin(['2018'])) & (df_plot['Country'].isin(['RU'])) & (df_plot['Quarter'].isin(['1']))]
        data_llr_only = data[(data['LLR_Only'].isin(['Yes']))]
        data_e_tr_only = data[(data['E_TR_Only'].isin(['Yes']))]
        data_llr_e_tr_only = data[(data['LLR/E_TR'].isin(['Yes']))]
        # ##print('data_llr_only_sum', data_llr_only["SQM"].sum())
        # ##print('data_e_tr_only', data_e_tr_only["SQM"].sum())
        # ##print('data_llr_e_tr_only', data_llr_e_tr_only["SQM"].sum())
        d = {'Type': ['LLR', '(E)TR', 'LLR/(E)TR'],
             'SQM': [data_llr_only["SQM"].sum(), data_e_tr_only["SQM"].sum(), data_llr_e_tr_only["SQM"].sum()]}
        df_graph = pd.DataFrame(data=d)

        width = 600
        height = 450

        pv = pd.pivot_table(
            df_graph,
            index=["Type"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)
        colors_pie = [color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_light_blue]
        pie1 = go.Pie(values=pv["SQM"],
                      labels=['LLR', '(E)TR', 'LLR/(E)TR'],
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
        return {
            'data': [pie1],
            'layout': go.Layout(
                title='1q 2018',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

    @app.callback(
        dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-five-years-RU', 'figure'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_pie_graph_6(values):

        df_plot = static.all_deals_query_df.copy()
        data = df_plot[(df_plot['Country'].isin(['RU']))]
        data_llr_only = data[(data['LLR_Only'].isin(['Yes'])) & (df_plot['Country'].isin(['RU']))]
        data_e_tr_only = data[(data['E_TR_Only'].isin(['Yes']))]
        data_llr_e_tr_only = data[(data['LLR/E_TR'].isin(['Yes']))]
        # ##print('data_llr_only_sum', data_llr_only["SQM"].sum())
        # ##print('data_e_tr_only', data_e_tr_only["SQM"].sum())
        # ##print('data_llr_e_tr_only', data_llr_e_tr_only["SQM"].sum())
        d = {'Type': ['LLR', '(E)TR', 'LLR/(E)TR'],
             'SQM': [data_llr_only["SQM"].sum(), data_e_tr_only["SQM"].sum(), data_llr_e_tr_only["SQM"].sum()]}
        df_graph = pd.DataFrame(data=d)

        width = 600
        height = 450

        pv = pd.pivot_table(
            df_graph,
            index=["Type"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)
        colors_pie = [color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_light_blue]
        pie1 = go.Pie(values=pv["SQM"],
                      labels=['LLR', '(E)TR', 'LLR/(E)TR'],
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
        return {
            'data': [pie1],
            'layout': go.Layout(
                title='2013-2018',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

    @app.callback(
        dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-2017-MOS', 'figure'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_pie_graph_7(values):

        df_plot = static.all_deals_query_df.copy()
        data = df_plot[(df_plot['Year'].isin(['2017'])) & (df_plot['City'].isin(['Moscow']))]
        data_llr_only = data[(data['LLR_Only'].isin(['Yes']))]
        data_e_tr_only = data[(data['E_TR_Only'].isin(['Yes']))]
        data_llr_e_tr_only = data[(data['LLR/E_TR'].isin(['Yes']))]
        # ##print('data_llr_only_sum', data_llr_only["SQM"].sum())
        # ##print('data_e_tr_only', data_e_tr_only["SQM"].sum())
        # ##print('data_llr_e_tr_only', data_llr_e_tr_only["SQM"].sum())
        d = {'Type': ['LLR', '(E)TR', 'LLR/(E)TR'],
             'SQM': [data_llr_only["SQM"].sum(), data_e_tr_only["SQM"].sum(), data_llr_e_tr_only["SQM"].sum()]}
        df_graph = pd.DataFrame(data=d)

        width = 600
        height = 450

        pv = pd.pivot_table(
            df_graph,
            index=["Type"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)
        colors_pie = [color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_light_blue]
        pie1 = go.Pie(values=pv["SQM"],
                      labels=['LLR', '(E)TR', 'LLR/(E)TR'],
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
        return {
            'data': [pie1],
            'layout': go.Layout(
                title='2017',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

    @app.callback(
        dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS', 'figure'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_pie_graph_8(values):

        df_plot = static.all_deals_query_df.copy()
        data = df_plot[
            (df_plot['Year'].isin(['2018'])) & (df_plot['City'].isin(['Moscow'])) & (df_plot['Quarter'].isin(['1']))]
        data_llr_only = data[(data['LLR_Only'].isin(['Yes']))]
        data_e_tr_only = data[(data['E_TR_Only'].isin(['Yes']))]
        data_llr_e_tr_only = data[(data['LLR/E_TR'].isin(['Yes']))]
        # ##print('data_llr_only_sum', data_llr_only["SQM"].sum())
        # ##print('data_e_tr_only', data_e_tr_only["SQM"].sum())
        # ##print('data_llr_e_tr_only', data_llr_e_tr_only["SQM"].sum())
        d = {'Type': ['LLR', '(E)TR', 'LLR/(E)TR'],
             'SQM': [data_llr_only["SQM"].sum(), data_e_tr_only["SQM"].sum(), data_llr_e_tr_only["SQM"].sum()]}
        df_graph = pd.DataFrame(data=d)

        width = 600
        height = 450

        pv = pd.pivot_table(
            df_graph,
            index=["Type"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)
        colors_pie = [color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_light_blue]
        pie1 = go.Pie(values=pv["SQM"],
                      labels=['LLR', '(E)TR', 'LLR/(E)TR'],
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
        return {
            'data': [pie1],
            'layout': go.Layout(
                title='1q 2018',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

    @app.callback(
        dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS', 'figure'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_pie_graph_9(values):

        df_plot = static.all_deals_query_df.copy()
        data = df_plot[(df_plot['City'].isin(['Moscow']))]
        data_llr_only = data[(data['LLR_Only'].isin(['Yes']))]
        data_e_tr_only = data[(data['E_TR_Only'].isin(['Yes']))]
        data_llr_e_tr_only = data[(data['LLR/E_TR'].isin(['Yes']))]
        # ##print('data_llr_only_sum', data_llr_only["SQM"].sum())
        # ##print('data_e_tr_only', data_e_tr_only["SQM"].sum())
        # ##print('data_llr_e_tr_only', data_llr_e_tr_only["SQM"].sum())
        d = {'Type': ['LLR', '(E)TR', 'LLR/(E)TR'],
             'SQM': [data_llr_only["SQM"].sum(), data_e_tr_only["SQM"].sum(), data_llr_e_tr_only["SQM"].sum()]}
        df_graph = pd.DataFrame(data=d)

        width = 600
        height = 450

        pv = pd.pivot_table(
            df_graph,
            index=["Type"],
            values=["SQM"],
            aggfunc=sum,
            fill_value=0)
        colors_pie = [color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_light_blue]
        pie1 = go.Pie(values=pv["SQM"],
                      labels=['LLR', '(E)TR', 'LLR/(E)TR'],
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
        return {
            'data': [pie1],
            'layout': go.Layout(
                title='2013-2018',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }


default_graphics()  # вызов функции с отображением базовых pie графиков


'''Функция по отрисовке дефолтных таблиц по крупнейшим этим сделкам за этот период'''


def default_tables():
    @app.callback(
        dash.dependencies.Output('biggest-deal-tab-test', 'figure'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_biggest_deals_tab(values):
        all_deals_2017 = static.all_deals_query_df[static.all_deals_query_df['Year'].isin(['2017'])]
        all_deals_2017 = all_deals_2017.sort_values('SQM', ascending=False)

        all_deals_2017_selected = all_deals_2017[['Agency', 'Property_Name', 'SQM',
                                                  'Company', 'Business_Sector', 'Type_of_Deal']].head(10)
        # ##print(all_deals_2017_selected.Property_Name.tolist())

        trace = go.Table(
            columnwidth=[80, 200, 100, 150, 200, 100],

            header=dict(values=["Agency", "Property Name", "Office area", "Company", "Business Sector", "Type of Deal"],
                        line=dict(color=color.white),
                        fill=dict(color=color.sar_color),
                        align=['left'] * 6,
                        font=dict(color='white', size=12), ),

            cells=dict(values=[all_deals_2017_selected.Agency.tolist(),
                               all_deals_2017_selected.Property_Name.tolist(),
                               all_deals_2017_selected.SQM,
                               all_deals_2017_selected.Company,
                               all_deals_2017_selected.Business_Sector,
                               all_deals_2017_selected.Type_of_Deal

                               ],
                       line=dict(color=color.white),
                       fill=dict(color='#EDFAFF'),
                       align=['left'] * 6))

        layout = dict(width=830, height=330)
        data = [trace]
        fig = dict(data=data, layout=layout)
        return fig

    @app.callback(
        dash.dependencies.Output('html-tab-RU-2017', 'children'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_html_tab(values):
        all_deals_2017 = static.all_deals_query_df[static.all_deals_query_df['Year'].isin(['2017'])]
        all_deals_2017 = all_deals_2017.sort_values('SQM', ascending=False)
        all_deals_2017['SQM'] = all_deals_2017['SQM'].round()
        all_deals_2017_selected = all_deals_2017[['Agency', 'Property_Name', 'SQM',
                                                  'Company', 'Business_Sector', 'Type_of_Deal']].head(10)
        return my_method.generate_table_top_deals(all_deals_2017_selected)

    @app.callback(
        dash.dependencies.Output('html-tab-RU-1q2018', 'children'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_html_tab(values):
        all_deals_2018 = static.all_deals_query_df[
            static.all_deals_query_df['Year'].isin(['2018']) & static.all_deals_query_df['Quarter'].isin(['1'])]
        all_deals_2018 = all_deals_2018.sort_values('SQM', ascending=False)
        all_deals_2018['SQM'] = all_deals_2018['SQM'].round()
        all_deals_2018_selected = all_deals_2018[['Agency', 'Property_Name', 'SQM',
                                                  'Company', 'Business_Sector', 'Type_of_Deal']].head(10)
        return my_method.generate_table_top_deals(all_deals_2018_selected)

    @app.callback(
        dash.dependencies.Output('html-tab-RU-five-years', 'children'),
        [dash.dependencies.Input('interface-default-graphics', 'values')
         ])
    def update_html_tab(values):
        all_deals_2018 = static.all_deals_query_df
        all_deals_2018 = all_deals_2018.sort_values('SQM', ascending=False)
        all_deals_2018['SQM'] = all_deals_2018['SQM'].round()
        all_deals_2018_selected = all_deals_2018[['Agency', 'Property_Name', 'SQM',
                                                  'Company', 'Business_Sector', 'Type_of_Deal']].head(10)
        return my_method.generate_table_top_deals(all_deals_2018_selected)


default_tables()  # вызов функции с отображением базовых таблиц

''' Начало блока по отрисовке статических изображений. Код закомментирован до обсуждения  '''


# БЛОК КОДА ПО СТРАНИЦЕ СО СДЕЛКАМИ И ГРАФИКАМ К НИМ

'''
Отображение tree-like блока со списком
На вход принимается значение чеклиста 'select columns'
Если значение выбрано, то отрисовывается новый блок со списком, как в дереве
'''


@app.callback(dash.dependencies.Output('interface-columns', 'labelStyle'),
              # на вход принимается значение чеклиста 'colums'
              [dash.dependencies.Input('tree-checklist-columns', 'values')
               # если значение выбрано, то отрисовывается новый блок со списком, как в дереве
               ])
def show_tree_columns(val):
    if 'Show' in val:
        children = {'display': 'block',
                    'width': '192px',
                    'margin': '0 0 0 10px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children


'''
Функция отображение выпадающих списков по значению checklist`а
Эта функция введена искуственно для возможности скрыть блок кода
'''


def select_drop_from_check_columns():
    @app.callback(dash.dependencies.Output('Include_in_Market_Share_Div', 'style'),
                  # проверка checklist со значениями выбранных столбов в таблице
                  [dash.dependencies.Input('interface-columns', 'values')
                   # при выборе столбца добавляется выпадающий список
                   ])
    def update_drop_include(val):
        try:
            if 'Include_in_Market_Share' in val:
                style_include = {'display': 'inline-block',
                                 'width': '150px',
                                 }

            if 'Include_in_Market_Share' not in val:
                style_include = {'display': 'none',
                                 'width': '80px',
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_include

    @app.callback(dash.dependencies.Output('Agency_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_agency(val):
        try:
            if 'Agency' in val:
                style_agency = {'display': 'inline-block',
                                'width': '110px',
                                }

            if 'Agency' not in val:
                style_agency = {'display': 'none',
                                'width': '80px',
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_agency

    @app.callback(dash.dependencies.Output('Country_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_country(val):
        try:
            if 'Country' in val:
                style_country = {'display': 'inline-block',
                                 'width': '86px',
                                 }

            if 'Country' not in val:
                style_country = {'display': 'none',
                                 'width': '80px',
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_country

    @app.callback(dash.dependencies.Output('City_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_city(val):
        try:
            if 'City' in val:
                style_city = {'display': 'inline-block',
                              'width': '110px',
                              }

            if 'City' not in val:
                style_city = {'display': 'none',
                              'width': '80px',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_city

    @app.callback(dash.dependencies.Output('Property_name_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_property_name(val):
        try:
            if 'Property_Name' in val:
                style_property_name = {'display': 'inline-block',
                                       'width': '230px',
                                       }

            if 'Property_Name' not in val:
                style_property_name = {'display': 'none',
                                       'width': '80px',
                                       }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_property_name

    @app.callback(dash.dependencies.Output('Class_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_class(val):
        try:
            if 'Class' in val:
                style_class = {'display': 'inline-block',
                               'width': '76px',
                               }

            if 'Class' not in val:
                style_class = {'display': 'none',
                               'width': '80px',
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_class

    @app.callback(dash.dependencies.Output('SQM_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_SQM(val):
        try:
            if 'SQM' in val:
                style_SQM = {'display': 'inline-block',
                             'width': '80px',
                             }

            if 'SQM' not in val:
                style_SQM = {'display': 'none',
                             'width': '80px',
                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_SQM

    @app.callback(dash.dependencies.Output('Company_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Company(val):
        try:
            if 'SQM' in val:
                style_Company = {'display': 'inline-block',
                                 'width': '184px',
                                 }

            if 'SQM' not in val:
                style_Company = {'display': 'none',
                                 'width': '80px',
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Company

    @app.callback(dash.dependencies.Output('Business_Sector_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Business_Sector(val):
        try:
            if 'Business_Sector' in val:
                style_Business_Sector = {'display': 'inline-block',
                                         'width': '250px',
                                         }

            if 'Business_Sector' not in val:
                style_Business_Sector = {'display': 'none',
                                         'width': '80px',
                                         }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Business_Sector

    @app.callback(dash.dependencies.Output('Type_of_Deal_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Type_of_Deal(val):
        try:
            if 'Type_of_Deal' in val:
                style_Type_of_Deal = {'display': 'inline-block',
                                      'width': '130px',
                                      }

            if 'Type_of_Deal' not in val:
                style_Type_of_Deal = {'display': 'none',
                                      'width': '80px',
                                      }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Type_of_Deal

    @app.callback(dash.dependencies.Output('Type_of_Consultancy_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Type_of_Consultancy(val):
        try:
            if 'Type_of_Consultancy' in val:
                style_Type_of_Consultancy = {'display': 'inline-block',
                                             'width': '170px',
                                             }

            if 'Type_of_Consultancy' not in val:
                style_Type_of_Consultancy = {'display': 'none',
                                             'width': '80px',
                                             }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Type_of_Consultancy

    # @app.callback(dash.dependencies.Output('LLR/TR_Div', 'style'),
    #               [dash.dependencies.Input('interface-columns', 'values')
    #                ])
    # def update_drop_Type_of_Consultancy(val):
    #     try:
    #         if 'LLR_TR' in val:
    #             style_LLR_TR = {'display': 'inline-block',
    #                             'width': '80px',
    #                             }
    #
    #         if 'LLR_TR' not in val:
    #             style_LLR_TR = {'display': 'none',
    #                             'width': '80px',
    #                             }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return style_LLR_TR

    @app.callback(dash.dependencies.Output('Year_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Year(val):
        try:
            if 'Year' in val:
                style_Year = {'display': 'inline-block',
                              'width': '90px',
                              }

            if 'Year' not in val:
                style_Year = {'display': 'none',
                              'width': '80px',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Year

    @app.callback(dash.dependencies.Output('Quarter_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Quarter(val):
        try:
            if 'Quarter' in val:
                style_Quarter = {'display': 'inline-block',
                                 'width': '90px',
                                 }
            if 'Quarter' not in val:
                style_Quarter = {'display': 'none',
                                 'width': '80px',
                                 }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Quarter

    @app.callback(dash.dependencies.Output('Address_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Address(val):
        try:
            if 'Address' in val:
                style_Addres = {'display': 'inline-block',
                                'width': '250px',
                                }

            if 'Address' not in val:
                style_Addres = {'display': 'none',
                                'width': '80px',
                                }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Addres

    @app.callback(dash.dependencies.Output('Submarket_Large_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Submarket_large(val):
        try:
            if 'Submarket_Large' in val:
                style_Submarket_Large = {'display': 'inline-block',
                                         'width': '150px',
                                         }

            if 'Submarket_Large' not in val:
                style_Submarket_Large = {'display': 'none',
                                         'width': '80px',
                                         }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Submarket_Large

    @app.callback(dash.dependencies.Output('Owner_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Owner(val):
        try:
            if 'Owner' in val:
                style_Owner = {'display': 'inline-block',
                               'width': '150px',
                               }

            if 'Owner' not in val:
                style_Owner = {'display': 'none',
                               'width': '80px',
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Owner

    @app.callback(dash.dependencies.Output('Date_of_acquiring_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Date_of_acquiring(val):
        try:
            if 'Date_of_acquiring' in val:
                style_Date_of_acquiring = {'display': 'inline-block',
                                           'width': '150px',
                                           }

            if 'Date_of_acquiring' not in val:
                style_Date_of_acquiring = {'display': 'none',
                                           'width': '80px',
                                           }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Date_of_acquiring

    @app.callback(dash.dependencies.Output('Class_Colliers_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Class_Colliers(val):
        try:
            if 'Class_Colliers' in val:
                style_Class_Colliers = {'display': 'inline-block',
                                        'width': '150px',
                                        }

            if 'Class_Colliers' not in val:
                style_Class_Colliers = {'display': 'none',
                                        'width': '80px',
                                        }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Class_Colliers

    @app.callback(dash.dependencies.Output('Floor_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Floor(val):
        try:
            if 'Floor' in val:
                style_Floor = {'display': 'inline-block',
                               'width': '150px',
                               }

            if 'Floor' not in val:
                style_Floor = {'display': 'none',
                               'width': '80px',
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Floor

    @app.callback(dash.dependencies.Output('Deal_Size_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Deal_Size(val):
        try:
            if 'Deal_Size' in val:
                style_Deal_Size = {'display': 'inline-block',
                                   'width': '150px',
                                   }

            if 'Deal_Size' not in val:
                style_Deal_Size = {'display': 'none',
                                   'width': '80px',
                                   }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Deal_Size

    @app.callback(dash.dependencies.Output('Sublease_Agent_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Sublease_Agent(val):
        try:
            if 'Sublease_Agent' in val:
                style_Sublease_Agent = {'display': 'inline-block',
                                        'width': '150px',
                                        }

            if 'Sublease_Agent' not in val:
                style_Sublease_Agent = {'display': 'none',
                                        'width': '80px',
                                        }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Sublease_Agent

    # @app.callback(dash.dependencies.Output('LLR_Only_Div', 'style'),
    #               [dash.dependencies.Input('interface-columns', 'values')
    #                ])
    # def update_drop_LLR_Only(val):
    #     try:
    #         if 'LLR_Only' in val:
    #             style_LLR_Only = {'display': 'inline-block',
    #                               'width': '80px',
    #                               }
    #
    #         if 'LLR_Only' not in val:
    #             style_LLR_Only = {'display': 'none',
    #                               'width': '80px',
    #                               }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return style_LLR_Only
    #
    # @app.callback(dash.dependencies.Output('E_TR_Only_Div', 'style'),
    #               [dash.dependencies.Input('interface-columns', 'values')
    #                ])
    # def update_drop_E_TR_Only(val):
    #     try:
    #         if 'E_TR_Only' in val:
    #             style_E_TR_Only = {'display': 'inline-block',
    #                                'width': '80px',
    #                                }
    #
    #         if 'E_TR_Only' not in val:
    #             style_E_TR_Only = {'display': 'none',
    #                                'width': '80px',
    #                                }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return style_E_TR_Only
    #
    # @app.callback(dash.dependencies.Output('LLR/E_TR_Div', 'style'),
    #               [dash.dependencies.Input('interface-columns', 'values')
    #                ])
    # def update_drop_LLR_E_TR(val):
    #     try:
    #         if 'LLR/E_TR' in val:
    #             style_LLR_E_TR = {'display': 'inline-block',
    #                               'width': '80px',
    #                               }
    #
    #         if 'LLR/E_TR' not in val:
    #             style_LLR_E_TR = {'display': 'none',
    #                               'width': '80px',
    #                               }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return style_LLR_E_TR

    @app.callback(dash.dependencies.Output('Month_Div', 'style'),
                  [dash.dependencies.Input('interface-columns', 'values')
                   ])
    def update_drop_Month(val):
        try:
            if 'Month' in val:
                style_Month = {'display': 'inline-block',
                               'width': '146px',
                               }

            if 'Month' not in val:
                style_Month = {'display': 'none',
                               'width': '80px',
                               }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return style_Month


select_drop_from_check_columns()  # вызов функции с отображением выпадающих списков

'''
Отображение tree-like блока со списком графиков
На вход принимается значение чеклиста 'select graphics'
'''


@app.callback(dash.dependencies.Output('interface-graphics', 'labelStyle'),
              # на вход принимается значение чеклиста 'colums'
              [dash.dependencies.Input('tree-checklist-graphics', 'values')
               # если значение выбрано, то отрисовывается новый блок со списком, как в дереве
               ])
def show_graphics_tree(val):
    if 'Show' in val:
        children = {'display': 'block',
                    'width': '192px',
                    'margin': '0 0 0 10px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children


'''
Отображение tree-like блока со списком типов сделок
На вход принимается значение чеклиста 'select data'
'''


@app.callback(dash.dependencies.Output('interface-data', 'labelStyle'),
              # на вход принимается значение чеклиста 'colums'
              [dash.dependencies.Input('tree-checklist-data', 'values')
               # если значение выбрано, то отрисовывается новый блок со списком, как в дереве
               ])
def show_data_tree(val):
    if 'Show' in val:
        children = {'display': 'block',
                    'width': '192px',
                    'margin': '0 0 0 10px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children

'''
Отображение tree-like блока со списком статических картинок графиков
На вход принимается значение чеклиста 'select data'
'''


@app.callback(dash.dependencies.Output('interface-graphics-image', 'labelStyle'),
              # на вход принимается значение чеклиста 'colums'
              [dash.dependencies.Input('tree-checklist-graphics-image', 'values')
               # если значение выбрано, то отрисовывается новый блок со списком, как в дереве
               ])
def show_image_tree(val):
    if 'Show' in val:
        children = {'display': 'block',
                    'width': '192px',
                    'margin': '0 0 0 10px',
                    }
    else:
        children = {'display': 'none'
                    }
    return children



'''
Функция отображения графиков по значению checklist`а
Эта функция введена искуственно для возможности скрыть блок кода
'''


def select_graph_from_check_graphics():
    @app.callback(dash.dependencies.Output('market-graph-tab', 'style'),
                  # проверка checklist со значениями выбранных столбов в таблице
                  [dash.dependencies.Input('interface-graphics', 'values')
                   # при выборе столбца добавляется выпадающий список
                   ])
    def update_bar_stacked_graph(val):
        try:
            if 'Bar-stacked' in val:
                show_graph = {'display': 'inline-block'
                              }

            if 'Bar-stacked' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('market-graph-non-stack-tab', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_bar_unstacked_graph(val):
        try:
            if 'Bar-unstacked' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'Bar-unstacked' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('market-graph-horizontal-tab', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_bar_stacked_horizontal_graph(val):
        try:
            if 'Bar-stacked-horizontal' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'Bar-stacked-horizontal' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('market-pie-graph-tab', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_pie_graph(val):
        try:
            if 'Pie-chart' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'Pie-chart' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('market-graph-percent-tab', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_bar_stacked_percent_graph(val):
        try:
            if 'Bar-stacked-percent' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'Bar-stacked-percent' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    @app.callback(dash.dependencies.Output('market-graph-horizontal-total-tab', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_bar_horizontal_graph(val):
        try:
            if 'Bar-horizontal' in val:
                show_graph = {'display': 'inline-block',
                              }

            if 'Bar-horizontal' not in val:
                show_graph = {'display': 'none',
                              }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_graph

    # @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-2017-RU', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_graph_ru(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' in val:
    #             show_graph = {'display': 'inline-block',
    #                           'padding': '100px 0px 0px 50px'
    #                           }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' not in val:
    #             show_graph = {'display': 'none',
    #                           }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_graph
    #
    # @app.callback(dash.dependencies.Output('pie-4-text', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_text_ru(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' in val:
    #             show_text = {'display': 'inline-block',
    #                          'padding-left': '150px'
    #                          }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-RU' not in val:
    #             show_text = {'display': 'none',
    #                          }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_text
    #
    # @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_1q_2018_graph_ru(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' in val:
    #             show_graph = {'display': 'inline-block',
    #                           'padding': '100px 0px 0px 50px'
    #                           }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' not in val:
    #             show_graph = {'display': 'none'
    #                           }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_graph
    #
    # @app.callback(dash.dependencies.Output('pie-5-text', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_text_ru(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' in val:
    #             show_text = {'display': 'inline-block',
    #                          'padding-left': '150px'
    #                          }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU' not in val:
    #             show_text = {'display': 'none',
    #                          }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_text
    #
    # @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-five-years-RU', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_five_years_graph_ru(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' in val:
    #             show_graph = {'display': 'inline-block',
    #                           'padding': '100px 0px 0px 50px'
    #                           }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' not in val:
    #             show_graph = {'display': 'none',
    #                           }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_graph
    #
    # @app.callback(dash.dependencies.Output('pie-6-text', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_text_ru(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' in val:
    #             show_text = {'display': 'inline-block',
    #                          'padding-left': '90px'
    #                          }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-RU' not in val:
    #             show_text = {'display': 'none',
    #                          }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_text
    #
    # @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-2017-MOS', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_graph_mos(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' in val:
    #             show_graph = {'display': 'inline-block',
    #                           }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' not in val:
    #             show_graph = {'display': 'none',
    #                           }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_graph
    #
    # @app.callback(dash.dependencies.Output('pie-7-text', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_text_mos(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' in val:
    #             show_text = {'display': 'inline-block',
    #                          'padding-left': '50px'
    #                          }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-2017-MOS' not in val:
    #             show_text = {'display': 'none',
    #                          }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_text
    #
    # @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_1q_2018_graph_mos(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' in val:
    #             show_graph = {'display': 'inline-block',
    #                           }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' not in val:
    #             show_graph = {'display': 'none',
    #                           }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_graph
    #
    # @app.callback(dash.dependencies.Output('pie-8-text', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_text_mos(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' in val:
    #             show_text = {'display': 'inline-block',
    #                          'padding-left': '50px'
    #                          }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS' not in val:
    #             show_text = {'display': 'none',
    #                          }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_text
    #
    # @app.callback(dash.dependencies.Output('LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_five_years_graph_mos(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' in val:
    #             show_graph = {'display': 'inline-block',
    #                           }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' not in val:
    #             show_graph = {'display': 'none',
    #                           }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_graph
    #
    # @app.callback(dash.dependencies.Output('pie-9-text', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_llr_etr_pie_2017_text_mos(val):
    #     try:
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' in val:
    #             show_text = {'display': 'inline-block',
    #                          'padding-left': '50px'
    #                          }
    #
    #         if 'LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS' not in val:
    #             show_text = {'display': 'none',
    #                          }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_text

    @app.callback(dash.dependencies.Output('biggest-deal-tab-test', 'style'),
                  [dash.dependencies.Input('interface-graphics', 'values')
                   ])
    def update_biigest_deal_table_test(val):
        try:
            if 'biggest-deal-tab-test' in val:
                show_tab = {'display': 'inline-block',
                            }

            if 'biggest-deal-tab-test' not in val:
                show_tab = {'display': 'none',
                            }
        except Exception as e:
            return html.Div([
                'There was an error'
            ])
        return show_tab

    # @app.callback(dash.dependencies.Output('html-tab-RU-2017-div', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_bigest_deal_table_2017(val):
    #     try:
    #         if 'biggest-deal-tab-2017' in val:
    #             show_tab = {'display': 'inline',
    #                         }
    #
    #         if 'biggest-deal-tab-2017' not in val:
    #             show_tab = {'display': 'none',
    #                         }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_tab
    #
    # @app.callback(dash.dependencies.Output('html-tab-RU-1q2018-div', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_bigest_deal_table_1q2018(val):
    #     try:
    #         if 'biggest-deal-tab-1q2018' in val:
    #             show_tab = {'display': 'inline',
    #                         }
    #
    #         if 'biggest-deal-tab-1q2018' not in val:
    #             show_tab = {'display': 'none',
    #                         }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_tab
    #
    # @app.callback(dash.dependencies.Output('html-tab-RU-five-years-div', 'style'),
    #               [dash.dependencies.Input('interface-graphics', 'values')
    #                ])
    # def update_bigest_deal_table_2013_2018(val):
    #     try:
    #         if 'biggest-deal-tab-2013-2018' in val:
    #             show_tab = {'display': 'inline',
    #                         }
    #
    #         if 'biggest-deal-tab-2013-2018' not in val:
    #             show_tab = {'display': 'none',
    #                         }
    #     except Exception as e:
    #         return html.Div([
    #             'There was an error'
    #         ])
    #     return show_tab


select_graph_from_check_graphics()  # вызов функции с отображением графиков и подписей к ним


'''
Вывод строк таблицы
На вход принимается значение выпадающих списков и выбранных элементов в списке слева
На основе этих значение формируется dataframe, поещаемый в таблицу
'''


@app.callback(dash.dependencies.Output('datatable', 'rows'),
              # здесь на вход принимается значение значение выпадающих списков и на основе этих значение формируется dataframe, поещаемый в таблицу
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
               # dash.dependencies.Input('LLR/TR', 'value'),
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
               # dash.dependencies.Input('LLR_Only', 'value'),
               # dash.dependencies.Input('E_TR_Only', 'value'),
               # dash.dependencies.Input('LLR/E_TR', 'value'),
               dash.dependencies.Input('Month', 'value'),
               dash.dependencies.Input('interface-columns', 'values'),
               dash.dependencies.Input('interface-data', 'value')
               # значение чеклиста из дерева с выбором столбцов interface-data
               ])
def update_datatable(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large, Owner,
                     Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month, col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                      Month)
    cond_1 = cond.copy()  # копия словаря
    list_of_values_copy = list(filter(None,
                                      list_of_values))  # очистка кортежа от пустых элементов (при не выбранном значении value, значение по умолчанию = None
    data_to_table = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    data_to_table = data_to_table.sort_values('Year', ascending=False)  # отсортировнный по годам датафрейм

    return data_to_table[col].to_dict('records')



'''  Подсчёт суммы по отфильтрованным данным  '''


@app.callback(dash.dependencies.Output('sum-string', 'children'),
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
               # dash.dependencies.Input('LLR/TR', 'value'),
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
               # dash.dependencies.Input('LLR_Only', 'value'),
               # dash.dependencies.Input('E_TR_Only', 'value'),
               # dash.dependencies.Input('LLR/E_TR', 'value'),
               dash.dependencies.Input('Month', 'value'),
               dash.dependencies.Input('interface-columns', 'values'),
               dash.dependencies.Input('interface-data', 'value')  # значение чеклиста из дерева с выбором столбцов
               ])
def update_sum(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
               Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large, Owner,
               Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
               Month, col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency], City=[City],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                Property_Name=[Property_Name], Class=[Class], SQM=[SQM], Company=[Company],
                Business_Sector=[Business_Sector], Type_of_Deal=[Type_of_Deal],
                Type_of_Consultancy=[Type_of_Consultancy], Quarter=[Quarter],
                Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large], Owner=[Owner], Date_of_acquiring=[Date_of_acquiring],
                Class_Colliers=[Class_Colliers], Floor=[Floor], Deal_Size=[Deal_Size],
                Sublease_Agent=[Sublease_Agent], Month=[Month])
    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month)
    cond_1 = cond.copy()

    list_of_values_copy = list(filter(None, list_of_values))

    data_to_table = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)

    data_sum = int(round(data_to_table["SQM"].sum()))
    sqm_sum = '{0:,}'.format(data_sum).replace(',', ' ')

    sum_parameters = 'Type of deal = {0}, sorting options = '.format(str(data_in).strip("[]'"))
    if list_of_values_copy != []:
        params = str(list_of_values_copy).split()
        for i in range(len(params)):
            if i == 0:
                sum_parameters += '{0}'.format(params[i].strip("[],'"))
            else:
                sum_parameters += ', {0}'.format(params[i].strip("[],'"))
    else:
        sum_parameters += 'default'
    return 'Суммарная площадь по сделкам составляет ', sqm_sum, ' кв.м ( ', sum_parameters, ' )'


'''  Скачивание csv файла с дампом всей базы данных по сделкам  '''


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
    csv_string = static.all_deals_query_df.to_csv(index=False, encoding='utf-8', sep=';')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string


'''  Скачивание csv файла с выбранными данными  '''


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
     # dash.dependencies.Input('LLR/TR', 'value'),
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
     # dash.dependencies.Input('LLR_Only', 'value'),
     # dash.dependencies.Input('E_TR_Only', 'value'),
     # dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),
     dash.dependencies.Input('interface-data', 'value')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_download_link(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                         Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                         Owner,
                         Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                         Month, col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                      Month)
    cond_1 = cond.copy()

    list_of_values_copy = list(filter(None, list_of_values))

    data_to_table = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)

    csv_string = data_to_table.to_csv(index=False, encoding='utf-8', sep=';')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string


'''
Начало блока по отрисовке графиков
Callback`и, отрисовывающие графики, принимают на вход данные выпающих списков.
График принимает те же переменные, как и таблица, сначала фильтруется датафрейм по выбранным данным,
после этот датафрейм переводится в сводную таблицу в pandas и по значениям сводной таблицы строится график.
'''


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
     # dash.dependencies.Input('LLR/TR', 'value'),
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
     # dash.dependencies.Input('LLR_Only', 'value'),
     # dash.dependencies.Input('E_TR_Only', 'value'),
     # dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),
     dash.dependencies.Input('interface-data', 'value'),
     # значение чеклиста из дерева с выбором столбцов market-graph-tab-slider-width
     # dash.dependencies.Input('market-graph-tab-slider-width', 'value'),
     # dash.dependencies.Input('market-graph-tab-slider-height', 'value')
     ])
def update_graph_tab(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                     Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month, col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class], SQM=[SQM], Company=[Company],
                Business_Sector=[Business_Sector], Type_of_Deal=[Type_of_Deal],
                Type_of_Consultancy=[Type_of_Consultancy], Quarter=[Quarter],
                Include_in_Market_Share=[Include_in_Market_Share], Address=[Address], Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    width = 700
    height = 500

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    df_plot = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    df_plot = df_plot.sort_values('Year', ascending=False)  # отсортировнный по годам датафрейм

    pv = pd.pivot_table(  # создание сводной таблицы из текущего датафрейма
        df_plot,  # выбор текущего датафрейма
        index=['Year'],  # выбор индекса ("строки" в Excel Pivot Tables)
        columns=['Agency'],  # выбор столбцов ("столбцы" в Excel Pivot Tables)
        values=["SQM"],  # выбор подсчитываемого значения ("значения" в Excel Pivot Tables)
        aggfunc=sum,  # параметр поля значения (сумма, кол-во, среднее итд)
        fill_value=0)  # заполнение пустых ячеек

    if len(df_plot['Agency'].unique()) == 6:
        colliers_sum = (((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64))
        cw_sum = (((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64))
        cbre_sum = (((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64))
        jll_sum = (((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64))
        kf_sum = (((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64))
        sar_sum = (((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64))
        data = []
        annotations = []
        trace1 = go.Bar(x=pv.index, y=pv[("SQM", 'Colliers')],
                        name='Colliers',
                        marker=dict(
                            color=color.colliers_dark_blue),
                        width=0.4,
                        text=list(colliers_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                        name='CW',
                        marker=dict(
                            color=color.colliers_extra_light_blue),
                        width=0.4,
                        text=list(cw_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace3 = go.Bar(x=pv.index, y=pv[("SQM", 'CBRE')],
                        name='CBRE',
                        marker=dict(
                            color=color.colliers_grey_40),
                        width=0.4,
                        text=list(cbre_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))
        trace4 = go.Bar(x=pv.index, y=pv[("SQM", 'JLL')],
                        name='JLL',
                        marker=dict(
                            color=color.colliers_yellow),
                        width=0.4,
                        text=list(jll_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12))

        trace5 = go.Bar(x=pv.index, y=pv[("SQM", 'KF')],
                        name='KF',
                        marker=dict(
                            color=color.colliers_red),
                        width=0.4,
                        text=list(kf_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))

        trace6 = go.Bar(x=pv.index, y=pv[("SQM", 'SAR')],
                        name='SAR',
                        marker=dict(
                            color=color.colliers_light_blue),
                        width=0.4,
                        text=list(sar_sum),
                        textposition='none',
                        textfont=dict(
                            color=color.white,
                            size=12))

        # добавление подписи на графике по центру трейса
        for year, value in zip(pv.index, colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex in zip(pv.index, cw_sum, colliers_sum):
            annotations.append(dict(
                x=year,
                y=value_ex * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex, value_ex_ex in zip(pv.index, cbre_sum, cw_sum, colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex) * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex, value_ex_ex, value_ex_ex_ex in zip(pv.index, jll_sum, cbre_sum, cw_sum,
                                                                      colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex + value_ex_ex_ex) * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.colliers_grey_80),
            )
            )

        for year, value, value_ex, value_ex_ex, value_ex_ex_ex, value_ex_ex_ex_ex in zip(pv.index, kf_sum, jll_sum,
                                                                                         cbre_sum, cw_sum,
                                                                                         colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex + value_ex_ex_ex + value_ex_ex_ex_ex) * 1000 + (value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        for year, value, value_ex, value_ex_ex, value_ex_ex_ex, value_ex_ex_ex_ex, value_ex_ex_ex_ex_ex in zip(pv.index,
                                                                                                               sar_sum,
                                                                                                               kf_sum,
                                                                                                               jll_sum,
                                                                                                               cbre_sum,
                                                                                                               cw_sum,
                                                                                                               colliers_sum):
            annotations.append(dict(
                x=year,
                y=(value_ex + value_ex_ex + value_ex_ex_ex + value_ex_ex_ex_ex + value_ex_ex_ex_ex_ex) * 1000 + (
                        value * 1000) / 2,
                xref='x',
                yref='y',
                text=value,
                showarrow=False,
                font=dict(family='Arial',
                          size=12,
                          color=color.white),
            )
            )

        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])

    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        annotations = []
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
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = '2013-2018'

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
                    # title='Years'
                ),
                yaxis={'title': 'Area in sq.m'},
                legend=dict(orientation="h",
                            traceorder="normal"),
                barmode='stack',
                annotations=annotations
            )
    }


@app.callback(
    dash.dependencies.Output('market-graph-tab-string', 'children'),
    # подпись под графиком (возможно стоит перенесть в Div на странице)
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
     #dash.dependencies.Input('LLR/TR', 'value'),
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
     #dash.dependencies.Input('LLR_Only', 'value'),
     #dash.dependencies.Input('E_TR_Only', 'value'),
     #dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),
     # значение чеклиста из дерева с выбором столбцов market-graph-tab-slider-width
     # dash.dependencies.Input('market-graph-tab-slider-width', 'value'),
     # dash.dependencies.Input('market-graph-tab-slider-height', 'value')
     ])
def update_graph_tab_string(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                            Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address,
                            Submarket_Large, Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                            Month, col):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))
    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    my_method.replace_index(list_of_ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_index = ', '.join(str(e) for e in list_of_ind)

        format_year = 'All years'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        # ##print('list_of_ind BEFORE', list_of_ind)
        # ##print('list_of_ind AFTER', list_of_ind)
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_index = ', '.join(str(e) for e in list_of_ind)
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = 'all years'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        my_method.replace_index(list_of_ind)
        # ##print('list_of_ind', list_of_ind)
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_index = ', '.join(str(e) for e in list_of_ind)

        format_year = ', '.join(Year)

    return format_index + format_data



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
#      dash.dependencies.Input('interface-columns', 'values'),  # значение чеклиста из дерева с выбором столбцов
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
#             df_plot = static.all_deals_query_df.copy()
#     except TypeError:
#         df_plot = static.all_deals_query_df.copy()
#     except IndexError:
#         df_plot = static.all_deals_query_df.copy()
#     # __________________________________________________________________________________________________ #
#
#     if len(list_of_values_copy) != 0:
#         for i in range(len(list_of_values_copy)):
#             ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
#             if i == 0:
#                 data = static.all_deals_query_df[(static.all_deals_query_df[ind].isin(list_of_values_copy[i]))]
#             else:
#                 data = data[(static.all_deals_query_df[ind].isin(list_of_values_copy[i]))]
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
#         ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
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
#     ###print('Data loaded from Plotly')
#     #plot_url = py.plot(image_data, filename='my plot', auto_open=False)
#     ###print(plot_url)
#     #plot_url_png = plot_url + '.png'
#     ###print(plot_url_png)
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
     # dash.dependencies.Input('LLR/TR', 'value'),
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
     # dash.dependencies.Input('LLR_Only', 'value'),
     # dash.dependencies.Input('E_TR_Only', 'value'),
     # dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),
     dash.dependencies.Input('interface-data', 'value')  # значение чеклиста из дерева с выбором столбцов
     ])
def update_graph_tab_none_stack(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                                Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address,
                                Submarket_Large,
                                Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month,
                                col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    df_plot = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    df_plot = df_plot.sort_values('Year', ascending=False)  # отсортировнный по годам датафрейм

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
                        # text=list(((pv[("SQM", 'Colliers')] / 1000).round()).apply(np.int64)),
                        textposition='outside',
                        textfont=dict(
                            color=color.colliers_grey_80,
                            size=12))

        trace2 = go.Bar(x=pv.index, y=pv[("SQM", 'CW')],
                        name='CW',
                        marker=dict(
                            color=color.colliers_extra_light_blue),
                        width=0.4,
                        # text=list(((pv[("SQM", 'CW')] / 1000).round()).apply(np.int64)),
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
                        # text=list(((pv[("SQM", 'CBRE')] / 1000).round()).apply(np.int64)),
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
                        # text=list(((pv[("SQM", 'JLL')] / 1000).round()).apply(np.int64)),
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
                        # text=list(((pv[("SQM", 'KF')] / 1000).round()).apply(np.int64)),
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
                        # text=list(((pv[("SQM", 'SAR')] / 1000).round()).apply(np.int64)),
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
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = '2013-2018'

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
                    # title='Years'
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
     # dash.dependencies.Input('LLR/TR', 'value'),
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
     # dash.dependencies.Input('LLR_Only', 'value'),
     # dash.dependencies.Input('E_TR_Only', 'value'),
     # dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),  # значение чеклиста из дерева с выбором столбцов
     dash.dependencies.Input('interface-data', 'value')
     ])
def update_graph_horizontal(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                            Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                            Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month, col,
                            data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    df_plot = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    df_plot = df_plot.sort_values('Year', ascending=False)  # отсортированный по годам датафрейм

    width = 700
    height = 500

    pv = pd.pivot_table(
        df_plot,
        index=["Year"],
        columns=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    data = []
    list_of_unique = df_plot['Agency'].unique()
    list_of_unique = list_of_unique.tolist()
    list_of_unique = sorted(list_of_unique)

    if 'Colliers' in list_of_unique:
        list_of_unique.remove('Colliers')
        list_of_unique.insert(0, 'Colliers')

    for i in range(len(list_of_unique)):
        trace = go.Bar(y=pv.index,
                       x=pv[("SQM", list_of_unique[i])],
                       name=list_of_unique[i],
                       marker=dict(color=color.dict_colors_of_companies[list_of_unique[i]]),
                       width=0.45,
                       orientation='h',
                       text=list(((pv[("SQM", list_of_unique[i])] / 1000).round()).apply(np.int64)),
                       textposition='auto',
                       textfont=dict(color=color.white, size=14)
                       )
        data.append(trace)

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    return {
        'data': data,
        'layout': go.Layout(
            annotations=[dict(
                x=pv["SQM"].sum(),
                y=pv.index,
                showarrow=False,
                text=' ',
                xref="x",
                yref="y"
            )
            ],
            title='{}<br>'
                  'in {}'.format(format_data, format_year),
            autosize=False,
            bargap=0.3,
            bargroupgap=0,
            font=dict(
                color=color.colliers_grey_80,
                family='Arial',
                size=12
            ),
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
                # title='Area in sq.m'
            ),
            yaxis=dict(autorange=True,
                       showgrid=True,
                       zeroline=True,
                       showline=True,
                       autotick=False,
                       ticks='',
                       showticklabels=True,
                       # title='Year'
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
     # dash.dependencies.Input('LLR/TR', 'value'),
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
     # dash.dependencies.Input('LLR_Only', 'value'),
     # dash.dependencies.Input('E_TR_Only', 'value'),
     # dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),  # значение чеклиста из дерева с выбором столбцов
     dash.dependencies.Input('interface-data', 'value')
     ])
def update_pie_graph(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                     Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large, Owner,
                     Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month, col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    df_plot = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    df_plot = df_plot.sort_values('Year', ascending=False)  # отсортировнный по годам датафрейм

    width = 700
    height = 500

    pv = pd.pivot_table(
        df_plot,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    all_sqm = df_plot.SQM.sum()
    mylist = list(round(i) for i in pv["SQM"]/all_sqm*100)
    print(mylist)
    colors_pie = [color.colliers_dark_blue, color.colliers_extra_light_blue, color.colliers_grey_40,
                  color.colliers_yellow, color.colliers_red, color.colliers_light_blue]
    pie1 = go.Pie(values= pv["SQM"],
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
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = '2013-2018'

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
     # dash.dependencies.Input('LLR/TR', 'value'),
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
     # dash.dependencies.Input('LLR_Only', 'value'),
     # dash.dependencies.Input('E_TR_Only', 'value'),
     # dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),  # значение чеклиста из дерева с выбором столбцов
     dash.dependencies.Input('interface-data', 'value')
     ])
def update_graph_percent(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                         Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                         Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent, Month, col,
                         data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    df_plot = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    df_plot = df_plot.sort_values('Year', ascending=False)  # отсортированный по годам датафрейм

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

    # из исходного датафрейма с real получить список из str, причем каждому элементу добавить знак процента
    # чтобы отбросить 0 перевожу в интеджер, потом в строку, к строке + %, эту историю из строки обратно в список
    if len(df_plot['Agency'].unique()) == 6:
        data = []

        trace1 = go.Bar(x=pv1.index, y=pv1[("SQM", 'Colliers')] * 100 / pv2["SQM"].sum(),
                        name='Colliers',
                        marker=dict(
                            color=color.colliers_dark_blue),
                        width=0.4,
                        text=(
                            list(map(lambda x: str(x) + "%",
                                     list(((pv1[("SQM", 'Colliers')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                         np.int64))))),
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
                                     list(((pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                         np.int64))))),
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
                                     list(((pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                         np.int64))))),
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
                                     list(((pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                         np.int64))))),
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
                                     list(((pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                         np.int64))))),
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
                                     list(((pv1[("SQM", 'SAR')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                         np.int64))))),
                        textposition='auto',
                        textfont=dict(
                            color=color.white,
                            size=12))
        data.extend([trace1, trace2, trace3, trace4, trace5, trace6])

    elif len(df_plot['Agency'].unique()) < 6:
        data = []
        list_of_unique = df_plot['Agency'].unique()
        if 'Colliers' in list_of_unique:
            trace1 = go.Bar(x=pv1.index, y=pv1[("SQM", 'Colliers')] * 100 / pv2["SQM"].sum(),
                            name='Colliers',
                            marker=dict(
                                color=color.colliers_dark_blue),
                            width=0.4,
                            text=(
                                list(map(lambda x: str(x) + "%",
                                         list((
                                             (pv1[("SQM", 'Colliers')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                             np.int64))))),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace1)

        if 'CW' in list_of_unique:
            trace2 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum(),
                            name='CW',
                            marker=dict(
                                color=color.colliers_extra_light_blue),
                            width=0.4,
                            text=(
                                list(map(lambda x: str(x) + "%",
                                         list(((pv1[("SQM", 'CW')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                             np.int64))))),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace2)

        if 'CBRE' in list_of_unique:
            trace3 = go.Bar(x=pv1.index, y=pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum(),
                            name='CBRE',
                            marker=dict(
                                color=color.colliers_grey_40),
                            width=0.4,
                            text=(
                                list(map(lambda x: str(x) + "%",
                                         list(((pv1[("SQM", 'CBRE')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                             np.int64))))),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace3)

        if 'JLL' in list_of_unique:
            trace4 = go.Bar(x=pv1.index, y=pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum(),
                            name='JLL',
                            marker=dict(
                                color=color.colliers_yellow),
                            width=0.4,
                            text=(
                                list(map(lambda x: str(x) + "%",
                                         list(((pv1[("SQM", 'JLL')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                             np.int64))))),
                            textposition='auto',
                            textfont=dict(
                                color=color.colliers_grey_80,
                                size=12))
            data.append(trace4)

        if 'KF' in list_of_unique:
            trace5 = go.Bar(x=pv1.index, y=pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum(),
                            name='KF',
                            marker=dict(
                                color=color.colliers_red),
                            width=0.4,
                            text=(
                                list(map(lambda x: str(x) + "%",
                                         list(((pv1[("SQM", 'KF')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                             np.int64))))),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace5)

        if 'SAR' in list_of_unique:
            trace6 = go.Bar(x=pv1.index, y=pv1[("SQM", 'SAR')] * 100 / pv2["SQM"].sum(),
                            name='SAR',
                            marker=dict(
                                color=color.colliers_light_blue),
                            width=0.4,
                            text=(
                                list(map(lambda x: str(x) + "%",
                                         list(((pv1[("SQM", 'SAR')] * 100 / pv2["SQM"].sum()).apply(np.round)).apply(
                                             np.int64))))),
                            textposition='auto',
                            textfont=dict(
                                color=color.white,
                                size=12))
            data.append(trace6)

    list_of_ind = []
    for i in range(len(list_of_values_copy)):
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    annotations = []
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
                    autorange=True,
                    showgrid=True,
                    zeroline=True,
                    showline=True,
                    autotick=False,
                    ticks='',
                    showticklabels=True,
                    # title='Years'
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
     # dash.dependencies.Input('LLR/TR', 'value'),
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
     # dash.dependencies.Input('LLR_Only', 'value'),
     # dash.dependencies.Input('E_TR_Only', 'value'),
     # dash.dependencies.Input('LLR/E_TR', 'value'),
     dash.dependencies.Input('Month', 'value'),
     dash.dependencies.Input('interface-columns', 'values'),  # значение чеклиста из дерева с выбором столбцов
     dash.dependencies.Input('interface-data', 'value')

     ])
def update_graph_horizontal_total(Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                                  Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address,
                                  Submarket_Large, Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size,
                                  Sublease_Agent, Month, col, data_in):
    cond = dict(Year=[Year], Country=[Country], Agency=[Agency],
                # создание словаря с ключом - названием столбца, значением - выбранным параметрам
                City=[City], Property_Name=[Property_Name], Class=[Class],
                SQM=[SQM], Company=[Company], Business_Sector=[Business_Sector],
                Type_of_Deal=[Type_of_Deal], Type_of_Consultancy=[Type_of_Consultancy],
                Quarter=[Quarter], Include_in_Market_Share=[Include_in_Market_Share], Address=[Address],
                Submarket_Large=[Submarket_Large],
                Owner=[Owner], Date_of_acquiring=[Date_of_acquiring], Class_Colliers=[Class_Colliers], Floor=[Floor],
                Deal_Size=[Deal_Size], Sublease_Agent=[Sublease_Agent], Month=[Month])

    list_of_values = (Year, Country, Agency, City, Property_Name, Class, SQM, Business_Sector, Type_of_Deal,
                      Type_of_Consultancy, Quarter, Company, Include_in_Market_Share, Address, Submarket_Large,
                      Owner,
                      Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                      Month)
    cond_1 = cond.copy()
    list_of_values_copy = list(filter(None, list_of_values))

    df_plot = my_method.data_to_table_preparation(data_in, list_of_values_copy, cond_1)
    df_plot = df_plot.sort_values('Year', ascending=False)  # отсортированный по годам датафрейм

    width = 700
    height = 500

    pv = pd.pivot_table(
        df_plot,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)

    # ##print(pv['SQM'].sum())
    pv_sorted = pv.sort_values(by='SQM', ascending=True)
    # ##print((list(map(lambda x: x, list((pv_sorted[("SQM")] / 1000).apply(np.int64))))))
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
        ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
        list_of_ind.append(ind)

    if len(list_of_values_copy) == 0:
        format_data = 'All deals'
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' not in list_of_ind:  # перепчать этот код!
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = '2013-2018'

    if len(list_of_values_copy) > 0 and 'Year' in list_of_ind:
        list_of_values_copy_chain = list(chain(*list_of_values_copy))
        for i in Year:
            list_of_values_copy_chain.remove('{}'.format(i))
        format_data = ', '.join(str(e) for e in list_of_values_copy_chain)
        format_year = ', '.join(Year)

    annotations = []

    for agency, value in zip(pv_sorted.index, pv_sorted["SQM"] / 1000):
        # ##print('value=', value)
        # ##print('PV SQM SUM', pv['SQM'].sum() / 1000)
        # ##print(str(((value / pv['SQM'].sum())) * 100) + '%'),
        annotations.append(dict(
            x=value + 100,
            y=agency,
            # xref='x',
            # yref='y',
            text='<b>' + str(int(round(((value / (pv['SQM'].sum() / 1000)) * 100)))) + '%' + '</b>',
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

    for agency, value, text, color_1 in zip(pv_sorted.index, pv_sorted["SQM"] / 1000,
                                            list(map(lambda x: x, list((pv_sorted[("SQM")] / 1000).apply(np.int64)))),
                                            [color.white, color.white, color.white, color.white, color.white,
                                             color.colliers_grey_80]):
        annotations.append(dict(
            x=0.02,
            y=agency,
            xref='paper',
            # yref='y',
            text=text,
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
                    # title='Area in sq.m'
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
                # showlegend=False,
                barmode='stack',
                annotations=annotations,

            )
    }


''' КОЛБЭКИ СТРАНИЦЫ 'СОМНИТЕЛЬНЫЕ СДЕЛКИ' '''


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
                                 'width': '80px',
                                 }

            if 'Include_in_Market_Share' not in val:
                style_include = {'display': 'none',
                                 'width': '80px',
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
                                'width': '80px',
                                }

            if 'Agency' not in val:
                style_agency = {'display': 'none',
                                'width': '80px',
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
                                 'width': '80px',
                                 }

            if 'Country' not in val:
                style_country = {'display': 'none',
                                 'width': '80px',
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
                              'width': '80px',
                              }

            if 'City' not in val:
                style_city = {'display': 'none',
                              'width': '80px',
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
                                       'width': '80px',
                                       }

            if 'Property_Name' not in val:
                style_property_name = {'display': 'none',
                                       'width': '80px',
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
                               'width': '80px',
                               }

            if 'Class' not in val:
                style_class = {'display': 'none',
                               'width': '80px',
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
                             'width': '80px',
                             }

            if 'SQM' not in val:
                style_SQM = {'display': 'none',
                             'width': '80px',
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
                                 'width': '80px',
                                 }

            if 'SQM' not in val:
                style_Company = {'display': 'none',
                                 'width': '80px',
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
                                         'width': '80px',
                                         }

            if 'Business_Sector' not in val:
                style_Business_Sector = {'display': 'none',
                                         'width': '80px',
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
                                      'width': '80px',
                                      }

            if 'Type_of_Deal' not in val:
                style_Type_of_Deal = {'display': 'none',
                                      'width': '80px',
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
                                             'width': '80px',
                                             }

            if 'Type_of_Consultancy' not in val:
                style_Type_of_Consultancy = {'display': 'none',
                                             'width': '80px',
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
                                'width': '80px',
                                }

            if 'LLR_TR' not in val:
                style_LLR_TR = {'display': 'none',
                                'width': '80px',
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
                              'width': '80px',
                              }

            if 'Year' not in val:
                style_Year = {'display': 'none',
                              'width': '80px',
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
                                 'width': '80px',
                                 }
            if 'Quarter' not in val:
                style_Quarter = {'display': 'none',
                                 'width': '80px',
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
                                'width': '80px',
                                }

            if 'Address' not in val:
                style_Addres = {'display': 'none',
                                'width': '80px',
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
                                         'width': '80px',
                                         }

            if 'Submarket_Large' not in val:
                style_Submarket_Large = {'display': 'none',
                                         'width': '80px',
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
                               'width': '80px',
                               }

            if 'Owner' not in val:
                style_Owner = {'display': 'none',
                               'width': '80px',
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
                                           'width': '80px',
                                           }

            if 'Date_of_acquiring' not in val:
                style_Date_of_acquiring = {'display': 'none',
                                           'width': '80px',
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
                                        'width': '80px',
                                        }

            if 'Class_Colliers' not in val:
                style_Class_Colliers = {'display': 'none',
                                        'width': '80px',
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
                               'width': '80px',
                               }

            if 'Floor' not in val:
                style_Floor = {'display': 'none',
                               'width': '80px',
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
                                   'width': '80px',
                                   }

            if 'Deal_Size' not in val:
                style_Deal_Size = {'display': 'none',
                                   'width': '80px',
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
                                        'width': '80px',
                                        }

            if 'Sublease_Agent' not in val:
                style_Sublease_Agent = {'display': 'none',
                                        'width': '80px',
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
                                  'width': '80px',
                                  }

            if 'LLR_Only' not in val:
                style_LLR_Only = {'display': 'none',
                                  'width': '80px',
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
                                   'width': '80px',
                                   }

            if 'E_TR_Only' not in val:
                style_E_TR_Only = {'display': 'none',
                                   'width': '80px',
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
                                  'width': '80px',
                                  }

            if 'LLR/E_TR' not in val:
                style_LLR_E_TR = {'display': 'none',
                                  'width': '80px',
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
                               'width': '80px',
                               }

            if 'Month' not in val:
                style_Month = {'display': 'none',
                               'width': '80px',
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
                          Submarket_Large, Owner, Date_of_acquiring, Class_Colliers, Floor, Deal_Size, Sublease_Agent,
                          LLR_Only, E_TR_Only, LLR_E_TR, Month, col):
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

    suspecious_deals_df_equal_sqm = static.all_deals_query_df[
        static.all_deals_query_df.duplicated(['SQM'], keep=False)].sort_values(
        'SQM', ascending=False)
    # #print('equal SQM')
    # #print(suspecious_deals_df_equal_sqm['SQM'])

    sort_for_dif = static.all_deals_query_df.sort_values('SQM', ascending=False)
    suspecious_deals_df_sqm_diff_less_five = sort_for_dif[sort_for_dif['SQM'].diff() < 5]
    # #print('difference between SQM')
    # #print(suspecious_deals_df_sqm_diff_less_five)

    suspecious_deals_df_merged_by_equal_and_diff = pd.merge(suspecious_deals_df_equal_sqm,
                                                            suspecious_deals_df_sqm_diff_less_five, how='inner')
    # #print('merged')
    # #print(suspecious_deals_df_merged_by_equal_and_diff)

    # suspecious_deals_df_sqm_diff_year = sort_for_dif[sort_for_dif['Year'].diff() <= 1]
    # suspecious_deals_df_sqm_diff_year_sorted = suspecious_deals_df_sqm_diff_year.sort_values('Year', ascending=False)
    # ##print('suspecious_deals_df_sqm_diff_year_sorted')
    # ##print(suspecious_deals_df_sqm_diff_year_sorted)

    sort_for_dif = static.all_deals_query_df.sort_values('Quarter', ascending=False)
    suspecious_deals_df_quar_diff = sort_for_dif[sort_for_dif['Quarter'].diff() <= 2]

    suspecious_deals_df_merged_by_equal_year_qurter_diff = pd.merge(suspecious_deals_df_merged_by_equal_and_diff,
                                                                    suspecious_deals_df_quar_diff, how='inner')

    suspecious_deals_total = suspecious_deals_df_merged_by_equal_year_qurter_diff

    if len(list_of_values_copy) == 0:
        return suspecious_deals_total[col].to_dict('records')
    if len(list_of_values_copy) != 0:
        for i in range(len(list_of_values_copy)):
            ind = my_method.get_key(cond_1, [list_of_values_copy[i]])
            if i == 0:
                data = suspecious_deals_total[(suspecious_deals_total[ind].isin(list_of_values_copy[i]))]
            else:
                data = suspecious_deals_total[(suspecious_deals_total[ind].isin(list_of_values_copy[i]))]
        return data[col].to_dict('records')


''' Обновление базы данных по сделкам  '''


@app.callback(
    dash.dependencies.Output('download-example-button', 'href'),
    # формирования файла-шаблона с первой строкой - названием столбцов таблицы
    [dash.dependencies.Input('download-example-button', 'n_clicks')]
)
def example_button(n_clicks):
    data = pd.DataFrame.from_records([static.list_of_columns])  # создание датафрейма из списка заголовков столбца
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
            df.columns = static.list_of_columns
        elif 'xls' in filename:  # проверка, является ли загруженный файл xls, не всегда работает корректно, так что пока лучше остановиться на csv
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
            df.columns = static.list_of_columns
    except Exception as e:
        # #print(e)
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
        # #print(e)
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
        dff.columns = static.list_of_columns
        dff.to_sql('Market_Share', static.con, if_exists='append', index=None, index_label=static.list_of_columns)
        return  # #print('База обновлена')
    else:
        print('empty json')


'''  обновление страницы: если параметра pathname совпадает с ссылкой страницы, то отрисовывается выбранная страница '''


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-deals':
        return page_deals_layout
    elif pathname == '/page-update-database':
        return page_update_database_layout
    elif pathname == '/suspicious_deals':
        return suspicious_deals_layout
    elif pathname == '/page-default-graphs':
        return page_default_graphs_and_tabs
    elif pathname == '/page-help':
        return page_help_layout
    elif pathname == '/page-about':
        return page_about_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True, host='10.168.207.102')
