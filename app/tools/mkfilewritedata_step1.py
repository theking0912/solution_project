# -*- coding:utf-8 -*-
import codecs

import cx_Oracle
import os

dir = "/Users/lishun/Documents/qwe/"
html = """<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<style type="text/css">
		body, html,#allmap {width: 100%;height: 100%;overflow: hidden;margin:0;font-family:"微软雅黑";}
	</style>
	<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=YSIvEImCI0B8liguWgr80EEiSYtVAffY "></script>
	<title>计算驾车时间与距离</title>
</head>
<body>
	<div id="allmap"></div>
</body>
</html>
<script type="text/javascript">
	// 百度地图API功能
	var map = new BMap.Map("allmap");
	map.centerAndZoom(new BMap.Point(116.404, 39.915), 12);
	var output = "从[#begin#]到[#end#]驾车需要";
	var searchComplete = function (results){
		if (transit.getStatus() != BMAP_STATUS_SUCCESS){
			return ;
		}
		var plan = results.getPlan(0);
		output += plan.getDuration(true) + "\\n";                //获取时间
		output += "总路程为：" ;
		output += plan.getDistance(true) + "\\n";             //获取距离
	}
	var transit = new BMap.DrivingRoute(map, {renderOptions: {map: map},
		onSearchComplete: searchComplete,
		onPolylinesSet: function(){
			setTimeout(function(){alert(output)},"1000");
	}});
	transit.search("[#begin#]", "[#end#]");
</script>
"""

str_q_1 = """select station_begin from point_2_address"""

inster_sql_init_2 = """insert into tbl_init_lines_data
  (STATION_BEGIN, STATION_END)
values
  (:STATION_BEGIN, :STATION_END)"""

truncate_sql = """truncate table tbl_init_lines_data"""

sql = """select a.station_begin, b.address, a.station_end, c.address
  from tbl_init_lines_data a
  left join point_2_address b
    on a.station_begin = b.station_begin
  left join point_2_address c
    on a.station_end = c.station_begin"""

def save_data_bind(sql, bindVar):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(sql, bindVar)
    cursor.close()
    conn.commit()
    conn.close()

def conn_db():
    conn = cx_Oracle.connect('BIetluser', 'qawsedrF123', 'SHUHAI_PRD')
    # conn = cx_Oracle.connect('system', 'system', 'ORCL_LOC')
    return conn


def sqlDML(sql):
    conn = conn_db()
    cr = conn.cursor()
    cr.execute(sql)
    tables = cr.fetchall()
    cr.close()
    conn.commit()
    conn.close()
    return tables

def sqlDML_q(sql):
    conn = conn_db()
    cr = conn.cursor()
    cr.execute(sql)
    cr.close()
    conn.commit()
    conn.close()

def rename():
    tables = sqlDML(sql)
    for v in tables:
        data = html.replace('[#begin#]', v[1]).replace('[#end#]', v[3])
        fp = codecs.open(dir + v[0]+'-'+v[2] + ".html", 'w', 'utf-8')
        fp.write(data)
        fp.close()

# 初始化路线数据
def init_lins_data():
    # 生成两点配送
    data_a = sqlDML(str_q_1)
    data_b = sqlDML(str_q_1)
    sqlDML_q(truncate_sql)
    for v in data_a:
        for x in data_b:
            if v[0] == x[0]:
                continue
            else:
                STATION_BEGIN = v[0]
                STATION_END = x[0]
                bindVar = {'STATION_BEGIN': STATION_BEGIN, 'STATION_END': STATION_END}
                save_data_bind(inster_sql_init_2, bindVar)
        data_b.pop(data_b.index(v))

if __name__ == '__main__':
    init_lins_data()
    rename()
