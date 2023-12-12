from flask import Blueprint,render_template,flash,redirect,url_for,request
from .scripts import comparePasswords
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['button'] == 'search':
            sTerm = request.form.get('search')
            return redirect(url_for('customerView.search', term = sTerm))
        if request.form['button'] == 'products':
            return redirect(url_for('customerView.products', page = 0))
        if request.form['button'] == 'specials':
            return redirect(url_for('customerView.specials'))
    
    return render_template("login/home.html", view = 4)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user = User.query.filter(User.name == username).first()
            if user:
                password = request.form.get('password')
                if comparePasswords(password, user):
                    if user.role == 1:
                        return redirect(url_for('adminView.admin'))
                    elif user.role == 2:
                        return redirect(url_for('retailerView.retailer'))
                    elif user.role == 3:
                        return redirect(url_for('kioskView.kiosk'))
                else:
                    flash('Incorrect Password')
            else:
                flash('Incorrect Username')
    
    return render_template("login/login.html", view = 0)