from dash import Dash, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from requests_app import *
from components import *


external_stylesheets = [dbc.themes.SIMPLEX, "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

colors_genes = generate_color_palette(get_list_of_genes())
colors_factors = generate_color_palette(get_list_of_factors())


navbar = dbc.NavbarSimple(
    brand=dbc.NavbarBrand(
        [
            "Bio App"
        ]
    ),
    color="#154C8E",
    dark=True,
    className="p-0 shadow",
    fluid=True
)

app.layout = dbc.Container(
    [
     dbc.Row([navbar]),
     dbc.Row([
              dbc.Row([html.H5("Select death type"),
                       dcc.Dropdown([], id='deaths_dropdown', placeholder="Select death type", className="mb-2"),
                       dbc.Row([html.Table(id='table')],className="table-container")
                       ])],
             className="shadow m-3 p-3 border rounded w-90"),
        dbc.Row([
            dbc.Row([html.H5("Edit death types"),
                     dbc.Col([
                         dbc.Col([dbc.Input(id="add-death-input", type="text", placeholder="Death type",
                                            className="name-input"),
                                  html.Button("Add", className="button-add  button", id="add-death-button"),
                                  dbc.Toast(
                                      id="toast",
                                      header="Notification",
                                      is_open=False,
                                      dismissable=True,
                                      icon="success",
                                      duration=4000,
                                      children="Death type added successfully!",
                                  )
                                  ],
                                 className="d-inline-flex w-50")]),
                     dbc.Col([dcc.Dropdown([], id="remove-death-select", placeholder="Death type",
                                           className="name-input", multi=True),
                              html.Button("Remove", className="button-remove button", id="remove-death-button")
                              ], className="d-inline-flex w-50")])
        ], className="shadow m-3 p-3 border rounded"),
        dbc.Row([
            dbc.Row([html.H5("Edit factors"),
                     dbc.Col([
                         dbc.Col([dbc.Input(id="add-gene-input", type="text", placeholder="Death type",
                                            className="name-input"),
                                  html.Button("Add", className="button-add  button", id="add-gene-button")],
                                 className="d-inline-flex w-50")]),
                     dbc.Col([dcc.Dropdown([], id="remove-gene-select", placeholder="Death type",
                                           className="name-input", multi=True),
                              html.Button("Remove", className="button-remove button", id="remove-gene-button")
                              ], className="d-inline-flex w-50")])
        ], className="shadow m-3 p-3 border rounded"),
        dbc.Row([
            dbc.Row([html.H5("Edit genes"),
                     dbc.Col([
                         dbc.Col([dbc.Input(id="add-gene-input", type="text", placeholder="Death type", className="name-input"),
                         html.Button("Add", className="button-add  button", id="add-gene-button")], className="d-inline-flex w-50")]),
                     dbc.Col([dcc.Dropdown([], id="remove-gene-select", placeholder="Death type", className="name-input", multi=True),
                                      html.Button("Remove", className="button-remove button", id="remove-gene-button")
                     ], className="d-inline-flex w-50")])
        ], className="shadow m-3 p-3 border rounded")
     ], fluid=True, className="p-0 m-0")

@app.callback(
    Output("deaths_dropdown", "options"),
    Output("deaths_dropdown", "value"),
    Input("deaths_dropdown", "id")
)
def fetch_death_types(_):
    data = get_death_types()
    options = [{"label": item["name"], "value": item["id"]} for item in data]
    value = options[0]["value"] if options else None
    return options, value

@app.callback(
    Output("table", "children"),
    Input("deaths_dropdown", "value")
)
def render_table(death_id):
    data = get_death_types_by_id(death_id)
    if not data:
        return []
    rows = flatten_data(data, colors_genes, colors_factors)
    return [html.Thead(html.Tr([html.Th("ID"),
                                html.Th("Description"),
                                html.Th("Factors"),
                                html.Th("Genes")])), html.Tbody(rows, )]

@app.callback(
    Output("remove-death-select", "options"),
    Output("toast", "is_open"),
    Input("add-death-button", "n_clicks"),
    State("add-death-input", "value")
)
def update_output(n_clicks, value):
    toast=False
    status=0
    if n_clicks and n_clicks > 0 and value:
        status = add_death_type(value)
    data = get_death_types()
    options = [{"label": item["name"], "value": item["id"]} for item in data]
    if status == 200:
        toast = True
    return options, toast

if __name__ == "__main__":
    app.run_server(debug=True)