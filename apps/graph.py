from .models import *
from apps import db
from sqlalchemy import or_
from datetime import datetime
import json
import pandas as pd
import plotly
import plotly.figure_factory as ff
import plotly.graph_objects as go
import collections

#eqp 리스트
def eqp_list():
    eqp = db.session.query(StdEQP.id).filter().order_by("id").all()
    listeqp = []
    for i in eqp:
        listeqp.append(i[0])
    return listeqp

##간트차트 그래프
def process_product():
    planeqp = db.session.query(PlanEQP).filter()
    df1 = pd.read_sql(planeqp.statement, planeqp.session.bind)
    df1.rename(columns = {"start_t":"Start", "end_t":"Finish", "id":"Task"}, inplace = True)

    df1=df1.to_dict('records')
    for i in df1:
        i['Task'] = StdLineEQP.query.filter_by(id = i['line_eqp_id']).first().eqp_id
    
    fig = ff.create_gantt(df1, index_col='prod_id', title='Process by products', group_tasks=True,
                        show_colorbar=True, bar_width=0.2, showgrid_x=True, showgrid_y=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def process_product_fig(start, end, admit_type):
    
    line_eqp_id = []
    for eqp_id in admit_type:
        line_eqp_id.append(StdLineEQP.query.filter_by(eqp_id = eqp_id).first().id)

    planeqp = db.session.query(PlanEQP).filter(
        PlanEQP.start_t > start, 
        PlanEQP.start_t < end,
        PlanEQP.line_eqp_id.in_(line_eqp_id))

    df1 = pd.read_sql(planeqp.statement, planeqp.session.bind)
    df1.rename(columns = {"start_t":"Start", "end_t":"Finish", "id":"Task"}, inplace = True)
  
    df1=df1.to_dict('records')
    for i in df1:
        i['Task'] = StdLineEQP.query.filter_by(id = i['line_eqp_id']).first().eqp_id
    # print(df1)
    fig = ff.create_gantt(df1, index_col='prod_id', title="Process of product", group_tasks=True,
                        show_colorbar=True, bar_width=0.2, showgrid_x=True, showgrid_y=True, width=1080, height=600)

    return fig

def operating_ratio_fig(start, end, admit_type):
    line_eqp_id = []
    for eqp_id in admit_type:
        line_eqp_id.append(StdLineEQP.query.filter_by(eqp_id = eqp_id).first().id)

    vewres = db.session.query(ViewRes).filter(
        ViewRes.t_day > start, 
        ViewRes.t_day < end,
        ViewRes.line_eqp_id.in_(line_eqp_id))
    df2 = pd.read_sql(vewres.statement, vewres.session.bind)
    df2.sort_values(by=['t_day'], axis=0, inplace=True)

    eqp_operate = {}
    for idx, dr in df2.iterrows():
        id = StdLineEQP.query.filter_by(id = dr['line_eqp_id']).first().eqp_id
        if id not in eqp_operate:
            eqp_operate[id]=[]
        eqp_operate[id].append(dr["busy"])
    
    target_d = []
    for date in df2['t_day'].unique():
        # numpy datetime64를 string으로,,
        # date = pd.to_datetime(str(date))
        # target_d.append(date.strftime("%Y%m%d"))
        
        # numpy datetime64를 timestamp로,,
        target_d.append(pd.to_datetime(date))
    eqp_operate = collections.OrderedDict(sorted(eqp_operate.items()))

    fig = go.Figure()

    for n in eqp_operate:
        fig.add_trace(go.Scatter(x=target_d, y=eqp_operate[n], name=n, 
        line=dict(color='%s' % ('firebrick' if 'EQP1' in n else ('BLUE' if 'EQP2' in n else 'GREEN')), 
        width=3, dash='%s' % ('solid' if n[-1:] == '1' else ('dot' if n[-1:]== '2' else 'dash')))))
    ##color list={'firebrick'......}, dash style 리스트로 만들어서 나머지 n일때마다 다음 보기 선택
        
    fig.update_layout(title='Operating rate by Equipments', xaxis_title='Date', yaxis_title='Operating Rate(%)')


    return fig

## 가동률그래프 index2.html
def operating_ratio():
    vewres = db.session.query(ViewRes).filter()
    df2 = pd.read_sql(vewres.statement, vewres.session.bind)
    df2.sort_values(by=['t_day'], axis=0, inplace=True)

    eqp_operate = {}
    for idx, dr in df2.iterrows():
        id = StdLineEQP.query.filter_by(id = dr['line_eqp_id']).first().eqp_id
        if id not in eqp_operate:
            eqp_operate[id]=[]
        eqp_operate[id].append(dr["busy"])
    
    target_d = []
    for date in df2['t_day'].unique():
        # numpy datetime64를 string으로,,
        # date = pd.to_datetime(str(date))
        # target_d.append(date.strftime("%Y%m%d"))
        
        # numpy datetime64를 timestamp로,,
        target_d.append(pd.to_datetime(date))
    eqp_operate = collections.OrderedDict(sorted(eqp_operate.items()))

    fig = go.Figure()

    for n in eqp_operate:
        fig.add_trace(go.Scatter(x=target_d, y=eqp_operate[n], name=n, 
        line=dict(color='%s' % ('firebrick' if 'EQP1' in n else ('BLUE' if 'EQP2' in n else 'GREEN')), 
        width=3, dash='%s' % ('solid' if n[-1:] == '1' else ('dot' if n[-1:]== '2' else 'dash')))))
    ##color list={'firebrick'......}, dash style 리스트로 만들어서 나머지 n일때마다 다음 보기 선택
        
    fig.update_layout(title='Operating rate by Equipments', xaxis_title='Date', yaxis_title='Operating Rate(%)')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

