import dash_html_components as html
import colors_and_fonts as color


def get_key(d, value):
    """ФУНКЦИЯ ВОЗВРАЩЕНИЯ ИМЕНИ КЛЮЧА В СЛОВАРЕ ПО ЗНАЧЕНИЮ"""
    for k, v in d.items():
        if v == value:
            return k


def generate_table_top_deals(dataframe, max_rows=10):
    """ФУНКЦИЯ ОТРИСОВКИ ТАБЛИЦЫ ЧЕРЕЗ  HTML, ДЛЯ НАСТРОЙКИ СТИЛЯ ИСПОЛЬЗУЕТСЯ CSS РАЗМЕТКА"""
    return html.Table(
        [
            html.Tr(    # HEADER
                [
                    html.Th(col,
                            style={
                                'text-align': 'center',
                                'width': wid,
                                'height': '20px'
                            })
                    for col, wid in zip(["Agency", "Property Name", "Office area", "Company", "Business Sector", "Type of Deal"],
                                     ['70px', '175px', '105px', '171px', '229px', '102px'])
                ],
                style={  # CSS разметка
                     'background-color': color.colliers_light_blue,
                     'color': color.white
                }
            )
        ]
        +
        [
            html.Tr(            # BODY
                [
                    html.Td(dataframe.iloc[i][col],
                            style={
                                'text-align': 'center',
                                'width': wid,
                                'height': '20px'

                            })
                    for col, wid in zip(dataframe.columns, ['70px', '175px', '105px', '171px', '229px', '102px'])
                ],
                style={  # CSS разметка
                      'background-color': color.colliers_pale_blue,
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
