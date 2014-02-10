# coding:utf-8

from flask import Module,request, render_template,flash,redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from scapp.models import SC_User
from scapp.models import SC_Industry
from scapp.models import SC_UserRole
from scapp.models import SC_Privilege

from scapp.config import logger
from scapp import app
from scapp import db

# 登陆
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = SC_User.query.filter_by(login_name=request.form['login_name'], login_password=request.form['login_password']).first()
        if user:
            if user.active == '0':
                flash('该用户被禁用，请联系管理员','error')
                return render_template("login.html")
            else:
                login_user(user)
                role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
                return render_template("welcome.html",role=role)
        else:
            flash('用户名或密码错误','error')
            return render_template("login.html")

    else:
        return render_template("login.html")

# 注销
@app.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")
    
# 欢迎界面
@app.route('/welcome', methods=['GET'])
@login_required
def welcome():
    # privileges = SC_UserRole.query.filter_by(user_id=current_user.id).first().role.privileges
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("welcome.html",role=role)

# 信息管理
@app.route('/xxgl', methods=['GET'])
@login_required
def xxgl():
    # privileges = SC_UserRole.query.filter_by(user_id=current_user.id).first().role.privileges
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("index.html",menu = 'xxgl',role=role)

# 流程管理
@app.route('/lcgl', methods=['GET'])
@login_required
def lcgl():
    # privileges = SC_UserRole.query.filter_by(user_id=current_user.id).first().role.privileges
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("index.html",menu = 'lcgl',role=role)

# 系统工具
@app.route('/xtgj', methods=['GET'])
@login_required
def xtgj():
    # privileges = SC_UserRole.query.filter_by(user_id=current_user.id).first().role.privileges
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("index.html",menu = 'xtgj',role=role)

# 系统管理
@app.route('/xtgl', methods=['GET'])
@login_required
def xtgl():
    # privileges = SC_UserRole.query.filter_by(user_id=current_user.id).first().role.privileges
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    print role.role_level
    return render_template("index.html",menu = 'xtgl',role=role)

#客户经理绩效管理
@app.route('/jxgl', methods=['GET'])
@login_required
def jxgl():
    # privileges = SC_UserRole.query.filter_by(user_id=current_user.id).first().role.privileges
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("index.html",menu = 'jxgl',role=role)

# 统计报表
@app.route('/tjbb', methods=['GET'])
@login_required
def tjbb():
    # privileges = SC_UserRole.query.filter_by(user_id=current_user.id).first().role.privileges
    role = SC_UserRole.query.filter_by(user_id=current_user.id).first().role
    return render_template("index.html",menu = 'tjbb',role=role)

# 修改密码
@app.route('/change_password/<int:id>', methods=['GET','POST'])
def change_password(id):
    if request.method == 'POST':
        try:
            user = SC_User.query.filter_by(id=id).first()
            if user.login_password == request.form['old_password']:
                user.login_password = request.form['login_password']
            else:
                raise Exception

            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('修改密码成功，请重新登录！','success')

        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('修改密码失败，为保障账号安全，请重新登录后再尝试修改！','error')

        logout_user()
        return redirect("login")
    else:
        return render_template("change_password.html")

# 还款计划计算工具
@app.route('/Tools/hkjhjsgj', methods=['GET'])
def Tools_hkjhjsgj():
    return render_template("Tools/hkjhjsgj.html")

# 测试CRM
@app.route('/testCRM', methods=['GET','POST'])
def testCRM():
    if request.method == 'POST':

        customer_name = request.form['customer_name']
        zjlx = request.form['zjlx']
        card_num = request.form['card_num']

        sql_cust_id = 'SELECT DISTINCT ODS_CUST_ID FROM A_CI_ODS_SYS_RESOURCE WHERE SOURCE_CUST_NAME=\'%s\' AND CERT_TYPE=\'%s\' AND CERT_NO=\'%s\'' % (customer_name,zjlx,card_num)
        print sql_cust_id
        item_cust_id = db.session.execute(sql_cust_id,bind=db.get_engine(app,bind="CRM_DB2")).fetchall()
        item_store=[]
        for obj in item_cust_id:
            ODS_CUST_ID = obj[0]
            print ODS_CUST_ID
            #item_store.append([obj.ODS_CUST_ID])
            # 对公
            #sql_cust_unit_info = 'SELECT * from a_ci_ods_unitinfo where cust_id=\'%s\'' % (ODS_CUST_ID)
            #item_cust_unit_info = db.session.execute(sql_cust_unit_info,bind=db.get_engine(app,bind="CRM_DB2")).fetchall()

            # 零售
            sql_cust_person_info = 'SELECT birthday from A_CI_ODS_PERSONINFO where cust_id=\'%s\'' % (ODS_CUST_ID)
            item_cust_person_info = db.session.execute(sql_cust_person_info,bind=db.get_engine(app,bind="CRM_DB2")).fetchall()
            for obj_cust_person in item_cust_person_info:
                print obj_cust_person[0]

        #return render_template("testCRM_res.html",cust_unit_obj=cust_unit_obj,item_cust_person_info=item_cust_person_info)
        return render_template("testCRM.html")
    else:
        return render_template("testCRM.html")