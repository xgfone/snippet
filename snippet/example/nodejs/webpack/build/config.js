// import * as path from 'path';
const path = require('path');
const process = require('process');
const _ = require('lodash');

const ROOT = path.join(__dirname, '..');
const resolve_path = (...dirs) => path.join(ROOT, ...dirs);
const resolve_dll = (file) => path.join(config.DLL_OUTPUT_PATH, file);

const config = {
    ROOT,
    get DEBUG() {
        return process.env.NODE_ENV != 'production';
    },

    // For Enter Points
    // The path is the relative path to ROOT.
    entry: {
        index: './src/index.js',
    },

    // For Output
    OUTPUT_PUBLIC_PATH: '/dist/', // http://static.example.com/
    get OUTPUT_PATH() {
        const subdir = config.DEBUG ? 'dev' : 'dist';
        return resolve_path(subdir);
    },

    // For DLL
    DLL_NAMES: ['vendor'],
    DLL_OUTPUT_PATH: resolve_path('dll'),

    // For Development
    DEV_HOST: '0.0.0.0',
    DEV_PORT: 8000,

    // For Other Plugin Options
    HTML_TEMPLATE_PATH: ROOT,
    UGLIFY_JS_OPTION: {
        exclude: /\.min\.js$/,
        sourceMap: true,
        comments: false,
        mangle: false,
    },

    // Some convenient functions
    resolve_path,
    resolve_dll,
    path_join: path.join,
}

// export default config;
module.exports = config;
