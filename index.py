import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from app import server

from apps import dashboard, model_stats, more_stats

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(children=[
        dbc.NavItem(dbc.NavLink('Główne statystyki', href='/apps/dashboard')),
        dbc.NavItem(dbc.NavLink('Statystyki szczegółowe', href='/apps/more_stats')),
        dbc.NavItem(dbc.NavLink('Sprawdź dla modelu', href='/apps/model_stats'))
    ],
        color="primary",
        dark=True,
        expand='xs'
    ),
    html.Div(id='content', children=[]),
    html.Footer(id='footer', children=[
        html.P(style={'text-align': 'center'},
               children=["Autor: Oskar Nowakowski, E-mail: oskar.r.nowakowski@gmail.com, Kod źródłowy: ",
                         html.A(href="https://github.com/ONowakowski/polish-cars-stats",
                                children="GitHub", target='_blank'),
                         html.Br(),
                         "Dane zostały zebrane z portalu otomoto.pl (marzec/kwiecień 2021) i służą jedynie do statystyk."
                         ]),

    ])
])


@app.callback(
    Output(component_id='content', component_property='children'),
    [Input(component_id='url', component_property='pathname')]
)
def display_page(pathname):
    if (pathname == '/apps/dashboard') | (pathname == '/'):
        return dashboard.layout
    elif pathname == '/apps/model_stats':
        return model_stats.layout
    elif pathname == '/apps/more_stats':
        return more_stats.layout
    else:
        return "404 Page Error, choose a correct site!"


if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=False)
