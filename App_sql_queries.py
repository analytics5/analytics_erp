deals_query = """SELECT "Agency"::text, "SQM"::real, "Year"::text
            FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Country"='RU' AND "Include_in_Market_Share"='Y'"""
tenant_rep_query = """SELECT "Agency"::text, "SQM"::real, "Year"::text
            FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Country"='RU' AND "City"='Moscow' AND  "LLR/TR" IN ('TR','LLR/TR','LLR/ETR','ETR') AND "Include_in_Market_Share"='Y'"""

llr_query = """SELECT "Agency"::text, "SQM"::real, "Year"::text
            FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Country"='RU' AND "City"='Moscow' AND  "LLR/TR" IN ('LLR','LLR/TR','LLR/ETR') AND "Include_in_Market_Share"='Y'"""

sale_lease_query = """SELECT "Agency":: text, "SQM"::real, "Year"::text,"Type_of_deal"::text
            FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Type_of_deal" NOT LIKE 'None' AND "Country"='RU' AND "Include_in_Market_Share"='Y'"""


sale_lease_query_sale = """SELECT "Agency":: text, "SQM"::real, "Year"::text,"Type_of_deal"::text
                FROM "Market_Share"
                WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Type_of_deal" NOT LIKE 'None' AND "Type_of_deal" IN ('Sale', 'Purchase') AND "Country"='RU' AND "Include_in_Market_Share"='Y' """


sale_lease_query_lease = """SELECT "Agency":: text, "SQM"::real, "Year"::text,"Type_of_deal"::text
                FROM "Market_Share"
                WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices' AND "Type_of_deal" NOT LIKE 'None' AND "Country"='RU' AND "Include_in_Market_Share"='Y' AND "Type_of_deal" NOT IN ('Sale', 'Purchase')"""


table_query = """SELECT "Agency":: text, "Country":: text, "City":: text, "Property_Name", "Class", "SQM"::real, "Company"::text, "Type_of_Consultancy","Year"::text, "Quarter"::text
                      FROM "Market_Share"
            WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'"""

table_query_new = """SELECT "Agency":: text, "Country":: text, "City":: text, "Property_Name", "Class", "SQM"::real, "Company"::text, "Business_Sector"::text,"Type_of_deal", "Type_of_Consultancy", "LLR/TR"::text, "Year"::text, "Quarter"::text

                      FROM "Market_Share"
                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'"""

table_query_new_all = """SELECT "Include_in_Market_Share","Agency","Country", "City",  "Property_Name", "Address", 
                                "Submarket_Large", "Owner", "Date_of_acquiring","Class", "Class_Colliers", 
                                "Floor", "SQM"::real , "Deal_Size", "Company", "Business_Sector", "Sublease_Agent",
                                 "Type_of_deal", "Type_of_Consultancy", "LLR/TR", "LLR_Only", "E_TR_Only", "LLR/E_TR",
                                 "Month",  "Year", "Quarter"

                      FROM "Market_Share"
                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'"""



suspicious_deals = """SELECT "Agency":: text, "Country":: text, "City":: text, "Property_Name", "Class", "SQM"::real, "Company"::text, "Type_of_Consultancy","Year"::text, "Quarter"::text
                      FROM "Market_Share"

                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'
                      AND "SQM"::real IN (SELECT "SQM"::real
                      FROM "Market_Share"
                      WHERE "SQM" NOT LIKE '%w/s' AND "SQM" NOT LIKE '%offices'

                      GROUP BY "Year", "Agency", "SQM"
                      HAVING count(*)>1)
                      ORDER BY "SQM" DESC """



create_table = """
CREATE TABLE public."Market_Share"
(
    "Include_in_Market_Share" text,
    "Agency" text,
    "Country" text,
    "City" text,
    "Property_Name" text,
    "Address" text,
    "Unk" text,
    "Owner" text,
    "Qof" text,
    "Class" text,
    "Class_colliers" text,
    "Floor" text,
    "SQM" character varying,
    "Deal_size" character varying,
    "Company" character varying,
    "Sector" character varying,
    "Sublease_company" text,
    "Type_of_deal" text,
    "Type_of_Consultancy" text,
    "LLR/TR" text,
    "type_1" text,
    "type_2" text,
    "type_3" text,
    "Month" text,
    "Quarter" integer,
    "Year" integer
    
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public."Market_Share"
    OWNER to postgres;
"""