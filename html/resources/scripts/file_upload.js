Ext.onReady(function() {
    Ext.create('Ext.form.Panel', {
        renderTo: 'fi-form',
        width: 400,
        frame: true,
        title: '上传数据文件',
        bodyPadding: '10 10 0',

        defaults: {
            anchor: '100%',
            allowBlank: false,
            msgTarget: 'side',
            labelWidth: 50
        },

        items: [{
            xtype: 'filefield',
            id: 'form-file1',
            emptyText: '上传应收表...',
            fieldLabel: '应收表',
            name: 'checkin-path',
            buttonText: '选择',
            buttonConfig: {
                iconCls: 'upload-icon'
            }
        }],
        buttons: [{
            text: '上传应收表',
            handler: function() {
                var form = this.up('form').getForm();
                if(form.isValid()){
                    form.submit({
                        url: '/######',
                        waitMsg: '正在上传应收表...',
                        success: function(fp, o) {
                            msg('上传成功', '文件已经上传到了服务器。');
                        }, error: function(fp, o) {
                            msg('Failed!', 'fail to upload.');
                        }
                    });
                }
            }
        },{
            text: '清空',
            handler: function() {
                this.up('form').getForm().reset();
            }
        }]
    });

});