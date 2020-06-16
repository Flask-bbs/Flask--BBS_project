// 帖子后台管理的静态资源文件：static/cms/js/posts.js
$(function () {
    //  帖子加精、取消加精按钮
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));           // 获取cms_posts.html页面的data-highlight属性进行判断路由选择
        var url = "";
        if(highlight){
            url = "/cms/uhpost/";                     // 取消加精
        }else{
            url = "/cms/hpost/";                     // 帖子加精路由
        }
        lgajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    lgalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    lgalert.alertInfo(data['message']);
                }
            }
        });
    });
});


$(function () {
    $(".btn-xs").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        lgalert.alertConfirm({
            "msg":"您确定要删除这篇帖子吗？",
            'confirmCallback': function () {
                lgajax.post({
                    'url': '/cms/dpost/',
                    'data':{
                        'post_id': post_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();           // 重新加载这个页面
                        }else{
                            lgalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});
