
第一部分 词法预览
==============

## 1 控制字符
```shell
||  &  &&  ;  ;;  ( )  |  |&  <newline>
```

## 2 元字符
元字符在没有引用时具有特殊含义
```shell
|   &  ;   (   )   <   >    space    tab
```

## 3 保留字
```shell
! case do done elif esac fi for function if in select then until while {  } time [[  ]]
```
注：保留字除其特有含义之外，不能另作他用。

## 4 注释

Shell中的注释以`#`开头，在`#`之后同行上的所有字符序列都将被shell忽略。

`#`能在非交互式shell（如脚本）中正常使用，没有什么限制；但在交互式shell中有限制。要在交互式shell中使用`#`进行注释，必须启用`interactive_comments`选项；若没有启动该选项，交互式shell不允许进行注释。在交互式shell中，`interactive_comments`选项默认被启用。
