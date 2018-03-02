#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: app.py
@time: 2017/12/5 上午11:24
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1 style='color:red'>hello world</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
