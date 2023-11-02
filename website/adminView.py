from flask import Blueprint,render_template,flash,redirect,url_for,request
from sqlalchemy import exc
from .models import Beer
from .scripts import init_database
from . import db

adminView = Blueprint('adminView', __name__)

@adminView.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['button'] == 'create':
            return redirect(url_for('adminView.createDatabase'))
        if request.form['button'] == 'read':
            input = request.form.get('readID')
            if input:
                input = int(input)
                if Beer.query.filter_by(id=input).first() != None:
                    return redirect(url_for('adminView.readDatabase', index = input))
                else:
                    flash('Enter existing ID')        
        if request.form['button'] == 'update':
            input = request.form.get('updateID')
            if input:
                input = int(input)
                if Beer.query.filter_by(id=input).first() != None:
                    return redirect(url_for('adminView.updateDatabase', index = input))
                else:
                    flash('Enter existing ID')        
        if request.form['button'] == 'delete':
            input = request.form.get('readID')
            if input:
                input = int(input)
                if Beer.query.filter_by(id=input).first() != None:
                    return redirect(url_for('adminView.deleteDatabase', index = input))
                else:
                    flash('Enter existing ID')
        if request.form['button'] == 'initialize':
            try:
                init_database()
            except exc.SQLAlchemyError:
                flash('Database is already initialized')
        
    return render_template("admin/admin.html") 

@adminView.route('/admin/createDatabase', methods=['GET', 'POST'])
def createDatabase():
    index = int(Beer.query.order_by(Beer.id.desc()).first().id) + 1
    if request.method == 'POST':
        if request.form['button'] == 'create':
            new_beer = Beer(id=index,
                            name=request.form.get('name'),
                            price=float(request.form.get('price')),
                            brewer=request.form.get('brewer'),
                            region=request.form.get('region'),
                            country=request.form.get('country'),
                            state=request.form.get('state'),
                            tempBeerStyle1=request.form.get('temp1'),
                            tempBeerStyle2=request.form.get('temp2'),
                            primaryBeerStyle=request.form.get('primary'),
                            primaryBeerStyleDesc=request.form.get('primaryD'),
                            specificBeerStyle=request.form.get('style'),
                            specificBeerStyleDesc=request.form.get('styleD'),
                            foodPairing=request.form.get('food'),
                            oz=request.form.get('oz'),
                            ml=request.form.get('ml'),
                            container=request.form.get('container'),
                            abv=request.form.get('abv'),
                            ibu=request.form.get('ibu'),
                            srm=request.form.get('srm'),
                            malt=request.form.get('malt'),
                            hops=request.form.get('hops'),
                            cals=request.form.get('cals'),
                            desc=request.form.get('desc'),
                            special=0,
                            searchFreq=0)
            db.session.add(new_beer)
            db.session.commit()
            flash('create successful')
            return redirect(url_for('adminView.admin'))
        
    return render_template("admin/createDatabase.html") 

@adminView.route('/admin/readDatabase', methods=['GET', 'POST'])
def readDatabase():
    index = request.args.get('index', None)
    beer = Beer.query.filter_by(id=index).first()
    if request.method == 'POST':
        if request.form['button']=='back':
            return redirect(url_for('adminView.admin'))

    return render_template("admin/readDatabase.html", data = beer) 

@adminView.route('/admin/updateDatabase', methods=['GET', 'POST'])
def updateDatabase():
    index = request.args.get('index', None)
    beer = Beer.query.filter_by(id=index).first()
    if request.method == 'POST':
        if request.form['button'] == 'update':
            beer.name = request.form.get('name')
            beer.price = request.form.get('price')
            beer.brewer=request.form.get('brewer')
            beer.region=request.form.get('region')
            beer.country=request.form.get('country')
            beer.state=request.form.get('state')
            beer.tempBeerStyle1=request.form.get('temp1')
            beer.tempBeerStyle2=request.form.get('temp2')
            beer.primaryBeerStyle=request.form.get('primary')
            beer.primaryBeerStyleDesc=request.form.get('primaryD')
            beer.specificBeerStyle=request.form.get('style')
            beer.specificBeerStyleDesc=request.form.get('styleD')
            beer.foodPairing=request.form.get('food')
            beer.oz=request.form.get('oz')
            beer.ml=request.form.get('ml')
            beer.container=request.form.get('container')
            beer.abv=request.form.get('abv')
            beer.ibu=request.form.get('ibu')
            beer.srm=request.form.get('srm')
            beer.malt=request.form.get('malt')
            beer.hops=request.form.get('hops')
            beer.cals=request.form.get('cals')
            beer.desc=request.form.get('desc')
            db.session.commit()
            flash('update successful')
            return redirect(url_for('adminView.admin'))

    return render_template("admin/updateDatabase.html", data = beer)

@adminView.route('/admin/deleteDatabase', methods=['GET', 'POST'])
def deleteDatabase():
    index = request.args.get('index', None)
    beer = Beer.query.filter_by(id=index).first()
    if request.method == 'POST':
        if request.form['button'] == 'delete':
            db.session.delete(beer)
            db.session.commit()
            flash('delete successful')
            return redirect(url_for('adminView.admin'))

    return render_template("admin/deleteDatabase.html", data = beer)  