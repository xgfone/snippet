
## 1. `node-gpy` failed to build the C/C++ package on Windows.

Run `npm install --global --production windows-build-tools`.

**Notice:** Reference to https://github.com/nodejs/node-gyp#installation.


## 2. `shim` 和 `polyfill` 有什么区别？

`shim` 是一个库，它将一个新的 API 引入到一个旧的环境中，而且仅靠旧环境中已有的技术实现，有时候也称 `shiv`。

`polyfill` 是一段代码（或者插件），提供那些开发者们希望 **浏览器** 原生提供支持的功能。因此，一个 `polyfill` 就是一个用在浏览器 API 上的 `shim`。通常的做法是先检查当前浏览器是否支持某个 API，如果不支持的话就加载对应的 `polyfill`。然后新旧浏览器就都可以使用这个 API 了。

**Reference:** https://remysharp.com/2010/10/08/what-is-a-polyfill.
