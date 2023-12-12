from flask import Blueprint,render_template,flash,redirect,url_for,request
import os

kioskView = Blueprint('kioskView', __name__)

@kioskView.route('/kiosk', methods=['GET', 'POST'])
def kiosk():
    if request.method == 'POST':
        if request.form['button'] == 'backup':
            flag = os.system('COPY C:\\Users\\kaies\\OneDrive\\Desktop\\PythonVsProjects\\SoftwareEngineeringProject\\instance\\database.db C:\\Users\\kaies\\OneDrive\\Desktop\\PythonVsProjects\\SoftwareEngineeringProject\\backup\\backup.db')
            print(flag)
            if flag == 0:
                flash("Backup Successful")
            else:
                flash("Backup Unsuccessful")
    return render_template("kiosk/kiosk.html", view = 3)