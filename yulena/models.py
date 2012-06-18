# -*- coding:UTF-8 -*-
from django.db import models
from django.contrib import admin

class record(models.Model):
    #记录表，提供各项数据的记录
    month = models.IntegerField(default=0)
    #这项记录的月份
    #如月份为0，则为去年年底
    #如年份为13，则为整年总和
    num = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #记录的数值
    related_id = models.IntegerField(default=0)
    #关联的id，一般用于找father-id
 
class checkin_reason(models.Model):
    name = models.CharField(max_length=50)
    #原因名称

class inventory_reason(models.Model):
    name = models.CharField(max_length=50)
    #原因名称

class yewuyuan(models.Model):
    """
        业务员表:
    """
    name = models.CharField(max_length=50)
    #名字：业务员表
    dispatch_plan = models.IntegerField(default=0)
    #订单计划
    dispatch_sum = models.IntegerField(default=0)
    #实际的订单
    inventory_rec = models.IntegerField(default=0)
    #库存的记录
    inventory_sum = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #总库存
    inventory_lastmonth = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #上月月底库存：常数表
    inventory_lastyear = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #去年年底库存：常数表
    inventory_plan = models.IntegerField(default=0)
    #库存计划
    checkin_sum = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #应收总和
    checkin_lastmonth = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #上月月底应收
    checkin_lastyear = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #去年年底应收
    checkin_rec = models.IntegerField(default=0)
    #应收记录
    checkin_plan = models.IntegerField(default=0)
    #应收计划

    
class client(models.Model):
    name = models.CharField(max_length=50)
    #名称
    inventory = models.DecimalField(max_digits=18,decimal_places=5,default=0)
    #总库存
    inventory_rec =  models.IntegerField(default=0)
    #库存记录
    checkin = models.DecimalField(max_digits=18,decimal_places=5,default=0) 
    #应收总和
    checkin_rec = models.IntegerField(default=0)
    #应收记录
class checkin(models.Model):
    wd = models.CharField(max_length=520)
    # A 1 网点
    yh = models.CharField(max_length=220)
    # B 2 用户
    zzyh = models.CharField(max_length=220)
    # C 3 最终用户
    hy = models.CharField(max_length=220)
    # D 4 行业
    ywy = models.CharField(max_length=220)
    # E 5 业务员
    hth = models.CharField(max_length=220)
    # F 6 合同号
    ysye = models.DecimalField(max_digits=18,decimal_places=5) 
    # G 7 应收余额
    ysws = models.DecimalField(max_digits=18,decimal_places=5) 
    # H 8 应收未收
    kprq = models.DateField()
    # I 9 开票日期
    ysfl = models.CharField(max_length=220)
    # J 10 应收分类
    yyfx = models.CharField(max_length=520)
    # K 11 原因分析
    yyfl = models.CharField(max_length=220)
    # L 12 原因分类
    yjysrq = models.DateField()
    # M 13 预计应收日期
    bmfgfzr = models.CharField(max_length=50)
    # N 14 部门分管责任人
    bmfgfzryj = models.CharField(max_length=520)
    # O 15 部门分管负责人意见
    bmclyj = models.CharField(max_length=520)
    # P 16 部门处理意见
    ysbz = models.CharField(max_length=520)
    # Q 17 应收备注
    whrq = models.DateTimeField()
    # R 18 维护日期

class inventory(models.Model):
    wd = models.CharField(max_length=50) 
    # A 1 网点
    yh = models.CharField(max_length=220)
    # B 2 用户
    zzyh = models.CharField(max_length=220)
    # C 3 最终用户
    hy = models.CharField(max_length=220)
    # D 4 行业
    ywy = models.CharField(max_length=50)
    # E 5 业务员 
    hth = models.CharField(max_length=220)
    # F 6 合同号
    gzh = models.CharField(max_length=220)
    # G 7 工作号
    dqkcs = models.IntegerField()
    # H 8 当前库存数
    kcje = models.DecimalField(max_digits=18,decimal_places=5) 
    # I 9 库存金额
    zhrkrq = models.DateField()
    # J 10 最后入库日期
    ykwtje = models.DecimalField(max_digits=18,decimal_places=5) 
    # K 11 已开未提金额
    kcfl = models.CharField(max_length=220)
    # L 12 库存分类
    yyfx = models.CharField(max_length=520)
    # M 13 原因分析
    yyfl = models.CharField(max_length=220)
    # N 14 原因分类
    yjckrq = models.DateField()
    # O 15 预计出库日期
    bmfgfzr = models.CharField(max_length=220)
    # P 16 部门分管负责人
    bmfgfzryj = models.CharField(max_length=520)
    # Q 17 部门分管负责人意见
    bmclyj = models.CharField(max_length=520)
    # R 18 部门处理意见
    kcbz = models.CharField(max_length=520)
    # S 19 库存备注
    whrq = models.DateTimeField()
    # T 20 维护日期
    
class glvar(models.Model):
    updatetime = models.DateTimeField()
    # 更新时间
    uptimes = models.IntegerField(default=0)
    # 更新次数
    for_rec = models.IntegerField(default=0)
    #专门给record做游标用的
    zhibiao_now = models.DecimalField(max_digits=8,decimal_places=3,default=0) 
    #目前指标
    zhibiao_year = models.DecimalField(max_digits=8,decimal_places=3,default=0) 
    #年度指标
    zhibiao_month = models.DecimalField(max_digits=8,decimal_places=3,default=0) 
    #月度指标
class glvarAdmin(admin.ModelAdmin):
    list_display = ('id','updatetime','uptimes','zhibiao_now','zhibiao_year','zhibiao_month')
class inventoryAdmin(admin.ModelAdmin):
    list_display = ('id','ywy','yh','dqkcs','kcje')
class checkinAdmin(admin.ModelAdmin):
    list_display = ('id','ywy','yh','ysye','ysws')
class clientAdmin(admin.ModelAdmin):
    list_display = ('id','name','checkin','inventory')
class yewuyuanAdmin(admin.ModelAdmin):
    list_display = ('id','name','dispatch_sum','inventory_sum','checkin_sum')


admin.site.register(yewuyuan,yewuyuanAdmin)
admin.site.register(glvar,glvarAdmin)
admin.site.register(inventory,inventoryAdmin)
admin.site.register(client,clientAdmin)
admin.site.register(checkin,checkinAdmin)

    
