# !/usr/bin/env python
# encoding: utf-8

"""
@version: 0001
@author: Leroy.Lee
@license: -------
@file: forms.py
@time: 2017/11/8 下午3:46
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, FileField, TextAreaField, SelectField, \
    SelectMultipleField, \
    DecimalField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Auth, Role, tbl_trans_things_num_temp, tbl_trans_things_num_template, \
    tbl_trans_things_num_head

auth_list = Auth.query.all()
role_list = Role.query.all()


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "required": "required"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, filed):
        account = filed.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在！")


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
            # "required": "required"
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")


class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称！")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称！"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称"
        }
    )
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("请选择权限！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in auth_list],
        render_kw={
            "class": "form-control"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码！"
        }
    )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[
            DataRequired("请输入管理员重复密码！"),
            EqualTo("pwd", message="两次密码不一致！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请重复输入管理员密码！"
        }
    )
    role_id = SelectField(
        label="所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in role_list],
        render_kw={
            "class": "form-control"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class Kpi_detailForm(FlaskForm):
    part = StringField(
        label="片区",
        validators=[
            DataRequired("请输入片区名称！")
        ],
        description="片区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    company_code = StringField(
        label="公司代码",
        validators=[
            DataRequired("请输入公司代码！")
        ],
        description="公司代码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入公司代码！"
        }
    )
    company = StringField(
        label="公司名称",
        validators=[
            DataRequired("请输入公司名称！")
        ],
        description="公司名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入公司名称！"
        }
    )
    unit = StringField(
        label="部门名称",
        validators=[
            DataRequired("请输入部门名称！")
        ],
        description="部门名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入部门名称！"
        }
    )
    position_code = StringField(
        label="职位代码",
        validators=[
            DataRequired("请输入职位代码！")
        ],
        description="职位代码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入职位代码！"
        }
    )
    position = StringField(
        label="职位名称",
        validators=[
            DataRequired("请输入职位名称！")
        ],
        description="职位名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入职位名称！"
        }
    )
    emp_id = StringField(
        label="员工代码",
        validators=[
            DataRequired("请输入员工代码！")
        ],
        description="员工代码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入员工代码！"
        }
    )
    emp_name = StringField(
        label="员工姓名",
        validators=[
            DataRequired("请输入员工姓名！")
        ],
        description="员工姓名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入员工姓名！"
        }
    )
    gender = StringField(
        label="性别",
        validators=[
            DataRequired("请输入性别！")
        ],
        description="性别",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入性别！"
        }
    )
    direct_leader = StringField(
        label="直接领导",
        validators=[
            DataRequired("请输入直接领导！")
        ],
        description="直接领导",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入直接领导！"
        }
    )
    indirect_leader = StringField(
        label="间接领导",
        validators=[
            DataRequired("请输入间接领导！")
        ],
        description="间接领导",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入间接领导！"
        }
    )
    kpi_order = StringField(
        label="kpi顺序",
        validators=[
            DataRequired("请输入kpi顺序！")
        ],
        description="kpi顺序",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入kpi顺序！"
        }
    )
    kpi_name = StringField(
        label="kpi名称",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    assessment_content = StringField(
        label="片区",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    measurement_standard = StringField(
        label="片区",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    weight = StringField(
        label="片区",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    information_source = StringField(
        label="片区",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class Tbl_Table_A_Result_Form(FlaskForm):
    station_name = StringField(
        label="站点名称",
        validators=[
            DataRequired("请输入站点名称！")
        ],
        description="站点名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入站点名称！"
        }
    )
    box_sum = StringField(
        label="要货量",
        validators=[
            DataRequired("请输入要货量！")
        ],
        description="要货量",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入要货量！"
        }
    )
    who_first = StringField(
        label="装载顺序",
        validators=[
            DataRequired("请输入装载顺序！")
        ],
        description="装载顺序",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入装载顺序！"
        }
    )
    driver = StringField(
        label="司机姓名",
        validators=[
            DataRequired("请输入司机姓名！")
        ],
        description="司机姓名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入司机姓名！"
        }
    )
    lines = StringField(
        label="运送路线",
        validators=[
            DataRequired("请输入运送路线！")
        ],
        description="运送路线",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入运送路线！"
        }
    )
    remark = StringField(
        label="备注",
        validators=[
            DataRequired("请输入备注！")
        ],
        description="备注",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入备注！"
        }
    )
    order_date = StringField(
        label="订单日期",
        validators=[
            DataRequired("请输入订单日期！")
        ],
        description="订单日期",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入订单日期！"
        }
    )
    station_name1 = StringField(
        label="站点1",
        validators=[
            DataRequired("请输入站点1")
        ],
        description="站点1",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入站点1"
        }
    )
    station_name2 = StringField(
        label="站点2",
        validators=[
            DataRequired("请输入站点2")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入站点2"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class Tbl_Trans_Things_Num_Head_Form(FlaskForm):
    things_head_id = StringField(
        label="头ID",
        description="头ID",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入头ID"
        }
    )
    station_num = DecimalField(
        label="站点数量",
        description="站点数量",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入站点数量"
        }
    )
    box_num_sum = DecimalField(
        label="总要货量",
        description="总要货量",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入总要货量"
        }
    )
    order_date = StringField(
        label="订单日期",
        description="订单日期",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入订单日期"
        }
    )
    import_by = StringField(
        label="操作人",
        description="操作人",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入操作人"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class Tbl_Trans_Things_Num_Temp_Form(FlaskForm):
    things_id = StringField(
        label="序号",
        validators=[
            DataRequired("请输入序号！")
        ],
        description="序号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入序号！"
        }
    )
    station_name = StringField(
        label="站点名称",
        validators=[
            DataRequired("请输入站点名称！")
        ],
        description="站点名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入站点名称！"
        }
    )
    per_box_num = DecimalField(
        label="预估箱数",
        validators=[
            DataRequired("请输入预估箱数")
        ],
        description="预估箱数",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预估箱数"
        }
    )
    box_num = DecimalField(
        label="实际箱数",
        validators=[
            DataRequired("请输入实际箱数")
        ],
        description="实际箱数",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入实际箱数"
        }
    )
    order_date = DateField(
        label="订单日期",
        format="yyyy-mm-dd",
        render_kw={
            "data-date-format": "yyyy-mm-dd"
        }
    )
    import_by = StringField(
        label="操作人",
        validators=[
            DataRequired("请输入操作人")
        ],
        description="操作人",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入操作人"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class Tbl_Trans_Things_Num_Template_Form(FlaskForm):
    things_id = StringField(
        label="序号",
        validators=[
            DataRequired("请输入序号！")
        ],
        description="序号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入序号！"
        }
    )
    station_name = StringField(
        label="站点名称",
        validators=[
            DataRequired("请输入站点名称！")
        ],
        description="站点名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入站点名称！"
        }
    )
    per_box_num = DecimalField(
        label="预估箱数",
        validators=[
            DataRequired("请输入预估箱数")
        ],
        description="预估箱数",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预估箱数"
        }
    )
    box_num = DecimalField(
        label="实际箱数",
        validators=[
            DataRequired("请输入实际箱数")
        ],
        description="实际箱数",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入实际箱数"
        }
    )
    order_date = StringField(
        label="订单日期",
        validators=[
            DataRequired("请输入订单日期！")
        ],
        description="订单日期",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入订单日期！"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class People_Form(FlaskForm):
    id = StringField(
        label="序号",
        validators=[
            DataRequired("请输入序号！")
        ],
        description="序号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入序号！"
        }
    )
    name = StringField(
        label="站点名称",
        validators=[
            DataRequired("请输入站点名称！")
        ],
        description="站点名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入站点名称！"
        }
    )
    age = StringField(
        label="预估箱数",
        validators=[
            DataRequired("请输入预估箱数")
        ],
        description="预估箱数",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预估箱数"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )
