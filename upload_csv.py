import base64
import io
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import psycopg2 as pg
import sqlalchemy
import pandas as pd

dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = '3334'
port = 5432
conn = pg.connect(dbname=dbname, host=host, user=user, password=password)  # рисоединение к базе данных

url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, dbname)
con = sqlalchemy.create_engine(url, client_encoding='utf8')
meta = sqlalchemy.MetaData(bind=con, reflect=True)
# df.columns = ['ID', 'Name', 'Info']
# df.to_sql('update_test', con, if_exists='append', index=False)



app = dash.Dash()

app.scripts.config.serve_locally = True

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string + "==")

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv((io.StringIO(decoded.decode('utf-8'))), header=None)
            df.columns = ['ID', 'Name', 'Info']
            df.to_sql('update_test', con, if_exists='append', index=False)


        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel((io.BytesIO(decoded)), header=None)
            df.columns = ['ID', 'Name', 'Info']
            df.to_sql('update_test', con, if_exists='append', index=False)


    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # if df is not None:
    #     df.columns = ['ID', 'Name', 'Info']
    #     df.to_sql('update_test', con, if_exists='append', index=False)

    return html.Div(
        [
            html.H5(filename),
            dt.DataTable(rows=df.to_dict('records')),
        ]
    )


@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
               [dash.dependencies.Input('upload-data', 'contents'),
                dash.dependencies.Input('upload-data', 'filename')],
              )

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
             parse_contents(c, n) for c, n in
             zip(list_of_contents, list_of_names)]
        return children


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})



if __name__ == '__main__':
    app.run_server(debug=True)