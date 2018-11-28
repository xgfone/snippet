# 杂记（还未整理）

只有所有的公共依赖 `crate` 是稳定的，当前 `crate` 才是稳定；否则就是不稳定的。

所有公共的 `struct` 都应该实现 `Debug` 特性。

只有智能指针才可以实现 `Deref` 和 `DerefMut` 特性。


重要的通用特性：
Copy
Clone
Eq
PartialEq
Ord
PartialOrd
Hash
Debug
Display
Default

可使用转换特性：
From
TryFrom
AsRef
AsMut

永不应使用的转换特性：
Into
TryInto
因为它们可以分别基于 From 和 TryFrom 特性来实现。

收集类型（如何字典、集合等）应实现 FromIterator 和 Extend 特性
`FromIterator` is for creating a new collection containing items from an iterator, and `Extend` is for adding items from an iterator onto an existing collection.

只要可能，数据结构尽量实现 `Send` 和 `Sync` 特性。


命名约定
Item	Convention
Crates	unclear
Modules	snake_case
Types	UpperCamelCase
Traits	UpperCamelCase
Enum variants	UpperCamelCase
Functions	snake_case
Methods	snake_case
General constructors	new or with_more_details
Conversion constructors	from_some_other_type
Macros	snake_case!
Local variables	snake_case
Statics	SCREAMING_SNAKE_CASE
Constants	SCREAMING_SNAKE_CASE
Type parameters	concise UpperCamelCase, usually single uppercase letter: T
Lifetimes	short lowercase, usually a single letter: 'a, 'de, 'src
Features	unclear


类型间的转换应该作为方法来提供，并有下面的约定前缀：
Prefix	Cost	Ownership
as_	Free	borrowed -> borrowed
to_	Expensive	borrowed -> borrowed
borrowed -> owned (non-Copy types)
owned -> owned (Copy types)
into_	Variable	owned -> owned (non-Copy types)

Conversions prefixed `as_` and `into_` typically decrease abstraction, either exposing a view into the underlying representation (`as`) or deconstructing data into its underlying representation (`into`). Conversions prefixed `to_`, on the other hand, typically stay at the same level of abstraction but do some work to change one representation into another.

If the `mut` qualifier in the name of a conversion method constitutes part of the return type, it should appear as it would appear in the type. For example `Vec::as_mut_slice` returns a mut slice; it does what it says. This name is preferred over `as_slice_mut`.


变量能被隐藏（shadow）：即在同一个作用域内，对于同一个变量名，可以通过 `let` 将其重新声明或定义为另一种类型的变量。

Rust 有四种标量值：**整数**、**浮点数**、**布尔**、**字符（串）**。

整数标量类型有 12 种（有符号 6 种，无符号 6 种）：`i8`、`i16`、`i32`、`i64`、`i128`、`isize`、`u8`、`u16`、`u32`、`u64`、`u128`、`usize`。`isize` 和 `usize` 类型在 64 位系统中是 64 位值，在 32 位系统中是 32 位值。

字符类型 `char` 是一个四字节的整数值，可以表示一个 Unicode 标量值，其范围从 `U+0000` 到 `U+D7FF` 及 `U+E000` 到 `U+10FFFF` 区间。

函数或方法的参数的生命周期叫输入生命周期（`input lifetime`），返回值的生命周期叫输出生命周期（`output lifetime`）：
（1）每个引用类型的参数都有各自的生命周期，即互不相同；
（2）如果只有一个输入生命周期参数，它将赋给所有的输出生命周期参数；
（3）如果有多个生命周期参数，但它们其中有一个是 `&self` 或 `&mut self`，由于它是一个方法，所以，`self` 的生命周期参数将赋给所有的输出生命周期参数。
如果还有未确定的生命周期参数，则必须明确指定生命周期，而不能省略它、让编译器去推断。

Rust 自动推导闭包使用方式的步骤:
（1）如果一个外部变量在闭包中，只通过 `&` 借用指针使用，那么这个变量就可通过引用 `&` 的方式捕获。
（2）如果一个外部变量在闭包中，通过 `&mut` 指针使用过，那么这个变量就须要使用 `&mut` 的方式捕获。
（3）如果一个外部变量在闭包中，通过 `move` 方式使用过，那么这个变量就须要使用 `by value` 的方式捕获（即所有权转移）。
总之，在保证能正确编译通过的情况下，编译器会自动选择一种对外部影响最小的类型存储：对于被捕获的类型为 T 的外部变量，在匿名结构体中的存储方式为，尽可能先选择 `&T` 类型，其次选择 `&mut T` 类型，最后才选择 `T` 类型。

```rust
pub trait FnOnce<Args> {
    type Output;
    extern "rust-call" fn call_once(self, args: Args) -> Self::Output;
}

pub trait FnMut<Args> : FnOnce<Args> {
    extern "rust-call" fn call_mut(&mut self, args: Args) -> Self::Output;
}

pub trait Fn<Args> : FnMut<Args> {
    extern "rust-call" fn call(&self, args: Args) -> Self::Output;
}
```
`FnOnce`、`FnMut`、`Fn` 三种 trait 的主要区别在于，被调用的时候，`self` 参数的类型。由于 `FnOnce` 的 `self` 是 `by value` 方式，因此在调用后它的所有权将会转移到闭包内部，在调用结束后，闭包本身将会被销毁。所以，`FnOnce` 类型的闭包本身只能调用一次。

`Fn` 是 `FnMut` 的子特性，`FnMut` 是 `FnOnce` 的子特性，因此，`Fn` 类型的闭包能当作 `FnMut` 和 `FnOnce` 类型的参数进行传递，`FnMut` 类型的闭包能被当作 `FnOnce` 类型的参数进行传递。

`FnOnce` 会接管所捕获变量的所有权。
`FnMut` 通过 `&mut` 方式来借用所捕获的变量，因此，它可以修改所捕获的变量的值。
`Fn` 通过 `&` 方式来借用所捕获的变量，因此，它只能读取所捕获的变量，但不能修改它。


引用与智能指针不同：引用是仅借用数据的普通指针，而智能指针并不是一个真实的指针，只是一个行为上类似指针并拥有额外元数据和能力的数据结构；在大部分情况下，智能指针拥有它所指向的数据。`String`、`Vec<T>` 等都是智能指针。


Here is a recap of the reasons to choose `Box<T>`, `Rc<T>`, or `RefCell<T>`:
- `Rc<T>` enables multiple owners of the same data; `Box<T>` and `RefCell<T>` have single owners.
- `Box<T>` allows immutable or mutable borrows checked at compile time; `Rc<T>` allows only immutable borrows checked at compile time; `RefCell<T>` allows immutable or mutable borrows checked at runtime.
- Because `RefCell<T>` allows mutable borrows checked at runtime, you can mutate the value inside the `RefCell<T>` even when the `RefCell<T>` is immutable.
- `Arc<T>` is the same as `Rc<T>`, but it is thread-safe.
- `Mutex<T>` provides interior mutability.


当一个 `T` 类型实现了 `Send`，它向编译器指示这个类型的所有权可以在线程间安全的转移。
当一个类型 `T` 实现了 `Sync`，它向编译器指示这个类型在多线程并发时没有导致内存不安全的可能性。
这隐含了没有内部可变性的类型天生就是 `Sync` 的，这包含了基本类型和只包含他们的聚合类型。


一个 `trait` 只有是安全的，才能作为 `trait object`。
只要一个 `trait` 中的所有方法既都不返回 `Self`又都没有泛型类型参数，那么它就是对象安全的（`object-safe`），因此也是 `trait object`。

`Box<T>` 是“自我复制”，在堆上分配存储的智能指针。它与一般数据类型相比，除了将数据分配在堆上外，没有其它新的特性。

`&` 和 `&mut`：普通的不可变引用和可变引用。

`*const T` 和 `*mut T`：不可变原始指针和可变原始指针。

`Rc<T>`：引用计数智能指针，它通过引用计数（强引用）允许一个数据类型有多个所有权。由于它的计数引用是强引用，因此，如果创建了一个循环引用，则可能造成数据泄漏。当克隆多份时，它内部的数据是不可变引用约束（即不能获得可变引用）。它（即引用计数的变量）不是线程安全的。

`Weak<T>`：弱引用智能指针。它没有所有权，也不能被借用；因此，也没有生命周期的限制（即可以永久存在），但在使用前要先检查它所引用的数据是否存在。

`Cell<T>`：无运行时开销的内部可变类型，但它只用于 `Copy` 类型，因为编译器知道它包含的值所对应的所有数据都位于栈上，所以并没有通过简单的替换数据而导致任何位于引用之后的数据泄漏的担心。

`RefCall<T>`：有运行开销（读写锁）的内部可变类型。与 `Cell<T>` 不同的是，它并不限于 `Copy` 类型。注：如果是一个能用 `&` 指针的非常简单的情形，应该避免使用 `RefCell<T>`。

---

`Arc<T>` 是 `Rc<T>` 的原子操作版，可以用于多线程间。

`Mutex<T>` 互斥锁
`RwLock<T>` 读写锁

`Rc<RefCell<Vec<T>>>` 类似于 `&mut Vec<T>`，可以随时添加/删除元素。
`Rc<Vec<RefCell<T>>>` 类似于 `&mut [T]`，可以借用/修改其中的元素，但不能添加/删除元素。


`unsafe` 可以实现四种操作：
（1）解引用一个原始指针；
（2）调用一个 `unsafe` 函数或方法；
（3）访问/修改一个可修改的静态变量（即全局变量）；
（4）实现一个 `unsafe trait`。
注：还有内联汇编。

`unsafe` 并不意味着其代码是危险的，或其有内存安全问题；它只是告诉编译器，其代码会以有效地方式去访问内存，至于它是否真正地以有效地方式去访问内存，这是程序员的责任。

只要不解引用原始指针，可以不使用 `unsafe` 块。

只要 `trait` 中有一个方法是不安全的（`unsafe`），那么整个 `trait` 都是不安全的。

只要 `struct` 中的所有成员都是 `Send` 或 `Sync` 类型，那么编译器将自动为该 `struct` 实现 `Send` 或 `Sync`。

当变量赋值时，Rust 默认执行 `move` 语义；赋值结束后，之前的变量就不能再被访问。但如果该变量的类型实现了 `Copy` 特性，Rust 会通过在栈上执行潜拷贝，为新变量分配一份新的存储空间，而旧变量不变；此时，旧变量仍可继续使用。

默认情况下，`Copy` 是潜拷贝，`Clone` 是深拷贝。
