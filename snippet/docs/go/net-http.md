
Golang net.http标准库
====================

关于`net.http`包`Server`的执行过程，`astaxie`（`beego`、`beedb`等名库的开发者和维护者）给出了下面的 [`说明`](https://github.com/astaxie/build-web-application-with-golang/blob/master/ebook/03.4.md#go%E4%BB%A3%E7%A0%81%E7%9A%84%E6%89%A7%E8%A1%8C%E6%B5%81%E7%A8%8B)：

通过对`http`包的分析之后，现在让我们来梳理一下整个的代码执行过程。

    首先调用 http.HandleFunc (按顺序做了几件事)：
        1. 调用了DefaultServerMux的HandleFunc
        2. 调用了DefaultServerMux的Handle
        3. 往DefaultServeMux的map[string]muxEntry中增加对应的handler和路由规则

    其次调用 http.ListenAndServe(":9090", nil) (按顺序做了几件事情)：
        1. 实例化Server
        2. 调用Server的ListenAndServe()
        3. 调用net.Listen("tcp", addr)监听端口
        4. 启动一个for循环，在循环体中Accept请求
        5. 对每个请求实例化一个Conn，并且开启一个goroutine为这个请求进行服务go c.serve()
        6. 读取每个请求的内容w, err := c.readRequest()
        7. 判断handler是否为空，如果没有设置handler（这个例子就没有设置handler），handler就设置为DefaultServeMux
        8. 调用handler的ServeHttp
        9. 在这个例子中，下面就进入到DefaultServerMux.ServeHttp
        10. 根据request选择handler，并且进入到这个handler的ServeHTTP
            mux.handler(r).ServeHTTP(w, r)
        11. 选择handler：
            A. 判断是否有路由能满足这个request（循环遍历ServerMux的muxEntry）
            B. 如果有路由满足，调用这个路由handler的ServeHttp
            C. 如果没有路由满足，调用NotFoundHandler的ServeHttp

上述是概括性说明，下文笔者将详细描述一下其执行流程。

使用 `net.http` 包时，一般常用的三个函数时：
```go
func Serve(listen net.Listener, handler Handler) error
func ListenAndServe(addr string, handler Handler) error
func ListenAndServeTLS(addr string, certFile string, keyFile string, handler Handler) error
```
后两个函数会先使用 `addr`、`certFile`、`keyFile` 等参数通过 `net` 包来建立一个 `TCP` 监听器`Listener`，然后监听客户端的到来；而第一个则使用已经存在 `TCP Listener`。

上面三个函数的最后一个参数 `handler` 是要注册的处理器 `Handler`，可以为 `nil`；如果为 `nil`，则使用默认的处理器 `DefaultServeMux`。

下面以 `net.http.ListenAndServe` 函数为例进行说明。

**`ListenAndServe`**(addr string, handler Handler)

    1 创建一个Server对象 server = &Server{Addr: addr, Handler: handler}
    2 启动 server.ListenAndServe 方法
        2.1 打开TCP监听器（默认是HTTP，即80端口），即 listen = net.Listen("tcp", addr)
        2.2 调用 server.serve(listen) ——进入死循环：
            2.2.1 等待客户端的到来，rwconn = listen.Accept()
            2.2.2 为新的客户端连接（此连接是net.TCP连接，即上一步的rwconn）建立一个新的连接对象
                （该连接对象是net.http包内建的类型conn，专门为一个客户端进行服务的），
                _conn = srv.newConn(rwconn)
            2.2.3 打开一个goroutine，在其中执行_conn.serve()，即在一个GO例程中为一个客户端进行服务。
                2.2.3.1 处理 TLS 连接
                2.2.3.2 进行死循环，服务客户端的每次请求，即一个完整的请求为一个循环。
                    (1) 读取一个完整的客户端请求（包括请求行、请求头、请求体），并将这些请求信息封装到一个Request对象
                        request中，然后在建立一个response类型（net.http内建类型）的对象resp，并将request对象作为
                        resp.req 的属性值。
                        相关代码：resp = c.readRequest() ;   resp.req = request

                    (2) 调用 serverHandler{conn.server}.ServeHTTP(resp, resp.req)，其意是：创建一个serverHandler
                        类型的对象，并调用它的 ServeHTTP 方法。

                        注：serverHandler是net.http包内建的类型，它只有一个方法 ServeHTTP，我们可以并不关心这个类型，
                            只需要关心在它的这个方法中做了些什么即可。

                        A.  该方法首先检查：在创建Server对象时，是否注册过一个处理器 Handler，如果注册过，则使用
                            注册的处理器；否则，使用默认处理器 DefaultServeMux。
                        B.  调用 Handler.ServeHTTP(resp,  resp.req)

                        注：DefaultServeMux 是定义于 net.http 模块的全局变量（ServeMux类型的），它实现了Handler
                            interface（即具有 ServeHTTP 方法），它的主要功能就是实现了一个简单的 URL 路由器——根据URL
                            来将请求分发到不同的 Handler 上，即根据不同的URL，来执行不同的 Handler。

                        除了使用默认的 Handler（DefaultServeMux）外，也可以实现自己的 Handler，只要这个自定义 Handler
                        类型拥有 ServeHTTP 方法即可（即实现了 Handler interface 接口）。如果提供了自己的 Handler，
                        则需要实现者自己实现其处理逻辑，比如：路由（可以实现更强大的路由，DefaultServeMux 实现的路由
                        比较简单，看下文）。从这可以看出，通过这个 Handler 处理器可以实现 RESTfull API。

                        为了便于理解，根据其功能，我们在此把此 Handler 处理器看成是路由，即 route_handler，
                        与下文的另一个处理器进行区别，且下文的 route_handler 一律指代此处理器；另外，除非特殊说明，
                        Handler 不再指代此处理器，如果出现了，则指代其它类型的处理器。

                        下面介绍 DefaultServeMux 到底做了什么，即其处理流程是什么。

                        DefaultServeMux.ServeHTTP(resp, resp.req) 的执行流程（下文以route指代DefaultServeMux）：
                            (1) 根据 Host 和 Path（即URL请求路径）来查找一个 Handler。查找规则模式匹配字符患必须
                                完全匹配请求的主机（如果设定）和路径的前几个字符串，即请求路径的前几个字符串必须
                                和模式匹配字符串完全相同，比如：请求路径 /hello/world 匹配模式字符串 /hello，但
                                不匹配 /bye。如果查找不到一个 Handler，则返回一个 NotFoundHandler 处理器对象
                                （net.http包内建的）。调用链是：
                                route.Handler(...) ->route.handler(...) -> route.match(...) -> pathMatch(...)
                            (2) 调用 Handler.ServeHTTP(resp, resp.req)

                        注：此处的 Handler 与上文的 route_handler 不同，此 Handler 是必须包含在 route_handler
                        中的。另外，这个处理器 Handler 是用户必须定义的接口，它必须有一个 ServeHTTP(resp,  resp.req)
                        方法，即只要符合这个方法就符合这个接口，这和 route_handler 的 interface 一样，因为它们都是
                        Hanler，只是处理问题不一样罢了：route_handler 处理像 URL 路由这类的，而此 Handler 处理相关
                        的 URL 的，即处理具体的某一个URL网页的请求，因此，可以将些 Handler 看作是 url_handler。

                        再次明确一点，上文提到的 route_handler 和 url_handler 都是 Handler，它们有相同的 interface，
                        即 ServeHTTP 方法；但它们处理的问题不同，一个是处理像路由这种问题的，一个是处理具体的某一个
                        URL 网页请求。

                    (3) 结束本次请求， resp.finishRequest()

                    (4) 如果不是 KeepAlive 或者连接已经关闭（如客户端断开连接），则关闭服务端的连接
                        (关闭Write，此后就不能再进行向客户端发送数据)，并跳出死循环，这意味着当前的 goroutine
                        将终止、退出。如果是 KeepAlive 并保持连接，将进入下一个循环，等待并读取下一个请求。


## 备注

如果可以不编写 `route_handler`，但必须编写 `url_handler`，此时，默认使用 `DefaultServeMux` 作为默认的 `route_handler`，并且 `url_handler` 将会被注册到 `DefaultServeMux` 中。

### 1、自定义`route_handler`

    一旦编写并注册 route_handler，则实现者必须自己实现其处理逻辑。另外，一个 Server 对象只能有一个 route_handler，
    但一个 route_handler 可以有多个 url_handler。

### 2、使用 `DefaultServeMux` 作为 `route_handler`。

#### （1）如何编写并注册一个 `url_handler`？
答：有两种方法：

**`第一种：`**写一个 `struct`，并为这个类型附加一个 `ServeHTTP` 方法，然后将这个 `url_handler` 注册到 `DefaultServeMux` 中。如：
```go
type HelloHandler struct {};
func (*HelloHandler) ServeHTTP(w http.ResponseWrite, r* http.Request) {
    // 做一些处理
}
http.Handle("/hello", HelloHandler{})   // 注册一个 url_handler
```

**`第二种：`**编写一个函数，它和 `ServeHTTP` 方法具有相同的参数和返回值（包括个数、类型和顺序），然后将其注册到 `DefaultServeMux` 中。如：
```go
func HelloHandler(w http.ResponseWrite, r* http.Request) {
    // 做一些处理
}
http.HandleFunc("/hello",  HelloHandler)
```

在这种方法下，`http.HandleFunc` 会在 `HelloHandler` 函数外包装一个 `ServeHTTP` 方法，该方法不做其他的事，仅调用该函数处理器。其具体做法是：`http` 模块定义了一个 函数型的类型，然后为它附加一个 `ServeHTTP` 方法，在实例化该类型的对象`handler`时，是把此处理器函数作为参数来实例化它的；由于 `handler` 的类型是函数型的，且用的是函数处理器实例化的，因此，可以认为 `handler` 就是此函数处理器；又因为 `handler` 是一个类型`type`，且它有一个 `ServeHTTP` 方法，所以， `handler` 有两种操作： `handler.ServeHTTP(...)` 和 `handler(...)`，它们的参数是一样的，前者调用一个自身的方法，后者自身作为一个方法来调用，而前者的主体就是仅仅调用后者。

#### （2）启动Server时，如何使用默认的 route_handler（即 DefaultServeMux）？
答：在调用 `http.Serve`、`http.ListenAndServe` 和 `http.ListenAndServeTLS` 时，指定`Handler`为 `nil`；或者实例化 `http.Server` 对象时，不指定 `Handler` 属性或指定为 `nil`。如果 `Server` 对象的 `Handler` 属性最终不为 `nil`，则使用指定的 `Handler`。

### 3、间接路由处理器 indirect_route_handler。

从前面知道，不管是 `route_handler`，还是 `url_handler`，它们都有是 `Handler`，都有相同的 `interface` —— `ServeHTTP` 方法。其实在 `route_handler` 和 `url_handler` 之间，我们还可以运用间接路由器，具体地做法时，再写个 `indirect_route_handler`，然后注册到 `route_handler` 中，最后把 `url_handler` 注册到 `indirect_route_handler` 中。关于 `indirect_route_handler` 的注册，用户可以自己定义，当然也可以参考 `DefaultServeMux` 的实现。这种间接路由器的一般作用是将不同的`URL`进行划分，可以把不同的`URL`划分到不同的组，而不同的组有不用不同的前缀来表示，并且每个组有一个间接路由器。

这种方法比较麻烦，用处不是特别大，也很少使用。一般 `Server API` 简单时，使用默认的`Handler`（即`DefaultServeMux`）就可以了；如果功能比较多、复杂，一般使用控制器路由处理器比较方便些。控制器路由方式最早应该是由 `Ruby On Rails` 框架实现了，其它语言也逐渐地实现了这样功能的库，比如：`Python`下比较有名的是 `Routes`。
