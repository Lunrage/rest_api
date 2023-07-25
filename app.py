from flask import Flask, request, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import func
import json
import helpers

app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cakesdb.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

hp = helpers.DBClass()
hp.createAllTables()

class Cake():
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
    
    def getName(self):
        return self.name
    
    def getPrice(self):
        return self.price
    
    def getDescription(self):
        return self.description
    
    def setName(self, nm):
        self.name = nm
        
    def setPrice(self, pr):
        self.price = pr
    
    def setDescription(self, des):
        self.description = des

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cakes')
def get_cakes():
    cakes = hp.getAllCakes()
    cakes_list = []
    if cakes is not None:
        for cake in cakes:
            cakes_list.append({'id':cake.id, 'name':cake.name, 'price':str(cake.price), 'description':cake.description})
    
    return render_template('cakes.html', cakes=json.dumps(cakes_list, separators=(',',':')))

@app.route('/cakes/<id1>')
def get_cake(id1):
    cake = hp.getCakeById(id1)
    if cake is not None:
        return {'id':cake.id, 'name':cake.name, 'price':str(cake.price), 'description':cake.description}
    else:
        return {}

@app.route('/add_cake')
def create_cake():
    return render_template('add_cake.html')

@app.route('/cakes', methods=['POST'])
def add_cake():
    na=request.form['name']
    pr=request.form['price']
    des=request.form['description']
    my_cake = Cake(name=na, price=pr, description=des)
    id1 = hp.saveCake(my_cake)
    return redirect("/cakes", code=301)

@app.route('/cakes', methods=['DELETE'])
def delete_cake():
    id1=request.form['id1']
    res = hp.deleteCake(id1)
    return "1"

@app.route('/update_cake/<id1>')
def load_update_cake(id1):
    my_cake = hp.getCakeById(id1)
    if my_cake is not None:
        cake = {'id':my_cake.id, 'name':my_cake.name, 'price':str(my_cake.price), 'description':my_cake.description}
    else:
        cake = {'id': "", 'name':"", 'price':"", 'description':""}

    return render_template('update_cake.html', cake=json.dumps(cake))

@app.route('/cakes', methods=['PUT'])
def update_cake():
    id1 = request.form['id']
    na=request.form['name']
    pr=request.form['price']
    des=request.form['description']
    my_cake = Cake(name=na, price=pr, description=des)
    res = hp.updateCake(id1, my_cake)
    return "1"
