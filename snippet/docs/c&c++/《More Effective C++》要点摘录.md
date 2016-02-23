
### 1、仔细区别pointers和references。——条款1
一般而言，当你需要考虑“不指向任何对象”的可能性时，或是考虑“在不同时间指向不同对象”的能力时，你就应该采用pointer。前一种情况你可以将pointer设为null，后一种情况你可以改变pointer所指对象。而当你确定“总是会代表某个对象”，而且“一旦代表了该对象就不能够再改变”，那么你应该选用reference。

当你知道你需要指向某个东西，而且绝不会改变指向其他东西，或是当你实现一个操作符而其语法需求无法由pointers达成，你就应该选择references。任何其他时候，请采用pointers。

### 2、最好使用C＋＋转型操作符。——条款2
为了解决C旧式转型的缺点，C＋＋引入了4个新的转型操作符：`static_cast`、`const_cast`、`dynamic_cast`、`reinterpret_cast`。

`static_cast`用于替换旧式的C转型：`static_cast<type>(expression)`用以替换`(type)expression`。

`const_cast`用以改变一个对象或变量的常量性或变易性（即添加或去除cosnt属性）：形式如`const_cast<type>(expression)`。

`dynamic_cast`用以将“指向base class objects的pointers或references“转型为”指向derived（或sibling base）class objects的pointers或references"，并得知转型是否成功。如果转型失败，会以一个null指针（当转型对象是指针）或一个exception（当转型对象是reference）表现出来。

`reinterpret_cast`用以重新解释后面的表达式，它的结果几乎总是与编译平台息息相关，所以它不具移植性。

### 3、绝对不要以多态（polymorphically）方式处理数组。——条款3

### 4、非必要不要提供default constructor。——条款4
在一个完美的世界中，凡可以“合理地从无到有生成对象”的classes，都应该内含default constructors，而“必须有某些外来信息才能生成对象”的classes，则不必拥有default constructors。

### 5、对定制的“类型转换函数”保持警觉。——条款5
有两种函数允许编译器隐式地自动进行转换：单自变量constructors和隐式类型转换操作符。

最好不要提供任何类型转换函数。 尽可能地避免任何类型的隐式类型转换；如果确实需要，请使用显示地且仅使用显示地。对于单自变量constructors而言，可以在其前面使用explicit关键字进行声明；对于隐式类型转换操作符，可以使用另外一个公有成员函数来代替它，让使用者显示调用该公有成员函数来完成相应的功能。

### 6、千万不要重载&&、||和,操作符。———条款7
一旦重载了这些函数，将无法再保证短路运算。

### 7、利用destructors避免泄漏资源。——条款9
只要坚持这个规则，把资源封装在对象内，通常便可以在exceptions出现时避免泄漏资源。本条在“条款10”中讲述的更加详细。

### 8、在constructors内阻止资源泄漏（resource leak）。——条款10
参见“资源管理”。

### 9、禁止异常（exceptions）流出destructors之外。——条款11
析构函数不应该也不能抛出任何异常。有两个好理由支持我们全力阻止exceptions传出destructors之外“：

	第一，它可以避免terminate函数在exception传播过程的栈展开（stack-unwinding）机制中被调用；
	第二，它可以协助确保destructors完成其应该完成的所有事情。

### 10、理解异常。——条款12
一个被抛出的对象可以简单地用byreference的方式捕捉，不需要以byreference-to-const的方式捕捉。函数调用过程中将一个临时对象传递给一个non-const reference参数是不允许的，但对exceptions则是合法的。

exception objects总是会被复制（为exception所做的复制动作，其结果是一个临时对象），如果以by value方式捕捉，它们甚至被复制两次。

“被抛出成为exceptions“的对象，其被允许的类型转换动作，比”被传递到函数去“的对象少。

“exceptions与catch子句相匹配”的过程，仅有两种转换可以发生：

	第一种是“继承架构中的类转换（inheritance-based conversions）”；
	第二种是从一个“有型指针”转为“无型指针”，所以一个针对const void*指针面设计的catch子句，可捕捉任何指针类型的exception。

catch子句以其“出现于源代码的顺序”被编译器检验比对，其中第一个匹配成功者便执行；而当我们以某对象调用一个虚函数，被选中执行的是那个“与对象类型最佳吻合”的函数，不论它是不是源代码所列的第一个。

### 11、以by reference方式捕捉exceptions。——条款13
异常传递（或称捕获）有三种选择：`by pointer`、`by value`、`by reference`。

`by pointer`可以直接排除（不建议使用）。

`by value`会导致较大的时间与空间的开销（两次分配和销毁临时对象），并且还会导致exception object的切割问题。

`by reference`相对前两者比较高效、安全。

### 12、明智运用exception specifications。——条款14
没有什么方法可以知道一个template的类型参数可能抛出什么exceptions，所以千万不要为template提供意味深长的exception specification。因此，不应该将templates和exception specifications混合使用。

如果A函数内调用了B函数，而B函数无exception specifications，那么A函数本身也不要设定exceptionspecifications。

总之，exceptionspecifications是一把双面刃，在将它加入函数之前，请考虑它所带来的程序行为是否真是你所想要的。

### 13、了解异常处理（exception handling）的成本。——条款15
编译过程中如果没有加上对exceptions的支持，程序通常比较小，执行时比较快；如果编译过程中加上对exceptions的支持，程序就比较大，执行时比较慢。

粗略估计，如果使用try语句块，代码大约整体膨胀5%-10%，执行速度亦大约下降这个数。为了将此成本最小化，你应该避免非必要的try语句块。

面对exceptionspecifications，编译器产出的代码倾向于类似面对try语句块的作为，所以一个exceptionspecifications通常会招致与try语句块相同的成本。

总之，为了让exception的相关成本最小化，只要能够不支持exceptions，编译器便不劫持；请将你对try和exception specifications的使用限制于非用不可的地点，并且在真正异常的情况下才抛出exceptions。如果你还是有性能上的问题，请利用分析工具（profiler）分析你的程序，以决定“对exception的支持”是否是一个影响因素。

### 14、谨记80-20法则。——条款16
80-20法则说：一个程序80%的资源用于20%的代码身上。软件的整体性能几乎总是由其构成要素（代码）的一小部分决定。

### 15、考虑使用lazy evalutation（缓式评估）。——条款17

### 16、分期摊还预期的计算成本。——条款18
此条款背后的哲学是超急评估（over-eagerevaluation）。Over-eagerevaluation背后的观念是，如果你预期程序常常会用到某个计算，你可以降低每次计算的平均成本，办法就是设计一份数据结构以便能够极有效地处理需求。

当你必须支持某些运算而其结果并不总是需要的时候，lazy evaluation可以改善程序效率；当你必须支持某些运算而其结果几乎总是被需要，或其结果常常被多次需要的时候，over-eager evaluation可以改善程序效率。两者都比最直截了当的eager-evaluation难实现，但是两者都能为适当的程序来巨大的性能提升。

### 17、了解临时对象的来源。——条款19
C＋＋真正的所谓的临时对象是不可见的——不会在你的源代码中出现。只要你产生一个non-heap object而没有为它命名，便诞生了一个临时对象。此等匿名对象通常发生于两种情况：一是当隐式类型转换被施行起来以求函数调用能够成功；二是当函数返回对象的时候。

临时对象可能很耗成本，所以你应该尽可能消除它们。任何时候只要你看到一个reference-to-const参数，就极可能会有一个临时对象被产生出来绑定到该参数上；任何时候只要你看到函数返回一个对象，就会产生临时对象（并于稍后销毁）。

### 18、协助完成“返回值优化（RVO）”。——条款20
有些函数硬是得返回对象，它必须得如此。也就是说，如果函数一定得以by-value方式返回对象，你绝对无法消除它。从效率的眼光来看，你不应该在乎函数返回了一个对象，你应该在乎的是那个对象的成本几何。你需要做的，是努力找出某种方法以降低被返回对象的成本，而不是想尽办法消除对象本身。

我们可以用某种特殊方法来撰写函数，使它在返回对象时，能够让编译器消除临时对象的成成本。我们使用的伎俩是：返回所谓的constructor arguments以取代对象。虽然这并不能总是凑效，但是C＋＋允许编译器将这种临时对象优化掉，使之不存在。注：这并不总能凑效，因为C＋＋并没有强制要求编译器必须这么做，也就是说编译器可以不这么做。不管编译器做不做，我们并没有吃多大的亏！不是吗？

### 19、利用重载技术避免隐式类型转换。——条款21

### 20、考虑以操作符复合形式（op=）取代其独身形式（op）。——条款22

### 21、考虑使用其他程序库。——条款23
理想的程序库应该小、快速、威力强大、富弹性、有扩展性、直观、可广泛运用、有良好支持、使用时没有束缚，而且没有臭虫。

### 22、杂项讨论。——条款32、34
（1）只要有人删除B*而它实际上指向D，便表示你需要一个virtual destructor。

（2）如果一个`public base class`没有`virtual destructor`，那么其`derived class`及“该derived class的data members”都不应该有destructor。

（3）如果多重继承（multiple inheritance）体系中有任何destructors，那么每一个base class都应该有一个virtual destructor。

（4）如果你打算在同一个程序中混用C++和C，请记住以下几个简单守则：

	(1) 确定你的C++和C编译器产出兼容的目标文件。
    (2) 将双方都使用的函数声明为extern"C"。
    (3) 如果可能，尽量在C++中撰写main。
    (4) 总是以delete删除new返回的内存，总是以free释放malloc返回的内存。
    (5) 将两个语言间的“数据结构传递”限制于C所能了解的形式；C++structs如果内含非虚函数，倒是不受此限。

