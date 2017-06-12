const path = require('path');
const process = require('process');
const _ = require('lodash');

const DEV_DIR = 'dev';
const DIST_DIR = 'dist';

const ROOT = path.join(__dirname, '..');
const resolve_path = (...dirs) => path.join(ROOT, ...dirs);
const resolve_dll = (file) => path.join(config.DLL_OUTPUT_PATH, file);

const config = {
    ROOT,
    ESLINT: false,
    APP_ROOT: resolve_path('src'),
    get DEBUG() {
        return process.env.NODE_ENV != 'production';
    },

    TARGET: 'web',

    // For Entry Points
    // The path is the relative path to ROOT.
    ENTRY: {
        // Set up an ES6-ish environment
        // babel: 'babel-polyfill',

        index1: ['./src/index1.js'],
        index2: ['./src/index2.js'],
    },

    // For Output
    get OUTPUT_PUBLIC_PATH() {
        // const DIST_DIR = 'http://static.example.com/static/';
        return config.DEBUG ? `/${DEV_DIR}/` : `/${DIST_DIR}/`;
    },
    get OUTPUT_PATH() {
        const subdir = config.DEBUG ? DEV_DIR : DIST_DIR;
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
        beautify: false,
        compress: {
            warnings: false,
            drop_console: true,
            collapse_vars: true,
            reduce_vars: true,
        },
    },

    // Some convenient functions
    resolve_path,
    resolve_dll,
    path_join: path.join,
}

module.exports = config;
