
十、其他要点
=========

### （一）向类中添加方法

#### 1、手工向类中添加方法
该方法是直接通过给类增加新的属性的方式来完成。

##### (1) 添加一般实例方法
```python
class Client1:
    def __init__(self, value):
        self.value = value

    def spam(self):
        return self.value * 2

class Client2:
    value = "ni?"

def eggsfunc(obj):
    return obj.value * 4


def hamfunc(obj, value):
    return value + 'ham'

Client1.eggs = eggsfunc
Client1.ham = hamfunc

Client2.eggs = eggsfunc
Client2.ham = hamfunc

X = Client1("Ni!")
print(X.spam())           # 输出 Ni!Ni!
print(X.eggs())           # 输出 <class '__main__.Client1'>
                          #     Ni!Ni!Ni!Ni!
print(X.ham("bacon"))     # 输出 <class '__main__.Client1'>
                          #     baconham

Y = Client2()
print(Y.eggs())           # 输出 <class '__main__.Client2'>
                          #     ni?ni?ni?ni?
print(Y.ham("bacon"))     # 输出 <class '__main__.Client2'>
                          #     baconham
```

#####（2）添加静态方法和类方法
```python
class Client1:
    pass

class Client2:
    pass

@staticmethod
def staticfunc():
    print("static method")

@classmethod
def classfunc(cls):
    print(cls)

Client1.staticmethod = staticfunc
Client2.staticmethod = staticfunc

Client1.classmethod = classfunc
Client2.classmethod = classfunc

X = Client1()
X.staticmethod()   # 输出 static method
X.classmethod()    # 输出 <class '__main__.Client1'>

Y = Client2()
Y.staticmethod()   # 输出 static method
Y.classmethod()    # 输出 <class '__main__.Client2'>
```

#### 2、基于元类向类中添加方法
该方法是，在元类中的`__new__`或`__init__`方法中，向新建的class对象的属性字典添加方法。
```python
def instancefunc(self):
    print(type(self))

@staticmethod
def staticfunc():
    print("static method")

@classmethod
def classfunc(cls):
    print(cls)

class Meta(type):
    def __new__(meta, classname, supers, classdict):
        classdict['instance_method'] = instancefunc
        classdict['static_method'] = staticfunc
        classdict['class_method'] = classfunc
        return type.__new__(meta, classname, supers, classdict)

class Client1(metaclass=Meta):
    pass

class Client2(metaclass=Meta):
    pass

X = Client1()
X.instance_method()    # 输出 <class '__main__.Client1'>
X.class_method()       # 输出 <class '__main__.Client1'>
X.static_method()      # 输出 static method

Y = Client1()
Y.instance_method()    # 输出 <class '__main__.Client2'>
Y.class_method()       # 输出 <class '__main__.Client2'>
Y.static_method()      # 输出 static method
```

#### 3、使用装饰器添加类方法
该方法和手工添加相似，不同之处在于将手工添加方法封装到一个装饰器中。
```python
def instancefunc(self):
    print(type(self))

@staticmethod
def staticfunc():
    print("static method")

@classmethod
def classfunc(cls):
    print(cls)

def decorator(cls):
    cls.instance_method = instancefunc
    cls.class_method = classfunc
    cls.static_method = staticfunc
    return cls

@decorator
class Client:
    pass

X = Client()
X.instance_method()    # 输出 <class '__main__.Client'>
X.class_method()       # 输出 <class '__main__.Client'>
X.static_method()      # 输出 static method
```

###（二）向类中添加属性
向类中添加属性的方式和向类中添加方法的方式相同，唯一不同的是是，向类中添加的属性属于类的属性，不属于类实例的属性（类的属性和类实例的属性是不对的），没有办法以这些方式来给类实例添加属性，因为类实例的属性是在类实例创建时添加的，而此时类实例还没有创建。关于“`类的属性`”和“`类实例的属性`”，请参见“[`Python中的属性管理`](./python-attr.md)”一章。


###（三）Python2中的编码错误问题
在Python2中，常常出现编码错误和乱码问题（这种情况在Python3很少出现，因为Python3的普通字符串是用UNICODE编码），其解决办法建议使用`__future__`模块中的`unicode_literals`特性——它将普通字符串会编码成UNICODE字符串，该特性在Python3中默认被打开。具体情况是：在每个Python文件的第一个非注释行使用
```python
from __future__ import unicode_literals
```

关于Python编码的问题，具体的请参见 [`Python文件编码`](./python-file-encoding.md)。
