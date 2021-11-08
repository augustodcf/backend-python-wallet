from typing import List

from flask import Flask, escape, request, url_for, render_template, abort, flash, redirect, session, jsonify
import json
from controllers import blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectFieldBase, PasswordField, DateField
from wtforms.validators import DataRequired
from flask_debug import Debug
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.curdir)+os.sep+"static/page"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

Bootstrap(app)
Debug(app)
app.secret_key = b"""_5#y2L"F4Q8z\n\xec]/"""
app.config["SQLALCHEMY_DATABASE_URI"] = """mysql://root:6=2Cxl{3t6}g[pD@localhost/mydb"""
db = SQLAlchemy(app)
nav = Nav()

login_manager = LoginManager()
login_manager.init_app(app)


class Sale(db.Model):
    idsale = db.Column(db.Integer, primary_key=True, autoincrement=True)
    costumer_idcostumer = db.Column(db.Integer, unique=False, nullable=False)
    sold_at = db.Column(db.DateTime, unique=False, nullable=False)
    cashback = db.Column(db.Float, unique=False, nullable=True)

class Customer(db.Model):
    idcustomer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String(45), unique=False, nullable=False)

class Product_has_selling(db.Model):
    idproduct_has_sale = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_idproduct = db.Column(db.Integer, unique=False, nullable=False)
    sale_idsale = db.Column(db.Integer, unique=False, nullable=False)
    qty = db.Column(db.Integer, unique=False, nullable=True)

class Product(db.Model):
    idproduct = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, unique=False, nullable=True)
    productType = db.Column(db.Integer, unique=True, nullable=False)

producttypes = ["A","B","C","D"]



@app.route("/")
def index():
    return "server on"




@app.route('/api/cashback', methods=['GET', 'POST'])
def cashback():


    if request.method == "POST":
        entering = request.get_json()

        if entering == None:
            return jsonify({"message": "Missing JSON in request"}), 404

        thisdatetime = datetime.strptime(entering["sold_at"], '%y-%m-%d %H:%M:%S')


        if thisdatetime > datetime.today():
            return "Invalid date time"
        else:
            custumer = entering["customer"].strip
            if Customer.query.filter_by(cname=custumer["name"]).all():
                existscustomer = Customer.query.filter_by(document=custumer["document"]).all()
                if existscustomer:
                    totalsum = 0
                    for eachproduct in entering["products"]:
                        if eachproduct["type"] in producttypes:
                            totalsum = totalsum + eachproduct["value"]
                        else:
                            return "One or all product type are invalid"
                    if totalsum != entering["total"]:
                        return "Invalid total sum"
                    else:
                        cashback = totalsum * 0.05
                        newsale = Sale(customer_idcustomer=existscustomer.idcustomer, sold_at=sold_at, cashback=cashback)
                        for eachproduct in entering["products"]:
                            thisproduct = Product.query.filter_by(productType=eachproduct["type"]).all()
                            newPHS = Product_has_sale(product_idproduct=thisproduct.idproduct, sellin_idsale=newsale.idsale)
                            db.session.add(newPHS)

                        db.session.add(newsale)
                        db.session.commit()
                        db.session.commit()
                        out = {
                                  "createdAt": "2021-07-26T22:50:55.740Z",
                                  "message": "Cashback criado com sucesso!",
                                  "id": "NaN",
                                  "document": "33535353535",
                                  "cashback": "10"
                                }

                        return jsonify(out)
                else:
                    return "Invalid user document"
            else:
                return "Invalid user name"


    # user = User(UserName="arbusto", Password="werwer", Email="jenkins@leroy.com")
    # db.session.add(user)
    # db.session.commit()
    print(request.form)
    return "falhou"





app.run(debug=True, host='0.0.0.0')
