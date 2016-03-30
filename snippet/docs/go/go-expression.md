
表达式
=====

## 1、内建函数new
表达式`new(T)`分配一个零初始化的值，并返回指向它的指针。如：
```go
var t *T = new(T)
```
或
```go
t := new(T)
```


## 2、操作符
GO中只有 `一元操作符` 和 `二元操作符`，没有`三元操作符`。

一元操作符：`+    -    !    ^    *    &    <-`

二元操作符：`||   &&   ==   !=   <    <=   >   >=   +   -   *   /   %   |   ^   >>   <<   &   &^`

注：像`+`、`-`、`*`、`^`、`&`均可以作为`一元操作符`或`二元操作符`，但其具有不同的含义。


## 3、操作符优先级
（1）**`一元操作符有最高的优先级`**；但是 `++`` 和 `--`` 操作符不再操作符优先级之内，因为它们是语句，而不表达式。

如：`*p++`` 等价于 `(*p)++`，并且此语法是个语句，并不是表达式，因为不能用在其他语句之内。

（2）**`二元操作符有五个优先级等级`**，从高到低，依次是：`乘法（Multiplication）`、`加法（Addition）`、`比较（Comparison）`、`逻辑与&&（logical AND）`、`逻辑或||（logical OR）`。如下表：
```go
    Precedence              Operator
        5                     *    /    %    <<   >>   &   &^
        4                     +    -    |    ^
        3                     ==   !=   <    <=   >    >=
        2                     &&
        1                     ||
```
注：当二元操作符有相同的优先级时，则按 `从左到右` 的顺序进行结合。


## 4、计算顺序
当需要计算一个表达式的操作数时，`赋值语句`、`return语句`、`所有的函数调用`、`方法调用` 以及 `通信操作`（如channel管道）都将会按照 `从左到右` 的顺序依次计算。如：
```go
y[f()], ok = g(h(), i()+x[j()], <-c), k()
```
注：
（1）函数调用和通信操作的执行顺序依次是：`f()`、`h()`、`i()`、`j()`、`<-c`、`g()`、`k()`。但是对于 `x` 的索引 和 `y` 的计算的顺序并没有作出规定。

（2）最佳实践一般不会写出这样的代码（计算顺序不确定）；如果确实需要这样的代码，应该将其拆句几个语句。


## 5、类型推断表达式
（1）“`类型推断`”可将一个`interface类型`的`变量x`转换成`T类型`的变量。

（2）“`类型推断表达式`”有两个要求：

    A. 变量x必须是非 nil 值的interface变量；
    B. 变量x中存储的是T类型的值。

（3）在“`类型推断`”中，`类型T` 即可以是`interface`，也可以是`非interface类型`。准确地说，

    A. 如果类型T不是interface类型，那么x.(T)将认定 x 的动态类型标识化T类型，即 x 的动态类型和T类型有完全相同的标识化。
       在这种情况下，类型T 必须实现 x 的 interface类型，否则这个类型推断是无效的，因为x不能存储 类型T 的值。
    B. 如果类型T 是interface类型，那么x.(T) 将认定 x 的动态类型实现了 interface类型T。

注：关于`类型标识化（Type Identical）`，请参见上文的“类型标识”。

（4）如果类型推断有效，那么其表达式的值就是存储在 `x` 中的值，而且其类型是`T类型`；否则，运行时`panic`将会发生。

（5）类型推断表达式可以用于赋值或初始化中，其格式如下：
```go
v, ok = x.(T)
v, ok := x.(T)
var v, ok = x.(T)
```
其中，`ok` 是一个`boolean`值，如果推断成功，`ok` 为 `true`；否则，则 `ok` 为`false`，并且 `v` 的值是`类型T`的`零值`。


## 6、索引表达式
（1）索引表达式的格式：`a[x]`

其中，`a`是`数组Array`、`指向数组的指针Pointer`、`分片Slice`、`字符串String` 或 `映射Map`，`x`是`索引`；根据 `a` 的类型的不同，`x`分别叫做 `索引Index` 或 `键Key`。

（2）如果 a 不是 `Map`：

    A. 索引 x 必须是整数类型或untyped的整数字面值；并且它的值必须满足 0 <= x < len(a)，否则它是超出值域，将会抛出Panic。
    B. 常量索引值必须是非负整数，并且可以表示为 int类型的值。

（3）如果 a 的类型是 `Array类型A`：

    A. 常量索引必须位于值域内，即 0 <= x < len(a)，否则将发生运行Panic。
    B. a[x] 的值是索引x 处的数组a的元素，其类型是元素类型A。

（4）如果 a 的类型是`指向Array的Pointer类型`：

    A. a[x] 是 (*a)[x] 的简化，即简短表示，二者是等价的。

（5）如果 a 的类型是 `Slice类型S`：

    A. a[x] 的值是索引x 处的分片a 的元素，其类型是元素类型S。

（6）如果 a 的类型是 `String类型S`：

    A. a[x] 的值是索引x处的非常量（non-constant）字节，其类型是byte。
    B. a[x] 不能被赋值，因为string是只读的。

（7）如果 a 的类型是 `Map类型M`（假设Key的类型为K，Value的类型为V）：

    A. x 的类型必须可确定为类型K。
    B. 如果映射中包含一个键为x的一个键值对，那么 a[x] 就是键为x的 map 值，且其类型就是类型V。
    C. 如果映射为 nil 或没有包含键为 x 的键值对，那么 a[x] 的值就是类型V的零值。

（8）其它任何情况，`a[x]` 都是`非法的`、`无效的`。

（9）一个 `map[K]V` 类型的索引表达式可以用于`赋值`或`初始化`中，格式如下：
```go
v, ok = a[x]
v, ok := a[x]
var v, ok = a[x]
```
其中，`ok` 是一个`boolean`值，如果`a`中存在键为`x`的键值对，则 `ok` 为 `true`；否则，`ok` 为`false`，并且 `v` 的值是`类型T`的`零值`。

（10）如果给一个值为 `nil` 的 `Map` 变量添加键值对，将引发运行时`Panic`。 但是`获取是可以的`，`其值为相应类型的零值`。


## 7、类型转换
类型转换可以将一个非类型 T 的表达式 x 转换成T类型变量。语法为：`T(x)`。

如果类型 T 以 **`*`** 或 **`<-`** 开头，或者以关键字`func`开头且没有结果列表，那么它必须放在`圆括号`中，以避免歧义。
```go
*Point(p)        // same as *(Point(p))
(*Point)(p)      // p is converted to *Point
<-chan int(c)    // same as <-(chan int(c))
(<-chan int)(c)  // c is converted to <-chan int
func()(x)        // function signature func() x
(func())(x)      // x is converted to func()
(func() int)(x)  // x is converted to func() int
func() int(x)    // x is converted to func() int (unambiguous)
```

#### 常量值转换
一个常量值 x 可以在以下情况下转换为类型T：

    (1) x 可以被类型 T 的变量来表示。
    (2) x 是一个浮点常量，T 是浮点类型，且 x 在根据IEEE754 round-to-even规则 Rounding 之后可被 T 类型的浮点类型来表示。
    (3) x 是一个整数常量，T 是一个字符串类型，这和 x 是非常量时的转换规则一致。

转换一个（未类型化untyped）常量值将产生一个类型化的(typed)的常量值。
```go
uint(iota)               // iota value of type uint
float32(2.718281828)     // 2.718281828 of type float32
complex128(1)            // 1.0 + 0.0i of type complex128
float32(0.49999999)      // 0.5 of type float32
float64(-1e-1000)        // 0.0 of type float64
string('x')              // "x" of type string
string(0x266c)           // "♬" of type string
MyString("foo" + "bar")  // "foobar" of type MyString
string([]byte{'a'})      // not a constant: []byte{'a'} is not a constant
(*int)(nil)              // not a constant: nil is not a constant, *int is not a boolean, numeric, or string type
int(1.2)                 // illegal: 1.2 cannot be represented as an int
string(65.0)             // illegal: 65.0 is not an integer constant
```

#### 非常量值转换
一个非常量值 x 可以在以下情况下被转换成类型 T：

    (1) x 对类型 T 是可赋值的。
    (2) x 的类型和 T 有相同标识的底层类型。
    (3) x 的类型和 T 都是未命名的指针类型，且它们指向的基础类型有相同标识的底层类型。
    (4) x 的类型和 T 都是整数类型或浮点类型。
    (5) x 的类型和 T 都是复数类型。
    (6) x 是整数，或是bytes或rune类型的分片；且 T 是字符串类型。
    (7) x 是字符串，T 是 bytes或rune 类型的分片。

特定的规则适应于(1)数值类型之间的转换，(2)转换成字符串类型或从字符串转换而来。但这些转换可能会改变 x 的底层表示，以及增加运行时开销；而其他所有的转换都仅仅是改变 x 的类型，并不改变 x 的底层表示。

在指针和整数之间的类型转换并不没有语言上的机制。标准库 unsafe 在受限环境下实现了这个功能。

#### 数值类型间的转换
对于非常量数值类型值间的转换，适应于下面的规则：

    (1) 当在整数类型间转换时，如果一个值是有符号整数，那么它的符号被扩展到无限的精度；否则，它是0。
        然后，它会被截断以便适合结果类型的大小。例如，如果 v := uint16(0x10F0)，那么 uint32(int8(v)) == 0xFFFFFFF0。
        这个转换总是产生一个有效的值，不会有溢出。
    (2) 当把一个浮点数转换成整数时，小数部分会被移除，即向0方向截断。
    (3) 当把一个整数或浮点数转换成另一个浮点数，或把一个复数转换成另一个复数时，其结果值是四舍五入到目的类型的精确度。

在所有的非常量转换（包括浮点数值或复数值）中，如果结果类型不能表示成功转换后的值，那么结果值将是未定义的。

#### 转换到字符串类型 或 从字符串类型转换

(1) 把一个有符号或无符号的整数值转换成字符串类型，将产生一个包含整数表述的UTF8字符串。超出有效的Unicode Code Point范围的值会被转换成 "\uFFFD"。
```go
string('a')       // "a"
string(-1)        // "\ufffd" == "\xef\xbf\xbd"
string(0xf8)      // "\u00f8" == "ø" == "\xc3\xb8"
type MyString string
MyString(0x65e5)  // "\u65e5" == "日" == "\xe6\x97\xa5"
```

(2) 把一个bytes类型的分片转换成字符串类型，将产生一个字符串值，它的连续的字节就是分片的元素。
```go
string([]byte{'h', 'e', 'l', 'l', '\xc3', '\xb8'})   // "hellø"
string([]byte{})                                     // ""
string([]byte(nil))                                  // ""

type MyBytes []byte
string(MyBytes{'h', 'e', 'l', 'l', '\xc3', '\xb8'})  // "hellø"
```

(3) 把一个rune类型的分片转换成字符串类型，将产生一个字符串值，该值是所有被转换成字符串的、单独的rune值的串联。
```go
string([]rune{0x767d, 0x9d6c, 0x7fd4})   // "\u767d\u9d6c\u7fd4" == "白鵬翔"
string([]rune{})                         // ""
string([]rune(nil))                      // ""

type MyRunes []rune
string(MyRunes{0x767d, 0x9d6c, 0x7fd4})  // "\u767d\u9d6c\u7fd4" == "白鵬翔"
```

(4) 把一个字符串类型的值转换成 bytes 分片，将产生一个分片，它的连续的元素 就是字符串的每个字节。
```go
[]byte("hellø")   // []byte{'h', 'e', 'l', 'l', '\xc3', '\xb8'}
[]byte("")        // []byte{}

MyBytes("hellø")  // []byte{'h', 'e', 'l', 'l', '\xc3', '\xb8'}
```

(5) 把一个字符串类型的值转换成 rune 分片，将产生一个包含该字符串的每个单独的 Unicode Code Point 的分片，它的连续的元素 就是字符串的每个字节。
```go
[]rune(MyString("白鵬翔"))  // []rune{0x767d, 0x9d6c, 0x7fd4}
[]rune("")                 // []rune{}

MyRunes("白鵬翔")           // []rune{0x767d, 0x9d6c, 0x7fd4}
```


## 8、比较
(1) interface类型可以比较相等与不不等，但不能进行大小比较，以及加减运算。
