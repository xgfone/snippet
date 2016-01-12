
不常用的特性
=========

## 字节对齐

（1）GO1 语言规范将保证下面的最小字节对齐特性：

    A. 对于任何类型的变量 x： unsafe.Alignof(x) 至少是 1。
    B. 对于一个struct类型变量 x：unsafe.Alignof(x) 是 x 的所有域（假设为f）中 unsafe.Alignof(x.f) 最大的，但至少为 1。
    C. 对于一个数组类型的变量 x：unsafe.Alignof(x) 和 unsafe.Alignof(x[0]) 相同，但至少为 1。

（2）如果一个 `struct类型` 没有包含任何域，或者包含的所有域的内存大小为`0`，那么此 `struct类型`的大小为0。

（3）如果一个数组没有包含任何元素（即元素个数为0），那么该数组类型的大小为0。

（4）两个大小同为0的不同变量可能拥有相同的内存地址。


GO环境变量
========

由于Go是编译性语言，因此需要安装Go编译器`golang`，不过Go开发团队也为GCC写了编译前端，也就是说，可以安装基于GCC的Go编译器（即`gccgo`）。

在安装好Go编译器后，可以用其编译一些小程序；但如果是想要开发大型程序，还是`Go Tools`的好。Gotool会自动查找、编译程序中`import`的包。为了让Gotool能够找到被导入的包，需要定义一个`GOROOT`和`GOPATH`环境变量，其中，`GOROOT`指向Go的安装位置（其中包含有Go标准库包），如果是使用Linux下的DEB或RPM包，或者Windows下的EXE来安装GO，那么`GOROOT`默认自动设置好，如果是手工编译安装，就有可能需要自己来设置其值了；`GOPATH`是指项目代码所在的位置，换句话说就是，我们创建的GO工程的根目录，其下要有`src`、`pkg`、`bin`等三个目录，Gotool编译好的二进制程序会自动拷贝到`bin目录`下，如果`bin目录`在`PATH`环境变量中的话，就可以在命令行直接通过二进制程序的名字而非绝对路径来运行它。另外，`GOPATH`可以设置成一个`列表`，表示有多个GO工程；如果是Linux或其他符合POSIX标准的系统，列表的分隔符是冒号（`:`），如果是Windows系统，其分隔符就是分号（`;`）。关于`GOPATH`具体的信息，可以参考 http://golang.org/pkg/go/build/ ，或者在命令行执行 `go  help  gopath`，就会打印出关于`gopath`的帮助信息。

因此，在安装好Go编译器之后，通常会需要设置`GOPATH`环境变量；另外，为了能够通过程序名直接执行二进制程序，一般还会设置`PATH`环境变量，即将 `${GOPATH}/bin` 路径加入到 `PATH` 环境变量中，如果是Linux或其他符合POSIX标准的系统中，可以在SHELL的配置文件中添加一行： `PATH=$PATH:${GOPATH//://bin:}/bin`
如果`GOPATH`的值是个列表，上一行会把列表中所有工程目录中的`bin目录`添加到`PATH`环境变量中。

gotools是一套工具集，包括`go`、`godoc`、`gofmt`等命令，不过其他命令可以由`go`通过子命令来调用（如：`go fmt` 将会调用`gofmt`），一般直接使用 “`go 子命令`”即可，比如，要编译并安装程序`helloworld`，可以直接执行 `go install helloworld`。

另外，一旦定义了`GOPATH`环境变量，可以在任何地方运行`go命令`来编译并安装程序，因为`go命令`会自动查找`GOPATH`环境变量，而不需要当前目录。


格式化与自动补全
=============
首先要先安装 `gocode` 和 `godef` 两个包。

### 获取、安装 GoCode
```shell
$ go get -v github.com/nsf/gocode
$ go install github.com/nsf/gocode
```

### 获取、安装 GoDef

(1) 打开 http://gopm.io/download

(2) 下载 `code.google.com/p/rog-go/exp/cmd/godef`，然后解压并放到 `GOPATH` 环境中

(3) 下载 https://github.com/9fans/go ，并放到 `GOPATH` 环境中的 `9fans.net` 目录下，即 `$GOPATH/9fans.net/go`

(4) 安装：`go install code.google.com/p/rog-go/exp/cmd/godef`

注：如果 http://gopm.io/download 无法下载，可以从 http://golangtc.com/download/package 上下载。

**建议：**

直接使用 http://golangtc.com/download/package 下载 `code.google.com/p/rog-go/exp/cmd/godef`，它会自动把依赖包 `9fans.net/go` 也下载下来。
