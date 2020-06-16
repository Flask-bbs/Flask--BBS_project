/**
 * // 前台帖子详情页面样式js文件：static/front/js/front_pdetail.js
 */
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
            'beforeSend':function(xhr,settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        });
    }
};

// 初始化 百度文本编辑器
$(function(){
    var ue = UE.getEditor("editor", {
        "serverUrl": "/ueditor/upload",               // 图片上传路径
       toolbars: [                                    // 复制http://fex.baidu.com/ueditor/#start-toolbar中的多行列表代码
        ['fullscreen', 'source', 'undo', 'redo'],
        ['bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat',
         'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist',
         'insertunorderedlist', 'selectall', 'cleardoc'],
]
    });
    window.ue = ue;
})

$(function () {
    // 发表评论按钮
    $("#comment-btn").click(function (event) {
        event.preventDefault();

//        var content = $("#comment").val();                                  // 普通文本框的获取方法
        var content = window.ue.getContent();                                 // content使用了百度富文本编辑器之后，使用这种方法
        var post_id = $("#post-content").attr("data-id");                     // attr("data-id")是front_detail.html文件传输过来
        lgajax.post({
            'url': '/acomment/',
            'data':{
                'content': content,
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    window.location.reload();
                }else{
                    lgalert.alertInfo(data['message']);
                }
            }
        });
    });
});