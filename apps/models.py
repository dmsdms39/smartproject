from apps import db, ma
import pandas as pd
from datetime import datetime

class BaseModel(db.Model):
    __abstract__=True
    id = db.Column(db.String(30), primary_key = True, nullable= False)

    create_t = db.Column(db.DateTime)
    update_t = db.Column(db.DateTime)
    # nullable= True 넣으나 마나 결과는 같음 


class StdID1(BaseModel):
    __tablename__ = 'tb_std_cst'
    def __init__(self, id):
        self.id = id
        self.create_t = datetime.now()
    

class StdID2(BaseModel):
    __tablename__ = 'tb_std_line'
    def __init__(self, id):
        self.id = id
        self.create_t = datetime.now()

class StdID3(BaseModel):
    __tablename__ = 'tb_std_lot'
    def __init__(self, id):
        self.id = id
        self.create_t = datetime.now()

class StdID4(BaseModel):
    __tablename__ = 'tb_std_prod'
    def __init__(self, id):
        self.id = id
        self.create_t = datetime.now()

class StdID5(BaseModel):
    __tablename__ = 'tb_std_step'
    def __init__(self, id):
        self.id = id
        self.create_t = datetime.now()
    
class StdSchema(ma.Schema):
    class Meta:
        fields = ('id', 'create_t', 'update_t')

        

class LotSize(db.Model): # tb_ist_lot_size
    __tablename__ = 'tb_ist_lot_size'
    id = db.Column(db.Integer, primary_key = True)

# class StdDay(db.Model): # tb_std_day
#     __tablename__ = 'tb_std_day'
#     id = db.Column(db.DateTime, primary_key = True)


class StdEQP(db.Model): # tb_std_eqp
    __tablename__ = 'tb_std_eqp'
    id = db.Column(db.String(30), primary_key = True, nullable= False)

    step_id = db.Column(db.ForeignKey('tb_std_step.id'), nullable= False)
    create_t = db.Column(db.DateTime, default = datetime.now)
    update_t = db.Column(db.DateTime)

    step = db.relationship('StdID5', primaryjoin='StdEQP.step_id == StdID5.id', backref='std_eqp', lazy=True)

class EQPSchema(ma.Schema):
    class Meta:
        fields = ('id', 'step_id', 'create_t', 'update_t')

    # @property
    # def eqp_id(self):
    #     return self.id
    
    # @property
    # def eqp_info(self):
    #     return "{0}/{1}:::/{2}".format(id, step_id)


class StdLineEQP(db.Model): # tb_std_line_eqp
    __tablename__ = 'tb_std_line_eqp'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable= False)

    line_id = db.Column(db.ForeignKey('tb_std_line.id'), default = 'Not Matched')
    eqp_id = db.Column(db.ForeignKey('tb_std_eqp.id'), nullable= False)

    line = db.relationship('StdID2', primaryjoin='StdLineEQP.line_id == StdID2.id', backref='std_line_eqp', lazy=True)
    eqp = db.relationship('StdEQP', primaryjoin='StdLineEQP.eqp_id == StdEQP.id', backref='std_line_eqp', lazy=True)

class LineEQPSchema(ma.Schema):
    class Meta:
        fields = ('id', 'line_id', 'eqp_id')
  


class PlanDM(db.Model): # tb_pln_dm
    __tablename__ = 'tb_pln_dm'
    id = db.Column(db.String(30), primary_key = True, nullable= False)
    due_d = db.Column(db.DateTime, default = 'Not Determined')
    qty = db.Column(db.Integer, default = 'Not Determined')
    prod_id = db.Column(db.ForeignKey('tb_std_prod.id'), nullable= False)
    cst_id = db.Column(db.ForeignKey('tb_std_cst.id'), nullable= False)

    prod = db.relationship('StdID4', primaryjoin='PlanDM.prod_id == StdID4.id', backref='pln_dm', lazy=True)
    cst = db.relationship('StdID1', primaryjoin='PlanDM.cst_id == StdID1.id', backref='pln_dm', lazy=True)

    def __init__(self, id, due_d, qty, prod_id, cst_id):
        self.id = id
        self.due_d = datetime.strptime(due_d, '%Y%m%d')
        self.qty = int(qty)
        self.prod_id = prod_id
        self.cst_id = cst_id

class PlanDMSchema(ma.Schema):
    class Meta:
        fields = ('id', 'due_d', 'qty', 'prod_id','cst_id')



class ViewRes(db.Model): # vw_res_eqp
    __tablename__ = 'vw_analysis_eqp'
    line_eqp_id = db.Column(db.ForeignKey('tb_std_line_eqp.id'), primary_key = True, nullable= False)
    t_day = db.Column(db.DateTime, primary_key = True, nullable= False)
    setup = db.Column(db.Float, default = '-')
    busy = db.Column(db.Float, default = '-')
    idle = db.Column(db.Float, default = '-')
    pm = db.Column(db.Float, default = 0)
    down = db.Column(db.Float, default = 0)

    line_eqp = db.relationship('StdLineEQP', primaryjoin='ViewRes.line_eqp_id == StdLineEQP.id', backref='res_eqp', lazy=True)

class ResEQPSchema(ma.Schema):
    class Meta:
        fields = ('line_eqp_id', 't_day', 'setup','busy','idle','pm','down')

    

class PlanEQP(db.Model): # tb_pln_eqp
    __tablename__ = 'tb_pln_eqp'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable= False)
    
    lot_id = db.Column(db.ForeignKey('tb_std_lot.id'), nullable= False)
    state_id = db.Column(db.String(30), nullable= False)
    start_t = db.Column(db.DateTime, default = 'Not Determind')
    end_t = db.Column(db.DateTime, default = 'Not Determind')
    prod_id = db.Column(db.ForeignKey('tb_std_prod.id'), nullable= False)
    lot_size = db.Column(db.ForeignKey('tb_ist_lot_size.id'), nullable= False)
    line_eqp_id = db.Column(db.ForeignKey('tb_std_line_eqp.id'), nullable= False)

    lot = db.relationship('StdID3', primaryjoin='PlanEQP.lot_id == StdID3.id', backref='pln_eqp', lazy=True)
    prod = db.relationship('StdID4', primaryjoin='PlanEQP.prod_id == StdID4.id', backref='pln_eqp', lazy=True)
    size = db.relationship('LotSize', primaryjoin='PlanEQP.lot_size == LotSize.id', backref='pln_eqp', lazy=True)
    line_eqp = db.relationship('StdLineEQP', primaryjoin='PlanEQP.line_eqp_id == StdLineEQP.id', backref='pln_eqp', lazy=True)
    # 객체에 삽입되는 가상 필드 이름입니다. 즉, 게시물을 `tb_std_line_eqp`라는 변수에 저장했다고 한다면 
    # 이 게시물을 작성한 게시자를 `tb_std_line_eqp.pln_eqp`을 이용해 접근할 수 있음

class PlanEQPSchema(ma.Schema):
    class Meta:
        fields = ('lot_id', 'state_id', 'start_t','end_t','prod_id','lot_size','line_eqp_id')
  