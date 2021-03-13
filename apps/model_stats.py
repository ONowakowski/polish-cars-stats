import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from apps import dashboard as dsh
from app import app


layout = html.Div([
    html.H4(id='header',children='Statystyki dla wybranego modelu')
])

