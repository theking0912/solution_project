# !/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: forms.py
@time: 2017/11/8 下午3:46
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:122461@127.0.0.1:3306/seckill"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class People(db.Model):
    __tablename__ = "peoples"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age= db.Column(db.Integer)

    def __repr__(self):
        return "<%r %r %r>" % (self.id, self.name, self.age)

if __name__ == "__main__":
    # step 0 : 创建数据库并指定字符集utf8
    # CREATE DATABASE IF NOT EXISTS movie DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

    # step 1 : 创建表
    db.create_all()



    # step 2 : 添加角色和管理员
    # role = Role(
    #     name="超级管理员",
    #     auths="",
    #     addtime=datetime.now()
    # )
    # db.session.add(role)
    # db.session.commit()
    #
    # from werkzeug.security import generate_password_hash  # 生成hash密码
    #
    # admin = Admin(
    #     name="leroylee",
    #     pwd=generate_password_hash("leroylee"),
    #     is_super=0,
    #     role_id=1
    # )
    # db.session.add(admin)
    # db.session.commit()
