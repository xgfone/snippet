const webpack = require("webpack");
const config = require('./config');

const webpack_dll_config = {
    cache: true,
    target: 'web',
    context: config.ROOT,
    devtool: 'cheap-module-source-map',

    output: {
        path: config.DLL_OUTPUT_PATH,
        filename: '[name]-[chunkhash].js',
        library: "[name]",
    },

    entry: (() => {
        let result = {};
        config.DLL_NAMES.forEach((name) => {
            result[name] = [config.resolve_dll(name + '.js')];
        });
        return result;
    })(),

    plugins: [
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify('production'),
        }),
        new webpack.optimize.UglifyJsPlugin(config.UGLIFY_JS_OPTION),
        new webpack.DllPlugin({
            path: config.resolve_dll('[name]-manifest.json'),
            name: "[name]",
            // context: config.DLL_OUTPUT_PATH,
        }),
    ],
};

module.exports = webpack_dll_config;
