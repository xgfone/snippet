// 创建 XMLHttpRequest 对象的通用函数
function createXMLHttpRequest() {
	var xmlhttp = null;
	if (window.XMLHttpRequest) { // for DOM2(IE7+, Firefox, Chrome, Safari, Opera)
		xmlhttp = new XMLHttpRequest();
	} else if (window.ActiveXObject) { // for IE5, IE6
		var i,
			versions = [
				'Microsoft.XMLHTTP',
				'MSXML.XMLHTTP',
				'Microsoft.XMLHTTP',
				'Msxml2.XMLHTTP.7.0',
				'Msxml2.XMLHTTP.6.0',
				'Msxml2.XMLHTTP.5.0',
				'Msxml2.XMLHTTP.4.0',
				'MSXML2.XMLHTTP.3.0',
				'MSXML2.XMLHTTP'
			];
		// versions = [
		// 	"MSXML2.XMLHTTP.6.0",
		// 	"MSXML2.XMLHTTP.5.0",
		// 	"MSXML2.XMLHTTP.4.0",
		// 	"MSXML2.XMLHTTP.3.0",
		// 	"MSXML2.XMLHTTP",
		// 	"Microsoft.XMLHTTP",
		// ];

		for (i = 0; i < versions.length; i++) {
			try {
				xmlhttp = new ActiveXObject(versions[i]);
				break;
			} catch (e) {
				// Pass
			}
		}
	}

	if (xmlhttp) {
		return xmlhttp;
	}

	throw new Error("XMLHttpRequest is not supported");
}


// 将日志消息写到 JavaScript 控制台上
function log(message) {
	if (typeof console === "object") {
		console.log(message);
	} else if (typeof opera === "object") {
		opera.postError(message);
	} else if (typeof java === "object" && typeof java.lang === "object") {
		java.lang.System.out.println(message);
	}
}


// 将消息记录到当前页面
function log(message) {
	var console = document.getElementById("debuginfo");
	if (console === null) {
		console = document.createElement("div");
		console.id = 'debuginfo';
		console.style.background = '#dedede';
		console.style.border = '1px solid silver';
		console.style.padding = '5px';
		console.style.width = '400px';
		console.style.position = 'absolute';
		console.style.right = '0px';
		console.style.top = '0px';
		document.body.appendChild(console);
	}
	console.innerHTML += "<p>" + message + "</p>";
}



// 根据用户代理字符串，检测呈现引擎、平台、Windows操作系统、移动设备和游戏系统
var client = function () {
	// 呈现引擎
	var engine = {
		ie: 0,
		gecko: 0,
		webkit: 0,
		khtml: 0,
		opera: 0,

		// 完整的版本号
		ver: null,
	};

	// 浏览器
	var browser = {
		// 主要浏览器
		ie: 0,
		firfox: 0,
		safari: 0,
		konq: 0,
		opera: 0,
		chrome: 0,

		// 具体的版本号
		ver: null,
	};

	// 平台、设备和操作系统
	var system = {
		win: false,
		mac: false,
		x11: false,

		// 移动设备
		iphone: false,
		ipod: false,
		ipad: false,
		ios: false,
		android: false,
		nokiaN: false,
		winMobile: false,

		// 游戏系统
		wii: false,
		ps: false,
	};

	// 检测呈现引擎和浏览器
	var ua = navigator.userAgent;
	if (window.opera) {
		engine.ver = browser.ver = window.opera.versions();
		engine.opera = browser.opera = parseFloat(engine.ver);
	} else if (/AppleWebKit\/(\S+)/.test(ua)) {
		engine.ver = RegExp["$1"];
		engine.webkit = parseFloat(engine.ver);

		// 确定 Chrome 还是 Safari
		if (/Chrome\/(\S+)/.test(ua)) {
			browser.ver = RegExp["$1"];
			browser.chrome = parseFloat(browser.ver);
		} else if (/Version\/(\S+)/.test(ua)) {
			browser.ver = RegExp["$1"];
			browser.safari = parseFloat(browser.ver);
		} else {
			// 近似地确定版本号
			var safariVersion = 1;
			if (engine.webkit < 100) {
				safariVersion = 1;
			} else if (engine.webkit < 312) {
				safariVersion = 1.2;
			} else if (engine.webkit < 412) {
				safariVersion = 1.3;
			} else {
				safariVersion = 2;
			}
			browser.safari = browser.ver = safariVersion;
		}
	} else if (/KHTML\/(\S+)/.test(ua) || /Konqueror\/([^;]+)/.test(ua)) {
		engine.ver = browser.ver = RegExp["$1"];
		engine.khtml = browser.konq = parseFloat(engine.ver);
	} else if (/rv:([^\)]+)\) Gecko\/\d{8}/.test(ua)) {
		engine.ver = RegExp["$1"];
		engine.gecko = parseFloat(engine.ver);

		// 确定是不是 Firefox
		if (/Firefox\/(\S+)/.test(ua)) {
			browser.ver = RegExp["$1"];
			browser.firfox = parseFloat(browser.ver);
		}
	} else if (/MSIE ([^;]+)/.test(ua)) {
		engine.ver = browser.ver = RegExp["$1"];
		engine.ie = browser.ie = parseFloat(engine.ver);
	}

	// 检测浏览器
	browser.ie = engine.ie
	browser.opera = engine.opera

	// 检测平台
	var p = navigator.platform;
	system.win = p.indexOf("Win") === 0;
	system.mac = p.indexOf("Mac") === 0;
	system.x11 = (p === "x11") || (p.indexOf("Linux") === 0);

	// 检测 Windows 操作系统
	if (system.win) {
		if (/Win(?:dows )?([^do](2))\s?(\d+\.\d+)?/.test(ua)) {
			if (RegExp["$1"] === "NT") {
				switch (RegExp["$2"]) {
				case "5.0":
					system.win = "2000";
					break;
				case "5.1":
					system.win = "XP";
					break;
				case "6.0":
					system.win = "Vista";
					break;
				case "6.1":
					system.win = "7":
				default:
					system.win = "NT";
					break;
				}
			} else if (RegExp["$1"] === "9x") {
				system.win = "ME";
			} else {
				system.win = RegExp["$1"];
			}
		}
	}

	// 移动设备
	system.iphone = ua.indexOf("iPhone") > -1;
	system.ipod = ua.indexOf("iPod") > -1;
	system.ipad = ua.indexOf("iPad") > -1;
	system.nokiaN = ua.indexOf("NokiaN") > -1;

	// Windows mobile
	if (system.win === "CE") {
		system.winMobile = system.win;
	} else if (system.win === "Ph") {
		if (/Windows Phone OS (\d+.\d+)/.test(ua)) {
			system.win = "Phone";
			system.winMobile = parseFloat(RegExp["$1"]);
		}
	}

	// 检测 iOS 版本
	if (system.mac && ua.indexOf("Mobile*") > -1) {
		if (/CPU (?:iPhone )?OS (\d+_\d+)/.test(ua)) {
			system.ios = parseFloat(RegExp.$1.replace("_", "."));
		} else {
			system.ios = 2; // 不能真正检测出来，所以只能猜测
		}
	}

	// 检测 Android 版本
	if (/Android (\d+\.\d+)/.test(ua)) {
		system.android = parseFloat(RegExp["$1"]);
	}

	// 游戏系统
	system.wii = ua.indexOf("Wii") > -1;
	system.ps = /playstation/i.test(ua);

	// 返回这些对象
	return {
		engine: engine,
		browser: browser,
		system: system,
	};
}();