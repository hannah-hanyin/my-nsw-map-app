import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc

mapbox_access_token = 'pk.eyJ1Ijoiamh1YSIsImEiOiJja2cwamMyencwMzZiMzZtaDM5aGQxajgzIn0.UC7uZu27XHGxQF4ZR785wQ'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

result = pd.read_csv('Database/result_merge2.csv')
suburbs = pd.read_csv('Database/suburb_list.csv', header=None, names=['ID', 'suburb'])

Types = []
for Type in result['types']:
    if Type not in Types:
        Types.append(Type)

suburb_options = [
    {"label": suburb, "value": suburb}
    for suburb in suburbs['suburb']
]

type_options = [
    {"label": Type, "value": Type}
    for Type in Types
]

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=150.864899, lat=-33.874619),
        zoom=7,
    )
)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Dropdown(
        id='suburb',
        options=suburb_options,
        value='Abbotsbury'
    ),
    dcc.Dropdown(
        id='Types',
        options=type_options,
        value='restaurant'
    ),
    html.Div([
        dcc.Graph(id='maps')
    ])
])


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
def update_map(suburb, Types):
    global layout
    dff = filter_dataframe(result, [suburb], [Types])

    traces = []

    for Suburb, dfff in dff.groupby('suburb'):
        trace = dict(
            type='scattermapbox',
            lon=dfff['lng'],
            lat=dfff['lat'],
            text=dfff['name'],
            name=suburb,
            marker=dict(size=4, opacity=0.6),

        )
        traces.append(trace)

    layout = dict(
        autosize=True,
        automargin=True,
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=10), orientation="h"),
        title="Satellite Overview",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style="light",
            # style="open-street-map",
            center=dict(lon=dfff['lng'].mean(), lat=dfff['lat'].mean()),
            zoom=12,
            )
        )
    figure = dict(data=traces, layout=layout)

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
