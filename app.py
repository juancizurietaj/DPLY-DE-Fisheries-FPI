from helpers import *

# App constructor
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Methods
# Methods
methods = dbc.Card(
    html.Div(
        [
            html.H1("Indicadores de desempeño pesquero", className="h1"),
            html.P(methods_text_1, className="labels"),
            html.P(methods_text_2, className="texts"),
            html.Div([
                html.Div([
                    html.Label("Componentes monitoreados", className="labels"),
                    html.P(len(data_fpi["Componente"].dropna().unique()), className="value-cards-value")
                ], style={"display": "flex", "flex-direction": "column"}),
                html.Div([
                    html.Label("Dimensiones monitoreadas", className="labels"),
                    html.P(len(data_fpi["Dimensión"].dropna().unique()), className="value-cards-value")
                ], style={"display": "flex", "flex-direction": "column"}),
                html.Div([
                    html.Label("Métricas monitoreadas", className="labels"),
                    html.P(len(data_fpi["Métrica"].dropna().unique()), className="value-cards-value")
                ], style={"display": "flex", "flex-direction": "column"})
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "space-around"}),
            html.Br(),
            html.Div(html.P(methods_text_3)),
            dcc.Graph(figure=create_example_methods_fig(), config={'displayModeBar': False}),
            dcc.Graph(figure=create_methods_fig(df=data_fpi,
                                                path_array=["Tipo", "Componente", "Dimensión", "Métrica"],
                                                values="Treemap_counter",
                                                color="Tipo"), config={'displayModeBar': False})
        ]
    ), className="methods-card-box"
)

# Overview
meters_layout = html.Div([
    html.Div(id="main-meter"),
    html.Br(),
    html.P("Componentes:", className="component-labels"),
    html.Br(),
    html.Div(id="io-meter", className="components-container"),

    # Input
    html.Div(id="i-cont", children=[html.Div([
        html.Div([html.Div(id="i-comp-1"), dbc.Button("Ver métricas", id="i-btn-1", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="i-comp-2"), dbc.Button("Ver métricas", id="i-btn-2", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="i-comp-3"), dbc.Button("Ver métricas", id="i-btn-3", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="i-comp-4"), dbc.Button("Ver métricas", id="i-btn-4", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="i-comp-5"), dbc.Button("Ver métricas", id="i-btn-5", n_clicks=0)],
                 className="component-element"),
    ], className="components-container")
    ]),

    # Output
    html.Div(id="o-cont", children=[html.Div([
        html.Div([html.Div(id="o-comp-1"), dbc.Button("Ver métricas", id="o-btn-1", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="o-comp-2"), dbc.Button("Ver métricas", id="o-btn-2", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="o-comp-3"), dbc.Button("Ver métricas", id="o-btn-3", n_clicks=0)],
                 className="component-element"),
    ], className="components-container")
    ]),

    # Output TLB
    html.Div(id="otlb-cont", children=[html.Div([
        html.Div([html.Div(id="otlb-comp-1"), dbc.Button("Ver métricas", id="otlb-btn-1", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="otlb-comp-2"), dbc.Button("Ver métricas", id="otlb-btn-2", n_clicks=0)],
                 className="component-element"),
        html.Div([html.Div(id="otlb-comp-3"), dbc.Button("Ver métricas", id="otlb-btn-3", n_clicks=0)],
                 className="component-element"),
    ], className="components-container")
    ]),
    html.Br(),

    # Modal
    dbc.Modal(id="modal",
              children=[],
              size="xl",
              is_open=False,
              )
])

overview = html.Div(
    [
        html.Br(),
        html.Div(dbc.Card([
            html.Label("Seleccione una pesquería", className="labels"),
            fishery_selector
        ], className="card-box-overview-dropdown")),
        html.Br(),
        dbc.Card([
            html.H4("Datos históricos de la pesquería", className="h4"),
            html.Br(),
            dbc.Tabs(
                [
                    tab_creator("GRÁFICO", [html.Div(id="historic-charts"),
                                            html.Div(id="fig-citation"),
                                            html.Br(),
                                            html.Button(id="btn-image",
                                                        n_clicks=0,
                                                        className="download-button",
                                                        children=["Descargar imagen",
                                                                  dbc.Spinner(html.Div(id="loading-image"),
                                                                              color="white",
                                                                              spinner_style={"width": "2rem",
                                                                                             "height": "2rem",
                                                                                             "margin-top": "0px"})]),
                                            html.Div(id="download-container")
                                            ]),

                    tab_creator("TABLA", [html.Br(),
                                          html.Div(id="historic-table-header"),
                                          create_table("historic-table"),
                                          html.Br(),
                                          html.Div(id="table-citation"),
                                          html.Button(children=["Descargar tabla",
                                                                dbc.Spinner(html.Div(id="loading-table"),
                                                                            color="white",
                                                                            spinner_style={"width": "2rem",
                                                                                           "height": "2rem",
                                                                                           "margin-top": "0px"})],
                                                      id="btn-table", n_clicks=0, className="download-button"),
                                          html.Div(id="download-container-table")])
                ])
        ], className="card-box-overview"),

        html.Br(),
        dbc.Card([
            html.H4("Desempeño de la pesquería", className="h4"),
            html.Div(
                [
                    html.Label("Mostrar inputs o outputs:", className="labels"),
                    dcc.Dropdown(id="io-selection",
                                 options=[{"label": "Input", "value": "Input"},
                                          {"label": "Output", "value": "Output"},
                                          {"label": "Output TBL", "value": "Output-tbl"}],
                                 value="Input",
                                 clearable=False)
                ]
            ),
            html.Br(),
            dbc.Tabs([tab_creator("GRÁFICO", meters_layout),
                      tab_creator("TABLA", html.Div(id="main-meter-table"))])], className="card-box-overview")
    ])

# Metrics
controls = html.Div(
    [
        html.Label("Métricas por nivel", className="labels"),
        html.Br(),
        html.Br(),
        html.P("Seleccione las métricas para el gráfico"),
        dbc.Accordion(
            dbc.AccordionItem(
                title="Input",
                children=[
                    dbc.Accordion(
                        dbc.AccordionItem(
                            title="Componentes y dimensiones",
                            children=[
                                html.Label("Factores macro", className="lab-a"),
                                html.Label("Desempeño ambiental general", className="lab-b"),
                                create_metrics_checklist("Desempeño ambiental general",
                                                         "Índice de Desempeño Ambiental",
                                                         "m1"),

                                html.Br(),
                                html.Label("Factores ambientales exógenos", className="lab-b"),
                                create_metrics_checklist("Factores ambientales exógenos", "Enfermedades y patógenos",
                                                         "m2"),

                                html.Br(),
                                html.Label("Gobernanza", className="lab-b"),
                                create_metrics_checklist("Gobernanza", "Calidad de gobernanza", "m3"),

                                html.Br(),
                                html.Label("Condiciones económicas", className="lab-b"),
                                create_metrics_checklist("Condiciones económicas", "", "m4"),

                                html.Br(),
                                html.Label("Derechos de propiedad y responsabilidad", className="lab-a"),
                                html.Label("Derechos de acceso a la pesca", className="lab-b"),
                                create_metrics_checklist("Derechos de acceso a la pesca",
                                                         "Proporción de la captura manejada bajo acceso limitado",
                                                         "m5"),
                            ]
                        )
                    )
                ]
            ), start_collapsed=False
        ),
        html.Br(),
        dbc.Accordion(
            dbc.AccordionItem(
                title="Output",
                children=[]
            ), start_collapsed=True
        )
    ]
)
## Metrics body
metrics = html.Div(
    dbc.Row(
        [
            dbc.Col(dbc.Card(controls, body=True),
                    width=4,
                    style={"marginTop": "20px"},
                    id="controls-col",
                    className="card-box"),
            dbc.Col([
                html.Div(dbc.Card([
                    html.Label("Seleccione una pesquería", className="labels"),
                    fishery_selector_metrics
                ], className="card-box-metrics-dropdown")),
                dbc.Card(
                    dbc.Tabs([
                        tab_creator("GRÁFICO", html.Div(id="metrics-chart")),
                        tab_creator("TABLA", html.Div(id="metrics-table"))
                    ]), body=True, className="card-box-behind")],
                width=8,
                style={"marginTop": "20px"},
                id="charts-col")
        ], style={"display": "flex"}, id="controls"
    )
)

# Tabs
tab0 = tab_creator("MÉTODOS", methods)
tab1 = tab_creator("OVERVIEW", overview)
tab2 = tab_creator("MÉTRICAS", metrics)
tab3 = tab_creator("DATOS ABIERTOS", downloads)

tabs = dbc.Tabs([tab0, tab1, tab2, tab3])

# App layout
app.layout = html.Div(
    [
        header,
        tabs,
        html.Hr(),
        footer
    ], style={"width": "99%"}  # This avoids the horizontal scroll bar
)


@app.callback(
    # Charts & tables
    Output("historic-charts", "children"),
    Output("historic-table", "data"),
    Output("historic-table", "columns"),
    Output("historic-table-header", "children"),
    # Input layout
    Output("i-cont", "style"),
    Output("o-cont", "style"),
    Output("otlb-cont", "style"),
    # Output Meter
    Output("main-meter", "children"),
    # Output component contents
    Output("i-comp-1", "children"),
    Output("i-comp-2", "children"),
    Output("i-comp-3", "children"),
    Output("i-comp-4", "children"),
    Output("i-comp-5", "children"),
    Output("o-comp-1", "children"),
    Output("o-comp-2", "children"),
    Output("o-comp-3", "children"),
    Output("otlb-comp-1", "children"),
    Output("otlb-comp-2", "children"),
    Output("otlb-comp-3", "children"),
    # User selections
    Input("fishery-selection", "value"),
    Input("io-selection", "value")
)
def update_overview_layout(fishery_selection, input_selection):
    # Historical charts layout:
    df_a = data_h[data_h["Pesquería"] == fishery_selection]

    fig = historical_charts(df_a, fishery_selection)

    charts_layout = [dcc.Graph(figure=fig, config={'displayModeBar': False})]

    # Historical table layout:
    data_for_table = pd.pivot_table(data=df_a,
                                    values="value",
                                    index=["Pesquería", "type"],
                                    columns="year",
                                    aggfunc="sum")

    data_for_table.reset_index(inplace=True)
    columns_for_table = [{"name": i, "id": i} for i in data_for_table.columns]
    data_for_table = data_for_table.round(2).to_dict(orient="records")
    header = "Datos históricos para pesquería de " + fishery_selection.lower()
    year_min = df_a["year"].min()
    year_max = df_a["year"].max()
    header_for_table = [
        html.Label(header, className="labels"),
        html.P("Valores del periodo entre " + str(year_min) + " y " + str(year_max), style={"fontStyle": "italic"})]

    # Meters layout:
    df_b = data_fpi[data_fpi["Pesquería"] == fishery_selection].sort_values(by="Calificación", ascending=False)

    df_c = data_comp[data_comp["Pesquería"] == fishery_selection].sort_values(by="Calificación", ascending=False)
    # df_c.to_csv(r"data\data_comp.csv")

    # Components variables need to be instantiated before assignments in conditionals:
    i_comp_1 = []
    i_comp_2 = []
    i_comp_3 = []
    i_comp_4 = []
    i_comp_5 = []
    o_comp_1 = []
    o_comp_2 = []
    o_comp_3 = []
    otlb_comp_1 = []
    otlb_comp_2 = []
    otlb_comp_3 = []

    if input_selection == "Input":
        header_metric = "Input"
        type_meter_value = round(df_b[df_b["Tipo"] == "Input"]["Calificación"].mean(), 2)
        labels = df_c[df_c["Tipo"] == "Input"]["Componente"].dropna()
        values = df_c[df_c["Tipo"] == "Input"]["Calificación"].dropna()
        labels.reset_index(drop=True, inplace=True)
        values.reset_index(drop=True, inplace=True)

        layout = []

        for i in range(len(labels)):
            layout.append(html.Div([html.Label(labels[i]), create_secondary_meter(values[i], qA, qB, "meter-c")]))

        i_comp_1 = layout[0]
        i_comp_2 = layout[1]
        i_comp_3 = layout[2]
        i_comp_4 = layout[3]
        i_comp_5 = layout[4]

        i_cont = {"display": "block"}
        o_cont = {"display": "none"}
        otlb_cont = {"display": "none"}

    elif input_selection == "Output":
        header_metric = "Output"
        type_meter_value = round(df_b[df_b["Tipo"] == "Output"]["Calificación"].mean(), 2)
        labels = df_c[df_c["Tipo"] == "Output"]["Componente"].dropna()
        values = df_c[df_c["Tipo"] == "Output"]["Calificación"].dropna()
        labels.reset_index(drop=True, inplace=True)
        values.reset_index(drop=True, inplace=True)

        layout = []

        for i in range(len(labels)):
            layout.append(html.Div([html.Label(labels[i]), create_secondary_meter(values[i], qA, qB, "meter-c")]))

        o_comp_1 = layout[0]
        o_comp_2 = layout[1]
        o_comp_3 = layout[2]

        i_cont = {"display": "none"}
        o_cont = {"display": "block"}
        otlb_cont = {"display": "none"}

    else:
        header_metric = "Output TLB"
        type_meter_value = round(df_b[df_b["Tipo"] == "Output"]["Calificación"].mean(), 2)

        df_c_copy = df_c[df_c["Componente"].isin(["Economía", "Ecología", "Comunidad"])]

        labels = df_c_copy[df_c_copy["Tipo"] == "Output"]["Componente"].dropna()
        values = df_c_copy[df_c_copy["Tipo"] == "Output"]["Calificación"].dropna()
        labels.reset_index(drop=True, inplace=True)
        values.reset_index(drop=True, inplace=True)

        layout = []

        for i in range(len(labels)):
            layout.append(html.Div([html.Label(labels[i]), create_secondary_meter(values[i], qA, qB, "meter-c")]))

        otlb_comp_1 = layout[0]
        otlb_comp_2 = layout[1]
        otlb_comp_3 = layout[2]

        i_cont = {"display": "none"}
        o_cont = {"display": "none"}
        otlb_cont = {"display": "block"}

    main_meter_layout = (create_main_meter(header_metric, type_meter_value, qA, qB))

    return charts_layout, data_for_table, columns_for_table, header_for_table, i_cont, o_cont, otlb_cont, main_meter_layout, i_comp_1, i_comp_2, i_comp_3, i_comp_4, \
           i_comp_5, o_comp_1, o_comp_2, o_comp_3, otlb_comp_1, otlb_comp_2, otlb_comp_3


@app.callback(
    Output("modal", "is_open"),
    Output("modal", "children"),
    Output("i-btn-1", "n_clicks"),
    Output("i-btn-2", "n_clicks"),
    Output("i-btn-3", "n_clicks"),
    Output("i-btn-4", "n_clicks"),
    Output("i-btn-5", "n_clicks"),
    Output("o-btn-1", "n_clicks"),
    Output("o-btn-2", "n_clicks"),
    Output("o-btn-3", "n_clicks"),
    Output("otlb-btn-1", "n_clicks"),
    Output("otlb-btn-2", "n_clicks"),
    Output("otlb-btn-3", "n_clicks"),
    # Inputs
    Input("i-btn-1", "n_clicks"),
    Input("i-btn-2", "n_clicks"),
    Input("i-btn-3", "n_clicks"),
    Input("i-btn-4", "n_clicks"),
    Input("i-btn-5", "n_clicks"),
    Input("o-btn-1", "n_clicks"),
    Input("o-btn-2", "n_clicks"),
    Input("o-btn-3", "n_clicks"),
    Input("otlb-btn-1", "n_clicks"),
    Input("otlb-btn-2", "n_clicks"),
    Input("otlb-btn-3", "n_clicks"),
    Input("i-comp-1", "children"),
    Input("i-comp-2", "children"),
    Input("i-comp-3", "children"),
    Input("i-comp-4", "children"),
    Input("i-comp-5", "children"),
    Input("o-comp-1", "children"),
    Input("o-comp-2", "children"),
    Input("o-comp-3", "children"),
    Input("otlb-comp-1", "children"),
    Input("otlb-comp-2", "children"),
    Input("otlb-comp-3", "children"),
    Input("fishery-selection", "value")
)
def toggle_modal(i_btn_1, i_btn_2, i_btn_3, i_btn_4, i_btn_5, o_btn_1, o_btn_2, o_btn_3, otlb_btn_1, otlb_btn_2,
                 otlb_btn_3, i_comp_1, i_comp_2, i_comp_3, i_comp_4, i_comp_5, o_comp_1, o_comp_2, o_comp_3,
                 otlb_comp_1, otlb_comp_2, otlb_comp_3, fishery_selection):
    df = data_fpi[data_fpi["Pesquería"] == fishery_selection]

    modal_children = []
    open_modal = False

    if i_btn_1 > 0:
        component_name = i_comp_1["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        i_btn_1 = 0

    elif i_btn_2 > 0:
        component_name = i_comp_2["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        i_btn_2 = 0

    elif i_btn_3 > 0:
        component_name = i_comp_3["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        i_btn_3 = 0

    elif i_btn_4 > 0:
        component_name = i_comp_4["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        i_btn_4 = 0

    elif i_btn_5 > 0:
        component_name = i_comp_5["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        i_btn_5 = 0

    elif o_btn_1 > 0:
        component_name = o_comp_1["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        o_btn_1 = 0

    elif o_btn_2 > 0:
        component_name = o_comp_2["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        o_btn_2 = 0

    elif o_btn_3 > 0:
        component_name = o_comp_3["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        o_btn_3 = 0

    elif otlb_btn_1 > 0:
        component_name = otlb_comp_1["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        otlb_btn_1 = 0

    elif otlb_btn_2 > 0:
        component_name = otlb_comp_2["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        otlb_btn_2 = 0

    elif otlb_btn_3 > 0:
        component_name = otlb_comp_3["props"]["children"][0]["props"]["children"]
        modal_children, open_modal = create_modal_layout(df, component_name)
        otlb_btn_3 = 0

    return open_modal, modal_children, i_btn_1, i_btn_2, i_btn_3, i_btn_4, i_btn_5, o_btn_1, o_btn_2, o_btn_3, otlb_btn_1, otlb_btn_2, otlb_btn_3


@app.callback(
    Output("metrics-chart", "children"),
    Input("m1", "value"),
    Input("m2", "value"),
    Input("m3", "value"),
    Input("m4", "value"),
    Input("m5", "value"),
    Input("fishery-selection-metrics", "value")
)
def update_metrics_chart(m1, m2, m3, m4, m5, fishery_selection):
    pre_selections = [m1, m2, m3, m4, m5]
    selections = list(chain(*pre_selections))
    df = data_fpi[data_fpi["Pesquería"] == fishery_selection]

    df_unsorted = df[df["Métrica"].isin(selections)]
    df_plot = df_unsorted.sort_values(by="Calificación").dropna()
    # print(df_plot[["Métrica", "Calificación"]])

    fig = px.bar(x=df_plot["Calificación"],
                 y=df_plot["Métrica"],
                 color=df_plot["Dimensión"],
                 text_auto=True,
                 color_discrete_sequence=color_gradients)

    fig.update_layout(legend=dict(orientation="h"),
                      # plot_bgcolor="white",
                      legend_title_text="Dimensiones",
                      title="<b>Desempeño de las métricas de " + fishery_selection.lower() + "</b><br> Según filtros seleccionados",
                      title_font_family="Roboto",
                      title_font_color="#333f54")

    fig.update_yaxes(title="")
    fig.update_xaxes(title="")

    layout = html.Div([
        dcc.Graph(figure=fig, config={'displayModeBar': False})
    ])

    return layout


if __name__ == '__main__':
    app.run_server(debug=False)
