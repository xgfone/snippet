
# 目录

1. 简介
2. 功 能
	1. 全局命令
	2. 书签
		- 1.书签表
		- 2.书签命令
		- 3.无效书签
	3. Nerdtree 映射
	4. 文件系统菜单
3. 选项
  1. 选项总结
  2. 选项明细


## 1.简介
Nerd tree可以让你浏览文件系统并打开文件或目录。
你可以通过键盘或鼠标控制它以树状图显示文件系统，也可以在其中进行一些简单的文件系统操作。

nerdtree 提供如下功能及特性：
- 以继承树的形式显示文件和目录
- 对如下类型的文件进行不同的高亮显示
	- 文件
	- 目录
	- sym-links
	- 快捷方式
	- 只读文件
	- 可执行文件
- 提供许多映射来控制树状结构
	- 对展开/收拢/浏览目录结点的映射
	- 对在新的或已存在的窗口或Tab页中打开文件的映射
	- 对改变根结点的映射
	- Mappings to navigate around the tree
- 可以将文件和目录添加到收藏夹
- 可以用鼠标进行大部分的树状结构导航
- 对树状结构内容的过滤（可在运行时切换）
	- 自定义文件过 滤器可以阻止某些文件（比如vim备份文件等）的显示
	- 可选是否显示隐藏文 件
	- 可选不显示文件只显示目录
- 提供文本文件系统菜单来创建/删除/移动/复制目录或文件
- 可以自定义Nerd窗口的位置和大小
- 可以自定义结点排序方式
- 当你浏览文件系统的时候就会有一 个文件系统的模型被创建或维护。这样做有几个优点：
	- 所有文件系统信息都被 缓存了，有需要的时候只要重新读入缓存
	- 如果重新浏览之后访问过的 tree 的一部分，结点就会以上次保持的展开或合拢的样子显示
- 该脚本能记住光标位置和窗口位置，所以可以用 `NERDTreeToggle` 来切换tree的显示与隐藏
- 对于多Tab，可以共享一个Tree，也可以各自拥有各自的tree，还可以混合以上两种方式
- 默认情况下，该脚本覆盖vim的默认文件浏览器(netrw)，所以如果直接输入:edit命令也会用nerd树打开



## 2 功能
### 2.1 全局命令
          Command         |         Description
--------------------------|---------------------------------------------------
  **`:NERDTree [ | ]`**   | 打开一个Nerdtree，根结点由参数指定，不指定参数就是以当前目录为根结点
  **`:NERDTreeFromBookmark`**   | 打开一个Nerdtree，根结点由参数所指定的书签
  **`:NERDTreeToggle [ | ]`**   | 在当前Tab中如果Nerdtree已经存在，就切换显示与隐藏；如果不存在，就相当于执行:NERDTree命令
  **`:NERDTreeMirror`**         | 从另一个Tab中共享一个NerdTree过来（在当前Tab的Tree所作的改变也反应到原Tab中）。如果总共只有一个Tree，就直接共享；如果不止一个，就会询问共享哪个
  **`:NERDTreeClose`**          | 在当前Tab中关闭Tree

### 2.2 书签
在NerdTree中，书签用于标记某个感兴趣的文件或目录，比如可以用书签标记所有 Project目录

#### 2.2.1 书签表
如果书签被激活，则显示于树状图的上方。

可以双击或用 **`NERDTree-o`** 来激活选中文件。

可以用 **`NERDTree-t`** 映射使选中文件用新Tab打开，并跳到新tab页

可以用 **`NERDTree-T`** 映射使选中文件用新Tab打开，但不跳到新Tab页

#### 2.2.2 书签命令
以下命令只在在 Nerdtree 的 buffer 中有效

       Bookmark     | Description
--------------------|---------------------------------------------------
  **`:Bookmark`**          | 将选中结点添加到书签列表中，并命名为name（书签名不可包含空格）；如与现有书签重名，则覆盖现有书签。
  **`:BookmarkToRoot`**    | 以指定目录书签或文件书签的父目录作为根结点显示NerdTree
  **`:RevealBookmark`**    | 如果指定书签已经存在于当前目录树下，打开它的上层结点并选中该书签
  **`:OpenBookmark`**      | 打开指定的文件（参数必须是文件书签）。如果该文件在当前的目录树下，则打开它的上层结点并选中该书签
  **`:ClearBookmarks`** [] | 清除指定书签；如未指定参数，则清除所有书签
  **`:ClearAllBookmarks`** | 清除所有书签

##### :ReadBookmarks
	重新读入'NERDTreeBookmarksFile'中的所有书签

#### 2.2.3 无效书签
如果监测到无效书签，脚本就会发布一个错误消息并将无效书签置为不可用；
无效书签将被移到书签文件的最后，在有效书签和无效书签之间有一个空行。

书签文件中的每一行代表一个书签。

如果修正了某个无效书签，则可以重启vim或使用 `:ReadBookmarks` 命令重新读入书签信息

### 2.3 Nerdtree 映射
     Key    |             Description                           |   Section
------------|---------------------------------------------------|------------------
  **`o`**   | 在已有窗口中打开文件、目录或书签，并跳到该窗口    | `|NERDTree-o|`
  **`go`**  | 在已有窗口 中打开文件、目录或书签，但不跳到该窗口 | `|NERDTree-go|`
  **`t`**   | 在新Tab中打开选中文件/书签，并跳到新Tab           | `|NERDTree-t|`
  **`T`**   | 在新Tab中打开选中文件/书签，但不跳到新Tab         | `|NERDTree-T|`
  **`i`**   | split 一个新窗口打开选中文件，并跳到该窗口        | `|NERDTree-i|`
  **`gi`**  | split一个新窗口打开选中文件，但不跳到该窗口       | `|NERDTree-gi|`
  **`s`**   | vsp一个新窗口打开选中文件，并跳到该窗口           | `|NERDTree-s|`
  **`gs`**  | vsp一个新 窗口打开选中文件，但不跳到该窗口        | `|NERDTree-gs|`
  **`!`**   | 执行当前文件                                      | `|NERDTree-!|`
  **`O`**   | 递归打开选中 结点下的所有目录                     | `|NERDTree-O|`
  **`x`**   | 合拢选中结点的父目录                              | `|NERDTree-x|`
  **`X`**   | 递归 合拢选中结点下的所有目录                     | `|NERDTree-X|`
  **`e`**   | Edit the current dif                              | `|NERDTree-e|`
  **`双击`**| 相当于NERDTree-o   |
  **`中键`**| 对文件相当于NERDTree-i，对目录相当于NERDTree-e  |
  **`D`**   | 删除当前书签  |
  **`P`**   | 跳到根结点    |
  **`p`**   | 跳到父结点    |
  **`K`**   | 跳到当前目录下同级的第一个结点    |
  **`J`**   | 跳到当前目录下同级的最后一个结点  |
  **``**   | 跳到当前目录下同级的前一个结点    |
  **``**   | 跳到当前目录下同级的后一个结点    |
  **`C`**   | 将选中目录或选中文件的父目录设为根结点             |
  **`u`**   | 将当前根结点的父目录设为根目录，并变成合拢原根结点 |
  **`U`**   | 将当前根结点的父目录设为根目录，但保持展开原根结点 |
  **`r`**   | 递归刷新选中目录       |
  **`R`**   | 递归刷新根结点         |
  **`m`**   | 显示文件系统菜单       |
  **`cd`**  | 将CWD设为选中目录      |
  **`I`**   | 切换是否显示隐藏文件   |
  **`f`**   | 切换是否使用文件过滤器 |
  **`F`**   | 切换是否显示文件       |
  **`B`**   | 切换是否显示书签       |
  **`q`**   | 关闭NerdTree窗口       |
  **`?`**   | 切换是否显示Quick Help |


### 2.4 文件系统菜单
帮助说中包含 **`新建`**、**`复制`**、**`移动`**、**`删除`** 四种命令，但 copy 只支持 *nix 系统

## 3 自定义选项
     Options                |    Description
----------------------------|--------------------------------------------------------
loaded_nerd_tree            | 不使用NerdTree脚本
NERDChristmasTree           | 让Tree把自己给装饰得多姿多彩漂亮点
NERDTreeAutoCenter          | 控制当光标移动超过一定距离时，是否自动将焦点调整到屏中心
NERDTreeAutoCenterThreshold | 与NERDTreeAutoCenter配合使用
NERDTreeCaseSensitiveSort   | 排序时是否大小写敏感
NERDTreeChDirMode           | 确定是否改变Vim的CWD
NERDTreeHighlightCursorline | 是否高亮显示光标所在行
NERDTreeHijackNetrw         | 是否使用:edit命令时打开第二NerdTree
NERDTreeIgnore              | 默认的“无视”文件
NERDTreeBookmarksFile       | 指定书签文件
NERDTreeMouseMode           | 指定鼠标模式（1.双击打开；2.单目录双文件；3.单击打开）
NERDTreeQuitOnOpen          | 打开文件后是否关闭NerdTree窗口
NERDTreeShowBookmarks       | 是否默认显示书签列表
NERDTreeShowFiles           | 是否默认显示文件
NERDTreeShowHidden          | 是否默认显示隐藏文件
NERDTreeShowLineNumbers     | 是否默认显示行号
NERDTreeSortOrder           | 排序规则
NERDTreeStatusline          | 窗口状态栏
NERDTreeWinPos              | 窗口位置（'left' or 'right'）
NERDTreeWinSize             | 窗口宽

## 我的配置
```vim
"NERD Tree
let NERDChristmasTree=1
let NERDTreeAutoCenter=1
let NERDTreeBookmarksFile=$VIM.'\Data\NerdBookmarks.txt'
let NERDTreeMouseMode=2
let NERDTreeShowBookmarks=1
let NERDTreeShowFiles=1
let NERDTreeShowHidden=1
let NERDTreeShowLineNumbers=1
let NERDTreeWinPos='left'
let NERDTreeWinSize=31
nnoremap f :NERDTreeToggle
```

------

From: http://www.cnblogs.com/mo-beifeng/archive/2011/09/08/2171018.html
