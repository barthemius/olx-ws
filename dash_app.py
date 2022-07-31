# Plotly dash app for creating a visualisation dashboard of the real estate data in Lublin
# This is a simple dash app for visualising the data from the real estate market in Lublin.
# The data is collected from olx.pl and otodom.pl.
#

from dash import Dash, callback_context, no_update, html, Input, Output, dcc

app = Dash(__name__)

