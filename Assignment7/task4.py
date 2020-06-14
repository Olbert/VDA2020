import os
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html

from plotly import tools


class DIR(object):
    __slots__ = ()
    CHECKOUT = os.path.dirname(os.path.realpath('__file__'))
    RES = os.path.join(CHECKOUT, 'res')
    OUT = os.path.join(CHECKOUT, 'out')


DIR = DIR()
input_file = os.path.join(DIR.RES, 'Data_Cortex_Nuclear.xls')

# columns=['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'target']
# fig = px.scatter_matrix(df,
#                         dimensions=["pPKCG_N", "pP70S6_N", "pS6_N", "pGSK3B_N", "ARC_N"],
#                         color="class",
#                         title="Scatter matrix of Data_Cortex_Nuclear")
# fig.show()


# read input file
columns = ['pPKCG_N', 'pP70S6_N', 'pS6_N', 'pGSK3B_N', 'ARC_N','class']
df = pd.read_excel(input_file, index_col=0)
# filter columns
df = df[columns]
df = df[(df['class'] == 't-CS-s') | (df['class'] == 'c-CS-s')]#.drop(columns='class')

fig = tools.make_subplots(rows=5, cols=5)

# Notes:
# c-CS-s = green
# t-CS-s = red



for i in range(len(columns)-1):
    for k in range(len(columns)-1):
        # Non diagonal
        if i != k:
            # Add the scatterplots
            fig.append_trace(go.Scatter(
                x=df[df['class'] == 'c-CS-s'][columns[i]],
                y=df[df['class'] == 'c-CS-s'][columns[k]],
                mode='markers',
                text=['c-CS-s'] * df[df['class'] == 'c-CS-s'].shape[0],
                marker=dict(
                    color='green',
                ),
                name='c-CS-s',
                opacity = 0.7,
            ), i + 1, k + 1)
            fig.append_trace(go.Scatter(
                x=df[df['class'] == 't-CS-s'][columns[i]],
                y=df[df['class'] == 't-CS-s'][columns[k]],
                mode='markers',
                text=['t-CS-s'] * df[df['class'] == 't-CS-s'].shape[0],
                marker=dict(
                    color='blue'
                ),
                name='t-CS-s',
                opacity=0.7,
            ), i + 1, k + 1)
        else:
                fig.append_trace(go.Histogram(
                    x=df[df['class'] == 'c-CS-s'][columns[i]],
                    text='c-CS-s',
                    name='c-CS-s',
                    marker=dict(
                        color='green'
                    ),
                    opacity=0.7,
                ), i + 1, k + 1)
                fig.append_trace(go.Histogram(
                    x=df[df['class'] == 't-CS-s'][columns[i]],
                    text='t-CS-s',
                    name='t-CS-s',
                    marker=dict(
                        color='blue'
                    ),
                    opacity=0.7,
                ), i + 1, k + 1)




fig.layout.update(go.Layout(
    barmode='overlay',
    clickmode='event+select',
    # x axis
    annotations=[
        dict(
            x=0.1,
            y=1.03,
            text=columns[0],
            xref='paper',
            yref='paper'
        ),
        dict(
            x=0.3,
            y=1.03,
            text=columns[1],
            xref='paper',
            yref='paper'
        ),
        dict(
            x=0.5,
            y=1.03,
            text=columns[2],
            xref='paper',
            yref='paper',
        ),
        dict(
            x=0.7,
            y=1.03,
            text=columns[3],
            xref='paper',
            yref='paper'
        ),
        dict(
            x=0.9,
            y=1.03,
            text=columns[4],
            xref='paper',
            yref='paper'
        )],

    # y axis
    yaxis1=dict(
        title=columns[0],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis6=dict(
        title=columns[1],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis11=dict(
        title=columns[2],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis16=dict(
        title=columns[3],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis21=dict(
        title=columns[4],
        titlefont=dict(
            size=12,
        )
    )
))

# Layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#115511',
    'text': '#7FDBFF'
}
app.layout = html.Div(children=[
    html.H1(
        children='Assignment 6. Task 4',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Scatterplot Matrix of Data_Cortex_Nuclear.xls',
             style={
                 'textAlign': 'center'
             }
             ),

    dcc.Graph(
        id='example-graph',
        style={
            'height': 1000
        },
        figure=fig
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)