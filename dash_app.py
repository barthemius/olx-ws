# Plotly dash app for creating a visualisation dashboard of the real estate data in Lublin
# This is a simple dash app for visualising the data from the real estate market in Lublin.
# The data is collected from olx.pl and otodom.pl.
#

from dash import Dash, callback_context, no_update, html, Input, Output, dcc
from load_data import *

dtolx, dtod = load_data(get_filenames())

# Dropdown options
dropdown_options = [i.time.strftime("%d %B %Y") for i in dtolx]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1('Lublin Real Estate Market'),

        dcc.Dropdown(
            id='date-dropdown', 
            options=dropdown_options, 
            value=dropdown_options[0]
            ),

        # Plots
        html.Div(
            id='plots',
            children=[
                dcc.Graph(id="price-hist")
            ]
        ),
    ]
)


# Callback for the every graph
@app.callback(
    Output(component_id = "price-hist", component_property='figure'),
    Input(component_id = "date-dropdown", component_property='value')
)
def update_price_graph(input_value):
    pass




if __name__ == '__main__':
    app.run_server(debug=True)