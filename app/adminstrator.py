from flask import Blueprint, render_template, redirect, request, url_for, flash
from jinja2 import TemplateNotFound
from app.generalFunctions import create_account

adminstrator = Blueprint('admin', __name__)

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

@adminstrator.route('edit')
def editAccount():
    return render_template("admin/admin_edit.html")

@adminstrator.route('/delete')
def deleteAccount():
    return render_template("admin/admin_delete.html")
