import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
import pathlib


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df1 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data.csv'))
df2 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data_1.csv'))
df3 = pd.read_csv(DATA_PATH.joinpath('preprocessed_otomoto_data_2.csv'))

df = df1.append([df2, df3])

fig_1 = px.histogram(df, x=df.price)
fig_1.update_layout(
    xaxis_title="Cena (PLN)",
    yaxis_title="Ilość",
)
fig_1.update_traces(marker_color='orange',
                    hovertemplate='Cena: %{x} <br>Ilość: %{y}')

card_histogram_price_graph = dbc.Card([
    dbc.CardBody([
        html.H4("Rozkład cen samochodów", className="card-title"),
        dcc.Graph(figure=fig_1)
    ])
], className="card text-white bg-primary")

fig_2 = px.histogram(df, x='prod_year')
fig_2.update_layout(
    xaxis_title="Rok produkcji",
    yaxis_title="Ilość",
)
fig_2.update_traces(marker_color='orange',
                    hovertemplate='Rok produkcji: %{x} <br>Ilość: %{y}')

card_histogram_prod_year_graph = dbc.Card([
    dbc.CardBody([
        html.H4("Rozkład lat produkcji samochodów", className="card-title"),
        dcc.Graph(figure=fig_2)
    ])
], className="card text-white bg-primary")

fig_3 = px.histogram(df, x='make')

max_price = df.price.max()
min_price = df.price.min()

marks_step = (max_price - min_price) / 9
marks_values = [int(val) for val in np.arange(0, max_price + marks_step, step=marks_step)]

labels = [(i * 20000 if i <= 5 else 0) for i in range(0, 10)]
for i in range(1, 5):
    labels[i + 5] = int((max_price - labels[5]) / 4 * i) + labels[5]

card_make_price_graph = dbc.Card([
    dbc.CardBody([
        html.H4(id='card_make_price_title', children=f'Samochody w cenie od {min_price} do {max_price} zł'),
        dcc.RadioItems(id='card_make_price_radioitems', inputStyle={"margin-right": "5px", "margin-left": "3px"},
                       options=[
                           {'label': 'Wszystkie', 'value': 'ALL'},
                           {'label': 'Używane', 'value': 'USED'},
                           {'label': 'Nowe', 'value': 'NEW'}],
                       value='ALL'
                       ),
        dcc.Dropdown(id='card_make_price_dropdown', className='text-black',
                     options=[dict(label=make, value=make) for make in df['make'].unique()],
                     value=df['make'].unique(),
                     multi=True
                     ),
        html.H5(id='card_make_price_sum_of_cars', children=f'Łącznie ofert: {df["offer_id"].count()}'),
        dcc.Graph(id='graph_make_price_range', figure=fig_3),
        html.Br(),
        dcc.RangeSlider(
            id='price_range_slider',
            min=min_price.astype(int),
            max=max_price.astype(int),
            marks={marks_values[i]: {'label': str(labels[i]), 'style': {'color': 'white'}} for i in range(0, 10)},
            value=[min_price, max_price]
        )
    ])
], className="card text-white bg-primary")

layout = html.Div(className='p-4',  # bg-secondary
                  children=[
                      dbc.Row([
                          html.H3('Oferty sprzedaży samochodów w Polsce', className="text-white mb-4")
                      ], justify='center'),
                      dbc.Row([
                          dbc.Col([
                              dbc.Card([f'Ilość analizowanych ofert: {df.shape[0]}'],
                                       body=True, className="card text-white bg-primary"
                                       )
                          ]),
                          dbc.Col([
                              dbc.Card(['Najdroższa oferta: {:10.2f} zł'.format(df.price.max())],
                                       body=True, className="card text-white bg-primary")
                          ]),
                          dbc.Col([
                              dbc.Card([f"Samochody używane: {df.condition.value_counts().to_dict()['Używane']}"],
                                       body=True, className="card text-white bg-primary")
                          ]),
                          dbc.Col([
                              dbc.Card([f"Samochody nowe: {df.condition.value_counts().to_dict()['Nowe']}"],
                                       body=True, className="card text-white bg-primary")
                          ])
                      ]),
                      dbc.Row(className='mt-3', children=[
                          dbc.Col([
                              dbc.Card([f'Średnia cena samochodu: ' + '{:10.2f}'.format(df.price.mean()) + ' zł'],
                                       body=True, className="card text-white bg-primary"
                                       )
                          ]),
                          dbc.Col([
                              dbc.Card(['Mediana cen: {:10.2f} zł'.format(df.price.median())],
                                       body=True, className="card text-white bg-primary")
                          ]),
                          dbc.Col([
                              dbc.Card(["Średni rok produkcji: {:10.0f}".format(df.prod_year.mean())],
                                       body=True, className="card text-white bg-primary")
                          ]),
                          dbc.Col([
                              dbc.Card(["Średni przebieg używanych samochodów: {:10.0f} km".format(
                                  df.loc[df.condition == 'Używane', 'mileage'].mean())],
                                  body=True, className="card text-white bg-primary")
                          ])
                      ]),
                      dbc.Row(className='mt-3', children=[
                          dbc.Col([
                              card_histogram_price_graph
                          ],
                              width={'size': 6}
                          ),
                          dbc.Col([
                              card_histogram_prod_year_graph
                          ],
                              width={'size': 6}
                          )
                      ]),
                      dbc.Row(className='mt-3', children=[
                          dbc.Col([
                              card_make_price_graph
                          ])
                      ])
                  ])


@app.callback(
    Output(component_id='graph_make_price_range', component_property='figure'),
    Output(component_id='card_make_price_title', component_property='children'),
    Output(component_id='card_make_price_sum_of_cars', component_property='children'),
    Input(component_id='price_range_slider', component_property='value'),
    Input(component_id='card_make_price_radioitems', component_property='value'),
    Input(component_id='card_make_price_dropdown', component_property='value')
)
def update_output_graph(input_range_value, input_radio_value, input_makes_value):
    min_val = input_range_value[0]
    max_val = input_range_value[1]
    price_min = 0
    price_max = 0

    half_input = df.price.max() * 5 / 9
    half_range = half_input - df.price.min()

    second_range = df.price.max() - half_input
    label_second_range = df.price.max() - labels[5]

    if min_val <= half_input:
        price_min = (min_val - df.price.min()) / half_input * (labels[5])
    else:
        price_min = (min_val - half_input) / second_range * label_second_range + labels[5]

    if max_val <= half_input:
        price_max = (max_val - df.price.min()) / half_range * (labels[5])
    else:
        price_max = (max_val - half_input) / second_range * label_second_range + labels[5]

    if input_radio_value == 'USED':
        dff = df.loc[(df.price >= price_min) & (df.price <= price_max) & (df.condition == 'Używane')]
    elif input_radio_value == 'NEW':
        dff = df.loc[(df.price >= price_min) & (df.price <= price_max) & (df.condition == 'Nowe')]
    else:
        dff = df.loc[(df.price >= price_min) & (df.price <= price_max)]

    dff = dff[dff['make'].isin(input_makes_value)]

    fig = px.histogram(dff, x='make')
    fig.update_layout(
        xaxis_title="Marka",
        yaxis_title="Ilość",
        xaxis={'categoryorder': 'total descending'}
    )
    fig.update_traces(marker_color='orange',
                      hovertemplate='Marka: %{x} <br>Ilość: %{y}')

    title = 'Samochody w cenie od {:10.0f} do {:10.0f} zł'.format(price_min, price_max)
    sum_of_cars_title = f'Łącznie ofert: {dff["offer_id"].count()}'

    return fig, title, sum_of_cars_title
