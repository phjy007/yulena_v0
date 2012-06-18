Ext.define('index_total_data',{
	extend: 'Ext.data.Model',
	fields: [
	{name: 'total_momey_this_month',                 type: 'float'}, //本月收款计划总额
	{name: 'plan_check_this_month',                  type: 'float'}, //本月开票计划总额
	{name: 'finish_inventory_percentage_last_month', type: 'float'}, //数据上月计划库存完成百分比
    {name: 'finish_checkin_percentage_last_month', type: 'float'}, //数据上月计划应收完成百分比
	{name: 'plan_running',                           type: 'float'}, //办事处本月预计运行指标
	{name: 'current_running',                       type: 'float'}, //办事处目前运行指标
	{name: 'year_running',                          type: 'float'}	 //办事处年度运行指标
    ]
});

Ext.define('index_checkin',{    
	extend: 'Ext.data.Model',
	fields: [
        {name: 'related_data_data', 		type: 'float'},
        {name: 'related_data_title',  		type: 'string'}
    ]
});

Ext.define('index_inventory',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'related_data_data', 		type: 'float'},
        {name: 'related_data_title',  		type: 'string'}
    ]
});

Ext.define('index_order',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'related_data_data', 		type: 'float'},
        {name: 'related_data_title',  		type: 'string'}
    ]
});

Ext.define('index_chart_model',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'month',   	            type: 'int'},
		{name: 'plan',  			    type: 'float'},
		{name: 'finish', 				type: 'float'},
        {name: 'percentage', 		    type: 'float'}
    ]
});