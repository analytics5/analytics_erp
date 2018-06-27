import project_methods as my_method
import project_colors_and_fonts as color
import project_static as static
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import base64
import numpy as np



# БЛОК КОДА ПО ОТРИСОВКЕ ШАБЛОНОВ ДЛЯ ПРЕЗЕНТАЦИИ

def update_pie_graph_for_pres():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['1'])) & (df_plot['Country'].isin(['RU']))]
    df_graph = data

    width = 700
    height = 500

    pv = pd.pivot_table(
        df_graph,
        index=["Agency"],
        values=["SQM"],
        aggfunc=sum,
        fill_value=0)
    colors_pie = [color.cbre_color, color.cw_color, color.colliers_color,
                  color.jll_color, color.kf_color, color.sar_color]
    pie1 = go.Pie(values=round(pv["SQM"]),
                  labels=pv.index,
                  hoverinfo='label+value+percent',
                  textinfo='percent',
                  textposition='inside',
                  textfont=dict(
                      color=color.white,
                      size=12,
                      family='Arial, bold'),
                  marker=dict(colors=colors_pie,
                              line=dict(
                                  color=color.white,
                                  width=1
                              )
                              )
                  )
    #image_data =

    # img = py.image.get(image_data, format='png')
    # plot_bytes_encode = str(base64.b64encode(img))
    # plot_bytes_encode = plot_bytes_encode[0:-1]
    # plot_bytes_encode_fin = plot_bytes_encode[2:]
    # stringpic = "data:image/png;base64," + plot_bytes_encode_fin  # строчка с байткодом картинки
    # # stringpic = plot_url_png                # строчка с сылкой на файл картинки на сайте плотли

    return {
        'data': [pie1],
        'layout': go.Layout(
            title='<b>'+'Объём сделок (аренда и продажа)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="v",
                        traceorder="normal"),
        )
    }


def update_table_for_pres():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    all_deals_2018 = static.all_deals_query_df
    all_deals_2018 = all_deals_2018[
        (all_deals_2018['Year'].isin(['2018'])) & (all_deals_2018['Quarter'].isin(['1'])) & (all_deals_2018['Country'].isin(['RU']))]
    all_deals_2018 = all_deals_2018[['SQM','Agency']]
    all_deals_2018['Percent'] = (all_deals_2018[['SQM']] / all_deals_2018['SQM'].sum())*100
    all_deals_2018 = all_deals_2018.groupby('Agency',as_index=False).sum()
    all_deals_2018['SQM'] = all_deals_2018['SQM'].apply(np.round).astype(int)
    all_deals_2018['Percent'] = all_deals_2018['Percent'].apply(np.round).astype(int).astype(str) + '%'
    all_deals_2018 = all_deals_2018.sort_values('SQM', ascending=False)

    nan_df = pd.DataFrame(
        {'Agency': [np.nan],
         'SQM': [all_deals_2018['SQM'].sum()],
         'Percent': [np.nan]
         })
    all_deals_2018 = pd.concat((all_deals_2018, nan_df))
    return my_method.generate_table_for_pres_1(all_deals_2018)
