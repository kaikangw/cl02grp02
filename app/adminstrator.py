from flask import Blueprint, render_template, redirect, request, url_for, flash
from jinja2 import TemplateNotFound
from app.generalFunctions import create_account, get_alluser_list, get_user_details, change_details, getuserid, delete_user

adminstrator = Blueprint('admin', __name__)

current_uid = 0


@adminstrator.route('/main')
def admin_page():
    return render_template("admin/admin_main.html")

@adminstrator.route('/create', methods=["GET","POST"])
def createAccount():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        accountType = request.form["accountType"]
        if create_account(username,email,accountType,password):
            flash("Successful Account Creation!")
            return render_template("admin/admin_create.html")
        else:
            flash("User already exists!")
            return render_template("admin/admin_create.html")   
    return render_template("admin/admin_create.html")

@adminstrator.route('edit', methods=["GET","POST"])
def editAccount():
    users = get_alluser_list()
    return render_template("admin/admin_edit.html", users = users, chose = "False")

@adminstrator.route('edit_<user>', methods=["GET","POST"])
def editFor(user):
    
    chosenUser = get_user_details(user)
    current_uid = getuserid(user)
    
    if request.method == "POST":
        
        username = request.form["username"]
        email = request.form["email"]
        accountType = request.form["type"]
        tenancy = request.form["tenancy"]
        instituition = request.form["instituition"]
        location = request.form["location"]
        description = request.form["description"]
        password = request.form["password"]
        print("This is the password: "+password)
        change_details(current_uid,username,email,accountType,instituition,tenancy, description, location, password)

        return redirect(url_for("admin.editAccount"))

    return render_template("admin/admin_edit.html", user = chosenUser, chose = "True")




@adminstrator.route('/delete')
def deleteAccount():
    users = get_alluser_list()
    return render_template("admin/admin_delete.html", users = users)

@adminstrator.route('/deleteUser/<user>')
def deleteUser(user):
    print("chosen acc: "+user)
    uid = getuserid(user)
    delete_user(uid)
    return redirect(url_for("admin.deleteAccount"))
