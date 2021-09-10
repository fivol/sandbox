import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import random
import pandas as pd
import re
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div('Название файла'),
                dcc.Input(id='input', placeholder='hello world', className='mt-5')
            ]
        ),

        html.Div('Hello world', id='text')
    ], className='container'
)


@app.callback(
    Output('text', 'children'),
    Input('input', 'value'),
)
def add_task(input_value):
    if input_value:
        return input_value.capitalize()
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)
