from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# -----------------Read excel files and transpose columns and rows-----------
df = pd.read_excel("path/credits.xlsx", index_col=0)
df1 = df.T

df_kred = pd.read_excel("path/consumtie_en_hyp_kred.xlsx", index_col=0)
df_kred2 = df_kred.T

df_werk = pd.read_excel("path/werkgelegenheid.xlsx", index_col=0)
fig = px.pie(data_frame=df_werk, values=df_werk['  2022Q1'], names=df_werk.index)

df_vertrouwen = pd.read_excel("path/vooruitzicht.xlsx", index_col=0)
df_vertrouwen1 = df_vertrouwen.T

df_inflatie = pd.read_excel("path/inflatie.xlsx", index_col=0)
df_inflatie1 = df_inflatie.T

# -----------------------create chart vertrouwen------------------------------
fig2 = px.line(data_frame=df_vertrouwen1[1:],
               x=df_vertrouwen1.index[1:],
               y=df_vertrouwen1.columns[1:],
               labels=dict(x='Periode', y='Waarde'))

fig3 = px.line(data_frame=df_inflatie1,
               x=df_inflatie.index,
               y=df_inflatie1.loc['Inflatie'],
               labels=dict(x='Periode', y='Waarde'))

# -----------------------Initialize app and layout------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Financieel Dashboard - Economische situatie Belgie", style={"text-align": 'center'}),

    html.Hr(),
    html.Br(),
    html.H4("Inflatie", style={'text-align': 'center'}),
    dcc.Graph(id='graph_inflatie', figure=fig3, style={'padding-left': '175px', 'padding-right': '175px'}),

    dbc.Row([
        dbc.Col(html.H4("Kredieten sectoren"), width={'size': 3, 'offset': 2},),
        dbc.Col(html.H4("Kredieten consumenten"), width={'size': 3, 'offset': 2},)
    ]),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id="my-dropdown", multi=False,
            options=[{'label': x, 'value': x} for x in df1],
            value="Landbouw, bosbouw en visserij"),
            width={'size': 3, 'offset': 2}
            ),

        dbc.Col(dcc.Dropdown(
            id="my-dropdown_kred", multi=False,
            options=[{'label': x, 'value': x} for x in df_kred2],
            alue="Aantal uitstaande kredieten"), width={'size': 3, 'offset': 2}
            ),
        ],
    ),

    dbc.Row([
        dbc.Col(
            dcc.Graph(
                    id='graph',
                    figure={}
                ),
            width=8,
            lg={'size': 5,  "offset": 1}
        ),

        dbc.Col(
            dcc.Graph(
                id='graph_kred',
                figure={}
            ),
            width=8,
            lg={'size': 5,  "offset": 0}
        )],

    ),
    html.Br(),
    html.Br(),
    html.H4("Werkgelegenheid", style={'textAlign': 'center'}),
    dcc.Graph(id='pie-graph', figure=fig),
    html.H4("Consumentenvertrouwen", style={'textAlign': 'center'}),
    dcc.Graph(id='mul-chart', figure=fig2, style={'padding-left': '100px'})

])


# -----------------------Callbacks and updates------------------------------
@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='my-dropdown', component_property='value')],
    prevent_initial_call=False
)
def update_graph(val):
    if len(val) > 0:
        fig = px.line(df1, x=df1.index[0:], y=df1[val],  labels=dict(x='Periode', y='Aantal kredieten'))
        fig.update_layout(transition_duration=500, xaxis=dict(showticklabels=True))
        return fig
    elif len(val) == 0:
        raise PreventUpdate


@app.callback(
    Output(component_id='graph_kred', component_property='figure'),
    [Input(component_id='my-dropdown_kred', component_property='value')],
    prevent_initial_call=False)
def update_graph_kred(val):
    if len(val) > 0:
        fig2 = px.line(
            df_kred2,
            x=df_kred2.index[0:],
            y=df_kred2[val],
            labels=dict(x='Periode', y='Aantal uitstaande kredieten'))
        fig2.update_layout(transition_duration=500)
        return fig2
    elif len(val) == 0:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)


