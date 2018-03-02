#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: __init__.py.py
@time: 2017/11/8 下午3:44
"""
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:122461@127.0.0.1:3306/precision_business"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Shuhai2017@10.2.222.52:3306/precision_business"
app.config["SQLALCHEMY_BINDS"] = {
    'tools_db':'oracle+cx_oracle://bietluser:qawsedrF123@SHUHAI_PRD'
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "3414f2dc9f6d4782877504a1d3d2e0a7"
app.config["REDIS_URL"] = "redis://localhost:6379/0"
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")
app.debug = True

db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
