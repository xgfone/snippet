
十二、Python C 扩展
=================

Python C 扩展首先是个 C 源文件，一般地写作要求如下：

    （1）包含头文件 Python.h。如：#include <Python.h>
    （2）定义一个初始化函数。
        当导入该模块时，Python会调用该函数，以初始化该模块（该函数只会被调用一次，调用时机就在该模块第一次被导入时）。
        该初始化函数的格式有如下要求：
            A. 函数名必须以 init 开头，其后的所有字符表示模块名，如："init_MyModule"表示模块名是"_MyModuld"。
            B. 不能有返回值，即返回值必须是 void。
            C. 参数列表必须为空或 void。
    （3）在初始化函数中初始化该模块。
        Python提供了多个初始化（或创建）一个模块的函数，常用的有 Py_InitModulde()，它需要两个参数：
            第一个参数是个字符串，表示当前模块的名字；
            第二个参数是个 PyMethodDef 类型的数组，其中最后一个元素必须是全空，以表明数组结束。
    (4) (可选)为当前模块定义一些属性或函数。
        常用的是函数，即 Py_InitModule 函数的第二个参数。该参数是个数组，其中每个元素的类型是 PyMethodDef 结构体，
        有如下成员：
            第一个是字符串，表示函数名；
            第二个是C函数指针，指向一个C语言函数的具体实现；
            第三个是宏常量，表示参数的类型（可变长参数或字典参数）；
            第四个是字符串，表示函数的说明文档，就是Python源码中的函数文档。
        这个数组参数必须以 {NULL, NULL, 0, NULL} 成员结尾，以表明数组到此结束（相当于C语言字符数组中的'\0'）。

### 注意
当前C 扩展源文件的名字必须是模块的名字（除源文件的后缀外，如 `.c`）。因此，我们可以发现，Python C 扩展有三处须要保持一致:

    源文件的名字（除后缀外）
    初始化函数的函数名（除前缀init）
    Py_InitModule函数的每一个参数，

如果不一致，则导入该模块，将会抛出 ImportError 异常。

### 说明

Python3 的 C 扩展写法和 Python2 的略有差异，主要是在初始化函数的定义和模块的创建。

1. 初始化函数的定义：

    1. 返回值是 `PyMODINIT_FUNC`，而非 `void`。
    2. 初始化函数的名字模板为 `PyInit_XXX`，而非 `initXXX`。

2. 模块的创建：

    使用宏 `PyModule_Create` 创建，其参数只有一个，即 `struct PyModuleDef *`。

`struct PyModuleDef` 可用如下方式初始化：
```c
static struct PyModuleDef XXX_Module = {
        PyModuleDef_HEAD_INIT,              // 初始化头
        "XXX",                              // 模块名
        "This is the doc of the module",    // 模块的文档
        -1,                                 // 可以忽略它
        XXX_Methods                         // 模块的属性、方法集，它即是 Python2 中 Py_InitModule 宏的参数
};
```

初始化函数的定义形如：
```c
PyMODINIT_FUNC
PyInit_XXX()
{
        return PyModule_Create(&XXX_Module);
}
```

### 样例

这里有一个样例，曾是笔者为 Netlink 封装的 Python C 扩展模块，参见 https://github.com/xgfone/gnetlink 项目。

https://github.com/xgfone/gnetlink/blob/master/src/test_netlink/_netlink.c
