# Plotly dash app for creating a visualisation dashboard of the real estate data in Lublin
# This is a simple dash app for visualising the data from the real estate market in Lublin.
# The data is collected from olx.pl and otodom.pl.
#

from dash import Dash, callback_context, no_update, html, Input, Output, dcc, dash_table
from load_data import *
import plotly.express as px
import datetime

# Initalization - loading the data

dtolx, dtod = load_data(get_filenames())
n = len(dtolx)
reliable_future = (datetime.datetime.now() + datetime.timedelta(days=10 * 365)).year

# Dropdown options
dropdown_options = [i.time.strftime("%d %B %Y") for i in dtolx]

# Create app object

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "Lublin Real Estate Market",
            style={"textAlign": "center", "padding": 10, "color": "#000000"},
        ),
        dcc.Dropdown(
            id="date-dropdown", options=dropdown_options, value=dropdown_options[0]
        ),
        html.Br(),
        html.Div(id="div-table", children=[dash_table.DataTable(id="data-table")]),
        html.Br(),
        # Plots 2x2 grid
        html.Div(
            [
                html.Div(
                    id="first_col",
                    children=[
                        dcc.Graph(id="price-hist"),
                        dcc.Graph(id="days-on-market-hist"),
                    ],
                    style={"padding": 10, "flex": 1},
                ),
                html.Div(
                    id="second_col",
                    children=[
                        dcc.Graph(id="price-per-m2-hist"),
                        dcc.Graph(id="rooms-pie"),
                    ],
                    style={"padding": 10, "flex": 1},
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
        # html.Div(
        #         id='build_year_row',
        #         children=[
        #             dcc.Graph(id="build-year-hist")
        #         ],
        #     ),
    ],
)


# TODO 'https://plotly.com/python/figure-labels/ '
# Callback for data table
@app.callback(
    [Output("data-table", "data"), Output("data-table", "columns")],
    [Input("date-dropdown", "value")],
)
def update_data_table(input_value):
    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = DataSet(dtolx[i].time, dtolx[i].data)
        # if dtod[i].time.strftime("%d %B %Y") == input_value:
        #     dod = DataSet(dtod[i].time, dtod[i].data)

    # Debugging printing
    # print(float(dolx.days_passed().mean()))

    # Compute descritive statistics for the data
    mean_price = int(dolx.price().mean())
    median_price = int(dolx.price().median())
    mean_price_per_m2 = int(dolx.ppm2().mean())
    mean_days_passed = int(dolx.days_passed().mean())
    # mean_build_year = 0

    # Create data table
    data_table = [
        {
            "date": input_value,
            "mean_price": mean_price,
            "median_price": median_price,
            "mean_price_per_m2": mean_price_per_m2,
            "mean_days_passed": mean_days_passed,
            # 'mean_build_year': mean_build_year
        }
    ]

    # Create columns
    columns = [{"name": i, "id": i} for i in data_table[0].keys()]

    # print(data_table)
    # print(columns)

    return data_table, columns


# Callback for the every graph
@app.callback(
    Output(component_id="price-hist", component_property="figure"),
    Input(component_id="date-dropdown", component_property="value"),
)
def update_price_graph(input_value):
    # Get the data for the selected date

    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        # if dtod[i].time.strftime("%d %B %Y") == input_value:
        #     dod = dtod[i]

    # Create the figure
    full_data = dolx.price()
    full_data = full_data[full_data < 1200000]
    fig = px.histogram(
        full_data,
        x="price",
        nbins=30,
        title="Price distribution",
        labels={"price": "Price", "count": "Count"},
    )

    return fig


@app.callback(
    Output(component_id="price-per-m2-hist", component_property="figure"),
    Input(component_id="date-dropdown", component_property="value"),
)
def update_price_per_m2_graph(input_value):
    # Get the data for the selected date

    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        # if dtod[i].time.strftime("%d %B %Y") == input_value:
        #     dod = dtod[i]

    # Create the figure
    full_data = dolx.ppm2()
    full_data = full_data[full_data < 20000]
    fig = px.histogram(
        full_data,
        x="price_per_m2",
        nbins=50,
        title="Price per m2 distribution",
        labels={"price_per_m2": "Price per m2", "count": "Count"},
    )

    return fig


# @app.callback(
#     Output(component_id = "build-year-hist", component_property='figure'),
#     Input(component_id = "date-dropdown", component_property='value')
# )
# def update_build_year_graph(input_value):
#     # Get the data for the selected date

#     for i in range(n):
#         if dtolx[i].time.strftime("%d %B %Y") == input_value:
#             dolx = dtolx[i]
#         # if dtod[i].time.strftime("%d %B %Y") == input_value:
#         #     dod = dtod[i]

#     # Create the figure
#     full_data = dod.data['build_year']

#     # Clear stupid entries
#     full_data = full_data[(full_data > 1800) & (full_data < reliable_future)]

#     fig = px.histogram(
#         full_data,
#         x="build_year",
#         nbins=30,
#         title="Build year distribution",
#         labels = {"build_year": "Build year", "count": "Count"}
#         )


#     return fig


@app.callback(
    Output(component_id="rooms-pie", component_property="figure"),
    Input(component_id="date-dropdown", component_property="value"),
)
def update_rooms_pie_graph(input_value):
    # Get the data for the selected date

    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        # if dtod[i].time.strftime("%d %B %Y") == input_value:
        #     dod = dtod[i]

    # Create the figure
    full_data = dolx.rooms()
    fig = px.pie(
        full_data,
        values="rooms",
        names="rooms",
        title="Rooms distribution",
        labels={"rooms": "Rooms", "count": "Count"},
    )

    return fig


@app.callback(
    Output(component_id="days-on-market-hist", component_property="figure"),
    Input(component_id="date-dropdown", component_property="value"),
)
def update_days_on_market_graph(input_value):
    # Get the data for the selected date

    for i in range(n):
        if dtolx[i].time.strftime("%d %B %Y") == input_value:
            dolx = dtolx[i]
        # if dtod[i].time.strftime("%d %B %Y") == input_value:
        #     dod = dtod[i]

    # Create the figure
    full_data = dolx.days_passed()
    fig = px.histogram(
        full_data,
        x="days_passed",
        nbins=30,
        title="Days on market distribution",
        labels={"days_passed": "Days on market", "count": "Count"},
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
