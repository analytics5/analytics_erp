import psycopg2 as pg

dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = '3334'

conn = pg.connect(dbname=dbname, host=host, user=user, password=password)   #рисоединение к базе данных
query1 = """SELECT "Property_Name", "Class"
                     FROM "Market_Share"
                     WHERE "Agency"= 'Colliers' ;"""

query2 = """CREATE TABLE public."Market_Share"
(   "Include_in_Market_Share" text,
    "Agency" text,
    "Country" text,
    "City" text,
    "Property_Name" text,
    "Address" text,
    "Submarket_Large" text,
    "Owner" text,
    "Date_of_acquiring" text,
    "Class" text,
    "Class_Colliers" text,
    "Floor" text,
    "SQM" character varying,
    "Deal_Size" text,
    "Company" text,
    "Business_Sector" text,
    "Sublease_Agent" text,
    "Type_of_deal" text,
    "Type_of_Consultancy" text,
    "LLR/TR" text,
    "LLR_Only" text,
    "(E)TR_Only" text,
    "LLR/(E)TR" text,
    "Month" text,
    "Year" character varying(4),
    "Quarter" integer
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public."Market_Share"
    OWNER to postgres;"""
with conn:
    cur = conn.cursor()
    cur.execute(query2)  # выполнение SQL запроса


