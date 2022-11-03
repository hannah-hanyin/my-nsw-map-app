# from urllib.request import urlopen
# import json
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# with urlopen('https://raw.githubusercontent.com/stephenmuss/suburb-boundaries-geojson/master/nsw.json') as response:
#     counties = json.load(response)
#
# print(counties[0])
from typing import Dict, Callable, Optional, Any

import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('../data/aggregated_data_census_rental.csv').set_index('Label')

# Option = Dict[str, str]

# def suburb_to_option(suburb: str) -> Option:
#     return {'label': suburb, 'value': suburb}

# options = [{'label': 'Suburbs', 'value': 'Index', 'disabled': True}] \
#           + list(map(suburb_to_option, dff.index.values))

# suburb_to_option: Callable[[str], Option] = lambda suburb: {'label': suburb, 'value': suburb}

options = [{'label': 'Suburbs', 'value': 'Index', 'disabled': True}] \
          + list(map(lambda suburb: {'label': suburb, 'value': suburb}, df.index.values))


app.layout = html.Div([
    html.Div([
        html.Label(['test1']),
        dcc.Dropdown(
            id='suburb_choice',
            options=options,
            value='Abbotsbury',
            multi=False,
            clearable=False,
            style={'width': '50%'}
        ),
    ]),
    html.Div([
        dcc.Graph(id = 'the_population_graph'),
        dbc.Row([
            dbc.Col(dbc.Card(
                id='rental_card',
                children=[
                    dbc.CardHeader(id='rental_card_title', className="card-title"),
                    dbc.CardBody(
                        [
                            html.H4("Weekly median advertised rent"),
                            html.Br(),
                            html.H2([
                                html.Span("$ "),
                                html.Span(id="rental_card_subtitle")
                            ], className="card-subtitle"),
                            html.Br(),
                        ]
                    )
                ],
                color='info',
                inverse=True,
                # style={"width": "20rem"},
                )
            ),
            dbc.Col(dbc.Card(
                id='income_card',
                children=[
                    dbc.CardHeader(id='income_card_title', className="card-title"),
                    dbc.CardBody(
                        [
                            html.H4("Household weekly income"),
                            html.Br(),
                            html.H2([
                                html.Span("$ "),
                                html.Span(id="income_card_subtitle")
                            ],className="card-subtitle"),
                            html.Br(),
                        ]
                    )
                ],
                color='danger',
                inverse=True,
                # style={"width": "20rem"},
            )
        )

        ], className="mt-3"),
        dcc.Graph(id='educational_graph'),
        dcc.Graph(id='labor_graph')

    ])
], className="p-4")

# --------------------------------------------------------
#connect plotly and dash, create population census graph
@app.callback(
    Output(component_id='the_population_graph', component_property='figure'),
    [Input(component_id='suburb_choice', component_property='value')]
)

def update_graph(suburb_choice):
    dff = df[['Males - Total (no.)', 'Females - Total (no.)', 'Persons - Total (no.)']]
    dff = dff.rename(
        columns={'Males - Total (no.)': 'Male', 'Females - Total (no.)': 'Female', 'Persons - Total (no.)': 'Total'})
    parents = ['Total', 'Total', '']

    fig = go.Figure(go.Sunburst(
        labels=dff.columns,
        parents=parents,
        values=dff.loc[suburb_choice],
        branchvalues='total',
        name=suburb_choice,
        hovertemplate='<b>%{label} </b> <br> Population Percentage: %{percentRoot:.3%}',
        textinfo='label + value '
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                      # Add annotations in the center of the donut pies.
                      # annotations = [dict(text='population', x=0.82, y=0.5, font_size=20, showarrow=False)],
                      # title_text = "Census based on 2018"
                      )

    return (fig)


#connect plotly and dash, create Weekly median advertised rental cost card
@app.callback(
    Output(component_id='rental_card_title', component_property='children'),
    [Input(component_id='suburb_choice', component_property='value')]
)
def get_rental_card_title(suburb_choice):
    return suburb_choice


@app.callback(
    Output(component_id='rental_card_subtitle', component_property='children'),
    [Input(component_id='suburb_choice', component_property='value')]
)
def get_rental_card_subtitle(suburb_choice):
    df_rental = df[['Weekly median advertised rent']]
    return df_rental.loc[suburb_choice]


#connect with dash, create weekly household income card
@app.callback(
    Output(component_id='income_card_title', component_property='children'),
    [Input(component_id='suburb_choice', component_property='value')]
)
def get_income_card_title(suburb_choice):
    return suburb_choice


@app.callback(
    Output(component_id='income_card_subtitle', component_property='children'),
    [Input(component_id='suburb_choice', component_property='value')]
)
def get_income_card_subtitle(suburb_choice):
    df_income = df[['Median Household Weekly Income']]
    return df_income.loc[suburb_choice]


#connect plotly and dash, create education level graph

@app.callback(
    Output(component_id='educational_graph', component_property='figure'),
    [Input(component_id='suburb_choice', component_property='value')]
)

def update_graph(suburb_choice):
    dff = df[['Postgraduate Degree (%)','Graduate Diploma/Graduate Certificate (%)','Bachelor Degree (%)',\
              'Advanced Diploma/Diploma (%)','Certificate (%)']]

    dff.insert(len(dff.columns),'Others',dff.apply(lambda x: 100-x.sum(), axis=1))
    dff.insert(len(dff.columns),'Total population aged 15 years', df['Total population aged 15 years and over (no.)'])
    dfd = dff.copy()
    for col in ['Postgraduate Degree (%)', 'Graduate Diploma/Graduate Certificate (%)', 'Bachelor Degree (%)', \
                'Advanced Diploma/Diploma (%)', 'Certificate (%)','Others']:
        dfd.loc[:,col] = (dfd.loc[:,col] / 100) * dfd.loc[:,'Total population aged 15 years']

    dfd = dfd.rename(columns={'Postgraduate Degree (%)': 'Postgraduate Degree level',
            'Graduate Diploma/Graduate Certificate (%)': 'Graduate Diploma/Certificate level',
            'Bachelor Degree (%)': 'Bachelor Degree', 'Advanced Diploma/Diploma (%)': 'Advanced Diploma level', \
            'Certificate (%)': 'Certificate'})

    parents = ['Total population aged 15 years', 'Total population aged 15 years', 'Total population aged 15 years',\
               'Total population aged 15 years','Total population aged 15 years','Total population aged 15 years','']


    fig = go.Figure(go.Sunburst(
        labels=dfd.columns,
        parents=parents,
        values=dfd.loc[suburb_choice],
        branchvalues='total',
        name=suburb_choice,
        hovertemplate='<b>%{label} </b> <br> Total Population: %{value:d3-format}',
        texttemplate = '%{percentRoot:.2%}'
    ))

    # fig = go.Figure([go.Pie(
    #                         labels = dff.columns,
    #                         values = dff.loc[suburb_choice],
    #                         hole = 0.6,
    #                         hoverinfo ='label+percent'
    #                         )
    #                  ])

    # fig.update_layout(title_text = 'educational level (%) ')
    return (fig)



#connect plotly and dash, create employment graph
@app.callback(
    Output(component_id='labor_graph', component_property='figure'),
    [Input(component_id='suburb_choice', component_property='value')]
)

def update_graph(suburb_choice):
    dff = df[['Employed (no.)','Unemployed (no.)','Labour Force (no.)']]
    dff = dff.rename(
        columns = {'Employed (no.)': 'Employed', 'Unemployed (no.)': 'Unemployed',\
                 'Labour Force (no.)': 'Total labour Force' })
    parents = ['Total labour Force','Total labour Force','']

    fig = go.Figure(go.Sunburst(
        labels=dff.columns,
        parents=parents,
        values=dff.loc[suburb_choice],
        branchvalues='total',
        name=suburb_choice,
        hovertemplate='<b>%{label} </b> <br> Population : %{value}',
        textinfo='label + percent root '
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                      # Add annotations in the center of the donut pies.
                      # annotations = [dict(text='population', x=0.82, y=0.5, font_size=20, showarrow=False)],
                      # title_text = "Census based on 2018"
                      )

    return (fig)

if __name__ == '__main__':
    app.run_server(debug=True, port='8050', host='0.0.0.0')
