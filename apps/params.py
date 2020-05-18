from .models import *
from apps import db
import pandas as pd

def uploadOne(clss, df):
    if not clss.query.all():
        for i in df :
            step_obj = clss(id = i)
            db.session.add(step_obj)
        db.session.commit()

def uploadStdEQP(df):
    if not StdEQP.query.all():
        for idx, eqp in df.iterrows():
            eqp_obj = StdEQP(id=eqp['EQP_ID'], step_id=eqp['STEP_ID'])
            db.session.add(eqp_obj)
        db.session.commit()
    
def uploadStdLineEQP(df):
    if not StdLineEQP.query.all():
        for idx, line_eqp in df.iterrows():
            line_eqp_obj = StdEQP(eqp_id=line_eqp['EQP_ID'], line_id=line_eqp['LINE_ID'])
            db.session.add(line_eqp_obj)
        db.session.commit()

def uploadPlanDM(df):
    if not PlanDM.query.all():
        for idx, dm in df.iterrows():
            dm_obj = PlanDM(id=dm['DM_ID'], due_d=dm['DUE_DATE'], qty=dm["DM_QTY"], cst_id=dm["CST_ID"], prod_id=dm["PROD_ID"])
            db.session.add(dm_obj)
        db.session.commit()
    
def uploadViewRes(df):
    if not ViewRes.query.all():
        for idx, res in df.iterrows():
            res_obj = ViewRes(line_eqp_id=StdLineEQP.query.filter_by(eqp_id = res['EQP_ID']).first().id, t_day=res['TARGET_DATE'], setup=res["SETUP"], busy=res["BUSY"], idle=res["IDLE"], pm=res["PM"], down=res["DOWN"])
            db.session.add(res_obj)
        db.session.commit()
    
def uploadPlanEQP(df):
    if not PlanEQP.query.all():
        for idx, plneqp in df.iterrows():
            plneqp_obj = PlanEQP(line_eqp_id=StdLineEQP.query.filter_by(eqp_id = plneqp['EQP_ID'],line_id = plneqp["LINE_ID"]).first().id, lot_id=plneqp['LOT_ID'], state_id=plneqp["STATE_ID"], start_t=plneqp["START_TIME"], end_t=plneqp["END_TIME"], prod_id=plneqp["PROD_ID"], lot_size=plneqp["LOT_QTY"])
            db.session.add(plneqp_obj)
        db.session.commit()  

def insertall():

    file_name = "data/Tumbler_Factory_revision.xlsx"
    DF_CSTDM = pd.read_excel('%s' %file_name, sheet_name = 'CUSTOMER_DEMAND', header=0, encoding='utf-8')
    DF_EQPPLN = pd.read_excel('%s' %file_name, sheet_name = 'EQP_PLAN', header=0, encoding='utf-8')
    DF_ANL = pd.read_excel('%s' %file_name, sheet_name = 'ANALYSIS', header=0, encoding='utf-8')

    ##get articles
    uploadOne(StdID1, DF_CSTDM["CST_ID"].unique())
    uploadOne(StdID2, DF_EQPPLN["LINE_ID"].unique())
    uploadOne(StdID3, DF_EQPPLN["LOT_ID"].unique())
    uploadOne(StdID4, DF_CSTDM["PROD_ID"].unique())
    uploadOne(StdID5, DF_EQPPLN["STEP_ID"].unique())
    uploadOne(LotSize, DF_EQPPLN["LOT_QTY"].unique())
    uploadStdEQP(DF_EQPPLN[{"EQP_ID","STEP_ID"}].drop_duplicates(subset=['EQP_ID']))
    uploadStdLineEQP(DF_EQPPLN[{"LINE_ID","EQP_ID"}].drop_duplicates(subset=['EQP_ID']))
    uploadPlanDM(DF_CSTDM)
    uploadViewRes(DF_ANL)
    uploadPlanEQP(DF_EQPPLN)
        


