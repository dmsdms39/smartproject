from flask import render_template, jsonify, request
from apps import app, db, ma
from .models import *
from datetime import datetime


planeqp_schema = PlanEQPSchema()
planeqps_schema = PlanEQPSchema(many=True)

# Get All
@app.route('/planeqp', methods=['GET'])
def get_planeqps():
  all_planeqps = PlanEQP.query.all()
  result = planeqps_schema.dump(all_planeqps)
  return jsonify(result)

# Get Single
@app.route('/planeqp/<id>', methods=['GET'])
def get_planeqp(id):
  planeqp = PlanEQP.query.get(id)
  return planeqp_schema.jsonify(planeqp)

# Update
@app.route('/planeqp/<id>', methods=['PUT'])
def update_planeqp(id):
  planeqp = PlanEQP.query.get(id)
  lot_id = request.json['lot_id']
  state_id = request.json['state_id']
  start_t = request.json['start_t']
  end_t = request.json['end_t']
  prod_id = request.json['prod_id']
  lot_size = request.json['lot_size']
  line_eqp_id = request.json['line_eqp_id']

  planeqp.lot_id = lot_id
  planeqp.state_id = state_id
  planeqp.start_t = start_t
  planeqp.end_t = end_t
  planeqp.prod_id = prod_id
  planeqp.lot_size = lot_size
  planeqp.line_eqp_id = line_eqp_id
  db.session.commit()
  return planeqp_schema.jsonify(planeqp)

# Delete
@app.route('/planeqp/<id>', methods=['DELETE'])
def delete_planeqp(id):
  planeqp = PlanEQP.query.get(id)
  db.session.delete(planeqp)
  db.session.commit()
  return planeqp_schema.jsonify(planeqp)


plandm_schema = PlanDMSchema()
plandms_schema = PlanDMSchema(many=True)


# Get All
@app.route('/plandm', methods=['GET'])
def get_plandms():
  all_plandms = PlanDM.query.all()
  result = plandms_schema.dump(all_plandms)
  return jsonify(result)

# Get Single
@app.route('/plandm/<id>', methods=['GET'])
def get_plandm(id):
  plandm = PlanDM.query.get(id)
  return plandm_schema.jsonify(plandm)

# Insert
@app.route('/plandm', methods=['POST'])
def add_plandm():
  id = request.json['id']
  due_d = request.json['due_d']
  qty = request.json['qty']
  prod_id = request.json['prod_id']
  cst_id = request.json['cst_id']

  new_plandm = PlanDM(id, due_d, qty, prod_id, cst_id)
  
  db.session.add(new_plandm)
  db.session.commit()

  return plandm_schema.jsonify(new_plandm)

# Update
@app.route('/plandm/<id>', methods=['PUT'])
def update_plandm(id):
  plandm = PlanDM.query.get(id)
  id = request.json['id']
  due_d = request.json['due_d']
  qty = request.json['qty']
  end_t = request.json['end_t']
  prod_id = request.json['prod_id']
  cst_id = request.json['cst_id']

  plandm.id = id
  plandm.due_d = due_d
  plandm.qty = qty
  plandm.end_t = end_t
  plandm.prod_id = prod_id
  plandm.cst_id = cst_id
  db.session.commit()
  return plandm_schema.jsonify(plandm)

# Delete
@app.route('/plandm/<id>', methods=['DELETE'])
def delete_plandm(id):
  plandm = PlanDM.query.get(id)
  db.session.delete(plandm)
  db.session.commit()
  return plandm_schema.jsonify(plandm)


eqp_schema = EQPSchema()
eqps_schema = EQPSchema(many=True)

# Get All
@app.route('/eqp', methods=['GET'])
def get_eqps():
  all_eqps = StdEQP.query.all()
  result = eqps_schema.dump(all_eqps)
  return jsonify(result)

# Get Single
@app.route('/eqp/<id>', methods=['GET']) #id없고 바로 eqp_id로 바꿔줘야됌
def get_eqp(id):
  eqp = StdEQP.query.get(id)
  return eqp_schema.jsonify(eqp)

# Update
@app.route('/eqp/<id>', methods=['PUT'])
def update_eqp(id):
  eqp = StdEQP.query.get(id)
  lot_id = request.json['lot_id']
  state_id = request.json['state_id']
  start_t = request.json['start_t']
  end_t = request.json['end_t']
  prod_id = request.json['prod_id']
  lot_size = request.json['lot_size']
  line_eqp_id = request.json['line_eqp_id']

  eqp.lot_id = lot_id
  eqp.state_id = state_id
  eqp.start_t = start_t
  eqp.end_t = end_t
  eqp.prod_id = prod_id
  eqp.lot_size = lot_size
  eqp.line_eqp_id = line_eqp_id
  db.session.commit()
  return eqp_schema.jsonify(eqp)

# Delete
@app.route('/eqp/<id>', methods=['DELETE'])
def delete_eqp(id):
  eqp = StdEQP.query.get(id)
  db.session.delete(eqp)
  db.session.commit()
  return eqp_schema.jsonify(eqp)


reseqp_schema = ResEQPSchema()
reseqps_schema = ResEQPSchema(many=True)


# Get All
@app.route('/reseqp', methods=['GET'])
def get_reseqps():
  all_reseqps = ViewRes.query.all()
  result = reseqps_schema.dump(all_reseqps)
  return jsonify(result)

# Get Single
@app.route('/reseqp/<line_eqp_id>', methods=['GET']) #line_eqp_id와 eqp_id 연결해서 가져오기
def get_reseqp(line_eqp_id):
  reseqp = ViewRes.query.get(line_eqp_id)
  return reseqp_schema.jsonify(reseqp)


## 입력받지 않아서 삭제나 수정은 필요없음
# # Update
# @app.route('/reseqp/<id>', methods=['PUT'])
# def update_reseqp(id):
#   reseqp = ViewRes.query.get(id)
#   line_eqp_id = request.json['line_eqp_id']
#   t_day = request.json['t_day']
#   setup = request.json['setup']
#   busy = request.json['busy']
#   idle = request.json['idle']
#   pm = request.json['pm']
#   down = request.json['down']

#   reseqp.line_eqp_id = line_eqp_id
#   reseqp.t_day = t_day
#   reseqp.setup = setup
#   reseqp.busy = busy
#   reseqp.idle = idle
#   reseqp.pm = pm
#   reseqp.down = down
#   db.session.commit()
#   return reseqp_schema.jsonify(reseqp)

# # Delete
# @app.route('/reseqp/<id>', methods=['DELETE'])
# def delete_reseqp(id):
#   reseqp = ViewRes.query.get(id)
#   db.session.delete(reseqp)
#   db.session.commit()
#   return reseqp_schema.jsonify(reseqp)


lineeqp_schema = LineEQPSchema()

stdid_schema = StdSchema()
stdids_schema = StdSchema(many=True)

# Get All
@app.route('/stdid', methods=['GET'])
def get_stdids():
  all_stdids = StdID1.query.all()
  result = stdids_schema.dump(all_stdids)
  return jsonify(result)

# Insert
@app.route('/stdid', methods=['POST'])
def add_stdid():
  id = request.json['id']
  
  new_stdid = StdID1(id)
  
  db.session.add(new_stdid)
  db.session.commit()

  return plandm_schema.jsonify(new_stdid)

# Update
@app.route('/stdid/<id>', methods=['PUT'])
def update_stdid(id):
  stdid = StdID1.query.get(id)

  id = request.json['id']
  
  stdid.id = id
  stdid.update_t = datetime.now()

  db.session.commit()
  return eqp_schema.jsonify(stdid)

# Delete
@app.route('/stdid/<id>', methods=['DELETE'])
def delete_stdid(id):
  stdid = StdID1.query.get(id)
  db.session.delete(stdid)
  db.session.commit()
  return eqp_schema.jsonify(stdid)