Ext.define('reason_list',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'reason',   type: 'string'}
    ]
});

Ext.define('kehu_name_list',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'name',   type: 'string'}
    ]
});

Ext.define('yewuyuan_name_list',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'name',   type: 'string'}
    ]
});


Ext.define('all_result',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'mum',   type: 'float'}
    ]
});
Ext.define('choose_result',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'son',   type: 'float'}
    ]
});


Ext.define('pie_data',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'item_data',   type: 'float'},
        {name: 'name',        type: 'string'}
    ]
});

Ext.define('inventory_table_data',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'contract_no',                   type: 'string'},
        {name: 'user',                          type: 'string'},
        {name: 'current_inventory_number',      type: 'float'},
        {name: 'inventory_money',               type: 'float'},
        {name: 'inventory_date',                type: 'string'},
        {name: 'inventory_kind',                type: 'string'},
        {name: 'come_out_date',                 type: 'string'},
        {name: 'suggestion',                    type: 'string'},
        {name: 'maintain_date',                 type: 'string'}
    ]
});

Ext.define('checkin_table_data',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'contract_no',                   type: 'string'},
        {name: 'user',                          type: 'string'},
        {name: 'checkin_money',                 type: 'float'},
        {name: 'checkin_money_not_come',        type: 'float'},
        {name: 'checkin_kind',                 type: 'string'},
        {name: 'suggestion',                    type: 'string'},
        {name: 'maintain_date',                 type: 'string'},
        {name: 'sign_time',                 type: 'string'},
        {name: 'want_time',                 type: 'string'}
    ]
});
