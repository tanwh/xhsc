# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for
from scapp import db
from scapp import app
from scapp.config import PER_PAGE
from scapp.config import PROCESS_STATUS_DKFKJH

from scapp.models import View_Loan_Expected

import datetime,time,xlwt,re
from scapp.tools.export_excel import export_excel
ezxf=xlwt.easyxf #样式转换
	
# 贷款根据状态分类——7. 预期的贷款 
@app.route('/Report/dkgjztfl_7', methods=['GET'])
def dkgjztfl_7():
    return render_template("Report/dkgjztfl_7.html")

# 贷款根据状态分类——7. 预期的贷款 
@app.route('/Report/dkgjztfl_7_search/<int:page>', methods=['POST'])
def dkgjztfl_7_search(page):
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    view_Loan_expected = View_Loan_Expected.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("Report/dkgjztfl_7_search.html",loan_type=loan_type,customer_name=customer_name,
        view_Loan_expected=view_Loan_expected)

# 贷款根据状态分类——7. 预期的贷款--导出
@app.route('/Report/dkgjztfl_7_export', methods=['POST'])
def dkgjztfl_7_export():
    customer_name = request.form['customer_name']
    loan_type = request.form['loan_type']
    sql = ""
    if loan_type != '0':
        sql = "loan_type='"+loan_type+"' and "
    if customer_name:
        sql += " and customer_name like '%"+customer_name+"%'"

    data = View_Loan_Expected.query.filter(sql)

    exl_hdngs=['贷款编号','客户名称','利率','放款日期','贷款金额','负责客户经理','贷款状态']

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
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+'已发放的贷款统计表'+'.xls'
    exp=export_excel()
    return exp.export_download(filename,'已发放的贷款统计表',exl_hdngs,data,exl_hdngs_xf,data_xfs)
