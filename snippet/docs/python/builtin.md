
Python中的内建模块
================

在学习Python时，很多人会问到`__builtin__`、`__builtins__`和`builtins`之间有什么关系。百度或Google一下，有很多答案，但是这些答案要么不准确，要么只说了一点点，并不全面。本文将给大家一个较为全面的答案。以下结果是经过本人试验过的（测试环境：`Linux Mint 14`， `Python2.7.3`和`Python3.2.3`），并参考了Python的邮件列表。

## `__builtin__` 和 `builtins` 的关系
在Python中，有一个内建模块，该模块中有一些常用函数；而该模块在Python启动后、且没有执行程序员所写的任何代码前，Python会首先加载该内建函数到内存。另外，该内建模块中的功能可以直接使用，不用在其前添加内建模块前缀，其原因是对函数、变量、类等标识符的查找是按LE(N)GB法则，其中B即代表内建模块。比如：内建模块中有一个abs()函数，其功能是计算一个数的绝对值，如abs(-20)将返回20。

在`Python2.X`版本中，内建模块被命名为**`__builtin__`**，而到了`Python3.X`版本中，却更名为**`builtins`**。

当使用内建模块中函数或其它功能时，可以直接使用，不用添加内建模块的名字；但是，如果想要向内建模块中添加一些功能，以便在任何函数中都能直接使用而不用再进行`import`，这时，就要导入内建模块，在内建模块的命名空间（即`__dict__`字典属性）中添加该功能。在导入时，如果是`Python2.X`版本，就要导入**`__builtin__`**模块；如果是`Python3.X`版本，就要导入**`builtins`**模块。如：在Python2.X中，向内建模块添加一个函数（该函数打印“hello, world”），可以这样写（以下的用法是在主模块中的使用，其它模块请看下面）：
```python
import __builtin__
def print_hello():
    print "hello, world"
__builtin__.__dict__['hello'] = print_hello
print_hello()               # 将打印"hello, world"
hello()                     # 将打印"hello, world"
```
此时，`print_hello`和`hello`两个函数名几乎是一样，但是有一点区别，`print_hello`只能在该模块中使用，而`hello`可以在本程序中的其它任何一个模块中使用，因为`hello`已经放到内建模块中了。

## `__builtins__`

现在，`__builtin__`和`builtins`之间的关系已经说清楚了，现在该说说`__builtins__`了。为了统一`Python2.X`和`Python3.X`，在下面的论述中，内建模块一律统称为`__builtin__`。

由上面的论述，我们知道，**`__builtin__`**存在于`Python2.X`中，而**`builtins`**存在于`Python3.X`中，但是对于**`__builtins__`**，它却同时存在于`Python2.X`和`Python3.X`中。那么它到底是什么东西呢？由名字可知，它肯定与内建模块有关。其实简单地说，它就是对内建模块一个引用。

1、**`__builtins__`**即是引用，那么它内建模块有一个相同点：Python程序一旦启动，它们二者就会在程序员所写的代码没有运行之前就已经被加载到内存中了。

2、虽是一个引用，但**`__builtins__`**和`内建模块`是有一点区别的：

（1）_**无论任何地方要想使用内建模块，都必须在该位置所处的作用域中导入内建模块**_；而对于`__builtins__`却不用导入，**`它在任何模块都直接可见，可以把它当作内建模块直接使用`**（这句并不完全正确，请看第（2）点）。即：**`__builtins__在任何地方、任何模块都可见`**，而**`内建模块名只在相应的作用域中被import后才可以`**（该import并不是把内建模块加载到内存中——内建早已经被加载了，它仅仅是让内建模块名在该作用域中可见）。

（2）**`__builtins__`**虽是对内建模块的引用，但这个引用要看是使用**`__builtins__`**的模块是哪个模块：

    1) 在主模块__main__中：
       __builtins__是对内建模块__builtin__本身的引用，即__builtins__完全等价于__builtin__，二者完全是一个东西，不分彼此。
       它在任何地方都可见，即在任何地方都可使用它。此时，__builtins__的类型是模块类型。

       __builtin__仅仅在导入它时才可见。哪个作用域中使用__builtin__，哪个作用域就要导入它（导入仅仅是让__builitin__
       标识符在该作用域内可见）。一般都是在模块的顶层（即模块的全局作用域）导入__builtin__，这样，其后的任何作用域可
       通过标识符向上查找来引用__builtin__。

    2) 在非__main__模块中：
       __builtins__仅是对__builtin__.__dict__的引用，而非__builtin__本身。它在任何地方都可见。此时__builtins__的类型是字典。

       __builtin__和在主模块中的情况一样。

由上面的异同，我们可以出，**`__builtins__`**、**`__builtin__`**和**`builtins`**之间并没有太大的不同；在使用**`__builtins__`**时，只要注意其引用的到底是`__builtin__`还是`__builtin__.__dict__`即可。

此时，可能会有人说，既然`__builtin__`和`builtins`由于Python版本的不同而不同，导致在写兼容2.X和3.X版本时的代码时比较麻烦，而`__builtins__`在`2.X`和`3.X`中都是一样的，那么，不再使用`builtins`和`__builin__`，改用`__builtins__`不是更好？！这种做法并没有错，但是有一点，在使用`__builtins__`时，要区分是在`主模块__main__`中，还是在其他的`非__main__模块`中。笔者看了Python标准库（比如`gettext`），其中使用的是`__builtin__`（在`Python2.X`中）和`builtins`（在`Python3.X`中），而并没有使用`__builtins__`。这仅仅给一些参考。


## 主模块`__main__`
在Python中，一个代码文件就是一个模块，一个模块就是一个代码文件；用来启动Python或者说首先执行的那个文件（相当于C语言中main主函数所在的C文件）的模块名被Python命名为`__main__`，称为`主模块`，而对于其它被主模块或其他非主模块导入的模块，它们的模块名则是文件名本身（除了后缀.py、.pyc或.pyo等）。每个模块都有一个名为`__name__`的属性，它表示着该模块的名字。除此之外，主模块与其它非主模块之间还有一点区别，比如：
```python
from __future__ import absolute_import
```
该语句在`非主模块`中可以正常使用，反而在`主模块`中，好像没有什么效果——有等无；根据官方文档，`__future__`不能用于主模块中，即`__future__`所在的模块的模块名不能是`__main__`。


## 附录
Python邮件列表中对`__builins__`、`__builtin__`的讨论（至于`builtins`，可以看成是`__builtin__`，其仅因版本不同而已）：

    A little investigation reveals:
        In module __main__:
            __builtins__ is a reference to module __builtin__.
            __builtin__ only exists if you import it.

        In any other module:
            __builtins__ is a reference to module __builtin__'s __dict__.
            __builtin__ only exists if you import it.

    In order of increasing boldness,here are some possible fixes:
        1. Make __builtins__ always refer to a dict. I think there's quite a strong argument for this -- in general,
           you should be able to take the same code and run it as a script or a module with similar behaviour.

        2. Rename __builtins__ so it isn't so easily mistaken for __builtin__. I haven't thought of any awesome
           names to propose.

        3. Unify the roles of the names __builtins__ and __builtin__ -- having both is too confusing.
           a. Instead of putting __builtins__ into every module namespace, import __builtin__ into every module
              namespace.
           b. Do the last resort for name lookups in __builtin__.__dict__ instead of __builtins__.
           c. To make this no slower than it is today, make each module cache a pointer to its __builtin__.__dict__ and
              update that pointer when __builtin__ is reassigned.

    Going all the way to #3 would be the cleanest, I think. Maybethere are other solutions for unifying the two,
    as well -- any ideas?
