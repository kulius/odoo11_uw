/**
 * CFPrint打印辅助类
 * ver 1.2.1
 * 康虎软件工作室
 * Email: wdmsyf@sina.com
 * QQ: 360026606
 * 微信: 360026606
 *
 * 用法：
 * 启动康虎云打印服务器后，在Odoo中，通过自定义模块，生成打印所需要的报表数据Json字符中，并命名为_reportData，即可自动打印。
 * 通过重设 _delay_send 和 _delay_close 两个参数，可以调整发送打印以及打印完毕后关闭报表页面的延时时长。
 */

//var _reportData = '{"template":"waybill_huaxia3.fr3","Cols":[{"type":"str","size":255,"name":"HAWB#","required":false},{"type":"int","size":0,"name":"NO","required":false},{"type":"float","size":0,"name":"华夏单号","required":false},{"type":"integer","size":0,"name":"鹭路通单号","required":false},{"type":"str","size":255,"name":"发件人","required":false},{"type":"str","size":255,"name":"发件人地址","required":false},{"type":"str","size":255,"name":"发件人电话","required":false},{"type":"str","size":255,"name":"发货国家","required":false},{"type":"str","size":255,"name":"收件人","required":false},{"type":"str","size":255,"name":"收件人地址","required":false},{"type":"str","size":255,"name":"收件人电话","required":false},{"type":"str","size":255,"name":"收货人证件号码","required":false},{"type":"str","size":255,"name":"收货省份","required":false},{"type":"float","size":0,"name":"总计费重量","required":false},{"type":"int","size":0,"name":"总件数","required":false},{"type":"float","size":0,"name":"申报总价（CNY）","required":false},{"type":"float","size":0,"name":"申报总价（JPY）","required":false},{"type":"int","size":0,"name":"件数1","required":false},{"type":"str","size":255,"name":"品名1","required":false},{"type":"float","size":0,"name":"单价1（JPY）","required":false},{"type":"str","size":255,"name":"单位1","required":false},{"type":"float","size":0,"name":"申报总价1（CNY）","required":false},{"type":"float","size":0,"name":"申报总价1（JPY）","required":false},{"type":"int","size":0,"name":"件数2","required":false},{"type":"str","size":255,"name":"品名2","required":false},{"type":"float","size":0,"name":"单价2（JPY）","required":false},{"type":"str","size":255,"name":"单位2","required":false},{"type":"float","size":0,"name":"申报总价2（CNY）","required":false},{"type":"float","size":0,"name":"申报总价2（JPY）","required":false},{"type":"int","size":0,"name":"件数3","required":false},{"type":"str","size":255,"name":"品名3","required":false},{"type":"float","size":0,"name":"单价3（JPY）","required":false},{"type":"str","size":255,"name":"单位3","required":false},{"type":"float","size":0,"name":"申报总价3（CNY）","required":false},{"type":"float","size":0,"name":"申报总价3（JPY）","required":false},{"type":"int","size":0,"name":"件数4","required":false},{"type":"str","size":255,"name":"品名4","required":false},{"type":"float","size":0,"name":"单价4（JPY）","required":false},{"type":"str","size":255,"name":"单位4","required":false},{"type":"float","size":0,"name":"申报总价4（CNY）","required":false},{"type":"float","size":0,"name":"申报总价4（JPY）","required":false},{"type":"int","size":0,"name":"件数5","required":false},{"type":"str","size":255,"name":"品名5","required":false},{"type":"float","size":0,"name":"单价5（JPY）","required":false},{"type":"str","size":255,"name":"单位5","required":false},{"type":"float","size":0,"name":"申报总价5（CNY）","required":false},{"type":"float","size":0,"name":"申报总价5（JPY）","required":false},{"type":"str","size":255,"name":"参考号","required":false},{"type":"AutoInc","size":0,"name":"ID","required":false}],"Data":[{"鹭路通单号":730293,"发货国家":"日本","单价1（JPY）":null,"申报总价2（JPY）":null,"单价4（JPY）":null,"申报总价2（CNY）":null,"申报总价5（JPY）":null,"华夏单号":200303900791,"申报总价5（CNY）":null,"收货人证件号码":null,"申报总价1（JPY）":null,"单价3（JPY）":null,"申报总价1（CNY）":null,"申报总价4（JPY）":null,"申报总价4（CNY）":null,"收件人电话":"182-1758-8628","收件人地址":"上海市闵行区虹梅南路1660弄蔷薇八村39号502室","HAWB#":"860014010055","发件人电话":"03-3684-3676","发件人地址":" 1-1-13,Kameido,Koto-ku,Tokyo","NO":3,"ID":3,"单价2（JPY）":null,"申报总价3（JPY）":null,"单价5（JPY）":null,"申报总价3（CNY）":null,"收货省份":null,"申报总价（JPY）":null,"申报总价（CNY）":null,"总计费重量":3.20,"收件人":"张振泉2","总件数":13,"品名5":null,"品名4":null,"品名3":null,"品名2":null,"品名1":"纸尿片","参考号":null,"发件人":"NAKAGAWA SUMIRE 2","单位5":null,"单位4":null,"单位3":null,"单位2":null,"单位1":null,"件数5":null,"件数4":null,"件数3":3,"件数2":null,"件数1":10},{"鹭路通单号":730291,"发货国家":"日本","单价1（JPY）":null,"申报总价2（JPY）":null,"单价4（JPY）":null,"申报总价2（CNY）":null,"申报总价5（JPY）":null,"华夏单号":200303900789,"申报总价5（CNY）":null,"收货人证件号码":null,"申报总价1（JPY）":null,"单价3（JPY）":null,"申报总价1（CNY）":null,"申报总价4（JPY）":null,"申报总价4（CNY）":null,"收件人电话":"182-1758-8628","收件人地址":"上海市闵行区虹梅南路1660弄蔷薇八村39号502室","HAWB#":"860014010035","发件人电话":"03-3684-3676","发件人地址":" 1-1-13,Kameido,Koto-ku,Tokyo","NO":1,"ID":1,"单价2（JPY）":null,"申报总价3（JPY）":null,"单价5（JPY）":null,"申报总价3（CNY）":null,"收货省份":null,"申报总价（JPY）":null,"申报总价（CNY）":null,"总计费重量":3.20,"收件人":"张振泉","总件数":13,"品名5":null,"品名4":null,"品名3":null,"品名2":null,"品名1":"纸尿片","参考号":null,"发件人":"NAKAGAWA SUMIRE","单位5":null,"单位4":null,"单位3":null,"单位2":null,"单位1":null,"件数5":null,"件数4":null,"件数3":3,"件数2":null,"件数1":10},{"鹭路通单号":730292,"发货国家":"日本","单价1（JPY）":null,"申报总价2（JPY）":null,"单价4（JPY）":null,"申报总价2（CNY）":null,"申报总价5（JPY）":null,"华夏单号":200303900790,"申报总价5（CNY）":null,"收货人证件号码":null,"申报总价1（JPY）":null,"单价3（JPY）":null,"申报总价1（CNY）":null,"申报总价4（JPY）":null,"申报总价4（CNY）":null,"收件人电话":"182-1758-8628","收件人地址":"上海市闵行区虹梅南路1660弄蔷薇八村39号502室","HAWB#":"860014010045","发件人电话":"03-3684-3676","发件人地址":" 1-1-13,Kameido,Koto-ku,Tokyo","NO":2,"ID":2,"单价2（JPY）":null,"申报总价3（JPY）":null,"单价5（JPY）":null,"申报总价3（CNY）":null,"收货省份":null,"申报总价（JPY）":null,"申报总价（CNY）":null,"总计费重量":3.20,"收件人":"张振泉1","总件数":13,"品名5":null,"品名4":null,"品名3":null,"品名2":null,"品名1":"纸尿片","参考号":null,"发件人":"NAKAGAWA SUMIRE 1","单位5":null,"单位4":null,"单位3":null,"单位2":null,"单位1":null,"件数5":null,"件数4":null,"件数3":3,"件数2":null,"件数1":10}]}';
var _reportData = _reportData || '';
var _delay_send = 1000;  //发送打印服务器前延时时长
var _delay_close = 1000;  //打印完成后关闭窗口的延时时长, -1则表示不关闭
var cfprint_addr = "127.0.0.1";
var cfprint_port = 54321;

//在页面显示结果
function _log(message) {
    var output = document.getElementById("output");
    var pre = document.createElement("p");
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message;
    if(typeof(output)!="undefined")
        output.appendChild(pre);
    else
        console.log(message);
}
/**
 * 把字符串中的HTML标签去掉
 * 用法：
var str = "<span name='233241' id=2341>张酝</span><span name='233241' id=2341>张酝AAA</span>";
var s = str.removeHTMLTag();
alert(s);
 */
if(typeof(String.prototype.removeHTMLTag)=="undefined"){
	String.prototype.removeHTMLTag = function(){
		return this.replace(/<.+?>([^<>]+?)<.+?>/g, '$1');
	}
}

var cfprint;
var init = function(){
	var _addr = cfprint_addr || "192.168.56.1";
	var _port = cfprint_port || 54321;
	cfprint = CFPrint.createNew(_addr, _port); //设置云打印服务器的地址和端口
	cfprint.setOnOpen(function(evt){
		_log("CONNECTED");
	});

	cfprint.setOnClose(function(evt){
		_log("DISCONNECTED");
	});

	cfprint.setOnMessage(function(evt){
		_log('<span style="color: blue;">RESPONSE: ' + evt.data+'</span>');
        respObj = JSON && JSON.parse(evt.data) || $.parseJSON(evt.data);
        if(respObj.result == 1){
            if(_delay_close>0)
                setTimeout(function(){open(location, '_self').close();}, _delay_close); //延时后关闭报表窗口
        }else{
            alert("Print failed: "+respObj.message);
        }
	});

	cfprint.setOnError(function(evt){
		_log('<span style="color: red;">ERROR:</span> ' + evt.data);
	});

	cfprint.connect();		//Connect to print server
}

//发送数据到打印服务器
function doSend(message) {
  _log("SENT: <br/>" + message);
  cfprint.send(message);
}

function doInit(){
	init();
}

/**
 * JQuery 下的用法
$(document).ready(function(){
	doInit();
  if(typeof(_reportData) != "undefined" && _reportData != ""){
      setTimeout(function () {
          doSend(_reportData);
      }, _delay_send);
  }else {
      _log("要打印的报表内容为空，取消打印。");
  }
});
*/

window.addEventListener("load", function(){
	doInit();
	if(typeof(_reportData) != "undefined" && _reportData != ""){
	    if(_delay_send>0){
	      setTimeout(function () {
	          doSend(_reportData);
	      }, _delay_send);
	    }
	}else {
	    _log("要打印的报表内容为空，取消打印。");
	}
}, false);