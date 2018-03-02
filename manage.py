#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: manage.py.py
@time: 2017/12/5 上午11:10
"""
from app import app
from flask_script import Manager

manager = Manager(app)

if __name__ == "__main__":
    app.run()