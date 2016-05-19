
声明与语句
========

## 1、声明与赋值

（1）在函数中，“`:=`” 简洁赋值语句在明确类型的地方，可以用于代替`var`定义变量。

但函数外的每个语法块都必须以`关键字`开始（如“var”、“func”等），因此，**“`:=`” 结构不能在函数外使用**。

（2）在`Go`中，不同类型之间的赋值必须显式转换。


## 2、常量

常量不能使用 “`:=`” 定义，必须使用 `const` 关键字。

定义的常量是**`无类型的（untyped）`**，当其赋值给一个变量或与一个变量进行比较时，它将获得其类型。

**语言规范：**数字常量有任意精度。

**实现限制：**具体实现时可以有个精度限制，但是必须满足：

    （1）对于整数，必须至少使用 256 位精度来表示；
    （2）对于浮点数以及复数的虚、实部，其小数部分必须至少使用256位精度，其指数部分必须至少使用32位精度；
    （3）如果无法精确地表示一个整数常量，实现应当给出一个错误；
    （4）如果由于溢出而无法表示一个浮点数或复数，实现应当给出一个错误；
    （5）如果由于精度的限制而无法准确地表示一个浮点数或复数，实现必须向最接近常量的表示进行舍入，如：
        假设实现无法表示1.10000000001，则须要表示成1.1；如果无法表示1.1999999999，则须要表示成1.2。


## 3、控制语句

（1）在`Go`中，只有一个循环结构`for`，其中，“`{`”和“``}`”是必须的，但条件中的分号是可以省略的，此时就像C中的`while`。_**如果循环条件被省略，相当于“永远为真”**_。

（2）`if`、`for`语句可以在条件之前执行一个简单的语句，并且由这个语句定义的变量的作用域仅在`if`或`for`语句作用域范围之内。另外，`if`便捷语句定义的变量同样可以在任何对应的`else`块中使用。

（3）除非使用 `fallthrough` 语句作为结尾，否则 `case` 部分会自动终止（正好与C中`break`相反）。

（4）`switch` 的条件从上到下执行匹配，当匹配成功时停止。没有条件的`switch`同“`switch true`”一样。


## 4、GO例程

（1）`goroutine`是由Go运行时环境管理的轻量级线程，其语法是： **`go` 关键字后紧跟着一个函数调用**。


## 5、方法声明

（1）`方法（method）`就是带有`接收器（receiver）`的函数。

    方法声明就是将一个标识符（即方法名）绑定到一个方法上，并将其关联到接收器的基本类型上。
    接收器的类型必须是 T 或者 *T（假设T是一个类型名）。

（2）**语法：**在 `func` 关键字和函数名之间添加 “`(T)`” 或 “`(*T)`” ，同时也可以在其中指定接收器的名字，如：`(t T)`` 或 `(t *T)`。

（3）如果要是通过方法来修改接收器中的内容，需要使用 `*T` 类型的接收器。因为在 GO 中，所有类型的变量都拷贝型的，即在变量赋值时，整个变量的值都会拷贝一份（数组也不例外，这和C中的数组不同），如果变量是指针类型的，那么即使发生拷贝，拷贝的也是地址，仍然可以修改该地址所指向的内存空间中的内容；但如果不是指针类型的，那么拷贝一份副本，对接收器的修改只是作用在副本身上，而不会作用在原先的变量身上。

但有一点例外，如果这个接收器是像 `slice`、`map` 这样的类型的，可以不需要使用 `*T` 类型的，因为这样的类型保存了底层存储空间的地址（即指针），即使拷贝了一份副本，它仍然能修改原变量的内容。

（4）`T` 和 `*T` 对于接收器的另一个区别是：

    在方法集（Method Sets）中，
    T 的方法集只包含接收器声明为 T 类型的方法，
    *T 的方法集却包含接收器声明为 T 和 *T 类型的方法。

（5）接收器的基本类型不仅仅是`struct`，只要是通过 `type` 关键字定义的类型都可以作为接收器。


## 6、if 语句
### 语法一
```go
if  expr {
        statements
}
```

### 语法二
```go
if  expr {
        statements
} else {
        statements
}
```

### 语法三
```go
if  expr1 {
        statements
} else if  expr2 {
        statements
} else {
        statements
}
```

**说明：**

以上各 `expr` 表达式，可以是单个表达式（如 `a > b`），也可以是以分号隔开的两个表达式（如 `x := 10; x < y`），此时前一个表达式一般是个简单语句（常用的是赋值语句）。


## 7、switch 和 fallthrough 语句
`switch` 语句有两种：`表达式switch` 和 `类型switch`。在`表达式switch`中，`case`后的表达式用来与`switch表达式`的值进行比较是否相等；在`类型switch`中，`case`后的类型用来与`switch表达式`所表述的类型进行比较是否相同。

### 表达式Switch
```go
switch  [ SimpleSmt ; ] [ SwitchExpr ] {
        case CaseExprList1: statements
        case CaseExprList2: statements
        ......
        default: statements
}
```

#### 说明
（1）`case` 后的表达式不一定是常量，也可以是变量；其值的计算顺序是：`从左到右`，`从上到下`。

（2）一旦有一个 `case表达式` 与 `switch表达式` 匹配，就会执行相应的 `statements`，之后结束整个`Switch`语句，即其它的`case`或`default`语句不会被执行。

注：这一点与C、C++等语言不同。

（3）如果没有任何`case表达式`匹配，则执行 `default` 语句。

（4）在一个`Switch`语句中，只能有一个 `default` 语句，但它可以出现在该`Switch`语句的任何地方，即它与`case`语句没有顺序关系。

（5）如果没有`Switch表达式`，则默认为布尔值 `true`。

（7）为了继续执行当前 `case` 或 `default` 语句后的 `case` 或 `default` 语句，需要在当前 `case` 或 `default` 语句中的最后添加一个 `fallthrough` 语句（即 `fallthrough;`）。

（8）`fallthrough` 语句只能用于 `Switch` 语句中。

（9）多个`case`可以合并，即多个`CaseExprList`可以合并到一个`case表达式`中。

#### 例子
```go
switch tag {
        default: s3()
        case 0, 1, 2, 3: s1()
        case 4, 5, 6, 7: s2()
}

switch x := f(); {      // missing switch expression means "true"
        case x < 0: return -x
        default: return x
}

switch {
        case x < y:  f1()
        case x < z:  f2()
        case x == 4:  f3()
}
```

### 类型Switch

`类型Switch`与`表达式Switch`相似，唯一不同的是，`类型Switch`比较的是`类型`，而不是`值`。

在语法上，`类型Switch`与`表达式Switch`的不同体现在 `Switch 表达式（SwitchExpr）` 和 `Case 表达式（CaseExprList）` 上。

在`类型Switch`中，`SwitchExpr` 使用的是`类型假定语法`（通过使用关键字 type），`CaseExprList` 则是一个变量或函数的`具体类型`。

#### 例子
```go
switch i := x.(type) {
    case nil:
        printString("x is nil")   // type of i is type of x (interface{})
    case int:
        printInt(i)               // type of i is int
    case float64:
        printFloat64(i)           // type of i is float64
    case func(int) float64:
        printFunction(i)          // type of i is func(int) float64
    case bool, string:
        printString("type is bool or string")  // type of i is type of x (interface{})
    default:
        printString("don't know the type")     // type of i is type of x (interface{})
}
```

说明：`fallthrough` 关键字不能用于 `类型Switch` 中。


## 8、for 语句

### 语法一
```go
for Condition {
    statements
}
```

**Example:**
```go
i := 1
for i <= 3 {
    fmt.Println(i)
    i = i + 1
}
```

**注：**

`for      { S() }` 等同于 `for true     { S() }`。

`for cond { S() }` 等同于 `for ; cond ; { S() }`。

### 语法二：ForClause
```go
for [ InitStmt ] ; [ Condition ] ; [ PostStmt ] {
    statements
}
```

**说明：**

    （1）语义等同于C、C++等语言中的 for 语句；
    （2）如果 Condition 缺失，它的值等同于布尔值 true。

**Example:**
```go
for j := 7; j <= 9; j++ {
    fmt.Println(j)
}
```

### 语法三：For-Range-Clause
```go
for [ ExprList = ] range Expr {
    statements
}
```

**说明：**

（1）该语法能迭代`数组Array`、`分片Slice`、`字符串String`、`映射Map`，或者`从管道上接收的值`。
（2）如果迭代变量存在，那么每次迭代都会把迭代值赋值给迭代变量，然后执行`statements`。

（3）如果迭代变量存在，它必须是可寻址的（即有存储空间），或者是 `map` 的索引表达式。

（4）如果 `range表达式`是个管道（Channel），**_`最多只能有一个迭代变量`_**；如果是其它形式的`range表达式`，**_`迭代变量最多只能有两个`_**。

（5）当迭代变量有两个，且最后一个是下划线（即 `_`， blank identifier）时，`range 表达式`等价于没有下划线的表达式（即只有一个迭代变量的情况）。

（6）在迭代开始之前，`range表达式`仅仅被计算一次。但有一种情况例外：如果`range表达式`是个“`数组`”或者“`指向数组的指针`”，那么迭代变量最多只能有一个，而且只计算 `range表达式`的长度；但是，如果其长度是个常量，那么`range表达式`本身不会被计算。

（7） 如果赋值符号左边（即`ExprList`）是个`函数调用`，则每次迭代时都会被调用一次。

（8）每次迭代时，迭代值会被赋值给相应的迭代变量，其行为就如同赋值语句一般。

（9）每次迭代时，如果相应的迭代变量存在，迭代值都会按如下方式被处理：

RangeExpr                               |  1st value     |  2nd value
----------------------------------------|----------------|---------------
array or slice    a [n]E, *[n]E, or []E | index   i int  | a[i] E
string            s string type         | index   i int  | see below rune
map               m map[K]V             | key     k K    | m[k] V
channel           c chan E, <-chan E    | element e E    |

    A. 索引（index）从 0 开始。另外，如果在分片值 nil 上进行迭代，则迭代次数为 0（即不做任何迭代）。
    B. 如果迭代表达式是个string，则range从索引为0的字节上开始迭代。
       如果迭代成功，第二个迭代值为Unicode code point（rune类型），而第一个迭代值则是该Point的第一字节的索引值。
       如果迭代失败，第一个迭代值同上，第二个迭代值为 0xFFFD；
       当时进行下一次迭代时，则从当前字节的下一个字节开始，即下一次迭代的第一个迭代值为当前第一个迭代值加1。
    C. 对于Map的迭代，其迭代顺序是不确定的，即两次 for-range 循环的迭代顺序并不保证是相同的（这是Go1语言规范规定的）。
       如果map为nil，则迭代次数为 0（即不做任何迭代）。
    D. 对于 Channel，被处理的迭代值是成功发送到Channel上的值，直到Channel被关闭。
       如果channel为nil，则range表达式将永远被阻塞。

**Example:**
```go
var testdata *struct {
	a *[7]int
}
for i, _ := range testdata.a {
	// testdata.a is never evaluated; len(testdata.a) is constant
	// i ranges from 0 to 6
	f(i)
}

var a [10]string
for i, s := range a {
	// type of i is int
	// type of s is string
	// s == a[i]
	g(i, s)
}

var key string
var val interface {}  // value type of m is assignable to val
m := map[string]int{"mon":0, "tue":1, "wed":2, "thu":3, "fri":4, "sat":5, "sun":6}
for key, val = range m {
	h(key, val)
}
// key == last map key encountered in iteration
// val == map[key]

var ch chan Work = producer()
for w := range ch {
	doWork(w)
}

// empty a channel
for range ch {}
```


## 9、go 语句（Goroutine）
### 语法
```go
go Expr
```

### 说明
（1）`Expr` 必须是个函数调用或方法调用。

（2）Go语句会在当前地址空间中开启一个独立的`Go例程（goroutine）`，然后在其中执行`Expr`（函数或方法调用过程）。

（3）当函数或方法执行结束后，该Go例程也将消失。如果函数或方法有任何返回值，那么在其结束时，该返回值将会被丢弃。

（4）在Goroutine例程中的调用中，函数（或方法）值和其参数就像普通函数调用一样被计算。


## 10、select 语句


## 11、return 语句
### 语法
```go
return ExprList
```

A、`return`只能用于函数中，并且可以出现多次。

B、如果函数没有指定返回值类型，则 `return` 语句不能指定任何返回值。

C、如果函数指定了返回类型，则有三种方式可以返回`一个`或`多个`值。

    I. 将一个或多个返回值显式地列在return语句中；其中，每个表达式（即返回值）必须是单值的，且可赋值给相应的变量。如：

        func simpleF() int {
                return 2
        }

        func complexF1() (re float64, im float64) {
                return -7.0, -4.0
        }

    II. return 可以后跟一个函数调用，该函数调用可以返回多个值。这些返回值就如同一些临时变量，因此也要满足上一条限制。如：

        func complexF2() (re float64, im float64) {
                return complexF1()
        }

    III. 如果函数的返回值类型声明中指定返回值名，则 return 可以不用跟返回值。这些返回值名就如同函数参数一样来使用。
         对于此种情况，无论返回值参数如何声明，在进入函数实体之前，所有的返回值参数都会被初始化为相应类型的零值。
         而且，在任何 defer 函数执行之前，return 语句都会收集返回值参数。
         func complexF3() (re float64, im float64) {
             re = 7.0
             im = 4.0
             return
         }

         func (devnull) Write(p []byte) (n int, _ error) {
             n = len(p)
             return
         }

### 实现限制
在一个作用域（如if语句）中，如果有一个新的变量名和返回值参数名一样，那么，当在该作用域中执行`return语句`时，编译器会隐藏先前的返回值参数，而使用该作用域中的新的变量名。如：
```go
func f(n int) (res int, err error) {
    if _, err := f(n-1); err != nil {
        return    // invalid return statement: err is shadowed
    }
    return
}
```


## 12、break 语句
### 语法
```go
break [ Label ]
```

`break` 语句只能用在 `for`、`switch`、`select` 等语句中，以终止这些语句的执行。

如果 `break` 还有 `Label` 标签，则 `Label` 标签必须包围（enclosing）它要终止的 `for`、`switch` 或 `select` 语句，即放在该语句的前面。如：
```go
OuterLoop:
for i = 0; i < n; i++ {
    for j = 0; j < m; j++ {
        switch a[i][j] {
        case nil:
            state = Error
            break OuterLoop
        case item:
            state = Found
            break OuterLoop
        }
    }
}
```


### 13、continue 语句
### 语法
```go
continue  [ Label ]
```

`continue` 语句和 `break` 语句相似，不同之处是：

    A、continue 只能用于 for 语句中；
    B、用于结束当前循环，执行下一次循环。


## 14、goto 语句
### 语法
```go
goto Label
```

### 作用
将执行流程跳转到 `Label` 标签处。

### 说明

A、`goto` 语句不能跳转到任何变量还不存在的地方，即执行流程向前跳转没有问题，向后跳转有可能发送错误。

B、在一个 `block` 语句块外的 `goto` 语句不能跳转到该 `block` 语句块中。


## 15、defer 语句
### 语法
```go
defer Expr
```

`defer`用于将一个`函数调用（Expr）`推迟到当前函数（即包含defer语句的函数）执行结束（如：执行了`return语句`、`到达函数体末尾或发生了恐慌panic`——相当于面向对象中的异常）后再调用。其中，

Expr 必须是个函数调用。

Expr（函数及其参数）在每次 `defer` 语句执行时被计算，然后保存起来，但Expr函数并不会调用，而是在当前函数执行结束后才被调用。

Expr 以被 defer（推迟）的 `逆序` 被调用。


## 16、Label 语句
### 语法：
```go
LABEL: statement
```

### 作用

标记一个语句，用于 `goto`、`break` 或 `continue` 等语句的目标。


## 17、终止语句
语句包含以下形式：

    （1）return 或 goto 语句。
    （2）内建函数 panic 的调用。
    （3）一个以终止语句结尾的 block 语句块。
    （4）在 if 语句中，存在 else 分支，并且所有分支（block 语句块）都是终止语句。
    （5）在 for 语句中，没有引用该 for 语句的 break 语句（即 break 语句不带 Label 标签），且循环条件不存在。
    （6）在switch语句中，break语句不带Label标签，有一个default分支，且每个case分支（包括default）都以一个终止语句结束。
    （7）在select语句中，break语句不带Label标签，有一个default分支，且每个case分支（包括default）都以一个终止语句结束。
    （8）标记一个终止语句的 Label 语句。

除此之外，所有其他的语句都不是终止语句。
