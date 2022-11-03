import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Loading data
census = pd.read_csv('Database/aggregated_data_census_new.csv').set_index('suburb')
cost = pd.read_csv('Database/cost structure.csv').set_index('Category')
result = pd.read_csv('Database/results_merge.csv')
station = pd.read_csv('Database/Train Station Entries and Exits.csv')
count = pd.read_csv('Database/count_merge.csv').set_index('suburb')
suburbs = pd.read_csv('Database/suburb_list.csv').set_index('suburb')
market_cafe = pd.read_csv('Database/Market/market_cafe.csv').set_index('Category')
market_car = pd.read_csv('Database/Market/market_car.csv').set_index('Category')
market_clothing = pd.read_csv('Database/Market/market_clothing.csv').set_index('Category')
market_dentist = pd.read_csv('Database/Market/market_dentist.csv').set_index('Category')
market_hair = pd.read_csv('Database/Market/market_hair.csv').set_index('Category')
market_orchard = pd.read_csv('Database/Market/market_orchard.csv').set_index('Category')
market_restaurant = pd.read_csv('Database/Market/market_restaurant.csv').set_index('Category')

# Color Choices Setting
colors = ['darkgray', ] * 7
colors[1] = 'darkblue'
colors[3] = 'dodgerblue'
colors[2] = 'steelblue'
colors[0] = 'darkred'
colors[4] = 'indianred'
colors[6] = 'lightgray'

# Option Settings and Mapbox

suburb_options = [{'label': 'Suburbs', 'value': 'Index', 'disabled': True}] \
                 + list(map(lambda suburb: {'label': suburb, 'value': suburb}, suburbs.index.values))

industry_options = [{'label': 'Industry', 'value': 'Index', 'disabled': True}] \
                   + list(map(lambda industry: {'label': industry, 'value': industry}, cost.index.values))


# make tooltips and text inside for cards
def make_tooltip(title):
    if title == "rent":
        return dbc.Tooltip(
            "Average Rent Per Square Meters card displays average weekly rent cost in the suburb you choose."
            " (Data is updated in 2016)",
            target=f"tooltip-target-{title}",
            style={"font-size": 13})
    if title == "income":
        return dbc.Tooltip(
            "Household income card displays average income of household living in the suburb you choose."
            " (Data is updated in 2016)",
            target=f"tooltip-target-{title}",
            style={"font-size": 13})
    if title == "bus":
        return dbc.Tooltip(
            "No. of Bus Station card displays total number of bus stations in the suburb you choose."
            " (Data is updated in 2020)",
            target=f"tooltip-target-{title}",
            style={"font-size": 13})
    if title == "train":
        return dbc.Tooltip(
            "No. of Train Station card displays total number of train stations in the suburb you choose."
            " (Data is updated in 2020)",
            target=f"tooltip-target-{title}",
            style={"font-size": 13})
    if title == "competitor":
        return dbc.Tooltip(
            "No. of Competitors card displays total number of competitors who may affect your business in the suburb you choose."
            "Eg. if you choose restaurant industry in the dropdown list, the map will mark the location of other restaurants in the same suburb by using red dots."
            " (Data is updated in 2020)",
            target=f"tooltip-target-{title}",
            style={"font-size": 13})
    else:
        return None


mapbox_access_token = 'pk.eyJ1Ijoiamh1YSIsImEiOiJja2cwamMyencwMzZiMzZtaDM5aGQxajgzIn0.UC7uZu27XHGxQF4ZR785wQ'

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                        "assets/style.css"]

external_scripts = ["assets/jquery-3.5.1.min.js", 'assets/custom-script.js']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server
# Title and icon
app.title = "My NSW Business Map"
# Layout
app.layout = html.Div(
    html.Div([

        # Row 1: Service NSW Logo
        html.Div([
            html.Img(
                src=app.get_asset_url("NSW_logo.png"),
                id="NSW_logo",
                style={"height": "40px",
                       "width": "auto",
                       "margin-bottom": "15px",
                       "margin-top": "10px"})
        ], className="row"),

        # Row 2: Heading and introduction
        html.Div([html.H2(children="My NSW Business Map"),
                  html.Div(children='''My NSW Business Map aims to assist small business owners to make decisions
                  when they are planning to start a new business. Users can select a specific suburb and industry to
                  check their basic status.''')
                  ], style={
            "background-color": "navy",
            "color": "white",
            "border-style": "solid",
            "border": "15px solid navy",
            "padding": "20px",
            "font-family-name": "Arial"
        },
                 className="row"
                 ),

        # Row 3: Instruction
        html.Div([
            html.H3(children="Find a Suburb or an Industry",
                    style={
                        "margin-bottom": "0px",
                        "border-bottom": "solid 1px grey",
                        "font-family-name": "Arial",
                        "color": "#000000"
                    }),
            html.P(
                "The demographic, transportation and industry information of suburbs across the NSW are presented. To find a specific suburb and industry, you can search or select them from dropdown list.",
                style={
                    "color": "#696969",
                    "line-height": "100%",
                    "margin-top": "10px",
                    "fontSize": 18,
                    "font-family-name": "Arial"
                }),
        ],
            className="row",
            style={
                "margin-bottom": "15px",
            }
        ),

        # Row 4: Dropdown
        html.Div([

            # suburb selection
            html.Div([
                html.Label('Suburb Selection'),
                dcc.Dropdown(
                    id='suburb',
                    options=suburb_options,
                    placeholder="Select a suburb",
                    value='Sydney',
                    multi=False,
                    clearable=True,
                    style={'width': '100%'})
            ], className='four columns'),

            # Industry Selection
            html.Div([
                html.Label('Industry Selection'),
                dcc.Dropdown(
                    id='Types',
                    options=industry_options,
                    placeholder="Select a industry",
                    value='Restaurant',
                    multi=False,
                    clearable=True,
                    style={'width': '100%'})
            ], className='four columns')

        ], className="row",id='dropdiv'),

        # Row 5: Map and mini_container
        html.Div(
            [make_tooltip(t) for t in ["rent", "income", "bus", "train", "competitor"]] +
            [
                # Map
                html.Div([dcc.Graph(id='maps'),
                          html.I("Data source: Google Map API; Australian Bureau of Statistics Census Data; CoreLogic; (Note: Due to the limitation of the Google API, some data is not complete.)",
                                 style={"color": "black",
                                        "font-size": "10px",
                                        "font-family-name": "Arial"
                                        })
                          ],
                         className='nine columns'),

                # Mini_container
                html.Div([
                    dbc.CardDeck([

                        # Average rent
                        dbc.Card(id='average rent',
                                 children=[
                                     dbc.CardHeader("Average Rent Per Square Meters", id="tooltip-target-rent"),
                                     dbc.CardBody([
                                         html.H5([
                                             html.Span("$ "),
                                             html.Span(id='rental_card_title')
                                         ]),

                                     ])],
                                 className='card-light'
                                 ),

                        # Household income
                        dbc.Card(id='household income',
                                 children=[
                                     dbc.CardHeader("Household Weekly Income", id="tooltip-target-income"),
                                     dbc.CardBody([
                                         # html.Br(),
                                         html.H5([
                                             html.Span("$ "),
                                             html.Span(id='household_income')
                                         ]),

                                     ])],
                                 className='card-light'
                                 ),

                        # Bus station
                        dbc.Card(id='bus station',
                                 children=[
                                     dbc.CardHeader("No. of Bus Station", id="tooltip-target-bus"),
                                     dbc.CardBody([
                                         html.H5([
                                             html.Span(id='no_of_bus_station')
                                         ]),
                                     ]),
                                 ],
                                 className='card-light'
                                 ),

                        # Train station
                        dbc.Card(id='train station',
                                 children=[
                                     dbc.CardHeader("No. of Train Station", id="tooltip-target-train"),
                                     dbc.CardBody([
                                         html.H5([
                                             html.Span(id='no_of_train_station')
                                         ]),
                                     ]),
                                 ],
                                 className='card-light'
                                 ),

                        # Competitors
                        dbc.Card(id='competitors',
                                 children=[
                                     dbc.CardHeader("No. of Competitors", id="tooltip-target-competitor"),
                                     dbc.CardBody([
                                         html.H5([
                                             html.Span(id='no_of_competitor')
                                         ]),
                                     ]),
                                 ],
                                 className='card-light'
                                 ),

                    ])

                ], id='info container', className='three columns'),

            ], className='row'),
            
        # Demographic information text
        html.Div([html.H6(children="Demographic Information",
                              style={
                                  "margin-top": "35px",
                                  "margin-bottom": "0px",
                                  "border-bottom": "solid 1px grey",
                                  "font-family-name": "Arial",
                                  "color": "#000000"
                              }),
                      html.P(["Following graphs illustrate some demographic information of the selected suburb, which include population distribution, employment status and education level. To check detail category, put your mouse on the graph."],
                              style={
                                 "color": "#696969",
                                 "line-height": "100%",
                                 "margin-top": "10px",
                                 'fontSize': 18,
                                 "font-family-name": "Arial"

                             }),
                     html.P(["(Please note: if graph displays 0 or NaN, this means there is no related data of the suburb)"],
                              style={
                                 "color": "black",
                                 "font-style": "Italic",
                                 "font-size": "16px",
                                 "font-family-name": "Arial"})
                    ], className='row'),

        # Row 6: Demographic Plots
        html.Div([

            # Population
            html.Div([
                dcc.Graph(id='population'),
                html.I("Data source: Australian Bureau of Statistics Census Data (2016)", style={"color": "black", "font-size": "10px"})], className='four columns'),

            # Employment
            html.Div([
                dcc.Graph(id='employment')], className='four columns'),

            # Education level
            html.Div([
                dcc.Graph(id='education')], className='four columns'),

        ], className='row'),

        # Row 7: Industry information text
        html.Div([
            html.H6(children="Industry Information",
                    style={
                        "margin-bottom": "0px",
                        "border-bottom": "solid 1px grey",
                        "font-family-name": "Arial",
                        "color": "#000000"
                    }),
            html.P(
                "You can get a brief idea about where your major cost will be happened by checking the cost structure graph, which shows the average percentage of each cost from 2015 to 2020. And you can find the major customer group of your selected industry by checking the major market graph.",
                style={
                    "color": "#696969",
                    "line-height": "100%",
                    "margin-top": "10px",
                    'fontSize': 18,
                    "font-family-name": "Arial"
                }),
        ],
            className="row",
            style={
                "margin-bottom": "15px",
            }
        ),

        # Row 8: Industry Insight
        html.Div([

            # Average cost structure
            html.Div([
                dcc.Graph(id='cost_structure'),
                html.I("Data source: IBIS World", style={"color": "black", "font-size": "10px"})
            ], className='six columns'),

            # Major market
            html.Div([
                dcc.Graph(id='market')], className='six columns')

        ], className='row'),

        # Row 9: "Start a business in NSW" title
        html.Div([
            html.H3(children="Start a Business in NSW",
                    style={
                        "margin-bottom": "0px",
                        "border-bottom": "solid 1px grey",
                        "font-family-name": "Arial",
                        "color": "#000000"
                    }),
            html.P(
                "The following content shows the progress of how to start a new business in NSW. Cilck the text and you will find the detail information. To get more information, please refer to the 'more information' link.",
                style={
                    "color": "#696969",
                    "line-height": "100%",
                    "margin-top": "10px",
                    "fontSize": 18,
                    "font-family-name": "Arial"
                })], className="row"),

        # Row 10: Progress chart
        html.Div([
            html.Div([
                html.Div([
                    html.Img(id='step12',
                             src=app.get_asset_url('step12.png'),
                             style={"height": "90px",
                                    "width": "auto",
                                    "top": "5px"}),
                ], style={"height": "auto",
                          "width": "auto",
                          "margin-top": "10px"}),

                html.Div(
                    [
                        html.Div([
                            html.A(children='Set up as a solo trader',
                                   href="https://www.service.nsw.gov.au/transaction/set-sole-trader")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "center"}),
                        html.Div([
                            html.A(children='Register a company',
                                   href="https://www.service.nsw.gov.au/transaction/register-company")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "center"}),
                        html.Div([
                            html.A(children='Register a limited partnership',
                                   href="https://www.service.nsw.gov.au/transaction/register-limited-partnership")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "center"}),
                        html.Div([
                            html.A(children='Set up a trust business structure',
                                   href="https://www.service.nsw.gov.au/transaction/set-trust-business-structure")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "center"}),
                        html.Div([
                            html.A(children='Register a co-operative',
                                   href="https://www.service.nsw.gov.au/transaction/register-co-operative")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "center"}),
                    ], style={"margin-top": "5px"}),
                html.Div([
                    html.Img(id='step3',
                             src=app.get_asset_url('step3.png'),
                             style={"height": "90px",
                                    "width": "auto"})
                ], style={"height": "auto",
                          "width": "auto",
                          "margin-top": "10px"}),
                html.Div(
                    [
                        html.Div([
                            html.A(children='Register an Australia Business Number',
                                   href="https://www.service.nsw.gov.au/transaction/register-australian-business-number-abn")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "left"}),
                        html.Div([
                            html.A(children='Apply for an Administrator AUSkey',
                                   href="https://www.service.nsw.gov.au/transaction/apply-administrator-auskey")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "left"}),
                        html.Div([
                            html.A(children='Register a business name',
                                   href="https://www.service.nsw.gov.au/services/business-industries-and-employment/starting-business/register-business-association-name")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "left"}),
                        html.Div([
                            html.A(children='Register your business for Goods and Services Tax (GST)',
                                   href="https://www.service.nsw.gov.au/transaction/register-your-business-goods-and-services-tax-gst")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "left"}),
                        html.Div([
                            html.A(children='Apply for a business Tax File Number',
                                   href="https://www.service.nsw.gov.au/transaction/apply-business-tax-file-number-tfn")
                        ], style={"font-size": "12px", "margin-bottom": "0", "text-align": "left"}),
                    ], style={"margin-top": "5px"}),

            ], className='progress', style={"display": "flex",
                                            "justify-content": "center"}),
            html.Div([
                html.A(children="More information：", style={"text-decoration": "none", "color": "black"}),
                html.A(children="https://www.service.nsw.gov.au/guide/start-or-grow-business-nsw",
                       href="https://www.service.nsw.gov.au/guide/start-or-grow-business-nsw")
            ], style={"font-size": "10px", "font-style": "italic", "text-align": "center"}),
            html.I("Data source: Service NSW", style={"color": "black", "font-size": "10px"})
        ], className='row')
    ], style={"margin-bottom": "30px"}, className='ten columns offset-by-one'
    )
)


# Interactive
# Population
@app.callback(
    Output(component_id='population', component_property='figure'),
    [Input(component_id='suburb', component_property='value')]
)
def update_graph(suburb):
    dff = census[['Males - Total (no.)', 'Females - Total (no.)', 'Persons - Total (no.)']]
    dff = dff.rename(
        columns={'Males - Total (no.)': 'Male', 'Females - Total (no.)': 'Female',
                 'Persons - Total (no.)': 'Population'})
    parents = ['Population', 'Population', '']

    if dff.loc[suburb].sum() == 0:
        dic = dict(colorscale='rdbu')
    else:
        dic = dict(colorscale='rdbu',
                   colors=['rgb(178,24,43)', 'rgb(33,102,172)', 'white'])

    figure = go.Sunburst(
        labels=dff.columns,
        parents=parents,
        values=dff.loc[suburb],
        branchvalues='total',
        name=suburb,
        hovertemplate='<b>%{label} </b> <br> Population Percentage: %{percentRoot:.3%}',
        textinfo='label + value ',
        marker=dic,
        insidetextorientation='horizontal'
    )

    layout = go.Layout(title={'text': "Population",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                       #autosize=True,
                       #width=200,
                       margin=dict(b=10, l=30, r=30, t=20, pad=50)
                       )
    fig = go.Figure(data=[figure], layout=layout)
    return fig


# Employment

@app.callback(
    Output(component_id='employment', component_property='figure'),
    [Input(component_id='suburb', component_property='value')]
)
def update_graph(suburb):
    dff = census[['Employed (no.)', 'Unemployed (no.)', 'Labour Force (no.)']]
    dff = dff.rename(
        columns={'Employed (no.)': 'Employed', 'Unemployed (no.)': 'Unemployed', \
                 'Labour Force (no.)': 'Labour Force'})
    parents = ['Labour Force', 'Labour Force', '']

    if dff.loc[suburb].sum() == 0:
        dic = dict(colorscale='rdbu')
    else:
        dic = dict(colorscale='rdbu',
                   colors=['rgb(33,102,172)', 'rgb(178,24,43)', 'white'])

    figure = go.Sunburst(
        labels=dff.columns,
        parents=parents,
        values=dff.loc[suburb],
        branchvalues='total',
        name=suburb,
        hovertemplate='<b>%{label} </b> <br> Population Percentage : %{percentRoot:.3%}',
        textinfo='label + value ',
        marker=dic
    )

    layout = go.Layout(title={'text': "Employment",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                       #autosize=True,
                       #width=200,
                       margin=dict(b=10, l=30, r=30, t=20, pad=50)
                       )
    fig = go.Figure(data=[figure], layout=layout)

    return fig


# Education
@app.callback(
    Output(component_id='education', component_property='figure'),
    [Input(component_id='suburb', component_property='value')]
)
def update_graph(suburb):
    dff = census[['Non-School Qualifications (no.)', 'Postgraduate Degree (no.)', 'Graduate Diploma/Graduate Certificate (no.)',
                    'Bachelor Degree (no.)', 'Advanced Diploma/Diploma (no.)', 'Certificate (no.)',
                    'Total population aged 15 years and over (no.)']]

    dff.insert(len(dff.columns), 'Others', dff['Total population aged 15 years and over (no.)']-dff.iloc[:,:6].sum(axis=1))
    dfd = dff.copy()

    dfd = dfd.rename(columns={'Postgraduate Degree (no.)': 'Postgraduate',
                              'Graduate Diploma/Graduate Certificate (no.)': 'Graduate Diploma/Certificate',
                              'Bachelor Degree (no.)': 'Bachelor',
                              'Advanced Diploma/Diploma (no.)': 'Advanced Diploma',
                              'Certificate (no.)': 'Certificate',
                              'Non-School Qualifications (no.)':'Non-School Qualifications',
                              'Total population aged 15 years and over (no.)':'Population aged 15+'})

    parents = ['Population aged 15+', 'Population aged 15+','Population aged 15+',
               'Population aged 15+', 'Population aged 15+',
               'Population aged 15+', '','Population aged 15+']

    if dfd.loc[suburb].sum() == 0:
        dic = dict(colorscale='rdbu')
    else:
        dic = dict(colorscale='rdbu',
                   colors=['rgb(253,219,199)', 'rgb(209,229,240)', 'rgb(146,197,222)', 'rgb(178,24,43)',
                           'rgb(241,96,77)', 'rgb(168,218,220)', 'white','rgb(33,102,172)'])

    figure = go.Sunburst(
        labels=dfd.columns,
        parents=parents,
        values=dfd.loc[suburb],
        branchvalues='total',
        name=suburb,
        # hovertemplate='<b>%{label} </b> <br> Total Population: %{value:d3-format}',
        # texttemplate='%{percentRoot:.2%}',
        hovertemplate='<b>%{label} </b> <br> Population Percentage : %{percentRoot:.3%}',
        textinfo='label + value ',
        marker=dic,

    )

    layout = go.Layout(title={'text': "Education level",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top',
                              },
                       #autosize=True,
                       #width=200,
                       margin=dict(b=10, l=30, r=30, t=20, pad=50)
                       )
    fig = go.Figure(data=[figure], layout=layout)

    return fig


# Map
def filter_dataframe(df, suburb, Types):
    dff = df[
        df["suburb"].isin(suburb)
        & df["types"].isin(Types)

        ]
    return dff


@app.callback(
    dash.dependencies.Output('maps', 'figure'),
    [dash.dependencies.Input('suburb', 'value'),
     dash.dependencies.Input('Types', 'value')
     ])
# update map after selected suburb and industry
def update_map(suburb, Types):
    global layout, dfff, dfff_bus, dfff_train
    dff = filter_dataframe(result, [suburb], [Types])
    dff_bus = filter_dataframe(result, [suburb], ["Bus stop"])
    dff_train = filter_dataframe(result, [suburb], ["Train station"])
    # set default longitude and latitude
    def_lng = suburbs.loc[suburbs.index == suburb, 'lng'].values[0]
    def_lat = suburbs.loc[suburbs.index == suburb, 'lat'].values[0]
    traces = []
    trace = dict(
        type='scattermapbox',
        lon=151.205178,
        lat=-33.8674774

    )
    traces.append(trace)

    for Suburb, dfff in dff.groupby('suburb'):
        # set location as the competitor location
        def_lng = dfff['lng'].mean()
        def_lat = dfff['lat'].mean()
        trace = dict(
            type='scattermapbox',
            lon=dfff['lng'],
            lat=dfff['lat'],
            text=dfff['name'] + '.  Rating: ' + [str(i) for i in dfff['rating']],
            name='Exist Industry Competitors',
            hoverinfo='text',
            marker=dict(size=10, opacity=0.6, color='#C50C2F'),
        )
        traces.append(trace)

    # add bus information
    for Suburb, dfff_bus in dff_bus.groupby('suburb'):
        trace = dict(
            type='scattermapbox',
            lon=dfff_bus['lng'],
            lat=dfff_bus['lat'],
            text=dfff_bus['name'],
            name='Bus Station',
            hoverinfo='text',
            showlegend=False,
            marker=dict(size=10, opacity=0.6,color='#0033FF',symbol='bus'),
        )
        traces.append(trace)

    # add train information
    for Suburb, dfff_train in dff_train.groupby('suburb'):
        train_volume = []
        for st in dfff_train['name']:
            for st2 in range(len(station)):
                if st in station['STATION'][st2]:
                    train_volume.append(
                        [station['STATION'][st2], station['Entries 24 hours'][st2], station['Exits 24 hours'][st2]])
            if len(train_volume) == 0:
                train_volume.append([st, 'Null', 'Null'])
        trace = dict(
            type='scattermapbox',
            lon=dfff_train['lng'],
            lat=dfff_train['lat'],
            text=dfff_train['name'] + '.  entries/exits: ' + [str(i[1]) for i in train_volume] + '/' + [str(i[2]) for i
                                                                                                        in
                                                                                                        train_volume],
            name='Train Station',
            hoverinfo='text',
            showlegend=False,
            marker=dict(size=10, opacity=1, color='#00FF33',symbol='rail'),
        )
        traces.append(trace)

    try:
        layout = dict(
            autosize=True,
            automargin=True,
            margin=dict(l=30, r=30, b=20, t=40),
            hovermode="closest",
            plot_bgcolor="#C50C2F",
            paper_bgcolor="#F9F9F9",
            legend=dict(font=dict(size=10), orientation="h"),

            mapbox=dict(
                accesstoken=mapbox_access_token,
                style="light",
                # style="open-street-map",
                # center=dict(lon=dfff['lng'].mean(), lat=dfff['lat'].mean()),
                center=dict(lon=def_lng, lat=def_lat),
                zoom=12,
            )
        )
    except UnboundLocalError:
        layout = dict(
            autosize=True,
            automargin=True,
            margin=dict(l=30, r=30, b=20, t=40),
            hovermode="closest",
            plot_bgcolor="#C50C2F",
            paper_bgcolor="#F9F9F9",
            legend=dict(font=dict(size=10), orientation="h"),

            mapbox=dict(
                accesstoken=mapbox_access_token,
                style="light",
                # style="open-street-map",
                center=dict(lon=def_lng, lat=def_lat),
                zoom=12,
            )
        )

    figure = dict(data=traces, layout=layout)

    return figure


# Average Rent
@app.callback(
    Output(component_id='rental_card_title', component_property='children'),
    [Input(component_id='suburb', component_property='value')]
)
def get_rental_card_subtitle(suburb):
    df_rental = census['Weekly median advertised rent']
    if df_rental.loc[suburb] == 0:
        return 'Null'
    else:
        return df_rental.loc[suburb]




# Income
@app.callback(
    Output(component_id='household_income', component_property='children'),
    [Input(component_id='suburb', component_property='value')]
)
def get_income_card_subtitle(suburb):
    df_income = census['Median Household Weekly Income']
    if df_income.loc[suburb] == 0:
        return 'Null'
    else:
        return df_income.loc[suburb]


# No. of Bus Station
@app.callback(
    Output(component_id='no_of_bus_station', component_property='children'),
    [Input(component_id='suburb', component_property='value')]
)
def get_bus_station(suburb):
    df_bus_count = count['Bus stop']
    if df_bus_count.loc[suburb] == 0:
        return 'Null'
    else:
        return df_bus_count.loc[suburb]


# No. of Train Station
@app.callback(
    Output(component_id='no_of_train_station', component_property='children'),
    [Input(component_id='suburb', component_property='value')]
)
def get_train_station(suburb):
    df_train_station = count['Train station']
    if df_train_station.loc[suburb] == 0:
        return 'Null'
    else:
        return df_train_station.loc[suburb]


# No. of Competitor
@app.callback(
    Output(component_id='no_of_competitor', component_property='children'),
    [Input(component_id='suburb', component_property='value'),
     Input(component_id='Types', component_property='value')]
)
def get_count_competitor(suburb, Types):
    df_count_competitor = count[Types]
    if df_count_competitor.loc[suburb] == 0:
        return 'Null'
    else:
        return df_count_competitor.loc[suburb]


# Cost Structure
@app.callback(Output('cost_structure', 'figure'),
              [Input('Types', 'value')])
def update_cost_bar(Types):
    data = [go.Bar(
        y=cost.columns,
        x=cost.loc[Types],
        hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
        orientation='h',
        marker_color=colors)]

    layout = go.Layout(title='Average Cost structure (%)',
                       xaxis_title=Types)

    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(autosize=False, margin=dict(l=50))

    return fig


# Major Market
@app.callback(Output('market', 'figure'),
              [Input('Types', 'value')])
def update_market_bar(Types):
    if 'Restaurant' == Types:
        data = [go.Bar(y=market_restaurant.columns, x=market_restaurant.loc[Types],
                       hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
                       orientation='h', marker_color=colors)]
        layout = go.Layout(title='Major Market (%)',
                           xaxis_title=Types)
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(autosize=False, margin=dict(l=50))

        return fig

    if 'Coffee shop' == Types:
        data = [go.Bar(y=market_cafe.columns, x=market_cafe.loc[Types],
                       hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
                       orientation='h', marker_color=colors)]
        layout = go.Layout(title='Major Market (%)',
                           xaxis_title=Types)
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(autosize=False, margin=dict(l=50))

        return fig

    if 'Motor repair' == Types:
        data = [go.Bar(y=market_car.columns, x=market_car.loc[Types],
                       hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
                       orientation='h', marker_color=colors)]
        layout = go.Layout(title='Major Market (%)',
                           xaxis_title=Types)

        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(autosize=False, margin=dict(l=50))

        return fig

    if 'Hair care' == Types:
        data = [go.Bar(y=market_hair.columns, x=market_hair.loc[Types],
                       hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
                       orientation='h', marker_color=colors)]
        layout = go.Layout(title='Major Market (%)',
                           xaxis_title=Types)
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(autosize=False, margin=dict(l=50))

        return fig

    if 'Dentist' == Types:
        data = [go.Bar(y=market_dentist.columns, x=market_dentist.loc[Types],
                       hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
                       orientation='h', marker_color=colors)]
        layout = go.Layout(title='Major Market (%)',
                           xaxis_title=Types)
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(autosize=False, margin=dict(l=50))

        return fig

    if 'Clothing store' == Types:
        data = [go.Bar(y=market_clothing.columns, x=market_clothing.loc[Types],
                       hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
                       orientation='h', marker_color=colors)]
        layout = go.Layout(title='Major Market (%)',
                           xaxis_title=Types)
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(autosize=False, margin=dict(l=50))

        return fig

    if 'Orchard' == Types:
        data = [go.Bar(y=market_orchard.columns, x=market_orchard.loc[Types],
                       hovertemplate='%{label}: </b> %{value} %  <extra></extra> ',
                       orientation='h', marker_color=colors)]
        layout = go.Layout(title='Major Market (%)',
                           xaxis_title=Types)
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(autosize=False, margin=dict(l=50))

        return fig


if __name__ == '__main__':
    app.run_server()
