
九、高级特性
=========

## （一）装饰器

1、装饰器是为函数和类指定管理代码的一种方式。**`装饰器本身的形式是处理其他的可调用对象的可调用对象`**（如函数）。Python装饰器有两种：`函数装饰器` 和 `类装饰器`。函数装饰器在函数定义的时候进行名称重绑定，提供一个逻辑层来管理函数和方法或随后对它们的调用；类装饰器在类定义的时候进行名称重绑定，提供一个逻辑层来管理类，或管理随后调用它们所创建的示例。简而言之，_**装饰器提供了一种方法，在函数和类定义语句的末尾插入自动运行代码——对于函数装饰器，在def的末尾；对于类装饰器，在class的末尾**_。

2、**`函数装饰器安装包装器对象，以在需要的时候拦截随后的函数调用并处理它们；类装饰器安装包装器对象，以在需要的时候拦截随后的实例创建调用并处理它们。`**

3、装饰器通过自动把函数和类名重绑定到其他的可调用对象来实现这些效果，在def和class语句的末尾做到这点。当随后调用的时候，这些可调用对象可以执行诸如对函数调用跟踪和计时，管理对类实例属性的访问等任务。

4、**`函数装饰器也可以直接来管理函数对象，而不是随后对它们的调用；类装饰器也可以用来直接管理类对象，而不是实例创建调用`**。换句话说，**`函数装饰器可以用来管理函数调用和函数对象，类装饰器可以用来管理类实例和类自身`**。通过返回装饰的对象自身而不是一个包装器，装饰器变成了针对函数和类的一种简单的后创建步骤。

5、函数装饰器设计用来只增强一个特定函数和方法调用，而不是一个完整的对象接口。类装饰器更好地充当后一种角色——因为它们可以拦截实例创建调用，它们可以用来实现任意的对象接口扩展或管理任务。

6、`当主体函数或类定义的时候，装饰器应用一次`；在对类或函数的每次调用的时候，不必添加额外的代码（在未来可能必须改变）。

7、**`函数装饰器`**

（1）**实现：**`装饰器自身是一个返回可调用对象的可调用对象`。也就是说，它返回了一个对象，当随后装饰的函数通过其最初的名称调用的时候，将会调用这个对象——不管是拦截了随后调用的一个包装器对象，还是最初的函数以某种方式的扩展。实际上，装饰器可以是任意类型的可调用对象，并且返回任意类型的可调用对象：函数和类的任何组合都可以使用，尽管一些组合更适合于特定的背景。

（2）**参数：**如果当装饰器返回的可调用对象是一个内嵌在装饰器中的函数对象，在调用时，装饰器自身接受被装饰的函数，返回的调用对象会接受随后传递给被装饰函数的名称的任何参数（典型的是，被装饰的函数的参数是什么——如个数及类型，装饰器返回的可调用对象函数的参数也是什么）。这和类方法的工作方式相同：隐含的实例对象只是在返回的可调用对象的第一个参数中出现。例子：
```python
def decorator(arg1=22, arg2=33):
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            print arg1, arg2
            return func(*args, **kwargs)
        return wrapper
    return inner_decorator

@decorator(44)
def F(a, b):
    print a,b

F(77, 88)       # 将输出： 44 33
                #         77 88
```

（3）**例子：**
```python
def decorator(func):
    print "decorator function"
    return func

@decorator
def F():
    print "F test"

F()     # 将输出：decorator function
        #        F test
```

8、**`类装饰器`**

（1）**实现：**类装饰器的实现原理基本上与函数装饰器的实现原理一致，区别不大。

9、**注意事项**

（1）当普通函数装饰器应用到类中的方法上时，将出现意外效果。**`一般不要将将普通函数装饰器应用到类中的方法上`**。`如果确实需要将普通函数装饰器应用到类中的方法上，则需要特别设计`。问题例子（伪代码）：
```python
def decorator(F):
    def wrapper(*args):
        # F(*args) runs func or method
    return wrapper

@decorator
def func(x, y):
    ...
func(6, 7)      # 真实的是调用wrapper(6, 7)

class C:
    @decorator
    def method(self, x, y):
        ...

X = C()
X.method(6, 7)  # 真实的是调用wrapper(X, 6, 7)
```

（2）`类装饰器支持多个实例时，要特别设计`。问题例子：
```python
class Decorator:
    def __init__(self, C):
        self.C = C

    def __call__(self, *args):
        self.wrapped = self.C(*args)
        return self

    def __getattr__(self, attrname):
        return getattr(self.wrapped, attrname)

@Decorator
class C: ...        # C = Decorator(C)

x = C()             # 真实的是调用Decorator.__call__(self)，最后x等于self（即Decorator实例对象本身）
y = C()             # 真实的是调用Decorator.__call__(self)，最后y等于self（即Decorator实例对象本身），y覆盖掉x
```

（3）在Python中，函数或类本身也是一个对象，所以它们也有属性（比如表示函数或类文档的__doc__）；而且函数或类不同，它们的属性也不同。在对函数或类使用装饰器时，为了使装饰者更像被装饰者（即，从名字到属性等等，装饰者和被装饰者一样），使其二者看起来不分彼此，`可以使用 functools 标准库中的 wraps 装饰器来装饰我们的装饰器，它（wraps）能捕获被我们的装饰器装饰的函数或类，并将其属性等信息赋值给我们的装饰器`。否则，可以通过查看装饰者和被装饰者的属性来辨别出：被装饰者装饰过的东西不再是原来的模样了。
例子：
```python
def decorator(F):
    @wraps(F)
    def  inner_decorator(*args, **kwargs):
        """inner_decorator doc"""
        print("decorator")
        # F(*args) runs func or method
        return F(*args)

    return inner_decorator

@decorator
def  add(a, b):
    """add doc"""
    return a+b

print(add(1+2))               # 将输出 decorator
                              #       3
print(add.__doc__)            # 将输出 "add doc"，而不是"inner_decorator doc"
print(add.__name__)           # 将输出 "add"，而不是"inner_decorator"
```

## （二）属性管理
`特性`、`描述符`、`运算符重载（__getattr__、__getattribution__、__setattr__、__delattr__等）`、`__slots__`、`装饰器`等方法。

本内容较多，分录在“[`Python中的属性管理`](./python-attr.md)”一章中。


## （三）元类

### 1、基本介绍
像装饰器一样，**`元类允许我们拦截并扩展类的创建`**——它提供了一个API以插入在一条class语句结束时运行的额外逻辑，尽管是以与装饰器不同的方式。

另一方面，元类为各种没有它而难以实现或不可能实现的编码模式打开了大门，并且对于那些追求编写灵活的API或编程工具供其他人使用的程序员来说，它特别有用。

借Python开发者Time Peters在comp.lang.python新闻组中的话来说：“`[元类]比99%的用户所担心的魔力要更深。如果你犹豫是否需要它们，那你不需要它们（真正需要元类的人，能够确定地知道需要它们，并且不需要说明为什么需要）。`”

换句话说，**`元类主要是针对那些构建API和工具供他人使用的程序员`**。在很多情况下（如果不是大多数的话），它们可能不是应用程序工作的最佳选择。

和类装饰器不同，**`类装饰器通常是添加实例创建时运行的逻辑，而元类在类创建（即生成类的时候）时运行`**。

### 2、类是类型的实例

由于在Python中，一切皆对象，所以类也对象，类型也是对象。

    (1) 在Python3.0中，用户定义的类对象是名为type的对象的实例，type本身是一个类。
    (2) 在Python2.6中，新式类继承自object，它是type的一个子类；传统类是type的一个实例，并且并不创建自一个类。

**`实例创建自类，而类创建自type`**。在Python3.X中，“类型”的概念与“类”的概念合并了。实际上，这两者基本上是同义词——类是类型，类型也是类。即：

    (1) 类型由派生自type的类定义；
    (2) 用户定义的类是类型类的实例；
    (3) 用户定义的类是产生它们自己的实例的类型。

由上我们可得出一个疑问：既然在Python中一切皆对象，那么type类型也是一个对象，而对象又由类来创建，那么是什么创建了type类型呢？这有点像“到底是先有鸡还是先有蛋”的问题。根据进化论，这个问题会得到解答——先有鸡，即先有非鸡的物种进化成鸡，然后鸡再生蛋，而蛋是不能进化的。然而，我们上面的疑问也会有个答案：在创建type类型对象时，关于创建它的类，用一个指针指向它自身即可。注：Python内建类型会在Python解析器启动的时候被静态创建，作为一个对象存在，永不改变。

### 3、元类是Type的子类

由于类实际上是type类的实例，通过type定制的子类中创建自定义类，我们可以实现各种定制的类。

在Python3.X中以及在Python2.6的新式类中：

    (1) type是产生用户定义的类的一个类；
    (2) 元类是type类的一个子类；
    (3) 类对象是type类的一个实例，或一个子类。

换句话说，为了控制创建类以及扩展其行为的方式，我们所需要做的只是指定一个用户定义的元类，而不是常规的type类。

注：这个类型实例关系与继承并不完全相同：用户定义的类可能也拥有超类，它们及其实例从那里继承属性（继承超类在class语句的圆括号中列出，并且出现在一个类的`__bases__`元组中）。类创建自的类型，以及它是谁的实例，这是不同的关系。

我们已经知道，当Python遇到一条class语句时，它会运行其嵌套的代码块以创建其属性——所有在嵌套代码块的顶层分配的名称都产生类对象中的属性。这些名称通常是嵌套的def所创建的方法函数，但是，它们也可以是由所有实例共享的类数据的任意属性。

### 4、元类标准协议

_**从技术上讲，Python遵从一个标准的协议来使这发生：在一条class语句的末尾，并且在运行了一个类定义中的所有嵌套代码之后（其行为和时机就像装饰器（Decorator）一样），它调用type对象来创建class对象**_：
```python
class = type(classname, superclasses, attributedict)
```

type对象反过来定义了一个`__call__`运算符重载方法，当调用type对象的时候，该方法运行两个其他的方法：
```python
type.__new__(typeclass, classname, superclasses, attibutedict)
type.__init__(class, classname, superclasses, attibutedict)
```

其中，**`typeclass就是元类本身，class是由__new__方法创建的新的class对象`**，如随后例子中的Spam类本身；**`__new__方法创建并返回一个新的class对象，并且随后的__init__方法初始化了该新创建的class对象`**；这有点像C++ STL中对象的构造过程：__new__相当于C++ STL中的对象的内存分配，__init__相对于C++中的构造函数。例如：
```python
class Span(Eggs):
    data = 1

    def meth(self, arg):
        pass
```

Python先从内部运行嵌套的代码块来创建该类的两个属性（data和meth），然后在class语句的末尾调用type对象，产生class对象：
```python
Spam = type('Spam', (Eggs,), {'data': 1, 'meth': meth, '__module__': '__main__'})
```
由于这个type调用在class语句的末尾进行，所以它是用来扩展或处理一个类的、理想的钩子。


#### 元类协议反思

在类定义的末尾，Python会运行一个可调用对象（其传递的参数依次为`classname`、`superclasses`、`attributedict`，其中，`classname是个表示类名的字符串，superclasses是包含所有基类的元组，attributedict是个包含所有实例或类属性的字典）`，该可调用对象可以是任何可以调用的对象（如函数、具有`__call__`方法的实例对象等等），该可调用对象返回一个可以创建实例的类对象。默认的可调用对象（即type类中的`__call__`方法）是先后依次调用该可调用对象的`__new__`、`__init__`方法（即`type.__new__`和`type.__init__`）。如果该可调用对象不返回一个type类或其子类，或者重载`type.__call__`的执行流程，那么可以完成不再重载、调用`type.__new__`、`type.__init__`等方法；如果该可调用对象返回一个由type类（或其子类）创建的实例对象（通过调用`__call__`方法），那么Python会继续调用`type.__new__`、`type.__init__`等方法，此时，我们可以重载这两个方法来完成相应的类创建（而不是类创建实例对象）时的管理。


### 5、类定义的执行流程
1. 确定合适的元类
2. 准备类的命名空间
3. 执行类的定义体
4. 创建类对象

#### 5.1 确定合适的元类
在定义类时，根据下面的顺序来决定其合适的元类：
1. 如果没有指定Bases或显式的元类，则使用 `type`。
2. 如果显式地指定一个元类，并且它不是 `type` 的实例，则将直接它作为元类。
3. 如果显式地把 `type` 的一个实例作为元类，或 Bases 被定义，则使用最终派生的元类。

#### 5.2 准备类的命名空间
一旦元类被确定，随即准备类的命名空间。

如果元类有 `__prepare__` 属性，则会以 `namespace = metaclass.__prepare__(name, bases, **kwargs)` 的形式被调用。否则，类的命名空间则被初始化为一个空字典（dict）。

注：`kwargs` 中的键值对（如果有）都均来源于类定义。

#### 5.3 执行类的定义体
类的定义体将会以 `exec(body, globals(), namespace)` 方式被执行。这与普通的 `exec()` 调用的主要区别在于：当在函数内定义一个类时，词法作用域允许类的定义体（包括所有的方法）引用当前作用域或外层作用域中的名字。尽管如此，在函数中定义的类的方法，仍然不能引用类作用域中的名字，类属性必须通过类方法或实例方法的第一个参数来访问，因此，所有的静态方法均不能访问类的属性。

在执行类的定义体时，将填充类的命名空间（也即是类的属性）。

#### 5.4 创建类对象
一旦执行完类的定义体，Python 解析器将调用 `metaclass(name, bases, namespace, **kwargs)` 来创建类对象。注：其中的 `kwargs` 同 `__prepare__` 中的一样。

创建好类对象后，如果在类定义中还有类装饰器，则将其传递给类装饰器，装饰器返回的对象被绑定到本地命名间，就像被定义的类一样。

#### 5.5 例子
```python
# This example comes from https://docs.python.org/3/reference/datamodel.html#metaclass-example
class OrderedClass(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        result.members = tuple(namespace)
        return result

class A(metaclass=OrderedClass):
    def one(self): pass
    def two(self): pass
    def three(self): pass
    def four(self): pass

>>> A.members
('__module__', 'one', 'two', 'three', 'four')
```

### 6、元类的使用方法
在Python3.X中声明元类的方法：
```python
class Spam(metaclass=Meta):
```

在Python2.6中声明元类的方法：
```python
class Spam(object):
    __metaclass__ = Meta
```
其中，`__metaclass__`和`metaclass`是用来标识元类的，而Meta即是元类对象。

当以上面的方式声明元类的时候，创建类对象的调用在class语句的末尾运行，调用的是元类而不是默认的type：
```python
class = Meta(classname, superclasses, attributedict)
```

由于元类是type的一个子类，所以type类的`__call__`把创建和初始化新的类对象的调用委托给元类，如果它定义了这些方法的定制版本：
```python
Meta.__new__(Meta, classname, superclasses, attributedict)
Meta.__init__(class, classname, superclasses, attributedict)
```

由于以上我们知道，元类是按照标准协议来运行的，这也就是说，只要我们按照标准协议的流程，那么我们可以使用任何东西，而不仅仅是type或其子类。例如：把一个普通函数作为“元类”：
```python
def MetaFunc(classname, supers, classdict):
    print("MetaFunc")
    return type(classname, supers, classdict)

class Egg:
    pass

class Foo(Egg, metaclass=MetaFunc):
    data = 1

    def __init__(self):
        print("Foo __init__")

    def meth(self, args):
        pass

X = Foo()
```
以上将先后输出：
```python
MetaFunc        # 在定义类Foo时运行的
Foo __init__    # 在用类Foo创建一个实例X时运行的
```

注：**`元类中的__new__、__init__和自定义类定义中的__new__、__init__是不同的，元类中的__new__和__init__是在创建类对象（即类，因为类也是一个对象）时运行的，是用来创建和初始化类对象的；而类定义中的__new__和__init__是在用该类创建一个实例时运行的，是用来创建和初始化实例的`**。更深层次的细节：之所以元类和自定义类都有`__new__`、`__init__`等方法，是因为，自定义类（默认地）继承自object类，不规范地讲，元类和object类在底层都是属于自type类，可以看作元类和object类都继承自type类，不同之处是object对`__call__`方法作了更改，或是，对object类的处理做了更改。

### 7、实例与继承的关系

#### 7.1 元类继承自type类

尽管它们是一种特殊的角色元类，但元类是用class语句编写的，并且遵从Python中有用的OOP模型。例如，就像type的子类一样，它们可以重新定义type对象的方法，需要的时候重载或定制它们。元类通常重新定义type类的`__new__`和`__init__`，以定制类创建和初始化；但是，如果它们希望直接捕获类末尾的创建调用的话，它们也可以重新定义`__call__`。尽管元类不常见，它们甚至是返回任意对象而不是type子类的简单函数。

#### 7.2 元类声明由子类继承。
在用户定义的类中，`metaclass=M` 声明由该类的子类继承，因此，对时在超类链中继承了这一声明的每个类的构建，该元类都将运行。

#### 7.3 元类属性没有被类实例继承。
元类声明指定了一个实例关系，它和继承不同。由于类是元类的实例，所以元类中定义的行为应用于类，而不是类随后的实例。实例从它们的类和超类中获取行为，但是不是从任何元类中获取行为。从技术上讲，实例属性查找通常只是搜索实例及其所有类的`__dict__`字典；元类不包含在实例查找中。

为了说明最后两点，考虑如下的例子：
```python
class MetaOne(type):
    def __new__(meta, classname, supers, classdict):
        print("In MetaOne.new:", classname)
        return type.__new__(meta, classname, supers, classdict)

    def toast(self):
        print("MetaOne.toast")

class Super(metaclass=MetaOne):      # class语句是可运行语句，将输出 In MetaOne.new: Super
    def spam(self):
        print("Super.spam")

class C(Super):                      # class语句是可运行语句，将输出 In MetaOne.new: C
    def eggs(self):
        print("C.eggs")

X = C()
X.eggs()    # 从C中继承，输出 C.eggs
X.spam()    # 从Super中继承，输出 Super.spam
X.toast()   # 并不从元类中继承，将引发AttributeError('C' object has no attribute 'toast')异常
```
