
PasteDeploy
===========

Copyright © 2014 - 2016 xgfone(三界). All Rights Reserved.

## 前言

下文是一个学习摘要，并不保证看完之后，就对 `PasteDeploy` 精通了。要想明白下文的意思，需要简单地了解 `PasteDeploy` 的处理流程，或者能够使用 `PasteDeploy` 部署一个简单的应用程序。

如果不懂 `PasteDeploy`，可以参见它的 [官方文档](http://pythonpaste.org/deploy/)，整个文档才10页左右（按PDF来算），除了目录和一些没用的说明之外，整个核心文档大概在七、八页左右。但它是英文的，如果想看中文的，请猛点 [这里](http://blog.chinaunix.net/uid-22400280-id-3281767.html)，它是一个不完整、粗陋的、有点混乱的翻译（不知道别人感觉如何，反正笔者是这么个感觉）。


## 正文

`PasteDeploy`是一套用`Python`实现的、完整的、用于查找和配置 `WSGI`  `应用程序（Application）`和`服务器（Server）`的管理系统。

`PasteDeploy`是一套独立的管理系统，并不依赖其它的`Paste`组件。

### 1、PasteDeploy 默认暴露出了四个接口
```python
loadapp(uri, name=None, relative_to=None, global_conf=None)      # 用于加载 WSGI Application
loadfilter(uri, name=None, relative_to=None, global_conf=None)   # 用于加载 Filter，过滤 WSGI Application
loadserver(uri, name=None, relative_to=None, global_conf=None)   # 用于加载 Server，可以启动一个HTTP服务器
loadconfig(uri, name=None, relative_to=None, global_conf=None)   # 仅用于加载配置文件，得到配置信息，并不产生App等
```

上述四个接口的参数都相同，几乎具有相同的语义。下面以`加载App`为例说明：

#### (1) uri
这是必须的，不可省略。它指定了如何加载一个`Application`。`PasteDeploy`支持两种方式：

    A. 读取配置文件，根据配置文件的信息来加载；
    B. 通过EGG来加载。

建议使用`配置文件`，而不是`EGG`。`uri`参数的开头通过一个前缀来指定了使用哪个方式：

    如果前缀以 config，则使用配置文件；
    如果前缀以 egg 开头，则使用 EGG 方式。

`uri`参数由三部分组成：

    A. 配置方式前缀（config 和 egg）
    B. 配置路径（配置文件路径或egg导入路径）
    C. 要加载的App名字（可选）

前缀与路径之间使用`冒号（:）`分隔，路径与App名字之间使用`井号（#）`分隔。

注：App名字中可以包含 `#` 符号，因此，`路径与App名字的分隔符取 uri 字符串中的第一个 #`。如：
```
config:/path/to/conf.ini#name#aa#bb
```
其中，配置方式是`config`——使用配置文件，配置文件路径是 `/path/to/conf.ini`，App名字是 `name#aa#bb`。

#### (2) name
指定要加载的App的名字。

该参数与 `uri` 参数中指定的 `App` 名字之间的关系请参见下文。

#### (3) relative_to
指定要加载的配置文件的相对哪个路径，即指定配置文件的相对路径。

该参数与 `uri` 参数中指定的配置路径之间的关系请参见下文。

#### (4) global_conf
该选项是一个字典，用来指定额外的全局变量。

该选项中键值对将会被作为全局变量添加到配置文件中的全局变量章节（即 `DEFAULT` section）中。注意：这句话的意思并**`不是把该选项中的值写入到配置文件中的 DEFAULT 节中，而是指：PasteDeploy 会从配置文件中将 DEFAULT 节中的 “name = value” 对作为 “key: value” 对放到一个字典（假设为 GlobalConf）中，然后将该选项 global_conf 中的 K-V 对也放到 GlobalConf 字典中`**。

### 2、说明
#### (1) `name`参数 与 `uri` 参数中指定的 App 名字之间的关系。
A. 如果指定了 `name` 参数，就加载它；此时，如果 `uri` 参数中也指定了`App名字`，就忽略它，并把它及分隔符`#`` 一起去掉，即把剩余的部分作为“配置路径”。

B. 如果没有指定 `name` 参数，就使用 `uri` 参数中指定的 `App名字`。

C. 如果既没有指定 `name` 参数，`uri` 参数中也没有指定 `App名字`，就使用默认值 “`main`” 作为 App 的名字。

#### (2) `relative_to` 参数与 `uri` 参数中指定的“`配置路径`”之间的关系。
如果 `uri` 参数中指定的“`配置路径`”是绝对路径，则忽略 `relative_to` 参数；否则，必须提供该参数，`uri` 参数中指定的配置路径则相对该参数所指定的路径。

### 3、工厂
`loadconfig`主要是获取配置文件中指定的参数的，而其它三个都要是用来加载一个可调用对象的。因此，`PasteDeploy` 中主要有三种类型的可调用对象：`WSGI Application`、`Filter`、`Server`。

`PasteDeploy` 使用了《设计模式》中的“工厂模式”，为三个可调用对象建立了一些工厂（Factory）：
```python
paste.app_factory(global_conf, **local_conf)     # (1)
paste.filter_factory(global_conf, **local_conf)  # (2)
paste.server_factory(global_conf, **local_conf)  # (3)
```

为了便利，作为辅助，PasteDeploy 也定义了以下工厂：
```python
paste.filter_app_factory(wsgi_app, global_conf, **local_conf)  # (4)
paste.server_runner(wsgi_app, global_conf, **local_conf)       # (5)
paste.composite_factory(loader, global_conf, **local_conf)     # (6)
```

下面简单的说明一下这些工厂，具体的请参见 `PasteDeploy` 的 [官方文档](http://pythonpaste.org/deploy/#defining-factories)。

    (1) paste.app_factory 返回一个符合 WSGI 协议接口的 Application。
    (2) paste.filter_factory 返回一个过滤器，该过滤器的参数仅有一个，就是 WSGI Application，即 paste.app_factory 的返回值；
        同时，这个过滤器也要返回一个WSGI Application。
    (3) paste.server_factory 返回一个服务器可调用对象（其参数同过滤器）；当调用它时，就会启动一个服务器。
    (4) paste.filter_app_factory 返回一个带有过滤器的 WSGI Application，同时也要返回一个WSGI Application；
        可以看成是 paste.app_factory 和 paste.filter_factory 的接合。
    (5) paste.server_runner 同 paste.server_factory，但它要求HTTP服务器必须立即运行，不允许推迟；
        而且它还需要接受一个WSGI Application作为第一个参数。
    (6) paste.composite_factory 是一个复合工厂，自定义它时，会得到一个 Loader 实例，可以加载上述的各种可调用对象。
注：Paste 中有一个自定义的 `paste.composite_factory`（即 `paste.urlmap.urlmap_factory`），它返回一个 `URLMap` 实例。此工厂的作用完成一个 `URL` 分发，即`不同的 URL 可以对应不同处理器（Handler）`。

### 4、例子
#### (5) 定义一个服务器工厂
```python
def server_factory(global_conf, host, port):
      port = int(port)
      def serve(app):
            s = Server(app, host=host, port=port)
            s.serve_forever()
      return serve
```

#### (2) 配置样例
```ini
[composite:main]
use = egg:Paste#urlmap
/ = home
/blog = blog
/wiki = wiki
/cms = config:cms.ini

[app:home]
use = egg:Paste#static
document_root = %(here)s/htdocs

[filter-app:blog]
use = egg:Authentication#auth
next = blogapp
roles = admin
htpasswd = /home/me/users.htpasswd

[app:blogapp]
use = egg:BlogApp
database = sqlite:/home/me/blog.db

[app:wiki]
use = call:mywiki.main:application
database = sqlite:/home/me/wiki.db
```

#### (3) 小样例
```python
### app.py
from webob import Response
from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp

@wsgify
def application(req):
    return Response('Hello World')

@wsgify.middleware()
def my_filter(req, app):
    # just print a message to the console
    print('my_filter was called')
    return app(req)

def app_factory(global_config, **local_config):
    return application

def filter_factory(global_config, **local_config):
    return my_filter

wsgi_app = loadapp('config:/root/paste.ini')
httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)
```

```ini
### paste.ini
[pipeline:main]
pipeline = myfilter myapp

[app:myapp]
paste.app_factory = app:app_factory

[filter:myfilter]
paste.filter_factory = app:filter_factory
```

#### (4) Openstack项目中的样例
```python
### keystoneclient/middleware/auth_token.py
class AuthProtocol(object):
    """Auth Middleware that handles authenticating client calls."""
    def __init__(self, app, conf):
        pass

    def __call__(self, env, start_response):
        """Handle incoming request.
        Authenticate send downstream on success. Reject request if we can't authenticate.
        """

def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)
    def auth_filter(app):
          return AuthProtocol(app, conf)
    return auth_filter

def app_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    return AuthProtocol(None, conf)
```

```python
### factory.py
def root_app_factory(loader, global_conf, **local_conf):
    if not CONF.enable_v1_api:
        del local_conf['/v1']
    if not CONF.enable_v2_api:
        del local_conf['/v2']
    return paste.urlmap.urlmap_factory(loader, global_conf, **local_conf)
```

```ini
### glance_paste.ini
[composite:rootapp]
paste.composite_factory = glance.api:root_app_factory
/: apiversions
/v1: apiv1app
/v2: apiv2app
```

## 附录

关于如何编写配置文件，请参见 [官方文档](http://pythonpaste.org/deploy/#id8)。
