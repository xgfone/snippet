
基本语法
=======

## 1、Go1的兼容性声明
_**GO1规范中的内容在当前版本点能够运行的，那么在以后发布的任何GO1版本点都将继续、无改变地运行；但在 GO2 版本时，这个兼容性将不再保证。**_

举个例子：

    如果GO1.0规定了一个语法，那么这个语法将在GO1.1、GO1.2、GO1.3等等GO1.X版本中都能正常使用；另外，在GO1.2
    规范中规定的一个语法，在GO1.1和GO1.2中并不保证能够兼容，但能够保证在GO1.3、GO1.4等后续的GO1.X版本中
    正常运行；以此类推。但是，这些在GO1.X中规定的语法，其兼容性并不保证能够继续在GO2.X版本中正常运行。


## 2、关键字
Go中只有`25`个关键字

    break         default          func         interface       select
    case          defer            go           map             struct
    chan          else             goto         package         switch
    const         fallthrough      if           range           type
    continue      for              import       return          var

注：Go语法几乎与关键字有关，掌握了关键字的用法，就几乎等同于掌握了Go语言。Go语言不像其他面向对象语言那样除了关键字用法外，还有大量的、复杂的面向对象语法等。


## 3、Go中的访问规则
_**如果顶级类型名字的首字母**_（包括`function`、`method`、`constant`或`variable`、`struct`结构体中的`数据域field` 或 `方法method`）_**是大写，那么引用了这个包（package）的使用者就可以访问它；否则，名称和被命名的东西就只能在package内部看到并被使用**_。_`这是一个要严格遵循的规则，因为这个访问规则是由编译器强制规范的`_。在Go中，一组公开可见的名称被称为“exported”。另外，Go语言的命名习惯更偏爱于峰驼式，如：thisIsCase。


## 4、整数格式
Go只支持三种格式的整数：`八进制（以0开头）`、`十进制`、`十六进制（以0x或0X开头）`。


## 5、标识符
（1）_**程序中的每个标识符都必须被声明**_，且_**在相同的块中，标识符不能被声明两次**_，也_**不能在文件块和包块中同时声明**_。

（2）`blank` 标识符是 `_` （下划线），它是一个特殊的标识符——`忽略一切值`，如：将一个函数的返回值赋值给它，表明忽略返回值。


## 6、GOPATH
（1）值可以是一个字符串或字符串列表（Linux用`:`分隔，Windows用`;`分隔）；

（2）用来解决`import`语句；

（3）表示指定的Go代码的位置，不能指向Go的标准位置（即`GOROOT`指向的位置），必须用其他位置来`build`和`install`包。


## 7、块Block
（1）GO中的块分为两种：**`显示块`** 和 **`隐式块`**。

**显示块**：用大括号（即`{` `}`）括起来的部分就是一个块。

**隐式块**由以下几种：

    A. 整个GO源代码是一个整体块；
    B. 每个包都有一个包块——包含整个包中的源代码；
    C. 每个文件有一个文件块——包含该文件的所有源代码；
    D. 每个 if、for 和 switch 语句都有它自己的隐式块；
    E. 在 if 或 select 语句中每个 case 子句也都有它自己的隐式块。

（2）块能够互相嵌套，并且影响着作用——每个块都是一个作用域。

（3）块可以包含声明和语句；块也可以为空，对于显示块，它只有一对大括号。


## 8、预声明标识符

#### （1）类型（Types）

    bool    byte    complex64     complex128    error     float32      float64
    int     int8    int16         int32         int64     rune         string
    uint    uint8   uint16        uint32        uint64    uintptr

#### （2）常量（Constants）

    true false iota

#### （3）零值（Zero value）
    nil

#### （4）函数（Functions）

    append   cap    close     complex    copy     delete    imag    len    make    new
    panic    print  println   real       recover

注：对于`print`、`println`，它们是位于内建模块中，可以在全局使用，但语言规范并不保证此两个函数在以后的某个版本继续存在。


## 8、const 常量
（1）`const`常量只能声明`数值常量`、`布尔常量`、`字符串常量`。

    A. 数值常量：  Rune、Integer、Floating-Point、Complex
    B. 布尔常量：  Bool
    C. 字符串常量：String

（2）常量表达式必须是在编译期可计算的。

（3）声明常量的同时必须进行初始化，其值不可再次修改。

（4）如果定义多行常量而且表达式一致时，可省略其他行的表达式。

（5）声明时如果不指定数据类型，则该常量为无类型常量。

（6）一次可以声明多个常量，且同时赋值；当没有指定类型时，其类型可以不一致。

（7）声明多个变量，如果要指定其类型，不能分别指定数据类型，只能指定为同一种。

（8）常量可以是**`类型化的（typed）`** 和 **`未类型化的（untyped）`**。

    A. type：    指定类型的常量，以及包含 typed 常量操作数的常量表达式。
    B. untyped： 字面值常量、true、false、iota 以及只包含 untyped 常量操作数的常量表达式。

（9）一个 `untyped` 常量有一个相应的默认类型：`bool`、`rune`、`int`、`float64`、`complex128` 或 `string`。


## 9、iota 计数器
（1）`iota`是Golang语言的整数常量计数器，只能在常量表达式中使用（即只能用在`const常量表达式`中）。

（2）`iota`每遇到一次`const`关键字就被重置为 `0`（`const` 内部的第一行之前），`const`中每新增一行，常量声明将使 `iota` 计数一次，即使 `iota` 的值加 `1`（`iota`可理解为 **`const 语句块中的行索引`**。）
```go
const a = iota   // a=0
const (
    b = iota     // b=0
    c = 3        // c=3
    d = iota     // d=2
)
```

（3）在圆括号 `const` 声明列表中，表达式列表可以从任意处被省略（但第一个除外）。如果一个表达式列表被省略，那么它等价于向前数第一个非空的表达式列表的字面替代物以及它的类型（如果它有类型的话）；换句话说，_**省略一个表达式列表就等价于重复前一个表达式列表**_。但被省略的表达式列表的个数必须关一个表达式列表中表达式的个数。
```go
const (
    h = iota    // h=0
    i = 100     // i=100
    j           // j=100
    k = iota    // k=3
)
```

（4）自定义类型：自增长常量经常包含一个自定义枚举类型，允许你依靠编译器完成自增设置。
```go
type Stereotype int
const (
    TypicalNoob Stereotype = iota // 0
    TypicalHipster                // 1
    TypicalUnixWizard             // 2
    TypicalStartupFounder         // 3
)
```

（5）可跳过的值：我们可以使用下划线跳过不想要的值。
```go
type AudioOutput int
const (
    OutMute AudioOutput = iota // 0
    OutMono                    // 1
    OutStereo                  // 2
    _
    _
    OutSurround                // 5
)
```

（6）位掩码表达式
```go
type Allergen int
const (
    IgEggs Allergen = 1 << iota         // 1 << 0 which is 00000001
    IgChocolate                         // 1 << 1 which is 00000010
    IgNuts                              // 1 << 2 which is 00000100
    IgStrawberries                      // 1 << 3 which is 00001000
    IgShellfish                         // 1 << 4 which is 00010000
)
```

（7）定义数量级
```go
type ByteSize float64
const (
    _           = iota                   // ignore first value by assigning to blank identifier
    KB ByteSize = 1 << (10 * iota)       // 1 << (10*1)
    MB                                   // 1 << (10*2)
    GB                                   // 1 << (10*3)
    TB                                   // 1 << (10*4)
    PB                                   // 1 << (10*5)
    EB                                   // 1 << (10*6)
    ZB                                   // 1 << (10*7)
    YB                                   // 1 << (10*8)
)
```

（8）定义在一行的情况：`iota` 在下一行增长，而不是立即取得它的引用。
```go
const (
    Apple, Banana = iota + 1, iota + 2
    Cherimoya, Durian
    Elderberry, Fig
)
// Apple: 1
// Banana: 2
// Cherimoya: 2
// Durian: 3
// Elderberry: 3
// Fig: 4
```

## 10、Go的并发模型
Go 的座右铭之一就是：**`Share memory by communicating, don't communicate by sharing memory.`**

中文：**`通过通信来共享内存，而不要通过共享内存来通信。`**

关于 `sync.Mutex` 和 `Channel` 的一般使用向导：

Channel                                  |   Mutex
-----------------------------------------|------------
传送数据的所有权、分发工作单元、传递异步结果 | 缓存、状态


> Do not communicate by sharing memory; instead, share memory by communicating.
> [《–Effective Go》](http://golang.org/doc/effective_go.html)
