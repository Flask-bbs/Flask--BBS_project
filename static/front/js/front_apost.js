// 帖子提交页面关联的js样式：static/front/js/front_apost.js
$(function () {
    // 提交按钮绑定方法
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');                      // 收集Form表单填入的信息
        var boardSelect = $("select[name='board_id']");
        var contentText = $("textarea[name='content']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = contentText.val();

        lgajax.post({
            'url': '/apost/',                               // 上传路由
            'data': {                                       // 表单信息
                'title': title,
                'content':content,
                'board_id': board_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    lgalert.alertConfirm({
                        'msg': '恭喜！帖子发表成功！',                      // 弹出提示框
                        'cancelText': '回到首页',
                        'confirmText': '再发一篇',
                        'cancelCallback': function () {
                            window.location = '/';                          // 返回首页路由
                        },
                        'confirmCallback': function () {
                            titleInput.val("");                            // 再发一篇，将页面标题清空
                            contentText.val("");                           // 再发一篇，将页面内容清空
                        }
                    });
                }else{
                    lgalert.alertInfo(data['message']);
                }
            }
        });
    });
});
