// Load the JS dependencies Asynchronously, then call the callback.
//
// For example,
//
// getScripts(['http://example.com/js1.js', 'http://example.com/js2.js'], function () {
//     alert('Finish to load all the dependencies.');
// });
function getScripts(dependencies, callback) {
    'use strict';

    function _getScripts(i, linkArray, fn) {
        env || getEnv();
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = linkArray[i];
        var head = document.head || document.getElementsByTagName('head')[0];
        head.appendChild(script);

        if ('onload' in script) {
            script.onload = function () {
                if (i === linkArray.length - 1) {
                    if (fn) {
                        fn();
                    }
                } else {
                    _getScripts(++i, linkArray, fn);
                }
            };
        } else { // For IE.
            script.onreadystatechange = function () {
                if (/loaded|complete/.test(script.readyState)) {
                    script.onreadystatechange = null;
                    if (i === linkArray.length - 1) {
                        if (fn) {
                            fn();
                        }
                    } else {
                        _getScripts(++i, linkArray, fn);
                    }
                }
            };
        }
    }

    _getScripts(0, dependencies, callback);
}
