#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: __init__.py.py
@time: 2017/11/8 下午3:45
"""
from flask import Blueprint

home = Blueprint("home",__name__)

import app.home.views