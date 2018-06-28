import dash_html_components as html
import project_colors_and_fonts as color
import project_static as static
import pandas as pd

def get_key(d, value):
    """ФУНКЦИЯ ВОЗВРАЩЕНИЯ ИМЕНИ КЛЮЧА В СЛОВАРЕ ПО ЗНАЧЕНИЮ"""
    for k, v in d.items():
        if v == value:
            return k


def generate_table_top_deals(dataframe, max_rows=10):
    """ФУНКЦИЯ ОТРИСОВКИ ТАБЛИЦЫ ЧЕРЕЗ  HTML, ДЛЯ НАСТРОЙКИ СТИЛЯ ИСПОЛЬЗУЕТСЯ CSS РАЗМЕТКА"""
    return html.Table(
        [
            html.Tr(  # HEADER
                [
                    html.Th(col,
                            style={
                                'text-align': pos,
                                'width': wid,
                                'height': hei
                            })
                    for col, wid, hei,pos in zip(["Agency", "Property Name","City", "Office area", "Company",
                                              "Business Sector", "Type of Deal"],
                                             ['70px', '175px','70px','105px', '171px', '229px', '102px'],
                                             ['20px', '20px', '20px', '20px', '20px', '20px', '20px'],
                                             ['left', 'left', 'center', 'center', 'left', 'left', 'center'])
                ],
                style={  # CSS разметка
                    'background-color': color.colliers_light_blue,
                    'color': color.white,

                }
            )
        ]
        +
        [
            html.Tr(  # BODY
                [
                    html.Td(dataframe.iloc[i][col],
                            style={
                                'text-align': pos,
                                'width': wid,
                                'height': hei

                            })
                    for col, wid, hei, pos in zip(dataframe.columns,
                                             ['70px', '175px','70px', '105px', '171px', '229px', '102px'],
                                             ['20px', '20px', '20px', '20px', '20px', '20px', '20px'],
                                             ['left', 'left', 'center', 'center', 'left', 'left', 'center']
                                             )
                ],
                style={  # CSS разметка
                    'background-color': color.colliers_pale_blue,
                }
            ) for i in range(min(len(dataframe), max_rows))]
    )


def generate_table_top_deals_with_year(dataframe, max_rows=10):
    """ФУНКЦИЯ ОТРИСОВКИ ТАБЛИЦЫ ЧЕРЕЗ  HTML, ДЛЯ НАСТРОЙКИ СТИЛЯ ИСПОЛЬЗУЕТСЯ CSS РАЗМЕТКА"""
    return html.Table(
        [
            html.Tr(  # HEADER
                [
                    html.Th(col,
                            style={
                                'text-align': pos,
                                'width': wid,
                                'height': hei
                            })
                    for col, wid, hei, pos in zip(["Agency", "Property Name", "City", "Office area", "Company",
                                              "Business Sector", "Type of Deal", 'Year', 'Quarter'],
                                             ['70px', '175px', '70px', '105px', '171px', '229px',
                                              '102px', '60px', '30px'],
                                             ['20px', '20px', '20px', '20px', '20px', '20px', '20px','20px', '20px'],
                                                  ['left', 'left', 'center', 'center', 'left', 'left', 'center',
                                                   'center', 'center'])
                ],
                style={  # CSS разметка
                    'background-color': color.colliers_light_blue,
                    'color': color.white,

                }
            )
        ]
        +
        [
            html.Tr(  # BODY
                [
                    html.Td(dataframe.iloc[i][col],
                            style={
                                'text-align': pos,
                                'width': wid,
                                'height': hei

                            })
                    for col, wid, hei, pos in zip(dataframe.columns, ['70px', '175px', '70px', '105px', '171px', '229px',
                                              '102px', '60px', '30px'],
                                             ['20px', '20px', '20px', '20px', '20px', '20px', '20px', '20px', '20px'],
                                                  ['left', 'left', 'center', 'center', 'left', 'left', 'center',
                                                   'center', 'center'])
                ],
                style={  # CSS разметка
                    'background-color': color.colliers_pale_blue,
                }
            ) for i in range(min(len(dataframe), max_rows))]
    )


def generate_table_for_pres_1(dataframe, max_rows=10):
    """ФУНКЦИЯ ОТРИСОВКИ ТАБЛИЦЫ ЧЕРЕЗ  HTML, ДЛЯ НАСТРОЙКИ СТИЛЯ ИСПОЛЬЗУЕТСЯ CSS РАЗМЕТКА"""
    return html.Table(
        [
            html.Tr(  # HEADER
                [
                    html.Th(col,
                            style={
                                'text-align': 'center',
                                'width': wid,
                                'height': hei
                            })
                    for col, wid, hei in zip([" ", "Объём, кв. м", "Доля в объёме"],
                                             ['110px', '215px', '175px'],
                                             ['15px', '15px', '15px'])
                ],
                style={  # CSS разметка
                    'background-color': color.colliers_light_blue,
                    'color': color.white,
                    'allign': 'left'

                }
            )
        ]
        +
        [
            html.Tr(  # BODY
                [
                    html.Td(dataframe.iloc[i][col],
                            style={
                                'text-align': 'right',
                                'width': wid,
                                'height': hei

                            })
                    for col, wid, hei in zip(dataframe.columns,
                                             ['110px', '215px', '175px'],
                                             ['15px', '15px', '15px'])
                ],
                style={  # CSS разметка
                    'background-color': color.colliers_pale_blue,
                    'allign': 'left'
                }
            ) for i in range(min(len(dataframe), max_rows))]
    )


def replace_index(list_of_ind):
    """ФУНКЦИЯ УБИРАЕТ НИЖНИЕ ПОДЧЕРКИВАНИЯ В НАЗВАНИИ ИНДЕКСОВ ДЛЯ ВЫВОДА НА ЭКРАН"""
    list_of_ind = [w.replace('Property_Name', 'Property name') for w in list_of_ind]
    list_of_ind = [w.replace('Business_Sector', 'Business sector') for w in list_of_ind]
    list_of_ind = [w.replace('Type_of_Deal', 'Type of deal') for w in list_of_ind]
    list_of_ind = [w.replace('Type_of_Consultancy', 'Type of consultancy') for w in list_of_ind]
    list_of_ind = [w.replace('LLR_TR', 'LLR/TR') for w in list_of_ind]
    list_of_ind = [w.replace('Include_in_Market_Share', 'Include in market share') for w in list_of_ind]
    list_of_ind = [w.replace('Submarket_Large', 'Submarket') for w in list_of_ind]
    list_of_ind = [w.replace('Date_of_acquiring', 'Date of acquiring') for w in list_of_ind]
    list_of_ind = [w.replace('Class_Colliers', 'Class Colliers') for w in list_of_ind]
    list_of_ind = [w.replace('Deal_Size', 'Deal size') for w in list_of_ind]
    list_of_ind = [w.replace('Sublease_Agent', 'Sublease agent') for w in list_of_ind]
    list_of_ind = [w.replace('LLR_Only', 'LLR') for w in list_of_ind]
    list_of_ind = [w.replace('E_TR_Only', '(E)TR') for w in list_of_ind]
    list_of_ind = [w.replace('LLR_E_TR', 'LLR/(E)TR') for w in list_of_ind]
    print(list_of_ind)
    return list_of_ind


def data_to_table_preparation(llr_type, list_of_values_copy, cond_1, sale_type):
    """ФИЛЬТРУЕТ ДАННЫЕ ДЛЯ ТАБЛИЦЫ И ГРАФИКОВ ПО ЗНАЧЕНИЯМ, ВЫБРАННЫМ В ПОЛЕ СЛЕВА"""

    if 'All deals' in llr_type:
        data_to_table = static.all_deals_query_df
        if len(list_of_values_copy) != 0:
            for i in range(len(list_of_values_copy)):
                ind = get_key(cond_1, [list_of_values_copy[i]])
                data_to_table = data_to_table[(data_to_table[ind].isin(list_of_values_copy[i]))]
    if 'LLR' in llr_type:
        data_to_table = static.all_deals_query_df[static.all_deals_query_df['LLR_Only'].isin(['Y'])]
        if len(list_of_values_copy) != 0:
            for i in range(len(list_of_values_copy)):
                ind = get_key(cond_1, [list_of_values_copy[i]])
                data_to_table = data_to_table[(data_to_table[ind].isin(list_of_values_copy[i]))]
    if '(E)TR' in llr_type:
        data_to_table = static.all_deals_query_df[static.all_deals_query_df['E_TR_Only'].isin(['Y'])]
        if len(list_of_values_copy) != 0:
            for i in range(len(list_of_values_copy)):
                ind = get_key(cond_1, [list_of_values_copy[i]])
                data_to_table = data_to_table[(data_to_table[ind].isin(list_of_values_copy[i]))]
    if 'LLR/(E)TR' in llr_type:
        data_to_table = static.all_deals_query_df[static.all_deals_query_df['LLR/E_TR'].isin(['Y'])]
        if len(list_of_values_copy) != 0:
            for i in range(len(list_of_values_copy)):
                ind = get_key(cond_1, [list_of_values_copy[i]])
                data_to_table = data_to_table[(data_to_table[ind].isin(list_of_values_copy[i]))]
    if 'All LLR (include double)' in llr_type:
        data_to_table_double = static.all_deals_query_df[static.all_deals_query_df['LLR/E_TR'].isin(['Y'])]
        data_to_table_llr = static.all_deals_query_df[static.all_deals_query_df['LLR_Only'].isin(['Y'])]
        data_to_table = pd.concat([data_to_table_double, data_to_table_llr], join='outer')
        if len(list_of_values_copy) != 0:
            for i in range(len(list_of_values_copy)):
                ind = get_key(cond_1, [list_of_values_copy[i]])
                data_to_table = data_to_table[(data_to_table[ind].isin(list_of_values_copy[i]))]
    if 'All (E)TR (include double)' in llr_type:
        data_to_table_double = static.all_deals_query_df[static.all_deals_query_df['LLR/E_TR'].isin(['Y'])]
        data_to_table_etr = static.all_deals_query_df[static.all_deals_query_df['E_TR_Only'].isin(['Y'])]
        data_to_table = pd.concat([data_to_table_double, data_to_table_etr], join='outer')
        if len(list_of_values_copy) != 0:
            for i in range(len(list_of_values_copy)):
                ind = get_key(cond_1, [list_of_values_copy[i]])
                data_to_table = data_to_table[(data_to_table[ind].isin(list_of_values_copy[i]))]

    if "Sale" in sale_type:
        data_to_table_2 = data_to_table[data_to_table['Include_in_Market_Share'].isin(['Y']) &
                                      data_to_table['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    if "Lease" in sale_type:
        data_to_table_2 = data_to_table[data_to_table['Include_in_Market_Share'].isin(['Y']) &
                                      ~data_to_table['Type_of_Deal'].isin(['Sale', 'Purchase'])]

    if "Sale and Lease" in sale_type:
        data_to_table_2 = data_to_table

    return data_to_table_2


