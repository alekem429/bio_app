from dash import Dash, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from requests_app import *
from components import *

external_stylesheets = [dbc.themes.SIMPLEX, "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

colors_genes = generate_color_palette(get_list_of_genes())
colors_factors = generate_color_palette(get_list_of_factors())

death_description_canvas = html.Div(
    [
        html.Button(
            "Description", id="desc-button", n_clicks=0, className="button button-desc"
        ),
        dbc.Offcanvas(
            [html.H3("", id="desc-title"),
            html.P("", id="desc-text")],
            id="desc-canvas",
            title="Death type description",
            is_open=False,
        ),
    ]
)

navbar = dbc.NavbarSimple(
    brand=dbc.NavbarBrand(
        ["Bio App"]
    ),
    color="#154C8E",
    dark=True,
    className="p-0 shadow",
    fluid=True
)


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Modal(
            [
                dbc.ModalHeader("Notification"),
                dbc.ModalBody("New death type added successfully!"),
            ],
            id="modal-death-type",
            is_open=False,
            ),
            dbc.Row([
                dbc.Row([html.H5("Edit death types"),
                         dbc.Col([
                             dbc.Col([dbc.Input(id="add-death-type-input", type="text", placeholder="Death type",
                                                className="name-input"),
                                      html.Button("Add", className="button-add  button", id="add-death-type-button"),
                                      ],
                                     className="d-inline-flex w-50")]),
                         dbc.Col([dcc.Dropdown([], id="remove-death-type-select", placeholder="Death type",
                                               className="name-input", multi=True),
                                  html.Button("Remove", className="button-remove button", id="remove-death-type-button")
                                  ], className="d-inline-flex w-50")])
            ], className="shadow m-3 p-3 border rounded"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Row([html.H5("Edit deaths"),
                         dbc.Col([
                             dbc.Col([dbc.Input(id="add-death-input", type="text", placeholder="Death description",
                                                className="name-input"),
                                      html.Button("Add", className="button-add  button", id="add-death-button")],
                                     className="d-inline-flex w-50")]),
                         dbc.Col([dcc.Dropdown([], id="remove-death-select", placeholder="Death description",
                                               className="name-input", multi=True),
                                  html.Button("Remove", className="button-remove button", id="remove-death-button")
                                  ], className="d-inline-flex w-50")])
            ], className="shadow m-3 p-3 border rounded")
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
        dbc.Modal(
            [
                dbc.ModalHeader("Notification"),
                dbc.ModalBody("New factor added successfully!"),
            ],
            id="modal-factor",
            is_open=False,
            ),
            dbc.Row([
                dbc.Row([html.H5("Edit factors"),
                         dbc.Col([
                             dbc.Col([dbc.Input(id="add-factor-input", type="text", placeholder="Factor name",
                                                className="name-input"),
                                      html.Button("Add", className="button-add  button", id="add-factor-button")],
                                     className="d-inline-flex w-50")]),
                         dbc.Col([dcc.Dropdown([], id="remove-factor-select", placeholder="Factor name",
                                               className="name-input", multi=True),
                                  html.Button("Remove", className="button-remove button", id="remove-factor-button")
                                  ], className="d-inline-flex w-50")])
            ], className="shadow m-3 p-3 border rounded")
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Modal(
            [
                dbc.ModalHeader("Notification"),
                dbc.ModalBody("New gene added successfully!"),
            ],
            id="modal-gene",
            is_open=False,
            ),
            dbc.Row([
                dbc.Row([html.H5("Edit genes"),
                         dbc.Col([
                             dbc.Col([dbc.Input(id="add-gene-input", type="text", placeholder="Gene name",
                                                className="name-input"),
                                      html.Button("Add", className="button-add  button", id="add-gene-button")],
                                     className="d-inline-flex w-50")]),
                         dbc.Col([dcc.Dropdown([], id="remove-gene-select", placeholder="Gene name",
                                               className="name-input", multi=True),
                                  html.Button("Remove", className="button-remove button", id="remove-gene-button")
                                  ], className="d-inline-flex w-50")])
            ], className="shadow m-3 p-3 border rounded")
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Death Types"),
        dbc.Tab(tab4_content, label="Genes"),
        dbc.Tab(tab3_content, label="Factors"),
        dbc.Tab(tab2_content, label="Deaths")
    ]
)


app.layout = dbc.Container(
    [
     dbc.Row([navbar]),
        dcc.Interval(id="interval", interval=2000, n_intervals=0, disabled=True),
        dbc.Row([
            dbc.Row([html.H5("Select death type"),
                     dbc.Row([
                         dbc.Col(
                             dcc.Dropdown(
                                 [],
                                 id='deaths_dropdown',
                                 placeholder="Select death type",
                                 className="mb-2"
                             ),
                             width=6  # Adjust the column width (out of 12)
                         ),
                         dbc.Col(
                             death_description_canvas,
                             width=6  # Adjust the column width (out of 12)
                         )
                     ]),
                     dbc.Row([html.Table(id='table')], className="table-container")
                     ])],
            className="shadow m-3 p-3 border rounded w-90"),
        dbc.Row([tabs],
            className="shadow m-3 p-3 border rounded w-90"),
     ], fluid=True, className="p-0 m-0")

@app.callback(
    Output("desc-canvas", "is_open"),
     Output("desc-text", "children"),
     Output("desc-title", "children"),
    Input("desc-button", "n_clicks"),
    [State("desc-canvas", "is_open"),
     State("deaths_dropdown", "value")],
)
def toggle_death_canvas(n1, is_open, value):
    if n1:
        desc = "desc"
        return not is_open, desc, str(value)
    return is_open, [],[]


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


def render_table(death_id):
    data = get_death_types_by_id(death_id)
    if not data:
        return []
    rows = flatten_data(data, colors_genes, colors_factors)
    return [html.Thead(html.Tr([html.Th("ID"),
                                html.Th("Description"),
                                html.Th("Factors"),
                                html.Th("Genes"),
                                ])), html.Tbody(rows, )]

@app.callback(
    Output("remove-death-type-select", "options"),
    Output("modal-death-type", "is_open"),
    Input("add-death-type-button", "n_clicks"),
    State("add-death-type-input", "value"),
    prevent_initial_call=True
)
def input_death_type(n_clicks, value):
    toast=False
    status=0
    if n_clicks and n_clicks > 0 and value:
        status = add_death_type(value)
    data = get_death_types()
    options = [{"label": item["name"], "value": item["id"]} for item in data]
    if status == 200:
        toast = True
    return options, toast


@app.callback(
    Output("remove-gene-select", "options"),
    Output("modal-gene", "is_open"),
    Input("add-gene-button", "n_clicks"),
    State("add-gene-input", "value"),
    prevent_initial_call=True
)
def input_gene(n_clicks, value):
    toast = False
    status = 0
    if n_clicks and n_clicks > 0 and value:
        status = add_gene(value)
    data = get_list_of_genes()
    options = [{"label": item["name"], "value": item["id"]} for item in data]
    if status == 200:
        toast = True
    return options, toast

@app.callback(
    Output("remove-factor-select", "options"),
    Output("modal-factor", "is_open"),
    Input("add-factor-button", "n_clicks"),
    State("add-factor-input", "value"),
    prevent_initial_call=True
)
def input_factor(n_clicks, value):
    toast = False
    status = 0
    if n_clicks and n_clicks > 0 and value:
        status = add_factor(value)
    data = get_list_of_factors()
    options = [{"label": item["name"], "value": item["id"]} for item in data]
    if status == 200:
        toast = True
    return options, toast

@app.callback(
    Output("table", 'children'),
    Input({'type': 'delete-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    Input("deaths_dropdown", "value"),
    prevent_initial_call=True,
)
def update_table(n_clicks, death_id):
    ctx = dash.callback_context

    if not ctx.triggered or n_clicks is None or all(nc is None for nc in n_clicks):
        return render_table(death_id)


    triggered_prop_ids = [p['prop_id'] for p in ctx.triggered]
    clicked_button = [eval(prop_id.split('.')[0]) for prop_id in triggered_prop_ids if prop_id.endswith('.n_clicks')]

    if not clicked_button:
        return render_table(death_id)

    idx = clicked_button[0]['index']
    status = delete_death(idx)
    return render_table(death_id)

if __name__ == "__main__":
    app.run_server(debug=True)