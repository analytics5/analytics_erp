def get_key(d, value):
    """ФУНКЦИЯ ВОЗВРАЩЕНИЯ ИМЕНИ КЛЮЧА В СЛОВАРЕ ПО ЗНАЧЕНИЮ"""
    for k, v in d.items():
        if v == value:
            return k

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



