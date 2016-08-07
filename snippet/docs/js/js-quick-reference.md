JavaScript快速参考
=================

## 内置类型和字面量
类型     |   示例
---------|------------
Number   | 0、52、0.15、3e10、-3.12e-2
String   | "Hello"、'hello'(均可使用转义序列)；常用转义序列：`\r`、`\n`、`\t`、`\"`、`\'`、`\uXXXX(十六进制)`、`\0ooo(八进制)`
Boolean  | `true`、`false`
Array    | []、[1, 2, 3]、[[[3], 2], 1]等
Date     | `new Date(...)`(无字面表示法)
RegexExp | `/pattern/flags`(详见下文)
Function | `function(...){...}`(详见下文)
Object   | `{prop: value, prop2: value2... }`

`typeof 表达式` → 小写的类型名称

将 `0`、`''(空字符串)`、`null` 和 `undefined` 转换为 `布尔类型` 时会得到 `false`，转换其他值均会得到 `true`。

## 正则表达式回顾
类别               |         说明
-------------------|---------------------
类别(匹配字符的集合) | `.`、`\d`、`\D`、`\w`、`\W`、`\s`、`\S`、`[...]`、`[^...]`(必须以字面连字号结尾)
边界               | `\A`、`\Z`、`^`、`$`、`\b`、`\B`
贪婪匹配符(最大匹配) | `*`、`(0+)`、`?`、`(0-1)`、`+`、`(1+)`、`{min,}`、`{,max}`、`{min,max}`
懒惰匹配符(最小匹配) | `*?`、`??`、`+?`
分组               | `(...)` 捕获分组(可作为后向引用)、`(?:...)`不捕获分组(速度更快)
前向匹配            | `(?=...)` 要求字符串前的内容被匹配、`(?!...)`需要字符串前的内容不被匹配
后向引用            | `\1...\9`(代表组的序号)、`\&`(整个匹配串)
或                 | `|`(如果在一个组中出现,则仅作用于此组内的内容)

## 标识位
标识 | 说明
----|------
`g` | 全局匹配：匹配所有的目标字符串，而非第一次出现
`i` | 大小写敏感(对 Unicode 也适用)
`m` | 多行匹配：点字符(`.`)可匹配任意字符，包括换行符

- 多次编译同一个正则表达式会造成性能损耗，尽量对其进行预编译。
- 如果只想检查是否存在匹配而不关心其他细节(例如组)的话，使用 `regex.test(str)` 而不是 `str.match(regex)`。
- 如果不需要捕获组的内容作为后向引用，而仅仅是在组上应用一个限定符，请把这个组标记为非捕获型：`(?:...)`。

## 函数
### 声明
```js
function fnName(...) {
    // Statements
}
```

### 表达式
```js
function (...) {...}
```
声明被 **`提升`** 到它们的作用域中：作用域中的每一个函数都可以调用其他函数，而不受它们的声明顺序影响(这里并不需要 `原型声明`)。

### `return x;`
退出函数并返回 x。

### `return;`
退出函数返回 `undefined`。 函数本身也是一种对象，所以函数拥有自己的方法(比如 `apply` 和 `call`)，也可以按引用被传递(但这样你就会丢失它们的绑定关系：`this` 关键字原有的含义)。这意味着你可以对函数赋值，或者将函数作为参数来传递。

函数的参数列表中并不限定参数类型，参数名起到的更多是提示作用。JavaScript 会把实参赋到对应的形参上。需要注意的是，所有的 JavaScript 参数都像 varargs 一样：你可以传递任意数量的参数，并通过内置的参数变量表，以访问数组的形式访问它们。

## 特殊值
保留字           |     说明
----------------|-----------------
`undefined`     | 未被赋值的变量，未匹配实参的形参。
`null`          | 没有被明确的定义；一般是 DOM 调用 `无结果` 的返回值，一般在程序中被作为 `空值` 赋给某个变量。
`false`、`true` | 两个布尔值字面量。
`Infinity`      | 无限的数值(可以带有正负号，比如 `-Infinity`)。
`NaN`           | 非数值(Not-a-Number)表达式的返回值，比如说失败的数值解析。它与任何数值不等，包括它自己，所以一般通过 `isNaN(n)` 来判断变量是否为 `NaN`。

## 操作符
### 算术操作符 `+` `-` `*` `/` `%` `++` `--`
注意：JavaScript 中没有 `int` 或是 `float` 类型，只有 `Number` 类型。

- `%` 和 `=` 分别为 `求模` 和 `取余`。负号(一元操作符)会改变数值符号：-42。
- `++` 和 `--` 分别为 `自增` 和 `自减`。优先使用前置符(`++x`)，除非有明确的原因要使用后置符(`x++`)。

### 比较操作符 `==` `===` `<` `>` `<=` `>=` `!=`
- `==` 仅对值进行比较，并使用一套“转换协议”，所以会有 `5=="5"`、`0==false`、`null == undefined` 等。
- `===` 进行严格的比较，既对值作比较，也对类型作比较。`undefined === x` 非常适合严格的测试。
- `!=` 不等号。

### 布尔逻辑操作符 `&&(逻辑与)` `||(逻辑或)`
- `&&` 比 `||` 的优先级高。
- 如果 a 为真，`a || b` 会把 b 短路(即不去求值)。
- 如果 a 为假，`a && b` 会把 b 短路。

### 算术操作简写符 `+=` `-=` `*=` `/=` `%=`
`a += b` 等价于 `a = a + b`，其余类似。这样的写法更简洁。

### 成员选择符 `[...]`
- 数组通过下标来选择元素：`array[5]`(0作为起始下标)。
- 动态成员选择:
    - `obj['propName']` 等价于 `obj.propName`。
    - `obj['methodName'](...)` 等价于 `obj.methodName(...)`。例如：`node[visible? 'show' : 'hide']()`。

### 优先级
和 `C/C++/Java/Ruby` 中的操作符优先级类似。

- `* / %` 优先级高于 `+ -`。
- `&&` 优先级高于 `||`。
- `(...)` 强制改变优先级。
- `(5 * 3) + (6 / 2)` 等价于 `5 * 3 + 6 / 2`。
- `(a && b) || (c && d)` 等价于 `a && b || c && d`。

### 位操作符 `&` `|` `^` `<<` `>>` `>>>`
- `^` 是异或操作符。
- `<<` 和 `>>` 为右移位和左移位操作符。
- `>>>` 为无符号右移操作符。

### 变量和作用域
```js
var x, y=42, z, t=y*2;
```
局部变量必须通过 `var` 关键字声明。

**尽可能不要使用全局变量。**

变量可以在声明时被赋值，它们可以在其被声明的区域内被访问(大多数情况下是当前函数体)。

如果你的代码需要隐藏一些标识符(变量或者是函数)，请使用`模块模式`。
```js
(function(){
    // 这里的内容不会被外界所访问到
    // 除非你返回里面的成员或直接对里面的成员赋值
})();
```
注：如果是在 ES6 中，可以 `let` 关键字声明变量，这样的变量被限制在其声明所在的作用域中。

## 分支判断语句
```js
if (condition) {
    // Statements
}

if (condA) {
    // codeA
} else if (condB) {
    // codeB
} else {
    // codeC
}

switch(expr) {
    case valueA:
        // codeA
        break;
    case valB1:
    case valB2:
        // codeB
        break;
    default:
        // codeC
}
```
提示：尽早返回值，以免陷入到层层嵌套的 `else` 代码块中，同时请保持代码的缩进正常，以便阅读。

## 应该了解的数组知识
```js
var arr=[2, 3, 4, 5, 6];

arr.length                 // => 5
arr.concat([7, 8, 9])      // => [2..9]
arr                        // => [2..9]
arr.push(10)               // => [2..10]
arr.unshift(1)             // => [1..10]
arr.pop()                  // => 10
arr.shift()                // => 1
arr                        // => [2..9]
arr.slice(4, -2)           // => [6, 7, 8]
arr.join('')               // => '23456789'

arr.sort(function(a, b){
    return b - a;
})  // => [9, 8, 7, 6, 5, 4, 3, 2]

arr.sort()                 // => [2, 3, 4, 5, 6, 7, 8, 9]
arr.splice(5)              // => [7, 8, 9]
arr                        // => [2, 3, 4, 5, 6]
```

## 异常及错误处理
```js
try{
    // 可能发生异常的代码
} catch(e) {                           // e 引用了 error对象
    // 这段代码只在异常产生时执行
} finally {
    // 无论是否有异常产生，这段代码都会执行
}
```
你可以通过 `raise exceptionObject` 来抛出自定义的异常(可以是任何类型的对象)。

## 数学函数
全局的 `Math` 对象中包含了各种常用的操作以及一些有用的常量，举例如下。

- 幂相关：`E` `LN2` `LN10` `LOG2E` `LOG10E` `SQRT1_2` `SQRT2` `exp` `log` `pow` `sqrt`
- 三角：`PI` `acos` `asin` `atan` `atan2` `cos` `sin` `tan`
- 取整及其他：`abs` `ceil` `floor` `max` `min` `random` `round`

## 异步代码：使用 `timeout`
```js
var timer;

function callback(){
    timer && window.clearTimeout(timer);
    timer = null;
    // 回调代码;
}

window.setTimeout(callback, 100);  // 0.1秒
```

## 可怜人的调试器
全局的 `window` 对象含有 `alert(...)` 方法，调用它可以弹出一个对话框。如果可能的话(使用 Safari、装有 Firebug 的 Firefox 以及 Opera、IE8+)，使用控制台机制来获得更轻松的调试体验。

Firebug 的 `console` 对象在 `console.log` 的基础上增加了大量的内容。为了获得更多信息,请登录 http://getfirebug.com/logging。

## 循环
```js
for(decl; test; incr){
    代码;
}

while(条件) {
    可能永远不会执行的代码;
}

do {
    至少会执行一次的代码;
}while(条件);


while(true) {
    至少会执行一次的代码;
    if (跳过接下来的内容)
        continue;
    if (停止当前循环)
        break;
    其余的代码;
}

// 快速数组循环
for(var i=0, l=arr.length; i<l; ++i)
    代码;
```

## 非常有用的字符串操作
这里并没有提到 `length` 属性(返回包含的字符个数，而非字节的个数)。
```js
'yay'.charAt(1)
'hello'.indexOf('l')
'hello'.indexOf('l', 3)
'hello'.lastIndexOf('l')
'hello'.lastIndexOf('l', 2)
'hello'.replace('l', 'L')
'hello'.replace(/[aeiouy]/g,'-')
'hello'.replace(/(.)\1/g, function(s){
return s.toUpperCase();
 })  // => 'heLLo'

'a b c'.split(' ')          // => ['a',
'a b \nc'.split(/\s+/)      // => ['a',
'abc'.split('')             // => ['a',
'a b c'.split(' ', 2)       // => ['a',
'hello'.substring(2)        // => 'llo'
'hello'.substring(2, 4)     // => 'll'(指定了子串结束位置)
'hello'.slice(-3)           // => 'llo'(从倒数第3个字符开始)
'hello'.slice(-3, -1)       // => 'll'(指定了结束位置,到倒数第2个字符)
'ÉlodiE'.toLowerCase()      // => 'élodie'
'déjà ça'.toUpperCase()     // => 'DÉJÀ ÇA'
'hello'.match(/(.)\1/)      // ['ll', 'l'] †
```

下标0处为完整匹配,下标1处为组1捕获的内容,依此类推。

## 一些全局的好东西
```js
var x = 4;
eval('x * Math.sqrt(16)')           // => 20 - 请小心使用!
decodeURIComponent('%C3%89lodie')   // => 'Élodie'
encodeURIComponent('S & H')         // => 'S%20%26%20H'
parseInt('010')                     // => 8 †
parseInt('08')                      // => NaN †
parseInt('010', 10)                 // => 10 ††
parseFloat('314.15e-2')             // => 3.1415
isNaN(parseInt('foobar'))           // => true
Math.PI.toFixed(3)                  // => 3.142
(5.31762).toFixed(3)                // => 5.318
Math.PI.toPrecision(3)              // => 3.14
```

- 如果没有显式声明基数，`parseInt` 会自动作出判断。前缀为 `0` 代表八进制。
- 如果显式声明基数的话，就不会出现混乱了。推荐使用这种形式调用 `parseInt`。

## 标识符和保留字
标识符的起始字符必须是 `$`、`_` 或者`Unicode字符`(即使是这样，你仍应避免在标识符中包含怪异的字符)，接下来的字符可以是 `任意Unicode字符`。

JavaScript 现在的保留字不超过 `56` 个，而且它们中的大多数并不是当前版本 JavaScript 中真正的关键字。
```js
abstract
boolean break byte
case catch char class const continue
debugger default delete do double
else enum export extends
final finally float for function
goto
if implements import in instanceof int interface
long
native new
package private protected public
return
short static super switch synchronized
this throw throws transient try typeof
var void volatile
while with
```

------

From: 《Pragmatic Guide to JavaScript》（中文版《JavaScript修炼之道》）附录A《JavaScript快速参考》
