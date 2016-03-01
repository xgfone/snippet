
Python打包指南
============

最佳开源 Python 应用程序通常会提供出色的打包功能。我们首先将了解有关什么是打包及其基本实现的详细信息。然后更进一步探索与打包相关的版本控制与发布工作。


一个成功的开源项目的其核心功能是打包功能，而出色的打包功能的关键在于版本控制。因为项目是开源的，所以您希望发布的包能够体现出开源社区所具备的优点。不同的平台与语言具有不同的打包机制，本文主要讲述的是 Python 及其打包机制。本文所讨论的打包机制可以作为您的基础学习，此外还提供了大量的实例，可让您快速起步。

### 关注打包的理由
除了正确做法这条理由之外，打包软件还有三条实际的理由：

    易用性
    稳定性（带有版本控制）
    发布

尽量减少用户安装您的应用程序的工作量是值得的。打包会让您的软件变得更容易访问和安装。如果其安装流程更加简便，用户就会更加愿意使用您的软件。如果在 `Python Package Index (PyPI)` 上发布您的包，那么就可以通过像 `pip` 或 `easy_install` 这样的实用工具轻易地对其进行访问。

另外，通过对包进行版本控制，可以指定用户的项目依赖于某一个特定版本。例如，将 Pinax 指定为 `0.9a2.dev1017` 版本，表达如下：

    Pinax==0.9a2.dev1017

这样就会强制项目使用 `0.9a2.dev1017` 版本的 Pinax。

如果您稍后发布可能破坏接口的软件变更，版本控制会保证更好的稳定性。它允许用户确切地了解他们获得了什么，并使跟踪版本之间差异的工作变得更加轻松。此外，项目开发人员可以确切地知道他们正在基于什么进行编码。

将包发布到 PyPI（或者您自己的发布服务器）上的一种常用方法是创建一个源发布并上传。源发布是将项目源代码打包为一个可发布单元的一种标准方式。创建二进制发布有多种途径，但是为了开源，发布源代码也合乎情理。创建源发布可充许人们能够轻易地使用工具，在 Internet 上查找和下载软件并执行全自动软件安装。此过程不仅有助于本地开发，而且对软件的部署也有助益。

因此，通过让用户能够更加轻松地集成与安装您的软件，使用支持可靠固定技术的优秀版本控制，并发布您的包以实现更好的分布，您项目取得成功并获得广泛采用的机会就将大增。更广泛的采用意味着更多的参与者，这想必是每一位开源开发人员的希望。


### setup.py 文件的剖析
setup.py 脚本的用途之一是充当可执行文件，您可以运行它来打包软件并将其上传到发布服务器上。当您浏览流行的 Python 库时，setup.py 脚本的内容可能存在相当大的差异。本文主要关注于基础知识。

setup.py 文件有多种用途，但在这里创建它的目的是运行以下命令：
```
$ python setup.py register
$ python setup.py sdist upload
```
第一个命令 `register` 使用 setup.py 脚本中 `setup()` 函数提供的信息，并为您的包在 PyPI 上创建了一个入口。它不会上传任何内容，相反它会创建关于项目的元数据，以便您能够随后上传与保存版本。接下来的两个命令是串连在一起使用的：`sdist upload` 构造了一个源发布，然后将它上传到 PyPI。但是有一些先决条件，比如要设置您的 `.pypirc` 配置文件并实际写入 setup.py 的内容。

首先配置 `.pypirc` 文件，该文件应该位于您的主目录（根据操作系统的不同而有所变化）中。在 `UNIX®`、`Linux®` 与 `Mac OS X` 上，输入 `cd ~/` 即可访问该目录。该文件的内容应该包含您的 PyPI 证书，如清单 1 中所示。

##### 清单 1. 典型的 `.pypirc` 文件
```ini
[distutils]
index-servers =
        pypi
[pypi]
username:xxxxxxxxxxxxx
password:xxxxxxxxxxxxx
```

接下来，访问 PyPI 并注册一个账号（不用担心，它是免费的）。将您在 PyPI 上创建的用户名与密码放入 `.pypirc` 文件中，并确保文件名为 `~/.pypirc`。

在编写 setup.py 脚本时，您必须决定要在 PyPI 索引页面上显示什么内容，以及您想给项目取什么名称。从复制我对项目使用的 setup.py 模板开始（参见清单 2）。跳过导入与函数，查看模板末端，看看需要修改什么地方来适应您的项目。

##### 清单 2. setup.py 模板
```python
PACKAGE = ""
NAME = ""
DESCRIPTION = ""
AUTHOR = ""
AUTHOR_EMAIL = ""
URL = ""
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD", url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data=find_package_data(PACKAGE, only_in_packages=False	),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
```
首先要注意，这个模板希望您的项目具有两个不同文件。第一个文件用于 `long_description`，它读取与 setup.py 位于同一目录中的 README.rst 文件的内容，并将内容以字符串形式传递给 `long_description` 参数。此文件用于填充 PyPI 上的登录页面，因此在文件中简要描述项目并显示一些使用实例是个好主意。第二个文件是包的 `__init__.py` 文件。这里并没有明确提及它，但设置 `VERSION` 变量的行用于导入了您的包。而当执行此项操作时，Python 还需要一个 `__init__.py` 文件和一个在该模块中定义的名为 `__version__` 的变量。就目前而言，只要将它设置为一个字符串即可：
```python
# __init__.py
__version__ = "0.1"
```

现在，让我们看一看其余的输入：

    PACKAGE 是您项目中的 Python 包。它是顶级文件夹，其中包含应该与 setup.py 文件位于相同目录中的 __init__.py 模块，例如：
    /-
        |- README.rst
        |- setup.py
        |- dogs
            |- __init__.py
            |- catcher.py
    因此，这里的 dogs 就是您的包。

    NAME 一般类似或等同于您的 PACKAGE 名称，但可以是您希望的任何内容。NAME 就是人们引用您的软件时使用的名称，
    这个软件名称将会列在 PyPI 中，而且更重要的是，用户将使用这个名称来安装软件（例如，pip 安装 NAME）。

    DESCRIPTION 只是对您的项目的一段简要描述，一句话便已足够。

    AUTHOR 与 AUTHOR_EMAIL 正如它们字面上的意思：您的姓名和电子邮件地址。
    这些信息是可选的，但提供电子邮件地址是比较实际的做法，因为人们可能希望与您取得联系。

    URL 是项目的 URL。这个 URL 可能是一个项目网站、Github 库或您希望的任意 URL。再次强调，这些信息是可选的。

您可能还希望提供许可证与分类。


### 版本控制
版本控制本身就是一个很大的主题，但在打包时不得不提到它，因为优秀的打包需要正确的版本控制。 版本控制是您与用户进行某种形式的沟通：它也允许用户在其产品中实现更好的稳定性与可靠性。通过版本控制，您可以告诉用户您修改了哪些内容，并为这些修改出现的位置设定明显的界限。

在 [`Python Enhancement Proposal (PEP) 386`](https://www.python.org/dev/peps/pep-0386/) 中可以找到对 Python 包进行版本控制的一种标准。它给出了一些实用的规则。即使您没有阅读和理解或者甚至是赞同 PEP，最好也按照它来行事，因为越来越多的 Python 开发人员已经习惯于这样做。

另外，版本控制不仅用于您上传到 PyPI 上的稳定版本，而且还用于使用 devNN 后缀的开发版本。将这些开发版本上传到 PyPI 上通常不太好，但您可以通过设置自己公共的（或私有的）发布服务器，让它们变为可公共访问的。然后，想使用最新版本的用户就可以在他们的 pip 需求 .txt 文件中进行引用。下面给出了版本控制的一些例子：

    1.0.1         # 1.0.1 final release
    1.0.2a        # 1.0.2 Alpha (for Alpha, after Dev releases)
    1.0.2a.dev5   # 1.0.2 Alpha, Dev release #5


### 发布
如果没有发布，人们一般无法找到和安装您的软件。大多数时候，您需要把自己的包发布到 PyPI 上。在设置 `.pypirc` 配置文件之后，您传递给 setup.py 的 `upload` 命令将把您的包传输给 PyPI。通常，您在这样做的同时还会构建一个源发布：
```shell
$ python setup.py sdist upload
```

如果您使用的是自己的发布服务器，而且 `.pypirc` 文件中的授权部分也包含了这个新位置，只要在上传时引用它的名称即可：
```shell
$ python setup.py sdist upload -r mydist
```

### 搭建您自己的发布服务器
在开源环境中使用自己的发布服务器的主要原因是提供一个发布开发版本的位置，因为 PyPI 实际上只应该包含稳定的版本。例如，您很可能想使用如下命令：
```shell
$ pip install MyPackage
```

安装从 PyPI 上发现的最新稳定版本。然而，如果您添加后来的开发版本，该命令会结束最新版本的安装，也就是您的开发版本。固定版本始终是正确的做法，但并非所有的用户都能坚持这么做。因此，确保在指定版本号时总是返回最新的稳定版本。

一种两全其美的方法（只对 pip 的默认用法公开稳定的版本，同时允许用户安装打包的开发版本）是使用自己的发布服务器。Pinax 项目为它所有的开发版本都做了这项工作，网址是 http://dist.pinaxproject.com 。

发布服务器只是一个索引，基于 `Hypertext Transfer Protocol (HTTP)` 协议为服务器上的文件提供服务。它的文件结构应该如下：

    /index-name/package-name/package-name-version.tar.gz

通过在 Web 服务器上配置 Basic-Auth，您可以将服务器变为私有。您可能还想添加一些工具来上传源发布。为此，需要添加代码来处理上传，解析文件名，以及创建与上述模式相匹配的目录路径。这种结构在 Pinax 项目中已经开始应用，该项目拥有几个库。


### pip 与 virtualenv
尽管本文的讲述重点是打包，这部分内容描述了如何使用包，以及优秀的打包与版本控制为用户能够带来的好处。

`pip` 是可以直接安装的工具，但我建议使用它作为 `virtualenv` 的一部分。我建议对与 Python 相关的所有内容均使用 `virtualenv`，因为它可以保持 Python 环境的干净。正如一台虚拟机允许同时运行多个操作系统一样，`virtualenv` 也支持您同时运行多个 Python 环境。我没有在我的系统 Python 中安装任何内容，而是为我使用的每个新项目或实用工具都创建了一个新的 `virtualenv`。

安装 `virtualenv` 后，立即就可以使用：
```shell
$ mkvirtualenv —no-site-packages testing
$ pip install Pinax
$ pip freeze | grep Pinax
$ pip uninstall Pinax
$ pip install —extra-index-url=http://dist.pinaxproject.com/fresh-start/ Pinax==0.9a2.dev1017
$ pip freeze | grep Pinax
```
注意，第一个 pip 安装是从 PyPI 下载和安装的。`pip freeze` 可以显示当前 `virtualenv` 中已安装的所有包版本。`pip uninstall` 的用途与您猜想的完全一样：将它自己从 `virtualenv` 中删除。接下来，您要在全新的库中安装一个开发版本，地址是 http://dist.pinaxproject.com ，以便获取 `Pinax 0.9a2.dev1017` 版的开发版本。

无需访问网站，下载 `tarball`，并将代码与网站包建立符号链接（这是我通常的做法，会引发很多问题）。用户只有在项目中实现优秀的打包、发布与版本控制，才能做到这一切。


### 结束语
总的说来，您花费一些时间来学习打包的艺术与科学是值得的。由于对包进行版本控制会带来易安装性和稳定性，所以您的软件会被更多用户采用。使用 [参考资料](http://www.ibm.com/developerworks/cn/opensource/os-pythonpackaging/#resources) 和本文所提供的模板 setup.py，您可以快速而方便地给项目增加打包功能。通过正确的版本控制与用户沟通，站在用户的角度去考虑，可以让他们更容易跟踪版本之间的变化。最后，由于 `pip` 与 `virtualenv` 赢得了更为广泛的采用，对发布包的依赖（位于 PyPI 或您自己的发布服务器上）越来越大。因此，一定要发布你想要与全世界分享的项目。

---

From: http://www.ibm.com/developerworks/cn/opensource/os-pythonpackaging/
