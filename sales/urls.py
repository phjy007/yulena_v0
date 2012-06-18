# -*- coding:UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('yulena.views',
    #Ajax api url
#    (r'^main/$','showmain'),
#    (r'^main/$','showmain'),
#    (r'^showkc/$','showkc'),
#    (r'^showys/$','showys'),
#    (r'^showdd/$','showdd'),
#    (r'^showysfx/$','showysfx'),
#    (r'^showkcfx/$','showkcfx'),
    
	(r'^checkin/yewuyuan/table.json/$','checkin_yewuyuan_table'),
	(r'^checkin/yewuyuan/names.json/$','checkin_yewuyuan_names'),
	(r'^checkin/yewuyuan/related_data.json/$','checkin_yewuyuan_related_data'),
	(r'^checkin/yewuyuan/chart_data.json/$','checkin_yewuyuan_chart_data'),
	(r'^checkin/yewuyuan/related_data_specific.json/$','checkin_yewuyuan_related_data_specific'),
    (r'^checkin/kehu/table.json/$','checkin_kehu_table'),
	(r'^checkin/kehu/names.json/$','checkin_kehu_names'),
	(r'^checkin/kehu/related_data.json/$','checkin_kehu_related_data'),
	(r'^checkin/kehu/related_data_specific.json/$','checkin_kehu_related_data_specific'),
    (r'^checkin/kehu/chart_data.json/$','checkin_kehu_chart_data'),
    
    (r'^inventory/yewuyuan/table.json/$','inventory_yewuyuan_table'),
	(r'^inventory/yewuyuan/names.json/$','inventory_yewuyuan_names'),
	(r'^inventory/yewuyuan/related_data.json/$','inventory_yewuyuan_related_data'),
	(r'^inventory/yewuyuan/chart_data.json/$','inventory_yewuyuan_chart_data'),
	(r'^inventory/yewuyuan/related_data_specific.json/$','inventory_yewuyuan_related_data_specific'),
    (r'^inventory/kehu/table.json/$','inventory_kehu_table'),
	(r'^inventory/kehu/names.json/$','inventory_kehu_names'),
	(r'^inventory/kehu/related_data.json/$','inventory_kehu_related_data'),
	(r'^inventory/kehu/related_data_specific.json/$','inventory_kehu_related_data_specific'),
    (r'^inventory/kehu/chart_data.json/$','inventory_kehu_chart_data'),

    (r'^contract/table.json/$','contract_table'),
	(r'^contract/names.json/$','contract_names'),
	(r'^contract/related_data.json/$','contract_related_data'),
	(r'^contract/chart_data.json/$','contract_chart_data'),
    
    (r'^updatedb/$','updatedb'),

	(r'^target/inventory/reason.json/$','target_inventory_reason'),
    (r'^target/inventory/kehu_name.json/$','target_inventory_kehu_name'),
    (r'^target/inventory/yewuyuan_name.json/$','target_inventory_yewuyuan_name'),
    (r'^target/inventory/pie_chart_data.json/$','target_inventory_pie_chart_data'),
    (r'^target/inventory/table_data.json/$','target_inventory_table_data'),
    (r'^target/checkin/reason.json/$','target_checkin_reason'),
    (r'^target/checkin/kehu_name.json/$','target_checkin_kehu_name'),
    (r'^target/checkin/yewuyuan_name.json/$','target_checkin_yewuyuan_name'),
    (r'^target/checkin/pie_chart_data.json/$','target_checkin_pie_chart_data'),
    (r'^target/checkin/table_data.json/$','target_checkin_table_data'),


    (r'^index/total_data.json/$','index_total_data'),
    (r'^index/total_checkin_data.json/$','index_total_checkin_data'),
    (r'^index/total_inventory_data.json/$','index_total_inventory_data'),
    (r'^index/total_order_data.json/$','index_total_order_data'),
    (r'^index/total_checkin_chart.json/$','index_total_checkin_chart'),
    (r'^index/total_inventory_chart.json/$','index_total_inventory_chart'),
    (r'^index/total_order_chart.json/$','index_total_order_chart'),

    #HTML page request url
    (r'^$','show_login'),
    (r'^login_page/$','show_login'),
    (r'^login/$','login_view'),
    (r'^logout/$','logout_view'),
    (r'^index/$','show_index'),
    (r'^checkin/$','show_checkin'),
    (r'^checkin_kehu/$','show_checkin_kehu'),
    (r'^contract/$','show_contract'),
    (r'^inventory/$','show_inventory'),
    (r'^inventory_kehu/$','show_inventory_kehu'),
    (r'^target_inventory/$','show_inventory_target'),
    (r'^target_checkin/$','show_checkin_target'),
#    (r'^plan/$','show_plan'),


    # Examples:
    # url(r'^$', 'sales.views.home', name='home'),
    # url(r'^sales/', include('sales.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)