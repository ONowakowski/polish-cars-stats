import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from app import server

from apps import dashboard, model_stats


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(children=[
        dbc.NavItem(dbc.NavLink('Główne statystyki', href='/apps/dashboard')),
        dbc.NavItem(dbc.NavLink('Statystyki szczegółowe', href='#')),
        dbc.NavItem(dbc.NavLink('Sprawdź dla modelu', href='/apps/model_stats'))
    ],
        color="primary",
        dark=True,
        expand='xs'
    ),
    #dcc.Link('dsdas', href='/apps/dashboard'),
    #dcc.Link('dsassss', href='/apps/model_stats'),
    html.Div(id='content', children=[])
])


@app.callback(
    Output(component_id='content', component_property='children'),
    [Input(component_id='url', component_property='pathname')]
    # Output(component_id='testt', component_property='children'),
)
def display_page(pathname):
    if (pathname == '/apps/dashboard') | (pathname == '/'):
        return dashboard.layout
    elif pathname == '/apps/model_stats':
        return model_stats.layout
    else:
        return "404 Page Error, choose a correct site!"


if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=False)
