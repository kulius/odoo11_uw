/**
 * CFPrint打印类
 * ver 1.3.8.1
 * 康虎软件工作室
 * Email: wdmsyf@sina.com
 * QQ: 360026606
 * 微信: 360026606
 */

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

/**
 * 
 * MDN文档参考：https://developer.mozilla.org/en-US/docs/Web/API/WebSocket 
 * 模块导入方式的解释：http://stackoverflow.com/questions/27133852/export-module-pattern
 */
;(function(root, factory){
  var ws = factory(root);
  if(typeof define === 'function' && define.amd){
    define([],factory);
  }else if(typeof module !== 'undefined' &&module.exports){
    module.exports=factory();
  }else{
    root.ws = factory();
  }
}(this || window, function(root, undefined){

  if(!('WebSocket' in window)) return;

  var _handlers = {},
    wsocket,
    eventTarget = document.createElement('div'),
    settings = {
      //是否自动重连
      automaticOpen: true,
      //自动重连延迟重连速度
      reconnectDecay: 1.5,
      //默认地址
      host: "127.0.0.1",
      //默认端口
      port: 54321,
      //默认协议
      protocol: "ws",
    },
    func = function (evt) {
      switch(evt.type){
        case "connecting":
          console.log("Connecting to cfprint.", evt);
          break;
        case "open":
          console.log("Connected to cfprint.", evt);
          break;
        case "close":
          console.log("Disconnected from cfprint.", evt);
          break;
        case "message":
          console.log("Got a message from cfprint: "+evt.data, evt);
          break;
        case "error":
          console.log("A error occured: "+evt.data, evt);
          break;
        default:
          console.log("EVENT: ", evt);
      }
    },
    //对外泄露 API ??
    _api = {
      CONNECTING: WebSocket.CONNECTING,
      OPEN: WebSocket.OPEN,
      CLOSING: WebSocket.CLOSING,
      CLOSED: WebSocket.CLOSED
    };

  /**
   * [ws]
   * @param  参数 host 为打印服务器的地址
   * @param  参数 port 为打印服务器的监听端口
   * @param  参数 protocols 为服务器选择的子协定
   * @param  参数 options 初始化定义参数
   *         automaticOpen: 是否自动连接标志(true|false)，默认为true
   *         reconnectDecay:自动重连延迟重连速度，数字，默认为1.5
   *         protocol：　　通讯协议(ws|wss)，默认为"ws"
   *         host:　　　　　打印服务器地址，默认为"127.0.0.1"
   *         port:　　　　　打印服务器监听端口，数字，默认为54321
   */
  function ws(host, port, options){
    var self = this;
    this.ver = "1.3.8.1";      //版本号
        
    // 绑定选项定义设置
    if (!options) {options = {};}
    for (var key in settings) {
      if (typeof options[key] !== 'undefined') this[key] = options[key];
      else this[key] = settings[key];
    }
    
    //websocket host
    this.host = host || this.host;

    //websocket port
    this.port = port || this.port;

    /**
     * http://tools.ietf.org/html/rfc6455
     * 服务器选择的子协定，这是建立 WebSocket 对象时 protocols 参数里的其中一个字符串。
     */
    //this.protocol = protocol ? protocol : this.protocol;
    //this.protocol = this.protocol;

    //websocket url
    //this.url = (this.protocol||"ws") + "://"+this.host+":"+this.port;
    this.url = this.getURL();
    
    //websocket 状态
    this.readyState = WebSocket.CONNECTING;

    // 公开 API
    for(var a in _api) this[a] = _api[a];

    //用事件处理程序
    eventTarget.addEventListener('connecting', function(event) {  
      self!==window && self.onconnecting(event); 
    });
    eventTarget.addEventListener('open',     function(event) { 
      self!==window && self.onopen(event); 
    });
    eventTarget.addEventListener('message',  function(event) {
      self!==window && self.onmessage(event); 
    });
    eventTarget.addEventListener('close',    function(event) {
      self!==window && self.onclose(event); 
    });
    eventTarget.addEventListener('error',    function(event) {
      self!==window && self.onerror(event); 
    });

    // 公开事件目标的API
    this.addEventListener = eventTarget.addEventListener.bind(eventTarget);
    this.removeEventListener = eventTarget.removeEventListener.bind(eventTarget);
    this.dispatchEvent = eventTarget.dispatchEvent.bind(eventTarget);

    if(this.automaticOpen === true && this!==window) this.open();
    return this;
  }

  /**
   * [generateEvent 该函数产生一个事件，与标准兼容，兼容的浏览器和IE9 - IE11？]
   * http://stackoverflow.com/questions/19345392/why-arent-my-parameters-getting-passed-through-to-a-dispatched-event/19345563#19345563
   * https://msdn.microsoft.com/library/ff975299(v=vs.85).aspx
   * @param eventName 位字符串类型的事件名字
   * @param 参数的args对象的可选对象，该事件将使用
   */
  function generateEvent(eventName, args) {
    var evt = document.createEvent("CustomEvent");
    evt.initCustomEvent(eventName, false, false, args);
    return evt;
  }

  ws.prototype.onconnecting = func;
  ws.prototype.onopen = func;
  ws.prototype.onmessage = func;
  ws.prototype.onclose = func;
  ws.prototype.onerror = func;

  /**
   * 重新设置protocol
   */
  ws.prototype.setProtocol = function(_protocol){
    if(this.wsocket){
      this.protocol = _protocol;
    }
  }

  /**
   * 重新设置端口
   */
  ws.prototype.setPort = function(_port){
    if(this.wsocket){
      this.port = _port;
    }
  }
  
  /**
   * 重新设置Host
   */
  ws.prototype.setHost = function(_host){
    if(this.wsocket){
      this.host = _host;
    }
  }

  /**
   *获取URL，如果已连接，则返回当前连接的URL，否则根据协议、地址和端口参数进行拼接
   */
  ws.prototype.getURL = function(_url){
    if(this.wsocket && this.wsocket.readyState===this.OPEN){
      return this.wsocket.url;
    }else{
      return (this.protocol||"ws") + "://" + (this.host||"127.0.0.1") + ":" + (this.port||54321);
    }
  }

  /**
   * [send 发送 websocket 消息]
   * @param 参数 data 为发消息的内容
   */
  ws.prototype.send = function (data) {
    if(this.wsocket && this.wsocket.readyState===1) {
      var  _dat = "";
      if(typeof(data)==="string")
        _dat = data;
      else if(typeof(data)==="object")
        _dat = JSON.stringify(data, null, 2);
      else{
        var evt = generateEvent('error', {"message":"Invalid data format, only json string or json object is allowed."});
        eventTarget.dispatchEvent(evt);
        return;
      }
      try{
				//json转换成Base64，以避免有些语言中出现部分乱码
      	_dat = btoa(unescape(encodeURIComponent(_dat)));
      	//console.log(_dat);
      	_dat = "base64:"+_dat;  //增加"base64"头，以避免在Delphi中判断是否Base64编码
        this.wsocket.send(_dat);  
      }catch(e){
        var evt = generateEvent('error', {"message":e.message});
        eventTarget.dispatchEvent(evt);
      }
    }else{
      var evt = generateEvent('error', {"message":"Not connected to cfprint server or disconnected."});
      eventTarget.dispatchEvent(evt);
      //throw 'INVALID_STATE_ERR : Pausing to reconnect websocket';
    }
  };

  /**
   * [close 关闭 websocket 连接。]
   * 如果已经关闭了连接，此方法不起作用。
   * 
   * 错误代码参考：https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent
   * @param 参数 code 为错误代码 1000为正常关闭， The code must be either 1000, or between 3000 and 4999. 2000 is neither.
   * @param 参数 reason 为错误理由
   */
  ws.prototype.close = function (code, reason){
    // 默认CLOSE_NORMAL代码
    if (typeof code === 'undefined') code = 1000;
    if (this.wsocket) this.wsocket.close(code, reason);
  };

  /**
   * [open 打开建立 websocket 握手连接]
   */
  ws.prototype.open = function () {
    var self = this;
    
    //用最新的参数组装url
    //this.url = this.protocol + "://"+this.host+":"+this.port;
    this.url = this.getURL();
    
    wsocket = new WebSocket(this.url, this.protocol || []);
    eventTarget.dispatchEvent(generateEvent('connecting'));
    wsocket.onopen = function(event) {
      self.protocol = ws.protocol;
      self.readyState = WebSocket.OPEN;
      var e = generateEvent('open');
      eventTarget.dispatchEvent(e);
    };
    wsocket.onclose = function(event) {
      self.readyState = WebSocket.CLOSED;
      var e = generateEvent('connecting');
      e.code = event.code;
      e.reason = event.reason;
      e.wasClean = event.wasClean;
      eventTarget.dispatchEvent(e);
      eventTarget.dispatchEvent(generateEvent('close'));
    };
    wsocket.onmessage = function(event) {
      var e = generateEvent('message');
      e.data = event.data;
      eventTarget.dispatchEvent(e);
    };
    wsocket.onerror = function(event) {
      var e = generateEvent('error');
      eventTarget.dispatchEvent(e);
    };
    this.wsocket = wsocket;
    return this;
  };
  
  ws.prototype.state = function(){
    if(this.wsocket){
      return this.wsocket.readyState;
    }else{
      return WebSocket.CLOSED;
    }
  }
  
  /**
   * 输出调试日志
  */
  ws.prototype.log = function(s, e) {
    var _id = this.output || "output";
    var output = document.getElementById(_id);
    if(output && output.appendChild){
      var p = document.createElement("p");
      p.style.wordWrap = "break-word";
      p.style.padding="8px";
      p.style.background="#eee";
      //p.textContent = "LOG: "+s;
      p.innerHTML = "LOG: "+s;
      if(output.childNodes.length>0) 
        output.insertBefore(p, output.childNodes[0]);
      else
        output.appendChild(p);
    }
    e? console.log(s, e) : console.log(s);
  }
  
  return ws;
}));



/**
==========================================================
CFPrint类:
属性:
ver: 本类库版本号，只读

方法：
ws(protocols, host, port, options): 初始化打印对象
参数：
参数 host 为打印服务器的地址
参数 port 为打印服务器的监听端口
参数 protocols 为服务器选择的子协定
参数 options 初始化定义参数
         automaticOpen: 是否自动连接标志(true|false)，默认为true
         reconnectDecay:自动重连延迟重连速度，数字，默认为1.5
         protocols：　　通讯协议(ws|wss)，默认为"ws"

open():  建立与打印服务器的连接
close(): 关闭与打印服务器的连接
send(string|obj): 发送打印数据，可以是json字符串或json对象

事件：
onconnecting(event)：正在连接打印服务器事件，参数无实质内容

onopen(event)：　　　与打印服务器连接成功事件，参数无实质内容

onmessage(event)：　　接收到服务器消息事件，打印成功与否都从该事件获得
事件结构：
event.data： 打印服务器返回的信息，json格式。只读
返回打印结构格式为：{"result": 1, "message": "完成"}  或　{"result": 0, "message": "<出错信息>"}

onerror(event):　　　出错事件


数据格式：
打印数据为json格式，具体如下：
{
  "template": "waybill_huaxia3.fr3",

   //报表字段定义，与报表设计时的字段对应
   "Tables":[
     "table":{
       "Name": "Table1",
      "Cols": [
        {
          "type": "str",     //字段类型，取值为：str、int、float、
          "size": 255,       //字段长度
          "name": "HAWB#",     //字段名称
          "required": false    //是否必录字段
        },
        {"type": "int", "size": 0, "name": "NO", "required": false},
        {"type": "float", "size": 0, "name": "华夏单号", "required": false},
        {"type": "integer", "size": 0, "name": "鹭路通单号", "required": false},
        {"type": "str", "size": 255, "name": "发件人", "required": false},
        {"type": "str", "size": 255, "name": "发件人地址", "required": false},
        {"type": "str", "size": 255, "name": "发件人电话", "required": false},
        {"type": "str", "size": 255, "name": "发货国家", "required": false},
        {"type": "str", "size": 255, "name": "收件人", "required": false},
        {"type": "str", "size": 255, "name": "收件人地址", "required": false},
        {"type": "str", "size": 255, "name": "收件人电话", "required": false},
        {"type": "str", "size": 255, "name": "收货人证件号码", "required": false},
        {"type": "str", "size": 255, "name": "收货省份", "required": false},
        {"type": "float", "size": 0, "name": "总计费重量", "required": false},
        {"type": "int", "size": 0, "name": "总件数", "required": false},
        {"type": "float", "size": 0, "name": "申报总价（CNY）", "required": false},
        {"type": "float", "size": 0, "name": "申报总价（JPY）", "required": false},
        {"type": "int", "size": 0, "name": "件数1", "required": false},
        {"type": "str", "size": 255, "name": "品名1", "required": false},
        {"type": "float", "size": 0, "name": "单价1（JPY）", "required": false},
        {"type": "str", "size": 255, "name": "单位1", "required": false},
        {"type": "float", "size": 0, "name": "申报总价1（CNY）", "required": false},
        {"type": "float", "size": 0, "name": "申报总价1（JPY）", "required": false},
        {"type": "int", "size": 0, "name": "件数2", "required": false},
        {"type": "str", "size": 255, "name": "品名2", "required": false},
        {"type": "float", "size": 0, "name": "单价2（JPY）", "required": false},
        {"type": "str", "size": 255, "name": "单位2", "required": false},
        {"type": "float", "size": 0, "name": "申报总价2（CNY）", "required": false},
        {"type": "float", "size": 0, "name": "申报总价2（JPY）", "required": false},
        {"type": "int", "size": 0, "name": "件数3", "required": false},
        {"type": "str", "size": 255, "name": "品名3", "required": false},
        {"type": "float", "size": 0, "name": "单价3（JPY）", "required": false},
        {"type": "str", "size": 255, "name": "单位3", "required": false},
        {"type": "float", "size": 0, "name": "申报总价3（CNY）", "required": false},
        {"type": "float", "size": 0, "name": "申报总价3（JPY）", "required": false},
        {"type": "int", "size": 0, "name": "件数4", "required": false},
        {"type": "str", "size": 255, "name": "品名4", "required": false},
        {"type": "float", "size": 0, "name": "单价4（JPY）", "required": false},
        {"type": "str", "size": 255, "name": "单位4", "required": false},
        {"type": "float", "size": 0, "name": "申报总价4（CNY）", "required": false},
        {"type": "float", "size": 0, "name": "申报总价4（JPY）", "required": false},
        {"type": "int", "size": 0, "name": "件数5", "required": false},
        {"type": "str", "size": 255, "name": "品名5", "required": false},
        {"type": "float", "size": 0, "name": "单价5（JPY）", "required": false},
        {"type": "str", "size": 255, "name": "单位5", "required": false},
        {"type": "float", "size": 0, "name": "申报总价5（CNY）", "required": false},
        {"type": "float", "size": 0, "name": "申报总价5（JPY）", "required": false},
        {"type": "str", "size": 255, "name": "参考号", "required": false},
        {"type": "AutoInc", "size": 0, "name": "ID", "required": false}
      ],

      //报表数据列，字段名要与上面字段定义一一对应
      "Data": [
        {
          "鹭路通单号": 730293,
          "发货国家": "日本",
          "单价1（JPY）": null,
          "申报总价2（JPY）": null,
          "单价4（JPY）": null,
          "申报总价2（CNY）": null,
          "申报总价5（JPY）": null,
          "华夏单号": 200303900791,
          "申报总价5（CNY）": null,
          "收货人证件号码": null,
          "申报总价1（JPY）": null,
          "单价3（JPY）": null,
          "申报总价1（CNY）": null,
          "申报总价4（JPY）": null,
          "申报总价4（CNY）": null,
          "收件人电话": "182-1758-8628",
          "收件人地址": "上海市闵行区虹梅南路1660弄蔷薇八村39号502室",
          "HAWB#": "860014010055",
          "发件人电话": "03-3684-3676",
          "发件人地址": " 1-1-13,Kameido,Koto-ku,Tokyo",
          "NO": 3,
          "ID": 3,
          "单价2（JPY）": null,
          "申报总价3（JPY）": null,
          "单价5（JPY）": null,
          "申报总价3（CNY）": null,
          "收货省份": null,
          "申报总价（JPY）": null,
          "申报总价（CNY）": null,
          "总计费重量": 3.2,
          "收件人": "张振泉2",
          "总件数": 13,
          "品名5": null,
          "品名4": null,
          "品名3": null,
          "品名2": null,
          "品名1": "纸尿片",
          "参考号": null,
          "发件人": "NAKAGAWA SUMIRE 2",
          "单位5": null,
          "单位4": null,
          "单位3": null,
          "单位2": null,
          "单位1": null,
          "件数5": null,
          "件数4": null,
          "件数3": 3,
          "件数2": null,
          "件数1": 10
        },
        ...
      ]
    }
  ]
}
========================================================
*/
