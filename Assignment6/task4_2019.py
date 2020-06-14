# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:07:13 2019

@author: khatami
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
from textwrap import dedent as d
import plotly.graph_objs as go
from plotly import tools
from dash.dependencies import Input, Output
import json


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


path = 'res\\Data_Cortex_Nuclear.xls'

# read in the data
df = pd.read_excel(path)

# select c-SC-s and t-SC-s samples
data = pd.concat([df[df['class'] == 'c-SC-s'], df[df['class'] == 't-SC-s']])

# select the 5 features that explain the most variance
selected_data = data[['pPKCG_N', 'pP70S6_N', 'pS6_N', 'pGSK3B_N', 'ARC_N', 'class']]
selected_data = selected_data.reset_index(drop=True)  # reset index for concatenating

data_c = selected_data[selected_data['class'] == 'c-SC-s']
data_t = selected_data[selected_data['class'] == 't-SC-s']

attributes = ['pPKCG_N', 'pP70S6_N', 'pS6_N', 'pGSK3B_N', 'ARC_N']

fig = tools.make_subplots(rows=5, cols=5)

show_legend = False

# Add plot to the grid
for i in range(len(attributes)):
    for j in range(len(attributes)):
        # Place histograms on the diagonal
        if i == j:
            # Only add the legend once (for the last plot)
            if i == len(attributes) - 1 and j == len(attributes) - 1:
                show_legend = True
            fig.append_trace(go.Histogram(
                x=data_c[attributes[i]],
                opacity=0.5,
                text='c-SC-s',
                name='c-SC-s',
                marker=dict(
                    color='red'
                ),
                showlegend=show_legend,
            ), i + 1, j + 1)
            fig.append_trace(go.Histogram(
                x=data_t[attributes[i]],
                opacity=0.5,
                text='t-SC-s',
                name='t-SC-s',
                marker=dict(
                    color='blue'
                ),
                showlegend=show_legend,

            ), i + 1, j + 1)
        else:
            # Add the scatterplots
            fig.append_trace(go.Scatter(
                x=data_c[attributes[i]],
                y=data_c[attributes[j]],
                mode='markers',
                text=['c-SC-s'] * data_c.shape[0],
                opacity=0.5,
                marker=dict(
                    color='red',
                ),
                name='c-SC-s',
                showlegend=False,
            ), i + 1, j + 1)
            fig.append_trace(go.Scatter(
                x=data_t[attributes[i]],
                y=data_t[attributes[j]],
                mode='markers',
                text=['t-SC-s'] * data_t.shape[0],
                opacity=0.5,
                marker=dict(
                    color='blue'
                ),
                name='t-SC-s',
                showlegend=False
            ), i + 1, j + 1)

# Define the layout
fig.layout.update(go.Layout(
    barmode='overlay',
    clickmode='event+select',
    # add x axis titles
    annotations=[
        dict(
            x=0.06,
            y=1.05,
            showarrow=False,
            text=attributes[0],
            xref='paper',
            yref='paper'
        ),
        dict(
            x=0.26,
            y=1.05,
            showarrow=False,
            text=attributes[1],
            xref='paper',
            yref='paper'
        ),
        dict(
            x=0.5,
            y=1.05,
            showarrow=False,
            text=attributes[2],
            xref='paper',
            yref='paper',
        ),
        dict(
            x=0.75,
            y=1.05,
            showarrow=False,
            text=attributes[3],
            xref='paper',
            yref='paper'
        ),
        dict(
            x=0.93,
            y=1.05,
            showarrow=False,
            text=attributes[4],
            xref='paper',
            yref='paper'
        )],

    # Add y axis titles
    yaxis1=dict(
        title=attributes[0],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis6=dict(
        title=attributes[1],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis11=dict(
        title=attributes[2],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis16=dict(
        title=attributes[3],
        titlefont=dict(
            size=12,
        )
    ),
    yaxis21=dict(
        title=attributes[4],
        titlefont=dict(
            size=12,
        )
    )
))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#115511',
    'text': '#7FDBFF'
}
app.layout = html.Div(children=[
    html.H1(
        children='Exercise 6',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Introduction to Dash - Scatterplot Matrix',
             style={
                 'textAlign': 'center',
                 'color': 'green'
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