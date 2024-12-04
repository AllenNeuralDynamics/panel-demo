"""Starter code to get your panel app running"""
from panel_demo.utils import _get_metadata
import pandas as pd
import panel as pn


pn.extension('vega')

df = _get_metadata()

print(df.head())

# Filter based on a text input field

text_input = pn.widgets.TextInput(name='Filter by name')


def get_filtered_df(text):
    filtered_df = df[df['name'].str.contains(text)]
    return filtered_df


def get_dataframe(value):
    return pn.pane.DataFrame(get_filtered_df(value))


col = pn.Column(text_input, pn.bind(get_dataframe, value=text_input))

col.servable()