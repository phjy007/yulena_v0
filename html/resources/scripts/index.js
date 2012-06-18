Ext.onReady(function() {
     var index_total_data_grid, index_checkin_grid, index_inventory_grid, index_order_grid;

     var store_index_total_data = Ext.create('Ext.data.Store', {
					model: 'index_total_data',
					proxy: {
						type: 'ajax',
						url : '/index/total_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
     store_index_total_data.load({
					//scope   : this,
					callback: function(records, operation, success) {
						showIndexTotalData(store_index_total_data);
					}
	 });

     var store_index_checkin = Ext.create('Ext.data.Store', {
					model: 'index_checkin',
					proxy: {
						type: 'ajax',
						url : '/index/total_checkin_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
     store_index_checkin.load({
					//scope   : this,
					callback: function(records, operation, success) {
						showIndexCheckin(store_index_checkin);
					}
	 });

    var store_index_order = Ext.create('Ext.data.Store', {
					model: 'index_checkin',
					proxy: {
						type: 'ajax',
						url : '/index/total_order_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
     store_index_order.load({
					//scope   : this,
					callback: function(records, operation, success) {
						showIndexOrder(store_index_order);
					}
	 });

    var store_index_inventory = Ext.create('Ext.data.Store', {
					model: 'index_checkin',
					proxy: {
						type: 'ajax',
						url : '/index/total_inventory_data.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
     store_index_inventory.load({
					//scope   : this,
					callback: function(records, operation, success) {
						showIndexInventory(store_index_inventory);
					}
	 });

    var store_checkin_chart = Ext.create('Ext.data.JsonStore', {
					model: 'index_chart_model',
					proxy: {
						type: 'ajax',
						url : '/index/total_checkin_chart.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_checkin_chart.load({
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    showCheckinChart(store_checkin_chart);
                                }
                });

    var store_inventory_chart = Ext.create('Ext.data.JsonStore', {
					model: 'index_chart_model',
					proxy: {
						type: 'ajax',
						url : '/index/total_inventory_chart.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_inventory_chart.load({
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    showInventoryChart(store_inventory_chart);
                                }
                });

    var store_order_chart = Ext.create('Ext.data.JsonStore', {
					model: 'index_chart_model',
					proxy: {
						type: 'ajax',
						url : '/index/total_order_chart.json',
						reader: {
							type: 'json',
							totalProperty  : 'total',
							successProperty: 'success'
						}
					}
				});
                store_order_chart.load({
                                //scope   : this,
                                callback: function(records, operation, success) {
                                    showOrderChart(store_order_chart);
                                }
                });
    
});

function showIndexTotalData(store_index_total_data) {
    index_total_data_grid = Ext.create('Ext.grid.Panel', {
					store: store_index_total_data,
					columns: [
						{text: "本月收款计划总额", width: 145, dataIndex: 'total_momey_this_month', sortable: false},
						{text: "本月开票计划总额", width: 145, dataIndex: 'plan_check_this_month', sortable: false},
                        {text: "上月计划库存完成比例", width: 145, dataIndex: 'finish_inventory_percentage_last_month', sortable: false},
                        {text: "上月计划应收完成比例", width: 145, dataIndex: 'finish_checkin_percentage_last_month', sortable: false},
						{text: "本月预计运行指标", width: 143, dataIndex: 'plan_running', sortable: false},
                        {text: "目前运行指标", width: 120, dataIndex: 'current_running', sortable: false},
                        {text: "年度运行指标", width: 110, dataIndex: 'year_running', sortable: false}
					],
//                    title: '综合数据',
					renderTo:'index_total_data',
					width: 960,
					height: 60,
                    viewConfig: {
						stripeRows: true
					}
	});
}

function showIndexCheckin(store_index_checkin) {
    index_checkin_grid = Ext.create('Ext.grid.Panel', {
					store: store_index_checkin,
					columns: [
						{text: "项目", width: 160, dataIndex: 'related_data_title', sortable: false},
						{text: "数据", width: 88, dataIndex: 'related_data_data', sortable: false}
					],
                    title: '应收数据',
					renderTo:'index_checkin_table',
					width: 250,
					height: 285,
                    viewConfig: {
						stripeRows: true
					}
	});
}

function showIndexInventory(store_index_inventory) {
    index_inventory_grid = Ext.create('Ext.grid.Panel', {
					store: store_index_inventory,
					columns: [
						{text: "项目", width: 160, dataIndex: 'related_data_title', sortable: false},
						{text: "数据", width: 88, dataIndex: 'related_data_data', sortable: false}
					],
                    title: '库存数据',
					renderTo:'index_inventory_table',
					width: 250,
					height: 285,
                    viewConfig: {
						stripeRows: true
					}
	});
}

function showIndexOrder(store_index_order) {
    index_order_grid = Ext.create('Ext.grid.Panel', {
					store: store_index_order,
					columns: [
						{text: "项目", width: 160, dataIndex: 'related_data_title', sortable: false},
						{text: "数据", width: 88, dataIndex: 'related_data_data', sortable: false}
					],
                    title: '订单数据',
					renderTo:'index_order_table',
					width: 250,
					height: 285,
                    viewConfig: {
						stripeRows: true
					}
	});
}

function showCheckinChart(store_chart) {
    checkin_chart = new Ext.Panel({
					width: 665,
					height: 285,
					title: '按月应收图',
					renderTo: 'chart1',
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
							maximum: 3500,
							position: 'left',
							fields: ['finish'],
//							title: '应收额(万元)',
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
									this.setTitle((store_chart.get('month') + '月应收完成' + (store_chart.get('finish')+'万元')));
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
								height: 33
//								renderer: function(store_chart, item) {
//									this.setTitle((store_chart.get('month') + '月计划应收' + (store_chart.get('plan')+'万元<br /> 完成比例：'+  (parseFloat((store_chart.get('finish'))/parseFloat((store_chart.get('plan')+0.0000001))).toFixed
//                                        (2)*100 + '%'))));
//								}
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

function showInventoryChart(store_chart) {
   inventory_chart = new Ext.Panel({
					width: 665,
					height: 285,
					title: '按月库存图',
					renderTo: 'chart2',
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
							maximum: 6500,
							position: 'left',
							fields: '库存额(万元)',
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
									this.setTitle((store_chart.get('month') + '月库存完成' + (store_chart.get('finish')+'万元')));
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
								height: 33
//								renderer: function(store_chart, item) {
//									this.setTitle((store_chart.get('month') + '月计划库存' + (store_chart.get('plan')+'万元<br /> 完成比例：'+  (parseFloat((store_chart.get('finish'))/parseFloat((store_chart.get('plan')+0.0000001))).toFixed
//                                        (2)*100 + '%'))));
//								}
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

function showOrderChart(store_chart) {
    order_chart = new Ext.Panel({
					width: 665,
					height: 285,
					title: '按月订单图',
					renderTo: 'chart3',
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
							maximum: 9000,
							position: 'left',
							fields: ['finish'],
//							title: '应收额(万元)',
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
									this.setTitle((store_chart.get('month') + '月订单完成' + (store_chart.get('finish')+'万元')));
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
								height: 33
//								renderer: function(store_chart, item) {
//									this.setTitle((store_chart.get('month') + '月计划应收' + (store_chart.get('plan')+'万元<br /> 完成比例：'+  (parseFloat((store_chart.get('finish'))/parseFloat((store_chart.get('plan')+0.0000001))).toFixed
//                                        (2)*100 + '%'))));
//								}
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