(摘录)翻译自：[Rust Reference](http://doc.rust-lang.org/reference.html)

注：首次摘录翻译时参考的 `Rust` 版本是 `1.8.0`，后续会根据新版本的变动进行更新。

`第一部分(Introduction)`、`第二部分(Notation)` 未翻译，主要是因为笔者觉得这两部分没必要翻译。另外，本文是「摘录」翻译，并不是一句一句、原封不动地翻译。

------

### 目录（Content）

- [1. 词法结构](1-词法结构)
	- [1.1 源代码编码（Input Format）](11-源代码编码input-format)
	- [1.2 标识符（Identifier）](12-标识符identifier)
	- [1.3 注释（Comment）](13-注释comment)
		- [1.3.1 代码注释](131-代码注释)
		- [1.3.2 文档注释](132-文档注释)
			- [1.3.2.1 注释文档后的代码](1321-注释文档后的代码)
			- [1.3.2.2 注释包含该文档的代码](1322 注释包含该文档的代码)
	- [1.4 空白（Whitespace）](14-空白whitespace)
	- [1.5 字面值（Literal）](15-字面值literal)
		- [1.5.1 字符和字符串字面值](151-字符和字符串字面值)
			- [1.5.1.1 字符字面值](1511-字符字面值)
			- [1.5.1.2 字符串字面值](1512-字符串字面值)
			- [1.5.1.3 转义字符](1513-转义字符)
			- [1.5.1.4 Raw字符串字面值](1514-raw字符串字面值)
		- [1.5.2 字节和字节字面值](152-字节和字节字面值)
			- [1.5.2.1 字节字面值](1521-字节字面值)
			- [1.5.2.2 字节字符串字面值](1522-字节字符串字面值)
			- [1.5.2.3 Raw字节字符串字面值](1523-raw字节字符串字面值)
		- [1.5.3 数值字面值](153-数值字面值)
			- [1.5.3.1 整数字面值](1531-整数字面值)
			- [1.5.3.2 浮点数字面值](1532-浮点数字面值)
		- [1.5.4 布尔字面值](154-布尔字面值)
		- [1.5.5 例子](155-例子)
			- [1.5.5.1 字符和字符串](1551-字符和字符串)
			- [1.5.5.2 字节转义字符](1552-字节转义字符)
			- [1.5.5.3 数字](1553-数字)
			- [1.5.5.4 类型后缀](1554-类型后缀)
	- [1.6 路径（Path）](16-路径path)
- [2 语法扩展（Syntax Extension）](2-语法扩展syntax-extension)
	- [2.1 宏（Macro）](21-宏macro)
		- [2.1.1 样式宏](211-样式宏)
		- [2.1.2 解析限制](212-解析限制)
- [3 Crate和源文件](3-crate和源文件)
	- [3.1 `main`函数](31-main函数)
- [4 Item和属性（Attribute）](4-item和属性attribute)
	- [4.1 Item](41-item)
	- [4.2 可见性（Visibility）和私有性（Privacy）](42-可见性visibility和私有性privacy)
		- [4.2.1 重导出（Re-Export）及其可见性（Visibility）](421-重导出re-export及其可见性visibility)
	- [4.3 属性（Attribute）](43-属性attribute)
- [5 表达式（Expression）和语句（Statement）](5-表达式expression和语句statement)
	- [5.1 语句（Statement）](51-语句statement)
		- [5.1.1 声明语句](511-声明语句)
			- [5.1.1.1 Item声明](5111-item声明)
			- [5.1.1.2 `let`语句](5112-let语句)
		- [5.1.2 表达式语句](512-表达式语句)
	- [5.2 表达式（待写）](52-表达式)
- [6 类型系统（Type System）](6-类型系统type-system)
	- [6.1 类型（Type）](61-类型type)
		- [6.1.1 原始类型（Primitive Type）](611-原始类型primitive-type)
			- [6.1.1.1 机器类型](6111-机器类型)
			- [6.1.1.2 依赖机器的整数类型](6112-依赖机器的整数类型)
		- [6.1.2 文本类型（Textual Type）](612-文本类型textual-type)
		- [6.1.3 元组类型](613-元组类型)
		- [6.1.4 数组（Array）和分片（Slice）类型](614-数组array和分片slice类型)
		- [6.1.5 结构体类型（Struct）](615-结构体类型struct)
		- [6.1.6 枚举类型（Enumerated）](616-枚举类型enumerated)
		- [6.1.7 递归类型（Recursive）](617-递归类型recursive)
		- [6.1.8 指针类型（Pointer）](618-指针类型pointer)
			- [6.1.8.1 引用（Reference）](6181-引用reference)
			- [6.1.8.2 原指针（Raw Pointer）](6182-原指针raw-pointer)
		- [6.1.9 函数类型（Function）](619-函数类型function)
		- [6.1.10 闭包类型（Closure）](6110-闭包类型closure)
		- [6.1.11 特性对象（Trait）](6111-特性对象trait)
		- [6.1.12 类型参数](6112-类型参数)
		- [6.1.13 `Self`类型](6113-self类型)
	- [6.2 子类型（Subtyping）](62-子类型subtyping)
	- [6.3 类型强制转换（Type Coercion）](63-类型强制转换type-coercion)
		- [6.3.1 强制场所（Coercion Sites）](631-强制场所coercion-sites)
		- [6.3.2 强制类型（Coercion Types）](632-强制类型coercion-types)
- [7 Special `Trait`](7-special-trait)
	- [7.1 `Copy` Trait](71-copy-trait)
	- [7.2 `Sized` Trait](72-sized-trait)
	- [7.3 `Drop` Trait](73-drop-trait)
	- [7.4 `Deref` Trait](74-deref-trait)
- [8 内存模型（Memory Model）](8-内存模型memory-model)
	- [8.1 内存分配和生存时间](81-内存分配和生存时间)
	- [8.2 内存拥有权](82-内存拥有权)
	- [8.3 变量](83-变量)
- [9 链接（Linkage）](9-链接linkage)
- [10 非安全代码（Unsafety）](10-非安全代码unsafety)
	- [10.1 不安全函数（Unsafe Function）](101-不安全函数unsafe-function)
	- [10.2 不安全代码块（Unsafe Block）](102-不安全代码块unsafe-block)
	- [10.3 被认为未定义的行为（Behavior Considered Undedined）](103-被认为未定义的行为behavior-considered-undefined)
	- [10.4 并不认为不安全的行为（Behavior Not Considered Unsafe）](104-并不认为不安全的行为behavior-not-considered unsafe)
- [11 灵感（Influence）](11-灵感unfluence)


------

## 1 词法结构
### 1.1 源代码编码(Input Format)
（1）Rust 源代码被作为 `UTF8` 编码的Unicode字符进行解析。所以，Rust 源代码文件必须保存为 `UTF8` 编码。

### 1.2 标识符(Identifier)
（1）单个下划线(**`_`**)字符不是一个标识符。

（2）标识符可以是任何非空 Unicode 字符串。

（3）`关键字` 具有特殊含义，不能用作标识符。


### 1.3 注释(Comment)
Rust 的注释分为两种：**`代码注释`** 和 **`文档注释`**。

#### 1.3.1 代码注释
代码注释采用 C++ 风格的注释：**`行注释`** (`//`) 和 **`块注释`** (`/* ... */`)。

与 C++ 不同，Rust 的块注释可以被嵌套，但必须匹配成对；另外，代码注释会被解析成空白。

#### 1.3.2 文档注释
文档注释也分为两种：**`注释文档后的代码`**和**`注释包文档的代码`**。

这些注释作为所被注释的代码的文档存在，而不是被解析成空白。

##### 1.3.2.1 注释文档后的代码
此文档注释分为两种：**`行文档`**(`///`)和**`块文档`**(`/** ... */`)。

这两种文档注释等价于文档属性 **`#[doc="..."]`**，即它们可以被转换成此文档属性。

这些注释会被作为其后代码的文档。

##### 1.3.2.2 注释包含该文档的代码
此文档注释分为两种：**`行文档`**(`//!`)和**`块文档`**(`/*! ... */`)。

这两种文档注释等价于文档属性 **`#![doc="..."]`**，即它们可以被转换成此文档属性。

这些注释会被作为包含该文档的代码的文档，而不是文档后的代码的文档。

**`//!`** 注释通常用于模块的文档，即作为整个模块的文档。

### 1.4 空白(Whitespace)
只有这些字符 `U+0020(space, ' ')`、`U+0009(tab, '\t')`、`U+000A(LF, '\n')`、`U+000D(CR, '\r')` 才会被作为空白。

这些空白字符仅用于分隔语法Token（或者说分隔字符序列），除此之外，没有任何意义。

### 1.5 字面值(Literal)
#### 1.5.1 字符和字符串字面值
##### 1.5.1.1 字符字面值
一个字符字面值是用一对单引号(`'`)包围的、除单引号本身之外的单个Unicode字符。对于单引号字符字面值，必须使用反斜杠进行转义，如：`'\''`。

##### 1.5.1.2 字符串字面值
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

##### 1.5.1.3 转义字符
转义字符只在 **_字符字面值_** 或 **_非原始（non-Raw）字符串字面值_** 中有意义，在原始（Raw）字符串中没有意义，它们是两个或多个字符。

转义字符以一个 `反斜杠`(`\`) 开头，具体的规则参见下面的例子。

##### 1.5.1.4 Raw字符串字面值
Raw字符串字面值开始于`字符r`，后面紧跟着 `0或多个` 井号(`#`)以及 `一个` 双引号(`"`)，之后可以包含 `0或多个` 任何Unicode字符，最后终止于 `一个` 双引号(`""`)以及和先前的井号 `数目相同` 的井号(`#`)。

Raw字符串字面值不处理任何转义，其中的字符都表示它们自身，双引号（除了最后在`#`之前的那个双引号）和反斜杠没有任何特殊含义。

```rust
"foo"; r"foo";                     // foo
"\"foo\""; r#""foo""#;             // "foo"

"foo #\"# bar";
r##"foo #"# bar"##;                // foo #"# bar

"\x52"; "R"; r"R";                 // R
"\\x52"; r"\x52";                  // \x52
```

#### 1.5.2 字节和字节字面值
##### 1.5.2.1 字节字面值
字符字面值的规则同样适用于字节字面值，只不过，字节字面值前多个 **`字符b`**，以及其值域为ASCII码（U+0000 ~ U+007F）。

字节字面值等价于一个8位无符号整数(即`u8`)字面值。

##### 1.5.2.2 字节字符串字面值
字符串字面值的规则同样适用于字节字符串字面值，只不过，字节字符串字面值前多个 **`字符b`**，以及其值域为ASCII码。

一个长度为 n 的字节字符串字面值等价于一个 `borrowed` 型且大小固定的 8 位无符号整数数组，即 `&'static [u8; n]`。

##### 1.5.2.3 Raw字节字符串字面值
Raw字符串字面值的规则同样适用于Raw字节字符串字面值，只不过，Raw字节字符串字面值前多个 **`字符b`**，以及其值域为ASCII码。

```rust
b"foo"; br"foo";                     // foo
b"\"foo\""; br#""foo""#;             // "foo"

b"foo #\"# bar";
br##"foo #"# bar"##;                 // foo #"# bar

b"\x52"; b"R"; br"R";                // R
b"\\x52"; br"\x52";                  // \x52
```

#### 1.5.3 数值字面值
一个数值字面值包含 **`整数字面值`** 和 **`浮点数字面值`**。

##### 1.5.3.1 整数字面值
一个整数字面值有四种形式：**`二进制`**、**`八进制`**、**`十进制`**、**`十六进制`**。

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

##### 1.5.3.2 浮点数字面值
一个浮点数有下面两种形式：

    (1) 一个十进制字面值后紧跟一个圆点(`.`)，并可选地后跟另一个十进制字面值，以及一个可选的`指数部分(exponent)`，
        如：123.、12.3、12.3E+2。
    (2) 单个十进制字面值后紧跟一个`指数部分(exponent)`，如：12E+9。

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

#### 1.5.4 布尔字面值
布尔类型只有两个字面值：**`true`** 和 **`false`**。

#### 1.5.5 例子
##### 1.5.5.1 字符和字符串
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

##### 1.5.5.2 字节转义字符
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

##### 1.5.5.3 数字
| Number literals |   Example   | Exponentiation | Suffixes |
|-----------------|-------------|----------------|----------|
|Decimal integer  | 98_222      | N/A            | Integer suffixes |
|Hex integer      | 0xff        | N/A            | Integer suffixes |
|Octal integer    | 0o77        | N/A            | Integer suffixes |
|Binary integer   | 0b1111_0000 | N/A            | Integer suffixes |
|Floating-point   | 123.0E+77   | Optional       | Floating-point suffixes |

**所有数字字面值都可以在其中插入下划线(`_`)进行分隔，以使其更具有可读性。如：1_234.0E+18f64。**

##### 1.5.5.4 类型后缀
|Integer | Floating-point |
|--------|----------------|
|`u8`, `i8`, `u16`, `i16`, `u32`, `i32`, `u64`, `i64`, `isize`, `usize` | `f32`, `f64` |

### 1.6 路径(Path)
一个 `路径` 是一个或多个组件(components)的序列，它们被命名空间(namespace)修饰符(即双冒号 `::`)分隔。如果一个路径只包含一个组件，那么它可能引用一个 `Item` 或本地作用域中的一个变量；如果一个路径有多个组件，那么它引用一个 `Item`。 See `Item`。

每一个 Item 在它的 Crate 中都有一个标准路径，但表示一个 Item 的路径仅在一个 Crate 中才有意义。没有跨 Crate 的全局命名空间，一个 Item 的标准路径只是在 Crate 中标识它。

```rust
x;
x::y::z;
```

路径组件通常是标识符，但也有可能包含尖括号(`<>`)包围的类型参数列表。在一个表达式上下文，该类型参数列表跟随在命名空间修饰符(`::`)之后，目的是为了区别于包含小于符号(`<`)的关系表达式；在类型表达式上下文，最后一个命名空间修饰符(`::`)可以被省略。

```rust
type T = HashMap<i32,String>; // Type arguments used in a type expression
let x  = id::<i32>(10);       // Type arguments used in a call expression
```

路径可通过前导的修饰符来改变解析路径的方法。

(1) 以 `::` 开头的路径被作为 `全局路径`，路径中的组件从 `根(root)` Crate 开始解析，且路径中的每个标识符都必须被解析成一个 `Item`。
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

(2) 以关键字 `super` 开头的路径从 `当前模块的父模块` 开始解析，其中的每个标识符都必须被解析成一个 `Item`。
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

(3) 以关键字 `self` 开头的路径从 `当前模块` 开始解析，其中的每个标识符都必须被解析成一个 `Item`。
```rust
fn foo() {}
fn bar() {
    self::foo();
}
```

注：关键字 `super` 可以在第一个 `super` 或 `self` 后重复多次，以引用相应的祖先模块。
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

## 2 语法扩展(Syntax Extension)

在 Rust 中，一些并不特别重要的次要特性，并没有其自己的语法，也没有作为函数被实现。相反，它们有名字，并通过一致的语法被调用：`some_extension!(...)`。

rustc 的用户有两种方式来定义新的语法扩展：

    (1) 编译器插件：可以包含能在编译期操作语法树的任何 Rust 代码。注意：这种方式的接口有很大的不稳定性，随时可能被改变。
    (2) 宏(Macro)：以一个高层次、声明式的方式来定义一个语法。

### 2.1 宏(Macro)

`macro_rules`允许用户以声明的方式来定义一个语法扩展，我们称为 `样式宏(macros by example)` 或简称为 `宏(macros)`，以区别`编译器插件`中定义的`过程式宏(procedural macros)`。

目前，宏可以被扩展为 **`表达式`**、**`语句`**、**`Item`** 或 **`模式(pattern)`**。

一个 `sep_token` 是除 **`*`** 和 **`+`** 外任意 Token；一个 `non_special_token` 是除 **`界定符(delimiter)`** 和 **`$`** 外的任意 Token。

**_宏扩展会通过名字查找宏调用，依次尝试匹配每个宏规则，并转译第一个成功的匹配。_**匹配和转译是相互密切相关的。

#### 2.1.1 样式宏
宏扩展匹配(match)并转译(transcribe)每一个不是以 **`$`** 开头的 Token，包括`界定符`。由于解析的原因，界定符必须均衡，但是并不特别。

在匹配器中，**`$ name : designator`** 匹配命名为 **`designator`** 的非终止符。有效的 designator 有：

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

在匹配器和转译器中，克林星型操作符（Kleene Star Operator）包含 **`$`** 和 **圆括号对`()`**，可选地后面紧跟着一个 `分隔符(separator)`，以及 **`*`** 或 **`+`**；其中，**`*`** 表示 `0或多次重复`，**`+`**表示 `1或多次重复`，`圆括号对` 并不被匹配和转译。在匹配器中，一个名字被绑定到它匹配的所有名字；而转译器则是对这些匹配的名字进行排序。

这些重复操作的转义规则被称为 **`Macro By Example`**。Essentially, one "layer" of repetition is discharged at a time, and all of them must be discharged by the time a name is transcribed. Therefore, **`( $( $i:ident ),* ) => ( $i )`** is an invalid macro, but **`( $( $i:ident ),* ) => ( $( $i:ident ),* )`** is acceptable (if trivial).

当样式宏碰到一个重复时，它会检查所有出现在它的主体中的 **`$ name`**。在当前层(current layer)，它们都必须重复相同的次数，所以 **`( $( $i:ident ),* ; $( $j:ident ),* ) => ( $( ($i,$j) ),* )`** 对 **`(a,b,c ; d,e,f)`** 是有效的，对 **`(a,b,c ; d,e)`** 是无效的。这个重复操作将前后一致地遍历选择项(choices)，所以，前一个输入将被转译成 **`(a,d), (b,e), (c,f)`**。

#### 2.1.2 解析限制
Rust语言的宏系统解析器虽然相当强大，但却有两个限制：

    (1) 在解析Rust语法的表达式和其它位(bits)后，宏定义必须包含适当的分隔符(separator)。
        这意味着，像 `$i:expr [ , ]` 这样的宏定义不是合法的，因为 `[` 可以作为表达式的一部分；
        而像 `$i:expr,` 或 `$i:expr;` 这样的宏定义是合法的，因为 `,` 和 `;` 是合法的分隔符。
    (2)解析器在遇到 `$ name : designator` 时，必须消除二义性。

## 3 Crate 和 源文件
Rust语言作为一个编译器而被实现，并区分编译时间和运行时间。静态语义规则会在编译时间阶段控制编译的成功或失败；动态语义规则在运行时间阶段控制程序的行为。

Rust中的库以 `Crate` 的形式被组织。每个编译以单个源文件的形式来处理 Crate，如果成功，将会产生单个二进制形式的 Crate：要么是个可执行文件，要么是一些库。

**_一个 Crate 是一个编译和链接单元，以及版本、分发和运行时加载。_**一个 Crate 包含一个嵌套的模块作用树，这个树的顶层是一个匿名模块，并且在这个 Crate 中的任何 Item 都有一个统一的模块路径，用于表示该 Item 在 Crate 模块树中的路径。

**`Rust编译器总是把单个源代码文件作为输入，并总是产生单个Crate输出；这个源代码文件的处理可能导致其它源代码文件被作为模块加载。`**源代码文件的扩展名为 **`.rs`**。

一个Rust源代码文件描述了一个模块，它的名字和位置从源文件的外部被定义：要么在一个引用源文件中指定一个显式的 `mod_item`，要么使用 Crate 它自身的名字。每个源文件都是一个模块，但并不是每个模块都需要它自己的源文件，比如：模块定义能够被嵌套在一个文件中。

**_每个源文件都包含 `0或多个` Item 定义，也可以选择性地开始于任意数目的、作用在包含它的模块上的 `属性(attribute)`，这些属性大部分都可影响、改变编译器的行为。匿名 Crate 模块可以有额外的、作用于整个 Crate 上的`属性`。_**

```rust
// Specify the crate name.
#![crate_name = "projx"]

// Specify the type of output artifact.
#![crate_type = "lib"]

// Turn on a warning.
// This can be done in any module, not just the anonymous crate module.
#![warn(non_camel_case_types)]
```

### 3.1 main函数
包含一个 **`main`** 函数的Crate被编译成一个可执行文件。

如果存在一个 `main` 函数，它的返回类型必须是 **`()`** 且 **`没有任何参数`**。

## 4 Item 和 属性(Attribute)

### 4.1 Item
一个 Item 是 Crate 的一部分。Item 通过一个嵌套的模块集被组织在一个 Crate 中。每个 Crate 都有一个最外层的匿名模块。Item 在编译期完全被确定。

Item 为分以下几种：
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

### 4.2 可见性(Visibility) 和 私有性(Privacy)
在 Rust 中，所有的一切默认都是私有的(private)，除了一个例外：对于一个 `pub` 的 `枚举(Enum)`，其中的 `变体(variant)`(即成员) 默认也是公有的。

```rust
// Declare a private struct
struct Foo;

// Declare a public struct with a private field
pub struct Bar {
    field: i32,
}

// Declare a public enum with two public variants
pub enum State {
    PubliclyAccessibleState,
    PubliclyAccessibleState2,
}
```

对于 `公有性(public)` 和 `私有性(private)`，Rust 允许以下两种方法访问一个 Item：

    (1) 如果一个Item是公有的，那么可以从外部通过它的任何公有祖先来访问它。
    (2) 如果一个Item是私有的，那么它只能被当前模块和它的子孙访问。

注：**`访问`** 即 **`可见(visiable)`**，也就是说，如果一个Item对外 `可见`，那么外部就可以 `访问` 它，至于如何 `访问`，依赖于该 Item 是什么。比如：如果 Item 是一个模块，`访问` 意味着 `可以在该模块中查找另一个Item`；如果 Item 是一个函数，`访问` 意味着 `可以调用函数`。

```rust
// This module is private, meaning that no external crate can access this
// module. Because it is private at the root of this current crate, however, any
// module in the crate may access any publicly visible item in this module.
mod crate_helper_module {

    // This function can be used by anything in the current crate
    pub fn crate_helper() {}

    // This function *cannot* be used by anything else in the crate. It is not
    // publicly visible outside of the `crate_helper_module`, so only this
    // current module and its descendants may access it.
    fn implementation_detail() {}
}

// This function is "public to the root" meaning that it's available to external
// crates linking against this one.
pub fn public_api() {}

// Similarly to 'public_api', this module is public so external crates may look
// inside of it.
pub mod submodule {
    use crate_helper_module;

    pub fn my_method() {
        // Any item in the local crate may invoke the helper module's public
        // interface through a combination of the two rules above.
        crate_helper_module::crate_helper();
    }

    // This function is hidden to any module which is not a descendant of
    // `submodule`
    fn my_implementation() {}

    #[cfg(test)]
    mod test {

        #[test]
        fn test_my_implementation() {
            // Because this module is a descendant of `submodule`, it's allowed
            // to access private items inside of `submodule` without a privacy
            // violation.
            super::my_implementation();
        }
    }
}
```

#### 4.2.1 重导出(Re-Export)及其可见性(Visibility)
Rust 允许将一个 Item 通过 **`pub use`** 指令在当前模块中以公有的方式重新导出，也就是说，被 **`pub use`** 重新导出的 Item 就像在当前模块重新定义了一样，并且其访问性为公有的，且遵循上述的访问规则，同时，任何外部的模块或Crate都可以通过当前模块去访问它，这意味着，我们可以通过这种方式来简化一个Item的路径。如：
```rust
pub use self::implementation::api;

mod implementation {
    pub mod api {
        pub fn f() {}
    }
}
```


### 4.3 属性(Attribute)
对于任何Item的声明，都可以将一个属性作用它身上，以影响编译器对它的行为。Rust 中的属性规则遵循 ECMA-335 规范，该规范来源于 ECMA-334(C#)。

一个属性就是一个普通的、形式自由的元数据，它在解析时会依据名字、惯例(vonvention)、语言、以及编译器版本的不同而不同。

属性可以有以下形式：
- 单个标识符，即属性名。
- 标识符后跟着一个 `等号(=)` 和 一个字面值，作为一个 `键/值` 对。
- 标识符后跟着一个圆括号列表，它用来表示子属性参数。

一个属性以一个 **`井号(#)`** 开头，且该属性作用到其后的 Item 声明上；如果 `井号(#)` 后紧跟着一个 **`叹号(!)`**，那么，该属性作用到包含该属性的 Item 声明上。

```rust
// General metadata applied to the enclosing module or crate.
#![crate_type = "lib"]

// A function marked as a unit test
#[test]
fn test_foo() {
    /* ... */
}

// A conditionally-compiled module
#[cfg(target_os="linux")]
mod bar {
    /* ... */
}

// A lint attribute used to suppress a warning/error
#[allow(non_camel_case_types)]
type int8_t = i8;
```

**Notice**

    在将来某个版本中，编译器可能会区分 语言保留 和 用户可见 的属性，但是目前这两种之间没有什么不同。

关于各种不同的属性，参见 [Rust官方的语言规范](https://doc.rust-lang.org/reference.html#crate-only-attributes)`。


## 5 表达式(Expression) 和 语句(Statement)
Rust 是一个以表达式为主的语言。

### 5.1 语句(Statement)
`语句` 是 `块` 的一个组成成分，而 `块` 是更外边的表达式或函数的一个组成成分。

Rust 中只有两种语句：**`声明语句`** 和 **`表达式语句`**。

#### 5.1.1 声明语句
一个声明语句引入一个或多个名字到包围它的语句块，被声明的名字可以表示新的变量或新的 Item。

##### 5.1.1.1 Item 声明
在语句块中的 Item 声明语句和在模块中的 Item 声明有相同的语法形式，并且声明的该 Item 被严格地限制在当前语句块中，即被声明的该 Item 只在当前语句块中可见。

##### 5.1.1.2 `let` 语句
一个 `let` 语句可以以模式形式引入了一组变量。模式后可以跟随一个类型注解和一个初始化表达式；如果没有类型注解，编译器则会推断它的类型；如果类型信息不足，则引发一个异常。

**_被一个变量声明引入的任何变量的作用域（也即是可见性），从声明处开始，一直持续到包围它的块作用域的结束。_**

#### 5.1.2 表达式语句
一个表达式语句是一个只计算表达式但忽略它的结果的语句。对于一个表达式语句 `e;`，不管 `e` 的类型是什么，该表达式语句的类型总是 **`()`**。一般来说，一个表达式语句的目的主要是为了计算该表达式所带来的副作用。

### 5.2 表达式


## 6 类型系统(Type System)
Rust程序中的每个变量、Item和值都有一个类型，一个值的类型定义了对它所拥有的内存的解释。

内建类型和类型构建器被紧密地集成到语言中，主要是因为语言本身很难模拟用户自定义类型，所以用户自定义类型有局限性(limited capabilities)。
### 6.1 类型(Type)
Rust没有类型抽象的概念，也就是说，Rust没有一个一切类型的父类来作为最高类（如Python中的object）。

#### 6.1.1 原始类型(Primitive Type)
原始类型主要有以下几种：

- 布尔类型`bool`：只有 `true` 和 `false` 两种值
- 机器类型(整数和浮点数)
- 依赖机器的整数类型

##### 6.1.1.1 机器类型
机器类型有以下几种：

- **`无符号类型：`** `u8`、`u16`、`u32`和`u64`，其值域分别为 `[0, 2^8-1]`、`[0, 2^16-1]`、`[0, 2^32-1]`、`[0, 2^64-1]`。
- **`有符号类型：`** `i8`、`i16`、`i32`、`i64`，其值域分别为 `[-(2^7), 2^7-1]`、`[-(2^15), 2^15-1]`、`[-(2^31), 2^31-1]`、`[-(2^63), 2^63-1]`。
- **`浮点类型：`** `f32`、`f64`。

**注：**

    (1) 上面的`^`表示次幂，如：`2^16` 表示 2 的 16 次幂。
    (2) 浮点类型的标准为 IEEE 754-2008 binary32 和 binary64。

##### 6.1.1.2 依赖机器的整数类型
**`usize`** 是无符号整数类型，它的位数(bits)和该平台上指针类型的位数相同，它能表示进程中的任意内存地址。

**`isize`** 是有符号整数类型，它的位数(bits)和该平台上指针类型的位数相同。绑定到一个对象和数组大小上的理论上限是 `isize` 类型的最大值，这将确保 `isize` 能够用于计算两个指向对象或数组的指针之差，同时能获取一个对象内的每个字节（从第一个字节到最后一个字节）的地址。

#### 6.1.2 文本类型(Textual Type)
类型 **`char`** 和 **`str`** 拥有文本数据。

**`char`** 类型的值是一个 Unicode 标量值（不是替代品的代码点————Unicode Code Point），它用一个32位无符号整数进行表示，范围从 `0x0000` 到 `0xD7FF`，以及从 `0xE000` 到 `0x10FFFF`。一个 char 数组(即 `[char]`)实际上是一个 UCS-4/UTF-32 字符串。

**`str`** 类型的值是一个 Unicode 字符串，它用一个 8 位无符号字节数组来表示，字节数组中的的每个字节都是一个 UTF-8 格式的 Unicode Code Point。由于 `str` 类型的大小是未知的，所以，它不是 `第一类(first-class)` 类型，但是它可以(**_也只可以_**)通过一个指针类型(如：`&str`)进行实例化。

#### 6.1.3 元组类型
一个元组类型可以包含各种其它类型的值，这些值被称为`元组的元素`。元组类型没有名义上的名字，而只是一个结构类型。

元组的 类型 和 值 分别用它们的元素的 类型列表 和 值列表 来表示，相应地，这个是一个用圆括号包围，并以逗号分隔的列表。

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

#### 6.1.4 数组(Array)和分片(Slice)类型
Rust 有两种列表类型：

- **数组：**`[T; N]`
- **分片：**`&[T]`

数组有一个固定大小，不能动态增长和缩减，但既可以在堆上分配，也可以在栈上分配。

分片是一个数组的视图(view)，它并不 **`拥有(own)`** 它指向的数据，只是 **`借用(borrow)`** 它。

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

#### 6.1.5 结构体类型(Struct)
一个结构体类型可以包含各种其它类型的值，这些值被称为`结构体的域(field)`，有的将`field`翻译成`字段`。

一个 struct 的新实例可以通过一个`结构体表达式`来创建。

一个结构体的内存布局默认是未定义的，以便允许编译器进行优化，如：对域进行重新排序。但是，它可以通过属性 **`#[repr(...)]`** 进行固定，不允许编译器进行优化。在上述任何一种情况下，域都可以以相应于结构体表达式中的任何顺序而存在，因此，最终的结构体值总是拥有相同的内存布局。

结构体中的域可以被 `可见性修改符(visibility modifiers)` 来修改，以便允许在模块外访问结构体内的数据。

一个 `元组结构体类型` 像 `结构体类型` 一样，除了它的域是匿名的外。

一个 `类unix结构体类型(unit-like struct type)` 也像 `结构体类型` 一样，除了它没有域外。

#### 6.1.6 枚举类型(Enumerated)
一个枚举声明了一个类型和一些不同的构造器，这些构造器分别独立地被命名，并可以获取一组可选的参数。

一个枚举的新实例可以通过调用其中的某个构造器来创建。

一个枚举值的内存大小等于所有构造器所构造的对象中所需的最大内存，即哪个对象的内存最大，就等于哪个对象的内存大小。

#### 6.1.7 递归类型(Recursive)
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

#### 6.1.8 指针类型(Pointer)
Rust中的所有指针都是显式的第一类(`first-class`)值，它们可以被复制、存储到数据结构中、从函数中返回，等等。

Rust中的指针主要有两种：**`引用(References, &)`** 和 **`原指针(Raw Pointer, *)`**。

##### 6.1.8.1 引用(Reference)
引用指向被其它值 `拥有(own)` 的内存。一个引用类型可以写成 **`&type`** 或 **`&'a type`**，后一种情况是当你须要显式地指定一个生存时间时使用。**_引用的拷贝是一个浅拷贝：它只拷贝指针本身。_**释放一个引用并不影响它所指向的值，但对于一个临时值的引用除外，即：一个临时值只在它的引用的作用域内存活。

##### 6.1.8.2 原指针(Raw Pointer)
原指针是没有安全和生存周期保证的指针，它可以写成 **`*const T`** 或 **`*mut T`**，如：`*const i32` 表示一个指针32位整数的原指针。**_复制和丢弃一个原指针不影响任何其它值的生命周期。_**解引用(dereference)一个原指针或将它转换成任何其它指针类型，都是不安全的操作(See unsafety)。不建议在Rust代码中使用原指针，它们之所以存在，主要是为了支持：(1)与外围代码(非Rust代码)的互操作性；(2)写对性能十分挑剔或更底层的功能。

注：标准库中包含一个 `智能指针(smart pointer)`。

#### 6.1.9 函数类型(Function)
一个函数可以通过关键字 **`fn`** 进行定义。

一个函数类型包括：(1)**一个可空的`函数类型修改符`集合(如unsafe、extern)**，(2)**一个参数类型序列**，(3)**一个返回值类型**。

```rust
fn add(x: i32, y: i32) -> i32 {
    x + y
}

let mut x = add(5,7);

type Binop = fn(i32, i32) -> i32;
let bo: Binop = add;
x = bo(5,7);
```

#### 6.1.10 闭包类型(Closure)
一个 `Lambda` 表达式将产生一个闭包，它的类型是唯一的、不能被写出(written out)的匿名类型。

依赖于闭包的需要，它的类型实现了一或多个下面的闭包特性：

- **FnOnce**: 这样的闭包只能被调用一次，且能够把它环境中的值给`move out`出来。
- **FnMut**: 这样的闭包可以被调用多次，且能够修改它环境中的值。`FuMut` 继承自 `FnOnce`，也就是说，任何实现了 `FnMut` 的闭包同样也实现了 `FnOnce`。
- **Fn**: 这样的闭包能够通过一个共享引用被调用多次。但是，这样闭包既不能把它环境中的值给 `move out` 出来，也不能修改它环境中的值。`Fn` 继承自 `FnMut`，因此，自然也继承自 `FnOnce`。

#### 6.1.11 特性对象(Trait)
在 Rust 中，像 `&SomeTrait` 或 `Box<SomeTrait>` 这样的类型叫做 `特性对象(trait object)`。

Trait对象的每个实例都包含：
- 一个**`指针`**：该指针指向实现了 `SomeTrait` 的类型 `T` 的实例。
- 一个**`虚方法表(Virtual Method Table)`**：一般又叫 `vtable`，它通常包含一个指向类型 T 的实现(即一个函数指针)。

Trait对象目的是为了允许方法的 **`延迟绑定(late binding)`**。在Trait对象上调用一个方法将在运行时引发虚拟派发(Virtual Dispatch)，也就是说，一个函数指针将从 Trait 对象的 `vtable` 中被加载，并间接调用。每个 `vtable` 实体的实际实现根据基础对象的不同而不同。

对于一个被实例化的 Trait 对象，Trait 必须是对象安全的(`object-safe`)。对象安全性规则被定义在 [Rust RFC 255](https://github.com/rust-lang/rfcs/blob/master/text/0255-object-safety.md)。

假如有一个指针类型表达式 `E`，它的类型是 `&T` 或 `Box<T>`，其中 `T` 实现了 Trait `R`，把 `E` 转换成一个相应的指针类型 `&R` 或 `Box<R>` 将得到一个 Trait 对象 `R` 的值，该值可以表示成一对指针：`vtable` 指针(`R` 的 `T` 的实现)和 `E` 的指针值。

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

#### 6.1.12 类型参数
在一个有类型参数声明的 Item 的主体中，它的类型参数的名字是类型。

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

#### 6.1.13 Self类型
一个特殊的类型 **`Self`** 在 **`Trait`** 和 **`实现(impl)`** 中有特殊的含义。在 **`Trait定义`** 中，它引用一个表示 `implementing` 类型的隐式类型参数，即实现该 Trait 的类型对象。在 **`实现(impl)`** 中，它是 `implementing` 类型的别名，即该类型对象的别名。

标识 **`&self`** 是 **`self: &Self`** 的缩写。

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

### 6.2 子类型(Subtyping)
和其它语言不一样，Rust 没有 `类`，也没有 `类继承`，因此，Rust 中的 `子类型` 是基于 `生存时间(lifetime)` 的，也即是，**`生存时间短的类型是生存时间长的类型的子类型`**。如：
```rust
fn bar<'a>() {
    let s: &'static str = "hi";
    let t: &'a str = s;
}
```
因为 `'static` 比 `'a` 存活的更长（即生存时间更长），所以 `&'static str` 是 `&'a str` 的子类型。

和其它语言一样，子类型的变量可以赋值给父类型的变量。

### 6.3 类型强制转换(Type Coercion)
强制转换(Coercion)被定义在 [Rust RFC 401](https://github.com/rust-lang/rfcs/blob/master/text/0401-coercions.md)。

Coercion是隐式的，并没有任何显式语法。

#### 6.3.1 强制场所(Coercion Sites)
一个强制只可能发生在程序中的某个强制场所。可能的强制场所有：
- 显示指定类型的 `let` 语句。
    ```rust
    let _: i8 = 42; // 42 的类型被强制为 i8
    ```
- `static` 和 `const` 语句（和 `let` 语句相似）。
- 函数调用的参数。
    这些实际的参数值（即 `实参`）被强制为函数签名中的类型（即 `形参`）。
    ```rust
    fn bar(_: i8) {}
    fn main() {
        bar(42);   // 形参 42 被强制为类型 i8
    }
    ```
- `struct` 及其 `变体域(variant field)` 的实例。
    ```rust
    struct Foo {x: i8}
    fn main() {
        Foo {x: 42};
    }
    ```
- 函数的返回值。
    ```rust
    fn foo() -> i8 {
        42  // 返回值 42 被强制为类型 i8
    }
    ```

如果这些强制场所中的表达式是一个强制传播(propagating)表达式，那么，该表达式中相关的子表达式也是强制场所。另外，这种传播会从这些新的强制场所递归发生。`传播表达式` 及其 `相关的子表达式` 是以下几种：
- **类型为 `[U; n]` 的数组字面值**。数组字面值中的每个子表达式都是一个强制场所——强制到类型 `U`。
- **具有重复语法且类型为 `[U; n]` 的数组字面值**。每个重复的子表达式都是一个强制场所——强制到类型 `U`。
- **元组**，它的类型为 `(U_0, U_1, ..., U_n)`，每个子表达式都强制到相应的类型，如第零个子表达式被强制到类型 `U_0`。
- **圆括号子表达式(`(e)`)**：如果表达式的类型为 `U`，那么子表达式被强制为类型 `U`。
- **块**：如果一个块的类型为 `U`，那么块中最后一个表达式（如果它不是以分号结尾）被强制到类型 `U`。

#### 6.3.2 强制类型(Coercion Types)
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

    and where - coerce_inner(`[T, ..n]`) = `[T]` - coerce_inner(`T`) = `U` where `T` is a concrete type which implements the trait `U`.

    In the future, `coerce_inner` will be recursively extended to tuples and structs. In addition, coercions from sub-traits to super-traits will be added. See RFC401 for more details.

## 7 Special Trait

### 7.1 Copy Trait
Copy trait 改变了实现了它的类型的语义：实现了 Copy Trait 的类型的值在赋值时将会被拷贝、复制，而不是 move（即移交所有权）。

### 7.2 Sized Trait
Sized Trait 表示该类型的大小在编译时是可知的。

### 7.3 Drop Trait
Drop Trait 提供了一个析构函数；无论任何时候，只要实现 Drop 的类型的值被销毁，该析构函数就会被调用。

### 7.4 Deref Trait
`Deref<Target = U>` 允许一个类型隐式地实现类型 `U` 的所有方法。当试图解析一个方法调用时，编译器将先搜索最顶层的类型是否实现了该方法；如果没有找到该方法，`.deref()` 将被调用，编译器并在返回的类型 `U` 上继承搜索该方法的实现。

## 8 内存模型(Memory Model)
一个 Rust 程序的内存包含一组静态的 Item 和一个堆。对于堆，不可修改的部分可以在线程间被安全地共享，而可修改的部分不能被安全地共享，但是有一些机制可以保证可修改的值和不安全的代码被安全地共享。

在栈上分配的是 **`变量(variable)`**，在堆上分配的是 **`box`**。

### 8.1 内存分配和生存时间
Rust 程序中的 Item 包括 `函数(function)`、`模块(module)`、`类型(type)`，且类型的值会在编译期被计算，并唯一地存储在 Rust 进程的内存镜像中。这些 Item 既不会被动态地分配，也不会被动态地释放。

堆(heap)是一个描述 `box` 的一般术语。在堆上，一个分配的生命周期依赖于指向它的 `box` 的生命周期。由于 `box` 的值可以被传入/传出栈桢(frame)，或者存储在堆上，所以，堆分配可能比分配它的栈桢(frame)存活的更久。

### 8.2 内存拥有权
当退出一个栈桢(frame)时，在它本地分配的所有内存都会被释放，并且对 `box` 的引用也将会被丢弃掉。

### 8.3 变量
一个变量是一个栈桢的组成成分，可能是一个命名的函数参数，或者是一个匿名的临时值，亦或是一个命名的本地变量。

一个本地变量（即在本地栈上分配的）直接拥有一个在栈内存中分配的值，该值是栈桢的一部分。

本地变量是不可变的，除非用关键字 **`mut`** 声明，如：`let mut x = ...`。

函数参数也是不可变的，除非用关键字 **`mut`** 声明，并且关键字 **`mut`** 作用于其后紧邻的参数。如：`|mut x, y|` 和 `fn f(mut x: Box<i32>, y: Box<i32>)` 都声明了参数 x 是可变的，但参数 y 是不可变的。

和普通参数相似，对于接收 **`self`** 或 **`Box<Self>`** 的方法，可以在它们前面添加 **`mut`**，使其变为一个可修改变量。
```rust
trait Changer {
    fn change(mut self) -> Self;
    fn modify(mut self: Box<Self>) -> Box<Self>;
}
```

**`本地变量在分配时不会被初始化。`**本地变量会在当前栈桢上立即分配，但不会初始化它们，在一个函数中，其后的语句可能会/也不可能会初始化本地变量。但是**`本地变量只能在它们被初始化后才能使用，这是编译器强制要求的`**。

## 9 链接(Linkage)
Rust 编译器支持多种途径把 Crate 静态或动态地链接在一起。

在一个编译会话中，编译器能够通过 `命令行链接标志` 或 `crate_type` 属性来产生多个工件(artifacts)；但如果在命令行指定一个或多个链接标志，则所有的 `crate_type` 属性都将被忽略。

`命令行链接标志` 和 `crate_type` 属性：
- **--crate_type=bin, #[crate_type="bin"]**：一个可运行的可执行文件将被产生，这要求在将被运行的 Crate 中有一个 `main` 函数。这会链接所有 Rust 和本地的依赖，并产生一个可发布的二进制程序。
- **--crate_type=lib, #[crate_type="lib"]**
- **--crate-type=dylib, #[crate_type = "dylib"]**
- **--crate-type=staticlib, #[crate_type = "staticlib"]**
- **--crate-type=rlib, #[crate_type = "rlib"]**

一般情况下，**`--crate_type=bin`** 或 **`--crate_type=lib`** 应当对于所有的编译需要都是有效的；其它选项仅当以下情况可见：对于一个 Rust Crate 的输出格式，如果需要更细粒度的控制。

## 10 非安全代码(Unsafety)
不安全的操作是那些可能违反 Rust 静态语义的内存安全保证的操作。

下面的语言级特性不能使用在 Rust 的安全子集中：
- 解引用一个原指针(Raw Pointer)
- 读写一个可修改的静态变量
- 调用一个不安全的函数（包括 Rust 函数和非 Rust 函数）

### 10.1 不安全函数(Unsafe Function)
不安全函数是那些在所有上下文中都不安全的函数。这样的函数的前面必须放置关键字 `unsage`，并且只能在一个 `unsafe` 块或另一个 `unsafe` 函数中被调用。

### 10.2 不安全块(Unsafe Block)
在一个代码块前可以放置关键字 `unsafe`，以便在一个安全函数中调用一个 `unsafe` 函数，或解引用(dereference)一个原指针(Raw Pointer)。

如果一系列不安全的操作可以明确地确认为是安全的，那么它们可以被封装到一个 `unsafe` 块中；编译器将认为这样的代码是安全的。也就是说，凡是处于 `unsafe` 块中的代码，编译器都认为是安全的，即使它们不是安全；这个安全性由程序员来保证，而不是由编译器。

不安全块通常用于(1)**捕获外围库**、(2)**直接使用硬件**、(3)**实现语言中并不直接存在的特性(features)**。比如：在语言层面，Rust 提供了必须的特性以实现内存安全的并发，但线程或消息传递则是由标准库实现的。

Rust 的类型系统是动态安全需求的保守近似值(a conservative approximation of the dynamic safety requirements)，所以，在某些情况下，使用安全代码将会导致一个性能开销(performance cost)。

### 10.3 被认为未定义的行为(Behavior Considered Undefined)
略。

### 10.4 并不认为不安全的行为(Behavior Not Considered Unsafe)
下面的行为在 Rust 中并不被认为不安全，只是不期望它们发生。
- **死锁(Deadlock)。**
- **内存或其它资源的泄漏。**
- **退出时未调用析构函数。**
- **整数溢出。**
    除非使用 `wrapping` 原语，否则溢出被认为不期望的行为，并且总是一个用户错误。

## 11 灵感(Influence)
在设计上，Rust 从其它语言借鉴了一些特性，下面包含一个列表（包括曾经借鉴但后来又被删除的特性）：

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
