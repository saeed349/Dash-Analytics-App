import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dfPool = pd.read_csv('6_ml_log.csv')
# to display first item when page loaded
currencyPairs = list(set(dfPool[dfPool.columns[0]]))
df = (dfPool[dfPool['security'] == currencyPairs[0]])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


######processing intitial figure nnd indicators#########

indicators = []
for col in df.columns:
    if (col not in ['security', 'datetime', 'open', 'high', 'low', 'close']):
        indicators.append(col)

Currentfig = make_subplots(
    rows=len(indicators), cols=1, shared_xaxes=True, vertical_spacing=0.02
)

Currentfig.add_trace(go.Candlestick(x=df['datetime'],
                                    open=df['open'], high=df['high'],
                                    low=df['low'], close=df['close']))

# for i in indicators:
#     fig.add_trace(go.Scatter(x=df['datetime'], y=df[i], mode='lines'))


##########################################
app.layout = dhc.Div(children=[
    dcc.Graph(
        id="plot-candle",
        # figure={
        #     'data': [go.Candlestick(x=df['datetime'],
        #                             open=df['open'], high=df['high'],
        #                             low=df['low'], close=df['close'])
        #              ]
        # },
        figure=Currentfig

    ),
    dcc.Dropdown(id='dropdown-securities',
                 options=[{'label': i, 'value': i} for i in currencyPairs], multi=False, value=currencyPairs[0]),
    dcc.Dropdown(id='dropdown-indicators', multi=True,
                 options=[{'label': i, 'value': i} for i in indicators])

])


@app.callback(
    Output('plot-candle', 'figure'),
    [Input('dropdown-securities', 'value'),
     Input('dropdown-indicators', 'value')]
)
def updatePlot(securityValue, indicatorValues):
    df = (dfPool[dfPool['security'] == securityValue])
    fig = make_subplots(
        rows=len(indicators)+1, cols=1, shared_xaxes=True, vertical_spacing=0.1,
    )

    fig.add_trace(go.Candlestick(x=df['datetime'],
                                 open=df['open'], high=df['high'],
                                 low=df['low'], close=df['close'], name=securityValue), row=1, col=1)

    rowIndex = 2
    if (indicatorValues) :
        for i in indicatorValues:
            fig.add_trace(go.Scatter(
                x=df['datetime'], y=df[i], mode='lines', name=i), row=rowIndex, col=1)
            rowIndex += 1

    figure = Currentfig = fig

    return figure

# @app.callback(
#     Output('plot-candle', 'figure'),
#     [Input('dropdown-indicators', 'value')]
# )
# def updateIndicators(value):

#     for i in indicators:
#         fig.add_trace(go.Scatter(
#             x=df['datetime'], y=df[value], mode='lines', name=value), row=rowIndex, col=1)
#         rowIndex += 1


if __name__ == '__main__':
    app.run_server(debug=True)
