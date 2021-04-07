import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from app import app
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df1 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data.csv'))
df2 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data_1.csv'))
df3 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data_2.csv'))

df = df1.append([df2, df3])

df_mileage = df.loc[df.condition == 'Używane', ['mileage', 'prod_year']].groupby(['prod_year'], as_index=False).mean()
df_mileage = df_mileage.rename(columns={'prod_year': 'prod_year', 'mileage': 'mileage_avg'})
fig_1 = px.bar(df_mileage, x='prod_year', y='mileage_avg', log_y=True, text='mileage_avg')
fig_1.update_traces(texttemplate='%{text:.2s}', textposition='outside', marker_color='orange',
                    hovertemplate='Rok: %{x} <br>Przebieg: %{y:.3s}')
fig_1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
                    xaxis_title="Rok produkcji",
                    yaxis_title="Średni przebieg (km)")

df_capacity = df[['eng_capacity', 'prod_year']].groupby(['prod_year'], as_index=False).mean()
df_capacity = df_capacity.rename(columns={'prod_year': 'prod_year', 'eng_capacity': 'eng_capacity_avg'})
fig_2 = px.scatter(df_capacity, x='prod_year', y='eng_capacity_avg')
fig_2.update_traces(hovertemplate='Rok: %{x} <br>Średnia pojemność: %{y:.0f} cm<sup>3</sup>', marker_color='orange')
fig_2.update_layout(
    xaxis_title="Rok produkcji",
    yaxis_title="Średnia pojemność silnika (cm<sup>3</sup>)",
)


df_country = df.country_of_origin.value_counts().reset_index()
df_country.columns = ['country', 'count']
if len(df_country) > 10:
    sum_of_others = df_country['count'].iloc[9:].sum()
    df_country = df_country.iloc[:9]
    df_country = df_country.append({'country': 'Inny', 'count': sum_of_others}, ignore_index=True)

fig_3 = go.Figure(
    data=go.Pie(labels=df_country['country'], values=df_country['count'])
)


df_gearbox = df.gearbox.value_counts().rename_axis('gearbox').reset_index(name='count')
fig_4 = go.Figure(
    data=go.Pie(labels=df_gearbox['gearbox'], values=df_gearbox['count'])
)

df_models = df[['make', 'model']]
df_models['full_model_name'] = [f'{make} {model}' for make, model in zip(df_models.make, df_models.model)]
df_models = df_models.full_model_name.value_counts()[:10].reset_index()
df_models.columns = ['car', 'count']

fig_5 = px.bar(df_models, x='car', y='count', text='count')
fig_5.update_traces(hovertemplate='%{x} <br>Ilość: %{y}', marker_color='orange')
fig_5.update_layout(
    xaxis_title="Model",
    yaxis_title="Ilość",
)

fig_6 = px.histogram(x=df.eng_power, nbins=100)
fig_6.update_traces(hovertemplate='Moc: %{x} km <br>Ilość: %{y}', marker_color='orange')
fig_6.update_layout(
    xaxis_title="Moc silnika",
    yaxis_title="Ilość",
)


df_body = df.body.value_counts().reset_index()
df_body.columns = ['body', 'count']

fig_7 = go.Figure(
    data=go.Pie(labels=df_body['body'], values=df_body['count'])
)

df_fuel = df.fuel.value_counts().reset_index()
df_fuel.columns = ['fuel', 'count']

fig_8 = px.bar(df_fuel, x='fuel', y='count', log_y=True, text='count')
fig_8.update_traces(textposition='outside',
                    hovertemplate='%{x} <br>Ilość: %{y}',
                    marker_color='orange')
fig_8.update_layout(
    xaxis_title="Paliwo",
    yaxis_title="Ilość",
)


layout = html.Div(className='p-4', children=[
    dbc.Row([
        html.H3('Inne statystyki', className="text-white mb-4")
    ], justify='center'),
    dbc.Row(children=[
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Przebieg w zależności od roku produkcji', className="card-title"),
                dcc.Graph(id='mileage_graph', figure=fig_1)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6}),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Pojemność silnika w zależności od roku produkcji', className="card-title"),
                dcc.Graph(id='capacity_graph', figure=fig_2)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6})
    ]),
    dbc.Row(className='mt-3', children=[
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Kraj pochodzenia', className="card-title"),
                dcc.Graph(id='country_of_origin_graph', figure=fig_3)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6}),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Typ skrzyni biegów', className="card-title"),
                dcc.Graph(id='gearbox-type-graph', figure=fig_4)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6})
    ]),
    dbc.Row(className='mt-3', children=[
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Najpopularniejsze modele', className="card-title"),
                dcc.Graph(id='models-graph', figure=fig_5)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6}),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Rozkład mocy silnika', className="card-title"),
                dcc.Graph(id='power-graph', figure=fig_6)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6})
    ]),
    dbc.Row(className='mt-3', children=[
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Typ nadwozia', className="card-title"),
                dcc.Graph(id='body-graph', figure=fig_7)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6}),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4('Rodzaj paliwa', className="card-title"),
                dcc.Graph(id='fuel-graph', figure=fig_8)]),
                className="card text-white bg-primary"
            )
        ], width={'size': 6})
    ])
])
