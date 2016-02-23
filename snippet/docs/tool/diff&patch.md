
diff 和 patch
============

    本文由xgfone根据diff和patch的man手册以及其他的网络资源整理而成。

`diff`和`patch`是一对工具，在数学上来说，`diff是对两个集合的差运算`，`patch是对两个集合的和运算`。diff比较两个文件或文件集合的差异，并记录下来，生成一个diff文件，这也是我们常说的patch文件，即补丁文件。patch能将diff文件运用于原来的两个集合之一，从而得到另一个集合。举个例子来说文件A和文件B,经过diff之后生成了补丁文件C,那么着个过程相当于`A-B=C`，那么patch的过程就是`B+C=A`或`A-C=B`。因此我们只要能得到A, B, C三个文件中的任何两个，就能用diff和patch这对工具生成另外一个文件。

## 一、diff的用法
diff工具是Unix及其Unix-like下的标准配置工具，也是POSIX标准中的一员。

diff后面可以接两个文件名或两个目录名。 如果是一个目录名加一个文件名，那么只作用在那么个目录下的同名文件。如果是两个目录的话，作用于该目录下的所有文件，不递归。如果我们希望递归执行，需要使用-r参数。

命令“`diff  A  B > C`”,一般A是原始文件，B是修改后的文件，C称为A的补丁文件。不加任何参数生成的diff文件格式是一种简单的格式，这种格式只标出了不一样的行数和内容。我们需要一种更详细的格式，可以标识出不同之处的上下文环境，这样更有利于提高patch命令的识别能力。这个时候可以用`-c`开关。

### diff详解
#### 语法格式
```shell
diff [option] from-file to-file
```

#### 用途
    逐行比较两个文件或逐文件比较两个目录，并把其差异输出到标准输出。

#### 常用选项
    -c                 显示相异处的前后部分内容，并标出不同之处。
    -p                 若比较的文件是C语言文件，则列出差异所在的函数。
    -r                 递归地比较目录下的所有文件。
    -u                 以统一格式输出其差异（默认是3行，但是可以通过“-u  NUM”或"--unified[=NUM]” 来改变）。
    -i, --ignore-case  忽略大小写的差异（即大小写视为相同）。
    -a, --text         把所有文件都当作文件文件来看待（即可以包含二进制文件）。
    -x  FILE/DIR       不比较指定的名为FILE的目录或名为DIR的目录。
    -X file            把file中列出的文件和目录都忽略掉，不进行diff。在file中，每行一个文件和目录。
    -N, --new-file     把不存在的文件作为一个空文件，把不存在的目录作为一个空目录。

注：如果不指定文件名/目录名，或指定为“-”，则从标准输入读取内容。


## 二、patch的用法

补丁Patch是天才程序员、Perl的发明者Larry Wall发明的，它应高效地交流程序源代码之需求而生，随着以Linux为代表的开发源代码运行的蓬勃发展，patch这个概念已经成为开放源代码发起 者、贡献者和参与者的集体无意识的一部分。patch只包含了对源代码修改的部分，这对于开放源代码社区的协同开发模式具有重要意义，意味的软件新版本的 发布和对软件的缺陷或改进可以以更小的文件发布，可以减少网络的传输量，方便软件维护者的管理工作。

patch文件有多种格式，不同平台上所支持的格式不尽相同，但最常见的是**`context格式`**和**`unified格式`**。context格式被广泛使用，是 patch文件格式事实上的标准。该格式包含了差异部分及其邻近的若干行，邻近就是所谓的上下文，这些行虽然没有变化，但它们出现在patch文件使得还原patch的程序具备更强的容错性。**_unified格式常见于GNU的patch实现，以patch形式发布的linux内核就使用了该格式_**。此外，还有其它比较少用的格式，如**`Normal格式`**、**`并排对比模式(side-by-side)`**、**`ed script`**和**`RCS script模式`**等。除了并排对比模式方便用户观察文件差异，其它格式大多数是为了兼容旧的patch格式。

#### patch的用途
    根据原文件（即旧文件）和补丁文件（即存储新文件相对于旧文件的差异的文件）生成目标文件（即新文件）。

#### patch命令的用法
    “patch A C”就能得到B, 这一步叫做对A打上了B的名为C的补丁；之后，文件A就变成了文件B。
    如果打完补丁之后想再恢复到A，则可以使用命令“patch -R B C”。

所以不用担心会失去A的问题。

其实patch在具体使用的时候是不用指定原文件的，因为补丁文件中都已经记载了原文件的路径和名称。patch足够聪明可以认出来。但是有时候会有点小问 题。比如一般对两个目录diff的时候可能已经包含了原目录的名字，但是我们打补丁的时候会进入到目录中再使用patch,这个时候就需要你告诉 patch命令怎么处理补丁文件中的路径。可以利用-pN开关，告诉patch命令忽略的路径分隔符的个数。

A文件在 DIR_A下，修改后的B文件在DIR_B下，一般DIR_A和DIR_B在同一级目录。我们为了对整个目录下的所有文件一次性diff,我们一般会到DIR_A和DIR_B的父目录下执行以下命令“`diff -rc  DIR_A  DIR_B > C`”；这时，补丁文件C中会记录原始文件的路径为DIR_A/A。现
在另一个用户得到了A文件和C文件，其中A文件所在的目录也是DIR_A。一般，他会比较喜欢在DIR_A目录下面进行patch操作，它会执行“`patch < C`”。但是，这个时候patch分析C文件中的记录，认为原始文件是“`./DIR_A/A`”，但实际上是“`./A`”，此时patch会找不到原始文件。为了避免这种情况我们可以使用-p1参数，如下“`patch  -p1 < C`”。此时，patch会忽略掉第1个”/”之前的内容，认为原始文件是“`./A`”，这样就正确了。

使用patch有很多选项，但一般只要两个选项就能满足我们的需求：
```
patch -p1    < [patchfile]
patch -p1 -R < [patchfile]
```
其中，-p1选项代表patchfile中文件名左边目录的层数，顶层目录在不同的机器上有所不同。要使用这个选项，就要把你的patch放在要被打补丁的目录下，然后在这个目录中运行：`path -p1 < [patchfile]`。

#### patch详解
##### 语法格式
```
patch [option] [originalfile] [patchfile]
```
但通常仅使用
```
patch -pN < patchfile
```

##### 用途
    给原文件打上补丁，使之成为新文件

##### 常用选项

    -d  DIR                  在进行任何操作前先切换到目录DIR中
    -E, --remove-empty-file  移除空文件/空目录（与diff中的-N选项对应）
    -R, --reverse            变换新旧文件（即把新文件还原成旧文件）
    -pN, --strip=N           N为数字，代表补丁文件名左边目录的层数（即“/”的个数）。该选项表示把补丁文件名中前N层目录去掉。
    -I  patchfile, --input=patchfile  指定补丁文件的位置，如果patchfile为“-”，则从标准输入读取。这是默认选项。


## 三、diff和patch的常用用法总结
### 1、对单个文件
```
diff -uN from-file to-file > to-file.patch
```
生成to-file相对于from-file的补丁文件to-file.patch

```
patch -p0 < to-file.patch
```
给from-file打上补丁（to-file.patch），使from-file变成to-file

```
patch -p0 -PE < to-file.patch
```
给to-file打上补丁（to-file.patch），使to-file还原成from-file

### 2、对多个文件（即文件夹）
```
diff  -urN from-docu to-docu > to-docu.patch
patch -p1     < to-docu.patch
patch -p1 -PE < to-docu.patch
```
注：from-file与to-file的顺序不能变（在diff命令中，from-file在前，to-file在后），它们的顺序记录在to-file.patch文件中。


## 四、把diff和patch应用于Linux内核补丁

### 1、创建一个Linux内核补丁
假设当前目录为/src/linux/，且目录结构为：

    /src/linux/
        linux-2.6.12
        linux-2.6.12.2

```
diff -uprN -X linux-2.6.12.2/Documentation/dontdiff linux-2.6.12 linux-2.6.12.2 > patch-2.6.12.2
```
其中

   -u       以统一格式输出其差异；
   -p       比较的若是C语言文件，则列出差异所在的函数；
   -r       递归地比较目录下的所有文件；
   -N       把不存在的文件作为一个空文件，把不存在的目录作为一个空目录；
   -X file  把file中列出的文件和目录都忽略掉，不进行diff。在file中，每行一个文件和目录。

### 2、给Linux内核打补丁
假设当前目录为/src/linux/，且目录结构为：

    /src/linux/
        linux-2.6.12
        patch-2.6.12.2

首先切换到linux-2.6.12目录中：
```
$ cd linux-2.6.12
```
然后再给Linux内核打补丁：
```
$ patch -p1 < ../patch-2.6.12.2
```
此时，Linux内核的版本为`2.6.12.2`。

### 3、还原Linux内核版本
假设当前目录为/src/linux/，且目录结构为：

    /src/linux/
        linux-2.6.12.2
        patch-2.6.12.2

先切换到linux-2.6.12.2目录中：
```
$ cd linux-2.6.12.2
```
然后再给Linux内核打补丁：
```
$ patch -p1 -R < ../patch-2.6.12.2
```
此时，Linux内核的版本为`2.6.12`。

注：版本形如`2.6.XX.YY`的Linux内核补丁都是基于`2.6.XX`版本的Linux内核，并不是基于`2.6.XX.ZZ`版本的Linux内核，所以想要把Linux内核从`2.6.XX.ZZ`版本更改到`2.6.XX.YY`版本（如果YY大于ZZ，则为升级；否则，则为绛级），则须要先用`2.6.XX.ZZ`版本的补丁把当前的版本（即`2.6.XX.ZZ`）还原到`2.6.XX`版本，然后再用`2.6.XX.YY`版本的补丁把上一步还原成的`2.6.XX`版本升级到`2.6.XX.YY`版本；而不能直接从`2.6.XX.ZZ`版本更改到`2.6.XX.YY`版本。上述步骤总结为：`2.6.XX.ZZ  ====>  2.6.XX  ====>  2.6.XX.YY`。
