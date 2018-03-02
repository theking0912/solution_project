# -*- coding:utf-8 -*-

import os
import xlrd
import cx_Oracle
import datetime
import shutil

str_q = """select a.station_begin
  from point_2_address a"""

inster_sql_2 = """insert into tb_possiable_list
  (STATION_BEGIN, STATION_END)
values
  (:STATION_BEGIN, :STATION_END)"""

inster_sql_3 = """insert into tb_possiable_list
  (STATION_BEGIN,STATION_MID, STATION_END)
values
  (:STATION_BEGIN, :STATION_MID, :STATION_END)"""

truncate_sql = """truncate table tb_possiable_list"""

# ###############################################################################获取链接###############################################################################
def conn_db():
    conn = cx_Oracle.connect('BIetluser', 'qawsedrF123', 'SHUHAI_PRD')
    return conn


# ###############################################################################获取数据###############################################################################
def get_data(data):
    table = data.sheets()[0]
    nrows = table.nrows
    exec_str = ''
    params = []
    values = []
    for i in range(0, nrows):
        a = 0
        rowValues = table.row_values(i)
        # print('---------------------------------------------'+str(i)+'---------------------------------------------')
        if i == 0:
            for item in rowValues:
                exec_str += item + ','
                params.append(item)
            exec_str = 'values.append((' + exec_str[:-1] + '))'
        else:
            for item in rowValues:
                if 'date' in params[a]:
                    param_str = params[a] + '=xlrd.xldate.xldate_as_datetime(float(' + str(item) + '), 0)'
                else:
                    param_str = params[a] + '="' + str(item) + '"'
                exec(param_str)
                a += 1
            exec(exec_str)
    return values, params


# ###############################################################################保存数据###############################################################################
def save_data(values, data):
    conn = conn_db()
    cursor = conn.cursor()
    insert_sql_temp = create_sql_str(data)
    insert_sql = insert_sql_temp[1]
    cursor.prepare(insert_sql)
    cursor.executemany(None, values[0])
    cursor.close()
    conn.commit()
    conn.close()


# ###############################################################################保存bind数据###############################################################################
def save_data_bind(sql, bindVar):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(sql, bindVar)
    cursor.close()
    conn.commit()
    conn.close()


# ###############################################################################根据excel创建表###############################################################################
def create_table():
    conn = conn_db()
    cursor = conn.cursor()
    create_sql_temp = create_sql_str()
    create_sql = create_sql_temp[0]
    cursor.execute(create_sql)
    cursor.close()
    conn.commit()
    conn.close()


# ###############################################################################建表语句###############################################################################
def create_sql_str(data):
    table_name = data.sheet_names()[0]
    field_type = 'varchar2(2000)'
    create_table_str = 'create table ' + table_name + ' ('
    insert_values_str = 'insert into ' + table_name + ' ('
    insert_values_str_values = ''
    temp = get_data(data)
    table_files = temp[1]
    for i in range(0, len(table_files)):
        if i == len(table_files) - 1:
            create_table_str += table_files[i] + ' ' + field_type + ')'
            insert_values_str += table_files[i] + ') values ('
            insert_values_str_values += ':' + str(i + 1) + ')'
        else:
            create_table_str += table_files[i] + ' ' + field_type + ','
            insert_values_str += table_files[i] + ','
            insert_values_str_values += ':' + str(i + 1) + ','
    insert_values_str += insert_values_str_values
    return create_table_str, insert_values_str


# ###############################################################################执行sql###############################################################################
def sqlDML(sql):
    conn = conn_db()
    cr = conn.cursor()
    cr.execute(sql)
    cr.close()
    conn.commit()
    conn.close()


def sqlDML_a(sql):
    conn = conn_db()
    cr = conn.cursor()
    cr.execute(sql)
    tables = cr.fetchall()
    cr.close()
    conn.commit()
    conn.close()
    return tables


# ###############################################################################执行sp###############################################################################
def sqlDMLPROC(sql, order_date):
    conn = conn_db()
    cr = conn.cursor()
    cr.callproc(sql, [order_date])
    cr.close()
    conn.commit()
    conn.close()


# ###############################################################################循环文件名###############################################################################
def loopFilesSaveDatas(filepath):
    pathDir = os.listdir(filepath)
    today = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=0), '%Y%m%d%H%M%S')
    newdir = "/home/data/file_backup/excel_files_" + today
    os.mkdir(newdir)
    # delete_sql_str = 'delete FROM TB_REPORT_BI where substr(to_char(QINGQIUJH_DATE,\'yyyyMMdd\'),1,6) = substr(to_char(sysdate,\'yyyyMMdd\'),1,6)'
    # truncate_temp_sql_str = 'truncate table tb_report_bi_temp'
    # truncate_thbi_sql_str = 'truncate table TB_REPORT_BI_THBI'
    # truncate_kpi_sql_str = 'truncate table tb_kpi_info'
    # truncate table TB_REPORT_BI_REPORT;
    # truncate table TB_REPORT_BI_SERVICE_SIDE_DESC;
    # function_sql_str = "BIetluser.P_TRANS_DATAS"
    # 1、清空temp表,thbi表,kpi表
    # sqlDML(truncate_temp_sql_str)
    # sqlDML(truncate_thbi_sql_str)
    # sqlDML(truncate_kpi_sql_str)
    # 2、删除正式表本月所有数据
    # sqlDML(delete_sql_str)
    # 3、数据进入临时表
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print('==================================' + child + '==================================')
        data = xlrd.open_workbook(child)
        values = get_data(data)
        save_data(values, data)
        # 4、复制到新目录
        shutil.copyfile(child, newdir + '/' + child[18:])
        # # 5、删除该文件
        os.remove(child)
        # 6、数据进入正式表并处理数据到展示表
        # sqlDMLPROC(function_sql_str)


# ###############################################################################生成配送数据###############################################################################
def sum_box():
    # 生成两点配送
    data_a = sqlDML_a(str_q)
    data_b = sqlDML_a(str_q)
    for v in data_a:
        for x in data_b:
            if v[0] == x[0]:
                continue
            else:
                STATION_BEGIN = v[0]
                STATION_END = x[0]
                bindVar = {'STATION_BEGIN': STATION_BEGIN, 'STATION_END': STATION_END}
                save_data_bind(inster_sql_2, bindVar)
        data_b.pop(data_b.index(v))

    # 生成三点配送
    data_d = sqlDML_a(str_q)
    data_e = sqlDML_a(str_q)
    data_f = sqlDML_a(str_q)

    data_d.pop(len(data_d) - 1)
    data_d.pop(len(data_d) - 1)
    data_e.pop(len(data_e) - 1)
    data_e.pop(0)
    data_f.pop(0)
    data_f.pop(0)
    P = tuple(data_f)
    for x in data_d:
        for y in data_e:
            f = list(P)
            if y in P:
                u = P.index(y) + 1
                for v in range(0, u):
                    f.pop(0)
            for z in f:
                if x == y or x == z or y == z:
                    continue
                else:
                    STATION_BEGIN = x[0]
                    STATION_MID = y[0]
                    STATION_END = z[0]
                    bindVar3 = {'STATION_BEGIN': STATION_BEGIN, 'STATION_MID': STATION_MID, 'STATION_END': STATION_END}
                    save_data_bind(inster_sql_3, bindVar3)
        if x in data_e:
            data_e.remove(x)


# ###############################################################################主函数###############################################################################
if __name__ == '__main__':
    sqlDML(truncate_sql)
    sum_box()