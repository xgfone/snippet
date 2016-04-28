翻译自：[Rust Reference](http://doc.rust-lang.org/reference.html)

注：`Rust` 版本是 `1.8.0`。

----

## 词法结构
### 源代码编码
（1）Rust源代码被作为`UTF8`编码的Unicode字符进行解析。

### 标识符(Identifier)
（1）单个下划线(`_`)字符不是一个标识符。

（2）关键字不是标识符。

### 注释(Comment)
Rust的注释分为两种：`代码注释`和`文档注释`。

#### 代码注释
代码注释采用 C++ 风格的注释：`行注释`(`//`)和`块注释`(`/* ... */`)。

与 C++ 不同，Rust的块注释可以被嵌套。并且代码注释会被解析成空白。

#### 文档注释
文档注释也分为两种：`注释文档后的代码`和`注释包文档的代码`。

这些注释作为所被注释的代码的文档存在，而不是被解析成空白。

##### 注释文档后的代码
此文档注释分为两种：`行文档`(`///`)和`块文档`(`/** ... */`)。

这两种文档注释等价于文档属性`#[doc="..."]`，即它们可以被转换成此文档属性。

这些注释会被作为其后代码的文档。

##### 注释包文档的代码
此文档注释分为两种：`行文档`(`//!`)和`块文档`(`/*! ... */`)。

这两种文档注释等价于文档属性`#![doc="..."]`，即它们可以被转换成此文档属性。

这些注释会被作为包含该文档的代码的文档，而不是文档后的代码的文档。

`//!`注释通常用于模块的文档，即作为整个模块的文档。

### 空白(Whitespace)
只有这些字符 `U+0020(space, ' ')`、`U+0009(tab, '\t')`、`U+000A(LF, '\n')`、`U+000D(CR, '\r')` 才会被作为空白。

这些空白字符仅用于分隔语法Token（或者说分隔字符序列），除此之外，没有任何意义。

### 字面值(Literal)
#### 字符和字符串字面值
##### 字符字面值
一个字符字面值是用一对单引号(`'`)包围的、除单引号本身之外的单个Unicode字符。对于单引号字符字面值，必须使用反斜杠进行转义，如：`'\''`。

##### 字符串字面值
一个字符串字面值是用一对双引号(`"`)包围的、除双引号本身之外的任何Unicode字符。对于双引号字符串字面值，必须使用反斜杠进行转义，如：`"\""`。

行中断字符（如换行符）可以允许出现在字符串中，它们一般表示它们自身，而不做任何转换。如：`a` 和 `b` 相等。
```rust
let a = "foo\nbar";
let b = "foo
bar";

assert_eq!(a, b);
```

但是有一个特殊的例外：如果一个反斜杠（`\`）后紧随一个换行符（U+000A），那么，反斜杠、换行符，以及下一行开头的所有空白都将被忽略。如：`a` 和 `b` 相等。
```rust
let a = "foobar";
let b = "foo\
         bar";

assert_eq!(a, b);
```

##### 转义字符
转义字符只在字符字面值或非原始（non-Raw）字符串字面值中有意义，在原始（Raw）字符串中没有意义，它们是两个或多个字符。

##### Raw字符串字面值
Raw字符串字面值开始于`字符r`，后面紧跟着`0或多个`井号(`#`)以及`一个`双引号(`"`)，之后可以包含0或多个任何Unicode字符，最后终止于`一个`双引号(`""`)以及和先前的井号数目相同的井号(`#`)。

Raw字符串字面值不处理任何转义，其中的字符都表示它们自身，双引号（除了最后在`#`之前的那个双引号）和反斜杠没有任何特殊含义。

```rust
"foo"; r"foo";                     // foo
"\"foo\""; r#""foo""#;             // "foo"

"foo #\"# bar";
r##"foo #"# bar"##;                // foo #"# bar

"\x52"; "R"; r"R";                 // R
"\\x52"; r"\x52";                  // \x52
```

#### 字节和字节字面值
##### 字节字面值
字符字面值的规则同样适用于字节字面值，只不过，字节字面值前多个`字符b`，以及其值域为ASCII码（U+0000 ~ U+007F）。

字节字面值等价于一个8位无符号整数(即`u8`)字面值。

##### 字节字符串字面值
字符串字面值的规则同样适用于字节字符串字面值，只不过，字节字符串字面值前多个`字符b`，以及其值域为ASCII码。

一个长度为 n 的字节字符串字面值等价于一个 `borrowed` 型且大小固定的 8 位无符号整数数组，即 `&'static [u8; n]`。

##### Raw字节字符串字面值
Raw字符串字面值的规则同样适用于Raw字节字符串字面值，只不过，Raw字节字符串字面值前多个`字符b`，以及其值域为ASCII码。

```rust
b"foo"; br"foo";                     // foo
b"\"foo\""; br#""foo""#;             // "foo"

b"foo #\"# bar";
br##"foo #"# bar"##;                 // foo #"# bar

b"\x52"; b"R"; br"R";                // R
b"\\x52"; br"\x52";                  // \x52
```

#### 数值字面值
一个数值字面值包含`整数字面值`和`浮点数字面值`。

##### 整数字面值
一个整数字面值有四种形式：二进制、八进制、十进制、十六进制。

**二进制**

    前缀是 U+0030 U+0062 (0b)，其后可以是任意多个 0、1 或下划线(_)。

**八进制**

    前缀是 U+0030 U+006F (0o)，其后可以是任意多个 0~7 或下划线(_)。

**十进制**

    第一个字符是数字0~9，其后可以是任意多个 0~9 或下划线(_)。

**十六进制**

    前缀是 U+0030 U+0078 (0x)，其后可以是任意多个 0~f 或下划线(_)。

一个整数字面值后可以紧跟着一个整数类型后缀（注：之间没有空格），这将强制设置该字面值的类型。但是，整数类型后缀必须是下面之一：`u8`、`i8`、`u16`、`i16`、`u32`、`i32`、`u64`、`i64`、`isize`、`usize`。

一个没有类型后缀的整数字面值将根据下面的类型推断来决定：

    (1) 如果一个整数类型可以根据程序上下文被唯一地确定，那么，后缀类型就是该类型。
    (2) 如果程序上下文满足类型约束，那么，它默认是有符号32位整数，即`i32`。
    (3) 如果程序上下文不满足类型约束，那么，它被认为静态类型错误。

```rust
123i32;                            // type i32
123u32;                            // type u32
123_u32;                           // type u32
0xff_u8;                           // type u8
0o70_i16;                          // type i16
0b1111_1111_1001_0000_i32;         // type i32
0usize;                            // type usize
```

##### 浮点数字面值
一个浮点数有下面两种形式：

    (1) 一个十进制字面值后紧跟一个圆点(`.`)，并可选地后跟另一个十进制字面值，以及一个可选的`指数部分(exponent)`。
    (2) 单个十进制字面值后紧跟一个`指数部分(exponent)`。

一个浮点数字面值后也可以紧跟一个类型后缀，只要类型后缀前不以圆点结尾即可；这将强制设置该字面值的类型。只有两个有效的浮点后缀类型：`f32`和`f64`；它们显式地确定字面值的类型。

一个没有类型后缀的浮点数字面值将根据下面的类型推断来决定：

    (1) 如果一个浮点类型可以根据程序上下文被唯一地确定，那么，后缀类型就是该类型。
    (2) 如果程序上下文满足类型约束，那么，它默认为`f64`。
    (3) 如果程序上下文不满足类型约束，那么，它被认为静态类型错误。

```rust
123.0f64;        // type f64
0.1f64;          // type f64
0.1f32;          // type f32
12E+99_f64;      // type f64
let x: f64 = 2.; // type f64
```

注：最后一个例子是不同的，它不能使用后缀类型语法，因为该浮点数字面值以圆点结尾，而 `2.f64`将被解析为：在整数2对象身上调用一个名为`f64`的方法（`f64`是整数类型的一个方法）。

#### 布尔字面值
布尔类型只有两个字面值：`true` 和 `false`。

#### 例子
##### 字符和字符串
|                   |Example      | # sets | Characters  |  Escapes |
|-------------------|-------------|--------|-------------|---------|
|**Character**       | 'H'         |  N/A   | All Unicode | Quote & Byte & Unicode |
|**String**          | "hello"     |  N/A   | All Unicode | Quote & Byte & Unicode |
|**Raw**             | r#"hello"#  |  0...  | All Unicode | N/A |
|**Raw**             | r##"hello"##  |  0...  | All Unicode | N/A |
|**Byte**            | b'H'        |  N/A   | All ASCII   | Quote & Byte |
|**Byte String**     | b"hello"    |  N/A   | All ASCII   | Quote & Byte |
|**Raw Byte String** | br#"hello"# |  0...  | All ASCII   | N/A |
|**Raw Byte String** | br##"hello"## |  0...  | All ASCII   | N/A |

##### 字节转义字符
|     | Name |
|-----|-------------------------|
| \x7F | 8-bit character code (exactly 2 digits) |
| \n   | Newline |
| \r   | Carriage return |
| \t   | Tab |
| \\\  | Backslash |
| \0   | Null |
| \'   | Single quote |
| \"   | Double quote |
| \u{7FFF} | 24-bit Unicode character code (up to 6 digits) |

##### 数字
|Number literals* |   Example   | Exponentiation | Suffixes |
|-----------------|--- ---------|----------------|----------|
|Decimal integer  | 98_222      | N/A            | Integer suffixes |
|Hex integer      | 0xff        | N/A            | Integer suffixes |
|Octal integer    | 0o77        | N/A            | Integer suffixes |
|Binary integer   | 0b1111_0000 | N/A            | Integer suffixes |
|Floating-point   | 123.0E+77   | Optional       | Floating-point suffixes |

**所有数字字面值都可以在其中插入下划线(`_`)进行分隔，以使其更具有可读性。如：1_234.0E+18f64。**

##### 类型后缀
|Integer | Floating-point |
|--------|----------------|
|u8, i8, u16, i16, u32, i32, u64, i64, isize, usize | f32, f64 |

### 路径(Path)
一个`路径`是一个或多个组件(components)的序列，它们被命名空间(namespace)修饰符(即双冒号 `::`)分隔。如果一个路径只包含一个组件，那么它可能引用一个 Item 或本地作用域中的一个变量；如果一个路径有多个组件，那么它引用一个 Item。 See Item。

每一个 Item 在它的 Crate 中都有一个标准路径，但表示一个 Item 的路径仅在一个 Crate 中才有意义。没有跨 Crate 的全局命名空间，一个 Item 的标准路径只是在 Crate 中标识它。

```rust
x;
x::y::z;
```

路径组件通常是标识符，但也有可能包含尖括号(`<>`)包围的类型能数列表。在一个表达式上下文，该类型参数列表跟随在命名空间修饰符(`::`)之后，目的是为了区别于包含小于符号(`<`)的关系表达式；在类型表达式上下文，最后一个命名空间修饰符(`::`)可以被省略。

```rust
type T = HashMap<i32,String>; // Type arguments used in a type expression
let x  = id::<i32>(10);       // Type arguments used in a call expression
```

路径可通过前导的修饰符来改变解析路径的方法。

(1) 以`::`开头的路径被作为全局路径，路径中的组件从 `根(root)` Crate 开始解析，且路径中的每个标识符都必须被解析成一个 Item。
```rust
mod a {
    pub fn foo() {}
}
mod b {
    pub fn foo() {
        ::a::foo(); // call a's foo function
    }
}
```

(2) 以关键字`super`开头的路径从当前模块的父模块开始解析，其中的每个标识符都必须被解析成一个 Item。
```rust
mod a {
    pub fn foo() {}
}
mod b {
    pub fn foo() {
        super::a::foo(); // call a's foo function
    }
}
```

(3) 以关键字`self`开头的路径从当前模块开始解析，其中的每个标识符都必须被解析成一个 Item。
```rust
fn foo() {}
fn bar() {
    self::foo();
}
```

注：关键字`super`可以在第一个`super`或`self`后重复多次，以引用相应的祖先模块。
```rust
mod a {
    fn foo() {}

    mod b {
        mod c {
            fn foo() {
                super::super::foo(); // call a's foo function
                self::super::super::foo(); // call a's foo function
            }
        }
    }
}
```

## 语法扩展

在 Rust 中，一些并不特别重要的次要特性，并没有其自己的语法，也没有作为函数被实现。相反，它们有名字，并通过一致的语法被调用：`some_extension!(...)`。

rustc 的用户有两种方式来定义新的语法扩展：

    (1) 编译器插件：可以包含能在编译期操作语法数的任何 Rust 代码。注意：这种方式的接口有很大的不稳定性，随时可能被改变。
    (2) 宏(Macro)：以一个高层次、声明式的方式来定义一个语法。

### 宏(Macro)

`macro_rules`允许用户以声明的方式来定义一个语法扩展，我们称为 `样例宏(macros by example)` 或简称为 `宏(macros)`，以区别`编译器插件`中定义的`过程式宏(procedural macros)`。

目前，宏可以被扩展为`表达式`、`语句`、`Item`或`模式(pattern)`。

一个 `sep_token` 是除 `*` 和 `+` 外任意 Token，一个 `non_special_token` 是除 `界定符(delimiter)` 和 `$` 外的任意 Token。

宏扩展会通过名字查找宏调用，依次尝试匹配每个宏规则，并转译第一个成功的匹配。匹配和转译是相互密切相关的。

#### 样例宏
宏扩展匹配并转译每一个不是以 `$` 开头的 Token，包括界定符。由于解析的原因，界定符必须均衡，但是并不特别。

在匹配器中，`$ name : designator` 匹配命名为 `designator` 的非终止符。有效的 designator 有：

- `item`: an item
- `block`: a block
- `stmt`: a statement
- `pat`: a pattern
- `expr`: an expression
- `ty`: a type
- `ident`: an identifier
- `path`: a path
- `tt`: either side of the => in macro rules
- `meta`: the contents of an attribute

在转译器中，designator 已经众所周知，所以匹配的非终止符的名字只紧跟在 `$` 后面。

在匹配器和转译器中，克林星型操作符（Kleene Star Operator）包含`$`和圆括号对`()`，可选地后面紧跟着一个分隔符(separator)，以及 `*` 或 `+`；其中，`*` 表示0或多次重复，`+`表示1或多次重复，圆括号对并不被匹配和转译。在匹配器中，一个名字被绑定到它匹配的所有名字；而转译器则是对这些匹配的名字进行排序。

这些重复操作的转义规则被称为`Macro By Example`。Essentially, one "layer" of repetition is discharged at a time, and all of them must be discharged by the time a name is transcribed. Therefore, `( $( $i:ident ),* ) => ( $i )` is an invalid macro, but `( $( $i:ident ),* ) => ( $( $i:ident ),* )` is acceptable (if trivial).

当样例宏碰到一个重复时，它会检查所有出现在它的主体中的 `$ name`。在当前层(current layer)，它们都必须重复相同的次数，所以 `( $( $i:ident ),* ; $( $j:ident ),* ) => ( $( ($i,$j) ),* )` 对 `(a,b,c ; d,e,f)` 是有效的，对 `(a,b,c ; d,e)` 是无效的。这个重复操作将前后一致地遍历选择项(choices)，所以，前一个输入将被转译成 `(a,d), (b,e), (c,f)`。

#### 解析限制
Rust语言的宏系统解析器虽然相当强大，但却有两个限制：

    (1) 在解析Rust语法的表达式和其它位(bits)后，宏定义必须包含适当的分隔符(separator)。
        这意味着，像 `$i:expr [ , ]` 这样的宏定义不是合法的，因为 `[` 可以作为表达式的一部分；
        而像 `$i:expr,` 或 `$i:expr;` 这样的宏定义是合法的，因为 `,` 和 `;` 是合法的分隔符。
    (2)解析器在遇到 `$ name : designator` 时，必须消除二义性。

## Crate 和 源文件
Rust语言作为一个编译器而被实现，并区分编译时间和运行时间。静态语义规则会在编译时间阶段控制编译的成功或失败；动态语义规则在运行时间阶段控制程序的行为。

Rust中的库以 `Crate` 的形式被组织。每个编译处理单个源码形式Crate，如果成功，将会产生单个二进制形式的Crate：要么是个可执行文件，要么是一些库。

一个 Crate 是一个编译和链接单元，以及版本、分发和运行时加载。一个Crate包含一个嵌套的模块作用树，这个树的顶层是一个匿名模块，并且在这个Crate中的任何Item都有一个统一的模块路径，用于表示该Item在Crate模块树中的路径。

Rust编译器总是把单个源代码文件作为输入，并总是产生单个Crate输出；这个源代码文件的处理可能导致其它源代码文件被作为模块加载。源代码文件的扩展名为`.rs`。

一个Rust源代码文件描述了一个模块，它的名字和位置从源文件的外部被定义：要么在一个引用源文件中指定一个显式的 `mod_item`，要么使用 Crate 它自身的名字。每个源文件都是一个模块，但并不是每个模块都需要它自己的源文件，比如：模块定义能够被嵌套在一个文件中。

每个源文件都包含 0或多个 Item 定义，也可以选择性地开始于任意数目的、作用在包含它的模块上的`属性(attribute)`，这些属性大部分都可影响、改变编译器的行为。匿名Crate模块可以有额外的、作用于整个Crate上的`属性`。

```rust
// Specify the crate name.
#![crate_name = "projx"]

// Specify the type of output artifact.
#![crate_type = "lib"]

// Turn on a warning.
// This can be done in any module, not just the anonymous crate module.
#![warn(non_camel_case_types)]
```

#### main函数
包含一个 `main` 函数的Crate被编译成一个可执行文件。

如果存在一个 `main` 函数，它的返回类型必须是 `()` 且没有任何参数。

## Item And Attribute
### Item
一个Item是Crate的一部分。Item通过一个嵌套的模块集被组织在一个Crate中。每个Crate都有一个最外层的匿名模块。Item在编译期完全被确定。

Item为分以下几种：
- **extern crate 声明**
- **use 声明**
- **模块**
- **函数**
- **类型声明**
- **结构体**
- **枚举**
- **常量Item**
- **静态Item**
- **Trait**
- **实现(implementation)**

## Expression And Statement

## 类型系统(Type System)
Rust程序中的每个变量、Item和值都有一个类型，一个值的类型定义了对它所拥有的内存的解释。

内建类型和类型构建器被紧密地集成到语言中，主要是因为语言本身很难模拟用户自定义类型，所以用户自定义类型有局限性(limited capabilities)。
### 类型(Type)
Rust没有类型抽象的概念，也就是说，Rust没有一个一切类型的父类来作为最高类（如Python中的object）。

#### 原始类型(Primitive Type)
原始类型主要有以下几种：

- 布尔类型`bool`：只有 `true` 和 `false` 两种值
- 机器类型(整数和浮点数)
- 依赖机器的整数类型

##### 机器类型
机器类型有以下几种：

- 无符号类型：`u8`、`u16`、`u32`和`u64`，其值域分别为：`[0, 2^8-1]`、`[0, 2^16-1]`、`[0, 2^32-1]`、`[0, 2^64-1]`。
- 有符号类型：`i8`、`i16`、`i32`、`i64`，其值域分别为：`[-(2^7), 2^7-1]`、`[-(2^15), 2^15-1]`、`[-(2^31), 2^31-1]`、`[-(2^63), 2^63-1]`。
- IEEE 754-2008 binary32 和 binary64 浮点类型：`f32`、`f64`。

注：上面的`^`表示次幂，如：`2^16` 表示 2 的 16 次幂。

##### 依赖机器的整数类型
`usize` 是无符号整数类型，它的位数(bits)和该平台上指针类型的位数相同，它能表示进程中的任意内存地址。

`isize` 是有符号整数类型，它的位数(bits)和该平台上指针类型的位数相同。绑定到一个对象和数组大小上的理论上限是 `isize` 类型的最大值，这将确保 `isize` 能够用于计算两个指向对象或数组的指针之差，同时能获取一个对象内的每个字节（从第一个字节到最后一个字节）的地址。

#### 文本类型(Textual Type)
类型 `char` 和 `str` 拥有文本数据。

`char` 类型的值是一个 Unicode 标量值（不是替代品的代码点————Unicode Code Point），它用一个32位无符号整数进行表示，范围从 0x0000 到 0xD7FF，以及从 0xE000 到 0x10FFFF。一个char数组(即 `[char]`)实际上是一个 UCS-4/UTF-32 字符串。

`str` 类型的值是一个 Unicode 字符串，它用一个 8 位无符号字节数组来表示，字节数组中的的每个字节都是一个 UTF-8 格式的 Unicode Code Point。由于 `str` 类型的大小是未知的，所以，它不是 `第一类(first-class)` 类型，但是它可以(_也只可以_)通过一个指针类型(如：`&str`)进行实例化。

#### 元组类型
一个元组类型可以包含各种其它类型的值，这些值被称为`元组的元素`。元组类型没有名义上的名字，而只是一个结构类型。

元组的类型和值分别用它们的元素的类型列表和值列表来表示，相应地，这个是一个用圆括号包围，并以逗号分隔的列表。

由于元组的元素没有名字，所以它们只能：(1)通过模式匹配访问；（2）直接使用 `N` 作为一个域来访问第 N 个元素。

```rust
type Pair<'a> = (i32, &'a str);
let p: Pair<'static> = (10, "ten");
let (a, b) = p;

assert_eq!(a, 10);
assert_eq!(b, "ten");
assert_eq!(p.0, 10);
assert_eq!(p.1, "ten");
```

注：由于历史原因和便捷性，没有任何元素的元组类型（即 `()`）通常叫做 `unit` 或 `the unit type`。

#### 数组(Array)和分片(Slice)类型
Rust 有两种列表类型：

- 数组：`[T; N]`
- 分片：`&[T]`

数组有一个固定大小，不能动态增长和缩减，但既可以在堆上分配，也可以在栈上分配。

分片是一个数组的视图(view)，它并不`拥有(own)`它指向的数据，只是`借用(borrow)`它。

数组和分片边界内的所有元素总是会被初始化，并对一个数组或分片的访问总是会进行边界检查。

宏 `vec!` 可以允许你创建一个 `Vec[T]` 类型的对象（它是在堆上分配数组的一个类型），它属于标准库中的一部分，但不属于语言本身。

```rust
// A stack-allocated array
let array: [i32; 3] = [1, 2, 3];

// A heap-allocated array
let vector: Vec<i32> = vec![1, 2, 3];

// A slice into an array
let slice: &[i32] = &vector[..];
```

#### 结构体类型(Struct)
一个结构体类型可以包含各种其它类型的值，这些值被称为`结构体的域(field)`，有的将`field`翻译成`字段`。

一个Struct的新实例可以通过一个`结构体表达式`来创建。

一个结构体的内存布局默认是未定义的，以便允许编译器进行优化，如：对域进行重新排序。但是，它可以通过属性 `#[repr(...)]` 进行固定，不允许编译器进行优化。在上述任何一种情况下，域都可以以相应于结构体表达式中的任何顺序而存在，因此，最终的结构体值总是拥有相同的内存布局。

结构体中的域可以被`可见性修改符(visibility modifiers)`来修改，以便允许在模块外访问结构体内的数据。

一个`元组结构体类型`像`结构体类型`一样，除了它的域是匿名的外。

一个`类unix结构体类型(unit-like struct type)`也像`结构体类型`一样，除了它没有域外。

#### 枚举类型(Enumerated)
一个枚举声明了一个类型和一些不同的构造器，这些构造器分别独立地被命名，并可以获取一组可选的参数。

一个枚举的新实例可以通过调用其中的某个构造器来创建。

一个枚举值的内存大小等于所有构造器所构造的对象中所需的最大内存，即哪个对象的内存最大，就等于哪个对象的内存大小。

#### 递归类型(Recursive)
名义类型（如`枚举`和`结构体`）都是可递归的。也就是说，每个枚举构造器或结构体域可以直接或间接地引用枚举或结构体它们自身。但是，这样的递归有一些限制：

- 递归中，递归类型必须包括一个名义类型。
- 一个递归的枚举元素必须至少有一个非递归的构造器，以便无限递归。
- 递归类型的大小必须是有限的，换句话说，**递归类型的递归域必须是个指针类型**。
- 递归类型定义可以跨模块边界，但不能跨模块的可见性边界和Crate边界。这样做的目的是了为简化模块系统和类型检查。

```rust
enum List<T> {
    Nil,
    Cons(T, Box<List<T>>)
}

let a: List<i32> = List::Cons(7, Box::new(List::Cons(13, Box::new(List::Nil))));
```

#### 指针类型(Pointer)
Rust中的所有指针都是显式的第一类(`first-class`)值，它们可以被复制、存储到数据结构中、从函数中返回，等等。

Rust中的指针主要有两种：`引用(References, &)`和`原指针(Raw Pointer, *)`。

##### 引用(Reference)
引用指向被其它值`拥有(own)`的内存。一个引用类型可以写成 `&type` 或 `&'a type`，后一种情况是当你须要显式地指定一个生存时间时使用。引用的拷贝是一个浅拷贝：它只拷贝指针本身。释放一个引用并不影响它所指向的值，但对于一个临时值的引用除外，即：一个临时值只在它的引用的作用域内存活。

##### 原指针(Raw Pointer)
原指针是没有安全和生存周期保证的指针，它可以写成 `*const T` 或 `*mut T`，如：`*const i32` 表示一个指针32位整数的原指针。复制和丢弃一个原指针不影响任何其它值的生命周期。解引用(dereference)一个原指针或将它转换成任何其它指针类型，都是不安全的操作(See unsafety)。不建议在Rust代码中使用原指针，它们之所以存在，主要是为了支持：(1)与外围代码(非Rust代码)的互操作性；(2)写对性能十分挑剔或更底层的功能。

注：标准库中包含一个`智能指针(smart pointer)`。

#### 函数类型(Function)
一个函数可以通过关键字`fn`进行定义。

一个函数类型包括：(1)一个可空的`函数类型修改符`集合(如unsafe、extern)，(2)一个参数类型序列，(3)一个返回值类型。

```rust
fn add(x: i32, y: i32) -> i32 {
    x + y
}

let mut x = add(5,7);

type Binop = fn(i32, i32) -> i32;
let bo: Binop = add;
x = bo(5,7);
```

#### 闭包类型(Closure)
一个`Lambda`表达式将产生一个闭包，它的类型是唯一的、不能被写出(written out)的匿名类型。

依赖于闭包的需要，它的类型实现了一或多个下面的闭包特性：

- **FnOnce**: 这样的闭包只能被调用一次，且能够把它环境中的值给`move out`出来。
- **FnMut**: 这样的闭包可以被调用多次，且能够修改它环境中的值。`FuMut`继承自`FnOnce`，也就是说，任何实现了`FnMut`的闭包同样也实现了`FnOnce`。
- **Fn**: 这样的闭包能够通过一个共享引用被调用多次。但是，这样闭包既不能把它环境中的值给`move out`出来，也不能修改它环境中的值。`Fn`继承自`FnMut`，因此，自然也继承自`FnOnce`。

#### 特性对象(Trait)
在Rust中，像 `&SomeTrait` 或 `Box<SomeTrait>` 这样的类型叫做`特性对象(trait object)`。

Trait对象的每个实例都包含：
- 一个`指针`：该指针指向实现了 `SomeTrait` 的类型 `T` 的实例。
- 一个`虚方法表(Virtual Method Table)`：一般又叫 `vtable`，它通常包含一个指向类型 T 的实现(即一个函数指针)。

Trait对象目的是为了允许方法的`晚绑定(late binding)`。在Trait对象上调用一个方法将在运行时引发虚拟派发(Virtual Dispatch)，也就是说，一个函数指针将从Trait对象的`vtable`中被加载，并间接调用。每个`vtable`实体的实际实现根据基础对象的不同而不同。

对于一个被实例化的Trait对象，Trait必须是对象安全的(`object-safe`)。对象安全性规则被定义在[Rust RFC 255](https://github.com/rust-lang/rfcs/blob/master/text/0255-object-safety.md)。

假如有一个指针类型表达式`E`，它的类型是 `&T` 或 `Box<T>`，其中 `T` 实现了 Trait `R`，把 `E` 转换成一个相应的指针类型 `&R` 或 `Box<R>` 将得到一个 Trait 对象 `R` 的值，该值可以表示成一对指针：`vtable` 指针(`R` 的 `T` 的实现)和`E`的指针值。

```rust
trait Printable {
    fn stringify(&self) -> String;
}

impl Printable for i32 {
    fn stringify(&self) -> String { self.to_string() }
}

fn print(a: Box<Printable>) {
    println!("{}", a.stringify());
}

fn main() {
    print(Box::new(10) as Box<Printable>);
}
```

#### 类型参数
在一个有类型参数声明的Item的主体中，它的类型参数的名字是类型。

```rust
// first 有类型 A，它引用 to_vec 的 A 类型参数。
// rest 有类型 Vec<A>，它的元素类型为 A。
fn to_vec<A: Clone>(xs: &[A]) -> Vec<A> {
    if xs.is_empty() {
        return vec![];
    }
    let first: A = xs[0].clone();
    let mut rest: Vec<A> = to_vec(&xs[1..]);
    rest.insert(0, first);
    rest
}
```

#### Self类型
一个特殊的类型`Self`在`Trait`和`实现(impl)`中有特殊的含义。在`Trait定义`中，它引用一个表示`implementing`类型的隐式类型参数，即实现该Trait的类型对象。在`实现(impl)`中，它是`implementing`类型的别名，即该类型对象的别名。

标识 `&self` 是 `self: &Self` 的缩写。

```rust
trait Printable {
    // Self 是 String 对象的引用
    fn make_string(&self) -> String;
}

impl Printable for String {
    // Self 是 String 对象的别名
    fn make_string(&self) -> String {
        (*self).clone()
    }
}
```

### 类型强制转换(Type Coercion)
强制转换(Coercion)被定义在[Rust RFC 401](https://github.com/rust-lang/rfcs/blob/master/text/0401-coercions.md)。

Coercion是隐式的，并没有任何显式语法。

Coercion在以下类型之间是被允许的：
- `T` to `U` if `T` is subtype of `U`(reflexive case)
- `T_1` to `T_3` where `T_1` coerces to `T_2` and `T_2` coerces to `T_3`(transitive case). Note that this is not fully supported yet
- `&mut T` to `&T`
- `*mut T` to `*const T`
- `&T` to `*const T`
- `&mut T` to `*mut T`
- `&T` to `&U` if `T` implements `Deref<Target = U>`. For example:
    ```rust
    use std::ops::Deref;

    struct CharContainer {
      value: char
    }

    impl Deref for CharContainer {
      type Target = char;

      fn deref<'a>(&'a self) -> &'a char {
          &self.value
      }
    }

    fn foo(arg: &char) {}

    fn main() {
      let x = &mut CharContainer { value: 'y' };
      foo(x); //&mut CharContainer is coerced to &char.
    }
    ```
- `&mut T` to `&mut U` if `T` implements `DerefMut<Target = U>`
- TyCtor(`T`) to TyCtor(coerce_inner(`T`)), where TyCtor(`T`) is one of
    - `&T`
    - `&mut T`
    - `*const T`
    - `*mut T`
    - `Box<T>`

    and where - coerce_inner([T, ..n]) = [T] - coerce_inner(T) = U where T is a concrete type which implements the trait U.

    In the future, coerce_inner will be recursively extended to tuples and structs. In addition, coercions from sub-traits to super-traits will be added. See RFC401 for more details.

## 内存模型(Memory Model)
一个Rust程序的内存包含一组静态的Item和一个堆。对于堆，不可修改的部分可以在线程间被安全地共享，而可修改的部分不能被安全地共享，但是有一些机制可以保证可修改的值和不安全的代码被安全地共享。

在栈上分配的是`变量(variable)`，在堆上分配的是`box`。

### 内存分配和生存时间
Rust程序中的Item包括`函数(function)`、`模块(module)`、`类型(type)`，且类型的值会在编译期被计算，并唯一地存储在Rust进程的内存镜像中。这些 Item 既不会被动态地分配，也不会被动态地释放。

堆(heap)是一个描述`box`的一般术语。在堆上，一个分配的生命周期依赖于指向它的`box`的生命周期。由于`box`的值可以被传入/传出栈桢(frame)，或者存储在堆上，所以，堆分配可能比分配它的栈桢(frame)存活的更久。

### 内存拥有权
当退出一个栈桢(frame)时，在它本地分配的所有内存都会被释放，并且对`box`的引用也将会被丢弃掉。

### 变量
一个变量是一个栈桢的组成成分，可能是一个命名的函数参数，或者是一个匿名的临时值，亦或是一个命名的本地变量。

一个本地变量（即在本地栈上分配的）直接拥有一个在栈内存中分配的值，该值是栈桢的一部分。

本地变量是不可变的，除非用关键字`mut`声明，如：`let mut x = ...`。

函数参数也是不可变的，除非用关键字`mut`声明，并且关键字`mut`作用于其后紧邻的参数。如：`|mut x, y|` 和 `fn f(mut x: Box<i32>, y: Box<i32>)` 都声明了参数 x 是可变的，但参数 y 是不可变的。

和普通参数相似，对于接收`self`或`Box<Self>`的方法，可以在它们前面添加 `mut`，使其变为一个可修改变量。
```rust
trait Changer {
    fn change(mut self) -> Self;
    fn modify(mut self: Box<Self>) -> Box<Self>;
}
```

本地变量在分配时不会被初始化。本地变量会在当前栈桢上立即分配，但不会初始化它们，在一个函数中，其后的语句可能会/也不可能会初始化本地变量。但是本地变量只能在它们被初始化后才能使用，这是编译器强制要求的。

## 链接(Linkage)
Rust编译器支持多种途径把Crate静态或动态地链接在一起。

在一个编译会话中，编译器能够通过命令行链接标志或`crate_type`属性来产生多个工件(artifacts)；但如果在命令行指定一个或多个链接标志，则所有的`crate_type`属性都将被忽略。

命令行链接标志和`crate_type`属性：
- **--crate_type=bin, #[crate_type="bin"]**：一个可运行的可执行文件将被产生，这要求在将被运行的Crate中有一个`main`函数。这会链接所有Rust和本地的依赖，并产生一个可发布的二进制程序。
- **--crate_type=lib, #[crate_type="lib"]**
- **--crate-type=dylib, #[crate_type = "dylib"]**
- **--crate-type=staticlib, #[crate_type = "staticlib"]**
- **--crate-type=rlib, #[crate_type = "rlib"]**

一般情况下，`--crate_type=bin` 或 `--crate_type=lib` 应当对于所有的编译需要都是有效的；其它选项仅当以下情况可见：对于一个Rust Crate的输出格式，如果需要更细粒度的控制。

## 非安全代码(Unsafety)
不安全的操作是那些可能违反Rust静态语义的内存安全保证的操作。

下面的语言级特性不能使用在Rust的安全子集中：
- 解引用一个原指针
- 读写一个可修改的静态变量
- 调用一个不安全的函数（包括Rust函数和非Rust函数）

## 影响(Influence)
在设计上，Rust从其它语言借鉴了一些特性，下面包含一个列表（包括曾经借鉴但后来又被删除的特性）：

- **SML, OCaml**: algebraic data types, pattern matching, type inference, semicolon statement separation
- **C++**: references, RAII, smart pointers, move semantics, monomorphization, memory model
- **ML Kit, Cyclone**: region based memory management
- **Haskell(GHC)**: typeclasses, type families
- **Newsqueak, Alef, Limbo**: channels, concurrency
- **Erlang**: message passing, thread failure, ~~linked thread failure, lightweight concurrency~~
- **Swift**: optional bindings
- **Scheme**: hygienic macros
- **C#**: attributes
- **Ruby**：~~block syntax~~
- **NIL, Hermes**: ~~typestate~~
- **Unicode Annex #31**: identifier and pattern syntax
