
GO标准版本的主要变化
=================

# Go1

## 1、多赋值
Go语言支持`多值赋值`，但对于赋值操作符（即等号）左边的变量的计算，是在任何变量被赋值之前被完成，其计算顺序是`从左到右`，一旦计算完，则开始从左到右依次对每个变量进行赋值。如：
```go
sa := []int {1,2,3}
i := 0
i, sa[i] = 1, 2   //  sets i = 1, sa[0] = 2

sb := []int {1,2,3}
j := 0
sb[j], j = 2, 1   // sets sb[0] = 2, j = 1

sc := []int{1,2,3}
sc[0], sc[0] = 1, 2 // sets sc[0]=1, then sc[0]=2 (so sc[0]=2 at end)
```

## 2、相等比较
`struct`和`array`可以进行比较是否相等了，但`函数`和`map`不再支持相等比较了，除了它们`nil`值的比较。

## 3、struct初始化
在初始化`struct对象`时，最好指明`field字段名`，这是向后兼容的，当前也支持直接给初始值，但这并不保证能向后兼容，这个特性也有可能在后续的某个版本中被移除。


# Go1.1

## 1、语言改变
在`GO1`中，整数除以0将导致引发一个运行时“恐慌”（a run-time panic）。

在`GO1.1`中，这将是一个非法程序，是个编译时错误，即在编译时报错，无法通过编译。

## 2、方法值（Method Values）
`GO1.1`实现了`方法值（method values）`，它能绑定到一个指定的接收者上，即可以将一个函数附加到一个`struct`上，从而让此函数成为该`struct`的一个方法。

### 方法值
如果一个表达式X有一个静态类型T，并且M位于类型T方法集中，那么x.M就叫做方法值。
如：
```go
type  T struct {   a  int   }
func (tv  T) Mv(a int) int { return 0}          // value receiver
func (tp *T) Mp(f float32) float32 {return 1}   // pointer receiver
var t T
var pt *T
func makeT()  T
```
### 说明
（1）表达式 `t.Mv` 将产生类型为 `func(int) int` 的函数值。

（2）`t.Mv(7)`` 和 `f:=t.Mv; f(7)`` 是等式价的。

（3）表达式`pt.Mv`将产生类型为 `func(float32) float32` 的函数值。

具体参见语言规范中的“`Method Values`”一节。

## 3、return返回值
在`GO1`中，一个具有返回值的函数必须显示的执行`return`或调用`panic函数`。但在`GO1.1`中，这不必要的。但为保证函数在返回时能有个返回值且可以省略`return`，`GO1.1`引入了一个“`终止语句`”（`terminating statement`）的概念，它是一个能够保证是最后一个函数执行语句的语句。比如：for死循环（死循环一般表示是永不停止，一旦停止表示程序结束，注：这仅一般意义，死循环并不是真正的死循环，比如程序可以跳出死循环）。关于“`终止语句`”的详细信息请参见“`语言规范`”。

总之一句话，_**如果一个函数有返回值，则它必须明确返回一个值，它不像Python语言，如果没有return，默认返回None**_。

## 4、int 和 int32
在`GO1`中，在所有的系统中，`int`和`uint32`都有是`32位`的。但在`GO1.1`中，`int`和`uint32`都有是`64位`的。

## 5、堆大小
在`64位系统`中，相对`GO1`，`GO1.1`的堆大小从`GB`增大到`TB`级；而在`32位系统`中，堆大小并没有改变。

## 6、go get 命令
从`GO1.1`开始，`go get` 命令下载的源码包不再默认放到 `$GOROOT` 环境变量指向的目录中，而使用 `$GOPATH` 所指向的目录列表中的第一个目录中。另外，从`GO1.1`开始，`go` 工具链不再允许 `$GOPATH` 和 `$GOROOT` 设置成相同的值。

## 7、支持系统和平台
相对`GO1`，`GO1.1`支持更多的系统和平台。另外，在`GO1.1`中，`go tool` 默认取消 `cgo` 的支持，但可以设置 `CGO_ENABLED=1` 来显示地启用 `cgo`。

## 8、性能
`Go1.1`比`GO1`有了更大的性能提升，大约在 `30%~40%` 左右；垃圾回收器也已经做到了更大程序上并行处理。

## 9、time 包精度
`Go1`中，`time包`只能达到`微秒精度（microsecond precision）`；而在`GO1.1`中，`time包`能达到`纳秒精度（nanosecond precision）`。


# Go1.2

## 1、nil 指针
为了安全的考虑，从`Go1.2`开始，`nil` 指针的一些使用会被保证触发一个运行时“`恐慌`”（a run-time panic）。如：
```go
type T struct {
    X  [1<<24]byte
    Field  int32
}
func main() {
    var x *T
    ...
}
```
由于 `x` 变量没有初始化值，因此默认初始化为 `nil`。但在`Go1.2`之前，这个 `x` 变量能够以不正确的访问方式来访问内存：表达式 `x.Field` 能够访问地址为 `1<<24` 处的内存。为了阻止这个不安全的行为，在`Go1.2`中，编译器将保证 `nil` 指针的任何间接性的非法操作都将会引发一个“`panic`”或返回一个正确并安全的`non-nil`值。

总之一句话，_**任何显式或隐式地需要计算一个nil地址的表达式都是错误的**_。

## 2、三索引分片
从`GO1.2`开始，允许`三索引分片（Three-index slice）`：可以在分片操作中指定第三个索引，以表明新产生的分片是容量。如：
```go
var array [10]int
slice := array[2:4]
```
上述分片`slice`变量的容量是`8`，即从底层数组的第三个元素（因为数组下标从0开始）开始一直到最后，但是该分片变量`slice`能使用的只有其中的两个，除非使用内建的`append`函数来增加其使用量。

如果想指定分片`slice`的容量，在`GO1.2`中，可以在分片中指定第三个索引，该索引指定终止索引位。如：
```go
slice := array[2:4:7]
```
此时，`slice`的容量将是`5（7-2）`，其容量是`底层数组的第三个到第七个（包含第七个）`，即`底层数组的索引是2~6`，但是同上述一样，默认能使用的也只是2个，要想增加使用量，需要使用内建函数append来追加元素。

三索引的意思：

    第一个索引表示容量或能使用的底层数组的开始索引，
    第二个索引表示默认能使用的终止索引（不包含它，即整体是半开半闭区间），
    第三个索引表示其容量的终止索引（不包含它，即整体是半开半闭区间）。

目前的实现是：

    第一个索引可以省略，如果没有指定，则默认为0，但其他两个必须显示指定，然后将来的实现可以会为其引入一个默认值。
    第三个索引的值必须小于或等于产生新分片的源数组或源分片的容量，
    比如：上述例子中的第三个索引就不能指定为大于10的值，因为该数组的空间最大才是10个元素。

具体细节请参见“`语法规范`”。

## 3、goroutine和线程
在`GO1.2`之前，当通过`GOMAXPROCS`来设定只有一个用户线程时，一个永久循环（或死循环）的`goroutine`会使在同一线程中的其他`goroutine`因资源枯竭（如永远得不到CPU）而“死亡”（并不是真正的死亡、终结，而是因为永远得不到调度，名存实亡）。在`GO1.2`中，这种情况得到了缓解，或者说是部分解决，即GO调度器会偶尔地调度那些“名存实亡”的goroutine，使其“名存实存”。

为了避免在一些环境中导致资源枯竭，`GO1.2`引入了一个可配置的限制（默认是`10000`）来限制一个单独程序在它的地址空间中所能使用的线程总数。由于`goroutine`是`多路复用在线程上`的，所以这个限制并不直接限制`goroutine`的数量，而仅仅是同时被阻塞在一个系统调用上的数量。

## 4、栈大小
在`GO1.2`中，增大了GO例程栈的大小，能够减少栈溢出。

    在32位系统上，默认大小是250M；
    在64位系统上，默认大小是1GB。

## 5、包
`GO1.2`要求在每个包中的每个文件中必须明确通过 `package` 语句指定其包名。

## 6、Go工具链
（1）在`GO1.2`中，`cgo`可以调用C++编译器构造的C++代码链接库了。

（2）在`GCC4.8.2`版本中，`gccgo`只实现到 `Go1.1.2`；有望在 `GCC4.9` 版本中完全支持 `GO1.2`。

（3）在`GO1.2`中，`go get` 命令新增了 `-t` 标志，它在下载一个包时，同时也会下载该包的依赖包。

## 7、Go标准库
（1）在`GO1.2`中，部分标准库包得到了优化，性能提高了将近 `30%` 左右，如：`comress/bzip2`、`crypto/des`、`encoding/json`以及网络通信包。

（2）在`GO1.2`中，标准库包 `fmt` 中的格式化输出例程允许为输出数据指定索引操作，以便以任意的顺序来访问输出数据。如：
```go
fmt.Sprintf("%[3]c %[1]c %c", 'a', 'b', 'c')
```
其结果是 "`c a b`"。

（3）在`Go1.2`中，标准库 `text/template` 和 `html/template` 包新增了一些比较函数，如：`eq`、`ne`、`lt`、`le`、`gt`、`ge`等。

注：这些比较函数和相应的GO操作符不同。

    其一，这些函数只能比较基本类型，如：bool、int、float64、string等等；
    而GO操作符除了能比较基本类型外，还能比较数组和结构体struct。

    其二，只要它们的值有相同的分类（注：所有的整数都是一类的，而不管其表示位数），那么它们就能直接进行比较操作；
    然而，Go操作符却不允许，如：GO不允许int8和int16直接进行比较操作，必须先进行类型转换。

（4）在`Go1.2`中，标准库 `text/template` 和 `html/template` 包也新增了 `{{else if}}`` 语法。如：
```go
{{if  eq  .A  1}}  X  {{else}}  {{if  eq  .A  2}}  Y  {{end}}  {{end}}
```

在`GO1.2`中，可以简写成：
```go
{{if  eq  .A  1}}  X  {{else  if  eq  .A  2}}  Y  {{end}}
```
二者是等效的，仅仅是语法不同罢了。


# Go1.3

## 1、总体变化
在语言规范没有作任何改变。此版本的改变主要聚焦在实现上，如更加精确的垃圾回收机制、编译工具链的重构（以提高构建速度）、性能的提升以及更多平台的支持。在兼容性上，与之前的版本完全兼容。

## 2、内存模型变化
主要增加了一条新的规则，此规则会影响到缓冲区管道（Buffered Channels）的发送和接收。

## 3、栈（Stack）
Goroutine Stack的实现由段（Segmented）模型改变成邻近（Contiguous）模型。

## 4、垃圾回收器
从Go1.3开始，运行时假定指针类型的值包含指针，而其它类型的值则不会。因此，使用 `unsafe` 包在一个指针类型变量中存储整数为非法操作；如果运行时侦测到此行为，程序将会崩溃。同样的，使用 `unsafe` 包在一个整数类型变量中存储指针也为非法操作，但是，此行为在执行期间很难被诊断。

与以前代码不兼容的之处：不能使用 `unsafe.Pointer`，将一个整型类型变量转换成一个指针，否则，将产生一个非法操作。

## 5、Map迭代
此版本之前，Go规范规定，不大于8个元素的小Map在迭代时，其迭代顺序是有序的，但对于大Map，是无序的。
从Go1.3开始，小Map上的迭代也不再有序，而是随机的。

**备注：**

Go 1 标准规范规定：_**在Map上的迭代是无序的，前后两次的迭代顺序并不保证一致**_。
直到 Go 1.3 才真正实现了这一规范。


# Go1.4

## 1、For-range Loop
新增一种格式：
```go
for expr1 = range expr2 {  statements }
```
具体见上面For语句。

## 2、`**T` 的方法调用
Go规范不再允许双引用，而只允许单引用。

## 3、运行时
（1）大部分代码用Go语言重写，并且有更高的精度和消耗更小的堆空间。

（2）栈完全取消段模型。

（3）修改了 interface 的实现。


# Go1.5

## Map字面值
从 Go 1.5 开始，Map字面值中元素的类型可以被省略。如：
```go
// Before 1.5
m := map[Point]string{
    Point{29.935523, 52.891566}:   "Persepolis",
    Point{-25.352594, 131.034361}: "Uluru",
    Point{37.422455, -122.084306}: "Googleplex",
}

// Since 1.5
m := map[Point]string{
    {29.935523, 52.891566}:   "Persepolis",
    {-25.352594, 131.034361}: "Uluru",
    {37.422455, -122.084306}: "Googleplex",
}
```

## 开发实现
（1）除了额外的一小部分汇编外，编译器完全用 Go 重写。

（2）GC是并发的，并且在执行GC时，减少了整个程序的暂停时间：被限制在 10ms 以内，有时会更少。

（3）默认地，GOMACPROCS被设置到可见到的CPU核数。先前版本被默认设置到 1。

（4）Go 工具链开始试验性地支持包的版本依赖。

## 移植性
一些老的平台和系统版本不再支持。

## 工具链
（1）新增 `go tool trace` 命令，可进行细粒度地追踪程序的执行。

（2）新增 `go doc` 命令（与 `godoc` 不同）。

（3）编译器（`6g`、`8g`等）、汇编器（`6a`、`8a`等）和链接器（`6l`、`8l`等）被废弃，分别内建到 `go tool` 工具链中（`go tool compile`、`go tool asm`、`go tool link`）。如：
```shell
$ export GOOS=darwin GOARCH=amd64
$ go tool compile program.go
$ go tool link program.o
```


# Go1.6

## 移植
新增一些平台的支持：`Linux on 64-bit MIPS`、`Android on 32-bit x86`等。

## CGO
定义在 C 中共享 Go 指针的规则，以确保 C 语言代码和 Go 的 GC 可以共存。简单地说，Go 和
C 可以共享由 Go 分配的内存，即指向该内存的 Go 指针可通过作为 CGO 调用的一部分传递给 C。但是，该内存本身不再属于Go分配的内存；同时，调用返回后，C不再保留该指针。这些规则在程序执行中由运行时负责检查：如果运行时检测到违规，它会打印诊断信息并使程序崩溃。

## 性能
Go1基准测试套件比 Go1.5 更快了，GC停顿时间比 Go1.5 更短了。

对部分标准库进行了优化，带来了超过 10% 的性能提升，如：`compress/bzip2`、`compress/gzip`、`crypto/aes`、`crypto/elliptic`、`crypto/ecdsa`、`sort`等。

## 标准库
`net/http` 包透明地支持全新的 `HTTP/2` 协议。Go的客户端和服务器在使用 `https` 时将自动使用 `HTTP/2`。Go中并没有特定的可导出的 API 来处理 `HTTP/2`，就像没有特定的可导出 API 来处理 `HTTP/1.1` 一样。不过，程序可通过导入 `golang.org/x/net/http2` 包来调整`HTTP/2`的细节,特别是它的`ConfigureServer`和`ConfigureTransport`函数。


# Go1.7

除了一个小的语言规范方面的改变外，大部分改变都是关于工具链（toolchain）、运行时（runtime）和库（libraries）。

从 1.7 开始支持 `SSA`，CPU 性能将提升 5% ~ 35% 左右。

## 语言规范
1.7 之前：

    A statement list ends in a terminating statement if the list is not empty and
    its final statement is terminating.

1.7 中：

    A statement list ends in a terminating statement if the list is not empty and
    its final non-empty statement is terminating.

即：1.7 中多了个 `non-empty` 词，强调语句列表中的最后一个语句必须是 `非空的`。


# Go1.8

## 语言规范
1. 当把一个值从一个类型转换到另一个类型时，tags 将被忽略。也就是说，只有 tags 不同的两个结构体可以互相转换。
2. 语言规范现在最低要求实现支持 16 位（16-bit）指数的浮点常量。注：这并不影响 `gc` 或 `gccgo`，因为它们仍都支持 32 位(32-bit)指数。

## 移植
1. 在 Linux 大小端上，现在支持 32 位 MIPS。另外，对 ARMv5E 和 ARMv6 处理器，Go 1.8 是最后一个支持 Linux 的版本。从 Go 1.9 开始，至少要求 ARMv6K 及以后的处理器。

## 工具

1. 在 64-bit x86 和 PPC 系统上，添加一些汇编指令。
2. 从 Go 1.7 开始，Go 编译器已不再使用 Yacc 工具； 因此，从 Go 1.8 开始，Yacc 工具已经被移除。
3. 新的编译器后端将产生更加简洁、有效的代码，并提供更好优化，如边界检查消除。
4. 相比于 Go 1.7，编译器和链接器被优化地更快，快了大约 15%。
5. `GOPATH` 现在有了一个默认值了，在 Unix/Linux/Mac 上是 `$HOME/go`，在 Windows 上是 `%USERPROFILE%/go`。
6. 新增 `go bug` 命令。
7. 现在已初步开始支持 `plugin`（即可以将软件包构建为一个插件，然后通过标准库 `plugin` 包在运行时加载），但目前只支持 Linux 系统。

## 运行时
1. 提升对 Map 并发误用的侦测，并给出更详细的信息。

## 性能
1. 垃圾回收停顿时长比 Go 1.7 明显更短，通常在 100 us 以下，甚至达到 10 us，Go 1.9 会做更多优化工作。注：Go 1.6 和 1.7 的垃圾回收停顿被控制在 10 ms 以下。
2. `defer` 函数调用的开销 **降低** 了一半。
3. 从 `Go` 到 `C` 的调用开销也 **降低** 了一半。

## 标准库
1. 在标准库的很多包中添加了样例。
2. `sort` 包中添加三个便捷函数 `Slice`、`SliceStable`、`SliceIsSorted`。
3. `net/http` 包添加 `HTTP/2 Push` 机制。
4. `net/http` 已经支持 **优雅关闭** Socket 机制（通过 `Server.Shutdown` 方法）和 **立即关闭** Socket 机制（通过 `Server.Close` 方法）。*外部参考：* https://github.com/Scalingo/go-graceful-restart-example.
5. 一些标准库支持 `context.Context` 参数，如：`Server.Shutdown`、`database/sql`、`net.Resolver`，等等。
6. 添加对 `Mutex` 争用的 `profile`。
7. 其它一些标准库的改变。*参见：*https://golang.org/doc/go1.8#minor_library_changes。


# Go1.9

## 语言规范
主要有两个改变：
1. 支持类型别名。语法格式：`type T1 = T2`，这表示 `T1` 是类型 `T2` 的别名，它们拥有相同的底层类型。关于 `类型别名` 的设计，请参见 [这里](https://github.com/golang/proposal/blob/master/design/18130-type-alias.md)。
2. 实现可以多个浮点操作联合到单个混合操作。比如：某些架构可以提供 FMA（Fused Multiply and Add）指令，在不四舍五入 `x*y` 的中间结果的情况下，计算 `x*y + z` 的值。

## 移植
在这次的发行版中，没有添加新的操作系统或处理器架构支持。

**特别注意：** 在 FreeBSD 中，有一些众所周知的问题会导致整个程序突然崩溃，但目前还不知具体原因。具体参见 [这里](https://github.com/golang/go/issues/15658)。注：当你再看到这篇文章时，这个问题有可能已经被解决了，但截止到 Go 1.9 的发布时，还没找到原因。

## 工具

### 并发编译
Go 编译器现在可以并发地编译包中的函数，以便充分利用多核。并发编译功能默认是被打开的，但可以通过设置环境变量 `GO19CONCURRENTCOMPILATION` 为 `0` 来关闭它。

### Vendor 匹配 `./...` 的问题
在 `import` 一个 `./...` 格式的包时，再不匹配 `vendor` 目录中相应的包。为了匹配 `vendor` 中相应的包，请使用 `./vendor/...` 格式。

### 迁移 `GOROOT`
`go tool` 将要通过它调用的路径来试图定位 Go 的安装路径。

### 编译器工具链
复数的除法现在兼容 C99 标准。

### `pprof`
被 `runtime/pprof` 产生的性能剖析信息现在已经包括符号信息了。

## 性能
由于 GC 的速度提升、产生更好的代码以及核心库的优化，因此，大部分程序应该运行的更快一点了。


# Go1.10

## 语言规范
语言规范上并没有重大的改变。但有两个小的改变：

1. 对于一个未类型化(untyped)的常量，索引操作支持其`左移`/`右移`操作符。如：对于未类型化的常量 s，x[1.0 << s] 是合法的表达式。
2. 放松了方法表达的限制，允许任意类型的表达作为接收者。注：编译器早已实现，此次只是更新语言规范的文档。

## 移植
1. 没有新的操作系统或处理器被支持。
2. FreeBSD 最低版本要求 10.3。
3. NetBSD 最低版本要求 8。
4. OpenBSD 最低版本要求 6.0，且是最后一个支持 6.0 的版本。Go 1.11 最低要求 OpenBSD 6.2。
5. Mac OS X 最低要求 10.8，且是最后一个支持 10.8 和 10.9 的版本。 Go 1.11 最低要求 Mac OS X 10.10。
6. Windows 最低要求是 XP，且是最后一个支持 XP 和 Vista 的版本。Go 1.11 最低要求 Windows 7。


# Go1.11

## 移植
1. OpenBSD 最低版本要求 6.2。
2. Mac OS X 最低版本要求 10.10 Yosemite。
3. Windows 最低要求是 Windows 7。
4. 构建模式 `c-shared` 和 `c-archive` 现在已支持 `FreeBSD/AMD64`。
5. 实验性支持 `WebAssembly`：编译后的文件大小，最小为 2MB，压缩后为 500KB；另外，Go 程序可以通过包 `syscall/js` 来调用 JS，但目前只支持测试。

## 工具
1. Go 开始初步支持 `modules`。
2. 由于 `@` 符号对 Go `modules` 有特殊的意义，因此，不允许在导入路径中包含 `@` 符号。
3. 一个新的包 `golang.org/x/tools/go/packages` 提供一个简单的 API 用来定位和加载 Go 源码包。但它还不能完全支持 `modules`，暂时还没有成为标准库的一部分。
4. Go 1.11 是最后一个可以通过环境变量 `GOCACHE=off` 来禁用构建缓存（由 1.10 版本引入）的版本，从 1.12 版本开始，构建缓存是必须的。
5. Go 1.11 也是最后一个支持 `godoc` 作为命令行工具的版本，将来 `godoc` 仅作为一个 Web 服务，应当使用 `go doc` 以代替 `godoc`。
6. 编译器默认允许更多的函数进行内联，包括调用 `panic` 的函数。
7. 编译器（包括 `go` 和 `cgo`）不再允许 `switch guard` 中声明未使用的变量。如：
```go
func f(v interface{}) {
	switch x := v.(type) {
	}
}
```

## 运行时
Go 现在使用稀疏堆，因此，Go 堆空间的大小不会再有限制（之前被限制在 512GiB 以内）。

对于 `MacOS` 和 `iOS` 系统，Go 运行时将使用 `libSystem.dylib` 来代替直接调用内核，这会让 Go 二进制程序更容易兼容未来的 `MacOS` 和 `iOS` 版本。但 `syscall` 包仍是直接做系统调用。

## 性能

编译器会优化如下操作：
```go
for k := range maps {
    delete(maps, k)
}
```

编译器也会优化形式 `append(s, make([]T, n)...)` 的分片扩展。

编译器还会优化一些边界检查。比如：编译器如果识别到 `i<j` 且 `j<len(s)`，就不会对 `s[i]` 做边界检查。


# Go1.12

大部分改变都聚焦在工具链、运行时和库。

## 语言变化
无。

## 移植

1. 数据竞争侦测当前已支持 `linux/arm64` 架构。
2. Go1.12 是最后一个支持 `FreeBSD 10.x` 的版本，下一个版本将要求 `FreeBSD 11.2+/12.0+`。
3. Cgo 当前已支持 `linux/ppc64` 架构。
4. `hurd` 被 `GOOS` 保留为 `GNU/Hurd` 系统。
5. `windows/arm` 已可以运行在 32 位 ARM 的 Windows 10 IoT Core 系统上。
6. Go1.12 是最后一个支持 `macOS 10.10 Yosemite` 的版本，下一个版本将要求 `macOS 10.11 EI Capitan` 及以上。

## 工具

1. `go tool vet` 不再被支持。请使用 `go vet` 以代替。
2. Go1.12 是最一个支持 `binary-only` 包的版本。
3. Go1.12 将 C 类型 `EGLDisplay` 译成 Go 类型 `uintptr`。
4. `GO111MODULE` 被设置为 `on`。
5. 在 Go1.12 中，`godoc` 仅仅是一个 Web 服务器，不再提供命令行接口。同时，Go1.12 也是最后一个包含 `godoc` 二进制的版本，从下一个版本开始，`godoc` 二进制命令须要通过 `go get` 来获取。

## 运行时

`runtime.Caller` 和 `runtime.Callers` 不再包含编译器产生的初始化函数；其它的没有太大的变化，总体来说，就是性能又有所提升。

## 核心库

1. Go1.12 可以通过设置环境 `GODEBUG` 为 `tls13=1` 来选择性地支持 TLS 1.3。


# Go1.13

## 语言变化
1. 前缀 `0b` 或 `0B` 表示一个二进制整数字面值。
2. 前缀 `0o` 或 `0O` 表示一个八进制整数字面值。
3. 前缀 `0x` 或 `0X` 除了可以表示一个十六进制整数字面值外，还可以表示一个十六进制的浮点数字面值，其中，指数部分不能省略（跟随着 `p` 或 `P`），且是 2 的倍数，如：`0x1.0p-1021`。
4. 虚数后缀 `i` 可以跟随着任意进制的整数和浮点数。
5. 整数或浮点数字面值中间可以使用下划线（`_`）来分隔数字，以提高可读性。
6. 左移与右移操作符移除操作数必须是无符号的限制，也就是说，有符号整数也可以直接进行左移或右移，而不用先转换到无符号整数再进行左右移操作。

## 移植

1. Go1.13 是最后一个支持 Native Client(NaCl) 的版本。
2. 当 `GOARCH=wasm` 时，可以使用环境变量 `GOWASM` 指定一个逗号分隔的体验特性列表，以体验新特性。
3. 对于 AIX/PPC64 架构，支持 `CGO`、外部链接以及 `c-archive` 和 `pie` 构建模式。
4. 兼容性 Android 10。
5. 对于 Darwin 系统，最低要求 macOS 10.11 El Capitan。
6. 对于 FreeBSD 系统，最低要求 FreeBSD 11.2。
7. 当前支持 `illumos` 操作系统。

## 工具

1. `GO111MODULE` 环境变量继续默认为 `auto`，但它会激活模块模型。
2. 新的环境变量 `GOPRIVATE` 可以用来指示某些模块路径不是公共可见的，从而针对这些模块绕过代理。
3. `GOPROXY` 环境变量可以被设置为一个逗号分隔的代理 URL 或关键字 direct 列表，默认值是 `https://proxy.golang.org,direct`；代理将依次使用每个代理来下载模块，直到成功为止，或者直接访问不使用代理而是直接连接模块使在的服务器。
    1. 直接前一个代理 URL 返回 `404` 或 `410` 状态码时，才会尝试下一个代理 URL。
    2. `direct` 后面的所有代理都是无效的，所以 `direct` 应当是最后一个。
4. `go env` 支持新的 `-w` 选项，以便为每个用户设置相应的环境变量。相应地，`-u` 选项用来取消 `-w` 的设置。
5. `go build` 支持新的 `-trimpath` 选项，用来从编译成的可执行程序中移除所有的文件系统路径，以便提高构建的复现性。
6. `go build` 的 `-tags` 选项，支持逗号分隔的标签列表，原先的空格分隔被废弃，但仍然可以使用。
7. 二进制包不再被支持。
8. 编译器又实现且默认启用了一个新的逃逸分析，它更加精确，但是也可能会中断一些无效的代码。为了启用旧的逃逸分析，可以使用 `go build -gcflags=all=-newescape=false` 选项来构建程序，但它仅是个过滤选项，在未来的某个版本会被移除。
9. `godoc` 命令不再包含在二进制发行版中，为获取它，可以运行 `go get golang.org/x/tools/cmd/godoc`。

## 运行时

1. `defer` 的性能大部分下可以提升 30%。

## 核心库

1. `crypto/tls` 默认支持 TLS 1.3。但它能通过在 `GODEBUG` 环境变量中添加 `tls13=0` 来禁用它，不过，它只是个过滤选项，将在 Go 1.14 中被取消。
2. `errors` 添加三个新的函数 `As`、`Is`、`Unwrap` 用来捕获、解出、判断错误。


# Go1.14

大部分改变都聚焦在工具链、运行时和库。

## 语言改变
在内嵌 `interface` 时，允许被内嵌的 `interface` 与内嵌的 `interface` 存在方法集重叠：这些重叠的方法必须拥有相同的名字和一致的方法签名（即参数和返回值的个数及其顺序）。这个改变可以解决典型的菱型内嵌 `interface`，如：有四个 `interface`：A、B、C、D，其中，A 被内嵌到 B 和 C 中，而 B 和 C 又同时被内嵌到 D 中，这在之前是不允许的，但从 Go1.14 开始，这是被允许的。

## 移植

### Darwin
1. Go1.14 是最后一个支持 macOS 10.11 EI Capitan 的版本，从 Go1.15 开始则要求 macOS 10.12 Sierra 及以上。
2. Go1.14 是最后一个在 macOS 上支持 32 位的版本，因为从 10.15 开始，macOS 不再支持 32 位程序。

### Windows
1. Go 二进制程序现在将启用 [DEP(Data Execution Prevention)](https://docs.microsoft.com/en-us/windows/win32/memory/data-execution-prevention)。
2. 在创建文件时（即调用 `os.OpenFile` 或 `syscall.Open`），如果没有设置拥有者写权限位标志，则以只读权限模式创建该文件。

### WebAssembly
1. 通过从 GO 中的 `js.Value` 引用的 JavaScript 值，现在可以被 GC 回收了。
2. `js.Value` 值不再通过 `==` 操作符进行比较，相反必须通过调用其方法 `Equal`。（注：主要是因为该值可以被 GC 回收了。）
3. `js.Value` 现在有方法 `IsUndefined`、`IsNull`、`IsNaN` 以便用来判断该 JS 值是否是 `undefined`、`null`、`nan`。

### RISC-V
1. Go1.14 开始在 Linux 系统上试验性支持 64 位 RISC-V 指令集（`GOOS=linux GOARCH=riscv64`）。

### FreeBSD
1. Go现在开始在 FreeBSD 12.0 及其后续版本中支持 64 位 ARM 指令集。

### Native Client(NaCl)
1. 正如 Go1.13 中所声明的，从 Go1.14 开始，不再支持 NaCl（`GOOS=nacl`）。

### Illumos
对于 `runtime.NumCPU`，运行时现在遵守区域 CPU 容量（`zone.cpu-cap`资源控制），默认为 `GOMACPROCS`。

## 工具

1. 如果 `main` 模块顶层包含一个 `vendor` 目录并且 `go.mod` 指定 `go 1.14` 及其以上版本，则 `go` 命令自动将 `-mod` 默认设置到 `vendor`（即 `-mod=vendor`）。但是，一个新的标志 `mod=mod` 能改变这种默认设置行为，它将使 `go` 命令从模块缓存中加载模块，而不管 `vendor` 目录是否存在。
2. 当设置显式或默认设置 `-mod=vendor` 时，GO命令会验证 `main` 模块中的 `vendor/modules.txt` 文件是否和它的 `go.mod` 文件一致。
3. `go get` 命令不再接受命令行参数 `-mod`。
4. 新增环境变量 `GOINSECURE` 来指示 GO 命令在从代码源直接获取设置的包时，不再强求 HTTPS 连接以及跳过证书验证。`GOINSECURE` 的设置方式和 `GOPRIVATE` 一样。
5. 如果某个模块的最新版本中包含 `go.mod` 文件，`go get` 不再更新到一个 `incompatible` 的主版本，除非显式地请求这样的版本。另外，如果直接从代码源获取这样的模块时，`go list` 也会自动忽略 `incompatible` 的主版本
6. 除了 `go mod tidy` 之外的其它 GO 命令不再移除 `indirect` 依赖的 `require` 指令。
7. 如果只是对 `go.mod` 文件进行修改性的改变，除了 `go mod tidy` 之外的其它 GO 命令不再编辑 `go.mod` 文件。

## 运行时
1. 对于那些零开销调用，Go1.14 极大的提升了 `defer` 的性能。
2. Goroutines 可异步抢占。因此，没有任何函数调用的死循环不再导致锁死调度器。但仅支持除 `windows/arm`、`darwin/arm`、`js/wasm` 和 `plan9/*` 外的其它平台。
3. 页分配更高效，避免在大量 `GOMACPROCS` 情况下锁竞争，在高速并行分配大量内存时，延迟更低、吞吐量更高。
4. 被 `time.After`、`time.Tick`、`net.Conn.SetDeadline` 等使用的内部计时器更高效，减少了一些锁竞争和上下文切换。

## 核心库
1. 新增一个包 `hash/maphash`，它提供字节序列的 Hash 功能，可以被用来实现哈希表或其它需要映射任意字符串或字节序列到一个唯一 64 位无符号整数的数据结构。注：哈希函数是耐碰撞的，但不是加密性的。
