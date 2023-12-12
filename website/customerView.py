from flask import Blueprint, render_template,redirect,url_for,request
from .scripts import findTotal
from .models import Beer
from . import db

customerView = Blueprint('customerView', __name__)
cart = []
ll = [-1]

@customerView.route('/customer/products', methods=['GET','POST'])
def products():
    flag = 0
    page = int(request.args.get('page', None))
    beerList = Beer.query.filter(Beer.id >= int(page*10)).limit(10)
    len = beerList.count()
    if request.method == 'POST':
        if request.form['button'] == 'search':
            sTerm = request.form.get('search')
            return redirect(url_for('customerView.search', term = sTerm))
        elif request.form['button'] == 'back':
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

    if len < 10:
        flag = 1

    return render_template("customer/productList.html", data = beerList, page = page, flag = flag, view = 4)

@customerView.route('/customer/search', methods=['GET','POST'])
def search():
    flag = 0
    term = str(request.args.get('term', None))
    beerList = Beer.query.filter(Beer.name.contains(term),Beer.id > ll[-1]).limit(10)
    len = beerList.count()
    if len > 0:
        if request.method == 'POST':
            if request.form['button'] == 'search':
                sTerm = request.form.get('search')
                return redirect(url_for('customerView.search', term = sTerm))
            if request.form['button'] == 'back':
                return redirect(url_for('customerView.customer'))
            elif request.form['button'] == 'Checkout':
                return redirect(url_for('customerView.checkout'))
            elif request.form['button'] == 'previous':
                ll.pop()
                return redirect(url_for('customerView.search', ll = ll, term = term))
            elif request.form['button'] == 'next':
                ll.append(beerList[len - 1].id)
                return redirect(url_for('customerView.search', ll = ll, term = term))
            else:    
                index = int(request.form['button'])
                Beer.query.filter_by(id=index).first().searchFreq += 1
                db.session.commit()
                return redirect(url_for('customerView.product', index = index))
    
        if not Beer.query.filter(Beer.name.contains(term), Beer.id > beerList[len - 1].id).limit(1):
            flag = 1
        if len < 10:
            flag = 1

        return render_template("customer/productList.html", data = beerList, page = ll[-1], flag = flag, view = 4)
    else:
        return render_template("customer/searchError.html", term = term, view = 4)

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
    
    return render_template("customer/specials.html", data = Beer.query.filter(Beer.special==1), view = 4)

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

    params = [initBeer.id,-1,-1,-1]
    while -1 in params:
        if params[1] == -1:
            for id in range(len(beerList)):
                newBeer = Beer.query.filter(Beer.brewer == beerList[id].brewer).limit(4)
                if newBeer:
                    for each in newBeer:
                        if each.id not in params:
                            beerList.append(each)
                            params[1] = each.id
                            break
        if params[2] == -1:
            for id in range(len(beerList)):
                newBeer = Beer.query.filter(Beer.region == beerList[id].region).limit(4)
                if newBeer:
                    for each in newBeer:
                        if each.id not in params:
                            beerList.append(each)
                            params[2] = each.id
                            break
        if params[3] == -1:
            for id in range(len(beerList)):
                newBeer = Beer.query.filter(Beer.primaryBeerStyle == beerList[id].primaryBeerStyle).limit(4)
                if newBeer:
                    for each in newBeer:
                        if each.id not in params:
                            beerList.append(each)
                            params[3] = each.id
                            break
            
    return render_template('customer/product.html', data = beerList, view = 4)

@customerView.route('/customer/checkout', methods=['GET','POST'])
def checkout():
    total = findTotal(cart)
    if request.method == 'POST':
        if request.form['button'] == 'back':
            return redirect(url_for('customerView.products', page = 0))
        elif request.form['button'] == 'continue':
            cart.clear()
            return redirect(url_for('customerView.products', page = 0))
    
    return render_template('customer/checkout.html', data = cart, total = total, view = 4)