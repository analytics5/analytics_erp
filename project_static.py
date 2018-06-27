import pandas as pd
import psycopg2 as pg
import sqlalchemy
import project_sql as sql

country = ("Russia", "Ukraine", "Belarus", "Kazakhstan ",
           "Azerbaijan")  # кортеж со списком стран доля выпадающего списка
country_ind = ("RU", "UA", "BY", "KZ", "AZ")  # кортеж со списком стран доля выпадающего списка
years = (  # "All years",
    "2013", "2014", "2015", "2016", "2017", "2018")  # кортеж со списком годов доля выпадающего списка
Agency = (
    "Colliers", "KF", "JLL", "CW", "SAR", "CBRE")  # кортеж со списком компаний доля выпадающего списка
agency_list = ['Colliers', 'CBRE', 'CW', 'JLL', 'KF', 'SAR']  # список с компаниями для отрисовки
Agency_tab = ("Colliers", "KF", "JLL", "CW", "SAR", "CBRE")  # кортеж со списком компаний доля выпадающего списка
list_of_columns = [
    "Include_in_Market_Share",
    "Agency",
    "Country",
    "City",  # список заголовков таблицы по всем сделкам
    "Property_Name",
    "Address",
    "Submarket_Large",
    "Owner",
    "Date_of_acquiring",
    "Class",
    "Class_Colliers",
    "Floor",
    "SQM",
    "Deal_Size",
    "Company",
    "Business_Sector",
    "Sublease_Agent",
    "Type_of_Deal",
    "Type_of_Consultancy",
    # "LLR_TR",
    # "LLR_Only",
    # "E_TR_Only",
    # "LLR/E_TR",
    "Month",
    "Year",
    "Quarter"]

list_of_columns_for_example = [        # список заголовков таблицы для шаблона загрузки
    "Include_in_Market_Share",
    "Agency",
    "Country",
    "City",
    "Property_Name",
    "Address",
    "Submarket_Large",
    "Owner",
    "Date_of_acquiring",
    "Class",
    "Class_Colliers",
    "Floor",
    "SQM",
    "Deal_Size",
    "Company",
    "Business_Sector",
    "Sublease_Agent",
    "Type_of_deal",
    "Type_of_Consultancy",
    "LLR/TR",
    "LLR_Only",
    "E_TR_Only",
    "LLR/E_TR",
    "Month",
    "Year",
    "Quarter"]

list_of_columns_dataframe = [  # список заголовков таблицы по всем сделкам
    "Include_in_Market_Share",
    "Agency",
    "Country",
    "City",
    "Property_Name",
    "Address",
    "Submarket_Large",
    "Owner",
    "Date_of_acquiring",
    "Class",
    "Class_Colliers",
    "Floor",
    "SQM",
    "Deal_Size",
    "Company",
    "Business_Sector",
    "Sublease_Agent",
    "Type_of_Deal",
    "Type_of_Consultancy",
    "LLR_TR",
    "LLR_Only",
    "E_TR_Only",
    "LLR/E_TR",
    "Month",
    "Year",
    "Quarter"]

list_of_columns_suspicious = [  # список заголовков таблицы по сомнительным сделкам
    'Agency',
    'Country',
    'City',
    'Property Name',
    'Class',
    'SQM',
    'Company',
    'Type_of_Consultancy',
    'Year',
    'Quarter']

list_of_columns_for_gui = [  # список чеклиста для выбора столбцов таблицы из дерева
    "Include in market share",
    "Agency",
    "Country",
    "City",
    "Property name",
    "Address",
    "Submarket large",
    "Owner",
    "Date of acquiring",
    "Class",
    "Class Colliers",
    "Floor",
    "SQM",
    "Size of deal",
    "Company",
    "Business sector",
    "Sublease agent",
    "Type of deal",
    "Type of consultancy",
    # "LLR/TR",
    # "LLR",
    # "(E)TR",
    # "LLR/(E)TR",
    "Month",
    "Year",
    "Quarter"]

list_of_graphics_for_gui = [  # список чеклиста для выбора графика из дерева
    "Bar-stacked",
    "Bar-stacked-horizontal",
    "Bar-unstacked",
    "Pie-chart",
    "Bar-stacked-percent",
    "Bar-horizontal",
    # "LLR, (E)TR, LLR/(E)TR-pie-2017-RU",
    # 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU',
    # "LLR, (E)TR, LLR/(E)TR-pie-five-years-RU",
    # "LLR, (E)TR, LLR/(E)TR-pie-2017-MOS",
    # 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS',
    # "LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS",
    # 'biggest-deal-tab-2017',
    # 'biggest-deal-tab-1q2018',
    # 'biggest-deal-tab-2013-2018',
    # 'biggest-deal-tab-test'
]

list_of_deals_type = [  # список чеклиста для сортировки сделок из дерева llr/tr
    "All deals",
    "LLR",
    "(E)TR",
    "LLR/(E)TR",
    "All LLR (include double)",
    "All (E)TR (include double)"
]

list_of_deals_type_sale_lease = [   # список чеклиста для сортировки сделок из дерева sale / lease
    "Sale",
    "Lease",
    "Sale and Lease"
]


list_of_static_images = [
    "Bar-stacked",
    "Bar-stacked-horizontal",
    "Bar-unstacked",
    "Pie-chart",
    "Bar-stacked-percent",
    "Bar-horizontal",
    # "LLR, (E)TR, LLR/(E)TR-pie-2017-RU",
    # 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU',
    # "LLR, (E)TR, LLR/(E)TR-pie-five-years-RU",
    # "LLR, (E)TR, LLR/(E)TR-pie-2017-MOS",
    # 'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS',
    # "LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS"
]

list_of_default_graphics = [  # список чеклиста для выбора дефолтных графиков и таблиц из дерева
    "LLR, (E)TR, LLR/(E)TR-pie-2017-RU",
    'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-RU',
    "LLR, (E)TR, LLR/(E)TR-pie-five-years-RU",
    "LLR, (E)TR, LLR/(E)TR-pie-2017-MOS",
    'LLR, (E)TR, LLR/(E)TR-pie-1Q2018-MOS',
    "LLR, (E)TR, LLR/(E)TR-pie-five-years-MOS",
    'biggest-deal-tab-2017',
    'biggest-deal-tab-1q2018',
    'biggest-deal-tab-2013-2018',
]

dbname = 'postgres'  # название базы данных
host = 'localhost'  # IP адрес хоста, если сервер локальный, "localhost"
user = 'postgres'  # имя учетной записи в БД
password = '3334'  # пароль для подключения к БД
port = '5432'  # порт для подключения к БД
conn = pg.connect(dbname=dbname, host=host, user=user,
                  password=password)  # подключение к базе данных с помощью psycopg2

url = 'postgresql://{}:{}@{}:{}/{}'  # подключение к базе данных с помощью sqlalchemy
url = url.format(user, password, host, port, dbname)
con = sqlalchemy.create_engine(url, client_encoding='utf8')
meta = sqlalchemy.MetaData(bind=con, reflect=True)

all_deals_query = sql.table_query_new_all  # датафрейм с дампом всей базы по сделкам
suspicious_deals = sql.table_query  # датафрейм с дампом базы по сомнительным сделкам, возможно, стоит убрать

with conn:
    cur = conn.cursor()  # запорос к БД через psycopg2
    # cur.execute(sql.delete_query_1)
    # cur.execute(sql.delete_query_2)

    cur.execute(all_deals_query)  # исполнение SQL команды по дампу всей базы
    all_deals_query_data = cur.fetchall()  # запись данных во временную переменную
    all_deals_query_df = pd.DataFrame(all_deals_query_data)  # запись данных в pandas data frame
    all_deals_query_df.columns = list_of_columns_dataframe  # имена столбцов датафрейма по сделкам
    all_deals_query_df = all_deals_query_df.sort_values('Year', ascending=False)  # отсортировнный по годам датафрейм
    all_deals_query_df["LLR_Only"] = all_deals_query_df["LLR_Only"].replace(
        {True: 'Y', False: 'N'})  # замена булевых значений на yes и no
    all_deals_query_df["E_TR_Only"] = all_deals_query_df["E_TR_Only"].replace(
        {True: 'Y', False: 'N'})  # замена булевых значений на yes и no
    all_deals_query_df["LLR/E_TR"] = all_deals_query_df["LLR/E_TR"].replace(
        {True: 'Y', False: 'N'})  # замена булевых значений на yes и no

    cur.execute(suspicious_deals)  # выполнение SQL запроса по сделкам
    suspicious_deals_data = cur.fetchall()  # данные по сделкам
    suspicious_deals_df = pd.DataFrame(suspicious_deals_data)  # Запись в датафрейм
    suspicious_deals_df.columns = list_of_columns_suspicious  # имена столбцов датафрейма по сомнительным сделкам

    #  """SALE/LEASE DATA FRAMES"""


    all_deals_query_df[all_deals_query_df['Include_in_Market_Share'].isin(['Y']) & all_deals_query_df['Type_of_Deal'].isin(['Sale', 'Purchase'])]
    all_deals_query_df[all_deals_query_df['Include_in_Market_Share'].isin(['Y']) & ~all_deals_query_df['Type_of_Deal'].isin(['Sale', 'Purchase'])]

