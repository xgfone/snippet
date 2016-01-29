
VIM脚本语法
=========

教材推荐《[Learn Vimscript the Hard Way](http://learnvimscriptthehardway.stevelosh.com/)》

 本节原始选自《[VIM脚本学习](http://www.cnblogs.com/maxupeng/archive/2011/10/19/2217353.html)》，但经过笔者（xgfone）更改。

## 1、选项（option）

对于某个选项，比如number
```vim
set number      " 打开选项
set nonumber    " 关闭选项
set number!     " 切换选项，number -> nonumber，nonumber -> number
set number?     " 查看选项是否被设置，number打开时显示number, 关闭时显示nonumber
```

## 2、数值类型

### 2.1 整数
    十进制：   100
    十六进制： 0xff
    八进制：   070

### 2.2 浮点数
    100.1　　5.43e3　　5.43e+3　　5.43e-3

### 2.3 运算
    2 * 2.0，  结果 4.0
    3 / 2，    结果 1
    3 / 2.0，  结果 1.5
    5 % 2，    结果 1


## 3、字符串类型

### 3.1 合并
```vim
"Hello, " . "world"　　" 结果"Hello, world"
```

### 3.2 转义
```vim
"\nabc\\"             " 双引号进行转义
```

### 3.3 字面字符串
```vim
'\n\\'　　             " 单引号不进行转义
```

### 3.4 字符串函数

    长度      strlen
    切割      split　　split("one two three")　　    split("one,two,three",",")　　
    合并      join　　 joint(["one","two"],"...")　　结果"one...two"
    大小写     tolower/toupper


## 4、变量（variable）
```vim
let foo="bar"                   " 创建变量foo并将字符串bar赋值给变量foo
echo &number                    " 可以通过&符号获取选项的值，布尔值用0（false）和1（true）表示
let &textwidth=&textwidth+10    " 通过&给选项赋值
echo @                          " 显示寄存器（register）a的内容
let @a="hello"                  " 设置寄存器a的内容
echo  $EDITOR                   " 访问环境变量
```


## 5、变量作用域

    b:a  表示变量a的作用域在当前的buffer

type                |  symbol |   description
--------------------|---------|---------------------------
\|buffer-variable\|   |　  b:   | Local to the current buffer.
\|window-variable\|   | 　 w:   | Local to the current window.
\|tabpage-variable\|  | 　 t:   | Local to the current tab page.
\|global-variable\|   |    g:   | Global.
\|local-variable\|    |    l:   | Local to a function.
\|script-variable\|   |    s:   | Local to a |:source|'ed Vim script.
\|function-argument\| |    a:   | Function argument (only inside a function).
\|vim-variable\|      |    v:   | Global, predefined by Vim.


## 6、条件语句
```
if 条件1
    语句1
elseif 条件2
　　 语句2
else
　　 语句3
endif
```


## 7、while循环
```
while 表达式
    语句
endwhile
```


## 8、比较操作符

                         |  use 'ignorecase' |  match case  |  ignore case ~
-------------------------|-------------------|--------------|---------------------
equal                    |       ==          |      ==#     |    ==?
not equal                |       !=          |      !=#     |    !=?
greater than             |       >           |      >#      |    >?
greater than or equal    |       >=          |      >=#     |    >=?
smaller than             |       <           |      <#      |     <?
smaller than or equal    |       <=          |      <=#     |     <=?
regexp matches           |       =~          |      =~#     |     =~?
regexp doesn't match     |       !~          |      !~#     |     !~?
same instance            |       is          |              |
different instance       |       isnot       |              |

注：其它操作符：`与（&&）`、`或（||）`、`非（!）`、`字符串连接（.）`等。


## 9、函数

**`函数的首字母必须大写`**
```vim
function Xxx()
　　 函数体
endfunction
```

（1）单独调用函数
```vim
call Xxx()
```

（2）在表达式中调用函数
```vim
echo Xxx()
```

（3）如果函数没有return语句，函数的返回值默认为0

（4）函数参数，函数体内使用参数时，前面必须加`a:`
```vim
function Xxx(name)
　　 echom a:name
　　 a:name="xxx"　　  " 错误，不能对参数变量赋值
endfunction
```

（5）可变参数
```vim
function  Xxx(...)
　　 echom a:0　　    " a:0存放参数个数
 　　echom a:1　    　" a:1存放第一个参数，a:2存放第二个参数，以此类推
 　　echom a:000     " a:000存放参数列表
endfunction
```

（6）如果函数重复定义，则Vim将会报错，为了不让Vim报错，可以在function后添加一个叹号（!）
```vim
function! Xxx()
    函数体
endfunction
```

（7）Vimscript 中的函数声明为运行时语句，因此如果一个脚本被加载两次，那么该脚本中的任何函数声明都将被执行两次，因此将重新创建相应的函数。重新声明函数被看作一种致命的错误（这样做是为了防止发生两个不同脚本同时声明函数的冲突）。这使得很难在需要反复加载的脚本中创建函数，比如自定义的语法突出显示脚本。因此**Vimscript 提供了一个关键字修饰符（function!），允许在需要时指出某个函数声明可以被安全地重载**。

（8）要调用函数并使用它的返回值作为语言表达式的一部分，只需要命名它并附加一个使用圆括号括起的参数列表。

（9）与 C 或 Perl 不同，Vimscript 并不 允许您在未使用的情况下抛出函数的返回值。因此，**如果打算使用函数作为过程或子例程并忽略它的返回值，那么必须使用 call 命令为调用添加前缀**。

（10）可以在同一个函数中同时使用命名参数和可变参数，只需要将可变参数的省略号放在命名参数列表之后。


## 10、键映射（Key Map）
`map`、`nmap`、`vmap`、`imap`分别在`一般模式（Normal）`、`一般模式（Normal）`、`视图模式（Visual）`、`插入模式（Insert）`等下映射一组键，即`map`和`nmap`映射的按键只能在`一般模式`下使用，`vmap`映射的按键在`视图模式`下使用，`imap`映射的按键在`插入模式`下使用。如：
```vim
nmap  \  dd                  " 在一般模式下，将字符按键 \ 映射到dd命令上。
imap  <C-N>  <DOWN>          " 在插入模式下，将<Ctrl>-N组合按键映射到下方向键（<DOWN>）上。
```

除此之外，Vim还可以通过`nnoremap`在`一般模式`下映射一个键序列：
```vim
nnoremap  -d  dd
```
此时，在一般模式下，按键序列“`-d`”等同于“`dd`”。

在映射键时，可以指定一个全局的前缀`<leader>`；指定前缀的设置选项是`mapleader`，在映射时则使用`<leader>`，此时Vim会把`<leader>`替换成`mapleader`的值。如：
```vim
let  mapleader = ","
nnoremap  <leader>d  dd
```
此时，在一般模式下按键序列“`,d`”等同于“`dd`”。


## 11、函数示例
对齐赋值运算符的函数
```vim
function AlignAssignments ()
    " Patterns needed to locate assignment operators...
    let ASSIGN_OP = '[-+*/%|&]\?=\@<!=[=~]\@!'
    let ASSIGN_LINE = '^\(.\{-}\)\s*\(' . ASSIGN_OP . '\)'

    " Locate block of code to be considered (same indentation, no blanks)
    let indent_pat = '^' . matchstr(getline('.'), '^\s*') . '\S'
    let firstline = search('^\%('. indent_pat . '\)\@!','bnW') + 1
    let lastline = search('^\%('. indent_pat . '\)\@!', 'nW') - 1
    if lastline < 0
        let lastline = line('$')
    endif

    " Find the column at which the operators should be aligned...
    let max_align_col = 0
    let max_op_width = 0
    for linetext in getline(firstline, lastline)
        " Does this line have an assignment in it?
        let left_width = match(linetext, '\s*' . ASSIGN_OP)

        "If so, track the maximal assignment column and operator width...
        if left_width >= 0
            let max_align_col = max([max_align_col, left_width])
            let op_width = strlen(matchstr(linetext, ASSIGN_OP))
            let max_op_width = max([max_op_width, op_width+1])
        endif
    endfor

    "Code needed to reformat lines so as to align operators...
    let FORMATTER = '\=printf("%-*s%*s", max_align_col, submatch(1),  max_op_width, submatch(2))'

    " Reformat lines with operators aligned in the appropriate column...
    for linenum in range(firstline, lastline)
        let oldline = getline(linenum)
        let newline = substitute(oldline, ASSIGN_LINE, FORMATTER, "")
        call setline(linenum, newline)
    endfor
endfunction

nmap <silent> ;= :call AlignAssignments()<CR>
```
上述函数能把如下“`格式1`”转换成“`格式2`”：

**格式1**
```vim
let applicants_name = 'Luke'
let mothers_maiden_name = 'Amidala'
let closest_relative = 'sister'
let fathers_occupation = 'Sith'
```

**格式2**
```vim
let applicants_name     = 'Luke'
let mothers_maiden_name = 'Amidala'
let closest_relative    = 'sister'
let fathers_occupation  = 'Sith'
```
