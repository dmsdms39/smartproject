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
# DF_EQPPLN["EQP_ID"] = DF_EQPPLN["EQP_ID"].fillna("Not Identified")#비어있다면 이걸로 채워라
admit_list = DF_EQPPLN["EQP_ID"].unique()
all_departments = DF_CSTDM["PROD_ID"].unique().tolist()

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
            html.P("Select Clinic"),
            dcc.Dropdown(
                id="clinic-select",
                options=[{"label": i, "value": i} for i in clinic_list],
                value=clinic_list[0],
            ),
            html.Br(),
            html.P("Select Check-In Time"),
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
            html.P("Select Admit Source"),
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

# def generate_table_row(id, style, col1, col2, col3):
#     """ Generate table rows.

#     :param id: The ID of table row.
#     :param style: Css style of this row.
#     :param col1 (dict): Defining id and children for the first column.
#     :param col2 (dict): Defining id and children for the second column.
#     :param col3 (dict): Defining id and children for the third column.
#     """

#     return html.Div(
#         id=id,
#         className="row table-row",
#         style=style,
#         children=[
#             html.Div(
#                 id=col1["id"],
#                 style={"display": "table", "height": "100%"},
#                 className="two columns row-department",
#                 children=col1["children"],
#             ),
#             html.Div(
#                 id=col2["id"],
#                 style={"textAlign": "center", "height": "100%"},
#                 className="five columns",
#                 children=col2["children"],
#             ),
#             html.Div(
#                 id=col3["id"],
#                 style={"textAlign": "center", "height": "100%"},
#                 className="five columns",
#                 children=col3["children"],
#             ),
#         ],
#     )

# def generate_table_row_helper(department):
#     """Helper function.

#     :param: department (string): Name of department.
#     :return: Table row.
#     """
#     return generate_table_row(
#         department,
#         {},
#         {"id": department + "_department", "children": html.B(department)},
#         {
#             "id": department + "wait_time",
            
#             "children": dcc.Graph(
#                 id=department + "_wait_time_graph",
#                 style={"height": "100%", "width": "100%"},
#                 className="wait_time_graph",
#                 config={
#                     "staticPlot": False,
#                     "editable": False,
#                     "displayModeBar": False,
#                 },
#                 figure={
#                     "layout": dict(
#                         margin=dict(l=0, r=0, b=0, t=0, pad=0),
#                         xaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         yaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         paper_bgcolor="rgba(0,0,0,0)",
#                         plot_bgcolor="rgba(0,0,0,0)",
#                     )
#                 },
#             ),
#         },
#         {
#             "id": department + "_patient_score",
#             "children": dcc.Graph(
#                 id=department + "_score_graph",
#                 style={"height": "100%", "width": "100%"},
#                 className="patient_score_graph",
#                 config={
#                     "staticPlot": False,
#                     "editable": False,
#                     "displayModeBar": False,
#                 },
#                 figure={
#                     "layout": dict(
#                         margin=dict(l=0, r=0, b=0, t=0, pad=0),
#                         xaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         yaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         paper_bgcolor="rgba(0,0,0,0)",
#                         plot_bgcolor="rgba(0,0,0,0)",
#                     )
#                 },
#             ),
#         },
#     )

def generate_patient_volume(start, end, clinic, hm_click, admit_type, reset):
    print(admit_type)
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
    return df_to_table(df)

# def initialize_table():
#     """
#     :return: empty table children. This is intialized for registering all figure ID at page load.
#     """

#     # header_row
#     header = [
#         generate_table_row(
#             "header",
#             {"height": "50px"},
#             {"id": "header_department", "children": html.B("Department")},
#             {"id": "header_wait_time_min", "children": html.B("Wait Time Minutes")},
#             {"id": "header_care_score", "children": html.B("Care Score")},
#         )
#     ]

#     # department_row
#     rows = [generate_table_row_helper(department) for department in all_departments]
#     header.extend(rows)
#     empty_table = header

#     return empty_table


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
        Input("date-picker-select", "end_date"),#쿼리에서 필터로 2019.몇부터 몇 조절하기
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


# @dashapp.callback(
#     Output("patient_volume_hm", "figure"),
#     [
#         Input("well-map", "selectedData"),
#         Input("ternary-map", "selectedData"),
#         Input("operator-select", "value"),
#     ],
# )

@app.route('/dashboard')
def render_dashboard():
    return redirect('/dash1')


# from werkzeug.wsgi import DispatcherMiddleware
# app2 = DispatcherMiddleware(app, {'/dash1': dashapp.server})