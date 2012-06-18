
Ext.onReady(function() {
				//Ext.QuickTips.init();
				//Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));
                var combo_panel,contract_related_data_grid, contract_table_grid, related_data_specific_grid;

                var store_contract_related_data = Ext.create('Ext.data.Store', {
					model: 'related_data',
					proxy: {
						type: 'ajax',
						url : '/contract/related_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_contract_related_data.load({
                    params:{"name":"全部"},
					//scope   : this,
					callback: function(records, operation, success) {
						showRelatedData(store_contract_related_data);
					}
				});

				var store_contract_table = Ext.create('Ext.data.Store', {
					model: 'contract_table',
					proxy: {
						type: 'ajax',
						url : '/contract/table.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
				store_contract_table.load({
					//scope   : this,
					callback: function(records, operation, success) {
						showContract_table(store_contract_table);
					}
				});

                var stroe_contract_names = Ext.create('Ext.data.Store', {
					model: 'contract_table',
					proxy: {
						type: 'ajax',
						url : '/contract/names.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                stroe_contract_names.load({
					//scope   : this,
					callback: function(records, operation, success) {
//						showCombobox(stroe_contract_names);
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
                                store: stroe_contract_names,
                                typeAhead: true,
                                emptyText: '全部数据',
                                displayField: 'name'
                            }],
                            renderTo: 'contract_analysis_main_statistic_choice'
                        });
                        Ext.getCmp("combobox").on('select', function(comboBox) {
                            var name = comboBox.getValue();
                            store_contract_related_data.load({
                                params:{"name":name},
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    contract_related_data_grid.update();
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
					model: 'contract_chart_model',
					proxy: {
						type: 'ajax',
						url : '/contract/chart_data.json',
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



		});

function showRelatedData(store_contract_related_data) {
    contract_related_data_grid = Ext.create('Ext.grid.Panel', {
					store: store_contract_related_data,
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

function showContract_table(store_contract_table) {
	contract_table_grid = Ext.create('Ext.grid.Panel', {
					store: store_contract_table,
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
							text     : '合同额',
							sortable : true,
							dataIndex: 'contract_money'
						}
					],
					height: 280,
					width: 260,
					title: '合同分析表',
					renderTo: 'contract_analysis_main_left',
					viewConfig: {
						stripeRows: true
					}
    });
}

function showCombobox(stroe_contract_names) {
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
            store: stroe_contract_names,
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
//        store: stroe_contract_names,
//        queryMode: 'local',
//        typeAhead: true,
//        emptyText: '全部',
//        fieldLabel: '姓名',
//        labelWidth: 30
//    });
}

function showInventoryChart(store_chart) {
    inventory_chart = new Ext.Panel({
					width: 665,
					height: 460,
					title: '合同图',
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
							maximum: 21000,
							position: 'left',
							fields: ['finish'],
							title: '合同额(万元)',
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
									this.setTitle((store_chart.get('month') + '月合同完成' + (store_chart.get('finish')+'万元')));
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
								width: 170,
								height: 33,
								renderer: function(store_chart, item) {
									this.setTitle(('全年计划合同额' + (store_chart.get('plan')+'万元<br /> 完成比例：'+  (parseFloat((store_chart.get('finish'))/parseFloat((store_chart.get('plan')+0.0000001))).toFixed
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
