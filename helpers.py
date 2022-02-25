import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, State, html, dash_table
import dash
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from itertools import chain

# Data loading
data_fpi = pd.read_csv("https://raw.githubusercontent.com/juancizurietaj/opendata/main/FPI.csv")
data_h = pd.read_csv("https://raw.githubusercontent.com/juancizurietaj/opendata/main/Historical_data.csv")

methods_text_1 = "¿De dónde provienen estos datos?"
methods_text_2 = 'Los FPI están diseñados para evaluar el éxito en la generación de riqueza de los órganos de gestión, principalmente a nivel de consejo de gestión nacional o regional, y pueden incluir múltiples especies, buscando lograr un equilibrio entre el alcance de la autoridad de gestión y el tamaño económico de la pesquería evaluada. .Las medidas individuales están codificadas en niveles (1 a 5) y están diseñadas para que sean fáciles de recopilar y puntuar en una amplia gama de pesquerías. Se basan en un conjunto básico de datos que debería estar disponible en todas las pesquerías importantes (p. ej., volúmenes y precios) y en la evaluación de expertos de los niveles de indicadores cualitativos; no requiere recopilación de datos primarios. Cada uno de los insumos y productos se agrupa en categorías amplias que se dividen en dimensiones específicas de productos o insumos de riqueza, que se reflejan en varias medidas específicas. Si bien tales medidas multidimensionales se prestan a la agregación y clasificación ponderada, se prevé que los FPI respalden principalmente el análisis que vincula la creación de riqueza con insumos específicos. Por lo tanto, los puntajes de las medidas deben proporcionarse en cada dimensión clave y ponderarse por igual para obtener puntajes generales y de componentes. La clasificación resultante destacará las pesquerías con un desempeño particularmente fuerte y débil y llamará la atención sobre los puntos en común y las diferencias entre sus puntajes de entrada. Los usuarios individuales que deseen clasificar países para otros fines, con diferentes énfasis en los componentes o dimensiones clave de los componentes, pueden aplicar diferentes ponderaciones a cada dimensión.'
methods_text_3 = "La figura debajo muestra el esquema de los indicadores de desempeño. Hay Inputs y Outputs, cada una con componentes, dimensiones y finalmente métricas. Las caliificaciones son obtenidas desde el promedio de las métricas."

# Selectors
fishery_selector = dcc.Dropdown(id="fishery-selection",
                                options=[{"label": "Langosta", "value": "Langosta"},
                                         {"label": "Pepino de mar", "value": "Pepino de mar"},
                                         {"label": "Pesca de altura", "value": "Pesca de altura"}],
                                value="Langosta",
                                clearable=False)

fishery_selector_metrics = dcc.Dropdown(id="fishery-selection-metrics",
                                        options=[{"label": "Langosta", "value": "Langosta"},
                                                 {"label": "Pepino de mar", "value": "Pepino de mar"},
                                                 {"label": "Pesca de altura", "value": "Pesca de altura"}],
                                        value="Langosta",
                                        clearable=False)

# Colors
color_gradients = ["rgb(57, 73, 155)", "rgb(87, 72, 157)", "rgb(112, 70, 157)", "rgb(134, 68, 156)",
                   "rgb(155, 65, 151)", "rgb(174, 62, 146)", "rgb(191, 59, 138)", "rgb(206, 59, 129)",
                   "rgb(219, 61, 118)", "rgb(229, 66, 107)", "rgb(237, 74, 95)", "rgb(243, 84, 83)", "rgb(246, 96, 70)",
                   "rgb(246, 109, 56)", "rgb(244, 123, 41)"]

# Header
header = html.Div(
    [
        html.Img(src=r"./assets/de_logo.png",
                 width="130px",
                 style={'display': 'inline-block', "padding": "10px"}),
        html.H4("Indicadores de desempeño pesquero",
                style={'display': 'inline-block', "color": "white", 'marginLeft': 30, "bottom": 0})
    ], style={"background": "#333f54", 'display': 'inline-block', "width": "100%"}
)

# Footer
footer = html.Div(
    [
        html.Div(
            [
                html.Img(src="assets/BID.png",
                         height="60px",
                         style={"padding": "0px 15px", "display": "inline-block", "margin-top": "0px"}),
                html.P("Descripción del proyecto donde se enmarcan los datos, créditos a instituciones participantes.",
                       className="footer-grant")
            ]
        ),
        html.Div(
            [
                html.Img(src="assets/edit_dpng_fcd.png",
                         height="85px",
                         style={"padding": "0px 15px", "display": "inline-block", "margin-top": "0px"}),
                html.P("©Dirección del Parque Nacional Galápagos y Fundación Charles Darwin", className="footer-fcd"),
                html.P("Creado por el Departamento de Tecnologías, Información, Investigación y Desarrollo (TIID)",
                       className="footer-tiid")
            ], style={"text-align": "right"}
        )
    ], style={"display": "flex", "justify-content": "space-between", "padding": ""}
)


def create_download_cards(iconA, labelA, textA, buttonA, iconB, textB, labelB, buttonB, iconC, labelC, textC, buttonC):
    downloads = html.Div(
        [
            dbc.Card([html.Div(html.Img(src=iconA, height=50), className="downloads-card-item"),
                      html.Div(html.Label(labelA, className="labels"),
                               className="downloads-card-item"),
                      html.Div(html.P(textA),
                               className="downloads-card-item"),
                      html.Div(dbc.Button(buttonA, size="m"), className="downloads-card-item")],
                     body=True, className="downloads-card-container"),
            dbc.Card([html.Div(html.Img(src=iconB, height=50), className="downloads-card-item"),
                      html.Div(html.Label(labelB, className="labels"),
                               className="downloads-card-item"),
                      html.Div(html.P(textB),
                               className="downloads-card-item"),
                      html.Div(dbc.Button(buttonB, size="m"), className="downloads-card-item")],
                     body=True, className="downloads-card-container"),
            dbc.Card([html.Div(html.Img(src=iconC, height=50), className="downloads-card-item"),
                      html.Div(html.Label(labelC, className="labels"),
                               className="downloads-card-item"),
                      html.Div(html.P(textC),
                               className="downloads-card-item"),
                      html.Div(dbc.Button(buttonC, size="m"), className="downloads-card-item")],
                     body=True, className="downloads-card-container")
        ], className="downloads-container"
    )

    return downloads


def create_example_methods_fig():
    example_df = pd.DataFrame({"Tipo": ["Output", "Input", "Output", "Input"],
                               "Componente": ["Componente  C", "Componente A", "Componente D", "Componente B"],
                               "Dimensión": ["Dimensión C", "Dimensión A", "Dimensión D", "Dimensión B"],
                               "Métrica": ["Métrica 3", "Métrica 1", "Métrica 4", "Métrica 2"],
                               "Values": [1, 1, 1, 1]})

    fig = px.treemap(example_df,
                     path=["Tipo", "Componente", "Dimensión", "Métrica"],
                     values="Values",
                     color="Tipo",
                     color_discrete_map={"(?)": "white", "Output": "#ecf3f6", "Input": "#f6f3f6"})
    fig.update_layout(plot_bgcolor="#ecf3f6",
                      hoverlabel_namelength=35,
                      title_font_family="Roboto",
                      title_font_color="#333f54"
                      )

    fig.update_traces(hovertemplate="<b>%{label}</b> <br>Métricas:%{value} <br>Ubicación:%{id}")

    return fig


def create_methods_fig(df, path_array, values, color):
    fig = px.treemap(df,
                     path=path_array,
                     values=values,
                     color=color,
                     color_discrete_map={"(?)": "white", "Output": color_gradients[0], "Input": color_gradients[-1]},
                     maxdepth=3)
    fig.update_layout(
        title="<b>Esquema de la herramienta de evaluación</b><br>Clic sobre los elementos para mostrar más",
        plot_bgcolor="#ecf3f6",
        hoverlabel_namelength=35,
        title_font_family="Roboto",
        title_font_color="#333f54"
    )

    fig.update_traces(hovertemplate="<b>%{label}</b> <br>Métricas:%{value} <br>Ubicación:%{id}")

    return fig


# Helper functions
def tab_creator(label_name, content):
    tab = dbc.Tab(content, label=label_name,
                  tab_style={'backgroundColor': '#e9ebef'},
                  active_label_style={'color': '#333f54', 'fontWeight': 'bold'},
                  label_style={'color': 'gray'})
    return tab


def historical_charts(df, column):
    df = df[df["Pesquería"] == column]

    unique_indicators = df["type"].dropna().unique()

    rows = int((len(unique_indicators) % 2 + len(unique_indicators)) / 2)

    fishery_selection = df["Pesquería"].unique()

    header = "<b>Datos históricos para pesquería de " + fishery_selection[0].lower() + "</b><br>"
    year_min = df["year"].min()
    year_max = df["year"].max()
    description = "<i>Valores del periodo entre " + str(year_min) + " y " + str(year_max) + "</i>"

    fig = make_subplots(rows=rows, cols=2, subplot_titles=unique_indicators)

    for i in range(len(unique_indicators)):
        col_location = i % 2 + 1
        if i < 2:
            row_location = 1
        else:
            row_location = 2

        x = list(df["year"][df["type"] == unique_indicators[i]])
        y = list(df["value"][df["type"] == unique_indicators[i]])

        fig.add_trace(go.Scatter(x=x, y=y), row=row_location, col=col_location)

    fig.update_traces(line={"shape": "spline",
                            "color": color_gradients[0]},
                      showlegend=False)

    fig.update_layout(title=(header+description),
                      plot_bgcolor="white",
                      hovermode="x",
                      title_font_family="Roboto",
                      title_font_color="#333f54")

    return fig


def create_table_elements(df, values, array_for_index, columns, agg_func, metric, year_min, year_max):
    df = pd.pivot_table(data=df,
                        values=values,
                        index=array_for_index,
                        columns=columns,
                        aggfunc=agg_func)

    df.reset_index(inplace=True)
    data_for_table = df.round(2).to_dict(orient="records")
    columns_for_table = [{"name": i, "id": i} for i in df.columns]

    if len(array_for_index) > 1:
        header = metric + " por " + array_for_index[0] + " y por " + array_for_index[1]
    else:
        header = metric + " por " + array_for_index[0]

    header_for_table = [
        html.Label(header, className="labels"),
        html.P("Valores del periodo entre " + year_min + " y " + year_max, style={"fontStyle": "italic"})]

    return data_for_table, columns_for_table, header_for_table


def create_table(_id):
    table = dash_table.DataTable(
        id=_id,
        data=[],
        sort_action='native',
        style_table={'overflowX': 'auto'},
        style_header={
            "backgroundColor": "#333f54",
            "fontWeight": "bold",
            "color": "white",
        },
        style_cell={'textAlign': 'center',
                    'font-family': 'sans-serif',
                    'fontSize': 12},
        style_data_conditional=[
            {
                "if": {"state": "selected"},
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid #333f54",
            }
        ]
    )

    return table


# Metrics menu functions
def create_metrics_checklist(dimension, value, _id):
    options = dbc.Checklist(id=_id,
                            options=[{"label": i, 'value': i} for i in
                                     data_fpi[data_fpi["Dimensión"] == dimension]["Métrica"].unique()],
                            value=[value],
                            className="lab-c")
    return options


# Layouts functions
# Components layout data
df = data_fpi.groupby(["Tipo", "Componente", "Pesquería"])["Calificación"].mean()
df = pd.DataFrame(df)
df.reset_index(col_level=1, inplace=True)

df2 = data_fpi[data_fpi["Tipo"] == "Output"].groupby(["Tipo", "Categoría TLB", "Pesquería"])["Calificación"].mean()
df2 = pd.DataFrame(df2)
df2.reset_index(col_level=1, inplace=True)
df2.columns = df.columns
data_comp = pd.concat([df, df2], ignore_index=True)
data_comp["Calificación"] = round(data_comp["Calificación"], 2)
data_comp = data_comp.sort_values(by="Calificación", ascending=False)
data_comp.reset_index(inplace=True)

# Meter brakes
qA = 2
qB = 3.5


def create_component_layout(labels, values, index):
    layout = html.Div([html.Label(labels[index], className="component-labels"),
                       create_secondary_meter(values[index], qA, qB, "meter-c")],
                      className="component-element")

    return layout


def create_component_button(button_id):
    button = dbc.Button("Ver métricas",
                        outline=True,
                        color="primary",
                        size="sm",
                        n_clicks=0,
                        id=button_id)

    return button


## This function creates the metrics layout inside the modal (metrics headers and meters)
def create_metrics(df, dimension):
    df = df[df["Dimensión"] == dimension].sort_values(by="Calificación", ascending=False)
    df.reset_index(inplace=True)
    layout = []
    for i in range(len(df)):
        layout.append(html.Div([html.Label(df["Métrica"][i], className="metrics-labels"),
                                create_secondary_meter(df["Calificación"][i], qA, qB, "meter-c")
                                ], className="metrics-container"))
    return layout


## This function creates the modal layout (only dimensions divs and headers)
def create_dimensions(df, component):
    if component in ["Comunidad", "Ecología", "Economía"]:
        df = df[df["Categoría TLB"] == component]
    else:
        df = df[df["Componente"] == component]

    df_dimensions = df.groupby(["Dimensión"])["Calificación"].mean().dropna()
    df_dimensions = pd.DataFrame(df_dimensions)
    df_dimensions.reset_index(col_level=1, inplace=True)

    df_metrics = df.groupby(["Componente", "Dimensión", "Métrica"])["Calificación"].mean().dropna()
    df_metrics = pd.DataFrame(df_metrics)
    df_metrics.reset_index(col_level=1, inplace=True)

    layout_dimensions = []
    layout_metrics = []

    for i in range(len(df_dimensions.index)):
        layout_dimensions.append(dbc.Card([
            html.Div([
                html.Label("Dimensión: " + df_dimensions["Dimensión"][i], className="meter-header"),
                html.P("Calificación promedio de las métricas:", className="threshold-text"),
                create_secondary_meter(round(df_dimensions["Calificación"][i], 2), qA, qB, "meter-c-big")
            ], className="metrics-container-header"),
            html.Br(),
            html.P("Métricas:", className="component-labels"),
            html.Div(create_metrics(df, df_dimensions["Dimensión"][i]))
        ], className="card-container"))

    return layout_dimensions


## This function creates the modal header and body (references to create_dimensions for contents)
def create_modal_layout(df, component):
    modal_children = [dbc.ModalHeader(dbc.ModalTitle("Dimensiones y métricas para el componente: '" + component + "'")),
                      dbc.ModalBody(html.Div(create_dimensions(df, component), className="meter-container"))]
    open_modal = True

    return modal_children, open_modal


# Meter functions

## This function creates the main meter with bottom legend
def create_main_meter(variable, value, qA, qB):
    if value < qA:
        color = "danger"
    elif value < qB:
        color = "warning"
    else:
        color = "success"

    layout = html.Div([
        html.Label("Calificación promedio de " + variable,
                   className="meter-header"),
        dbc.Progress(label=str(value), min=0, max=5, value=value,
                     color=color,
                     className="meter-a"),
        html.P("¿Cómo leer esta cifra?", className="threshold-text"),
        dbc.Progress(
            [
                dbc.Progress(value=(qA / 5 * 100),
                             color="danger",
                             bar=True,
                             label="0 a " + str(qA) + ": bajo"),
                dbc.Progress(value=((qB - qA) / 5 * 100),
                             color="warning",
                             bar=True,
                             label=str(round(qA + 0.1, 2)) + " a " + str(qB) + ": medio"),
                dbc.Progress(value=((5 - qB) / 5 * 100),
                             color="success",
                             bar=True,
                             label=str(round(qB + 0.1, 2)) + " a 5: medio"),
            ], className="meter-b")
    ], className="meter-container")

    return layout


## This function creates individual meters (no legend)
def create_secondary_meter(value, qA, qB, meter_classname):
    if value < qA:
        color = "danger"
    elif value < qB:
        color = "warning"
    else:
        color = "success"

    meter = html.Div([
        dbc.Progress(label=str(value), min=0, max=5, value=value,
                     color=color,
                     className=meter_classname)
    ], className="meter-container")
    return meter


iconA = "assets/icon_metadata.png"
labelA = "Descarga de metadatos"
textA = "Los metadatos son 'datos acerca de los datos'. Describen el contenido, la calidad, el formato y otras características de este conjuntos de los datos. También incluyen las formas de citación, créditos y licencias de los datos."
buttonA = "Descargar metadatos"

iconB = "assets/icon_dix.png"
labelB = "Descarga de diccionario de datos"
textB = "Es el significado de cada una de los 'campos' o 'variables' del conjunto de datos. Muestra el significado de cada encabezado del conjunto de datos y la descripción de los datos que contiene."
buttonB = "Descargar diccionario de datos"

iconC = "assets/icon_data.png"
labelC = "Descarga los datos abiertos"
textC = "Los datos abiertos son el conjunto de datos detrás de este Data Explorer. Tienen un formato tabular (.csv) y muestran los datos en su forma más desagregada."
buttonC = "Descargar los datos abiertos"

downloads = create_download_cards(iconA, labelA, textA, buttonA, iconB, textB, labelB, buttonB, iconC, labelC, textC,
                                  buttonC)
