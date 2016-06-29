## 修改 `pypi` 源

当使用 `pip` 安装软件包时，如果无法访问官方 `pypi` 源，或者想要使用非官方 `pypi` 源时，可以指定一个特定的 `pypi` 源，此时 `pip` 将会使用该源而非官方源。

以下假设使用豆瓣的 pypi 源：`http://pypi.douban.com/simple`。

### 方法一
检查文件 `~/.pip/pip.conf` 是否存在，如果不存在，则创建之。然后，在其中写入以下内容
```ini
[global]
index-url = http://pypi.douban.com/simple
```

注：
- 关于 `pip.conf` 文件的查找路径，请参见 `https://pip.pypa.io/en/stable/user_guide/#config-file`。
- 在 Windows 系统下，配置文件的名字为 `pip.ini`。

### 方法二
当使用 `方法一` 后，发现使用 `pip` 安装软件包时，有时还是会从默认的官方源 `https://pypi.python.org` 下载。（注：有人发现的现象是：使用 `pip` 安装时，则从指定源下载；而使用 `python setup.py install` 安装时，还是从默认的官方源下载。）

此时需要修改 `distutils` 的配置，即创建一个 `~/.pydistutils.cfg` 文件，然后写入以下内容即可
```ini
[easy_install]
index_url = http://pypi.douban.com/simple
```

### 方法三
在和 `setup.py` 同级目录下，放置一个 `setup.cfg` 文件，然后写入以下内容即可
```ini
[easy_install]
index_url = http://pypi.douban.com/simple
```

### 探索 `setup.py`
对于 `方法二` 和 `方法三` 的探索如下。

在 `distutils` 标准库中，`dist.py` 文件中有个 `find_config_files` 方法，它负责搜索配置文件。

```python
def find_config_files(self):
    """Find as many configuration files as should be processed for this
    platform, and return a list of filenames in the order in which they
    should be parsed.  The filenames returned are guaranteed to exist
    (modulo nasty race conditions).

    There are three possible config files: distutils.cfg in the
    Distutils installation directory (ie. where the top-level
    Distutils __inst__.py file lives), a file in the user's home
    directory named .pydistutils.cfg on Unix and pydistutils.cfg
    on Windows/Mac; and setup.cfg in the current directory.

    The file in the user's home directory can be disabled with the
    --no-user-cfg option.
    """
    files = []
    check_environ()

    # Where to look for the system-wide Distutils config file
    sys_dir = os.path.dirname(sys.modules['distutils'].__file__)

    # Look for the system config file
    sys_file = os.path.join(sys_dir, "distutils.cfg")
    if os.path.isfile(sys_file):
        files.append(sys_file)

    # What to call the per-user config file
    if os.name == 'posix':
        user_filename = ".pydistutils.cfg"
    else:
        user_filename = "pydistutils.cfg"

    # And look for the user config file
    if self.want_user_cfg:
        user_file = os.path.join(os.path.expanduser('~'), user_filename)
        if os.path.isfile(user_file):
            files.append(user_file)

    # All platforms support local setup.cfg
    local_file = "setup.cfg"
    if os.path.isfile(local_file):
        files.append(local_file)

    if DEBUG:
        self.announce("using config files: %s" % ', '.join(files))

    return files
```

`distutils` 标准库会依次在以下目录中查找配置文件： (1)系统目录，(2)用户主目录，(3)软件包目录。但是，其优先级依次降低，即后面目录中的配置文件中指定的配置选项会覆盖掉前面的。

在 `Unix` 和 `Mac OS X` 系统下，配置文件顺序是：

 目录  | 位置
-------|-------
系统目录 | prefix/lib/pythonver/distutils/distutils.cfg
用户主目录 | $HOME/.pydistutils.cfg
本地目录（即软件包根目录） | setup.cfg

在 `Windows` 系统下，配置文件顺序是：

 目录  | 位置
-------|-------
系统目录 | prefix\Lib\distutils\distutils.cfg
用户主目录 | %HOME%\pydistutils.cfg
本地目录（即软件包根目录） | setup.cfg

### 其它

#### `trusted-host`
如果 `pip` 提示指定的源不是一个 `trusted` 或 `secure` 的主机，可以使用使用 `trusted-host` 选项来信任该主机源。

方法有两种：
1. 在 `pip` 命令行添加 `--trusted-host pypi.douban.com`。如：
	```shell
	$ pip install --trusted-host pypi.douban.com PACKAGE_NAME
	```
2. 在 `pip.conf` 文件中 `[install]` 节添加 `trusted-host` 选项。如：
	```ini
	[global]
	index-url = http://pypi.douban.com/simple

	[install]
	trusted-host = pypi.douban.com
	```

-----

From: http://everet.org/python-pypi-source.html

