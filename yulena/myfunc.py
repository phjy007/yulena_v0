#-*-  coding:UTF-8  -*-
import xlrd,datetime
from decimal import Decimal
from django.shortcuts import render,render_to_response
from yulena.models import *
import string
from django.http import HttpResponse
import json
from django.db.models import Sum

def turn_str_to_date(strdate):
    mystr = strdate.split('-')
    return datetime.date(string.atoi(mystr[0]),string.atoi(mystr[1]),string.atoi(mystr[2]))

def deal(x):
    if  isinstance(x, (float)):
        return Decimal(str(x))
    else:
        return Decimal(0)

__s_date = datetime.date(1899, 12, 31).toordinal()- 1
def getdate(date):
    if  isinstance(date, (str)):
        return datetime.datetime.now().strftime("%Y-%m-%d")
        e.today().strftime("%Y-%m-%d")
    if  isinstance(date, float):
        date = int(date)
    d = datetime.date.fromordinal(__s_date + date)
    return d.strftime("%Y-%m-%d")

def gettime(date):
    if  isinstance(date, (str)):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    d = datetime.date.fromordinal(__s_date + int(date))
    date = date - int(date)
    date = date * 3600 * 24
    t = datetime.time(int(date/3600),int((date%3600)/60))
    d = datetime.datetime.combine(d,t)
    return d.strftime("%Y-%m-%d %H:%M")
# 时间处理函数，主要将excel表里的时间转成python的datetime类

def initial():
    checkin_reason(name=u'全部').save()
    inventory_reason(name=u'全部').save()
    yewuyuan(name=u'全部').save()
    client(name=u'全部').save()
    glvar(updatetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                       uptimes=0,
                       zhibiao_now=50,
                       zhibiao_year=50,
                       zhibiao_month=50).save()
             

def reset_():
    yewuyuan.objects.all().update(dispatch_sum=0,inventory_sum=0,checkin_sum=0,dispatch_plan=0)
    client.objects.all().update(inventory=0,checkin=0)
    checkin.objects.all().delete()
    inventory.objects.all().delete()
    var = glvar.objects.get(id=1)
    var.uptimes += 1
    var.updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    var.save()

def update_order():
    book = xlrd.open_workbook(r'/media/Data/yulena/yulena-sales/excel/dd.xls')
    sheet = book.sheet_by_index(0)
    thevar = glvar.objects.get(id=1)
    qb = yewuyuan.objects.get(name=u'全部')
    qb_id = qb.dispatch_plan
    ps_thevar_id = thevar.for_rec
    if qb_id == 0:
        ps_thevar_id += 1
        qb_id = ps_thevar_id
        qb.dispatch_plan=qb_id
        qb.save()
    record.objects.filter(related_id=qb_id).update(num=0)
    for i in range(1,sheet.ncols):
        myname = sheet.cell_value(0,i)
        try:
            ywy = yewuyuan.objects.get(name=myname)
        except yewuyuan.DoesNotExist:
            ywy = yewuyuan(name=myname)
            ywy.save()
        plan_id = ywy.dispatch_plan
        if plan_id == 0:
            ps_thevar_id += 1
            plan_id = ps_thevar_id
            ywy.dispatch_plan = plan_id
            ywy.save()
        for j in range(1,14):
            try:
                plan = record.objects.get(related_id=plan_id,month=j-1)
            except record.DoesNotExist:
                plan = record(month=j-1,related_id=plan_id)
                plan.save()
            plan.num = deal(sheet.cell_value(j,i))
            plan.save()
            try:
                qb_plan = record.objects.get(related_id=qb_id,month=j-1)
            except record.DoesNotExist:
                qb_plan = record(month=j-1,related_id=qb_id)
                qb_plan.save()
            qb_plan.num += deal(sheet.cell_value(j,i)) 
            qb_plan.save()
            if j > 1:
                ywy.dispatch_sum += deal(sheet.cell_value(j,i))
                qb.dispatch_sum += deal(sheet.cell_value(j,i))
		ywy.save()
    qb.save()
    thevar.id = ps_thevar_id
    thevar.save()
def update_inventory():
    book = xlrd.open_workbook(r'/media/Data/yulena/yulena-sales/excel/kc.xls')
    sheet = book.sheet_by_index(0)
    for i in range(1,sheet.nrows):
        kc = inventory(
                    wd = sheet.cell_value(i,0),#models.CharField(max_digits=50) 
                    # A 1 网点
                    yh = sheet.cell_value(i,1),#models.CharField(max_digits=220)
                    # B 2 用户
                    zzyh = sheet.cell_value(i,2),#models.CharField(max_digits=220)
                    # C 3 最终用户
                    hy = sheet.cell_value(i,3),#models.CharField(max_digits=220)
                    # D 4 行业
                    ywy = sheet.cell_value(i,4),#models.CharField(max_digits=50)
                    # E 5 业务员 
                    hth = sheet.cell_value(i,5),#models.CharField(max_digits=220)
                    # F 6 合同号
                    gzh = sheet.cell_value(i,6),#models.CharField(max_digits=220)
                    # G 7 工作号
                    dqkcs = int(deal(sheet.cell_value(i,7))),#models.IntegerField()
                    # H 8 当前库存数
                    kcje = deal(sheet.cell_value(i,8)),#models.DecimalField(max_digits=18,decimal_places=5) 
                    # I 9 库存金额
                    zhrkrq = getdate(sheet.cell_value(i,9)),#models.DateField()
                    # J 10 最后入库日期
                    ykwtje = deal(sheet.cell_value(i,10)),#models.DecimalField(max_digits=18,decimal_places=5) 
                    # K 11 已开未提金额
                    kcfl = sheet.cell_value(i,11),#models.CharField(max_digits=220)
                    # L 12 库存分类
                    yyfx = sheet.cell_value(i,12),#models.CharField(max_digits=520)
                    # M 13 原因分析
                    yyfl = sheet.cell_value(i,13),#models.CharField(max_digits=220)
                    # N 14 原因分类
                    yjckrq = getdate(sheet.cell_value(i,14)),#models.DateField()
                    # O 15 预计出库日期
                    bmfgfzr = sheet.cell_value(i,15),#models.CharField(max_digits=220)
                    # P 16 部门分管负责人
                    bmfgfzryj = sheet.cell_value(i,16),#models.CharField(max_digits=520)
                    # Q 17 部门分管负责人意见
                    bmclyj = sheet.cell_value(i,17),#models.CharField(max_digits=520)
                    # R 18 部门处理意见
                    kcbz = sheet.cell_value(i,18),#models.CharField(max_digits=520)
                    # S 19 库存备注
                    whrq = gettime(sheet.cell_value(i,19)))#models.DateTimeField()
                    # T 20 维护日期
        kc.save()
        try:
            ywy = yewuyuan.objects.get(name=sheet.cell_value(i,4))
        except yewuyuan.DoesNotExist:
            ywy = yewuyuan(name=sheet.cell_value(i,4))
        ywy.inventory_sum = ywy.inventory_sum + deal(sheet.cell_value(i,8))
        ywy.save()
        try:
            kh = client.objects.get(name=sheet.cell_value(i,1))
        except client.DoesNotExist:
            kh = client(name=sheet.cell_value(i,1))
        kh.inventory = kh.inventory + deal(sheet.cell_value(i,8))
        kh.save()
        qb = yewuyuan.objects.get(name=u'全部')
        qb.inventory_sum = qb.inventory_sum + deal(sheet.cell_value(i,8))
        qb.save()
        qb = client.objects.get(name=u'全部')
        qb.inventory = qb.inventory + deal(sheet.cell_value(i,8))
        qb.save()
        try:
            tmp = inventory_reason.objects.get(name=sheet.cell_value(i,13))
        except inventory_reason.DoesNotExist:
            inventory_reason(name=sheet.cell_value(i,13)).save()
    
    mon = datetime.date.today().month - 1
    if mon == 0:
        mon = 12
    thevar = glvar.objects.get(id=1)
    ps = thevar.for_rec
    results = yewuyuan.objects.all()
    for item in results:
        if item.inventory_rec == 0:
            ps += 1
            item.inventory_rec = ps
            item.save()
            for i in range(1,13):
                record(month=i,related_id=ps,num=0).save()
        temp = record.objects.get(month=mon,related_id=item.inventory_rec)
        temp.num = item.inventory_sum
        temp.save()
    results = client.objects.all()
    for item in results:
        if item.inventory_rec == 0 :
            ps += 1
            item.inventory_rec = ps
            item.save()
            for i in range(1,13):
                record(month=i,related_id=ps,num=0).save()
	    
        temp = record.objects.get(month=mon,related_id=item.inventory_rec)
        temp.num = item.inventory
        temp.save()
    thevar.for_rec = ps
    thevar.save()
                
        
        
                

        
        



def update_checkin():
    book = xlrd.open_workbook(r'/media/Data/yulena/yulena-sales/excel/ys.xls')
    sheet = book.sheet_by_index(0)
    for i in range(1,sheet.nrows):
        ys = checkin(
                    wd = sheet.cell_value(i,0),#models.CharField(max_digits=520)
                    # A 1 网点
                    yh = sheet.cell_value(i,1),#models.CharField(max_digits=220)
                    # B 2 用户
                    zzyh = sheet.cell_value(i,2),#models.CharField(max_digits=220)
                    # C 3 最终用户
                    hy = sheet.cell_value(i,3),#models.CharField(max_digits=220)
                    # D 4 行业
                    ywy = sheet.cell_value(i,4),#models.CharField(max_digits=220)
                    # E 5 业务员
                    hth = sheet.cell_value(i,5),#models.CharField(max_digits=220)
                    # F 6 合同号
                    ysye = deal(sheet.cell_value(i,6)),#models.DecimalField(max_digits=18,decimal_places=5) 
                    # G 7 应收余额
                    ysws = deal(sheet.cell_value(i,7)),#models.DecimalField(max_digits=18,decimal_places=5) 
                    # H 8 应收未收
                    kprq = getdate(sheet.cell_value(i,8)),#models.DateField()
                    # I 9 开票日期
                    ysfl = sheet.cell_value(i,9),#models.CharField(max_digits=220)
                    # J 10 应收分类
                    yyfx = sheet.cell_value(i,10),#models.CharField(max_digits=520)
                    # K 11 原因分析
                    yyfl = sheet.cell_value(i,11),#models.CharField(max_digits=220)
                    # L 12 原因分类
                    yjysrq = getdate(sheet.cell_value(i,12)),#models.DateField()
                    # M 13 预计应收日期
                    bmfgfzr = sheet.cell_value(i,13),#models.CharField(max_digits=50)
                    # N 14 部门分管责任人
                    bmfgfzryj = sheet.cell_value(i,14),#models.CharField(max_digits=520)
                    # O 15 部门分管负责人意见
                    bmclyj = sheet.cell_value(i,15),#models.CharField(max_digits=520)
                    # P 16 部门处理意见
                    ysbz = sheet.cell_value(i,16),#models.CharField(max_digits=520)
                    # Q 17 应收备注
                    whrq = gettime(sheet.cell_value(i,17)))#models.DateTimeField()
                    # R 18 维护日期
        ys.save()
        try:
            ywy = yewuyuan.objects.get(name=sheet.cell_value(i,4))
        except yewuyuan.DoesNotExist:
            ywy = yewuyuan(name=sheet.cell_value(i,4))
        ywy.checkin_sum = ywy.checkin_sum + deal(sheet.cell_value(i,6))
        ywy.save()
        try:
            kh = client.objects.get(name=sheet.cell_value(i,1))
        except client.DoesNotExist:
            kh = client(name=sheet.cell_value(i,1))
        kh.checkin = kh.checkin + deal(sheet.cell_value(i,6))
        kh.save()
        qb = yewuyuan.objects.get(name=u'全部')
        qb.checkin_sum = qb.checkin_sum + deal(sheet.cell_value(i,6))
        qb.save()
        qb = client.objects.get(name=u'全部')
        qb.checkin = qb.checkin + deal(sheet.cell_value(i,6))
        qb.save()
        try:
            tmp = checkin_reason.objects.get(name=sheet.cell_value(i,11))
        except checkin_reason.DoesNotExist:
            checkin_reason(name=sheet.cell_value(i,11)).save()

    mon = datetime.date.today().month - 1
    if mon == 0:
        mon = 12
    thevar = glvar.objects.get(id=1)
    ps = thevar.for_rec
    results = yewuyuan.objects.all()
    for item in results:
        if item.checkin_rec == 0:
            ps += 1
            item.checkin_rec = ps
            item.save()
            for i in range(1,13):
                record(month=i,related_id=ps,num=0).save()
        temp = record.objects.get(month=mon,related_id=item.checkin_rec)
        temp.num = item.checkin_sum
        temp.save()
    results = client.objects.all()
    for item in results:
        if item.checkin_rec == 0 :
            ps += 1
            item.checkin_rec = ps
            item.save()
            for i in range(1,13):
                record(month=i,related_id=ps,num=0).save()
        temp = record.objects.get(month=mon,related_id=item.checkin_rec)
        temp.num = item.checkin
        temp.save()
    thevar.for_rec = ps
    thevar.save()
def update():
    reset_()
    #update_order()
    update_inventory()
    update_checkin()
    print 'finish update' 
