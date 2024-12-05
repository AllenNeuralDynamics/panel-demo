"""Starter code to get your panel app running"""
from panel_demo.utils import _get_metadata
import param
import panel as pn


class Database(param.Parameterized):
    name_filter = param.String(default="")
    derived_filter = param.String(default="All")

    def __init__(self):
        super().__init__()
        self.df = _get_metadata()

    def filter_data(self):
        df = self.df
        if self.name_filter:
            df = df[df["name"].str.contains(self.name_filter)]
        if not self.derived_filter == "All":
            df = df[df["derived"] == (self.derived_filter == "Derived")]
        return df


text_input = pn.widgets.TextInput(name="Filter by name:", value="")
derived_input = pn.widgets.Select(name="Filter by name:", options=["All", "Derived", "Not Derived"])

pn.state.location.sync(text_input, {"value": "name_filter"})
pn.state.location.sync(derived_input, {"value": "name_filter"})

db = Database()


def build_df_pane(text_filter, derived_filter):
    db.name_filter = text_filter
    db.derived_filter = derived_filter
    df = db.filter_data()
    return pn.pane.DataFrame(df)


df_pane = pn.bind(build_df_pane, text_input, derived_input)

pane = pn.Column(text_input, derived_input, df_pane)

pane.servable()
