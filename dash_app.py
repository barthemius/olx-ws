# Plotly dash app for creating a visualisation dashboard of the real estate data in Lublin
# This is a simple dash app for visualising the data from the real estate market in Lublin.
# The data is collected from olx.pl and otodom.pl.
#

from dash import Dash, callback_context, no_update, html, Input, Output, dcc
from load_data import *
import plotly.express as px
import datetime

# Initalization - loading the data

dtolx, dtod = load_data(get_filenames())
n = len(dtolx)
reliable_future = (datetime.datetime.now() + datetime.timedelta(days=10*365)).year

# Dropdown options
dropdown_options = [i.time.strftime("%d %B %Y") for i in dtolx]

# Create app object

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1('Lublin Real Estate Market'),

        dcc.Dropdown(
            id='date-dropdown', 
            options=dropdown_options, 
            value=dropdown_options[0]
            ),

        # Plots 2x2 grid

        html.Div(
            [
            html.Div(
                id='first_col',
                children=[
                    dcc.Graph(id="price-hist"),
                    dcc.Graph(id="days-on-market-hist"),   
                ],
                style={'padding': 10, 'flex': 1}
            ),

            html.Div(
                id='second_col',
                children=[
                    dcc.Graph(id="price-per-m2-hist"),
                    dcc.Graph(id="rooms-pie")
                ],
                style={'padding': 10, 'flex': 1}
            ),
        ],
        style={'display': 'flex', 'flex-direction': 'row'}
        ),

        html.Div(
                id='build_year_row',
                children=[
                    dcc.Graph(id="build-year-hist")
                ],
            ),
    ],
)


                
                
# TODO https://plotly.com/python/figure-labels/               

# Callback for the every graph
@app.callback(
    Output(component_id = "price-hist", component_property='figure'),
    Input(component_id = "date-dropdown", component_property='value')
)
def update_price_graph(input_value):
    # Get the data for the selected date
    
    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        if dtod[i].time.strftime("%d %B %Y") == input_value:
            dod = dtod[i]
        
    # Create the figure
    full_data = pd.concat((dolx.price(), dod.price()))
    fig = px.histogram(full_data, x="price", nbins=30)

    return fig


@app.callback(
    Output(component_id = "price-per-m2-hist", component_property='figure'),
    Input(component_id = "date-dropdown", component_property='value')
)
def update_price_per_m2_graph(input_value):
    # Get the data for the selected date
    
    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        if dtod[i].time.strftime("%d %B %Y") == input_value:
            dod = dtod[i]
        
    # Create the figure
    full_data = pd.concat((dolx.ppm2(), dod.ppm2()))
    fig = px.histogram(full_data, x="price_per_m2", nbins=50)

    return fig

@app.callback(
    Output(component_id = "build-year-hist", component_property='figure'),
    Input(component_id = "date-dropdown", component_property='value')
)
def update_build_year_graph(input_value):
    # Get the data for the selected date
    
    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        if dtod[i].time.strftime("%d %B %Y") == input_value:
            dod = dtod[i]
        
    # Create the figure
    full_data = dod.data['build_year']

    # Clear stupid entries
    full_data = full_data[(full_data > 1800) & (full_data < reliable_future)]

    fig = px.histogram(full_data, x="build_year", nbins=30)

    return fig


@app.callback(
    Output(component_id = "rooms-pie", component_property='figure'),
    Input(component_id = "date-dropdown", component_property='value')
)
def update_rooms_pie_graph(input_value):
    # Get the data for the selected date
    
    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        if dtod[i].time.strftime("%d %B %Y") == input_value:
            dod = dtod[i]
        
    # Create the figure
    full_data = pd.concat((dolx.rooms(), dod.rooms()))
    fig = px.pie(full_data, values="rooms", names="rooms")

    return fig


@app.callback(
    Output(component_id = "days-on-market-hist", component_property='figure'),
    Input(component_id = "date-dropdown", component_property='value')
)
def update_days_on_market_graph(input_value):
    # Get the data for the selected date
    
    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        if dtod[i].time.strftime("%d %B %Y") == input_value:
            dod = dtod[i]
        
    # Create the figure
    full_data = pd.concat((dolx.days_passed(), dod.days_passed()))
    fig = px.histogram(full_data, x="days_passed", nbins=30)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)