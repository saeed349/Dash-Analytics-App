import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('App1', href='/apps/app1'),
    html.Br(),
    dcc.Link('App2', href='/apps/app2'),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        # return '404'
        return index_page

# if __name__ == '__main__':
#     app.run_server(debug=True)



if __name__=="__main__":
    # app.run_server(debug=True, port=5001)
    app.run_server(
        host='0.0.0.0',
        port=8080,
        debug=True
    )