#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: views.py
@time: 2017/11/8 下午3:46
"""
import xlrd

from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort
from app.admin.forms import LoginForm, PwdForm, AuthForm, RoleForm, AdminForm, Kpi_detailForm, Tbl_Table_A_Result_Form, \
    Tbl_Trans_Things_Num_Temp_Form, Tbl_Trans_Things_Num_Head_Form, People_Form
from app.models import Admin, User, Comment, Oplog, Userlog, Adminlog, Auth, Role, Kpi_detail, tbl_table_a_result, \
    tbl_trans_things_num_temp, tbl_trans_things_num_template, tbl_trans_things_num_head, People
from xlrd import open_workbook
from functools import wraps
from app import db, app
from app.tools.importExcel import importExcel
from app.tools.generation_report_step4_rou import generation
from app.tools.generation_report import generation1
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
import flask_excel as excel
import os
import uuid
import datetime, time


# 上下文处理器
@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data


# 登录装饰器(访问控制）
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 权限访问装饰器(权限控制）
def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session["admin_id"]
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda v: int(v), auths.split(",")))
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if val == v.id]
        rule = request.url_rule
        if str(rule) not in urls:
            abort(404)
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# index页
@admin.route("/")
@admin_login_req
@admin_auth
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误！", 'err')
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        adminlog = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/", methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.commit()
        flash("修改密码成功，请重新登录！", 'ok')
        redirect(url_for('admin.login'))
    return render_template("admin/pwd.html", form=form)


# 会员列表
@admin.route("/user/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 会员视图
@admin.route("/user/view/<int:id>/", methods=["GET"])
@admin_login_req
@admin_auth
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)


# 删除会员
@admin.route("/user/del/<int:id>/", methods=["GET"])
@admin_login_req
@admin_auth
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("会员删除成功！", "ok")
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route("/comment/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        User
    ).filter(
        Comment.user_id == User.id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/comment_list.html", page_data=page_data)


# 删除评论
@admin.route("/comment/del/<int:id>/", methods=["GET"])
@admin_login_req
@admin_auth
def comment_del(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash("评论删除成功！", "ok")
    return redirect(url_for('admin.comment_list', page=1))


# ----------------------------------------------------------------------------------------------------------------------
# 操作日志
@admin.route("/oplog/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.admin_id
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/oplog_list.html", page_data=page_data)


# 管理员登录日志
@admin.route("/adminloginlog/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id
    ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


# 用户登录日志
@admin.route("/userloginlog/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=4)
    return render_template("admin/userloginlog_list.html", page_data=page_data)


# 添加权限
@admin.route("/auth/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth.query.filter_by(name=data["name"]).first()
        auth_count = Auth.query.filter_by(name=data["name"]).count()
        if auth_count == 1 and auth.name == data["name"]:
            flash("权限已经存在!", "err")
            return redirect(url_for('admin.auth_add'))
        auth = Auth(
            name=data["name"],
            url=data["url"]
        )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功", "ok")
    return render_template("admin/auth_add.html", form=form)


# 权限列表
@admin.route("/auth/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/auth_list.html", page_data=page_data)


# 权限删除
@admin.route("/auth/del/<int:id>/", methods=["GET"])
@admin_login_req
@admin_auth
def auth_del(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("权限删除成功", "ok")
    return redirect(url_for('admin.auth_list', page=1))


# 编辑权限
@admin.route("/auth/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(int(id))
    if form.validate_on_submit():
        data = form.data
        auth.name = data["name"]
        auth.url = data["url"]
        db.session.commit()
        flash("权限修改成功！", "ok")
        return redirect(url_for('admin.auth_edit', id=id))
    return render_template("admin/auth_edit.html", form=form, auth=auth)


# 添加角色
@admin.route("/role/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role_count = Role.query.filter_by(name=data["name"]).count()
        if role_count == 1:
            flash("角色已经存在！", "err")
            return redirect(url_for('admin.role_add'))
        role = Role(
            name=data["name"],
            auths=",".join(map(lambda v: str(v), data["auths"]))
        )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功！", "ok")
    return render_template("admin/role_add.html", form=form)


# 角色列表
@admin.route("/role/list/<int:page>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/role_list.html", page_data=page_data)


# 角色删除
@admin.route("/role/del/<int:id>/", methods=["GET"])
@admin_login_req
@admin_auth
def role_del(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash("角色删除成功", "ok")
    return redirect(url_for('admin.role_list', page=1))


# 编辑角色
@admin.route("/role/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(int(id))
    if request.method == "GET":
        auths = role.auths
        form.auths.data = list(map(lambda v: int(v), auths.split(",")))
    if form.validate_on_submit():
        data = form.data
        role.name = data["name"]
        role.auths = ",".join(map(lambda v: str(v), data["auths"]))
        db.session.commit()
        flash("角色修改成功！", "ok")
        return redirect(url_for('admin.role_edit', id=id))
    return render_template("admin/role_edit.html", form=form, role=role)


# 添加管理员
@admin.route("/admin/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin_count = Admin.query.filter_by(name=data["name"]).count()
        from werkzeug.security import generate_password_hash
        if admin_count == 1:
            flash("管理员名称已经存在！", "err")
            return redirect(url_for('admin.admin_add'))
        admin = Admin(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            role_id=data["role_id"],
            is_super=1
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功！", "ok")
    return render_template("admin/admin_add.html", form=form)


# 管理员列表
@admin.route("/admin/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/admin_list.html", page_data=page_data)


# kpi列表
@admin.route("/kpi/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def kpi_list(page=None):
    if page is None:
        page = 1
    page_data = Kpi_detail.query.order_by(
        Kpi_detail.addtime.asc()
    ).paginate(page=page, per_page=100)
    return render_template("admin/kpi_list.html", page_data=page_data)


# 编辑角色
@admin.route("/kpi/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def kpi_edit(id=None):
    form = Kpi_detailForm()
    kpi_detail = Kpi_detail.query.get_or_404(int(id))
    if form.validate_on_submit():
        data = form.data
        kpi_detail.name = data["name"]
        kpi_detail.url = data["url"]
        db.session.commit()
        flash("权限修改成功！", "ok")
        return redirect(url_for('admin.kpi_edit', id=id))
    return render_template("admin/kpi_edit.html", form=form, kpi_detail=kpi_detail)


# 添加kpi
@admin.route("/kpi/add/", methods=["GET"])
@admin_login_req
@admin_auth
def kpi_add():
    form = Kpi_detailForm()
    if form.validate_on_submit():
        data = form.data
        role_count = Kpi_detail.query.filter_by(name=data["name"]).count()
        if role_count == 1:
            flash("该条kpi已经存在！", "err")
            return redirect(url_for('admin.kpi_add'))
        role = Role(
            name=data["name"],
            auths=",".join(map(lambda v: str(v), data["auths"]))
        )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功！", "ok")
    return render_template("admin/kpi_add.html", form=form)


# kpi列表
@admin.route("/things/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def things_list(page=None):
    if page is None:
        page = 1
    # generation()
    page_data = tbl_trans_things_num_head.query.order_by(
        tbl_trans_things_num_head.order_date.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/things_list.html", page_data=page_data)


# 添加订单头
def things_add(order_date):
    # 转换日期
    if len(order_date) != 0:
        # 查重
        data_count = tbl_trans_things_num_head.query.filter_by(
            order_date=datetime.datetime.strptime(order_date, '%Y-%m-%d')
        ).count()
        if data_count == 0:
            things_head = tbl_trans_things_num_head(
                station_num=int(0),
                box_num_sum=int(0),
                order_date=datetime.datetime.strptime(order_date, '%Y-%m-%d'),
                import_by="import_by",
            )
            db.session.add(things_head)
            db.session.commit()
            msg = "新增数据成功！"
            flash(msg)
            return "success"
        else:
            msg = "已存在该天数据！"
            flash(msg)
            return "error"
    else:
        msg = "日期不可为空！"
        flash(msg)
        return "error"


# kpi列表
@admin.route("/trans/list/", methods=["GET"])
@admin_login_req
@admin_auth
def trans_list():
    pa_order_date = request.args.get('order_date', 1, type=str)[0:10]
    order_date = datetime.datetime.strptime(pa_order_date, '%Y-%m-%d')
    page_data = tbl_table_a_result.query.filter_by(
        order_date=order_date
    ).order_by(
        tbl_table_a_result.order_date.asc()
    ).paginate(page=1, per_page=100)
    list_count = len(page_data.items)
    num_list = []
    for x in range(1, list_count+1):
        num_list.append(x)
    return render_template("admin/trans_list.html", list_count=list_count, num_list=num_list, page_data=page_data)


# 添加每日要货量
@admin.route("/trans/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def trans_add():
    form = Tbl_Trans_Things_Num_Temp_Form()
    things_data = tbl_trans_things_num_template.query.order_by(
        tbl_trans_things_num_template.things_id.asc()
    ).paginate(page=1, per_page=100)
    # 删除数据
    order_date = request.form.get("start_date")
    if order_date is not None:
        if order_date != '':
            tbl_trans_things_num_temp.query.filter_by(
                order_date=datetime.datetime.strptime(order_date, '%Y-%m-%d')).delete()
            db.session.commit()
        else:
            flash("日期不可为空！")
        # 添加订单头
        things_add(order_date)
        # 提交数据到数据库
        tables = request.form.getlist("list[]")
        if len(tables) > 0:
            for v in tables:
                str_par = v.split(',')
                things = tbl_trans_things_num_temp(
                    station_name=str_par[1],
                    per_box_num=0,
                    box_num=str_par[2],
                    order_date=datetime.datetime.strptime(str_par[3], "%Y-%m-%d"),
                    import_by='admin',
                )
                db.session.add(things)
            db.session.commit()
        # 生成排程逻辑
        pa_order_date = order_date[0:4] + order_date[5:7] + order_date[8:10]
        msg = generation(pa_order_date)
        flash(msg)
        page_data = tbl_trans_things_num_head.query.order_by(
            tbl_trans_things_num_head.order_date.asc()
        ).paginate(page=1, per_page=10)
        return render_template("admin/things_list.html", page_data=page_data)
    else:
        flash("日期不可为空！")
    return render_template("admin/trans_add.html/", things_data=things_data, form=form)


# 添加kpi
@admin.route("/trans/submit/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def trans_submit():
    pass
    # print(form.validate_on_submit())
    # if form.validate_on_submit():
    #     print("asdasdasdasdasd")
    #     data = form.data
    #     print(data["station_name"])
    #     things_date = Kpi_detail.query.filter_by(name=data["order_date"]).count()
    #     if things_date == 1:
    #         flash("已经存在当前日期的数据！", "err")
    #         return redirect(url_for('admin.trans_add'))
    #     things = tbl_trans_things_num_temp(
    #         things_id=data["things_id"],
    #         station_name=data["station_name"],
    #         per_box_num=data["per_box_num"],
    #         box_num=data["box_num"],
    #         order_date=data["order_date"],
    #         import_by=data["import_by"]
    #     )
    #     db.session.add(things)
    #     db.session.commit()
    #     flash("添加角色成功！", "ok")


# ----------------
@admin.route("/demo/", methods=['GET'])
@admin_login_req
@admin_auth
def demo():
    print("oooooooooo")
    return render_template("admin/import_device.html")


@admin.route("/import/excels/", methods=['GET'])
@admin_login_req
@admin_auth
def import_excels():
    form_data = []
    exceldir = "/Users/lishun/PycharmProjects/solution_project/app/static/video/people.xlsx"
    bk = open_workbook(exceldir, encoding_override="utf-8")
    try:
        sh = bk.sheets()[0]
    except:
        print("no sheet in %s named sheet1" % exceldir)
    else:
        nrows = sh.nrows
        for i in range(1, nrows):
            row_data = sh.row_values(i)
            people = People()
            people.id = row_data[0]
            people.name = row_data[1]
            people.age = row_data[2]
            form_data.append(row_data)
            #     db.session.add(people)
            # db.session.commit()
    return render_template('admin/import_device.html', form_data=form_data)


def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file='file.xls', colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@admin.route("/import/device/", methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def import_device():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename

        # 判断文件名是否合规
        if file and allowed_file(filename):
            file.save(os.path.join('.\\upload', filename))
        else:
            flash('失败:上传文件格式不对')
            return render_template('admin/import_device.html')

        # file.save(os.path.join('c:\\mnt', filename))
        # file.save(os.path.join('.\\upload', filename))

        # 添加到数据库
        tables = excel_table_byindex(file='.\\upload\\' + filename)
        for row in tables:
            # 判断表格式是否对
            if '手持机DEVICEID' not in row or \
                            '手持机SIMID' not in row or \
                            '手持机硬件版本' not in row or \
                            '手持机软件版本' not in row or \
                            '脚扣DEVICEID' not in row or \
                            '脚扣SIMID' not in row or \
                            '脚扣硬件版本' not in row or \
                            '脚扣软件版本' not in row:
                flash('失败:excel表格式不对')
                return render_template('admin/import_device.html')

            # print('0x%04x' % int(str(row['手持机DEVICEID']).split('.')[0], base=16))
            # 判断手持机字段是否存在
            if row['手持机DEVICEID'] != '' and row['手持机SIMID'] != '' and \
                            row['手持机硬件版本'] != '' and row['手持机软件版本'] != '':
                id_format = '0x%04x' % int(str(row['手持机DEVICEID']).split('.')[0], base=16)
                device = Device(device_type='手持机',
                                device_id=id_format,
                                device_simid=str(row['手持机SIMID']).split('.')[0],
                                hard_version=int(row['手持机硬件版本']),
                                soft_version=int(row['手持机软件版本']),
                                warehouse=False,
                                shipment_time='无',
                                agent='无',
                                prison='无',
                                shutdown=False)
                # 判断是否id重复
                flag = True
                if Device.query.filter_by(device_id=device.device_id).count() > 0:
                    flash('失败:设备ID:%s已存在' % device.device_id)
                    flag = False
                # 判断simid是否重复
                elif Device.query.filter_by(device_simid=device.device_simid).count() > 0:
                    flash('失败:设备SIMID:%s已存在' % device.device_simid)
                    flag = False
                if flag:
                    db.session.add(device)
                else:
                    return render_template('admin/import_device.html')

            if row['脚扣DEVICEID'] != '' and row['脚扣SIMID'] != '' and \
                            row['脚扣硬件版本'] != '' and row['脚扣软件版本'] != '':
                id_format = '0x%04x' % int(str(row['脚扣DEVICEID']).split('.')[0], base=16)
                device = Device(device_type='脚扣',
                                device_id=id_format,
                                device_simid=str(row['脚扣SIMID']).split('.')[0],
                                hard_version=int(row['脚扣硬件版本']),
                                soft_version=int(row['脚扣软件版本']),
                                warehouse=False,
                                shipment_time='无',
                                agent='无',
                                prison='无',
                                shutdown=False)
                # 判断是否id重复
                flag = True
                if Device.query.filter_by(device_id=device.device_id).count() > 0:
                    flash('失败:设备ID:%s已存在' % device.device_id)
                    flag = False
                # 判断simid是否重复
                elif Device.query.filter_by(device_simid=device.device_simid).count() > 0:
                    flash('失败:设备SIMID:%s已存在' % device.device_simid)
                    flag = False
                if flag:
                    db.session.add(device)
                else:
                    return render_template('admin/import_device.html')
        return redirect(url_for('.index'))

    return render_template('admin/import_device.html')
