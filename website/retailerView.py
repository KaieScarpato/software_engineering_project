from flask import Blueprint,render_template,redirect,url_for,request,flash
from .models import Beer
from . import db

retailerView = Blueprint('retailerView', __name__)

@retailerView.route('/retailer', methods=['GET', 'POST'])
def retailer():
    if request.method == 'POST':
        if request.form['button'] == 'read':
            if request.form['button'] == 'read':
                input = request.form.get('readID')
            if input:
                input = int(input)
                if Beer.query.filter_by(id=input).first() != None:
                    return redirect(url_for('retailerView.readDatabase', index = input))
                else:
                    flash('Enter existing ID')
        elif request.form['button'] == 'specials':
            return redirect(url_for('retailerView.specials'))
        elif request.form['button'] == 'searchHigh':
            return redirect(url_for('retailerView.searchFreqHigh'))
        elif request.form['button'] == 'searchLow':
            return redirect(url_for('retailerView.searchFreqLow'))
    return render_template("retailer/retailer.html", view = 2)

@retailerView.route('/retailer/specials', methods=['GET', 'POST'])
def specials():
    if request.method == 'POST':
        if request.form['button']=='add':
            index = int(request.form.get('add'))
            beer = Beer.query.filter(Beer.id==index).first()
            beer.special=1
            beer.price=float(beer.price / 2)
            db.session.commit()
        elif request.form['button'] == 'back':
            return redirect(url_for('retailerView.retailer'))
        else:
            index = int(request.form['button'])
            beer = Beer.query.filter(Beer.id==index).first()
            beer.special=0
            beer.price=float(beer.price * 2)
            db.session.commit()

    return render_template("retailer/specials.html", data = Beer.query.filter(Beer.special==1), view = 2)


@retailerView.route('/retailer/searchFrequencyHigh', methods=['GET', 'POST'])
def searchFreqHigh():
    if request.method == 'POST':
        if request.form['button']=='back':
            return redirect(url_for('retailerView.retailer'))

    return render_template("retailer/searchFreq.html", data=Beer.query.order_by(Beer.searchFreq.desc()).limit(10), view = 2)

@retailerView.route('/retailer/searchFrequencyLow', methods=['GET', 'POST'])
def searchFreqLow():
    if request.method == 'POST':
        if request.form['button']=='back':
            return redirect(url_for('retailerView.retailer'))
    return render_template("retailer/searchFreq.html", data=Beer.query.order_by(Beer.searchFreq.asc()).limit(10), view = 2)

@retailerView.route('/retailer/editDatabase/readDatabase', methods=['GET', 'POST'])
def readDatabase():
    index = request.args.get('index', None)
    beer = Beer.query.filter_by(id=index).first()
    if request.method == 'POST':
        if request.form['button']=='update':
            return redirect(url_for('retailerView.updateDatabase', index = index))
        elif request.form['button']=='back':
            return redirect(url_for('retailerView.retailer'))

    return render_template("retailer/readDatabase.html", data = beer, view = 2) 

@retailerView.route('/retailer/editDatabase/updateDatabase', methods=['GET', 'POST'])
def updateDatabase():
    index = request.args.get('index', None)
    beer = Beer.query.filter_by(id=index).first()
    if request.method == 'POST':
        if request.form['button'] == 'update':
            price = request.form.get('price')
            beer.price = price
            db.session.commit()
            flash('update successful')
            return redirect(url_for('retailerView.readDatabase', index=index))
        elif request.form['button']=='back':
            return redirect(url_for('retailerView.retailer'))

    return render_template("retailer/updateDatabase.html", data = beer, view = 2)