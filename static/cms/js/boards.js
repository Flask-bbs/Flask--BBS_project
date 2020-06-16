// 板块后台管理的静态资源文件：static/cms/js/boards.js
$(function () {
    // 添加按钮
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        lgalert.alertOneInput({
            'text':'请输入板块名称！',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                lgajax.post({
                    'url': '/cms/aboard/',                         // 路由名称与视图文件:apps/cms/views.py文件中定义要一样
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            lgalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    // 编辑按钮
    $(".edit-board-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');                                   // 查询添加板块名称的属性，用于编辑板块名称的时候渲染到placeholder
        var board_id = tr.attr("data-id");

        lgalert.alertOneInput({
            'text': '请输入新的板块名称！',
            'placeholder': name,                                          // 编辑修改的时候，显示最早输入时候的名称
            'confirmCallback': function (inputValue) {
                lgajax.post({
                    'url': '/cms/uboard/',                               // 路由名称与视图文件:apps/cms/views.py文件中定义要一样
                    'data': {
                        'board_id': board_id,                           // 'board_id'是表单信息中输入的name，value值为board_id
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            lgalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});


$(function () {
    // 删除按钮
    $(".delete-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');
        lgalert.alertConfirm({
            "msg":"您确定要删除这个板块吗？",
            'confirmCallback': function () {
                lgajax.post({
                    'url': '/cms/dboard/',                                // 路由名称与视图文件:apps/cms/views.py文件中定义要一样
                    'data':{
                        // form  input name value
                        'board_id': board_id                             // 'board_id'是表单信息中输入的name，value值为board_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            lgalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});