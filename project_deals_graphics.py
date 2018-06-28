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
                  hoverinfo='skip',
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
            legend=dict(orientation="h",
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

# ______________________________________________________________


def update_pie_graph_def_sale_lease_1q_2018_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['1'])) & (df_plot['Country'].isin(['RU']))]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_sale_1q_2018_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['1'])) & (df_plot['Country'].isin(['RU']))]
    data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (продажа)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_lease_1q_2018_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['1'])) & (df_plot['Country'].isin(['RU']))]
    data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (аренда)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def update_pie_graph_def_sale_lease_2q_2018_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    if not df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:

        data = df_plot[
            (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2'])) & (df_plot['Country'].isin(['RU']))]
        df_graph = data

        width = 600
        height = 450

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
                      hoverinfo='skip',
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
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

    if df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:
            return {
            'data': [go.Pie(values=[1],
                      labels=['NONE'],
                      hoverinfo='skip',
                      textinfo='percent',
                      textposition='inside',
                      textfont=dict(
                          color=color.white,
                          size=12,
                          family='Arial, bold'),
                      marker=dict(colors=color.colliers_grey_80,
                                  line=dict(
                                      color=color.white,
                                      width=1
                                  )
                                  )
                      )],
            'layout': go.Layout(
                title='<b>' + 'НЕТ ДАННЫХ' + '</b>',
                width=600,
                height=450,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }


def update_pie_graph_def_sale_2q_2018_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    if not df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:

        data = df_plot[
            (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2'])) & (df_plot['Country'].isin(['RU']))]
        data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
        df_graph = data

        width = 600
        height = 450

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
                      hoverinfo='skip',
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
                title='<b>'+'Объём сделок (продажа)'+'</b>',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }
    if df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:

        return {
            'data': [go.Pie(values=[1],
                           labels=['NONE'],
                           hoverinfo='skip',
                           textinfo='percent',
                           textposition='inside',
                           textfont=dict(
                               color=color.white,
                               size=12,
                               family='Arial, bold'),
                           marker=dict(colors=color.colliers_grey_80,
                                       line=dict(
                                           color=color.white,
                                           width=1
                                       )
                                       )
                           )],
            'layout': go.Layout(
                title='<b>' + 'НЕТ ДАННЫХ' + '</b>',
                width=600,
                height=450,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }


def update_pie_graph_def_lease_2q_2018_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 2 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    print(type(df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]))
    if not df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:

        data = df_plot[
            (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2'])) & (df_plot['Country'].isin(['RU']))]
        data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
        df_graph = data

        width = 600
        height = 450

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
                      hoverinfo='skip',
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
                title='<b>'+'Объём сделок (аренда)'+'</b>',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }
    if df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:

        return {
            'data': [go.Pie(values=[1],
                           labels=['NONE'],
                           hoverinfo='skip',
                           textinfo='percent',
                           textposition='inside',
                           textfont=dict(
                               color=color.white,
                               size=12,
                               family='Arial, bold'),
                           marker=dict(colors=color.colliers_grey_80,
                                       line=dict(
                                           color=color.white,
                                           width=1
                                       )
                                       )
                           )],
            'layout': go.Layout(
                title='<b>' + 'НЕТ ДАННЫХ' + '</b>',
                width=600,
                height=450,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def update_pie_graph_def_sale_lease_2017_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2017'])) & (df_plot['Country'].isin(['RU']))]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_sale_2017_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2017'])) & (df_plot['Country'].isin(['RU']))]
    data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (продажа)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_lease_2017_ru():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2017'])) & (df_plot['Country'].isin(['RU']))]
    data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (аренда)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def update_pie_graph_def_sale_lease_1q_2018_mos():  # pie по ДОЛЯ РЫНКА ПО МОСКВЕ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['1'])) & (df_plot['Country'].isin(['RU'])) & (df_plot['City'].isin(['Moscow']))]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_sale_1q_2018_mos():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['1']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['Moscow']))]
    data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (продажа)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_lease_1q_2018_mos():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['1']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['Moscow']))]
    data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (аренда)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def update_pie_graph_def_sale_lease_2q_2018_mos():  # pie по ДОЛЯ РЫНКА ПО МОСКВЕ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    if not df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:
        data = df_plot[
            (df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2'])) & (df_plot['Country'].isin(['RU'])) & (df_plot['City'].isin(['Moscow']))]
        df_graph = data

        width = 600
        height = 450

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
                      hoverinfo='skip',
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
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }
    if df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:
        return {
            'data': [go.Pie(values=[1],
                           labels=['NONE'],
                           hoverinfo='skip',
                           textinfo='percent',
                           textposition='inside',
                           textfont=dict(
                               color=color.white,
                               size=12,
                               family='Arial, bold'),
                           marker=dict(colors=color.colliers_grey_80,
                                       line=dict(
                                           color=color.white,
                                           width=1
                                       )
                                       )
                           )],
            'layout': go.Layout(
                title='<b>' + 'НЕТ ДАННЫХ' + '</b>',
                width=600,
                height=450,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }


def update_pie_graph_def_sale_2q_2018_mos():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    if not df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:
        data = df_plot[
            (df_plot['Year'].isin(['2018']))
            & (df_plot['Quarter'].isin(['2']))
            & (df_plot['Country'].isin(['RU']))
            & (df_plot['City'].isin(['Moscow']))]
        data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
        df_graph = data

        width = 600
        height = 450

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
                      hoverinfo='skip',
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
                title='<b>'+'Объём сделок (продажа)'+'</b>',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }
    if df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:

        return {
            'data': [go.Pie(values=[1],
                           labels=['NONE'],
                           hoverinfo='skip',
                           textinfo='percent',
                           textposition='inside',
                           textfont=dict(
                               color=color.white,
                               size=12,
                               family='Arial, bold'),
                           marker=dict(colors=color.colliers_grey_80,
                                       line=dict(
                                           color=color.white,
                                           width=1
                                       )
                                       )
                           )],
            'layout': go.Layout(
                title='<b>' + 'НЕТ ДАННЫХ' + '</b>',
                width=600,
                height=450,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }


def update_pie_graph_def_lease_2q_2018_mos():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    if not df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:
        data = df_plot[
            (df_plot['Year'].isin(['2018']))
            & (df_plot['Quarter'].isin(['2']))
            & (df_plot['Country'].isin(['RU']))
            & (df_plot['City'].isin(['Moscow']))]
        data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
        df_graph = data

        width = 600
        height = 450

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
                      hoverinfo='skip',
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
                title='<b>'+'Объём сделок (аренда)'+'</b>',
                width=width,
                height=height,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }
    if df_plot[(df_plot['Year'].isin(['2018'])) & (df_plot['Quarter'].isin(['2']))]['SQM'].empty:

        return {
            'data': [go.Pie(values=[1],
                           labels=['NONE'],
                           hoverinfo='skip',
                           textinfo='percent',
                           textposition='inside',
                           textfont=dict(
                               color=color.white,
                               size=12,
                               family='Arial, bold'),
                           marker=dict(colors=color.colliers_grey_80,
                                       line=dict(
                                           color=color.white,
                                           width=1
                                       )
                                       )
                           )],
            'layout': go.Layout(
                title='<b>' + 'НЕТ ДАННЫХ' + '</b>',
                width=600,
                height=450,
                legend=dict(orientation="h",
                            traceorder="normal"),
            )
        }

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def update_pie_graph_def_sale_lease_1q_2018_sp():  # pie по ДОЛЯ РЫНКА ПО МОСКВЕ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018']))
        & (df_plot['Quarter'].isin(['1']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['St. Pete']))]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_sale_1q_2018_sp():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018']))
        & (df_plot['Quarter'].isin(['1']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['St. Pete']))]
    data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (продажа)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_lease_1q_2018_sp():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018']))
        & (df_plot['Quarter'].isin(['1']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['St. Pete']))]
    data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (аренда)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def update_pie_graph_def_sale_lease_2017_sp():  # pie по ДОЛЯ РЫНКА ПО МОСКВЕ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2017']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['St. Pete']))]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_sale_2017_sp():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['St. Pete']))]
    data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (продажа)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_lease_2017_sp():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['St. Pete']))]
    data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (аренда)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def update_pie_graph_def_sale_lease_2017_mos():  # pie по ДОЛЯ РЫНКА ПО МОСКВЕ В 1 КВ. 2018 ВСЕ СДЕЛКИ / СДЕЛКИ АРЕНДЫ
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2017']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['Moscow']))]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_sale_2017_mos():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['Moscow']))]
    data = data[data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (продажа)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }


def update_pie_graph_def_lease_2017_mos():  # pie по ДОЛЯ РЫНКА ПО РОССИИ В 1 КВ. 2018 SALE
    df_plot = static.all_deals_query_df.copy()
    data = df_plot[
        (df_plot['Year'].isin(['2018']))
        & (df_plot['Country'].isin(['RU']))
        & (df_plot['City'].isin(['Moscow']))]
    data = data[~data['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    df_graph = data

    width = 600
    height = 450

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
                  hoverinfo='skip',
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
            title='<b>'+'Объём сделок (аренда)'+'</b>',
            width=width,
            height=height,
            legend=dict(orientation="h",
                        traceorder="normal"),
        )
    }