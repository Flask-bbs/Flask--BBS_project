/**
 * // 后台重置密码的静态资源文件：static/cms/js/resetpwd.js
 */
$(function () {
    // #绑定submit按钮
    $("#submit").click(function (event) {
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        event.preventDefault();

        // 获取input表单中的值
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        var lgajax = {
            'get':function(args) {
                args['method'] = 'get';
                this.ajax(args);
            },
            'post':function(args) {
                args['method'] = 'post';
                this.ajax(args);
            },
            'ajax':function(args) {
                // 设置csrftoken
                this._ajaxSetup();
                $.ajax(args);
            },
            '_ajaxSetup': function() {
                $.ajaxSetup({
                    // beforeSend在发送请求之前，先执行function方法
                    'beforeSend':function(xhr,settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

                            // 请求之前发送csrf信息   将csrf信息name=csrf-token和content传递给cms_base.html头文件
                            var csrftoken = $('meta[name=csrf-token]').attr('content');
                            // var csrftoken = $('input[name=csrf-token]').attr('value');
                            xhr.setRequestHeader("X-CSRFToken", csrftoken)
                        }
                    }
                });
            }
        };

        // 表单提交方法：post提交
        lgajax.post({
            'url': '/cms/resetpwd/',      // 表单发送地址必须要和views.py中绑定的url地址相同
            'data': {                     // 表单发送数据
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {     // 表单提交成功
                // console.log(data);

            //  信息返回给弹窗进行显示在html页面
                if(data['code'] == 200){
                    lgalert.alertSuccess("密码修改成功")

                    // 修改密码的输入框清空
                    oldpwd.val("")
                    newpwd.val("")
                    newpwd2.val("")

                }else{
                    var message = data['message']    // 修改不成功
                    lgalert.alertInfo(message)       // 弹出错误信息

                    // 清空输入框
                    oldpwd.val("")
                    newpwd.val("")
                    newpwd2.val("")

                }
            },
            'fail': function (error) {               // 表单提交失败
                // console.log(error);
                lgalert.alertNetworkError()          // 弹出网络错误

                // 清空输入框
                oldpwd.val("")
                newpwd.val("")
                newpwd2.val("")
            }
        });
    });
});
