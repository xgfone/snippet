It is copied from http://exploringjs.com/es6/ch_overviews.html.

> Copyright 2018 Dr. Axel Rauschmayer

---

# An overview of what’s new in ES6

- [1. Categories of ES6 features](#1-categories-of-es6-features)
- [2. New number and Math features](#2-new-number-and-math-features)
    - [2.1. New integer literals](#21-new-integer-literals)
    - [2.2. New `Number` properties](#22-new-number-properties)
    - [2.3. New `Math` methods](#23-new-math-methods)
- [3. New string features](#3-new-string-features)
- [4. Symbols](#4-symbols)
    - [4.1. Use case 1: unique property keys](#41-use-case-1-unique-property-keys)
    - [4.2. Use case 2: constants representing concepts](#42-use-case-2-constants-representing-concepts)
    - [4.3. Pitfall: you can’t coerce symbols to strings](#43-pitfall-you-cant-coerce-symbols-to-strings)
    - [4.4. Which operations related to property keys are aware of symbols?](#44-which-operations-related-to-property-keys-are-aware-of-symbols)
- [5. Template literals](#5-template-literals)
- [6. Variables and scoping](#6-variables-and-scoping)
    - [6.1. `let`](#61-let)
    - [6.2. `const`](#62-const)
    - [6.3. Ways of declaring variables](#63-ways-of-declaring-variables)
- [7. Destructuring](#7-destructuring)
    - [7.1. Object destructuring](#71-object-destructuring)
    - [7.2. Array destructuring](#72-array-destructuring)
    - [7.3. Where can destructuring be used?](#73-where-can-destructuring-be-used)
- [8. Parameter handling](#8-parameter-handling)
    - [8.1. Default parameter values](#81-default-parameter-values)
    - [8.2. Rest parameters](#82-rest-parameters)
    - [8.3. Named parameters via destructuring](#83-named-parameters-via-destructuring)
    - [8.4. Spread operator (`...`)](#84-spread-operator-)
- [9. Callable entities in ECMAScript 6](#9-callable-entities-in-ecmascript-6)
- [10. Arrow functions](#10-arrow-functions)
- [11. New OOP features besides classes](#11-new-oop-features-besides-classes)
    - [11.1. New object literal features](#111-new-object-literal-features)
    - [11.2. New methods in Object](#112-new-methods-in-object)
- [12. Classes](#12-classes)
- [13. Modules](#13-modules)
    - [13.1. Multiple named exports](#131-multiple-named-exports)
    - [13.2. Single default export](#132-single-default-export)
    - [13.3. Browsers: scripts versus modules](#133-browsers-scripts-versus-modules)
- [14. The `for-of` loop](#14-the-for-of-loop)
- [15. New Array features](#15-new-array-features)
- [16. Maps and Sets](#16-maps-and-sets)
    - [16.1. Maps](#161-maps)
    - [16.2. Sets](#162-sets)
    - [16.3. WeakMaps](#163-weakmaps)
- [17. Typed Arrays](#17-typed-arrays)
- [18. Iterables and iterators](#18-iterables-and-iterators)
    - [18.1. Iterable values](#181-iterable-values)
    - [18.2. Constructs supporting iteration](#182-constructs-supporting-iteration)
- [19. Generators](#19-generators)
    - [19.1. What are generators?](#191-what-are-generators)
    - [19.2. Kinds of generators](#192-kinds-of-generators)
    - [19.3. Use case: implementing iterables](#193-use-case-implementing-iterables)
    - [19.4. Use case: simpler asynchronous code](#194-use-case-simpler-asynchronous-code)
    - [19.5. Use case: receiving asynchronous data](#195-use-case-receiving-asynchronous-data)
- [20. New regular expression features](#20-new-regular-expression-features)
- [21. Promises for asynchronous programming](#21-promises-for-asynchronous-programming)
    - [21.1. Chaining `then()` calls](#211-chaining-then-calls)
    - [21.2. Executing asynchronous functions in parallel](#212-executing-asynchronous-functions-in-parallel)
    - [21.3. Glossary: Promises](#213-glossary-promises)
- [22. Metaprogramming with proxies](#22-metaprogramming-with-proxies)

## 1 Categories of ES6 features
The introduction of the ES6 specification lists all new features:

> Some of [ECMAScript 6’s] major enhancements include modules, class declarations, lexical block scoping, iterators and generators, promises for asynchronous programming, destructuring patterns, and proper tail calls. The ECMAScript library of built-ins has been expanded to support additional data abstractions including maps, sets, and arrays of binary numeric values as well as additional support for Unicode supplemental characters in strings and regular expressions. The built-ins are now extensible via subclassing.

There are three major categories of features:

- Better syntax for features that already exist (e.g. via libraries). For example:
    - [Classes](http://exploringjs.com/es6/ch_classes.html#ch_classes)
    - [Modules](http://exploringjs.com/es6/ch_modules.html#ch_modules)
- New functionality in the standard library. For example:
    - New methods for [strings](http://exploringjs.com/es6/ch_strings.html#ch_strings) and [Arrays](http://exploringjs.com/es6/ch_arrays.html#ch_arrays)
    - [Promises](http://exploringjs.com/es6/ch_promises.html#ch_promises)
    - [Maps, Sets](http://exploringjs.com/es6/ch_maps-sets.html#ch_maps-sets)
- Completely new features. For example:
    - [Generators](http://exploringjs.com/es6/ch_generators.html#ch_generators)
    - [Proxies](http://exploringjs.com/es6/ch_proxies.html#ch_proxies)
    - [WeakMaps](http://exploringjs.com/es6/ch_maps-sets.html#sec_weakmap)


## 2 New number and Math features
### 2.1 New integer literals
You can now specify integers in binary and octal notation:
```js
> 0xFF // ES5: hexadecimal
255
> 0b11 // ES6: binary
3
> 0o10 // ES6: octal
8
```

### 2.2 New `Number` properties
The global object Number gained a few new properties:

- `Number.EPSILON` for comparing floating point numbers with a tolerance for rounding errors.
- `Number.isInteger(num)` checks whether `num` is an integer (a number without a decimal fraction):
```js
> Number.isInteger(1.05)
false
> Number.isInteger(1)
true

> Number.isInteger(-3.1)
false
> Number.isInteger(-3)
true
```
- A method and constants for determining whether a JavaScript integer is _safe_ (within the signed 53 bit range in which there is no loss of precision):
    - `Number.isSafeInteger(number)`
    - `Number.MIN_SAFE_INTEGER`
    - `Number.MAX_SAFE_INTEGER`
- `Number.isNaN(num)` checks whether `num` is the value `NaN`. In contrast to the global function `isNaN()`, it doesn’t coerce its argument to a number and is therefore safer for non-numbers:
```js
> isNaN('???')
true
> Number.isNaN('???')
false
```
- Three additional methods of `Number` are mostly equivalent to the global functions with the same names: `Number.isFinite`, `Number.parseFloat`, `Number.parseInt`.

### 2.3 New `Math` methods
The global object `Math` has new methods for numerical, trigonometric and bitwise operations. Let’s look at four examples.

`Math.sign()` returns the sign of a number:
```js
> Math.sign(-8)
-1
> Math.sign(0)
0
> Math.sign(3)
1
```

`Math.trunc()` removes the decimal fraction of a number:
```js
> Math.trunc(3.1)
3
> Math.trunc(3.9)
3
> Math.trunc(-3.1)
-3
> Math.trunc(-3.9)
-3
```

`Math.log10()` computes the logarithm to base 10:
```
> Math.log10(100)
2
```

`Math.hypot()` Computes the square root of the sum of the squares of its arguments (Pythagoras’ theorem):
```js
> Math.hypot(3, 4)
5
```


## 3 New string features
New string methods:
```js
> 'hello'.startsWith('hell')
true
> 'hello'.endsWith('ello')
true
> 'hello'.includes('ell')
true
> 'doo '.repeat(3)
'doo doo doo '
```

ES6 has a new kind of string literal, the _template_ literal:
```js
// String interpolation via template literals (in backticks)
const first = 'Jane';
const last = 'Doe';
console.log(`Hello ${first} ${last}!`);
    // Hello Jane Doe!

// Template literals also let you create strings with multiple lines
const multiLine = `
This is
a string
with multiple
lines`;
```


## 4 Symbols
Symbols are a new primitive type in ECMAScript 6. They are created via a factory function:
```js
const mySymbol = Symbol('mySymbol');
```

Every time you call the factory function, a new and unique symbol is created. The optional parameter is a descriptive string that is shown when printing the symbol (it has no other purpose):
```js
> mySymbol
Symbol(mySymbol)
```

### 4.1 Use case 1: unique property keys
Symbols are mainly used as unique property keys – a symbol never clashes with any other property key (symbol or string). For example, you can make an object _iterable_ (usable via the `for-of` loop and other language mechanisms), by using the symbol stored in `Symbol.iterator` as the key of a method (more information on iterables is given in [the chapter on iteration](http://exploringjs.com/es6/ch_iteration.html#ch_iteration)):
```js
const iterableObject = {
    [Symbol.iterator]() { // (A)
        ···
    }
}
for (const x of iterableObject) {
    console.log(x);
}
// Output:
// hello
// world
```

In line A, a symbol is used as the key of the method. This unique marker makes the object iterable and enables us to use the `for-of` loop.

### 4.2 Use case 2: constants representing concepts
In ECMAScript 5, you may have used strings to represent concepts such as colors. In ES6, you can use symbols and be sure that they are always unique:
```js
const COLOR_RED    = Symbol('Red');
const COLOR_ORANGE = Symbol('Orange');
const COLOR_YELLOW = Symbol('Yellow');
const COLOR_GREEN  = Symbol('Green');
const COLOR_BLUE   = Symbol('Blue');
const COLOR_VIOLET = Symbol('Violet');

function getComplement(color) {
    switch (color) {
        case COLOR_RED:
            return COLOR_GREEN;
        case COLOR_ORANGE:
            return COLOR_BLUE;
        case COLOR_YELLOW:
            return COLOR_VIOLET;
        case COLOR_GREEN:
            return COLOR_RED;
        case COLOR_BLUE:
            return COLOR_ORANGE;
        case COLOR_VIOLET:
            return COLOR_YELLOW;
        default:
            throw new Exception('Unknown color: '+color);
    }
}
```

Every time you call `Symbol('Red')`, a new symbol is created. Therefore, `COLOR_RED` can never be mistaken for another value. That would be different if it were the string `'Red'`.

### 4.3 Pitfall: you can’t coerce symbols to strings
Coercing (implicitly converting) symbols to strings throws exceptions:
```js
const sym = Symbol('desc');

const str1 = '' + sym; // TypeError
const str2 = `${sym}`; // TypeError
```

The only solution is to convert explicitly:
```js
const str2 = String(sym); // 'Symbol(desc)'
const str3 = sym.toString(); // 'Symbol(desc)'
```

Forbidding coercion prevents some errors, but also makes working with symbols more complicated.

### 4.4 Which operations related to property keys are aware of symbols?
The following operations are aware of symbols as property keys:

- `Reflect.ownKeys()`
- `Property access via []`
- `Object.assign()`

The following operations ignore symbols as property keys:

- `Object.keys()`
- `Object.getOwnPropertyNames()`
- `for-in loop`


## 5 Template literals
ES6 has two new kinds of literals: `template literals` and `tagged template literals`. These two literals have similar names and look similar, but they are quite different. It is therefore important to distinguish:

- **Template literals (code):** multi-line string literals that support interpolation
- **Tagged template literals (code):** function calls
- **Web templates (data):** HTML with blanks to be filled in

_Template literals_ are string literals that can stretch across multiple lines and include interpolated expressions (inserted via `${···}`):
```js
const firstName = 'Jane';
console.log(`Hello ${firstName}!
How are you
today?`);

// Output:
// Hello Jane!
// How are you
// today?
```

_Tagged template literals_ (short: _tagged templates_) are created by mentioning a function before a template literal:
```js
> String.raw`A \tagged\ template`
'A \\tagged\\ template'
```

Tagged templates are function calls. In the previous example, the method `String.raw` is called to produce the result of the tagged template.


## 6 Variables and scoping
ES6 provides two new ways of declaring variables: `let` and `const`, which mostly replace the ES5 way of declaring variables, `var`.

### 6.1 `let`
`let` works similarly to var, but the variable it declares is _block-scoped_, it only exists within the current block. var is _function-scoped_.

In the following code, you can see that the let-declared variable `tmp` only exists inside the block that starts in line A:
```js
function order(x, y) {
    if (x > y) { // (A)
        let tmp = x;
        x = y;
        y = tmp;
    }
    console.log(tmp===x); // ReferenceError: tmp is not defined
    return [x, y];
}
```

### 6.2 `const`
`const` works like `let`, but the variable you declare must be immediately initialized, with a value that can’t be changed afterwards.
```js
const foo;
    // SyntaxError: missing = in const declaration

const bar = 123;
bar = 456;
    // TypeError: `bar` is read-only
```

Since `for-of` creates one _binding_ (storage space for a variable) per loop iteration, it is OK to `const`-declare the loop variable:
```js
for (const x of ['a', 'b']) {
    console.log(x);
}
// Output:
// a
// b
```

### 6.3 Ways of declaring variables
The following table gives an overview of six ways in which variables can be declared in ES6 (inspired by [a table by kangax](https://twitter.com/kangax/status/567330097603284992)):

|Type       | Hoisting           | Scope         | Creates global properties
|-----------|--------------------|---------------|--------------------------
|`var`      | Declaration        | Function      | Yes
|`let`      | Temporal dead zone | Block         | No
|`const`    | Temporal dead zone | Block         | No
|`function` | Complete           | Block         | Yes
|`class`    | No                 | Block         | No
|`import`   | Complete           | Module-global | No


## 7 Destructuring
_Destructuring_ is a convenient way of extracting multiple values from data stored in (possibly nested) objects and Arrays. It can be used in locations that receive data (such as the left-hand side of an assignment). How to extract the values is specified via patterns (read on for examples).

### 7.1 Object destructuring
Destructuring objects:
```js
const obj = { first: 'Jane', last: 'Doe' };
const {first: f, last: l} = obj;
    // f = 'Jane'; l = 'Doe'

// {prop} is short for {prop: prop}
const {first, last} = obj;
    // first = 'Jane'; last = 'Doe'
```

Destructuring helps with processing return values:
```js
const obj = { foo: 123 };
const {writable, configurable} = Object.getOwnPropertyDescriptor(obj, 'foo');
console.log(writable, configurable); // true true
```

### 7.2 Array destructuring
Array destructuring (works for all iterable values):
```js
const iterable = ['a', 'b'];
const [x, y] = iterable;
    // x = 'a'; y = 'b'
```

Destructuring helps with processing return values:
```js
const [all, year, month, day] =
    /^(\d\d\d\d)-(\d\d)-(\d\d)$/
    .exec('2999-12-31');
```

### 7.3 Where can destructuring be used?
Destructuring can be used in the following locations (I’m showing Array patterns to demonstrate; object patterns work just as well):
```js
// Variable declarations:
const [x] = ['a'];
let [x] = ['a'];
var [x] = ['a'];

// Assignments:
[x] = ['a'];

// Parameter definitions:
function f([x]) { ··· }
f(['a']);
```

You can also destructure in a `for-of` loop:
```js
const arr = ['a', 'b'];
for (const [index, element] of arr.entries()) {
    console.log(index, element);
}
// Output:
// 0 a
// 1 b
```


## 8 Parameter handling
Parameter handling has been significantly upgraded in ECMAScript 6. It now supports parameter default values, rest parameters (varargs) and destructuring.

Additionally, the spread operator helps with function/method/constructor calls and Array literals.

### 8.1 Default parameter values
A _default parameter_ value is specified for a parameter via an equals sign (`=`). If a caller doesn’t provide a value for the parameter, the default value is used. In the following example, the default parameter value of `y` is 0:
```js
function func(x, y=0) {
    return [x, y];
}
func(1, 2); // [1, 2]
func(1); // [1, 0]
func(); // [undefined, 0]
```

### 8.2 Rest parameters
If you prefix a parameter name with the rest operator (`...`), that parameter receives all remaining parameters via an Array:
```js
function format(pattern, ...params) {
    return {pattern, params};
}
format(1, 2, 3);
    // { pattern: 1, params: [ 2, 3 ] }
format();
    // { pattern: undefined, params: [] }
```

### 8.3 Named parameters via destructuring
You can simulate named parameters if you destructure with an object pattern in the parameter list:
```js
function selectEntries({ start=0, end=-1, step=1 } = {}) { // (A)
    // The object pattern is an abbreviation of:
    // { start: start=0, end: end=-1, step: step=1 }

    // Use the variables `start`, `end` and `step` here
    ···
}

selectEntries({ start: 10, end: 30, step: 2 });
selectEntries({ step: 3 });
selectEntries({});
selectEntries();
```

The `= {}` in line A enables you to call `selectEntries()` without paramters.

### 8.4 Spread operator (`...`)
In function and constructor calls, the spread operator turns iterable values into arguments:
```js
> Math.max(-1, 5, 11, 3)
11
> Math.max(...[-1, 5, 11, 3])
11
> Math.max(-1, ...[-5, 11], 3)
11
```

In Array literals, the spread operator turns iterable values into Array elements:
```js
> [1, ...[2,3], 4]
[1, 2, 3, 4]
```


## 9 Callable entities in ECMAScript 6
In ES5, a single construct, the (traditional) function, played three roles:

- Real (non-method) function
- Method
- Constructor

In ES6, there is more specialization. The three duties are now handled as follows. As far as function definitions and class definitions are concerned, a definition is either a declaration or an expression.

- Real (non-method) function:
    - Arrow functions (only have an expression form)
    - Traditional functions (created via function definitions)
    - Generator functions (created via generator function definitions)
- Method:
    - Methods (created by method definitions in object literals and class definitions)
    - Generator methods (created by generator method definitions in object literals and class definitions)
- Constructor:
    - Classes (created via class definitions)

Especially for callbacks, arrow functions are handy, because they don’t shadow the `this` of the surrounding scope.

For longer callbacks and stand-alone functions, traditional functions can be OK. Some APIs use `this` as an implicit parameter. In that case, you have no choice but to use traditional functions.

Note that I distinguish:

- The entities: e.g. traditional functions
- The syntax that creates the entities: e.g. function definitions

Even though their behaviors differ (as explained later), all of these entities are functions. For example:
```js
> typeof (() => {}) // arrow function
'function'
> typeof function* () {} // generator function
'function'
> typeof class {} // class
'function'
```


# 10 Arrow functions
There are two benefits to arrow functions.

First, they are less verbose than traditional function expressions:
```js
const arr = [1, 2, 3];
const squares = arr.map(x => x * x);

// Traditional function expression:
const squares = arr.map(function (x) { return x * x });
```

Second, their `this` is picked up from surroundings (_lexical_). Therefore, you don’t need `bind()` or `that = this`, anymore.
```js
function UiComponent() {
    const button = document.getElementById('myButton');
    button.addEventListener('click', () => {
        console.log('CLICK');
        this.handleClick(); // lexical `this`
    });
}
```

The following variables are all lexical inside arrow functions:

- arguments
- super
- this
- new.target


## 11 New OOP features besides classes
### 11.1 New object literal features
Method definitions:
```js
const obj = {
    myMethod(x, y) {
        ···
    }
};
```

Property value shorthands:
```js
const first = 'Jane';
const last = 'Doe';

const obj = { first, last };
// Same as:
const obj = { first: first, last: last };
```

Computed property keys:
```js
const propKey = 'foo';
const obj = {
    [propKey]: true,
    ['b'+'ar']: 123
};
```

This new syntax can also be used for method definitions:
```js
const obj = {
    ['h'+'ello']() {
        return 'hi';
    }
};
console.log(obj.hello()); // hi
```

The main use case for computed property keys is to make it easy to use symbols as property keys.

### 11.2 New methods in Object
The most important new method of Object is `assign()`. Traditionally, this functionality was called `extend()` in the JavaScript world. In contrast to how this classic operation works, `Object.assign()` only considers _own_ (non-inherited) properties.
```js
const obj = { foo: 123 };
Object.assign(obj, { bar: true });
console.log(JSON.stringify(obj));
    // {"foo":123,"bar":true}
```


## 12 Classes
A class and a subclass:
```js
class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    toString() {
        return `(${this.x}, ${this.y})`;
    }
}

class ColorPoint extends Point {
    constructor(x, y, color) {
        super(x, y);
        this.color = color;
    }
    toString() {
        return super.toString() + ' in ' + this.color;
    }
}
```

Using the classes:
```js
> const cp = new ColorPoint(25, 8, 'green');

> cp.toString();
'(25, 8) in green'

> cp instanceof ColorPoint
true
> cp instanceof Point
true
```

Under the hood, ES6 classes are not something that is radically new: They mainly provide more convenient syntax to create old-school constructor functions. You can see that if you use `typeof`:
```js
> typeof Point
'function'
```


## 13 Modules
JavaScript has had modules for a long time. However, they were implemented via libraries, not built into the language. ES6 is the first time that JavaScript has built-in modules.

ES6 modules are stored in files. There is exactly one module per file and one file per module. You have two ways of exporting things from a module. [These two ways can be mixed](http://exploringjs.com/es6/ch_modules.html#sec_mixing-named-and-default-exports), but it is usually better to use them separately.

### 13.1 Multiple named exports
There can be multiple named exports:
```js
//------ lib.js ------
export const sqrt = Math.sqrt;
export function square(x) {
    return x * x;
}
export function diag(x, y) {
    return sqrt(square(x) + square(y));
}

//------ main.js ------
import { square, diag } from 'lib';
console.log(square(11)); // 121
console.log(diag(4, 3)); // 5
```

You can also import the complete module:
```js
//------ main.js ------
import * as lib from 'lib';
console.log(lib.square(11)); // 121
console.log(lib.diag(4, 3)); // 5
```

### 13.2 Single default export
There can be a single _default_ export. For example, a function:
```js
//------ myFunc.js ------
export default function () { ··· } // no semicolon!

//------ main1.js ------
import myFunc from 'myFunc';
myFunc();
```

Or a class:
```js
//------ MyClass.js ------
export default class { ··· } // no semicolon!

//------ main2.js ------
import MyClass from 'MyClass';
const inst = new MyClass();
```

Note that there is no semicolon at the end if you default-export a function or a class (which are anonymous declarations).

### 13.3 Browsers: scripts versus modules

|                                         |    Scripts    | Modules
|HTML element                             | `<script>`    | `<script type="module">`
|Default mode                             | non-strict    | strict
|Top-level variables are                  | global        | local to module
|Value of this at top level               | `window`      | `undefined`
|Executed                                 | synchronously | asynchronously
|Declarative imports (import statement)   | no            | yes
|Programmatic imports (Promise-based API) | yes           | yes
|File extension                           | `.js`         | `.js`


## 14 The `for-of` loop
`for-of` is a new loop in ES6 that replaces both `for-in` and `forEach()` and supports the new iteration protocol.

Use it to loop over _iterable_ objects (Arrays, strings, Maps, Sets, etc.; see Chap. “[Iterables and iterators](http://exploringjs.com/es6/ch_iteration.html#ch_iteration)”):
```js
const iterable = ['a', 'b'];
for (const x of iterable) {
    console.log(x);
}

// Output:
// a
// b
```

`break` and `continue` work inside `for-of` loops:
```js
for (const x of ['a', '', 'b']) {
    if (x.length === 0) break;
    console.log(x);
}

// Output:
// a
```

Access both elements and their indices while looping over an Array (the square brackets before `of` mean that we are using [destructuring](http://exploringjs.com/es6/ch_destructuring.html#ch_destructuring)):
```js
const arr = ['a', 'b'];
for (const [index, element] of arr.entries()) {
    console.log(`${index}. ${element}`);
}

// Output:
// 0. a
// 1. b
```

Looping over the `[key, value]` entries in a Map (the square brackets before of mean that we are using [destructuring](http://exploringjs.com/es6/ch_destructuring.html#ch_destructuring)):
```js
const map = new Map([
    [false, 'no'],
    [true, 'yes'],
]);
for (const [key, value] of map) {
    console.log(`${key} => ${value}`);
}

// Output:
// false => no
// true => yes
```


## 15 New Array features
New static Array methods:

- `Array.from(arrayLike, mapFunc?, thisArg?)`
- `Array.of(...items)`

New `Array.prototype` methods:

- Iterating:
    - `Array.prototype.entries()`
    - `Array.prototype.keys()`
    - `Array.prototype.values()`
- Searching for elements:
    - `Array.prototype.find(predicate, thisArg?)`
    - `Array.prototype.findIndex(predicate, thisArg?)`
- `Array.prototype.copyWithin(target, start, end=this.length)`
- `Array.prototype.fill(value, start=0, end=this.length)`


## 16 Maps and Sets
Among others, the following four data structures are new in ECMAScript 6: `Map`, `WeakMap`, `Set` and `WeakSet`.

### 16.1 Maps
The keys of a Map can be arbitrary values:
```js
> const map = new Map(); // create an empty Map
> const KEY = {};

> map.set(KEY, 123);
> map.get(KEY)
123
> map.has(KEY)
true
> map.delete(KEY);
true
> map.has(KEY)
false
```

You can use an Array (or any iterable) with `[key, value]` pairs to set up the initial data in the Map:
```js
const map = new Map([
    [ 1, 'one' ],
    [ 2, 'two' ],
    [ 3, 'three' ], // trailing comma is ignored
]);
```

### 16.2 Sets
A Set is a collection of unique elements:
```js
const arr = [5, 1, 5, 7, 7, 5];
const unique = [...new Set(arr)]; // [ 5, 1, 7 ]
```

As you can see, you can initialize a Set with elements if you hand the constructor an iterable (`arr` in the example) over those elements.

### 16.3 WeakMaps
A WeakMap is a Map that doesn’t prevent its keys from being garbage-collected. That means that you can associate data with objects without having to worry about memory leaks. For example:
```js
//----- Manage listeners

const _objToListeners = new WeakMap();

function addListener(obj, listener) {
    if (! _objToListeners.has(obj)) {
        _objToListeners.set(obj, new Set());
    }
    _objToListeners.get(obj).add(listener);
}

function triggerListeners(obj) {
    const listeners = _objToListeners.get(obj);
    if (listeners) {
        for (const listener of listeners) {
            listener();
        }
    }
}

//----- Example: attach listeners to an object

const obj = {};
addListener(obj, () => console.log('hello'));
addListener(obj, () => console.log('world'));

//----- Example: trigger listeners

triggerListeners(obj);

// Output:
// hello
// world
```


## 17 Typed Arrays
Typed Arrays are an ECMAScript 6 API for handling binary data.

Code example:
```js
const typedArray = new Uint8Array([0,1,2]);
console.log(typedArray.length); // 3
typedArray[0] = 5;
const normalArray = [...typedArray]; // [5,1,2]

// The elements are stored in typedArray.buffer.
// Get a different view on the same data:
const dataView = new DataView(typedArray.buffer);
console.log(dataView.getUint8(0)); // 5
```

Instances of ArrayBuffer store the binary data to be processed. Two kinds of views are used to access the data:

- Typed Arrays (`Uint8Array`, `Int16Array`, `Float32Array`, etc.) interpret the ArrayBuffer as an indexed sequence of elements of a single type.
- Instances of `DataView` let you access data as elements of several types (`Uint8`, `Int16`, `Float32`, etc.), at any byte offset inside an ArrayBuffer.

The following browser APIs support Typed Arrays ([details are mentioned in a dedicated section](http://exploringjs.com/es6/ch_typed-arrays.html#sec_browser-apis-supporting-typed-arrays)):

- File API
- XMLHttpRequest
- Fetch API
- Canvas
- WebSockets
- And more


## 18 Iterables and iterators
ES6 introduces a new mechanism for traversing data: _iteration_. Two concepts are central to iteration:

- An _iterable_ is a data structure that wants to make its elements accessible to the public. It does so by implementing a method whose key is `Symbol.iterator`. That method is a factory for _iterators_.
- An _iterator_ is a pointer for traversing the elements of a data structure (think cursors in databases).

Expressed as interfaces in TypeScript notation, these roles look like this:
```js
interface Iterable {
    [Symbol.iterator]() : Iterator;
}
interface Iterator {
    next() : IteratorResult;
}
interface IteratorResult {
    value: any;
    done: boolean;
}
```

### 18.1 Iterable values
The following values are iterable:

- Arrays
- Strings
- Maps
- Sets
- DOM data structures (work in progress)

Plain objects are not iterable (why is explained in [a dedicated section](http://exploringjs.com/es6/ch_iteration.html#sec_plain-objects-not-iterable)).

### 18.2 Constructs supporting iteration
Language constructs that access data via iteration:

- Destructuring via an Array pattern:
```js
const [a,b] = new Set(['a', 'b', 'c']);
```
- `for-of` loop:
```js
for (const x of ['a', 'b', 'c']) {
    console.log(x);
}
```
- `Array.from()`:
```js
const arr = Array.from(new Set(['a', 'b', 'c']));
```
- Spread operator (`...`):
```js
const arr = [...new Set(['a', 'b', 'c'])];
```
- Constructors of Maps and Sets:
```js
const map = new Map([[false, 'no'], [true, 'yes']]);
const set = new Set(['a', 'b', 'c']);
```
- `Promise.all()`, `Promise.race()`:
```js
Promise.all(iterableOverPromises).then(···);
Promise.race(iterableOverPromises).then(···);
```
- `yield*`:
```js
yield* anIterable;
```


## 19 Generators
### 19.1 What are generators?
You can think of generators as processes (pieces of code) that you can pause and resume:
```js
function* genFunc() {
    // (A)
    console.log('First');
    yield;
    console.log('Second');
}
```

Note the new syntax: `function*` is a new “keyword” for _generator functions_ (there are also _generator methods_). yield is an operator with which a generator can pause itself. Additionally, generators can also receive input and send output via yield.

When you call a generator function `genFunc()`, you get a _generator object_ `genObj` that you can use to control the process:
```js
const genObj = genFunc();
```

The process is initially paused in line A. `genObj.next()` resumes execution, a yield inside `genFunc()` pauses execution:
```js
genObj.next();
// Output: First
genObj.next();
// output: Second
```

### 19.2 Kinds of generators
There are four kinds of generators:

1. Generator function declarations:
```js
function* genFunc() { ··· }
const genObj = genFunc();
```
2. Generator function expressions:
```js
const genFunc = function* () { ··· };
const genObj = genFunc();
```
3. Generator method definitions in object literals:
```js
const obj = {
    * generatorMethod() {
        ···
    }
};
const genObj = obj.generatorMethod();
```
4. Generator method definitions in class definitions (class declarations or class expressions):
```js
class MyClass {
    * generatorMethod() {
        ···
    }
}
const myInst = new MyClass();
const genObj = myInst.generatorMethod();
```

### 19.3 Use case: implementing iterables
The objects returned by generators are iterable; each `yield` contributes to the sequence of iterated values. Therefore, you can use generators to implement iterables, which can be consumed by various ES6 language mechanisms: `for-of` loop, spread operator (`...`), etc.

The following function returns an iterable over the properties of an object, one `[key, value]` pair per property:
```js
function* objectEntries(obj) {
    const propKeys = Reflect.ownKeys(obj);

    for (const propKey of propKeys) {
        // `yield` returns a value and then pauses
        // the generator. Later, execution continues
        // where it was previously paused.
        yield [propKey, obj[propKey]];
    }
}
```

`objectEntries()` is used like this:
```js
const jane = { first: 'Jane', last: 'Doe' };
for (const [key,value] of objectEntries(jane)) {
    console.log(`${key}: ${value}`);
}
// Output:
// first: Jane
// last: Doe
```

How exactly `objectEntries()` works is explained in [a dedicated section](http://exploringjs.com/es6/ch_generators.html#objectEntries_generator). Implementing the same functionality without generators is much more work.

### 19.4 Use case: simpler asynchronous code
You can use generators to tremendously simplify working with Promises. Let’s look at a Promise-based function fetchJson() and how it can be improved via generators.
```js
function fetchJson(url) {
    return fetch(url)
    .then(request => request.text())
    .then(text => {
        return JSON.parse(text);
    })
    .catch(error => {
        console.log(`ERROR: ${error.stack}`);
    });
}
```

With [the library co](https://github.com/tj/co) and a generator, this asynchronous code looks synchronous:
```js
const fetchJson = co.wrap(function* (url) {
    try {
        let request = yield fetch(url);
        let text = yield request.text();
        return JSON.parse(text);
    }
    catch (error) {
        console.log(`ERROR: ${error.stack}`);
    }
});
```

ECMAScript 2017 will have `async` functions which are internally based on generators. With them, the code looks like this:
```js
async function fetchJson(url) {
    try {
        let request = await fetch(url);
        let text = await request.text();
        return JSON.parse(text);
    }
    catch (error) {
        console.log(`ERROR: ${error.stack}`);
    }
}
```

All versions can be invoked like this:
```js
fetchJson('http://example.com/some_file.json').then(obj => console.log(obj));
```

### 19.5 Use case: receiving asynchronous data
Generators can receive input from `next()` via yield. That means that you can wake up a generator whenever new data arrives asynchronously and to the generator it feels like it receives the data synchronously.


## 20 New regular expression features
The following regular expression features are new in ECMAScript 6:

- The new flag `/y` (sticky) anchors each match of a regular expression to the end of the previous match.
- The new flag `/u` (unicode) handles surrogate pairs (such as `\uD83D\uDE80`) as code points and lets you use Unicode code point escapes (such as `\u{1F680}`) in regular expressions.
- The new data property `flags` gives you access to the flags of a regular expression, just like `source` already gives you access to the pattern in ES5:
```js
> /abc/ig.source // ES5
'abc'
> /abc/ig.flags // ES6
'gi'
```
- You can use the constructor `RegExp()` to make a copy of a regular expression:
```js
> new RegExp(/abc/ig).flags
'gi'
> new RegExp(/abc/ig, 'i').flags // change flags
'i'
```


## 21 Promises for asynchronous programming
Promises are an alternative to callbacks for delivering the results of an asynchronous computation. They require more effort from implementors of asynchronous functions, but provide several benefits for users of those functions.

The following function returns a result asynchronously, via a Promise:
```js
function asyncFunc() {
    return new Promise(
        function (resolve, reject) {
            ···
            resolve(result);
            ···
            reject(error);
        });
}
```

You call `asyncFunc()` as follows:
```js
asyncFunc().then(result => { ··· }).catch(error => { ··· });
```

### 21.1 Chaining `then()` calls
`then()` always returns a Promise, which enables you to chain method calls:
```js
asyncFunc1()
.then(result1 => {
    // Use result1
    return asyncFunction2(); // (A)
})
.then(result2 => { // (B)
    // Use result2
})
.catch(error => {
    // Handle errors of asyncFunc1() and asyncFunc2()
});
```

How the Promise P returned by `then()` is settled depends on what its callback does:

- If it returns a Promise (as in line A), the settlement of that Promise is forwarded to P. That’s why the callback from line B can pick up the settlement of asyncFunction2’s Promise.
- If it returns a different value, that value is used to settle P.
- If throws an exception then P is rejected with that exception.

Furthermore, note how `catch()` handles the errors of two asynchronous function calls (`asyncFunction1()` and `asyncFunction2()`). That is, uncaught errors are passed on until there is an error handler.

### 21.2 Executing asynchronous functions in parallel
If you chain asynchronous function calls via `then()`, they are executed sequentially, one at a time:
```js
asyncFunc1().then(() => asyncFunc2());
```

If you don’t do that and call all of them immediately, they are basically executed in parallel (a _fork_ in Unix process terminology):
```js
asyncFunc1();
asyncFunc2();
```

`Promise.all()` enables you to be notified once all results are in (a _join_ in Unix process terminology). Its input is an Array of Promises, its output a single Promise that is fulfilled with an Array of the results.
```js
Promise.all([
    asyncFunc1(),
    asyncFunc2(),
])
.then(([result1, result2]) => {
    ···
})
.catch(err => {
    // Receives first rejection among the Promises
    ···
});
```

### 21.3 Glossary: Promises
The Promise API is about delivering results asynchronously. A _Promise object_ (short: Promise) is a stand-in for the result, which is delivered via that object.

States:

- A Promise is always in one of three mutually exclusive states:
    - Before the result is ready, the Promise is pending.
    - If a result is available, the Promise is _fulfilled_.
    - If an error happened, the Promise is _rejected_.
- A Promise is _settled_ if “things are done” (if it is either fulfilled or rejected).
- A Promise is settled exactly once and then remains unchanged.

Reacting to state changes:

- _Promise reactions_ are callbacks that you register with the Promise method `then()`, to be notified of a fulfillment or a rejection.
- A _thenable_ is an object that has a Promise-style `then()` method. Whenever the API is only interested in being notified of settlements, it only demands thenables (e.g. the values returned from `then()` and `catch()`; or the values handed to `Promise.all()` and `Promise.race()`).

Changing states: There are two operations for changing the state of a Promise. After you have invoked either one of them once, further invocations have no effect.

- _Rejecting_ a Promise means that the Promise becomes rejected.
- _Resolving_ a Promise has different effects, depending on what value you are resolving with:
    - Resolving with a normal (non-thenable) value fulfills the Promise.
    - Resolving a Promise P with a thenable T means that P can’t be resolved anymore and will now follow T’s state, including its fulfillment or rejection value. The appropriate P reactions will get called once T settles (or are called immediately if T is already settled).


## 22 Metaprogramming with proxies
Proxies enable you to intercept and customize operations performed on objects (such as getting properties). They are a _metaprogramming_ feature.

In the following example, `proxy` is the object whose operations we are intercepting and `handler` is the object that handles the interceptions. In this case, we are only intercepting a single operation, `get` (getting properties).
```js
const target = {};
const handler = {
    get(target, propKey, receiver) {
        console.log('get ' + propKey);
        return 123;
    }
};
const proxy = new Proxy(target, handler);
```

When we get the property `proxy.foo`, the handler intercepts that operation:
```js
> proxy.foo
get foo
123
```

Consult [the reference for the complete API](http://exploringjs.com/es6/ch_proxies.html#sec_reference-proxy-api) for a list of operations that can be intercepted.
