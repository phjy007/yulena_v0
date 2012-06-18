
Ext.onReady(function() {
    var store_taget_table_grid, reason_list_combo, kehu_name_list_combo, yewuyuan_name_list_combo, date_select;
    var dount, pie_panel;
//				Ext.QuickTips.init();
//				Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));

				var store_target_pie = Ext.create('Ext.data.Store', {
					model: pie_data,
                    proxy: {
						type: 'ajax',
						url : '/target/checkin/pie_chart_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});

                store_target_pie.load({
                    params:{  'reason':'',
                               'kehu_name':'',
                                'yewuyuan_name':'',
                                'checkin_time':'',
                                'greater_than_days': '',
                                'maintain_date': ''
                    },
					//scope   : this,
					callback: function(records, operation, success) {
						showPie(store_target_pie);
                        Ext.getCmp("choose_result").setValue(store_target_pie.getAt(0).get('item_data')+'万元');
                        Ext.getCmp("all_result").setValue((parseFloat(store_target_pie.getAt(1).get('item_data'))+parseFloat(store_target_pie.getAt(0).get('item_data'))).toFixed(2)+'万元');
					}
				});
               
                var store_reason_list = Ext.create('Ext.data.Store', {
					model: 'reason_list',
					proxy: {
						type: 'ajax',
						url : '/target/checkin/reason.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});

                var store_kehu_name_list = Ext.create('Ext.data.Store', {
					model: 'kehu_name_list',
					proxy: {
						type: 'ajax',
						url : '/target/checkin/kehu_name.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});

                var store_yewuyuan_name_list = Ext.create('Ext.data.Store', {
                                model: 'yewuyuan_name_list',
                                proxy: {
                                    type: 'ajax',
                                    url : '/target/checkin/yewuyuan_name.json',
                                    reader: {
                                        type: 'json',
                                        totalProperty  : 'total',
                                        successProperty: 'success'
                                    }
                                }
                            });

                var store_taget_table = Ext.create('Ext.data.Store', {
					model: 'checkin_table_data',
					proxy: {
						type: 'ajax',
						url : '/target/checkin/table_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_taget_table.load({
                    params:{  'reason':'',
                               'kehu_name':'',
                                'yewuyuan_name':'',
                                'checkin_time':'',
                                'greater_than_days': '',
                                'maintain_date': ''
                    },
					//scope   : this,
					callback: function(records, operation, success) {
						showTargetTable(store_taget_table);
					}
				});

    var simple = Ext.create('Ext.form.Panel', {
//        url:'save-form.php',
        frame:true,
        title: '选择区域',
        bodyStyle:'padding:5px 5px 0',
        width: 320,
        fieldDefaults: {
            msgTarget: 'side',
            labelWidth: 75
        },
        defaultType: 'textfield',
        defaults: {
            anchor: '100%'
        },

        items: [{
            xtype: 'combobox',
            id: 'reason_list_combo',
            fieldLabel: '原因',
            labelWidth: 80,
            store: store_reason_list,
            typeAhead: true,
            emptyText: '全部原因',
             displayField: 'reason'
        },{
            xtype: 'combobox',
            id: 'kehu_name_combo',
            fieldLabel: '客户',
            labelWidth: 80,
            store: store_kehu_name_list,
            typeAhead: true,
            emptyText: '全部客户',
            displayField: 'name'
        },{
            xtype: 'combobox',
            id: 'yewuyuan_name_combo',
            fieldLabel: '业务员',
            labelWidth: 80,
            store: store_yewuyuan_name_list,
            typeAhead: true,
            emptyText: '全部业务员',
            displayField: 'name'
        }, {
            xtype: 'datefield',
            id: 'checkin_time_combo',
			anchor: '100%',
			fieldLabel: '预计可收款',
			name: 'from_date',
//            value: new Date(),
            format:'Y-m-d'
        }, {
           xtype: 'datefield',
		    anchor: '100%',
		    fieldLabel: '维护时间',
		   name: 'maintain_date',
            id: 'maintain_time_comb',
//		    value: new Date(),
           format:'Y-m-d'
        }, {
           fieldLabel: '账龄小于(天)',
           name: 'last',
           id: 'greater_than_days'
        }, {
           fieldLabel: '筛选结果',
           name: 'last',
           id: 'choose_result',
           value: '-'
        }, {
           fieldLabel: '总额',
           name: 'last',
           id: 'all_result',
           value: '-'
        }],
        buttons: [{
            text: '查询',
            handler: function(){
//                alert(Ext.util.Format.date(Ext.getCmp("maintain_time_comb").getValue(), 'Y-m-d'));
//                    alert(Ext.getCmp("greater_than_days").getValue());
                 store_target_pie.load({
                     params:{
                         "reason":              Ext.getCmp("reason_list_combo").getValue(),
                         "kehu_name":           Ext.getCmp("kehu_name_combo").getValue(),
                         "yewuyuan_name":       Ext.getCmp("yewuyuan_name_combo").getValue(),
                         "checkin_time":       Ext.util.Format.date(Ext.getCmp("checkin_time_combo").getValue(), 'Y-m-d'),
                         "greater_than_days":   Ext.getCmp("greater_than_days").getValue(),
                         "maintain_date":       Ext.util.Format.date(Ext.getCmp("maintain_time_comb").getValue(), 'Y-m-d')
                     },
                     //scope   : this,
                     callback: function(records, operation, success) {
                        Ext.getCmp("choose_result").setValue(store_target_pie.getAt(0).get('item_data')+'万元');
                        Ext.getCmp("all_result").setValue((parseFloat(store_target_pie.getAt(1).get('item_data'))+parseFloat(store_target_pie.getAt(0).get('item_data'))).toFixed(2)+'万元');
                        pie_panel.update();
                     }
                 });
                store_taget_table.load({
                     params:{
                         "reason":              Ext.getCmp("reason_list_combo").getValue(),
                         "kehu_name":           Ext.getCmp("kehu_name_combo").getValue(),
                         "yewuyuan_name":       Ext.getCmp("yewuyuan_name_combo").getValue(),
                         "checkin_time":       Ext.util.Format.date(Ext.getCmp("checkin_time_combo").getValue(), 'Y-m-d'),
                         "greater_than_days":   Ext.getCmp("greater_than_days").getValue(),
                         "maintain_date":       Ext.util.Format.date(Ext.getCmp("maintain_time_comb").getValue(), 'Y-m-d')
                     },
                     //scope   : this,
                     callback: function(records, operation, success) {
                        store_taget_table_grid.update();
                     }
                 });
            }
        }]
    });
    simple.render('target_left_up_area');
});

function showTargetTable(store_taget_table) {
    store_taget_table_grid = Ext.create('Ext.grid.Panel', {
					store: store_taget_table,
					columns: [
						{text: "合同号", width: 90, dataIndex: 'contract_no', sortable: false},
                        {text: "用户", width: 150, dataIndex: 'user', sortable: false},
						{text: "应收余额", width: 80, dataIndex: 'checkin_money', sortable: true},
                        {text: "开票时间", width: 80, dataIndex: 'sign_time', sortable: true},
						{text: "应收未收", width: 80, dataIndex: 'checkin_money_not_come', sortable: false},
						{text: "应收分类", width: 95, dataIndex: 'checkin_kind', sortable: false},
                        {text: "预计收款时间", width: 80, dataIndex: 'want_time', sortable: true},
                        {text: "维护日期", width: 80, dataIndex: 'maintain_date', sortable: false},
						{text: "负责人意见", width: 70,  dataIndex: 'suggestion', sortable: false}

					],
					renderTo:'target_right_area',
                    title: '应收清单',
					width: 640,
					height: 560
				});
}

function showPie(store_target_pie) {
	pie_panel = Ext.create('widget.panel', {
					width: 320,
					height: 265,
					title: '饼状图 (整个圆饼代表总额)',
					renderTo: 'pie_chart_area',
					layout: 'fit',
					items: {
						xtype: 'chart',
						id: 'chartCmp',
						animate: true,
						store: store_target_pie,
						shadow: true,
						legend: {
							position: 'right'
						},
						insetPadding: 20,
						theme: 'Base:gradients',
						series: [{
							type: 'pie',
							colorSet: ["#CC0003", "#05388F", "#00f"],
							field: 'item_data',
							showInLegend: true,
							donut: false,
							tips: {
							  trackMouse: true,
							  width: 150,
							  height: 28,
							  renderer: function(storeItem, item) {
								var total = 0;
								store_target_pie.each(function(rec) {
									total += rec.get('item_data');
								});
								this.setTitle(storeItem.get('name') + '所占比例: ' + Math.round(storeItem.get('item_data') / total * 100) + '%');
							  }
							},
							highlight: {
							  segment: {
								margin: 10
							  }
							}
//                            ,
//							label: {
//								field: 'name',
//								display: 'rotate',
//								contrast: true,
//								font: '18px Arial'
//							}
						}]
					}
				});
}

