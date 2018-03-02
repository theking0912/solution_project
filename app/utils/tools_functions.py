#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: tools_functions.py
@time: 2018/2/27 下午2:34
"""
import cx_Oracle


def conn_db():
    # conn = cx_Oracle.connect('system', 'system', 'ORCL_LOC')
    conn = cx_Oracle.connect('BIetluser', 'qawsedrF123', 'SHUHAI_PRD')
    return conn


def sqlDML_a(sql):
    conn = conn_db()
    cr = conn.cursor()
    cr.execute(sql)
    tables = cr.fetchall()
    cr.close()
    conn.commit()
    conn.close()
    return tables

