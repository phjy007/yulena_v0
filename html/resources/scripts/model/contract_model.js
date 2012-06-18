Ext.define('contract_table',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'contract_money',   	type: 'float'},
		{name: 'name',  			type: 'string'},
		{name: 'rank', 				type: 'int'}
    ]
});

Ext.define('contract_names',{
	extend: 'Ext.data.Model',
	fields: [
		{name: 'name', type: 'string'}
	]
});

Ext.define('related_data',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'related_data_data', 		type: 'float'},
        {name: 'related_data_title',  		type: 'string'}
    ]
});

Ext.define('contract_chart_model',{
	extend: 'Ext.data.Model',
	fields: [
        {name: 'month',   	            type: 'int'},
		{name: 'plan',  			    type: 'float'},
		{name: 'finish', 				type: 'float'},
        {name: 'percentage', 		    type: 'float'}
    ]
});
