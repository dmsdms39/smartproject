from flask import Flask, jsonify, request, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/tbl_data'


db = SQLAlchemy(app)

#migrator 추가

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



import apps.controller
import apps.models

# res_eqp1 = vm_res_eqp.filter_by(std_day='2019-05-05').line
# res_eqp1.line

# line1 = tb_std_line.filter_by~~.get()
# line1.res_eqp

# joinedload => performance 향상

