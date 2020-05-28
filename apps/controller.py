from flask import render_template, jsonify, request
import pandas as pd

from apps import app, db
from .params import *
from .graph import *
from .apiurl import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

# @app.route('/index')
# def index():
#     bar = create_gantt()
#     return render_template('index.html', plot=bar)


##맨처음 sqlalchemy 공부
# @app.route('/<name>')
# def get_location(name):
#     user = User.query.filter_by(name = name).all()

#     return f'<h1>{user.location}</h1>'


# @app.route('/')
# def index():
#     return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/first_insert')
def insert():#초기화버튼
    insertall()


@app.route('/modify')
def modify():
    # 수정된 내용 넣기
    print("수정하기")


@app.route('/articles')
def articles():    
    planeqp = db.session.query(PlanEQP).filter()
    df1 = pd.read_sql(planeqp.statement, planeqp.session.bind)

    return render_template('articles.html',tables=[df1.to_html(classes='data')], titles=df1.columns.values, articles=planeqp)
    # #create cursor
    # cur = mysql.connection.cursor()
    # sql = "SELECT * FROM articles"
    # #get articles
    # result = cur.execute(sql)

    # articles = cur.fetchall()   
    # if result > 0:
    #         df = pd.read_sql(sql, db)
    #     df1= pd.DataFrame(df)
    #     dbdata = jsonify(articles)
    #     print(df1)
    #     # data = {"data1":df , "data2":dbdata}
    #     return render_template('articles.html',tables=[df1.to_html(classes='data')], titles=df.columns.values, articles=articles)
    # else:
    #     msg = 'No Articles Found'
    #     return render_template('articles.html',msg=msg)
    # #close connection
    # cur.close()

@app.route('/article/<string:idx>/')
def article(idx):
    planeqp = db.session.query(PlanEQP).filter().all()#eqpid, lineid 등등
    df1 = pd.read_sql(planeqp.statement, planeqp.session.bind)

    return render_template('article.html',article=planeqp)

# @app.route('/article/<string:id>/')
# def article(id):
#     #create cursor
#     cur = mysql.connection.cursor()

#     #get article
#     result = cur.execute("SELECT * FROM articles WHERE id = %s",[id])

#     article = cur.fetchone()

#     return render_template('article.html',article=article)


@app.route('/graph')
def graphjson():
    gantt_chart = process_product()

    return render_template('index.html', plot=gantt_chart)

@app.route('/graph2')
def graphjson2():
    operating_chart = operating_ratio()

    return render_template('index2.html', plot2=operating_chart)

@app.route('/api/process_product')
def process_product_api():
    return process_product()

