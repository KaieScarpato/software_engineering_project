from flask import Blueprint,render_template,flash,redirect,url_for,request

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['button'] == 'customer':
            return redirect(url_for('customerView.customer'))
        if request.form['button'] == 'admin':
            return redirect(url_for('auth.adminVerify'))
        if request.form['button'] == 'kiosk':
            return redirect(url_for('kioskView.kiosk'))
        if request.form['button'] == 'retailer':
            return redirect(url_for('retailerView.retailer'))
    
    return render_template("login/login.html")

@auth.route('/adminVerify', methods=['GET', 'POST'])
def adminVerify():
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            if password == "password":
                return redirect(url_for('adminView.admin'))
            else:
                flash('login unseccessful')
    return render_template("login/adminVerify.html")
