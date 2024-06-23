import dash
from dash import dcc, html, dash_table
from django_plotly_dash import DjangoDash
import pandas as pd
from .models import Transaction
import plotly.express as px

external_stylesheets = [
    '/static/css/styles.css'
]

app = DjangoDash('TransactionGraph', external_stylesheets=external_stylesheets)

transactions = Transaction.objects.all().values()
df = pd.DataFrame(transactions)


if df.empty:
    app.layout = html.Div(
        children=[
            html.Div(children='My First App with Data and a Graph'),
            html.Div(children='No data available to display.')
        ],
    )
else:
    app.layout = html.Div(
        children=[
            html.Div(children='My First App with Data and a Graph'),
            dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            dcc.Graph(figure=px.histogram(df, x='date', y='amount',
                                          histfunc='avg'))
        ],
    )
