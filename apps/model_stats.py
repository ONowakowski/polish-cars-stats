import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from apps import dashboard as dsh
from app import app
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df1 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data.csv'))
df2 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data_1.csv'))
df = df1.append(df2)

layout = html.Div(className='p-4',  # bg-secondary
                  children=[
                      dbc.Row([
                          html.H3('Statystyki dla wybranego samochodu', className="text-white mb-4")
                      ], justify='center'),
                      dbc.Row([
                          dbc.Col(width=4, children=[
                              html.H6('Marka:'),
                              dcc.Dropdown(id='make-dropdown',
                                           options=[dict(label=make, value=make) for make in df['make'].unique()]
                                           ),
                              html.H6('Model:'),
                              dcc.Dropdown(id='model-dropdown',
                                           options=[]),
                              html.H6('Wersja:'),
                              dcc.Dropdown(id='version-dropdown',
                                           options=[]),
                              html.H6('Rok produkcji:'),
                              dcc.Dropdown(id='year-dropdown',
                                           options=[])
                          ]),
                          dbc.Col([
                              dbc.Card([
                                  html.H5(id='output-name-of-car'),
                                  dbc.Progress(value=25, color="success", className="mb-3"),
                                  dbc.Progress(value=50, color="warning", className="mb-3"),
                                  dbc.Progress(value=75, color="danger", className="mb-3"),
                                  dbc.Progress(value=100, color="info")],
                                  body=True, className="card text-white bg-primary")
                          ])
                      ])
                  ])


@app.callback(
    Output(component_id='model-dropdown', component_property='options'),
    Output(component_id='model-dropdown', component_property='disabled'),
    Output(component_id='model-dropdown', component_property='value'),
    Input(component_id='make-dropdown', component_property='value')
)
def update_model_dropdown(chosen_make):
    if chosen_make is None:
        return [], True, None

    models = df.loc[df['make'] == chosen_make, 'model'].unique()
    models_options = [dict(label=model, value=model) for model in models]

    return models_options, False, None


@app.callback(
    Output(component_id='version-dropdown', component_property='options'),
    Output(component_id='version-dropdown', component_property='disabled'),
    Output(component_id='version-dropdown', component_property='value'),
    Input(component_id='make-dropdown', component_property='value'),
    Input(component_id='model-dropdown', component_property='value')
)
def update_version_dropdown(chosen_make, chosen_model):
    if chosen_model is None:
        return [], True, None

    versions = df.loc[(df['make'] == chosen_make) &
                      (df['model'] == chosen_model), 'version'].unique()
    versions_options = [dict(label=version, value=version) for version in versions]

    return versions_options, False, None


@app.callback(
    Output(component_id='year-dropdown', component_property='options'),
    Output(component_id='year-dropdown', component_property='disabled'),
    Output(component_id='year-dropdown', component_property='value'),
    Input(component_id='make-dropdown', component_property='value'),
    Input(component_id='model-dropdown', component_property='value'),
    Input(component_id='version-dropdown', component_property='value')
)
def update_year_dropdown(chosen_make, chosen_model, chosen_version):
    if chosen_version is None:
        return [], True, None

    years = df.loc[(df['make'] == chosen_make) &
                   (df['model'] == chosen_model) &
                   (df['version'] == chosen_version), 'prod_year'].unique()
    years_options = [dict(label=year, value=year) for year in years]

    return years_options, False, None


@app.callback(
    Output(component_id='output-name-of-car', component_property='children'),
    Input(component_id='make-dropdown', component_property='value'),
    Input(component_id='model-dropdown', component_property='value'),
    Input(component_id='version-dropdown', component_property='value'),
    Input(component_id='year-dropdown', component_property='value')
)
def update_prices(make, model, version, year):
    if make is None:
        return ''

    if model is None:
        return make

    if version is None:
        return f'{make} {model}'

    if year is None:
        return f'{make} {model} {version}'

    return f'{make} {model} {version} r. {year}'
