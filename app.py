import dash

app = dash.Dash(name=__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'Polish cars stats'
server = app.server
