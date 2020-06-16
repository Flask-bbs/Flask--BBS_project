// 轮播图的后台管理的静态资源文件：static/cms/js/banners.js


$(function () {
    // 保存轮播图按钮
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameInput = $("input[name='name']");                           // 获得表单输入的信息
        var imageInput = $("input[name='image_url']");
        var linkInput = $("input[name='link_url']");
        var priorityInput = $("input[name='priority']");


        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var submitType = self.attr('data-type');                           // 获取data-type的属性用于判断
        var bannerId = self.attr("data-id");

        if(!name || !image_url || !link_url || !priority){
            lgalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }

        var url = '';
        if(submitType == 'update'){                                         // 如果data-type的属性是update
            url = '/cms/ubanner/';               //  修改轮播图选项update   跳转到修改轮播图路由
        }else{
            url = '/cms/abanner/';               //  添加轮播图选项 add     跳转到添加轮播图路由
        }
        // form 发送 <form action="提交的地址" method="post">
        lgajax.post({                       // 方法是post，在视图文件:apps/cms/views.py文件中添加轮播图路由方法需要为POST
            "url": url,
            'data':{                             // Form表单名称
                'name':name,
                'image_url': image_url,
                'link_url': link_url,
                'priority':priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                dialog.modal("hide");                            // 添加轮播图Form表单界面隐藏
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();                   // 发送成功，页面刷新
                }else{
                    lgalert.alertInfo(data['message']);         // 弹出异常信息
                }
            },
            'fail': function () {
                lgalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    // 编辑轮播图按钮
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type",'update');                  // data-type属性update代表的是对轮播图的修改更新，而不是添加保存
        saveBtn.attr('data-id',tr.attr('data-id'));
    });
});

$(function () {
    // 删除轮播图选项按钮
    $(".delete-banner-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        lgalert.alertConfirm({
            "msg":"您确定要删除这个轮播图吗？",
            'confirmCallback': function () {
                lgajax.post({
                    'url': '/cms/dbanner/',
                    'data':{
                        'banner_id': banner_id
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

// 七牛云上传需要修改的部分内容
$(function () {
    lgqiniu.setUp({

        'domain': 'http://qbautq371.bkt.clouddn.com/',                      // 修改成自己账户的免费七牛云外链域名
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',                                       // 七牛云上传文件路由名称/uptoken/，与公共视图文件：apps/common/views.py中命名相同
        'success': function (up,file,info) {
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);
        }
    });
});