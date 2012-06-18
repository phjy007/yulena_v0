#-*-  coding:UTF-8  -*-
import xlrd,datetime
from decimal import Decimal
from django.shortcuts import render,render_to_response
from yulena.models import *
import string
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.db.models import Sum
import myfunc
from django.contrib.auth.decorators import login_required
from django.contrib import auth

# 静态页面呈现函数
def show_login(request):
    return render_to_response("login.html")

@login_required
def show_index(request):
    return render_to_response("index.html")

@login_required
def show_checkin(request):
    return render_to_response("checkin_analysis.html")
@login_required
def show_checkin_kehu(request):
    return render_to_response("checkin_analysis_kehu.html")

@login_required
def show_contract(request):
    return render_to_response("contract_analysis.html")

@login_required
def show_inventory(request):
    return render_to_response("inventory_analysis.html")
@login_required
def show_inventory_kehu(request):
    return render_to_response("inventory_analysis_kehu.html")

@login_required
def show_plan(request):
    return render_to_response("plan_analysis.html")

@login_required
def show_inventory_target(request):
    return render_to_response("target_inventory_analysis.html")
@login_required
def show_checkin_target(request):
    return render_to_response("target_checkin_analysis.html")

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print 'username=' + username
    print 'password=' + password
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/index")
    else:
        return HttpResponseRedirect("/login_page")

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/login_page")



#update
def updatedb(request):
    try:
        tmp = glvar.objects.get(id=1)
    except glvar.DoesNotExist:
        myfunc.initial()
    myfunc.update()
    return render_to_response("index.html")

#应收
def checkin_yewuyuan_table(request):
    ywy = yewuyuan.objects.all().order_by('-checkin_sum')
    data = []
    forcnt = 0
    for item in ywy:
        data.append({'rank':forcnt,
					 'name':item.name,
					 'checkin_money':round(float(item.checkin_sum),2)})
        forcnt += 1
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def checkin_yewuyuan_names(request):
    ywy = yewuyuan.objects.all().order_by('-checkin_sum')
    data = []
    for item in ywy:
        data.append({ 'name':item.name})
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


def checkin_yewuyuan_chart_data(request):
    data = []
    ywyname = request.REQUEST['name']
    ps = yewuyuan.objects.get(name=ywyname).checkin_rec
    for i in range(1,13):
        item = record.objects.get(related_id=ps,month=i)
        data.append({'month':i, 'plan':round(float(item.num)*1.1, 2), 'finish':round(float(item.num), 2), 'percentage':1.1 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
"""
    data = []
    ywyname = request.REQUEST['name']
    theywy = yewuyuan.objects.get(name=ywyname)
    timeline = datetime.date.today() + datetime.timedelta(days=90)
    if ywyname == u'全部':
        over_three_month = checkin.objects.filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
        with_in_three_month = checkin.objects.filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
    else:
        over_three_month = checkin.objects.filter(ywy=ywyname).filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
        with_in_three_month = checkin.objects.filter(ywy=ywyname).filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
    if over_three_month['ysye__sum']== None :
        over_three_month = 0
    else:
        over_three_month = float(over_three_month['ysye__sum'])
    if with_in_three_month['ysye__sum'] == None :
        with_in_three_month = 0
    else:
        with_in_three_month = float(with_in_three_month['ysye__sum'])
    
    data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':4, 'plan':round(float(theywy.checkin_sum)*1.1, 2), 'finish':round(float(theywy.checkin_sum), 2), 'percentage':1.1 })
    data.append({'month':5, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
"""

def checkin_yewuyuan_related_data_specific(request):
	ywyname = request.REQUEST['name']
	#ywyname = u'全部'
	if ywyname == u'全部':
		results = checkin.objects.all()
	else:
		results = checkin.objects.filter(ywy=ywyname)
	data = []
	timeline = datetime.date.today() + datetime.timedelta(days=90)
	for item in results:
		if item.yjysrq > timeline:
			is_over_three_month = u'是'
		else:
			is_over_three_month = u'否'
		data.append({'checkin_money':round(float(item.ysye),2),
					 'user':item.yh,
                     'contract_no':item.hth,
					 'sign_time':item.kprq.strftime("%Y-%m-%d"),
					 'money_within_time':round(float(item.ysye),2),
					 'money_over_time':round(float(item.ysws),2),
					 'is_over_three_month':is_over_three_month,
					 'want_time':item.yjysrq.strftime("%Y-%m-%d"),
                     'maintain_time':item.whrq.strftime("%Y-%m-%d")
					 })
	return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


def checkin_yewuyuan_related_data(request):
	ywyname = request.REQUEST['name']
	theywy = yewuyuan.objects.get(name=ywyname)
	timeline = datetime.date.today()+datetime.timedelta(days=90)
	if ywyname == u'全部':
		over_three_month = checkin.objects.filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
		with_in_three_month = checkin.objects.filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
	else:
		over_three_month = checkin.objects.filter(ywy=ywyname).filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
		with_in_three_month = checkin.objects.filter(ywy=ywyname).filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
	print over_three_month
	print with_in_three_month
	if over_three_month['ysye__sum']== None :
		over_three_month = 0
	else:
		over_three_month = float(over_three_month['ysye__sum'])
	if with_in_three_month['ysye__sum'] == None :
		with_in_three_month = 0
	else:
		with_in_three_month = float(with_in_three_month['ysye__sum'])
	data = [		  {'related_data_title':'所选择的人的应收', 'related_data_data':round(float(theywy.checkin_sum), 2)},
					  {'related_data_title':'与上月相比的波动','related_data_data':round(float(theywy.checkin_sum-theywy.checkin_lastmonth),2)},
					  {'related_data_title':'上月收款计划完成百分比','related_data_data':0.8},
					  {'related_data_title':'三个月以内','related_data_data':round(over_three_month,2)},
					  {'related_data_title':'三个月以上','related_data_data':round(with_in_three_month,2)}
			]
	return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


def checkin_kehu_table(request):
    clients = client.objects.all().order_by('-checkin')
    data = []
    forcnt = 0
    for item in clients:
        data.append({'rank':forcnt,
                                         'name':item.name,
                                         'checkin_money':round(float(item.checkin),2)})
        forcnt += 1
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def checkin_kehu_names(request):
        clients = client.objects.all().order_by('-checkin')
        data = []
        for item in clients:
                data.append({ 'name':item.name})
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


def checkin_kehu_chart_data(request):
    data = []
    ywyname = request.REQUEST['name']
    ps = client.objects.get(name=ywyname).checkin_rec
    for i in range(1,13):
        item = record.objects.get(related_id=ps,month=i)
        data.append({'month':i, 'plan':round(float(item.num)*1.1, 2), 'finish':round(float(item.num), 2), 'percentage':1.1 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
"""

    data = []
    client_name = request.REQUEST['name']
    theclient = client.objects.get(name=client_name)
    timeline = datetime.date.today()+datetime.timedelta(days=90)
    if client_name == u'全部':
            over_three_month = checkin.objects.filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
            with_in_three_month = checkin.objects.filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
    else:
            over_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
            with_in_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
    if over_three_month['ysye__sum']== None :
            over_three_month = 0
    else:
            over_three_month = float(over_three_month['ysye__sum'])
    if with_in_three_month['ysye__sum'] == None :
            with_in_three_month = 0
    else:
            with_in_three_month = float(with_in_three_month['ysye__sum'])

    data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':4, 'plan':round(float(theclient.checkin)*1.1, 2), 'finish':round(float(theclient.checkin), 2), 'percentage':1.1 })
    data.append({'month':5, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
"""


def checkin_kehu_related_data_specific(request):
        client_name = request.REQUEST['name']
        #ywyname = u'全部'
        if client_name == u'全部':
                results = checkin.objects.all()
        else:
                results = checkin.objects.filter(yh=client_name)
        results.order_by('-ysye')
        data = []
        timeline = datetime.date.today() + datetime.timedelta(days=90)
        for item in results:
                if item.yjysrq > timeline:
                        is_over_three_month = u'是'
                else:
                        is_over_three_month = u'否'
                data.append({'checkin_money':round(float(item.ysye),2),
                                         'user':item.yh,
                     'contract_no':item.hth,
                                         'sign_time':item.kprq.strftime("%Y-%m-%d"),
                                         'money_within_time':round(float(item.ysye),2),
                                         'money_over_time':round(float(item.ysws),2),
                                         'is_over_three_month':is_over_three_month,
                                         'want_time':item.yjysrq.strftime("%Y-%m-%d"),
                                         'maintain_time':item.whrq.strftime("%Y-%m-%d")
                                         })
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def checkin_kehu_related_data(request):
        client_name = request.REQUEST['name']
        theclient = client.objects.get(name=client_name)
        timeline = datetime.date.today()+datetime.timedelta(days=90)
        if client_name == u'全部':
                over_three_month = checkin.objects.filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
                with_in_three_month = checkin.objects.filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
        else:
                over_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
                with_in_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
        if over_three_month['ysye__sum']== None :
                over_three_month = 0
        else:
                over_three_month = float(over_three_month['ysye__sum'])
        if with_in_three_month['ysye__sum'] == None :
                with_in_three_month = 0
        else:
                with_in_three_month = float(with_in_three_month['ysye__sum'])
        data = [                  {'related_data_title':'所选择客户的应收', 'related_data_data':round(float(theclient.checkin), 2)},
                                          {'related_data_title':'与上月相比的波动','related_data_data':round(float(theclient.checkin), 2)},
                                          {'related_data_title':'上月收款计划完成百分比','related_data_data':0.8},
                                          {'related_data_title':'三个月以内','related_data_data':round(over_three_month,2)},
                                          {'related_data_title':'三个月以上','related_data_data':round(with_in_three_month,2)}
                        ]
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


################库存分析#####################

def inventory_yewuyuan_table(request):
    ywy = yewuyuan.objects.all().order_by('-inventory_sum')
    data = []
    forcnt = 0
    for item in ywy:
        data.append({'rank':forcnt,
                                         'name':item.name,
                                         'inventory_money':round(float(item.inventory_sum),2)})
        forcnt += 1
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def inventory_yewuyuan_names(request):
        ywy = yewuyuan.objects.all().order_by('-inventory_sum')
        data = []
        for item in ywy:
                data.append({ 'name':item.name})
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


def inventory_yewuyuan_chart_data(request):
    data = []
    ywyname = request.REQUEST['name']
    ps = yewuyuan.objects.get(name=ywyname).inventory_rec
    for i in range(1,13):
        item = record.objects.get(related_id=ps,month=i)
        data.append({'month':i, 'plan':round(float(item.num)*1.1, 2), 'finish':round(float(item.num), 2), 'percentage':1.1 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
"""
		
		ywyname = request.REQUEST['name']
        data = []
        ywyname = request.REQUEST['name']
        theywy = yewuyuan.objects.get(name=ywyname)
        timeline = datetime.date.today()+datetime.timedelta(days=90)
        if ywyname == u'全部':
                over_three_month = inventory.objects.filter(yjckrq__gt=timeline).aggregate(Sum('kcje'))
                with_in_three_month = inventory.objects.filter(yjckrq__lte=timeline).aggregate(Sum('kcje'))
        else:
                over_three_month = inventory.objects.filter(ywy=ywyname).filter(yjckrq__gt=timeline).aggregate(Sum('kcje'))
                with_in_three_month = inventory.objects.filter(ywy=ywyname).filter(yjckrq__lte=timeline).aggregate(Sum('kcje'))
        if over_three_month['kcje__sum']== None :
                over_three_month = 0
        else:
                over_three_month = float(over_three_month['kcje__sum'])
        if with_in_three_month['kcje__sum'] == None :
                with_in_three_month = 0
        else:
                with_in_three_month = float(with_in_three_month['kcje__sum'])
        data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':4, 'plan':round(float(theywy.inventory_sum)*1.1, 2), 'finish':round(float(theywy.inventory_sum), 2), 'percentage':1.1 })
        data.append({'month':5, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
"""

def inventory_yewuyuan_related_data_specific(request):
        ywyname = request.REQUEST['name']
        #ywyname = u'全部'
        if ywyname == u'全部':
                results = inventory.objects.all().order_by('-kcje')
        else:
                results = inventory.objects.filter(ywy=ywyname).order_by('-kcje')
        data = []
        timeline = datetime.date.today() + datetime.timedelta(days=90)
        for item in results:
                if item.yjckrq > timeline:
                        is_over_three_month = u'是'
                else:
                        is_over_three_month = u'否'
                data.append({'inventory_money':round(float(item.kcje),2),
                                         'user':item.yh,
										 'contract_no':item.hth,
                                         'sign_time':item.zhrkrq.strftime("%Y-%m-%d"),
                                         'is_over_three_month':'%d'%(datetime.date.today().month-item.zhrkrq.month)+u'个月',
                                         'want_time':item.yjckrq.strftime("%Y-%m-%d"),
                                         'maintain_time':item.whrq.strftime("%Y-%m-%d")
                                         })
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def inventory_yewuyuan_related_data(request):
        ywyname = request.REQUEST['name']
        theywy = yewuyuan.objects.get(name=ywyname)
        timeline = datetime.date.today()+datetime.timedelta(days=90)
        if ywyname == u'全部':
                over_three_month = inventory.objects.filter(yjckrq__gt=timeline).aggregate(Sum('kcje'))
                with_in_three_month = inventory.objects.filter(yjckrq__lte=timeline).aggregate(Sum('kcje'))
        else:
                over_three_month = inventory.objects.filter(ywy=ywyname).filter(yjckrq__gt=timeline).aggregate(Sum('kcje'))
                with_in_three_month = inventory.objects.filter(ywy=ywyname).filter(yjckrq__lte=timeline).aggregate(Sum('kcje'))
        if over_three_month['kcje__sum']== None :
                over_three_month = 0
        else:
                over_three_month = float(over_three_month['kcje__sum'])
        if with_in_three_month['kcje__sum'] == None :
                with_in_three_month = 0
        else:
                with_in_three_month = float(with_in_three_month['kcje__sum'])
        data = [                  {'related_data_title':'所选择的人的库存', 'related_data_data':round(float(theywy.inventory_sum), 2)},
                                          {'related_data_title':'与上月相比的波动','related_data_data':round(float(theywy.inventory_sum-theywy.inventory_lastmonth),2)},
                                          {'related_data_title':'上月收款计划完成百分比','related_data_data':0.8},
                                          {'related_data_title':'三个月以内','related_data_data':round(over_three_month,2)},
                                          {'related_data_title':'三个月以上','related_data_data':round(with_in_three_month,2)}
                        ]
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

#应收
def inventory_kehu_table(request):
    clients = client.objects.all().order_by('-inventory')
    data = []
    forcnt = 0
    for item in clients:
        data.append({'rank':forcnt,
                                         'name':item.name,
                                         'inventory_money':round(float(item.inventory),2)})
        forcnt += 1
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def inventory_kehu_names(request):
        clients = client.objects.all().order_by('-inventory')
        data = []
        for item in clients:
                data.append({ 'name':item.name})
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


def inventory_kehu_chart_data(request):
    data = []
    ywyname = request.REQUEST['name']
    ps = client.objects.get(name=ywyname).inventory_rec
    for i in range(1,13):
        item = record.objects.get(related_id=ps,month=i)
        data.append({'month':i, 'plan':round(float(item.num)*1.1, 2), 'finish':round(float(item.num), 2), 'percentage':1.1 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
"""
        ywyname = request.REQUEST['name']
        data = []
        client_name = request.REQUEST['name']
        theclient = client.objects.get(name=client_name)
        timeline = datetime.date.today()+datetime.timedelta(days=90)
        if client_name == u'全部':
                over_three_month = checkin.objects.filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
                with_in_three_month = checkin.objects.filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
        else:
                over_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
                with_in_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
        if over_three_month['ysye__sum']== None :
                over_three_month = 0
        else:
                over_three_month = float(over_three_month['ysye__sum'])
        if with_in_three_month['ysye__sum'] == None :
                with_in_three_month = 0
        else:
                with_in_three_month = float(with_in_three_month['ysye__sum'])
        data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':4, 'plan':round(float(theclient.inventory)*1.1, 2), 'finish':round(float(theclient.inventory), 2), 'percentage':1.1 })
        data.append({'month':5, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
        data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
"""

def inventory_kehu_related_data_specific(request):
        client_name = request.REQUEST['name']
        #ywyname = u'全部'
        if client_name == u'全部':
                results = inventory.objects.all()
        else:
                results = inventory.objects.filter(yh=client_name)
        results.order_by('-kcje')
        data = []
        timeline = datetime.date.today() + datetime.timedelta(days=90)
        for item in results:
                if item.yjckrq > timeline:
                        is_over_three_month = u'是'
                else:
                        is_over_three_month = u'否'
                data.append({'inventory_money':round(float(item.kcje),2),
                                         'user':item.yh,
                     'contract_no':item.hth,
                                         'sign_time':item.zhrkrq.strftime("%Y-%m-%d"),
                                         'is_over_three_month':is_over_three_month,
                                         'want_time':item.yjckrq.strftime("%Y-%m-%d"),
                                         'maintain_time':item.whrq.strftime("%Y-%m-%d")
                                         })
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def inventory_kehu_related_data(request):
        client_name = request.REQUEST['name']
        theclient = client.objects.get(name=client_name)
        timeline = datetime.date.today()+datetime.timedelta(days=90)
        if client_name == u'全部':
                over_three_month = checkin.objects.filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
                with_in_three_month = checkin.objects.filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
        else:
                over_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__gt=timeline).aggregate(Sum('ysye'))
                with_in_three_month = checkin.objects.filter(yh=client_name).filter(yjysrq__lte=timeline).aggregate(Sum('ysye'))
        if over_three_month['ysye__sum']== None :
                over_three_month = 0
        else:
                over_three_month = float(over_three_month['ysye__sum'])
        if with_in_three_month['ysye__sum'] == None :
                with_in_three_month = 0
        else:
                with_in_three_month = float(with_in_three_month['ysye__sum'])
        data = [                  {'related_data_title':'所选择客户的库存', 'related_data_data':round(float(theclient.inventory), 2)},
                                          {'related_data_title':'与上月相比的波动','related_data_data':round(float(theclient.inventory), 2)},
                                          {'related_data_title':'上月收款计划完成百分比','related_data_data':0.8},
                                          {'related_data_title':'三个月以内','related_data_data':round(over_three_month,2)},
                                          {'related_data_title':'三个月以上','related_data_data':round(with_in_three_month,2)}
                        ]
        return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
##################库存分析完毕########################



############################合同分析##########################
def contract_table(request):
	ywys = yewuyuan.objects.all().order_by('-dispatch_sum')
	data = []
	rank = 0
	for item in ywys:
		data.append({'name':item.name,'rank':rank,'contract_money':item.dispatch_sum})
		rank += 1
	return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def contract_names(request):
	ywys = yewuyuan.objects.all().order_by('-dispatch_sum')
	data = []
	for item in ywys:
		data.append({'name':item.name})
	return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def contract_related_data(request):
    thename = request.REQUEST['name']
    theywy = yewuyuan.objects.get(name=thename)
    year_plan = record.objects.get(related_id=theywy.dispatch_plan,month=0)
    print year_plan
    data = [
				{'related_data_title':'所选择人的合同','related_data_data':round(float(theywy.dispatch_sum),2)},
				{'related_data_title':'全年计划','related_data_data':round(float(year_plan.num),2)},
				{'related_data_title':'完成计划百分比(%)','related_data_data':round(float(theywy.dispatch_sum/year_plan.num*100),2)}
			]
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def contract_chart_data(request):
    data = []
    thename = request.REQUEST['name']
    theywy = yewuyuan.objects.get(name=thename)
    year_plan = record.objects.get(related_id=theywy.dispatch_plan,month=0)
    data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':4, 'plan':round(float(year_plan.num),2), 'finish':round(float(theywy.dispatch_sum),2), 'percentage':round(float(theywy.dispatch_sum/year_plan.num),2) })
    data.append({'month':5, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
###############################合同分析完毕#########################



###############################首页api开始####################

"""
url: /index/total_data.json
请求参数：无
返回数据：
[
	{'total_momey_this_month' : 2131.23,			//本月收款计划总额
	'plan_check_this_month' : 2131.23,			//本月开票计划总额
	'finish_inventory_percentage_last_month' : 0.23, //数据上月计划库存完成百分比
	'plan_running' : 45.23,						//办事处本月预计运行指标
	'current _running' : 45.23,					//办事处目前运行指标
	'year _running' : 45.23}						//办事处年度运行指标
]
"""
def index_total_data(request):
    data = [
        {'total_momey_this_month' : 888.88,			#本月收款计划总额
        'plan_check_this_month' : 888.88,			#本月开票计划总额
        'finish_inventory_percentage_last_month' : 0.9, #数据上月计划库存完成百分比
        'finish_checkin_percentage_last_month' : 0.9, #数据上月计划应收完成百分比
        'plan_running' : 0.3,						#办事处本月预计运行指标
        'current_running' : 0.3,					#办事处目前运行指标
        'year_running' : 0.3}						#办事处年度运行指标
        ]
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

"""
按月应收数据
url: /index/total_checkin_data.json/
请求参数：无（是否应该可以是本月的月份？）
返回数据：
[
		{'total_checkin' : 45.23				//总应收
		'checkin_last_month_ fluctuate' : -0.23,	//应收与上月相比的波动
		'checkin_last_year_ fluctuate' : -0.23}		//应收与去年年底相比的波动
]
"""

def index_total_checkin_data(request):
    theone = yewuyuan.objects.get(name=u'全部')
    data = [
                {'related_data_title':'总应收','related_data_data': round(float(theone.checkin_sum),2)},   #总应收
                {'related_data_title':'与上月相比的波动','related_data_data': round(float(theone.checkin_sum-theone.checkin_lastmonth),2)},     #应收与上月相比的波动
                {'related_data_title':'与去年年底相比的波动','related_data_data':round(float(theone.checkin_sum-theone.checkin_lastyear),2)}              #应收与去年年底相比的波动
             ]
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
"""
按月库存数据
url: /index/total_inventory_data.json/
请求参数：无（是否应该可以是本月的月份？）
返回数据：
[
		{'total_inventory' : 45.23				//总库存
		'inventory_last_month_ fluctuate' : -0.23,	//库存与上月相比的波动
		'inventory_last_year_ fluctuate' : -0.23}	//库存与去年年底相比的波动
]
"""

def index_total_inventory_data(request):
    theone = yewuyuan.objects.get(name=u'全部')
    data = [
             {'related_data_title':'总库存','related_data_data':round(float(theone.inventory_sum),2)},                     #总库存
             {'related_data_title':'与上月相比的波动','related_data_data':round(float(theone.inventory_sum-theone.inventory_lastmonth),2)},     #库存与上月相比的波动
             {'related_data_title':'与去年年底相比的波动','related_data_data':round(float(theone.inventory_sum-theone.inventory_lastyear),2)}   #库存与去年年底相比的波动
        ]
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


"""
按月总订单数据
url: /index/total_order_data.json/
请求参数：无（是否应该可以是本月的月份？）
返回数据：
[
		{'total_order' : 45.23				//总订单
		'order_last_month_ fluctuate' : -0.23,	//订单与上月相比的波动
		'order_last_year_ fluctuate' : -0.23}		//订单与去年年底相比的波动
]
"""

def index_total_order_data (request):
    theone = yewuyuan.objects.get(name=u'全部')
    data = [
                 {'related_data_title':'总订单','related_data_data':round(float(theone.dispatch_sum),2)},                  #总订单
                 {'related_data_title':'与上月相比的波动','related_data_data':round(float(theone.dispatch_sum),2)}, #订单与上月相比的波动
                 {'related_data_title':'与去年年底相比的波动','related_data_data':round(float(theone.dispatch_sum),2)}       #订单与去年年底相比的波动
            ]
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

def index_total_checkin_chart(request):
    data = []
    ps = yewuyuan.objects.get(name=u'全部').checkin_rec
    for i in range(1,13):
        item = record.objects.get(related_id=ps,month=i)
        data.append({'month':i, 'plan':round(float(item.num)*1.1, 2), 'finish':round(float(item.num), 2), 'percentage':1.1 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

    """
    theone = yewuyuan.objects.get(name=u'全部')
    data=[]
    data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':4, 'plan':0, 'finish':round(float(theone.checkin_sum),2), 'percentage':0 })
    data.append({'month':5, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
    """

def index_total_inventory_chart(request):
    data = []
    ps = yewuyuan.objects.get(name=u'全部').inventory_rec
    for i in range(1,13):
        item = record.objects.get(related_id=ps,month=i)
        data.append({'month':i, 'plan':round(float(item.num)*1.1, 2), 'finish':round(float(item.num), 2), 'percentage':1.1 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
"""
    theone = yewuyuan.objects.get(name=u'全部')
    data=[]
    data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':4, 'plan':0, 'finish':round(float(theone.inventory_sum),2), 'percentage':0 })
    data.append({'month':5, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
"""


def index_total_order_chart(request):
    theone = yewuyuan.objects.get(name=u'全部')
    data=[]
    data.append({'month':1, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':2, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':3, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':4, 'plan':0, 'finish':5555.55, 'percentage':0 })
    data.append({'month':5, 'plan':0, 'finish':6666.66, 'percentage':0 })
    data.append({'month':6, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':7, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':8, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':9, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':10, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':11, 'plan':0, 'finish':0, 'percentage':0 })
    data.append({'month':12, 'plan':0, 'finish':0, 'percentage':0 })
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

###############################首页api结束####################



####################################指标分析开始##########################
"""
一、库存
数据名称：原因分类
	url: /target/inventory/reason.json
请求参数：无
返回数据：
[
	{'reason'：’资金不足’}
]
"""

def target_inventory_reason (request):
    results = inventory_reason.objects.all()
    data = []
    for item  in results :
        data.append({'reason':item.name})
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

"""

数据名称：客户名称
url: /target/inventory/kehu_name.json
请求参数：无
返回数据：
[
		{'name': ‘上海电机厂’}
]
"""

def target_inventory_kehu_name(request):
    results = client.objects.filter(inventory__gt=0)
    data = []
    for item  in results :
        data.append({'name':item.name})
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")


"""
数据名称：业务员
url: /target/inventory/yewuyuan_name.json
请求参数：无
返回数据：
[
		{'name': ‘蔡一丁’}
]
"""

def target_inventory_yewuyuan_name(request):
    results = yewuyuan.objects.filter(inventory_sum__gt=0)
    data = []
    for item in results :
        data.append({'name':item.name})
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")



"""
数据名称：饼状图数据
url: /target/inventory/pie_chart_data.json
请求参数：
		'reason' : ‘资金不足’			//某条原因
		'kehu_name': ‘上海电机厂’		//客户名称
		'yewuyuan_name' : ‘蔡一丁’		//业务员名称
		'dispatch_time' : ‘2012-05-27’	//可发货时间
		'greater_than_days' : 31			//库存大于31天
		'maintain_date': ‘2012-04-12’	//维护日期在2012-04-12之前的
返回参数：（MODIFIED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
[
		{'son': 89.2,				//分子(所有“库存清单表格项的库存额的总和”)
		'mum' : 99.2}				//分母（总的库存额）
]
"""

def target_inventory_pie_chart_data(request):
    results = inventory.objects.all()
    reason = request.REQUEST['reason']
    if reason != '' and reason != None and reason != u'全部':
        results = results.filter(yyfl=reason)
    kehu_name = request.REQUEST['kehu_name']
    if kehu_name != '' and  kehu_name != None and kehu_name != u'全部':
        results = results.filter(yh=kehu_name)
    yewuyuan_name = request.REQUEST['yewuyuan_name']
    if yewuyuan_name != '' and yewuyuan_name != None and yewuyuan_name != u'全部':
        results = results.filter(ywy=yewuyuan_name)

#    dispatch_time = request.REQUEST['dispatch_time']
#    if dispatch_time != '' and dispatch_name != None:
#        dispatch_time = myfunc.turn_str_to_date(dispatch_time)
#        results = results.filter(yjckrq__lte=dispatch_time)

    dispatch_time = request.REQUEST['dispatch_time']
    if dispatch_time != '' and dispatch_time != None:
        dispatch_time = myfunc.turn_str_to_date(dispatch_time)
        results = results.filter(yjckrq__lte=dispatch_time)

    greater_than_days = request.REQUEST['greater_than_days']
    if greater_than_days != '' and greater_than_days != None:
        greater_than_days = string.atoi(greater_than_days)
        zltime = datetime.date.today() - datetime.timedelta(days=greater_than_days)
        results = results.filter(zhrkrq__lt=zltime)

    maintain_date = request.REQUEST['maintain_date']
    if maintain_date != '' and maintain_date != None:
        maintain_date = myfunc.turn_str_to_date(maintain_date)
        tmptime = datetime.time(0,0)
        whtime = datetime.datetime.combine(maintain_date,tmptime)
        results = results.filter(whrq__lte=whtime)

    results.order_by('-kcje_sum')

    son = results.aggregate(Sum('kcje'))

    if son['kcje__sum'] == None:
        son = 0
    else:
        son = son['kcje__sum']

    mum = yewuyuan.objects.get(name=u'全部').inventory_sum
    print son,' ',mum
    data = [
            {'name':'所选部分','item_data':round(float(son)+0.00000000001,2)},
            {'name':'剩余部分','item_data':(round(float(mum),2)-round(float(son),2))+0.00000000001}
    ]
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

"""
数据名称：库存清单
url: /target/inventory/table_data.json
请求参数：
		'reason' : ‘资金不足’			//某条原因
		'kehu_name': ‘上海电机厂’		//客户名称
		'yewuyuan_name' : ‘蔡一丁’		//业务员名称
		'dispatch_time' : ‘2012-05-27’	//可发货时间
		'greater_than_days' : 31			//库存大于31天
		'maintain_date': ‘2012-04-12’	//维护日期在2012-04-12之前的
返回参数：
[
		{
			'contract_no' : ‘A12/00-4009’,			//合同号
			'user' : ‘北方重工集团有限公司物资分公司’, 		//用户
			'current_inventory_number' : 3, 			//当前库存数
			'inventory_money' : 98.3,				//库存金额
			'inbventory_date' : ‘2011-05-07’, 			//最后入库日期
			'inventory_kind' : ‘延期’,				//库存分类
			'come_out_date': ‘2012-06-07’,			//预计出库日期
			'suggestion' : ‘多与用户沟通，确保4月发货。’,  //部门分管负责人意见
			'maintain_date' : ‘2012-04-6’					//维护日期
	}
]
"""

def target_inventory_table_data(request):
    results = inventory.objects.all()
    reason = request.REQUEST['reason']
    if  reason != None and reason != '' and reason != u'全部':
        results = results.filter(yyfl=reason)

    kehu_name = request.REQUEST['kehu_name']
    if kehu_name != '' and kehu_name != None and kehu_name != u'全部':
        results = results.filter(yh=kehu_name)

    yewuyuan_name = request.REQUEST['yewuyuan_name']
    if yewuyuan_name != '' and yewuyuan_name != None and yewuyuan_name != u'全部':
        results = results.filter(ywy=yewuyuan_name)

    dispatch_time = request.REQUEST['dispatch_time']
    if dispatch_time != '' and dispatch_time != None:
        dispatch_time = myfunc.turn_str_to_date(dispatch_time)
        results = results.filter(yjckrq__lte=dispatch_time)

    greater_than_days = request.REQUEST['greater_than_days']
    if greater_than_days != '' and greater_than_days != None:
        greater_than_days = string.atoi(greater_than_days)
        zltime = datetime.date.today() - datetime.timedelta(days=greater_than_days)
        results = results.filter(zhrkrq__lt=zltime)

    maintain_date = request.REQUEST['maintain_date']
    if maintain_date != '' and maintain_date != None:
        maintain_date = myfunc.turn_str_to_date(maintain_date)
        tmptime = datetime.time(0,0)
        whtime = datetime.datetime.combine(maintain_date,tmptime)
        results = results.filter(whrq__lte=whtime)

    results.order_by('-inventory_sum')

    data = []

    for item in results:
        data.append ({
                'contract_no' : item.hth,			#合同号
			    'user' : item.yh, 		#//用户
			    'current_inventory_number' : round(float(item.dqkcs),2),# 			//当前库存数
			    'inventory_money' : round(float(item.kcje),2),	#			//库存金额
			    'inventory_date' :item.zhrkrq.strftime("%Y-%m-%d"), 			#//最后入库日期
			    'inventory_kind' : item.kcfl,				#//库存分类
			    'come_out_date': item.yjckrq.strftime("%Y-%m-%d"),#			//预计出库日期
			    'suggestion' : item.bmclyj,#  //部门分管负责人意见
			    'maintain_date' : item.whrq.strftime("%Y-%m-%d")#				//维护日期
                })

    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")   

"""

二、应收
数据名称：原因分类
	url: /target/checkin/reason.json
请求参数：无
返回数据：
[
	{'reason'：’资金不足’}
]
"""
def target_checkin_reason (request):
    results = checkin_reason.objects.all()
    data = []
    for item  in results :
        data.append({'reason':item.name})
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

"""

数据名称：客户名称
url: /target/checkin/kehu_name.json
请求参数：无
返回数据：
[
		{'name': ‘上海电机厂’}
]
"""

def target_checkin_kehu_name(request):
    results = client.objects.filter(checkin__gt=0)
    data = []
    for item  in results :
        data.append({'name':item.name})
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

"""

数据名称：业务员
url: /target/checkin/yewuyuan_name.json
请求参数：无
返回数据：
[
		{'name': ‘蔡一丁’}
]
"""

def target_checkin_yewuyuan_name(request):
    results = yewuyuan.objects.filter(checkin_sum__gt=0)
    data = []
    for item  in results :
        data.append({'name':item.name})
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")
"""


数据名称：饼状图数据
url: /target/checkin/pie_chart_data.json
请求参数：
		'reason' : ‘资金不足’			//某条原因
		'kehu_name': ‘上海电机厂’		//客户名称
		'yewuyuan_name' : ‘蔡一丁’		//业务员名称
		'checkin_time' : ‘2012-05-27’	//预计可收款时间
		'greater_than_days' : 31			//应收大于31天
		'maintain_date': ‘2012-04-12’	//维护日期在2012-04-12之前的
返回参数：
[
		{'son': 89.2,				//分子(所有“应收清单表格项的应收额的总和”)
		'mum' : 99.2}				//分母（总的应收额）
]
"""


def target_checkin_pie_chart_data (request):
    results = checkin.objects.all()

    reason = request.REQUEST['reason']
    if reason != None and reason != '' and reason != u'全部':
        results = results.filter(yyfl=reason)

    kehu_name = request.REQUEST['kehu_name']
    if kehu_name != None and kehu_name != '' and kehu_name != u'全部':
        results = results.filter(yh=kehu_name)


    yewuyuan_name = request.REQUEST['yewuyuan_name']
    if yewuyuan_name != None and yewuyuan_name != '' and yewuyuan_name != u'全部':
        results = results.filter(ywy=yewuyuan_name)


    checkin_time = request.REQUEST['checkin_time']
    if checkin_time != None and checkin_time != '':
        checkin_time = myfunc.turn_str_to_date(checkin_time)
        results = results.filter(yjysrq__lte=checkin_time)

    greater_than_days = request.REQUEST['greater_than_days']
    if greater_than_days != None and greater_than_days != '':
        greater_than_days = string.atoi(greater_than_days)
        zltime = datetime.date.today() - datetime.timedelta(days=greater_than_days)
        results = results.filter(kprq__lt=zltime)

    maintain_date = request.REQUEST['maintain_date']
    if maintain_date != None and maintain_date != '':
        maintain_date = myfunc.turn_str_to_date(maintain_date)
        tmptime = datetime.time(0,0)
        whtime = datetime.datetime.combine(maintain_date,tmptime)
        results = results.filter(whrq__lte=whtime)

    results.order_by('-ysye_sum')


    son = results.aggregate(Sum('ysye'))
    print son
    if son['ysye__sum'] == None :
        son = 0
    else:
        son = son['ysye__sum']

    mum = yewuyuan.objects.get(name=u'全部').checkin_sum
    data = [
            {'name':'所选部分','item_data':round(float(son)+0.01,2)},
            {'name':'剩余部分','item_data':(round(float(mum),2)-round(float(son),2))+0.01}
    ]
    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")

"""

数据名称：应收清单
url: /target/checkin/table_data.json
请求参数：
		'reason' : ‘资金不足’			//某条原因
		'kehu_name': ‘上海电机厂’		//客户名称
		'yewuyuan_name' : ‘蔡一丁’		//业务员名称
		'checkin_time' : ‘2012-05-27’	//预计可收款时间
		'greater_than_days' : 31			//应收大于31天
		'maintain_date': ‘2012-04-12’	//维护日期在2012-04-12之前的
返回参数：
[
		{
			'contract_no' : ‘A12/00-4009’,			//合同号
			'user' : ‘北方重工集团有限公司物资分公司’, 		//用户
			'checkin _money' : 98.3,				//应收余额
			'checkin_money_not_come' : 98.3,	//应收未收
			'checkin _kind' : ‘延期’,				//应收分类
			'suggestion' : ‘多与用户沟通，确保4月发货。’,  //部门处理意见
			'maintain_date' : ‘2012-04-6’					//维护日期
	}
]
"""


def target_checkin_table_data(request):
    results = checkin.objects.all()
    reason = request.REQUEST['reason']
    if reason != None and reason != '' and reason != u'全部':
        results = results.filter(yyfl=reason)

    kehu_name = request.REQUEST['kehu_name']
    if kehu_name != None and kehu_name != '' and kehu_name != u'全部':
        results = results.filter(yh=kehu_name)

    yewuyuan_name = request.REQUEST['yewuyuan_name']
    if yewuyuan_name != None and yewuyuan_name != '' and yewuyuan_name != u'全部':
        results = results.filter(ywy=yewuyuan_name)

#    checkin_time = request.REQUEST['checkin_time']
#    if checkin_time != None and checkin_time != '':
#        checkin_time = myfunc.turn_str_to_date(checkin_time)
#        results = results.filter(yjysrq_lte=checkin_time)

    checkin_time = request.REQUEST['checkin_time']
    if checkin_time != None and checkin_time != '':
        checkin_time = myfunc.turn_str_to_date(checkin_time)
        results = results.filter(yjysrq__lte=checkin_time)

    greater_than_days = request.REQUEST['greater_than_days']
    if greater_than_days != None and greater_than_days != '':
        greater_than_days = string.atoi(greater_than_days)
        zltime = datetime.date.today() - datetime.timedelta(days=greater_than_days)
        results = results.filter(kprq__lt=zltime)

    maintain_date = request.REQUEST['maintain_date']
    if maintain_date != None and maintain_date != '':
        maintain_date = myfunc.turn_str_to_date(maintain_date)
        tmptime = datetime.time(0,0)
        whtime = datetime.datetime.combine(maintain_date,tmptime)
        results = results.filter(whrq__lte=whtime)

    results.order_by('-ysye_sum')
    data = []

    for item in results:
        data.append({
                    'contract_no' : item.hth,#			//合同号
			        'user' : item.yh,# 		//用户
			        'checkin_money' : round(float(item.ysye),2),		#		//应收余额
			        'checkin_money_not_come' : round(float(item.ysws),2),#	//应收未收
			        'checkin_kind' : item.ysfl,#				//应收分类
			        'suggestion' : item.bmclyj,  #//部门处理意见
			        'maintain_date' : item.whrq.strftime("%Y-%m-%d"),		#			//维护日期
                    'sign_time':item.kprq.strftime("%Y-%m-%d"),
                    'want_time':item.yjysrq.strftime("%Y-%m-%d")
                    })


    return HttpResponse(json.dumps(data,ensure_ascii=False), mimetype="application/json")   


##############################################指标分析结束######################################
