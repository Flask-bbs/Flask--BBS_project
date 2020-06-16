/**
 * // 前台注册模板文件的js样式文件：static/front/js/front_signup.js
 */


var param = {
    setParam: function (href,key,value) {
        // 重新加载整个页面
        var isReplaced = false;
        var urlArray = href.split('?');               // 通过？分割url

        // 判定图形验证码的url长度，需要控制长度
        if(urlArray.length > 1){
            var queryArray = urlArray[1].split('&');
            for(var i=0; i < queryArray.length; i++){
                var paramsArray = queryArray[i].split('=');
                if(paramsArray[0] == key){
                    paramsArray[1] = value;
                    queryArray[i] = paramsArray.join('=');
                    isReplaced = true;
                    break;
                }
            }

            if(!isReplaced){
                var params = {};
                params[key] = value;
                if(urlArray.length > 1){
                    href = href + '&' + $.param(params);
                }else{
                    href = href + '?' + $.param(params);
                }
            }else{
                var params = queryArray.join('&');
                urlArray[1] = params;
                href = urlArray.join('?');
            }
        }else{
            var param = {};
            param[key] = value;
            if(urlArray.length > 1){
                href = href + '&' + $.param(param);
            }else{
                href = href + '?' + $.param(param);
            }
        }
        return href;
    }
};


$(function(){
    // #captcha-img绑定这个id,在front_signup.html文件中绑定图形验证码的id
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        // 每次 click之后，srcd地址改变，图形验证码就会刷新
        var newsrc = param.setParam(src,'xx',Math.random());
        self.attr('src',newsrc);
    });
});


// $(function () {
// var __encode ='sojson.com',_a={}, _0xb483=["\x5F\x64\x65\x63\x6F\x64\x65","\x68\x74\x74\x70\x3A\x2F\x2F\x77\x77\x77\x2E\x73\x6F\x6A\x73\x6F\x6E\x2E\x63\x6F\x6D\x2F\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x6F\x62\x66\x75\x73\x63\x61\x74\x6F\x72\x2E\x68\x74\x6D\x6C"];(function(_0xd642x1){_0xd642x1[_0xb483[0]]= _0xb483[1]})(_a);var __Ox82dc8=["\x70\x72\x65\x76\x65\x6E\x74\x44\x65\x66\x61\x75\x6C\x74","\x76\x61\x6C","\x69\x6E\x70\x75\x74\x5B\x6E\x61\x6D\x65\x3D\x27\x74\x65\x6C\x65\x70\x68\x6F\x6E\x65\x27\x5D","\x74\x65\x73\x74","\u8BF7\u8F93\u5165\u6B63\u786E\u7684\u624B\u673A\u53F7\u7801\uFF01","\x61\x6C\x65\x72\x74\x49\x6E\x66\x6F","\x67\x65\x74\x54\x69\x6D\x65","\x71\x33\x34\x32\x33\x38\x30\x35\x67\x64\x66\x6C\x76\x62\x64\x66\x76\x68\x73\x64\x6F\x61\x60\x23\x24\x25","\x2F\x63\x2F\x73\x6D\x73\x5F\x63\x61\x70\x74\x63\x68\x61\x2F","\x63\x6F\x64\x65","\u77ED\u4FE1\u9A8C\u8BC1\u7801\u53D1\u9001\u6210\u529F\uFF01","\x61\x6C\x65\x72\x74\x53\x75\x63\x63\x65\x73\x73\x54\x6F\x61\x73\x74","\x64\x69\x73\x61\x62\x6C\x65\x64","\x61\x74\x74\x72","\x74\x65\x78\x74","\x72\x65\x6D\x6F\x76\x65\x41\x74\x74\x72","\u53D1\u9001\u9A8C\u8BC1\u7801","\x6D\x65\x73\x73\x61\x67\x65","\x61\x6C\x65\x72\x74\x49\x6E\x66\x6F\x54\x6F\x61\x73\x74","\x70\x6F\x73\x74","\x63\x6C\x69\x63\x6B","\x23\x73\x6D\x73\x2D\x63\x61\x70\x74\x63\x68\x61\x2D\x62\x74\x6E","\x75\x6E\x64\x65\x66\x69\x6E\x65\x64","\x6C\x6F\x67","\u5220\u9664","\u7248\u672C\u53F7\uFF0C\x6A\x73\u4F1A\u5B9A\u671F\u5F39\u7A97\uFF0C","\u8FD8\u8BF7\u652F\u6301\u6211\u4EEC\u7684\u5DE5\u4F5C","\x73\x6F\x6A\x73","\x6F\x6E\x2E\x63\x6F\x6D"];$(function(){$(__Ox82dc8[0x15])[__Ox82dc8[0x14]](function(_0x6781x1){_0x6781x1[__Ox82dc8[0x0]]();var _0x6781x2=$(this);var _0x6781x3=$(__Ox82dc8[0x2])[__Ox82dc8[0x1]]();if(!(/^1[345879]\d{9}$/[__Ox82dc8[0x3]](_0x6781x3))){lgalert[__Ox82dc8[0x5]](__Ox82dc8[0x4]);return};var _0x6781x4=( new Date)[__Ox82dc8[0x6]]();var _0x6781x5=md5(_0x6781x4+ _0x6781x3+ __Ox82dc8[0x7]);lgajax[__Ox82dc8[0x13]]({'\x75\x72\x6C':__Ox82dc8[0x8],'\x64\x61\x74\x61':{'\x74\x65\x6C\x65\x70\x68\x6F\x6E\x65':_0x6781x3,'\x74\x69\x6D\x65\x73\x74\x61\x6D\x70':_0x6781x4,'\x73\x69\x67\x6E':_0x6781x5},'\x73\x75\x63\x63\x65\x73\x73':function(_0x6781x6){if(_0x6781x6[__Ox82dc8[0x9]]== 200){lgalert[__Ox82dc8[0xb]](__Ox82dc8[0xa]);_0x6781x2[__Ox82dc8[0xd]](__Ox82dc8[0xc],__Ox82dc8[0xc]);var _0x6781x7=60;var _0x6781x8=setInterval(function(){_0x6781x7--;_0x6781x2[__Ox82dc8[0xe]](_0x6781x7);if(_0x6781x7<= 0){_0x6781x2[__Ox82dc8[0xf]](__Ox82dc8[0xc]);clearInterval(_0x6781x8);_0x6781x2[__Ox82dc8[0xe]](__Ox82dc8[0x10])}},1000)}else {lgalert[__Ox82dc8[0x12]](_0x6781x6[__Ox82dc8[0x11]])}}})})});;;(function(_0x6781x9,_0x6781xa,_0x6781xb,_0x6781xc,_0x6781xd,_0x6781xe){_0x6781xe= __Ox82dc8[0x16];_0x6781xc= function(_0x6781xf){if( typeof alert!== _0x6781xe){alert(_0x6781xf)};if( typeof console!== _0x6781xe){console[__Ox82dc8[0x17]](_0x6781xf)}};_0x6781xb= function(_0x6781x10,_0x6781x9){return _0x6781x10+ _0x6781x9};_0x6781xd= _0x6781xb(__Ox82dc8[0x18],_0x6781xb(__Ox82dc8[0x19],__Ox82dc8[0x1a]));try{_0x6781x9= __encode;if(!( typeof _0x6781x9!== _0x6781xe&& _0x6781x9=== _0x6781xb(__Ox82dc8[0x1b],__Ox82dc8[0x1c]))){_0x6781xc(_0x6781xd)}}catch(e){_0x6781xc(_0x6781xd)}})({})
// })

// js加密方法，使得md5加密方式不被破解
$(function () {
    /*
 * 加密工具已经升级了一个版本，目前为 sojson.v5 ，主要加强了算法，以及防破解【绝对不可逆】配置，耶稣也无法100%还原，我说的。;
 * 已经打算把这个工具基础功能一直免费下去。还希望支持我。
 * 另外 sojson.v5 已经强制加入校验，注释可以去掉，但是 sojson.v5 不能去掉（如果你开通了VIP，可以手动去掉），其他都没有任何绑定。
 * 誓死不会加入任何后门，sojson JS 加密的使命就是为了保护你们的Javascript 。
 * 警告：如果您恶意去掉 sojson.v5 那么我们将不会保护您的JavaScript代码。请遵守规则
 * 新版本: https://www.jsjiami.com/ 支持批量加密，支持大文件加密，拥有更多加密。 */
;var encode_version = 'sojson.v5', cvwjl = '__0x83a8c',  __0x83a8c=['w4HDvGjDgcKf','w4rDvE7CjMOJ','c8OeTGo1','KMKEwr48V8OyBmXChBRnNHB9AcOpw4k7w51fQcOYw6c3RyE=','VsKsw5lM','w5hVTSDDknYDw4Jyw6HDjFvDoiDCjA==','D8OZw5s=','556z5L6i6aiv6KyE56Ct5Yy/6YGJ5oqC5Ymu77yX','wrEQwrk=','MybDkMK2TcKJLQ==','wr9Hw50=','5Y+j6YCt6aqz6K6G56Co','wqXCp8Kcw7HCsg==','w7AUwrQ6wpk=','BXwkw6QU','wqpuw5xlSMOpc38JwrvDjMO/wrEyw7LChB8=','R8K8wp1ZwqM=','FXsBXw==','L8Ouw7xsKQ==','w4J+w4fDuDI=','HwvDq8KDSw==','w79WwozCt8K7I8KXVA==','5Y2/6YKK6aqr6K2Z56Op','wqAqHMK8w5HDlsKNdSEe','dxQjGMK6','S8OyZ2QP','ccKgw5JMfQ==','w6HDpmPCvg==','wqjDvsKyw5nDiA==','TsK5wr51IQ==','e8KAwoZEwo4=','E8OuwoYvc8KAQ8KvLcKvw5HDkcKWwpfCgxjDpw==','55+45L6i6aul6K6M56Oy5Y+V6YOR5oqW5Yq277yS','w6Yfw5zCuQ==','NsK8w7TCv3Q=','woNYw7Q=','w53DpE3Dq8KHQgLDrcOu','54iI5p+J5Y2177+RUyjkvZnlr73mnZ7lvIjnq4/vvYPovYDorqbml4Lmjr/mirHkuqfnmq/lt4LkvYo=','5YuX6ZmS54iq5p2/5Y2I77yJNsOS5LyJ5ayL5p6n5byB56id','OsOYwq4=','w7ggwo4=','cMKTw49Wdg==','wqXDhsKhw6bDtlnDomUs','wrfCpRAcwpg=','FWrCsR/DsQ==','w5tRMxsW','w6rDiE3CkcOH','w4PDpGLClcKO','wqLDjcKow6zDplXDjXQ8Fg==','wpNfETLDnWk5w4U=','w7saw6Jk','woVSw65qwpXDgTzDnxnDpcKEZnIX','wofDrXnCr8O2','ScK6wrhjwoE=','VSXCpcKbAsK6TMOoCMOvw7IWwrPDgQ==','wqfDsFjCqMOyw6zCqQ==','wr4swolzdA==','w7VmMAgn','w4vDrsKrEQ==','LSzDicK2Q8KAZsOkw4Q=','OcK2w7s=','w5LDnXXCq8Og','wqJjw7Vbbg==','N8KOw67Cs1Q=','Bk7Ctw==','TMKNHcOSw4o=','wrhnw41kdw==','w7QzwrYSwrI=','54mV5p+S5Y6v772mwrtW5L6M5a2H5p2s5by856mj77226L2N6K+D5peh5o+H5ouY5Lma55uL5ba15Lyv','Gg7Cn8OyFA==','AMOsZsOoSw==','GWkwY0g=','N8Ohwqk=','5YiU6Zit54qI5p+F5Y6B77+/SMO95L295ayh5p6C5b2O56mX','wrPDkcK2','w5pZHg==','XsOWcWcU','Y8KWw6/CrhQ4Ihc1UjAuwrUzwpnDkA==','w57DuULDrsKNQljDn8K+PnrCncKSwoU=','wr7ClMKFw4HChw==','KynDrMKdTg==','d8KWwqdB','RcKHw5t7Qg==','w6YHw43CucKLwrTCpsOJw5Q=','w7pTwprCpMKtBsKcVsK7','wrJwEcOZEA=='];(function(_0xa5baab,_0x2083da){var _0x57b54e=function(_0x4b9e87){while(--_0x4b9e87){_0xa5baab['push'](_0xa5baab['shift']());}};_0x57b54e(++_0x2083da);}(__0x83a8c,0x14c));var _0x4138=function(_0x359e5e,_0x1af3ae){_0x359e5e=_0x359e5e-0x0;var _0x35b06e=__0x83a8c[_0x359e5e];if(_0x4138['initialized']===undefined){(function(){var _0x1f0dbf=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x400dac='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0x1f0dbf['atob']||(_0x1f0dbf['atob']=function(_0x3c1e44){var _0x1decac=String(_0x3c1e44)['replace'](/=+$/,'');for(var _0x5d77b9=0x0,_0x46671c,_0x259e7f,_0xc758e8=0x0,_0x12847a='';_0x259e7f=_0x1decac['charAt'](_0xc758e8++);~_0x259e7f&&(_0x46671c=_0x5d77b9%0x4?_0x46671c*0x40+_0x259e7f:_0x259e7f,_0x5d77b9++%0x4)?_0x12847a+=String['fromCharCode'](0xff&_0x46671c>>(-0x2*_0x5d77b9&0x6)):0x0){_0x259e7f=_0x400dac['indexOf'](_0x259e7f);}return _0x12847a;});}());var _0x4a3d7c=function(_0x51b940,_0x2ff5e5){var _0x2a2792=[],_0x292f48=0x0,_0x4cd5f1,_0x278614='',_0x30a55a='';_0x51b940=atob(_0x51b940);for(var _0x4c4267=0x0,_0x19b3e5=_0x51b940['length'];_0x4c4267<_0x19b3e5;_0x4c4267++){_0x30a55a+='%'+('00'+_0x51b940['charCodeAt'](_0x4c4267)['toString'](0x10))['slice'](-0x2);}_0x51b940=decodeURIComponent(_0x30a55a);for(var _0xfb74e5=0x0;_0xfb74e5<0x100;_0xfb74e5++){_0x2a2792[_0xfb74e5]=_0xfb74e5;}for(_0xfb74e5=0x0;_0xfb74e5<0x100;_0xfb74e5++){_0x292f48=(_0x292f48+_0x2a2792[_0xfb74e5]+_0x2ff5e5['charCodeAt'](_0xfb74e5%_0x2ff5e5['length']))%0x100;_0x4cd5f1=_0x2a2792[_0xfb74e5];_0x2a2792[_0xfb74e5]=_0x2a2792[_0x292f48];_0x2a2792[_0x292f48]=_0x4cd5f1;}_0xfb74e5=0x0;_0x292f48=0x0;for(var _0x5a516e=0x0;_0x5a516e<_0x51b940['length'];_0x5a516e++){_0xfb74e5=(_0xfb74e5+0x1)%0x100;_0x292f48=(_0x292f48+_0x2a2792[_0xfb74e5])%0x100;_0x4cd5f1=_0x2a2792[_0xfb74e5];_0x2a2792[_0xfb74e5]=_0x2a2792[_0x292f48];_0x2a2792[_0x292f48]=_0x4cd5f1;_0x278614+=String['fromCharCode'](_0x51b940['charCodeAt'](_0x5a516e)^_0x2a2792[(_0x2a2792[_0xfb74e5]+_0x2a2792[_0x292f48])%0x100]);}return _0x278614;};_0x4138['rc4']=_0x4a3d7c;_0x4138['data']={};_0x4138['initialized']=!![];}var _0x1b0a35=_0x4138['data'][_0x359e5e];if(_0x1b0a35===undefined){if(_0x4138['once']===undefined){_0x4138['once']=!![];}_0x35b06e=_0x4138['rc4'](_0x35b06e,_0x1af3ae);_0x4138['data'][_0x359e5e]=_0x35b06e;}else{_0x35b06e=_0x1b0a35;}return _0x35b06e;};$(function(){var _0x3a0d9e={'owOYw':function _0xa9c050(_0xf36934,_0x15b631){return _0xf36934(_0x15b631);},'ujOXb':'input[name=\x27telephone\x27]','cDqCL':function _0x50817b(_0x3a564a,_0x14916b){return _0x3a564a===_0x14916b;},'hFZAQ':_0x4138('0x0',']6Ij'),'KAxJn':_0x4138('0x1','MRkN'),'QmSDD':'请输入正确的手机号码！','bXtsc':function _0x5d709c(_0x58608e,_0x25abfb){return _0x58608e+_0x25abfb;},'TcdYB':function _0x40e7a7(_0x1aed76,_0x5418db){return _0x1aed76+_0x5418db;},'ykYTc':function _0x1ed517(_0x2450fc,_0x1870c3){return _0x2450fc(_0x1870c3);}};_0x3a0d9e[_0x4138('0x2','j3SC')]($,_0x4138('0x3','58nk'))['click'](function(_0x4665e2){_0x4665e2[_0x4138('0x4','s^Y7')]();var _0x5d8ebc=_0x3a0d9e[_0x4138('0x5','zSKb')]($,this);var _0x46508f=_0x3a0d9e['owOYw']($,_0x3a0d9e[_0x4138('0x6','lrpU')])['val']();if(!/^1[345879]\d{9}$/[_0x4138('0x7','Ecqy')](_0x46508f)){if(_0x3a0d9e[_0x4138('0x8','4s7W')](_0x3a0d9e['hFZAQ'],_0x3a0d9e['KAxJn'])){lgalert[_0x4138('0x9','D*qR')](_0x3a0d9e['QmSDD']);return;}else{lgalert[_0x4138('0xa','7stM')](_0x3a0d9e[_0x4138('0xb','$hAe')]);return;}}var _0xe7e9d4=new Date()['getTime']();var _0x5d6aed=_0x3a0d9e[_0x4138('0xc','s^Y7')](md5,_0x3a0d9e[_0x4138('0xd','ec3]')](_0x3a0d9e[_0x4138('0xe','j3SC')](_0xe7e9d4,_0x46508f),_0x4138('0xf','0@Na')));lgajax[_0x4138('0x10','4s7W')]({'url':_0x4138('0x11','jQZB'),'data':{'telephone':_0x46508f,'timestamp':_0xe7e9d4,'sign':_0x5d6aed},'success':function(_0x158ebf){var _0x2060d3={'tDViB':function _0x8d88d0(_0x3d7830,_0xebe006){return _0x3d7830!==_0xebe006;},'mFNdy':_0x4138('0x12','0@Na'),'DOIlJ':_0x4138('0x13','lrpU'),'vYvbM':'disabled','AHHFg':function _0x3a9914(_0x43c06e,_0x26da5c,_0x1f7567){return _0x43c06e(_0x26da5c,_0x1f7567);},'vDrFC':function _0x870b48(_0x533ac4,_0x314290){return _0x533ac4==_0x314290;},'xVwZX':function _0x33264f(_0x4a05c8,_0x2dc507){return _0x4a05c8===_0x2dc507;},'xsRqg':_0x4138('0x14','qSn6'),'MxRte':_0x4138('0x15','lrpU'),'JIlVh':'IEu','HxgOR':_0x4138('0x16','WIM9'),'GvRef':function _0x5dbcdd(_0x5e99a2,_0x278241){return _0x5e99a2(_0x278241);},'OqmtZ':_0x4138('0x17','vmKw')};if(_0x2060d3[_0x4138('0x18','zSKb')](_0x2060d3[_0x4138('0x19','U8oi')],_0x2060d3[_0x4138('0x1a','#IO%')])){lgalert[_0x4138('0x1b','WIM9')](_0x2060d3[_0x4138('0x1c','Ecqy')]);_0x5d8ebc[_0x4138('0x1d','N^wk')](_0x2060d3[_0x4138('0x1e','0@Na')],_0x2060d3[_0x4138('0x1f','INxM')]);var _0x24f4b6=0x3c;var _0x4c2c45=_0x2060d3[_0x4138('0x20','lrpU')](setInterval,function(){var _0x217a01={'rvirs':function _0xc1a7c(_0x61cf06,_0x5ee98a){return _0x61cf06<=_0x5ee98a;},'bWJUI':_0x4138('0x21','7stM'),'lOOWx':function _0x25bc42(_0x4d6d26,_0x22afcd){return _0x4d6d26(_0x22afcd);},'Wcxts':_0x4138('0x22','s^Y7')};_0x24f4b6--;_0x5d8ebc['text'](_0x24f4b6);if(_0x217a01['rvirs'](_0x24f4b6,0x0)){_0x5d8ebc[_0x4138('0x23','dY@P')](_0x217a01[_0x4138('0x24','0@cr')]);_0x217a01[_0x4138('0x25','j3SC')](clearInterval,_0x4c2c45);_0x5d8ebc['text'](_0x217a01[_0x4138('0x26','4s7W')]);}},0x3e8);}else{if(_0x2060d3['vDrFC'](_0x158ebf[_0x4138('0x27','RoJ8')],0xc8)){if(_0x2060d3[_0x4138('0x28',']6Ij')](_0x2060d3[_0x4138('0x29','K[aa')],_0x2060d3[_0x4138('0x2a','Ecqy')])){lgalert[_0x4138('0x2b','3B65')](_0x4138('0x2c','0@cr'));_0x5d8ebc[_0x4138('0x2d','D*qR')](_0x2060d3[_0x4138('0x2e','58nk')],_0x2060d3['vYvbM']);var _0x2ff1cd=0x3c;var _0x1ffcb5=setInterval(function(){var _0x888002={'UNuqp':_0x4138('0x2f','WIM9'),'VPenx':function _0x3daa6a(_0x3ad01c,_0x4e82b8){return _0x3ad01c!==_0x4e82b8;},'hmpPl':function _0x1c02af(_0xe8b8f9,_0x252fb1){return _0xe8b8f9===_0x252fb1;},'WrfOU':_0x4138('0x30','s^Y7'),'vVrSr':function _0x3b6c3e(_0x43d9a6,_0x2700ad){return _0x43d9a6+_0x2700ad;},'iAQvW':_0x4138('0x31','58nk'),'Blwnm':_0x4138('0x32','jQZB'),'AmeNQ':function _0x5198b1(_0x17db86,_0x219b4b){return _0x17db86<=_0x219b4b;},'kyGhL':'发送验证码'};if(_0x888002['UNuqp']!==_0x4138('0x33','3B65')){c='al';try{c+=_0x4138('0x34','U8oi');b=encode_version;if(!(_0x888002[_0x4138('0x35','4s7W')](typeof b,_0x4138('0x36',']6Ij'))&&_0x888002['hmpPl'](b,_0x888002[_0x4138('0x37','QSUl')]))){w[c](_0x888002[_0x4138('0x38','KFJ(')]('删除',_0x888002[_0x4138('0x39','YqVY')]));}}catch(_0x53bf5d){w[c](_0x888002[_0x4138('0x3a','ec3]')]);}}else{_0x2ff1cd--;_0x5d8ebc['text'](_0x2ff1cd);if(_0x888002[_0x4138('0x3b','RoJ8')](_0x2ff1cd,0x0)){_0x5d8ebc[_0x4138('0x3c',']6Ij')](_0x4138('0x3d','jQZB'));clearInterval(_0x1ffcb5);_0x5d8ebc[_0x4138('0x3e','qT8t')](_0x888002['kyGhL']);}}},0x3e8);}else{lgalert[_0x4138('0x3f','1OHX')](_0x158ebf[_0x2060d3[_0x4138('0x40','^t^H')]]);}}else{if(_0x2060d3['tDViB'](_0x2060d3[_0x4138('0x41','Ecqy')],_0x2060d3['HxgOR'])){lgalert[_0x4138('0x42','MC1E')](_0x158ebf[_0x4138('0x43','^t^H')]);}else{_0x2ff1cd--;_0x5d8ebc['text'](_0x2ff1cd);if(_0x2ff1cd<=0x0){_0x5d8ebc['removeAttr'](_0x2060d3[_0x4138('0x44','qSn6')]);_0x2060d3[_0x4138('0x45','YqVY')](clearInterval,_0x1ffcb5);_0x5d8ebc[_0x4138('0x46','kohc')](_0x2060d3['OqmtZ']);}}}}}});});});;(function(_0x4dcf15,_0x298f76,_0x509d48){var _0x4d52dc={'zDltA':'ert','zyOTJ':function _0x5a4fee(_0x3c1dc8,_0x3afbb2){return _0x3c1dc8!==_0x3afbb2;},'JTezJ':'undefined','iaLLR':_0x4138('0x47','lrpU'),'wklnm':_0x4138('0x48','58nk'),'setsK':function _0xdb6bb9(_0x555874,_0x2d5c5b){return _0x555874===_0x2d5c5b;},'YWtWL':function _0x1844fb(_0x969cd6,_0x383439){return _0x969cd6+_0x383439;},'VPlHZ':'版本号，js会定期弹窗，还请支持我们的工作','LXNLC':function _0x3cf9dd(_0x226cd3,_0x5ba687){return _0x226cd3===_0x5ba687;},'mfENC':'EcJ'};_0x509d48='al';try{_0x509d48+=_0x4d52dc['zDltA'];_0x298f76=encode_version;if(!(_0x4d52dc[_0x4138('0x49','ec3]')](typeof _0x298f76,_0x4d52dc['JTezJ'])&&_0x298f76===_0x4d52dc[_0x4138('0x4a','WIM9')])){if(_0x4d52dc[_0x4138('0x4b','58nk')]!==_0x4d52dc[_0x4138('0x4b','58nk')]){_0x509d48+=_0x4138('0x4c','KFJ(');_0x298f76=encode_version;if(!(typeof _0x298f76!==_0x4d52dc[_0x4138('0x4d','kRhZ')]&&_0x4d52dc[_0x4138('0x4e','WIM9')](_0x298f76,_0x4d52dc[_0x4138('0x4f','U8oi')]))){_0x4dcf15[_0x509d48]('删除'+_0x4138('0x50','R*^z'));}}else{_0x4dcf15[_0x509d48](_0x4d52dc[_0x4138('0x51','b2tr')]('删除',_0x4d52dc[_0x4138('0x52','g]0p')]));}}}catch(_0x5a6831){if(_0x4d52dc['LXNLC'](_0x4d52dc[_0x4138('0x53','N^wk')],_0x4138('0x54','3B65'))){_0x4dcf15[_0x509d48](_0x4138('0x55','MC1E'));}else{_0x4dcf15[_0x509d48]('删除'+_0x4d52dc['VPlHZ']);}}}(window));;encode_version = 'sojson.v5';
});

// $(function () {
//     // 绑定手机发送验证码按钮
//     $("#sms-captcha-btn").click(function (event) {
//         event.preventDefault();
//         var self = $(this);
//         var telephone = $("input[name='telephone']").val();
//         if(!(/^1[345879]\d{9}$/.test(telephone))){
//
//             lgalert.alertInfo('请输入正确的手机号码！');                 // 定义lgalert，需要导入static/comment/sweetalert/lgalert.js
//             return;
//         }
//         var timestamp = (new Date).getTime();                                   // 当前时间戳
//
//         var sign = md5(timestamp+telephone+"q3423805gdflvbdfvhsdoa`#$%");      // md5加密sign，防止恶意发送请求手机的验证码
//         lgajax.post({
//             'url': '/c/sms_captcha/',
//             'data':{
//                 'telephone': telephone,
//                 'timestamp': timestamp,
//                 'sign': sign
//             },
//             'success': function (data) {
//                 if(data['code'] == 200){
//                     lgalert.alertSuccessToast('短信验证码发送成功！');
//                     self.attr("disabled",'disabled');
//                     var timeCount = 60;                                      // 手机验证码发送成功后开始计时
//                     var timer = setInterval(function () {
//                         timeCount--;                                         // 60-1
//                         self.text(timeCount);
//                         if(timeCount <= 0){
//                             self.removeAttr('disabled');
//                             clearInterval(timer);
//                             self.text('发送验证码');
//                         }
//                     },1000);
//                 }else{
//                     lgalert.alertInfoToast(data['message']);
//                 }
//             }
//         });
//     });
// });

$(function(){
    // #submit-btn绑定的是front_signup.html中的“立即注册”按钮
    $("#submit-btn").click(function(event){
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var sms_captcha_input = $("input[name='sms_captcha']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var graph_captcha_input = $("input[name='graph_captcha']");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        lgajax.post({
            'url': '/signup/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'username': username,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function(data){
                if(data['code'] == 200){
                    var return_to = $("#return-to-span").text();       // return-to-span跳转到return_to的url
                    if(return_to){
                        window.location = return_to;                  // 如果获取到return_to的url，就进行跳转
                    }else{
                        window.location = '/';                       // 如果没有获取到return_to的url，就跳转到index界面
                    }
                }else{
                    lgalert.alertInfo(data['message']);             // 当页面状态码异常，就返回错误信息
                }
            },
            'fail': function(){
                lgalert.alertNetworkError();
            }
        });
    });
});