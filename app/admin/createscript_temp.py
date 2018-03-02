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
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:122461@127.0.0.1:3306/precision_business"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志服
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 会员评论外键关联关系
    kpi_detail = db.relationship("Kpi_detail", backref='user')  # kpi详情外键关联关系
    kpi_person = db.relationship("Kpi_person", backref='user')  # kpi个人外键关联关系
    kpi_personlog = db.relationship("Kpi_personlog", backref='user')  # kpi详情操作日志外键关联关系

    def __repr__(self):
        return '<User %r>' % self.name  # 定义返回的类型 ---->类型为User类型


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户ID外键关联
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址  #路由权限与该地址匹配，如果不匹配则，说明没有权限访问
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 权限
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关联关系
    oplogs = db.relationship("Oplog", backref='admin')  # 管理员操作日志外键关联关系
    kpi_detaillog = db.relationship("Kpi_detaillog", backref='admin')  # kpi详情操作日志外键关联关系
    kpi_personlog = db.relationship("Kpi_personlog", backref='admin')  # kpi个人操作日志外键关联关系

    def __repr__(self):
        return '<Admin %r>' % self.name  # 定义返回的类型

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 管理员操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


# KPI明细
class Kpi_detail(db.Model):
    __tablename__ = "kpi_detail"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    part = db.Column(db.String(100), unique=False)  # 片区
    company_code = db.Column(db.String(100), unique=False)  # 公司代码
    company = db.Column(db.String(100), unique=False)  # 公司
    unit = db.Column(db.String(100), unique=False)  # 部门
    position_code = db.Column(db.String(100), unique=False)  # 岗位代码
    position = db.Column(db.String(100), unique=False)  # 岗位
    emp_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    emp_name = db.Column(db.String(100), unique=False)  # 人员姓名
    gender = db.Column(db.String(100), unique=False)  # 性别
    direct_leader = db.Column(db.String(100), unique=False)  # 直接上街
    indirect_leader = db.Column(db.String(100), unique=False)  # 间接上级
    kpi_order = db.Column(db.SmallInteger)  # KPI顺序
    kpi_name = db.Column(db.String(300), unique=False)  # 指标名称
    assessment_content = db.Column(db.String(1000), unique=False)  # 考核内容
    measurement_standard = db.Column(db.String(1000), unique=False)  # 衡量标准
    weight = db.Column(db.Float, unique=False)  # 权重
    information_source = db.Column(db.String(100), unique=False)  # 信息来源
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    kpi_person = db.relationship("Kpi_person", backref='kpi_detail')  # kpi个人操作日志外键关联关系

    def __repr__(self):
        return "<Kpi_detail %r>" % self.id


# KPI详情操作日志
class Kpi_detaillog(db.Model):
    __tablename__ = "kpi_detaillog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    content = db.Column(db.String(1000))  # 修改内容
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


# KPI个人
class Kpi_person(db.Model):
    __tablename__ = "kpi_person"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    monthly_quarter = db.Column(db.DateTime, index=True, default=datetime.now)  # 月/季度
    part = db.Column(db.String(100), unique=True)  # 片区
    company_code = db.Column(db.String(100), unique=True)  # 公司代码
    company = db.Column(db.String(100), unique=True)  # 公司
    unit = db.Column(db.String(100), unique=True)  # 部门
    position_code = db.Column(db.String(100), unique=True)  # 岗位代码
    position = db.Column(db.String(100), unique=True)  # 岗位
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    name = db.Column(db.String(100), unique=True)  # 人员姓名
    gender = db.Column(db.String(100), unique=True)  # 性别
    direct_leader = db.Column(db.String(100), unique=True)  # 直接上街
    indirect_leader = db.Column(db.String(100), unique=True)  # 间接上级
    kpi_detail_id = db.Column(db.Integer, db.ForeignKey('kpi_detail.id'))  # 所属kpidetail
    self_assessment_instructions = db.Column(db.String(1000), unique=True)  # 自评说明
    self_assessment_score = db.Column(db.String(1000), unique=True)  # 自评得分
    leader_score = db.Column(db.Integer, unique=False)  # 上级评分
    self_level = db.Column(db.CHAR, unique=False)  # 自评评级
    leader_level = db.Column(db.CHAR, unique=False)  # 上级评级
    remarks = db.Column(db.String(1000), unique=False)  # 备注
    kpi_status = db.Column(db.SmallInteger)  # kpi状态，0为新建，1提交，2退回，3归档，4删除
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Kpi_detail %r>" % self.id


# KPI详情操作日志
class Kpi_personlog(db.Model):
    __tablename__ = "kpi_personlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属管理员
    content = db.Column(db.String(1000))  # 修改内容
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


# 要货量
class tbl_trans_things_num_temp(db.Model):
    __tablename__ = "tbl_trans_things_num_temp"
    __bind_key__ = "tools_db"
    things_id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(1000))
    per_box_num = db.Column(db.Float)
    box_num = db.Column(db.Float)
    order_date = db.Column(db.DateTime, index=True, default=datetime.now)
    import_by = db.Column(db.String(1000))

    def __repr__(self):
        return "<tbl_trans_things_num %r>" % self.things_id



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
