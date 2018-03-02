# !/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: corr.py
@time: 2018/2/11 下午4:09
"""
import xlrd

from datetime import date, datetime

import xlwt


def read_excel():
    ExcelFile = xlrd.open_workbook(r'/Users/lishun/PycharmProjects/solution_project/app/tools/价格相关系数.xlsx')
    sheet = ExcelFile.sheet_by_index(0)
    table_detail = []
    for x in range(1, sheet.nrows):#227
        if x >= 2:
            for y in range(1, sheet.ncols):#224
                cell_value = sheet.cell(x, y).value
                if y >= 2 and cell_value != '':
                    if float(cell_value) >= float(-1) and float(cell_value) <= float(-0.8):
                        a = sheet.cell(1, y).value
                        b = sheet.cell(x, 1).value
                        lines_detail = [a, b, cell_value]
                        if lines_detail != []:
                            table_detail.append(lines_detail)
                        else:
                            continue
    return table_detail

def export_excel(table_detail):
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=False)  # 创建sheet
    for v in range(0,len(table_detail)):
        sheet1.write(v, 0, table_detail[v][0])
        sheet1.write(v, 1, table_detail[v][1])
        sheet1.write(v, 2, table_detail[v][2])
    f.save(r'/Users/lishun/PycharmProjects/solution_project/app/tools/result_-0.8~-1.xls')  # 保存文件


if __name__ == '__main__':
    e = read_excel()
    print(len(e))
    export_excel(e)
