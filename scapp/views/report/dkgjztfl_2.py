# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import db
from scapp import app
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKSQSH_JUJUE
from scapp.config import PROCESS_STATUS_DKSP_JUJUE
from scapp.config import PROCESS_STATUS_SPJY_JUJUE

from scapp.models import View_Loan_Disbursed

import datetime,time,xlwt,re
from scapp.tools.export_excel import export_excel
ezxf=xlwt.easyxf #样式转换
	
from scapp.models import SC_Loan_Product

# 贷款根据状态分类——2. 拒绝的贷款 
@app.route('/Report/dkgjztfl_2', methods=['GET'])
def dkgjztfl_2():
	loan_product = SC_Loan_Product.query.all()
	return render_template("Report/dkgjztfl_2.html",loan_product=loan_product)

# 贷款根据状态分类——2. 拒绝的贷款 
@app.route('/Report/dkgjztfl_2_search/<int:page>', methods=['POST'])
def dkgjztfl_2_search(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = " 1=1 "
    if loan_type != '0':
        sql += " and loan_type='"+loan_type+"'"
    sql += " and (loan_status='"+PROCESS_STATUS_DKSQSH_JUJUE+"' or loan_status='"+PROCESS_STATUS_DKSP_JUJUE+"' or loan_status='"+PROCESS_STATUS_SPJY_JUJUE+"')"
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    view_loan_disbursed = View_Loan_Disbursed.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Report/dkgjztfl_2_search.html",loan_type=loan_type,customer_name=customer_name,
        view_loan_disbursed=view_loan_disbursed)

# 贷款根据状态分类——2. 拒绝的贷款--导出
@app.route('/Report/dkgjztfl_2_export', methods=['POST'])
def dkgjztfl_2_export():
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = " 1=1 "
    if loan_type != '0':
        sql += " and loan_type='"+loan_type+"'"
    sql += " and (loan_status='"+PROCESS_STATUS_DKSQSH_JUJUE+"' or loan_status='"+PROCESS_STATUS_DKSP_JUJUE+"' or loan_status='"+PROCESS_STATUS_SPJY_JUJUE+"')"
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    #data = View_Loan_Disbursed.query.filter(sql)
    query_sql = "select id,create_date,loan_manager,loan_amount_num,'' as refuse_date,'' as refuse_reason,customer_name "
    query_sql += "from view_loan_disbursed where "
    query_sql += sql
    data=db.engine.execute(query_sql)

    exl_hdngs=['贷款编号','申请日期','拒绝人','贷款金额','拒绝日期','拒绝原因','客户名称']

    type_str = 'text text text date text text text'#1
    types= type_str.split()

    exl_hdngs_xf=ezxf('font: bold on;align: wrap on,vert centre,horiz center')
    types_to_xf_map={
        'int':ezxf(num_format_str='#,##0'),
        'date':ezxf(num_format_str='yyyy-mm-dd'),
        'datetime':ezxf(num_format_str='yyyy-mm-dd HH:MM:SS'),
        'ratio':ezxf(num_format_str='#,##0.00%'),
        'text':ezxf(),
        'price':ezxf(num_format_str='￥#,##0.00')
    }

    data_xfs=[types_to_xf_map[t] for t in types]
    date=datetime.datetime.now()
    year=date.year
    month=date.month
    day=date.day
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'拒绝的贷款统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'拒绝的贷款统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)

