import numpy as np
import pandas as pd
import plotly.express as px
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
df3 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data_2.csv'))

df = df1.append([df2, df3])

layout = html.Div(className='p-4',  # bg-secondary
                  children=[
                      dbc.Row([
                          html.H3('Statystyki dla wybranego samochodu', className="text-white mb-4")
                      ], justify='center'),
                      dbc.Row([
                          dbc.Col(width=4, children=[
                              html.H6('Marka:'),
                              dcc.Dropdown(id='make-dropdown',
                                           options=[dict(label=make, value=make) for make in df['make'].unique()],
                                           className='mb-3'),
                              html.H6('Model:'),
                              dcc.Dropdown(id='model-dropdown',
                                           options=[],
                                           className='mb-3'),
                              html.H6('Wersja:'),
                              dcc.Dropdown(id='version-dropdown',
                                           options=[],
                                           className='mb-3'),
                              html.H6('Rok produkcji:'),
                              dcc.Dropdown(id='year-dropdown',
                                           options=[],
                                           className='mb-3'),
                              dcc.RadioItems(id='condition-radioitems',
                                             inputStyle={"margin-right": "5px", "margin-left": "3px"},
                                             options=[
                                                 {'label': 'Wszystkie', 'value': 'ALL'},
                                                 {'label': 'Używane', 'value': 'USED'},
                                                 {'label': 'Nowe', 'value': 'NEW'}],
                                             value='ALL'
                                             )
                          ]),
                          dbc.Col(width=4, children=[
                              dcc.Graph(id='price-histogram-for-model')
                          ]),
                          dbc.Col([
                              dbc.Card([
                                  html.H5(id='output-name-of-car', children=' '),
                                  html.H6(id='cars-quantity', children=' '),
                                  dbc.Progress(id='1st-quantile', children='', value=25, color="success",
                                               className="mb-3"),
                                  dbc.Progress(id='2nd-quantile', children='', value=50, color="info",
                                               className="mb-3"),
                                  dbc.Progress(id='3rd-quantile', children='', value=75, color="warning",
                                               className="mb-3"),
                                  dbc.Progress(id='4th-quantile', children='', value=100, color="danger",
                                               className="mb-3")],
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
    Output(component_id='1st-quantile', component_property='children'),
    Output(component_id='2nd-quantile', component_property='children'),
    Output(component_id='3rd-quantile', component_property='children'),
    Output(component_id='4th-quantile', component_property='children'),
    Output(component_id='cars-quantity', component_property='children'),
    Output(component_id='price-histogram-for-model', component_property='figure'),
    Input(component_id='make-dropdown', component_property='value'),
    Input(component_id='model-dropdown', component_property='value'),
    Input(component_id='version-dropdown', component_property='value'),
    Input(component_id='year-dropdown', component_property='value'),
    Input(component_id='condition-radioitems', component_property='value')

)
def update_prices(make, model, version, year, condition):
    fig = px.histogram()

    if make is None:
        dfg = df
        output_name = 'Wszystkie samochody'

    elif model is None:
        dfg = df.loc[df['make'] == make]
        output_name = make

    elif version is None:
        dfg = df.loc[(df['make'] == make) & (df['model'] == model)]
        output_name = f'{make} {model}'

    elif year is None:
        dfg = df.loc[(df['make'] == make) & (df['model'] == model) & (df['version'] == version)]
        output_name = f'{make} {model} {version}'

    else:
        dfg = df.loc[(df['make'] == make) & (df['model'] == model) &
                     (df['version'] == version) & (df['prod_year'] == year)]

        output_name = f'{make} {model} {version} r. {year}'

    if condition == 'USED':
        dfg = dfg.loc[(dfg.condition == 'Używane')]
        if dfg.empty:
            return output_name, '', '', '', '', 'brak używanych w bazie', fig
    elif condition == 'NEW':
        dfg = dfg.loc[(dfg.condition == 'Nowe')]
        if dfg.empty:
            return output_name, '', '', '', '', 'brak nowych w bazie', fig

    q1 = f' max {np.quantile(dfg.price, 0.25)} zł'
    q2 = f' max {np.quantile(dfg.price, 0.5)} zł'
    q3 = f' max {np.quantile(dfg.price, 0.75)} zł'
    q4 = f' max {np.quantile(dfg.price, 1)} zł'
    quantity = f'Na podstawie {len(dfg)} szt.'
    fig = px.histogram(dfg, x='price')

    return output_name, q1, q2, q3, q4, quantity, fig
