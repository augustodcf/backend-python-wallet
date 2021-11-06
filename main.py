from typing import List

from flask import Flask, escape, request, url_for, render_template, abort, flash, redirect, session
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
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.curdir)+os.sep+"static/page"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

Bootstrap(app)
Debug(app)
app.secret_key = b"""_5#y2L"F4Q8z\n\xec]/"""
app.config["SQLALCHEMY_DATABASE_URI"] = """mysql://root:6=2Cxl{3t6}g[pD@localhost/medievalfights"""
db = SQLAlchemy(app)
nav = Nav()

login_manager = LoginManager()
login_manager.init_app(app)


class Selling(db.Model):
    idselling = db.Column(db.Integer, primary_key=True, autoincrement=True)
    costumer_idcostumer = db.Column(db.Integer, unique=False, nullable=False)
    sold_at = db.Column(db.DateTime, unique=False, nullable=False)
    cashback = db.Column(db.Float, unique=False, nullable=True)

class Costumer(db.Model):
    idcostumer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), unique=False, nullable=False)

class Product_has_selling(db.Model):
    idproduct_has_selling = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_idproduct = db.Column(db.Integer, unique=False, nullable=False)
    selling_idselling = db.Column(db.Integer, unique=False, nullable=False)
    qty = db.Column(db.Integer, unique=False, nullable=True)

class Product(db.Model):
    idproduct = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, unique=False, nullable=True)
    productType = db.Column(db.Integer, unique=True, nullable=False)

producttypes = ["A","B","C","D"]



@app.route("/")
def index():
    return render_template("index.html")




@app.route('/api/cashback', methods=['GET', 'POST'])
def cashback():


    if request.method == "POST":
        #parsint json to python

        entering = json.loads(request.form)

        if entering(y["sold_at"]) > DateTime.now:
            return "Invalid date time"
        else:
            if  Customer.query.filter_by(name=entering.customer.name).all():
                customer = Customer.query.filter_by(document=entering.customer.document).all()
                if customer:
                    totalsum = 0
                    for eachproduct in entering.products:
                        if eachproduct.value in producttypes:
                            totalsum = totalsum + eachproduct.value
                        else:
                            return "One or all product type are invalid"
                    if totalsum != entering.total:
                        return "Invalid total sum"
                    else:
                        cashback = totalsum * 0.05
                        newselling = Selling(customer_idcustomer=customer.idcustomer, sold_at=sold_at, cashback=cashback)
                        for eachproduct in entering.products:
                            thisproduct = Product.query.filter_by(productType=eachproduct.type).all()
                            newPHS = Product_has_selling (product_idproduct=thisproduct.idproduct,sellin_idselling=newselling.idselling)
                            db.session.add(newPHS)
                        db.session.add(newselling)
                        db.session.commit(thisproduct)
                        thisselling = Product_has_selling (idselling=newselling.idsellinselling.idselling).all()
                        out = {
                                    "createdAt": sold_at,
                                    "message": "Cashback criado com sucesso!",
                                    "id": thisselling.idsellig,
                                    "document": customer.document,
                                    "cashback": cashback
                        }
                        return json.dumps(out)
                else:
                    return "Invalid user document"
            else:
                return "Invalid user name"


    # user = User(UserName="arbusto", Password="werwer", Email="jenkins@leroy.com")
    # db.session.add(user)
    # db.session.commit()
    print(request.form)
    return "falhou"



@app.route("/pageadmo", methods=['GET', 'POST'])
@login_required
def pageadmo():
    table = {'headers': ['Select', 'Name', 'Editors', 'Status', 'Type'],
             'contents': []
             }
    checked = []
    pagetype = 0



    if request.method == "POST":
        for check in request.form:
            checked.append(check.split('_')[1])



        if checked == [("Revoke")] or checked == [('Share')]:
            flash("You must select pages first.")
            return redirect(url_for('pageadmo'))
        else:
            if ("Revoke") in checked:
                checked.remove("Revoke")
                session['checked'] = checked
                return redirect(url_for('userselection'))
            elif ("Share") in checked:
                checked.remove("Share")
                session['checked'] = checked
                return redirect(url_for('shareselection'))
            elif ("Delete") in checked:
                checked.remove("Delete")
                for check in checked:
                    page = Page.query.filter_by(nome=check).first()
                    # checking the page type and deleting content
                    fighter = Fighter.query.filter_by(page_idpage=page.idpage).first()
                    event = Event.query.filter_by(page_idpage=page.idpage).first()
                    other = Other.query.filter_by(page_idpage=page.idpage).first()
                    group = Group.query.filter_by(page_idpage=page.idpage).first()
                    if fighter is not None:
                        ghfs = Group_has_fighter.query.filter_by(fighter_idfighter=fighter.idfighter).all()
                        for ghf in ghfs:
                            db.session.delete(ghf)
                        db.session.delete(fighter)
                    if event is not None:
                        stages = Stage.query.filter_by(event_idevent=event.idevent).all()
                        for stage in stages:
                            stagefights = Fight.query.filter_by(stage_idstage=stage.idStage).all()
                            for fight in stagefights:
                                db.session.delete(fight)
                            db.session.delete(stage)
                        db.session.delete(event)
                    if other is not None:
                        db.session.delete(other)
                    if group is not None:
                        ghfs = Group_has_fighter.query.filter_by(group_idgroup=group.idgroup).all()
                        for ghf in ghfs:
                            db.session.delete(ghf)
                        db.session.delete(group)

                    flash("Page "+check+" deleted.")
                    # deleting relations
                    haspages = page.users
                    for objhaspage in haspages:
                        user = objhaspage.user
                        user.pages.remove(objhaspage)
                        page.users.remove(objhaspage)
                        db.session.delete(objhaspage)
                        db.session.add(user)
                    # finaly deleting page
                    db.session.delete(page)
                db.session.commit()
                return redirect(url_for('pageadmo'))

    for page in current_user.pages:
        # if request.method == "POST":
        #    if page.page.nome not in checked:
        #        continue
        #    else :
        #        pass
        editors = []
        # passing parameters if owner
        if page.user_has_page_relationtype == "o":
            select = "☑"

            for has_page in User_has_page.query.filter_by(user_has_page_relationtype="e").all():
                if has_page.user != current_user:
                    if page.page == has_page.page:
                        editors += [has_page.user.username]

        else:
            select = ""

        if page.page.status == 1:
            status = "Published"
        elif page.page.status == None:
            status = "Unpublished"
        elif page.page.status == 0:
            status = "Waiting aproval"

        editors = ", ".join(editors)

        if Fighter.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thistype = 'Fighter'
        elif Group.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thisgroup = Group.query.filter_by(page_idpage=page.page.idpage).first()
            if thisgroup.type == None:
                thistype = 'Team'
            else:
                thistype = 'Club'
        elif Event.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thistype = 'Event'
        elif Other.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thistype = 'Other'
        else:
            thistype = '﹃' #this symbol will construct a drop list with page options on template

        if page.user_has_page_relationtype == "o":
            dic = {'Select': select,
                   'Name': page.page.nome,
                   'Editors': editors,
                   'Status': status,
                   'Type': thistype
                   }
            table['contents'].append(dic)

    return render_template('beko/userhaspages.html', table=table, pagetype=pagetype)

@app.route("/pageadme", methods=['GET', 'POST'])
@login_required
def pageadme():
    table = {'headers': ['Select', 'Name', 'Status'],
             'contents': []
             }
    checked = []
    pagetype = 1

    if request.method == "POST":
        for check in request.form:
            #checked.append(check.split('_')[1])
            thispage = Page.query.filter_by(nome=(check.split('_')[1])).first()
            haspage = User_has_page.query.filter_by(page=thispage,user=current_user).first()
            #for haspage in haspages:
                #if haspage.user == current_user:
            current_user.pages.remove(haspage)
            db.session.delete(haspage)
            db.session.add(thispage)
            db.session.add(current_user)
            db.session.commit()
            flash("Editor power on " + check.split('_')[1] + " page successfully abdicated.")

        return redirect(url_for('pageadme'))

    for page in current_user.pages:
        # if request.method == "POST":
        #    if page.page.nome not in checked:
        #        continue
        #    else :
        #        pass

        if page.user_has_page_relationtype == "e":
            select = "☑"
        else:
            select = ""


        if page.page.status == 1:
            status = "Published"
        elif page.page.status == None:
            status = "Unpublished"
        elif page.page.status == 0:
            status = "Waiting aproval"

        if page.user_has_page_relationtype == "e":
            dic = {'Select': select,
                   'Name': page.page.nome,
                   'Status': status,

                   }
            table['contents'].append(dic)



    return render_template('beko/userhaspages.html', table=table, pagetype=pagetype)


@app.route("/pageregister", methods=['GET', 'POST'])
@login_required
def pageregister():
    pageform = Addpage()
    haspage = User_has_page()
    if pageform.validate_on_submit():
        if Page.query.filter_by(nome=pageform.pagename.data).first() is not None:
            flash("Sorry. This page already exists!")
        else:
            page = Page(nome=pageform.pagename.data)
            haspage.page = page
            haspage.user_has_page_relationtype = "o"
            haspage.user = current_user
            db.session.add(page)
            current_user.pages.append(haspage)
            db.session.add(haspage)
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('pageadmo'))

    return render_template('/beko/userregisterpage.html', form=pageform)

@app.route('/pagecontrol')
@login_required
def pagecontrol():

    thisUserPower = current_user.power
    return render_template('/beko/pagecontrol.html', thisUserPower=thisUserPower)

def iniciarbanco():
    #db.drop_all()
    #db.create_all()

    user1 = User(username="arbusto", password="werwer", email="jenkins@leroy.com")
    db.session.add(user1)

    user2 = User(username="tony", password="123123", email="jenkins@leroytcs.com")
    db.session.add(user2)

    fighter = Fighter(
    fighterName        = "Tornado Ferreira",
    fighterAge         = 1988,
    fighterWeight      = 90,
    fighterHeight      = 175,
    fighterMainHand    = "R",
    fighterEmail       = "johnbiritones@gmail.com",
    fighterGif         = None,
    fighterSex         = "M",
    )
    db.session.add(fighter)

    page = Page(
    nome     = "tferreira",
    header      = None,
    icone     = None,
    pagetypeid = 0,
    status = None,

    )
    db.session.add(page)

    user_page = User_has_page (
    user_id            = user1.idUser,
    page_idpage            = page.idpage,
    user_has_PageRelation  = "o",
    )

    user_page = User_has_page(
        user_id = user2.idUser,
        page_idpage=page.idpage,
        user_has_PageRelation="e",
    )

    db.session.add(user_page)

    db.session.commit()

#iniciarbanco()

app.run(debug=True, host='0.0.0.0')
