import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import flask
#test
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dfPool = pd.read_csv('app/6_ml_log.csv')
# to display first item when page loaded
currencyPairs = list(set(dfPool[dfPool.columns[0]])) #reading distict currency pairs/security
df = (dfPool[dfPool['security'] == currencyPairs[0]]) #reading first security data for initial rendering

server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets
)



indicators = []
for col in df.columns:
    if (col not in ['security', 'datetime', 'open', 'high', 'low', 'close']):
        indicators.append(col)

indicatorMap = [1 for x in indicators] #for mapping into rowsize vector for allocating height

try:
    indicatorMap.remove(1)  #for removing an item that represents candle stick
except ValueError:
    pass

Currentfig = make_subplots(
    rows=len(indicators), cols=1, shared_xaxes=True, vertical_spacing=0.02
)

Currentfig.add_trace(go.Candlestick(x=df['datetime'],
                                    open=df['open'], high=df['high'],
                                    low=df['low'], close=df['close']))

##########################################
app.layout = dhc.Div(children=[
    dcc.Graph(
        id="plot-candle",
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
    rowWidth = [0.2/len(indicators) for x in indicators]
    rowWidth.append(0.8)
    # rowWidth.append(0.6)
    # specs =  [[{"rowspan": 2}], [None], [{}], [{}], [{}]]
    fig = make_subplots(
        rows=len(indicators)+1, cols=1, shared_xaxes=True, vertical_spacing=0.1,
        row_width=rowWidth,
        # specs=specs,

    )

    fig.add_trace(go.Candlestick(x=df['datetime'],
                                 open=df['open'], high=df['high'],
                                 low=df['low'], close=df['close'], name=securityValue), row=1, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False, yaxis=dict(
        autorange=True,
        fixedrange=False
    ),
        xaxis={'type': 'category', 'categoryorder': 'category ascending'},
        # yaxis2_domain = [0, 1]
    )

    rowIndex = 2
    if (indicatorValues):    #rendering indicator plots based on dropdown 
        for i in indicatorValues:
            fig.add_trace(go.Scatter(
                x=df['datetime'], y=df[i], mode='lines', name=i), row=rowIndex, col=1)
            rowIndex += 1

    figure = Currentfig = fig

    return figure

if __name__ == '__main__':
    # test
    import os

    # debug = False if os.environ['DASH_DEBUG_MODE'] == 'False' else True

    app.run_server(
        host='0.0.0.0',
        port=8080,
        debug=False
    )
