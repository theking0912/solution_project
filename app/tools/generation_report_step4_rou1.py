# -*- coding:utf-8 -*-
import os

import cx_Oracle
import xlwt
import datetime
from app.utils import tools_functions as tf

# order_date = datetime.datetime.now().strftime('%Y%m%d')

# 1、先平谷和平谷区匹配，并将匹配出的元素在，怀柔区删掉；
# 2、再匹配怀柔区
# 3、最后匹配门头沟区
# special_list = ['平谷', '怀柔', '门头沟']
# special_ping = ['石园', '顺义', '马坡', '石门', '国展', '后沙峪']
# special_huai = ['石园', '马坡', '石门', '顺义', '后沙峪', '国展', '北七家', '立水桥', '红军营', '北苑', '天通苑']
# special_men = ['门头沟', '西小口', '回龙观', '二拨子', '上地东', '西北旺', '清河']



today = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=0), '%Y%m%d%H%M%S')
dir = "/Users/lishun/Documents/yunfei/data/"
# dir = "/usr/local/nginx/html/solution_project/app/static/yunfei/data/"

query_table_a_temp = """select a.station_name,
       a.box_sum,
       a.who_first,
       a.drivers,
       a.lines,
       nvl(e.remark, c.remark) as remark,
       a.order_date
  from tbl_table_a a
 outer apply (select remark
                from point_2_address b
               where b.station_begin = a.station_name1) c
 outer apply (select remark
                from point_2_address d
               where d.station_begin = a.station_name2) e
 where substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'
"""

query_table_b_temp = """select a.station_name,
       a.box_sum,
       a.drivers,
       b.remark,
       a.order_date
  from tbl_table_b a
  left join point_2_address b
    on b.station_begin = a.station_name
 where substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

sql_str_temp = """select * from tbl_box_line_result where point_type <> 'C' and substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

str_z_temp = """select * from tbl_trans_things_num where substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

insert_str_a = """insert into TBL_TABLE_A
  (STATION_NAME,BOX_SUM, WHO_FIRST, DRIVERS, LINES, REMARK, ORDER_DATE, STATION_NAME1,STATION_NAME2)
values
  (:STATION_NAME,:BOX_SUM, :WHO_FIRST, :DRIVERS, :LINES, :REMARK, :ORDER_DATE, :STATION_NAME1,:STATION_NAME2)"""

insert_str_b = """insert into TBL_TABLE_B
  (STATION_NAME,BOX_SUM, DRIVERS, REMARK, ORDER_DATE)
values
  (:STATION_NAME,:BOX_SUM, :DRIVERS, :REMARK, :ORDER_DATE)"""

query_str_all = """select * from tbl_box_line_result_r where substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

query_str_tbl_b = """select *
  from tbl_box_line_result_p
 where substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'
 order by sum_per_box_num desc"""

insert_str_r = """insert into tbl_box_line_result_r
  (STATION_BEGIN,  STATION_MID,  STATION_END,  LINE1_LENGTH,  LINE2_LENGTH,  LINE_BEGIN,  LINE_MID,  LINE_END,  LENGTH_SUM,  BOX_BEGIN,  BOX_MID,  BOX_END,  SUM_BOX_NUM,  POINT_TYPE)
values
  (:STATION_BEGIN,  :STATION_MID,  :STATION_END,  :LINE1_LENGTH,  :LINE2_LENGTH,  :LINE_BEGIN,  :LINE_MID,  :LINE_END,  :LENGTH_SUM,  :BOX_BEGIN,  :BOX_MID,  :BOX_END,  :SUM_BOX_NUM,  :POINT_TYPE)"""

query_str_find_sp_temp = """select *
  from tbl_box_line_result_r_temp
 where ((station_begin = '#special_station#' and
       substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#' and
       point_type = 'B' and
       station_end in (#zoo_list#))
    or (station_end = '#special_station#' and
       substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#' and
       point_type = 'B' and
       station_begin in (#zoo_list#)))
   and sum_box_num <= 170"""

query_str_find_temp1 = """select station_begin,
       station_mid,
       station_end
  from tbl_box_line_result_r
 where (station_begin = '#station#'
    or station_mid = '#station#'
    or station_end = '#station#')
   and station_begin not in (#station_list#)
   and station_mid not in (#station_list#)
   and station_end not in (#station_list#)
   and substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

query_str_find_temp2 = """select station_begin,
       station_mid,
       station_end
  from tbl_box_line_result_p
 where (station_begin = '#station#'
    or station_mid = '#station#'
    or station_end = '#station#')
   and station_begin not in (#station_list#)
   and station_mid not in (#station_list#)
   and station_end not in (#station_list#)
   and substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

query_str_find_temp = """select station_begin,
       station_mid,
       station_end
  from tbl_box_line_result_r
 where (station_begin = '#station#'
    or station_mid = '#station#'
    or station_end = '#station#')
   and substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

query_who_first_temp = """select *
  from tbl_box_line_result_r
 where station_begin = '#station_begin#'
   and station_mid = '#station_mid#'
   and station_end = '#station_end#'
   and substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

query_who_first_sp_temp = """select *
  from tbl_box_line_result_r_temp
 where station_begin = '#station_begin#'
   and station_mid = '#station_mid#'
   and station_end = '#station_end#'
   and substr(to_char(order_date, 'yyyymmdd'), 1, 8) = '#order_date#'"""

sql_order_date = """select to_char(order_date,'yyyymmdd') order_date from(select distinct order_date from tbl_trans_things_num order by order_date desc) where rownum = 1"""


def conn_db():
    # conn = cx_Oracle.connect('system', 'system', 'ORCL_LOC')
    conn = cx_Oracle.connect('BIetluser', 'qawsedrF123', 'SHUHAI_PRD')
    return conn


delete_sql_str_a = """delete from tbl_table_a where substr(to_char(order_date,'yyyymmdd'),1,8) = '#order_date#'"""
delete_sql_str_b = """delete from tbl_table_b where substr(to_char(order_date,'yyyymmdd'),1,8) = '#order_date#'"""


def sqlDML_a(sql):
    conn = conn_db()
    cr = conn.cursor()
    cr.execute(sql)
    tables = cr.fetchall()
    cr.close()
    conn.commit()
    conn.close()
    return tables


def sqlDML(sql):
    conn = conn_db()
    cr = conn.cursor()
    cr.execute(sql)
    cr.close()
    conn.commit()
    conn.close()


def save_data(sql, bindVar):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(sql, bindVar)
    cursor.close()
    conn.commit()
    conn.close()


# 装载数据
def load_data(a, b, c, d, e, f, g, h, i):
    STATION_NAME = a
    BOX_SUM = b
    WHO_FIRST = c
    DRIVERS = d
    LINES = e
    REMARK = f
    ORDER_DATE = g
    STATION_NAME1 = h
    STATION_NAME2 = i
    bindVar = {'STATION_NAME': STATION_NAME, 'BOX_SUM': BOX_SUM, 'WHO_FIRST': WHO_FIRST, 'DRIVERS': DRIVERS,
               'LINES': LINES, 'REMARK': REMARK, 'ORDER_DATE': ORDER_DATE, 'STATION_NAME1': STATION_NAME1,
               'STATION_NAME2': STATION_NAME2}
    save_data(insert_str_a, bindVar)


def set_style(name, height, bold=False, italic=False, format_type='General', horz=xlwt.Alignment.HORZ_CENTER,
              vert=xlwt.Alignment.VERT_CENTER):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    font.italic = italic

    alignment = xlwt.Alignment()
    alignment.horz = horz
    alignment.vert = vert
    style.font = font
    style.alignment = alignment
    style.font = font
    style.num_format_str = format_type

    borders = xlwt.Borders()
    borders.left = 6
    borders.right = 6
    borders.top = 6
    borders.bottom = 6

    style.borders = borders

    return style


# 获取血量列表------------l(c)
# 所有在范围内的点---------m(m)
# 总血量-----------------q(blood_num)
# 血量列表---------------a(blood_list_temp)
# 初始化数据
def init_data(sql):
    l = sqlDML_a(sql)
    m = []
    blood_list = []
    for v in l:
        m.append(v[0])
        if v[1] != '-':
            m.append(v[1])
        if v[2] != '-':
            m.append(v[2])
    m.sort()
    a = set(m)
    c = []
    for v in a:
        b = m.count(v)
        c.append((v, b))
    c.sort(key=lambda k: k[1])
    loop_c = 0
    blood_num = 0
    for x in c:
        blood_list.append(x[1])
        loop_c = loop_c + 1
        blood_num = blood_num + x[1]
    blood_list_temp = list(set(blood_list))

    return c, m, blood_num, blood_list_temp


# 获取剩余m1
def get_parm(n, m):
    m = list(m)
    for y in n:
        for v in range(len(m)):
            if y in m:
                m.remove(y)
    return m


# 获取血量列表m,l,blood_list,blood_num,j(组合)
# 参数j为组合，m为元素集合
def get_level(j, p):
    next_data_list = []
    blood_list = []
    m = list(p)
    m.sort()
    a = set(m)
    l = []
    for v in a:
        b = m.count(v)
        l.append((v, b))
    l.sort(key=lambda k: k[1])
    loop_c = 0
    blood_num = 0
    for x in l:
        blood_list.append(x[1])
        loop_c = loop_c + 1
        blood_num = blood_num + x[1]
    blood_list = list(set(blood_list))
    next_data_list.append(m)
    next_data_list.append(l)
    next_data_list.append(blood_list)
    next_data_list.append(j)
    next_data_list.append(blood_num)

    return next_data_list


def split_station(station_a):
    if '-->' in station_a:
        station_name = str(station_a).split('-->')
        if '[' in station_name[0]:
            station_one = station_name[0][:-3]
            station_two = station_name[1]
        elif '[' in station_name[1]:
            station_one = station_name[0]
            station_two = station_name[1][:-3]
        else:
            station_one = station_name[0]
            station_two = station_name[1]
    else:
        if '[' in station_a:
            station_one = station_a[:-3]
            station_two = ''
        else:
            station_one = station_a
            station_two = ''

    return station_one, station_two


def get_max_blood(station_list, station_list_special, special_list, class_blood_list,order_date):
    chose_point = class_blood_list[-1][0]
    if chose_point[2] in special_list or chose_point[0] in special_list:
        query_who_first = query_who_first_sp_temp.replace('#station_begin#', chose_point[0]).replace(
            '#station_mid#', chose_point[1]).replace('#station_end#', chose_point[2]).replace('#order_date#',
                                                                                              order_date)
    else:
        query_who_first = query_who_first_temp.replace('#station_begin#', chose_point[0]).replace(
            '#station_mid#', chose_point[1]).replace('#station_end#', chose_point[2]).replace('#order_date#',
                                                                                              order_date)
    who_first_tables = sqlDML_a(query_who_first)
    if chose_point[1] == chose_point[2] == '-':
        station_a = who_first(special_list, who_first_tables[0])
        if who_first_tables[0][12] >= 270:
            station_all = split_station(station_a[0])
            load_data(a=station_a[0], b=station_a[2],
                      c=station_a[1], d='', e=station_a[0],
                      f='',
                      g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0], i=station_all[1])
            station_all = split_station(station_a[3])
            load_data(a=station_a[3], b=station_a[5],
                      c=station_a[4], d='', e=station_a[3],
                      f='',
                      g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0], i=station_all[1])
            station_list.append(chose_point[0])
        else:
            station_all = split_station(station_a[0])
            load_data(a=station_a[0], b=station_a[2],
                      c=station_a[1], d='', e=station_a[0],
                      f='',
                      g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0], i=station_all[1])
            station_list.append(chose_point[0])
    elif chose_point[1] == '-':
        station_a = who_first(special_list, who_first_tables[0])
        if who_first_tables[0][12] >= 270:
            station_all = split_station(station_a[0])
            load_data(a=who_first_tables[0][0] + '-->' + who_first_tables[0][2], b=station_a[2],
                      c=station_a[1],
                      d='', e=station_a[0], f='', g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0],
                      i=station_all[1])
            station_all = split_station(station_a[3])
            load_data(a=who_first_tables[0][0] + '-->' + who_first_tables[0][2], b=station_a[5],
                      c=station_a[4],
                      d='', e=station_a[3], f='', g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0],
                      i=station_all[1])
            station_list.append(chose_point[0])
            station_list.append(chose_point[2])
        else:
            station_all = split_station(station_a[0])
            load_data(a=who_first_tables[0][0] + '-->' + who_first_tables[0][2], b=station_a[2],
                      c=station_a[1],
                      d='', e=station_a[0], f='', g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0],
                      i=station_all[1])
            station_list.append(chose_point[0])
            station_list.append(chose_point[2])
    else:
        station_a = who_first(special_list,who_first_tables[0])
        station_all = split_station(station_a[0])
        load_data(
            a=who_first_tables[0][0] + '-->' + who_first_tables[0][1] + '-->' + who_first_tables[0][2],
            b=station_a[2],
            c=station_a[1],
            d='', e=station_a[0], f='',
            g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0], i=station_all[1])
        station_all = split_station(station_a[3])
        load_data(
            a=who_first_tables[0][0] + '-->' + who_first_tables[0][1] + '-->' + who_first_tables[0][2],
            b=station_a[5],
            c=station_a[4],
            d='', e=station_a[3], f='',
            g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=station_all[0], i=station_all[1])
        station_list.append(chose_point[0])
        station_list.append(chose_point[1])
        station_list.append(chose_point[2])

    return chose_point


def get_max_station(station_list, station_list_special, special_list, m, x, zoo_list,order_date):
    class_blood_list = []
    for o in x:
        w = ''
        if o in special_list:
            for e in range(len(zoo_list)):
                w = w + "'" + zoo_list[e] + "',"
            w = w[:-1]
            query_str_find = query_str_find_sp_temp.replace('#special_station#', o).replace('#zoo_list#',
                                                                                            w).replace(
                '#order_date#', order_date)
        else:
            if zoo_list == 'second':
                for e in range(len(station_list)):
                    w = w + "'" + station_list[e] + "',"
                w = w[:-1]
                query_str_find = query_str_find_temp2.replace('#station#', o).replace('#order_date#',
                                                                                      order_date).replace(
                    '#station_list#', w)
            else:
                if len(station_list) != 0:
                    for e in range(len(station_list)):
                        w = w + "'" + station_list[e] + "',"
                    w = w[:-1]
                    query_str_find = query_str_find_temp1.replace('#station#', o).replace('#order_date#',
                                                                                          order_date).replace(
                        '#station_list#', w)
                else:
                    query_str_find = query_str_find_temp.replace('#station#', o).replace('#order_date#',
                                                                                         order_date)
        y = sqlDML_a(query_str_find)
        for j in y:
            n = list(m)
            m1 = get_parm(j[:3], n)
            l1 = get_level(j[:3], m1)
            class_blood_list.append((l1[3], l1[4]))
        class_blood_list.sort(key=lambda k: k[1])
    return class_blood_list


# 行走路线
def who_first(special_list, str_list):
    station_a = []
    v = str_list
    # 平谷类
    if v[0] in special_list or v[2] in special_list:
        if v[2] == '-':
            lines = v[0]
            load_first = v[0] + '(' + str(v[9]) + ')'
            station_a.append(lines)
            station_a.append(load_first)
            station_a.append(v[12])
        else:
            if v[5] >= v[7]:
                lines = v[2] + '-->' + v[0]
                load_first = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(v[11]) + ')'
            else:
                lines = v[0] + '-->' + v[2]
                load_first = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(v[9]) + ')'
            station_a.append(lines)
            station_a.append(load_first)
            station_a.append(v[12])

    if v[13] == 'A':
        if v[12] >= 270:
            if is_float(v[12]) is True:
                lines1 = v[0] + '[1]'
                box_num1 = (v[12] - 0.5) / 2
                load_first1 = v[0] + '[1]' + '(' + str(box_num1) + ')'
                box_num2 = (v[12] - 0.5) / 2 + 0.5
                lines2 = v[0] + '[1]'
                load_first2 = v[0] + '[2]' + '(' + str(box_num2) + ')'
            else:
                s = str(v[12] / 2)
                if is_float(s) is True:
                    lines1 = v[0] + '[1]'
                    box_num1 = (v[12] / 2) - 0.5
                    load_first1 = v[0] + '[1]' + '(' + str(box_num1) + ')'
                    box_num2 = (v[12] / 2) + 0.5
                    lines2 = v[0] + '[1]'
                    load_first2 = v[0] + '[2]' + '(' + str(box_num2) + ')'
                else:
                    lines1 = v[0] + '[1]'
                    box_num1 = (v[12] / 2)
                    load_first1 = v[0] + '[1]' + '(' + str(box_num1) + ')'
                    box_num2 = (v[12] / 2)
                    lines2 = v[0] + '[1]'
                    load_first2 = v[0] + '[2]' + '(' + str(box_num2) + ')'
            station_a.append(lines1)
            station_a.append(load_first1)
            station_a.append(box_num1)
            station_a.append(lines2)
            station_a.append(load_first2)
            station_a.append(box_num2)
        else:
            lines1 = v[0]
            box_num1 = v[12]
            load_first1 = v[0] + '(' + str(box_num1) + ')'
            station_a.append(lines1)
            station_a.append(load_first1)
            station_a.append(box_num1)

    # B类型按照路程长短安排先行车
    if v[13] == 'B':
        if v[12] >= 270:
            if v[5] >= v[7]:
                if is_float(v[12]) is True:
                    box_num1 = (v[12] - 0.5) / 2
                    box_num2 = (v[12] - 0.5) / 2 + 0.5
                    if v[9] > v[11]:
                        lines1 = v[2] + '-->' + v[0] + '[1]'
                        lines2 = v[0] + '[2]'
                        load_first1 = v[0] + '(' + str(box_num1 - v[11]) + ')' + '、' + v[2] + '(' + str(v[11]) + ')'
                        load_first2 = v[0] + '(' + str(box_num2) + ')'
                    else:
                        lines1 = v[2] + '[1]-->' + v[0]
                        lines2 = v[2] + '[2]'
                        load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                        load_first2 = v[2] + '(' + str(box_num2) + ')'
                else:
                    s = str(v[12] / 2)
                    if is_float(s) is True:
                        box_num1 = (v[12] / 2) - 0.5
                        box_num2 = (v[12] / 2) + 0.5
                        if v[9] > v[11]:
                            lines1 = v[2] + '-->' + v[0] + '[1]'
                            lines2 = v[0] + '[2]'
                            load_first1 = v[0] + '(' + str(box_num1 - v[11]) + ')' + '、' + v[2] + '(' + str(
                                v[11]) + ')'
                            load_first2 = v[0] + '(' + str(box_num2) + ')'
                        else:
                            lines1 = v[2] + '[1]-->' + v[0]
                            lines2 = v[2] + '[2]'
                            load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                            load_first2 = v[2] + '(' + str(box_num2) + ')'
                    else:
                        box_num1 = (v[12] / 2)
                        box_num2 = (v[12] / 2)
                        if v[9] > v[11]:
                            lines1 = v[2] + '-->' + v[0] + '[1]'
                            lines2 = v[0] + '[2]'
                            load_first1 = v[0] + '(' + str(box_num1 - v[11]) + ')' + '、' + v[2] + '(' + str(
                                v[11]) + ')'
                            load_first2 = v[0] + '(' + str(box_num2) + ')'
                        else:
                            lines1 = v[2] + '[1]-->' + v[0]
                            lines2 = v[2] + '[2]'
                            load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                            load_first2 = v[2] + '(' + str(box_num2) + ')'
                station_a.append(lines1)
                station_a.append(load_first1)
                station_a.append(box_num1)
                station_a.append(lines2)
                station_a.append(load_first2)
                station_a.append(box_num2)
            else:
                if is_float(v[12]) is True:
                    box_num1 = (v[12] - 0.5) / 2
                    box_num2 = (v[12] - 0.5) / 2 + 0.5
                    if v[9] > v[11]:
                        lines1 = v[0] + '[1]' + '-->' + v[2]
                        lines2 = v[0] + '[2]'
                        load_first1 = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(box_num1 - v[11]) + ')'
                        load_first2 = v[0] + '(' + str(box_num2) + ')'
                    else:
                        lines1 = v[0] + '-->' + v[2] + '[1]'
                        lines2 = v[2] + '[2]'
                        load_first1 = v[2] + '(' + str(box_num1 - v[9]) + ')' + '、' + v[0] + '(' + str(v[9]) + ')'
                        load_first2 = v[2] + '(' + str(box_num2) + ')'
                else:
                    s = str(v[12] / 2)
                    if is_float(s) is True:
                        box_num1 = (v[12] / 2) - 0.5
                        box_num2 = (v[12] / 2) + 0.5
                        if v[9] > v[11]:
                            lines1 = v[0] + '[1]' + '-->' + v[2]
                            lines2 = v[0] + '[2]'
                            load_first1 = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(
                                box_num1 - v[11]) + ')'
                            load_first2 = v[0] + '(' + str(box_num2) + ')'
                        else:
                            lines1 = v[0] + '-->' + v[2] + '[1]'
                            lines2 = v[2] + '[2]'
                            load_first1 = v[2] + '(' + str(box_num1 - v[9]) + ')' + '、' + v[0] + '(' + str(v[9]) + ')'
                            load_first2 = v[2] + '(' + str(box_num2) + ')'
                    else:
                        box_num1 = (v[12] / 2)
                        box_num2 = (v[12] / 2)
                        if v[9] > v[11]:
                            lines1 = v[0] + '[1]' + '-->' + v[2]
                            lines2 = v[0] + '[2]'
                            load_first1 = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(
                                box_num1 - v[11]) + ')'
                            load_first2 = v[0] + '(' + str(box_num2) + ')'
                        else:
                            lines1 = v[0] + '-->' + v[2] + '[1]'
                            lines2 = v[2] + '[2]'
                            load_first1 = v[2] + '(' + str(box_num1 - v[9]) + ')' + '、' + v[0] + '(' + str(v[9]) + ')'
                            load_first2 = v[2] + '(' + str(box_num2) + ')'
                station_a.append(lines1)
                station_a.append(load_first1)
                station_a.append(box_num1)
                station_a.append(lines2)
                station_a.append(load_first2)
                station_a.append(box_num2)
        else:
            if v[5] >= v[7]:
                lines = v[2] + '-->' + v[0]
                load_first = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(v[11]) + ')'
            else:
                lines = v[0] + '-->' + v[2]
                load_first = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(v[9]) + ')'
            station_a.append(lines)
            station_a.append(load_first)
            station_a.append(v[12])
    # C类型按照拆车安排先行车
    if v[13] == 'C':
        if v[9] >= v[10]:
            if v[9] >= v[11]:
                if is_float(v[12]) is True:
                    box_num1 = (v[12] - 0.5) / 2
                    box_num2 = (v[12] - 0.5) / 2 + 0.5
                    lines1 = v[0] + '[1]-->' + v[1]
                    load_first1 = v[1] + '(' + str(v[10]) + ')' + '、' + v[0] + '(' + str(box_num1 - v[10]) + ')'
                    lines2 = v[0] + '[2]-->' + v[2]
                    load_first2 = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(box_num2 - v[11]) + ')'
                    station_a.append(lines1)
                    station_a.append(load_first1)
                    station_a.append(box_num1)
                    station_a.append(lines2)
                    station_a.append(load_first2)
                    station_a.append(box_num2)
                else:
                    s = str(v[12] / 2)
                    if is_float(s) is True:
                        box_num1 = (v[12] / 2) - 0.5
                        box_num2 = (v[12] / 2) + 0.5
                        lines1 = v[0] + '[1]-->' + v[1]
                        load_first1 = v[1] + '(' + str(v[10]) + ')' + '、' + v[0] + '(' + str(box_num1 - v[10]) + ')'
                        lines2 = v[0] + '[2]-->' + v[2]
                        load_first2 = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(box_num2 - v[11]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)
                    else:
                        box_num1 = (v[12] / 2)
                        box_num2 = (v[12] / 2)
                        lines1 = v[0] + '[1]-->' + v[1]
                        load_first1 = v[1] + '(' + str(v[10]) + ')' + '、' + v[0] + '(' + str(box_num1 - v[10]) + ')'
                        lines2 = v[0] + '[2]-->' + v[2]
                        load_first2 = v[2] + '(' + str(v[11]) + ')' + '、' + v[0] + '(' + str(box_num2 - v[11]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)
            else:
                if is_float(v[12]) is True:
                    box_num1 = (v[12] - 0.5) / 2
                    box_num2 = (v[12] - 0.5) / 2 + 0.5
                    lines1 = v[2] + '[1]-->' + v[0]
                    load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                    lines2 = v[2] + '[2]-->' + v[1]
                    load_first2 = v[1] + '(' + str(v[10]) + ')' + '、' + v[2] + '(' + str(box_num2 - v[10]) + ')'
                    station_a.append(lines1)
                    station_a.append(load_first1)
                    station_a.append(box_num1)
                    station_a.append(lines2)
                    station_a.append(load_first2)
                    station_a.append(box_num2)
                else:
                    s = str(v[12] / 2)
                    if is_float(s) is True:
                        box_num1 = (v[12] / 2) - 0.5
                        box_num2 = (v[12] / 2) + 0.5
                        lines1 = v[2] + '[1]-->' + v[0]
                        load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                        lines2 = v[2] + '[2]-->' + v[1]
                        load_first2 = v[1] + '(' + str(v[10]) + ')' + '、' + v[2] + '(' + str(box_num2 - v[10]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)
                    else:
                        box_num1 = (v[12] / 2)
                        box_num2 = (v[12] / 2)
                        lines1 = v[2] + '[1]-->' + v[0]
                        load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                        lines2 = v[2] + '[2]-->' + v[1]
                        load_first2 = v[1] + '(' + str(v[10]) + ')' + '、' + v[2] + '(' + str(box_num2 - v[10]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)
        else:
            if v[10] >= v[11]:
                if is_float(v[12]) is True:
                    box_num1 = (v[12] - 0.5) / 2
                    box_num2 = (v[12] - 0.5) / 2 + 0.5
                    lines1 = v[1] + '[1]-->' + v[0]
                    load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[1] + '(' + str(box_num1 - v[9]) + ')'
                    lines2 = v[1] + '[2]-->' + v[2]
                    load_first2 = v[2] + '(' + str(v[11]) + ')' + '、' + v[1] + '(' + str(box_num2 - v[11]) + ')'
                    station_a.append(lines1)
                    station_a.append(load_first1)
                    station_a.append(box_num1)
                    station_a.append(lines2)
                    station_a.append(load_first2)
                    station_a.append(box_num2)
                else:
                    s = str(v[12] / 2)
                    if is_float(s) is True:
                        box_num1 = (v[12] / 2) - 0.5
                        box_num2 = (v[12] / 2) + 0.5
                        lines1 = v[1] + '[1]-->' + v[0]
                        load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[1] + '(' + str(box_num1 - v[9]) + ')'
                        lines2 = v[1] + '[2]-->' + v[2]
                        load_first2 = v[2] + '(' + str(v[11]) + ')' + '、' + v[1] + '(' + str(box_num2 - v[11]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)
                    else:
                        box_num1 = (v[12] / 2)
                        box_num2 = (v[12] / 2)
                        lines1 = v[1] + '[1]-->' + v[0]
                        load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[1] + '(' + str(box_num1 - v[9]) + ')'
                        lines2 = v[1] + '[2]-->' + v[2]
                        load_first2 = v[2] + '(' + str(v[11]) + ')' + '、' + v[1] + '(' + str(box_num2 - v[11]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)
            else:
                if is_float(v[12]) is True:
                    box_num1 = (v[12] - 0.5) / 2
                    box_num2 = (v[12] - 0.5) / 2 + 0.5
                    lines1 = v[2] + '[1]-->' + v[0]
                    load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                    lines2 = v[2] + '[2]-->' + v[1]
                    load_first2 = v[1] + '(' + str(v[10]) + ')' + '、' + v[2] + '(' + str(box_num2 - v[10]) + ')'
                    station_a.append(lines1)
                    station_a.append(load_first1)
                    station_a.append(box_num1)
                    station_a.append(lines2)
                    station_a.append(load_first2)
                    station_a.append(box_num2)
                else:
                    s = str(v[12] / 2)
                    if is_float(s) is True:
                        box_num1 = (v[12] / 2) - 0.5
                        box_num2 = (v[12] / 2) + 0.5
                        lines1 = v[2] + '[1]-->' + v[0]
                        load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                        lines2 = v[2] + '[2]-->' + v[1]
                        load_first2 = v[1] + '(' + str(v[10]) + ')' + '、' + v[2] + '(' + str(box_num2 - v[10]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)
                    else:
                        box_num1 = (v[12] / 2)
                        box_num2 = (v[12] / 2)
                        lines1 = v[2] + '[1]-->' + v[0]
                        load_first1 = v[0] + '(' + str(v[9]) + ')' + '、' + v[2] + '(' + str(box_num1 - v[9]) + ')'
                        lines2 = v[2] + '[2]-->' + v[1]
                        load_first2 = v[1] + '(' + str(v[10]) + ')' + '、' + v[2] + '(' + str(box_num2 - v[10]) + ')'
                        station_a.append(lines1)
                        station_a.append(load_first1)
                        station_a.append(box_num1)
                        station_a.append(lines2)
                        station_a.append(load_first2)
                        station_a.append(box_num2)

    return station_a


def is_float(s):
    s = str(s)
    if s.count('.5') == 1:
        return True
    else:
        return False


def sqlDMLPROC(sql, order_date):
    conn = conn_db()
    cr = conn.cursor()
    cr.callproc(sql, [order_date])
    cr.close()
    conn.commit()
    conn.close()


def loop_result(station_list, station_list_special, special_list, special_ping, special_huai, special_men, order_date):
    query_str = query_str_all.replace('#order_date#', order_date)
    generation_data(station_list, station_list_special, special_list, special_ping, special_huai, special_men,
                    query_str, order_date)
    sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_prepare_data', order_date=order_date)
    query_str_1 = query_str_tbl_b.replace('#order_date#', order_date)
    generation_data_second(query_str_1, order_date, 'second')


def generation_data(station_list, station_list_special, special_list, special_ping, special_huai, special_men, result,
                    order_date):
    print(result)
    base_data = init_data(result)
    m = tuple(base_data[1])
    l = base_data[0]
    a = base_data[3]
    print(m)
    print(l)
    print(a)

    # 处理平谷类问题
    for sp in special_list:
        h = []
        h.append(sp)
        if sp == '平谷':
            class_blood_list = get_max_station(station_list, station_list_special, special_list, m, h, special_ping,order_date)
        elif sp == '怀柔':
            class_blood_list = get_max_station(station_list, station_list_special, special_list, m, h, special_huai,order_date)
        else:
            class_blood_list = get_max_station(station_list, station_list_special, special_list, m, h, special_men,order_date)
        # ----------------------begin获取最大生命值的组合
        if class_blood_list != []:
            chose_point = get_max_blood(station_list, station_list_special, special_list, class_blood_list,order_date)
            if chose_point[0] in special_huai:
                special_huai.remove(chose_point[0])
            elif chose_point[2] in special_huai:
                special_huai.remove(chose_point[2])
            n = list(m)
            m1 = get_parm(chose_point, n)
            all_list = get_level(chose_point, m1)
            m = all_list[0]
            l = all_list[1]
            a = all_list[2]
        else:
            station_list.append(h[0])
            station_list_special.append(h[0])
            m1 = get_parm(h, m)
            all_list = get_level(h, m1)
            m = all_list[0]
            l = all_list[1]
            a = all_list[2]

    # 处理正常数据
    for s in range(0, 100):
        a.sort()
        if a == []:
            break
        else:
            a1 = a[0]
            a.remove(a[0])
            x = []
            if l == []:
                break
            else:
                for z in l:
                    if z[1] == a1:
                        x.append(z[0])
                # ----------------------begin获取各组合对应的血量明细
                class_blood_list = get_max_station(station_list, station_list_special, special_list, m, x, '',order_date)
                if class_blood_list != []:
                    # 添加最大血量相等情况的更深的判断
                    # ----------------------begin获取最大生命值的组合
                    chose_point = get_max_blood(station_list, station_list_special, special_list, class_blood_list,order_date)
                    n = list(m)
                    m1 = get_parm(chose_point, n)
                    all_list = get_level(chose_point, m1)
                    m = all_list[0]
                    l = all_list[1]
                    a = all_list[2]
                else:
                    continue
    # 生成未分配数据
    str_z = str_z_temp.replace('#order_date#', order_date)
    tables_noline = sqlDML_a(str_z)
    for v in tables_noline:
        if v[0] not in station_list:
            STATION_NAME = v[0]
            BOX_SUM = v[2]
            DRIVERS = ''
            REMARK = ''
            ORDER_DATE = v[3]
            bindVar = {'STATION_NAME': STATION_NAME, 'BOX_SUM': BOX_SUM, 'DRIVERS': DRIVERS, 'REMARK': REMARK,
                       'ORDER_DATE': ORDER_DATE}
            save_data(insert_str_b, bindVar)
        elif v[0] in station_list_special:
            STATION_NAME = v[0]
            BOX_SUM = v[2]
            DRIVERS = ''
            REMARK = ''
            ORDER_DATE = v[3]
            bindVar = {'STATION_NAME': STATION_NAME, 'BOX_SUM': BOX_SUM, 'DRIVERS': DRIVERS, 'REMARK': REMARK,
                       'ORDER_DATE': ORDER_DATE}
            save_data(insert_str_b, bindVar)


def generation_data_second(result, order_date, sc):
    except_list = []
    table_data = sqlDML_a(result)
    for v in table_data:
        if v[0] in except_list or v[2] in except_list:
            continue
        else:
            if v[13] == 'B':
                load_data(a=v[0] + '-->' + v[2], b=v[12],
                          c=v[2] + '【' + str(v[9]) + '】、' + v[0] + '【' + str(v[11]) + '】', d='',
                          e=v[0] + '-->' + v[2], f='', g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=v[0],
                          i=v[2])
                except_list.append(v[0])
                except_list.append(v[2])
            else:
                if v[12] > 170:
                    load_data(a=v[0], b=v[12] - 135, c=v[0] + '【' + str(v[12] - 135) + '】', d='',
                              e=v[0] + '[2]', f='', g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=v[0], i='')
                    load_data(a=v[0], b=135, c=v[0] + '【' + str(135) + '】', d='',
                              e=v[0] + '[1]', f='', g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=v[0], i='')
                    except_list.append(v[0])
                else:
                    load_data(a=v[0], b=v[12], c=v[0] + '【' + str(v[12]) + '】', d='',
                              e=v[0], f='', g=datetime.datetime.strptime(order_date, '%Y%m%d'), h=v[0], i='')
                    except_list.append(v[0])

                    # # 生成未分配数据
                    # str_z = str_z_temp.replace('#order_date#', order_date)
                    # tables_noline = sqlDML_a(str_z)
                    # for v in tables_noline:
                    #     if v[0] not in station_list:
                    #         STATION_NAME = v[0]
                    #         BOX_SUM = v[2]
                    #         DRIVERS = ''
                    #         REMARK = ''
                    #         ORDER_DATE = v[3]
                    #         bindVar = {'STATION_NAME': STATION_NAME, 'BOX_SUM': BOX_SUM, 'DRIVERS': DRIVERS, 'REMARK': REMARK,
                    #                    'ORDER_DATE': ORDER_DATE}
                    #         save_data(insert_str_b, bindVar)
                    #     elif v[0] in station_list_special:
                    #         STATION_NAME = v[0]
                    #         BOX_SUM = v[2]
                    #         DRIVERS = ''
                    #         REMARK = ''
                    #         ORDER_DATE = v[3]
                    #         bindVar = {'STATION_NAME': STATION_NAME, 'BOX_SUM': BOX_SUM, 'DRIVERS': DRIVERS, 'REMARK': REMARK,
                    #                    'ORDER_DATE': ORDER_DATE}
                    #         save_data(insert_str_b, bindVar)


def export_Excel(order_date):
    newdir = dir + order_date
    if os.path.exists(dir) == False:
        os.mkdir(dir)
    if os.path.exists(newdir) == False:
        os.mkdir(newdir)
    query_table_a = query_table_a_temp.replace('#order_date#', order_date)
    query_table_b = query_table_b_temp.replace('#order_date#', order_date)
    datatable_a = sqlDML_a(query_table_a)
    # datatable_b = sqlDML_a(query_table_b)
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=False)  # 创建sheet
    sheet1.write_merge(0, 0, 0, 5, u'每日优鲜路线编排表(' + order_date + ')', set_style('微软雅黑', 350, True, False, 'General'))
    title1 = [u'序号', u'建议装车顺序', u'装车总箱数', u'司机（车辆）', u'建议路线', u'备注']
    for i in range(0, len(title1)):
        sheet1.write(1, i, title1[i], set_style('微软雅黑', 220, True, 'General'))
    for v in datatable_a:
        p = datatable_a.index(v)
        sheet1.write(2 + p, 0, p + 1, set_style('微软雅黑', 220, False, False))
        sheet1.write(2 + p, 1, v[2], set_style('微软雅黑', 220, False, False))
        sheet1.write(2 + p, 2, v[1], set_style('微软雅黑', 220, False, False))
        sheet1.write(2 + p, 3, v[3], set_style('微软雅黑', 220, False, False))
        sheet1.write(2 + p, 4, v[4], set_style('微软雅黑', 220, False, False))
        sheet1.write(2 + p, 5, v[5], set_style('微软雅黑', 220, False, False))
    # sheet1.write_merge(0, 0, 9, 13, u'每日优鲜路线编排表(' + order_date + ')', set_style('微软雅黑', 350, True, False, 'General'))
    # title2 = [u'序号', u'配送门店', u'订货量', u'司机（车辆）', u'备注']
    # for i in range(0, len(title2)):
    #     sheet1.write(1, i + 9, title2[i], set_style('微软雅黑', 220, True, 'General'))
    # for v in datatable_b:
    #     p = datatable_b.index(v)
    #     sheet1.write(2 + p, 9, p + 1, set_style('微软雅黑', 220, False, False))
    #     sheet1.write(2 + p, 10, v[0], set_style('微软雅黑', 220, False, False))
    #     sheet1.write(2 + p, 11, v[1], set_style('微软雅黑', 220, False, False))
    #     sheet1.write(2 + p, 12, v[2], set_style('微软雅黑', 220, False, False))
    #     sheet1.write(2 + p, 13, v[3], set_style('微软雅黑', 220, False, False))
    f.save(newdir + '/information_detail' + order_date + '.xls')  # 保存文件


def generation(pa_order_date):
    # pa_order_date = sqlDML_a(sql_order_date)
    # order_date = str(pa_order_date[0][0])
    # ----------------
    station_list = []
    station_list_special = []
    special_list = []
    sql_list = "SELECT STATION_POINT_NAME FROM TBL_SPECIAL_STATION WHERE STATION_TYPE = 'special_list'"
    special_list_temp = tf.sqlDML_a(sql_list)
    for b in special_list_temp:
        special_list.append(b[0])
    special_men = []
    sql_men = "SELECT STATION_POINT_NAME FROM TBL_SPECIAL_STATION WHERE STATION_TYPE = 'special_men'"
    special_men_temp = tf.sqlDML_a(sql_men)
    for b in special_men_temp:
        special_men.append(b[0])
    # ----------------
    special_huai = []
    sql_huai = "SELECT STATION_POINT_NAME FROM TBL_SPECIAL_STATION WHERE STATION_TYPE = 'special_huai'"
    special_huai_temp = tf.sqlDML_a(sql_huai)
    for b in special_huai_temp:
        special_huai.append(b[0])
    # ----------------
    special_ping = []
    sql_ping = "SELECT STATION_POINT_NAME FROM TBL_SPECIAL_STATION WHERE STATION_TYPE = 'special_ping'"
    special_ping_temp = tf.sqlDML_a(sql_ping)
    for b in special_ping_temp:
        special_ping.append(b[0])
    a = 0
    sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_init_data', order_date=pa_order_date)
    sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_preparation_parameters', order_date=pa_order_date)
    sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_generate_result', order_date=pa_order_date)
    a = a + 1
    if a == 1:
        msg = 'step1 数据准备成功'
    delete_sql_a = delete_sql_str_a.replace('#order_date#', pa_order_date)
    delete_sql_b = delete_sql_str_b.replace('#order_date#', pa_order_date)
    sqlDML(delete_sql_a)
    sqlDML(delete_sql_b)
    print('1、生成可能性开始')
    loop_result(station_list, station_list_special, special_list, special_ping, special_huai, special_men,
                pa_order_date)
    a = a + 1
    if a == 2:
        msg = 'step2 生成可能性成功'
    print('2、excel生成开始')
    export_Excel(pa_order_date)
    a = a + 1
    if a == 3:
        msg = 'step3 生成可能性Excel成功'
    print('3、excel生成完成')
    sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_result_data', order_date=pa_order_date)
    a = a + 1
    if a == 4:
        msg = 'step4 结果生成成功'
    return msg

if __name__ == '__main__':
    msg = generation('20180303')
    print(msg)
# if __name__ == '__main__':
#     for v in xxx:
#         order_date = v
#         print(order_date)
#         sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_preparation_parameters', order_date=order_date)
#         sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_generate_result', order_date=order_date)
#         station_list = []
#         station_list_special = []
#         sqlDML(delete_sql_str_a)
#         sqlDML(delete_sql_str_b)
#         print('1、生成可能性开始')
#         loop_result(order_date)
#         print('2、excel生成开始')
#         export_Excel(order_date)
#         print('3、excel生成完成')

#
# if __name__ == '__main__':
#     pa_order_date = sqlDML_a(sql_order_date)
#     order_date = str(pa_order_date[0][0])
#     sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_preparation_parameters', order_date=order_date)
#     sqlDMLPROC('BIetluser.p_m_r_y_x_pkg.p_generate_result', order_date=order_date)
#     station_list = []
#     station_list_special = []
#     delete_sql_a = delete_sql_str_a.replace('#order_date#', order_date)
#     delete_sql_b = delete_sql_str_b.replace('#order_date#', order_date)
#     sqlDML(delete_sql_a)
#     sqlDML(delete_sql_b)
#     print('1、生成可能性开始')
#     loop_result(order_date)
#     print('2、excel生成开始')
#     export_Excel(order_date)
#     print('3、excel生成完成')
