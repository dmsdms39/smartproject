import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction

from .graph import *
from flask import render_template, jsonify, request, redirect
from apps import app, db, ma
import pandas as pd
from datetime import datetime

# Read data
file_name = "apps/data/Tumbler_Factory_revision.xlsx"
DF_CSTDM = pd.read_excel('%s' %file_name, sheet_name = 'CUSTOMER_DEMAND', header=0, encoding='utf-8')
DF_EQPPLN = pd.read_excel('%s' %file_name, sheet_name = 'EQP_PLAN', header=0, encoding='utf-8')
DF_ANL = pd.read_excel('%s' %file_name, sheet_name = 'ANALYSIS', header=0, encoding='utf-8')

clinic_list = ["Process of product", "Operating rate", "State of Eqipment(test)"]

#table view name
view_list = []
for c in db.Model._decl_class_registry.values():
    if hasattr(c, '__tablename__'):
        view_list.append(c.__tablename__)

admit_list = eqp_list()

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Smart Factory Dashboard"),
            html.H3("Welcome to the Smart Factory Scheduling System"),
            html.Div(
                id="intro",
                children="Explore Process by products and operating ratio of eqipment.",
            ),
        ],
    )

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Chart"),
            dcc.Dropdown(
                id="clinic-select",
                options=[{"label": i, "value": i} for i in clinic_list],
                value=clinic_list[0],
            ),
            html.Br(),
            html.P("Select Table"),
            dcc.Dropdown(
                id="view-select",
                options=[{"label": i, "value": i} for i in view_list],
                value=view_list[0],
            ),
            html.Br(),
            html.P("Select Day of Manufacture"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=datetime(2019, 11, 8),
                end_date=datetime(2019, 11, 15),
                min_date_allowed=datetime(2019, 1, 1),
                max_date_allowed=datetime(2019, 12, 31),
                initial_visible_month=datetime(2019, 11, 1),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Eqipments"),
            dcc.Dropdown(
                id="admit-select",
                options=[{"label": i, "value": i} for i in admit_list],
                value=admit_list[:],
                multi=True,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )


def generate_patient_volume(start, end, clinic, hm_click, admit_type, reset):
    
    if clinic == "Process of product" :
        figure = process_product_fig(start, end, admit_type)
        
        print("ff들어옴")
        return figure

    elif clinic == "Operating rate" :
        figure = operating_ratio_fig(start, end, admit_type)
        print("go들어옴")
        return figure


def df_to_table(df):
    return html.Table(
    [html.Tr([html.Th(col) for col in df.columns])]
    + [
        html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
        for i in range(len(df))
    ]
)

def initialize_table():
    df = DF_ANL
    df1 = DF_CSTDM
    df2 = DF_EQPPLN
    return df_to_table(df2)

def make_input_tb_std_eqp():
    return [
        dcc.Dropdown(
            id="table_idx_eqp",
            options=[{"label": i, "value": i} for i in admit_list],
            value="eqp_id",
        ),
        dcc.Dropdown(
            id="table_idx_step",
            options=[{"label": i, "value": i} for i in ["PRESS","PAINT","FINISH"]],
            value="step_id",
        ),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    ]

def make_input_PlanDM():
    dcc.Input(id='input_test2', type='text', value ="")

# def make_input_Pl():



dashapp = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')


# 전체 
dashapp.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=dashapp.get_asset_url("plotly_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="patient_volume_card",
                    children=[
                        # html.B("Gantt Chart"),
                        # html.Hr(),
                        dcc.Graph(id="patient_volume_hm"),
                    ],
                ),
                # Patient Wait time by Department
                html.Div(
                    id="wait_time_card",
                    children=[
                        html.B("View Table"),
                        html.Hr(),
                        html.Div(id="leads_table", className="row pretty_container table", children=initialize_table()),
                        # html.Div(id="wait_time_table", children=initialize_table()),
                        html.Div(
                            id="leads_input",#children
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@dashapp.callback(
    Output("patient_volume_hm", "figure"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("clinic-select", "value"),
        Input("patient_volume_hm", "clickData"),
        Input("admit-select", "value"),
        Input("reset-btn", "n_clicks"),
    ],
)
def patient_volume_hm_callback(start, end, clinic, hm_click, admit_type, reset):
    # df = d
    start = start + " 00:00:00"
    end = end + " 00:00:00"
    
    reset = False
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn":
            reset = True  
    return generate_patient_volume(start, end, clinic, hm_click, admit_type, reset)

@dashapp.callback(
    Output("leads_input", "children"),
    [
        Input("view-select", "value"),
        Input("reset-btn", "n_clicks"),
    ],
)
def leads_input_callback(view, reset):
    if(view == "tb_std_eqp"):
        return make_input_tb_std_eqp()
    else:
        return make_input_PlanDM()


@app.route('/dashboard')
def render_dashboard():
    return redirect('/dash1')


# from werkzeug.wsgi import DispatcherMiddleware
# app2 = DispatcherMiddleware(app, {'/dash1': dashapp.server})