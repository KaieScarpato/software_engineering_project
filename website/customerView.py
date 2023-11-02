from flask import Blueprint, render_template,redirect,url_for,request
from .scripts import findTotal
from .models import Beer
from . import db

customerView = Blueprint('customerView', __name__)
cart = []

@customerView.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        if request.form['button'] == 'products':
            return redirect(url_for('customerView.products', page = 0))
        if request.form['button'] == 'specials':
            return redirect(url_for('customerView.specials'))
        
    return render_template("customer/customer.html")

@customerView.route('/customer/products', methods=['GET','POST'])
def products():
    page = int(request.args.get('page', None))
    if request.method == 'POST':
        if request.form['button'] == 'back':
            return redirect(url_for('customerView.customer'))
        elif request.form['button'] == 'Checkout':
            return redirect(url_for('customerView.checkout'))
        elif request.form['button'] == 'previous':
            page = page - 1
            return redirect(url_for('customerView.products', page = page))
        elif request.form['button'] == 'next':
            page = page + 1
            return redirect(url_for('customerView.products', page = page))
        else:    
            index = int(request.form['button'])
            Beer.query.filter_by(id=index).first().searchFreq += 1
            db.session.commit()
            return redirect(url_for('customerView.product', index = index))
    
    return render_template("customer/productList.html", data = Beer.query.filter(Beer.id >= int(page*10)).limit(10), page = page)

@customerView.route('/customer/specials', methods=['GET','POST'])
def specials():
    if request.method == 'POST':
        if request.form['button'] == 'back':
            return redirect(url_for('customerView.customer'))
        elif request.form['button'] == 'Checkout':
            return redirect(url_for('customerView.checkout'))
        else:    
            index = int(request.form['button']) 
            Beer.query.filter_by(id=index).first().searchFreq += 1
            db.session.commit()
            return redirect(url_for('customerView.product', index = index))
    
    return render_template("customer/specials.html", data = Beer.query.filter(Beer.special==1))

@customerView.route('/customer/product', methods=['GET','POST'])
def product():
    index = request.args.get('index', None)
    if request.method == 'POST':
        if request.form['button'] == 'products':
            return redirect(url_for('customerView.products', page = 0))
        elif request.form['button'] == 'cart':
            num = int(request.form.get('numberInput'))
            for _ in range(num):
                cart.append(Beer.query.filter_by(id=index).first())
        else:
            index = int(request.form['button'])
            Beer.query.filter_by(id=index).first().searchFreq += 1
            db.session.commit()
            return redirect(url_for('customerView.product', index = index))
    
    beerList = []
    initBeer = Beer.query.filter_by(id=index).first()
    
    beerList.append(initBeer)

    beerList.append(Beer.query.filter(Beer.brewer == initBeer.brewer).filter(Beer.id != initBeer.id).first())
    beerList.append(Beer.query.filter(Beer.region == initBeer.region).filter(Beer.id != initBeer.id).filter(Beer.id != beerList[1].id).first())
    beerList.append(Beer.query.filter(Beer.primaryBeerStyle == initBeer.primaryBeerStyle).filter(Beer.id != initBeer.id).filter(Beer.id != beerList[1].id).filter(Beer.id != beerList[2].id).first())

    return render_template('customer/product.html', data = beerList)

@customerView.route('/customer/checkout', methods=['GET','POST'])
def checkout():
    total = findTotal(cart)
    if request.method == 'POST':
        if request.form['button'] == 'back':
            return redirect(url_for('customerView.products', page = 0))
        elif request.form['button'] == 'continue':
            return redirect(url_for('customerView.payment', total=str(total)))
    
    return render_template('customer/checkout.html', data = cart, total = total)

@customerView.route('/customer/checkout/payment', methods=['GET','POST'])
def payment():
    total = request.args.get('total', None)
    if request.method == 'POST':
        if request.form['button'] == 'back':
            return redirect(url_for('customerView.products', page = 0))
        elif request.form['button'] == 'pay':    
            cardNumber = request.form.get('cardNumber')
            month = request.form.get('month')
            year = request.form.get('year')
            cvv = request.form.get('cvv')
            print(cardNumber, month, year, cvv)
            cart.clear()
            return redirect(url_for('customerView.checkout'))
    
    return render_template('customer/payment.html', total = total)