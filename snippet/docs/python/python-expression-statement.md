
三、表达式与语句
=============

## 1、三元表达式
Python中的三元表达式：
```python
Y if X else Z
```
等同于C语言中的三元表达式：
```c
X ? Y : Z
```
注：Python中的三元表达式比C语言中的更加强大——Python中的三元表达式可以嵌套：
```python
A  if  B  else  C  if  D  else  E  if  F  else  D ...
```
该嵌套三元表达式等价于：
```python
A  if  B  else  ( C  if  D  else  ( E  if  F  else  D  ... ))
```

## 2、生成器与各种解析（推导）
### 2.1 生成器
```python
(expression  for  target  in iterator)
(expression1 for  target  in iterator  if expression2)
(expression  for  target1 in iterator1 for target2 in iterator2)
```
注：其中的`for`循环和`if`判断语句可以互相无限嵌套，但只要最左边的表达式是`for`循环即可，而最左边的`for`循环的右边可以是零或多个`for`循环或`if`循环。

**生成器是单迭代器对象。**

### 2.2 列表解析
把圆括号换成方括号即可。

### 2.3 集合解析
把圆括号换成大括号即可。

### 2.4 字典解析
```python
{ x:f(x)  for x in items }
```
字典解析的语法基本上与以上类似，只不过把相应的表达式改成字典的形式即可。

注：《学四》中将`comprehension`翻译成“`解析`”，其他一些书籍中翻译成“`推导`”，笔者也感觉“`推导`”更好些，但本文参考了《学四》，因此沿用《学四》中的翻译。

## 3、lambda表达式
(1) `lambda`是一个表达式，而不是一个语句，所以它有一个返回值（即函数对象）。

(2) `lambda`的主体是一个单个的表达式，而不是单个的代码块。

(3) `lambda`表达式中的参数列表完全使用的`def`定义语句中的函数参数列表，除了注解功能。

(4) 在`lambda`主体中的代码像在`def`内的代码一样都遵循相同的作用域查找法则。`lambda`表达式引入的一个本地作用域更像一个嵌套的`def`语句，将会自动从上层函数中、模块中以及内置作用域（通过LEGB法则）查找变量名。

(5) `注解`只在`def`语句中有效，在`lambda`表达式中无效，因为`lambda`的语法已经限制了它所定义的函数工具。

(6) `lambda`可以看成是一个被阉割了部分功能的小函数（比如：注解、主体只能是个表达式等等），所以，它具备了函数所具有的大部分功能，正所谓“麻雀虽小，五脏俱全”。

(7) 例子
```python
>>> tmp = lambda first, second: True if first > second else False
>>> tmp(1, 2)
False
>>> tmp(2, 1)
True
```

## 4、表达式与语句
在Python中，表达式有一个返回值，而语句没有返回值。又由于赋值是语句而不是表达式，所以赋值语句不能出现在表达式中。

## 5、赋值语句
赋值语句的求值顺序：

    先对等号右边的表达式列表从左到右依次计算，
    然后再对等号左边的目标列表依次计算，
    最后把等号右边求得的值赋值给等号左边相应的“目标”。

另外，**`赋值只生成引用，而不是拷贝`**。

## 6、省略符
在 `Python 3.X` 中，可以使用`...`（三个连续的英文“点”）代替 `pass` 语句来省略代码。

## 7、DEL语句
`del`语句仅仅是解除名字到底层对象的绑定，并不是释放底层对象所占用的内存空间；然而，底层对象占用的内存空间是由垃圾回收机制来释放的。

## 8、表达式的计算顺序
默认地，Python的表达式是**`从左到右`**依次计算。但是有个特例：赋值语句中的表达式的计算顺序是计算等号右边的表达式，然后再计算等号左边的表达式；但对于等号左边和右边的表达式都服从从左到右的计算顺序。举例：
```python
expr1, expr2, expr3, expr4
(expr1, expr2, expr3, expr4)
[expr1, expr2, expr3, expr4]
{expr1: expr2, expr3: expr4}
expr1 + expr2 * (expr3 - expr4)
expr1(epxr2, expr3, *expr4, **expr5)
expr3, expr4 = expr1, expr2
```
说明：以上各种表达式均依次、先后计算`expr1`, `expr2`, `expr3`, `epxr4`, `expr5`，即先计算`expr1`，再计算`expr2`，然后计算`expr3`，接着`expr4`，最后才计算`expr5`。

## 9、Python操作符的优先级

|                                Operator                            |                Description
|--------------------------------------------------------------------|---------------------------------------------------------------
|lambda                                                              | Lambda expression
|if - else                                                           | Conditional expression
|or                                                                  | Boolean OP
|and                                                                 | Boolean AND
|not x                                                               | Boolean  NOT
|in, not in, is, is not, <, <=, >, >=, !=, ==                        | Comparisons, including membership tests and identity tests
|\|                                                                  | Bitwise OR
|^                                                                   | Bitwise XOR
|&                                                                   | Bitwise AND
|<<, >>                                                              | Shifts
|+, -                                                                | Addition and subtraction
|*, /, //, %                                                         | Multiplication, division, remainder
|**                                                                  | Exponentiation
|x[index], x[index:index], x(arguments...), x.attribute              | Subscription, slicing, call, attribute reference
|(expression...), [expressions...], {key:datum...}, {expressions...} | Binding or tuple display, list display, dictionary display, set display

### 说明
    (1) 上述优先级从上到下依次升高，即下边的操作符比下边的优先级要高；
    (2) 同一行上的优先级相同，并且从左到右组合，即优先左结合，但有个特殊除外——乘方操作符的组合是从右到左，即优先右结合；
    (3) Python语句中赋值语句也是右结合，比如 a=b=c=d=1 等价于C语言中 a=(b=(c=(d=1)))；
    (4) 除非有语法明确指示，否则操作符均是二元操作符。

## 10、表达式列表
在Python中，由`逗号`分隔多个表达式构成了一个表达式列表，表达式列表也是表达式；**`表达式列表作为一个表达式，也有一个返回值，该返回值的类型是元组`**。当表达式列表中只有一个表达式时，如果该表达式后没有逗号（即表达式列表中没有逗号），则该表达式不是表达式列表，而仅是单个表达式，所以它的返回值并不是一个元组；**`在只有一个表达式的表达式列表中，只有在其后添加一个逗号才能成为表达式列表`**。

注：表达式列表两边可以添加一对圆括号，这将构成Parenthesized Forms（Python语言官方手册中是这么称呼的，它属于Atoms表达式之一——Atoms表达式是最基本的表达式），其效果和表达式列表一样，没有什么差别。

## 11、assert语句
Python中的 `assert` 相当于C中 `assert` 断点宏。

### 语法
```
"assert"  expression ["," expresseion]
```

#### 11.1 第一种格式（assert expression）等价于：
```python
if __debug__:
    if not expression:
        raise AssertionError
```

#### 11.2 第二种格式（assert expression1, expression2）等价于：
```python
if __debug__:
    if not expression1:
        raise AssertionError(expression2)
```
其中，`__debug__`是内建变量，除非在启动Python时添加`-O`参数，否则`__debug__`的值永为`True`。给`__debug__`赋值是非法操作。

## 12、yield语法
在 Python 语法中有 `yield表达式` 和 `yield语句`。一般来说，yield语句就是yield表达式，即yield表达式单独成一个语句，当然yield表达式也可以用在其它表达式可以出现的地方，比如：赋值语句，不过，一般很少这种使用，大部分情况下都是yield表达式单独成句，即yield语句。因此，为了统一说法，笔者称之为“yield语法”。

注：以下所述的`__next__()`方法是 `Python 3.X` 版本中的语法，但在 `Python 2.X` 版本中，该方法被命名为 `next()`。

**`yield语法只能在定义generator函数时使用，并且只能用在generator函数的主体中。在一个函数定义主体中，只要使用了yield语法，那么该函数将不在是一个普通的函数，而是一个generator函数。`**

**`当一个generator函数被调用时，它将返回一个迭代器（iterator）`**，众所周知被称为`generator迭代器（generator iterator）`，但更通用的称法是generator。

**`当重复调用generator的__next__()方法时，generator函数的主体将被重复地执行：每调用一次__next__()方法，generator函数的主体就会被执行一次，直到它引发一个异常。`**

 当一个yield语句被执行时，generator的状态将会被冻结（frozen），且在yield语句中yield关键词后的表达式（列表）的值也会返回给`__next__()`的调用者。被冻结，意思是所有的本地状态都会被保留，包括本地变量的当前绑定、指令指针、内部的计算栈：足够的信息会被保存，以便下一次调用`__next__()`方法——此时generator函数能够正确地继续处理，就好像yield语句仅是另一个外部的调用。

从Python2.5开始，yield语句允许在`try ... finally`语句中的`try`子句中使用；如果`try`子句被执行完时`generator`还没有重新被引发，则将会调用`generator`迭代器的`close()`方法。

### generator函数有以下方法（这些方法就是generator函数的协议）

#### (1) __next__()
开始执行generator函数，或者从上次执行yield表达式处重新执行它。**`当通过__next__()方法重新执行generator函数时，当前的yield表达式的值总是计算为None`**。`__next__()`方法执行generator函数主体代码，直到遇到（下一个）yield语句，此时generator函数将会被压制（suspended，即暂停执行之意，这里译成受“压制”而不在执行）而不在执行（而是在等待下一次__next__()的调用），并将yield关键字后的表达式的值返回给__next__()的调用者。**`如果generator没有产生另外一个值而退出，则Python会抛出StopIteration异常`**。

注：有网友对“`将yield关键字后的表达式的值返回给__next__()的调用者`”提出质释——这句可能会给读者带来误解，现解释如下：

    A. “yield关键字后的表达式的值”意思为，yield语法本身既是语句又是表达式，而yield关键字后的所有东西又构成一个表达式，
       即是表达式，那么它就有个值，此句指的就是该值。举例：对“yield  1,2,3,4”一句，该句既是yield语句，又是yield表达式；
       而“1,2,3,4”又构成了“元组”表达式，“yield关键字后的表达式的值”指的就是(1,2,3,4)这个元组，之所以这么称呼，请参见下面的说明。
    B. “返回给__next__()的调用者”意思为，作为__next__()函数的返回值返回给__next__()函数的调用者，换句话说，
       就是将1）中的值作为__next__()的返回值用在赋值语句中。
       举例：aa = gen_var.__next__()，其中gen_var是Generator函数对象，假设该次__next__()调用将执行“yield  1,2,3,4”语句，
       那么，元组（1,2,3,4）将作为__next__()函数的返回值赋值给变量aa。
    C. 如果以上有误或误解，请指正。

#### (2) send(value)
重新开始generator的执行并“send”一个值给generator函数。

**`参数value将会成为当前yield表达式的结果。send()方法的返回值是generator下一次产生的值，或者引发StopIteration异常`**（如果generator没有产生另一个值而退出）。

**`当通过调用send()第一次引发generator时，send()的参数必须是None，因为此时还没有yield表达式来接收该值`**。

send函数的作用是：`把参数value 通知给 generator迭代器。但是，send函数有个副作用：将会消耗一个yield，即相当于隐式地调用了一次__next__()函数`。

注意：**`如果Generator不处理send函数发送的值，那么send函数就不会改变Generator的流程（即产生的值及其顺序），但要注意其副作用，如果使用不当，则有可能丢失一个yield值。`**

#### (3) throw(type, [, value[, traceback]])

#### (4) close()

### 说明：Generator函数的暂停时机
在使用Generator函数时，如果不使用send函数而只使用`__next__`函数，那么并不需要对此问题需要了解；否则，我们就要明白，Generator在遇到yield语句而暂停时时在什么时候。以下是笔者的探索，曾有代码测试。

在没有解释之前，笔者先给出答案：**`是在yield表达式执行结束之后，yield表达式所在的语句还未执行完成之前，换句话说，就是就在yield表达式刚刚执行结束之时。`**

在此之前，我们先来看看send函数。在Generator.send(vale)的官方文档中有一句话“The value argument becomes the result of `the current yield expression`.”，而send函数的返回值则是Generator函数下一次执行yield语法时所产生的值。

我们现在来还原一下send函数的场景：_**generator.send(value)的功能是（重新）激活Generator的执行并“发送”value到Generator函数中，其中，value将成为“当前yield表达式”的结果，而send的返回值则是被Generator产生的下一个值**_。

以上是Python官方文档的说明，对此的解释：

当generator被暂停在yield处时，send函数会激活Generator函数的执行（即完成yield语句的执行），然而“yield表达式”做为表达式的一种，它会产生一个值，而当yield被send激活时，该表达式产生的值就是send发送给它的值（如果yield不是被激活时，它产生的值是None）。至于send的返回值说是被Generator产生的下一个值（也即下一次执行“yield表达式”时由“yield表达式”抛出的值——该值是“yield表达式”中“yield关键词后面的表达式”的值，而不是“yield表达式”产生的值），其中的“下一个”或“下一次”相对于在send函数没有激活Generator之前所说的（此时“yield表达式”已经执行完，而“yield语句”还没有执行完成），所以send会使用Generator继承执行并消耗一次yield表达式。

注：上文的“`当前yield表达式`”指的正是在Generator被暂停前刚刚被执行过的yield表达式——因为它所在yield语句还没有执行完。

#### 举例
以下是“Python高级编程”QQ群中的“北京-Phonenx”网友遇到一个问题：为什么只输出“9、8、7、6、5、1、0”而缺少了“2、3、4”。
```python
def countdown(n):
    print "Counting down from", n
    while n >= 0:
        newvalue = (yield n)
        # If a new value got sent in, reset n with it
        if newvalue is not None:
            n = newvalue
        else:
            n -= 1

# The holy grail countdown
c = countdown(9)
for x in c:
    print x
    if x == 5:
        c.send(2)
```
用以上观点对此进行解释：
当产生9到6时，很容易解释，在此略过。当yield产生5时（“yield表达式”已经执行完，“yield表达式”所在赋值语句还没有执行完），Generator函数会被暂停，此时输出5并执行c.send(2)；当执行c.send(2)时，将激活Generator函数（即完成赋值语句的执行——把“`当前yield表达式`”的值赋值给newvalue变量）然而，由于send函数会将它的参数替换掉“`当前yield表达式`”的值，所以“yield表达式”产生的值不是None，而是2，接着执行后面的if判断（即 if newvalue is not None），由于newvalue为2不为None，所以n被修改为newvalue的值（即2），程序将会继承执行并在下一次的“yield表达式”处暂停，由于n已经为2（不为5或4），所以“yield表达式”将产生2并暂停，被yield产生的值（2）会被send函数作为返回值来返回；再接着程序继承执行，Generator函数被激活，从“yield n（即yield 2）表达式”后继承执行——即yield表达式的值（None）会被赋值给newvalue，由于newvalue==None，所以n会被递减1而变成1，此后的执行过程将和程序刚开始时一样。

由此可以看出，send函数会向yield发送一个值，并消耗一个yield。如果yield表达式直接构成一个yield语句（即yield表达式不会用在其它语句中，比如上面的赋值语句），那么send函数会像next（在Python2.X中是next，在Python3.X中是__next__）函数一样得到Generator中的下一个值。换句话说，send不会改变Generator函数的执行结果；如果像上面一样用在赋值语句中，就有可能会改变Generator的执行结果。

如果将上面代码中的最后一行（即c.send(2)）换成“print  c.send(2)”语句，那么将会依次输出“9、8、7、6、5、2、1、0”，而不是“9、8、7、6、5、1、0”。

## 13、with语法
### 13.1 语法
```
with_stmt ::= "with" with_item ("," with_item)* ":" suite
with_item ::= expression ["as" target]
```

### 13.2 理解
with语句实现了一个内容管理器（a context manager），用来捕获一个代码块的执行。内容管理器是个对象，该对象在执行with语句时会定义运行时上下文。内容管理器处理入口（entry）的`进入`、`退出`操作。

内容管理器的典型使用包括保存、还原多种全局状态（进入时保存，退出时还原），加锁、解锁资源（进入时加锁，退出时解锁），打开、关闭文件（进入时打开，退出时关闭），等等。

内容管理器对象主要有两个实例方法：

    (1) __enter__(self)
        进入与内容管理器相关的运行时上下文。with语句会将这个方法的返回值绑定到在as后所指定的目标（如果有这个目标）上。
    (2) __exit__(self, exc_type, exc_value, traceback)
        退出与内容管理器相关的运行时上下文。
        其参数是引发上下文内容退出的异常；如果上下文内容退出时没有任何异常，则该三个参数都是None。
        当有异常发生时，如果想压制该异常不让其传播，可以使该方法返回一个布尔值为True的对象；否则，异常会在该方法退出时正常传播。
        注：该方法不应当重新引发被传进来的异常，因为这是调用者的责任。

with语句允许嵌套：
```python
with A() as a, B() as b:
    suite
```
等价于：
```python
with A() as a:
    with B() as b:
        suite
```

### 13.3 with语句的执行流程
    A、内容表达式（即with语法中的with_item部分）被计算，并获得一个内容管理器对象；
    B、加载内容管理器的__exit__( )方法以便以后使用；
    C、调用内容管理器的__enter__( )方法；
    D、如果with语句中包含一个目标（target），则将__enter__( )方法的返回值赋值给它。
    E、执行with语句的代码（即suite部分）；
    F、调用内容管理器的__exit__( )方法。如果suite部分的代码引发一个异常而被迫退出，那么该异常的类型、值以及栈回溯（traceback）
       将被作为参数传递给__exit__( )方法；否则三个None将被传递。如果suite部分是由于非异常的其他原因而结束，__exit__()的返回值
       则被忽略，并且执行流程也会在正常的位置继续处理。

### 13.4 例子
```python
with open("example.txt", "w") as f:
    f.write("Hello World")
```
注：Python中的文件对象支持内容管理器协议——粗略地讲，在进入内容管理器的时候打开文件，在退出时自动关闭文件。
