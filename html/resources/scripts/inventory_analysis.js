
Ext.onReady(function() {
				//Ext.QuickTips.init();
				//Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));
                var combo_panel, inventory_related_data_grid, inventory_table_grid, related_data_specific_grid, inventory_chart;

                var store_inventory_related_data = Ext.create('Ext.data.Store', {
					model: 'related_data',
					proxy: {
						type: 'ajax',
						url : '/inventory/yewuyuan/related_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_inventory_related_data.load({
                    params:{"name":"全部"},
					//scope   : this,
					callback: function(records, operation, success) {
						showRelatedData(store_inventory_related_data);
					}
				});

				var store_inventory_table = Ext.create('Ext.data.Store', {
					model: 'inventory_table',
					proxy: {
						type: 'ajax',
						url : '/inventory/yewuyuan/table.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
				store_inventory_table.load({
					//scope   : this,
					callback: function(records, operation, success) {
						showInventory_table(store_inventory_table);
					}
				});

                var stroe_inventory_names = Ext.create('Ext.data.Store', {
					model: 'inventory_table',
					proxy: {
						type: 'ajax',
						url : '/inventory/yewuyuan/names.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                stroe_inventory_names.load({
					//scope   : this,
					callback: function(records, operation, success) {
                        combo_panel = Ext.create('Ext.panel.Panel', {
                            bodyPadding: 5,
                            width: 260,
                            title: '人员选择',
                            id: 'combopanel',
                            items: [{
                                xtype: 'combobox',
                                id: 'combobox',
                                fieldLabel: '姓名',
                                labelWidth: 80,
                                store: stroe_inventory_names,
                                typeAhead: true,
                                emptyText: '全部数据',
                                displayField: 'name'
                            }],
                            renderTo: 'contract_analysis_main_statistic_choice'
                        });
                        Ext.getCmp("combobox").on('select', function(comboBox) {
                            var name = comboBox.getValue();
                            store_inventory_related_data.load({
                                params:{"name":name},
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    inventory_related_data_grid.update();
                                }
                            });
                            store_related_data_specific.load({
                                params:{"name":name},
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    store_related_data_specific.update();
                                }
                            });
                            store_chart.load({
                                params:{"name":name},
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    store_chart.update();
                                }
                            });

                        });
//
					}
				});


                var store_chart = Ext.create('Ext.data.JsonStore', {
					model: 'inventory_chart_model',
					proxy: {
						type: 'ajax',
						url : '/inventory/yewuyuan/chart_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_chart.load({
                                params:{"name":'全部'},
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    showInventoryChart(store_chart);
                                }
                });


                var store_related_data_specific = Ext.create('Ext.data.Store', {
					model: 'related_data_specific',
					proxy: {
						type: 'ajax',
						url : '/inventory/yewuyuan/related_data_specific.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_related_data_specific.load({
                    params:{"name":"全部"},
					//scope   : this,
					callback: function(records, operation, success) {
						showRelatedDataSpecific(store_related_data_specific);
					}
				});


		});

function showRelatedData(store_inventory_related_data) {
    inventory_related_data_grid = Ext.create('Ext.grid.Panel', {
					store: store_inventory_related_data,
					columns: [
						{text: "项目", width: 165, dataIndex: 'related_data_title', sortable: false},
						{text: "数据", width: 78, dataIndex: 'related_data_data', sortable: false}
					],
                    title: '综合数据',
					renderTo:'contract_analysis_main_related_data',
					width: 260,
					height: 180,
                    viewConfig: {
						stripeRows: true
					}
	});
}
function dataColorChange(val) {
        if (val > 0) {
            return '<span style="color:green;">' + val + '</span>';
        } else if (val < 0) {
            return '<span style="color:red;">' + val + '</span>';
        }
        return val;
 }

function showInventory_table(store_inventory_table) {
	inventory_table_grid = Ext.create('Ext.grid.Panel', {
					store: store_inventory_table,
					stateful: true,
					stateId: 'stateGrid',
					columns: [
						{
							text     : '排名',
							flex     : 1,
							sortable : true,
                            width    : 20,
							dataIndex: 'rank'
						},
						{
							text     : '销售员',
							flex     : 1,
							sortable : false,
							dataIndex: 'name'
						},
						{
							text     : '库存额',
							sortable : true,
							dataIndex: 'inventory_money'
						}
					],
					height: 280,
					width: 260,
					title: '库存分析表',
					renderTo: 'contract_analysis_main_left',
					viewConfig: {
						stripeRows: true
					}
    });
}

function showCombobox(stroe_inventory_names) {
    combo_panel = Ext.create('Ext.panel.Panel', {
        bodyPadding: 5,
        width: 260,
        title: '人员选择',
        id: 'combopanel',
        items: [{
            xtype: 'combobox',
            id: 'combobox',
            fieldLabel: '姓名',
            labelWidth: 80,
            store: stroe_inventory_names,
            typeAhead: true,
            emptyText: '全部',
            displayField: 'name'
        }],
        renderTo: 'contract_analysis_main_statistic_choice'
    });
//        var combo = Ext.create('Ext.form.field.ComboBox', {
//        renderTo: 'contract_analysis_main_statistic_choice',
//        displayField: 'name',
//        width: 150,
//        store: stroe_inventoryin_names,
//        queryMode: 'local',
//        typeAhead: true,
//        emptyText: '全部',
//        fieldLabel: '姓名',
//        labelWidth: 30
//    });
}

function showRelatedDataSpecific(store_related_data_specific) {
    related_data_specific_grid = Ext.create('Ext.grid.Panel', {
					store: store_related_data_specific,
					columns: [
						{text: "合同号", width: 100, dataIndex: 'contract_no', sortable: true},
						{text: "库存款金额", width: 85, dataIndex: 'inventory_money', sortable: true},
						{text: "用户", width: 235,  dataIndex: 'user', sortable: true},
						{text: "开票时间", width: 98, dataIndex: 'sign_time', sortable: true},
						{text: "库龄", width: 65,  dataIndex: 'is_over_three_month', sortable: false},
                        {text: "预计出库日期", width: 80,  dataIndex: 'want_time', sortable: false},
                        {text: "维护日期", width: 80,  dataIndex: 'maintain_time', sortable: false}
					],
                    title: '具体明细',
					renderTo:'specific_data',
					width: 665,
					height: 270,
                    viewConfig: {
                        stripeRows: true
                    }

				});
}

function showInventoryChart(store_chart) {
    inventory_chart = new Ext.Panel({
					width: 665,
					height: 260,
					title: '库存图',
					renderTo: 'contract_analysis_main_right_chart',
					layout: 'fit',
					items: {
						xtype: 'chart',
						animate: true,
						store: store_chart,
						insetPadding: 30,
						gradients: [{
						  angle: 90,
						  id: 'bar-gradient',
						  stops: {
							  0: {
								  color: '#99BBE8'
							  },
							  70: {
								  color: '#77AECE'
							  },
							  100: {
								  color: '#77AECE'
							  }
						  }
						}],
						axes: [{
							type: 'Numeric',
							minimum: 0,
							maximum: 7000,
							position: 'left',
							fields: ['finish'],
							title: '库存额(万元)',
							grid: true,
							label: {
//								renderer: Ext.util.Format.numberRenderer('0,0'),
								font: '10px Arial'
							}
						}, {
							type: 'Category',
							position: 'bottom',
							fields: ['month'],
							title: false,
							grid: false,
							label: {
								font: '11px Arial',
								renderer: function(month) {
									return month + '月';
								}
							}
						}],
						series: [{
							type: 'column',
							axis: 'left',
							xField: 'month',
							yField: 'finish',
							style: {
								fill: 'url(#bar-gradient)',
								'stroke-width': 3
							},
                            tips: {
								trackMouse: true,
								width: 150,
								height: 25,
								renderer: function(store_chart, item) {
									this.setTitle((store_chart.get('month') + '月库存' + (store_chart.get('finish')+'万元')));
								}
							},
							markerConfig: {
								type: 'circle',
								size: 4,
								radius: 4,
								'stroke-width': 0,
								fill: '#38B8BF',
								stroke: '#38B8BF'
							}
						}, {
							type: 'line',
							axis: 'left',
							xField: 'month',
							yField: 'plan',
							tips: {
								trackMouse: true,
								width: 150,
								height: 33,
								renderer: function(store_chart, item) {
									this.setTitle((store_chart.get('month') + '月计划库存' + (store_chart.get('plan')+'万元<br /> 比例：'+  (parseFloat((store_chart.get('finish'))/parseFloat((store_chart.get('plan')+0.0000001))).toFixed
                                        (2)*100 + '%'))));
								}
							},
							style: {
								fill: '#18428E',
								stroke: '#18428E',
								'stroke-width': 3
							},
							markerConfig: {
								type: 'circle',
								size: 4,
								radius: 4,
								'stroke-width': 0,
								fill: '#18428E',
								stroke: '#18428E'
							}
						}]
					}
				});
}
