import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.DataFrame(selectedPoints)


app.layout = html.Div([
    dcc.Graph(
        id='SPloM-selectedPoints',
        figure={
            'data': [
                go.Splom(dimensions=[dict(label=df.columns[0],
                                 values=df.iloc[:, 0]),
                            dict(label=df.columns[1],
                                 values=df.iloc[:, 1]),
                            dict(label=df.columns[2],
                                 values=df.iloc[:, 2]),
                            dict(label=df.columns[3],
                                 values=df.iloc[:, 3])],
                text=None,
                marker=dict(color='rgb(255,0,0)',
                            size=7,
                            showscale=False,
                            line=dict(width=0.5,
                                      color='rgb(230,230,230)')),
                hoverinfo= 'skip')
            ],
            'layout': [
            go.Layout(title='Selected Points',
                dragmode=None,
                width=600,
                height=600,
                autosize=True,
                hovermode=None,
                plot_bgcolor='rgba(240,240,240, 0.95)',
                xaxis1=dict(axis),
                xaxis2=dict(axis),
                xaxis3=dict(axis),
                xaxis4=dict(axis),
                yaxis1=dict(axis),
                yaxis2=dict(axis),
                yaxis3=dict(axis),
                yaxis4=dict(axis)
                )
            ]
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)