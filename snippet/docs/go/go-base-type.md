
基本类型、type和struct
====================

## 1、字符和字符串

（1）字符串是字符序列，不是字符数组。因此，可以创建新的字符串，但不能修改一个已经存在的字符串。

（2）Go中的字符串和C++中的“const strings”概念相似，字符串指针则相当于C++中的“const strings”的引用。

（3）在Go中，字符是单独的一种类型，称为 `Rune`。字符字面值用单引号 `'` 引住字符。

（4）一个`Rune`被计算成一个可以表示`Unicode`字符的整数值。

（5）字符串字面值有两种表示法：**`解释型字符串（interpreted string literals）`** 和 **`原始字符串（raw string literals）`**。

    位于两个反引号（`）之间的字符串称为 Raw 字符串；位于两个双引号（"）之间的字符串称为 Interpreted 字符串。

（6）对于 `Raw 字符串`，Go 不做任何解释：不会进行转义操作，并把转义字符看成是两个字符，而且还可以隐式的包含换行符。

    Go 中的 Raw 字符串，相当于 Python 中的 Raw 字符串（在字符串前添加 r 或 R 标识的字符串）。

（7）对于 `Interpreted 字符串`，不能包含`换行符`、`换页符`；同时，也会对`转义字符`进行转义，相当于 Python 中的普通字符串。

（8）`[]byte` 和 `string` 相互转换
`[]byte` 转 `string`：
```go
string(b)
```
`string` 转 `[]byte`：
```go
[]byte(s)
```

（9）多个字符串可以相加 ，重新生成一个新的字符串。如果相加的字符串个数过多，建议使用 `strings.Join` 函数。


## 2、数组
在Go中，数组是一个值对象，它在内部保存“int”指针；不同于C中的数组，**`Go中的数组在赋值是全拷贝`**。


## 3、指针
（1）特殊的前缀 `&` 指向（或获取，即可以看成是“`取址操作符`”）一个变量的指针。

（2）Go有指针，但没有指针运算。结构体字段也可以通过结构体指针来访问，并且通过指针间接访问是透明的。

    任何变量（包括结构体指针变量）在访问成员或域（Field）时，都是通过 <圆点>（而不是C中的->）来访问或操作的。


## 4、类型type
（1）一个类型声明是将一个标识符（即类型名）绑定到一个新的或已经存在的类型上；如果被绑定到已经存在的类型上，则二者具有相同的成分，可以认为新声明的标识符是已经存在的类型的别名。

（2）_如果新声明的类型标识符是被绑定到已经存在的类型上，则新声明的类型标识符的方法集为空，即不继承或拥有已经存在的类型的方法集，但是如果已经存在的类型是interface类型或者复合类型struct的元素，则可以继承或拥有它的方法集。_
```go
 // A Mutex is a data type with two methods, Lock and Unlock.
type Mutex struct       { /* Mutex fields */ }
func (m *Mutex) Lock()    { /* Lock implementation */ }
func (m *Mutex) Unlock()  { /* Unlock implementation */ }

// NewMutex has the same composition as Mutex but its method set is empty.
type NewMutex Mutex

// The method set of the base type of PtrMutex remains unchanged, but the method set of PtrMutex is empty.
type PtrMutex *Mutex

// The method set of *PrintableMutex contains the methods Lock and Unlock bound to its anonymous field Mutex.
type PrintableMutex struct {
    Mutex
}

// MyBlock is an interface type that has the same method set as Block.
type MyBlock Block
```

（3）任何用 `type` 定义的类型都有方法集。关于 `struct` 和 `interface` 两种类型的方法集规则，参见下文；除此之外，_`其它类型的方法集必须显式地声明，否则其方法集为空`_。


## 5、结构体struct
（1）一个`struct结构体`就是一个字段的集合（而`type`的含义跟其字面意思相符）。_**结构体中的字段通过点来访问**_。

（2）Go没有类，但可以在结构体上定义（附加一个）方法，从而使用结构体拥有方法。_方法接收者出现在func关键字和方法名之间的参数中。_

（3）可以对包中的任意类型定义任意方法，而不仅仅是针对结构体。但_**不能对基础类型或来自其他包的类型定义方法**_。

（4）`struct`类型声明中，其`field`（即成员或元素）可以指定名字（叫“显式filed”），也可以不指定名字（叫“`匿名field`”或“`嵌入field`”）。当不指定`field名字`时，其类型必须是一个`type类型T` 或 `一个指向非interface类型的指针`。也就是说，_**`当指定field名字时，其类型可以是任何类型，包括一个interface类型或interface类型指针；当不指定field名字时，其类型不能是interface类型指针，而其它的类型均可以，也可以是指向struct类型的指针`**_。

（5）当不指定`field名字`时，该类型的名字将成为field的名字。
```go
// A struct with four anonymous fields of type T1, *T2, P.T3 and *P.T4
struct {
    T1        // field name is T1
    *T2       // field name is T2
    P.T3      // field name is T3
    *P.T4     // field name is T4
    x, y int  // field names are x and y
}
```

（6）一个`struct类型`中的`field名`必须唯一。
```go
struct {
    T     // conflicts with anonymous field *T and *P.T
    *T    // conflicts with anonymous field T and *P.T
    *P.T  // conflicts with anonymous field T and *T
}
```

（7）在`struct类型`中的`field`声明中，其后可以包含一个可选的字符串字面值，这叫`Tag`，它可以作为该`field`的`属性`存在，并通过反射包`reflect`来获取。

Tag的格式是：**由以空白分隔的一系列 `Key:Value` 键值对组成字符串，其中，`Key`是没有被引号引住的非空字符串，`Value`是用双引号引住的字符串**。
```go
type S struct {
    F string `species:"gopher" color:"blue"`
}
s := S{}
st := reflect.TypeOf(s)
field := st.Field(0)
fmt.Println(field.Tag.Get("color"), field.Tag.Get("species"))
```

（8）在结构体`struct类型S`的`匿名field`中有一个`Field/Method f`，如果 `S.f` 是合法的`Selector`（选择子或选择器，可以理解为“`属性获取`”），则 `f` 被称为“`（域/方法）提升`”。

注：`被“提升”的域` 和 `struct类型`中的其它普通域一样，唯一的区别就是，_它不能通过field名字访问_。

（9） struct类型方法集：

    A.如果struct类型S声明中包含匿名域 T，则 S 和 *S 方法集中包含被提升的 “接收者T的所有方法”，
      同时 *S 也另外包含被提升的“接收者*T的所有方法”。
    B. 如果struct类型S声明中包含匿名域 *T，则 S 和 *S 方法集中包含被提升的“接收者T或*T的所有方法”。


## 6、接口interface
（1）接口类型是由一组方法定义的集合。


（2）接口类型的值可以存放实现这些方法的任何值。

（3）接口声明中只能放置：

    A. 方法的声明；
    B. 另一个interface接口类型的名字（不能是struct结构体类型的名字）。

（4）Interface类型的方法集：

_**Interface类型的方法集就是该类型所包含的方法。但如果接口类型T声明中是其它接口类型E的名字，那么接口类型E中所有可导出和不可导出的方法都将被添加到接口类型T中（即成为接口类型T方法集中的一员）。**_

注：_`包含接口类型E的所有方法集后所形成的接口类型T方法集，不能有相同的方法存在`_。比如：如果接口类型T1和T2的声明中都包含有接口类型E，那么接口类型T不能同时包含接口类型T1和T2，因为这将导致接口类型T中含有两个接口类型E中的所有方法，导致冲突。

例子：
```go
type ReadWriter interface {
    Read(b Buffer) bool
    Write(b Buffer) bool
}
type File interface {
    ReadWriter     // same as adding the methods of ReadWriter
    Locker         // same as adding the methods of Locker
    Close()
}
type LockedFile interface {
    Locker
    File        // illegal: Lock, Unlock not unique
    Lock()      // illegal: Lock not unique
}
```


### 7、slice、map和channel
```go
make([]T,  length [, capacity])    // 创建（或初始化）一个分片（slice）
make(map[T1]int [, capacity])      // 创建（或初始化）一个映射（map）
make(channelType  [, capacity])    // 创建（或初始化）一个管道（channel）
channelType := ("chan"["<-"] | "<-""chan") ElementType
```
**注：**

（1）值为 `nil` 的 `slice` 和 `map` 是未初始化的，等价于一个“`空slice`”或“`空map`”，不能添加任何元素。

（2）`slice`、`map` 和 `channel` 三个类型必须使用 `make` 内建函数进行初始化。

（3）初始化 `map` 时指定的 `capacity` 仅仅是预先分配给该 `map对象` 的存储空间，但 `map` 的最大存储空间并不限于它；也就是说，当 `map对象` 的存储空间不足时，`map` 会自动增长其存储空间以满足新元素的添加。


## 8、管道channel
`channel` 提供了一种两个并发执行的函数进行同步执行或通信的机制。

`channel` 里只能传输某一种指定的类型的值；`未初始化的channel的值nil，它不能进行通信。

#### 语法：
```go
channelType := ("chan"["<-"] | "<-""chan") ElementType
```

其中， `<-` 运算符指定了管道中传送的方向：`发送` / `接收`。如果管道的方向没有指定的话，则是双向的。如：
```go
    chan T      // 可以发送/接收T类型的数据
    chan<- T    // 只能发送T类型的数据
    <-chan T    // 只能接收T类型的数据
```

注：尽可能地左结合`chan`。

    chan<-  chan    int    <==>   chan<-  (chan   int)
    chan<-  <-chan  int    <==>   chan<-  (<-chan int)
    <-chan  <-chan  int    <==>   <-chan  (<-chan int)
    chan    (<-chan int)

#### 初始化
```go
make(channelType [, capacity])
```
**说明：**

（1）`capacity`是`channel`的容量，即`channel`中缓冲区的大小；如果容量大于`0`，那么管道就是`异步的`，也就是说，只有满的时候才阻塞发送、空的时候才阻塞接收，而其他任何时候均不阻塞。元素的接收顺序和发送顺序一致。

（2）如果容量是 `0` 或 `不指定`，那么中有在发送和接收都准备好的时候，通信才正常进行，否则都被阻塞，即此时管道是`同步的`。

（3）只有发送者才能关闭`channel`，而不是接收者。向一个已经关闭的`channel`发送数据时会引起`panic`。

（4）`channel`与文件不同，_**通常不需关闭它们**_。


## 9、变量初始化和零（zero）值
无论是通过一个变量声明，还是调用 `make` 或 `new` 内建函数，当分配一个内存用来存储一个值时，如果没有显式地提供初始化，那么这个内存将被初始化成默认值——**`将这个值中的每个元素将被初始化为它所属类型的零（zero）值`**（和整数0不同）：*布尔类型的零值是false，整数的零值是0，浮点数的零值是0.0，字符串的零值是空字符串，指针、函数、interface、slice、channel、map等类型的是零值是 nil*。另外，默认初始化将被递归地、有序地依次执行。


## 10、nil 标识符

（1）在Golang中，`nil` 标识符是预先声明的标识符，可以把它等同于关键字，虽然它不是关键字。

（2）在Golang中，`nil` 和其它语言的 `null`、`None`、`nil`、`NULL` 等一样，都指代`零值`或`空值`。

（3）在Golang中，`nil` 只能赋值给`pointer`、`channel`、`func`、`interface`、`map` 或 `slice` 等类型的变量；如果未遵循此规则，则会引发 `panic`。

（4）假设 `类型T` 实现了 `接口I`，把 `nil` 赋值给类型为 `*T` 的 `变量t`，然后再将 `变量t` 赋值给类型为 `I` 的 `变量v1`，并把 `nil` 赋值给类型为 `I` 的 `变量v2`，此时虽然 `v1` 和 `v2` 都是 `nil`，但它们并不相等。原因如下：

在底层，`interface`作为两个成员实现：`一个类型` 和 `一个值`。该值被称为 `接口的动态值`， 它是一个任意的具体值，而`该接口的类型则为该值的类型`。_`只有在内部值和类型都未设置时(nil, nil)，一个接口的值才为 nil`_。特别是，_一个 nil 接口将总是拥有一个 nil 类型_。若我们在一个接口值中存储一个 `int类型` 的指针，则内部类型将为 `int`，无论该指针的值是什么：`(*int, nil)`。 因此，这样的接口值会是非 `nil` 的，即使在该指针的内部为 `nil`。

当把一个`非interface类型`的`变量值x`赋值给一个`interface类型`的`变量v`后，无论再怎么给`变量v`赋值值（包括重新赋值为 nil），`变量v`都不会等于 `nil`，因为`变量v`中存储的动态类型永远不会是 `nil`，因此，不可能和 `nil` 再相等。

当一个返回一个`interface类型`时，如果想要返回 `nil`，_**必须显示地返回（即 `return nil`）**_，不能返回一个值为 `nil` 的变量，否则它不等于 `nil`。这在返回 `error` 的函数中很容易出错。


## 11、Selector

（1）对于非包名的一元表达式`x`，Selector表达式 `x.f` 表示值 `x` 或 `*x` 的 `Field/Method f`，即 `f` 是 `x` 或 `*x` 的 `Field/Method`，其中 `f` 就叫做 `selector`。

（2）`blank` 标识符（即下划线`_`）不能作为`selector`。

（3）`selector`表达式的类型就是 `f` 的类型。

（4）如果 `x` 是个包名，则 `x.f` 遵守包中标识符可导出的限制。

（5）Selector `f` 可以表示 `类型T` 的 `Field/Method f`，也可以表示 **嵌套在 `类型T` 中的某个匿名域的 `Field/Method f`**。

（6）访问到 `f` 所遍历的匿名域的个数叫做“`f 在 T 中的深度depth`”；其中：

    A. 直接声明在类型 T 中的 Field/Method f 的深度规定为0；
    B. 如果A是类型T的匿名域，f 是A的Field/Method，则“f在T中的深度”等于“f在A中的深度”加1。


## 12、类型标识

（1）两个类型，要么是完全相同的，要么是不同的。

（2）如果两个命名类型是通过相同的类型规范创建的，那么它们是完全相同的。

（3）**命名的类型和未命名的类型永远是不同的**。

注意：如果要使用 `未命名类型` 的变量，前后都要是 `未命名的类型`；但是，只要二者兼容，`未命名类型` 可以转换为 `命名类型`。

（4）**如果两个未命令的类型的类型字面值是相同的（即它们有相同的字面值结构体，而且其组成也是完全相同的类型），那么它们也是完全相同的**。

（5）详细规则如下：

        A. 如果两个Array类型有完全相同的元素类型和数组长度，那么它们是完全相同的。
        B. 如果两个Slice类型有完全相同的元素类型，那么它们是完全相同的。
        C. 如果两个Struct类型有相同序列的域Field，并且相应的域有相同的名字、类型、标签Tag，那么它们是完全相同的。
           注：（1）两个匿名域被认为有相同的名字；（2）来自不同包的小写域名总是不同的。
        D. 如果两个Pointer类型有完全相同的基本类型（Base Type），那么它们是完全相同的。
        E. 如果两个Function类型有相同数目的参数和返回值，相应参数和返回值的类型是完全相同的，
           而且它们要么都有可变参数，要么都没有，那么它们是完全相同的。
        F. 如果两个Interface类型有相同的方法集（即这些方法有相同的名字和完全相同的函数标识类型），那么它们是完全相同的。
           注：（1）来自不同包的小写方法名总是不同的；（2）方法的顺序是无关紧要的，即Interface类型的标识跟方法的顺序无关。
        G. 如果两个Map类型有完全相同的键类型和值类型，那么它们是完全相同的。
        H. 如果两个Channel类型有完全相同的值类型和方向，那么它们是完全相同的。


## 13、值的确定性（Assignability）
如果满足以下任何一条，则 `x` 的值可以确定为 `类型T` 的变量：

    （1）x 的类型和类型T完全相同。 注：有相同的类型标识，见上文“类型标识”。
    （2）x 的 类型V 和 类型T 有完全相同的底层类型（underlying type），并且其中至少有一个不是命名类型（named type）。
    （3）T 是 interface类型，并且 x 实现了 T。
    （4）x 是双向 channel 值，T 是 Chaneel类型，x 的 类型V 和 类型T 有完全相同的元素类型，并且其中至少有一个不是命名类型。
    （5）x 是预声明标识符 nil，T 是一个 Pointer、Function、 Slice、Map、Channel 或 Interface 类型。
    （6）x 是一个 可用类型T 的值来表示的 untyped 常量。


## 14、特殊的 interface
### 14.1 `String() string`
任何类型都可以实现 `fmt.Stringer` interface，即方法 `String() string`，这个方法主要用于打印值，如 `fmt.Print`，或者需要一个 `string` 类型的值（即如果一个类型不是`string`，但又需要`string`，可以使用此方法来获得）。

### 14.2 `Format(f State, c rune)`
这是一个自定义 `Formatter`，主要用于 `fmt.Sprintf(f)` 或 `fmt.Fprintf(f)` 调用，以产生它的输出。
