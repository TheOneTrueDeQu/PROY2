import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Cargar datos
df = pd.read_csv("C:/Users/Nicolas/Downloads/data_clean.csv")

def create_app():
    # Crear la aplicación Dash
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Contenido del tablero
    app.layout = html.Div([
        dbc.Row([
            dbc.Col(html.H2("Análisis de Clientes"), width=12),
        ]),
        
        dbc.Row([
            # Selector para la característica en el gráfico de comparación
            dbc.Col([
                html.H4("Seleccione la característica para comparar entre clientes que compraron y no compraron"),
                dcc.Dropdown(
                    id='feature-dropdown',
                    options=[
                        {'label': 'Balance', 'value': 'balance'},
                        {'label': 'Edad', 'value': 'age'},
                        {'label': 'Duración de la Llamada', 'value': 'duration'},
                    ],
                    value='balance'  # Valor inicial
                ),
                dcc.Graph(id='comparison-graph')
            ], width=6),

            # Gráfico de distribución con opciones seleccionables
            dbc.Col([
                html.H4("Distribución de características seleccionadas"),
                dcc.Dropdown(
                    id='x-axis-dropdown',
                    options=[
                        {'label': 'Ocupación', 'value': 'job'},
                        {'label': 'Estado Civil', 'value': 'marital'},
                        {'label': 'Educación', 'value': 'education'},
                        {'label': 'Balance', 'value': 'balance'},
                    ],
                    placeholder="Seleccione una característica para el eje X"
                ),
                dcc.Dropdown(
                    id='color-dropdown',
                    options=[
                        {'label': 'Ocupación', 'value': 'job'},
                        {'label': 'Estado Civil', 'value': 'marital'},
                        {'label': 'Educación', 'value': 'education'},
                        {'label': 'Balance', 'value': 'balance'},
                    ],
                    placeholder="Seleccione una característica para el color"
                ),
                dcc.Graph(id='distribution-graph')
            ], width=6),
        ]),

        dbc.Row([
            # Filtro para seleccionar segmentos
            dbc.Col([
                html.H4("Segmentación de Clientes"),
                dcc.Dropdown(
                    id='segment-filter',
                    options=[
                        {'label': 'Ocupación', 'value': 'job'},
                        {'label': 'Estado Civil', 'value': 'marital'},
                        {'label': 'Nivel Educativo', 'value': 'education'},
                        {'label': 'Balance', 'value': 'balance'}
                    ],
                    placeholder="Seleccione un segmento"
                ),
                dcc.Graph(id='segment-graph')
            ], width=12)
        ])
    ])

    # Callback para actualizar los gráficos
    @app.callback(
        [Output('comparison-graph', 'figure'),
         Output('distribution-graph', 'figure'),
         Output('segment-graph', 'figure')],
        [Input('feature-dropdown', 'value'),
         Input('x-axis-dropdown', 'value'),
         Input('color-dropdown', 'value'),
         Input('segment-filter', 'value')]
    )
    def update_graphs(selected_feature, x_feature, color_feature, segment):
        # Primer gráfico: Comparación entre clientes que compraron y no compraron
        fig_comparison = px.violin(
            df, y=selected_feature, x="y", color="y",
            box=True, points="all",
            title=f"Comparación de {selected_feature} entre clientes que compraron y no compraron",
            labels={'y': 'Compra (1: Sí, 0: No)', selected_feature: selected_feature.capitalize()}
        )

        # Segundo gráfico: Distribución con características seleccionadas
        if x_feature and color_feature:
            fig_distribution = px.histogram(
                df, x=x_feature, color=color_feature,
                title=f"Distribución de {x_feature.capitalize()} y {color_feature.capitalize()}",
                labels={x_feature: x_feature.capitalize(), color_feature: color_feature.capitalize()}
            )
        else:
            fig_distribution = px.histogram(
                pd.DataFrame({'x': [], 'y': []}), x="x", y="y",
                title="Seleccione ambas características para visualizar la distribución"
            )

        # Tercer gráfico: Segmentación de clientes según el filtro seleccionado
        if segment:
            if segment == 'balance':
                fig_segment = px.histogram(
                    df, x="balance", color="y",
                    title="Distribución de probabilidad de compra por balance",
                    labels={'y': 'Compra (1: Sí, 0: No)', 'balance': 'Balance'}
                )
            else:
                fig_segment = px.histogram(
                    df, x=segment, color="y",
                    title=f"Distribución de probabilidad de compra por {segment}",
                    labels={segment: segment.capitalize(), 'y': 'Compra (1: Sí, 0: No)'}
                )
        else:
            fig_segment = px.histogram(
                pd.DataFrame({'x': [], 'y': []}), x="x", y="y",
                title="Seleccione un segmento para visualizar la probabilidad de compra"
            )

        return fig_comparison, fig_distribution, fig_segment

    return app

# Ejecutar la aplicación
app = create_app()

if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=8050)
