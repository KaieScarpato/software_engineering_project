from flask import Blueprint,render_template,flash,redirect,url_for,request
import os

kioskView = Blueprint('kioskView', __name__)

@kioskView.route('/kiosk', methods=['GET', 'POST'])
def kiosk():
    if request.method == 'POST':
        if request.form['button'] == 'backup':
            path = os.getcwd()
            flag = os.system(f'COPY {path}\\instance\\database.db {path}\\backup\\backup.db')
            print(flag)
            if flag == 0:
                flash("Backup Successful")
            else:
                flash("Backup Unsuccessful")
    return render_template("kiosk/kiosk.html", view = 3)