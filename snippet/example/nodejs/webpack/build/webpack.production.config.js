const process = require('process');
const webpack = require('webpack');
const webpack_merge = require('webpack-merge');

process.env.NODE_ENV = 'production';
const config = require('./config');
const webpack_base_config = require('./webpack.base.config');

const webpack_production_config = {
    // How Source Maps are generated.
    devtool: 'cheap-module-source-map',

    plugins: [
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify('production'),
        }),
        new webpack.optimize.UglifyJsPlugin(config.UGLIFY_JS_OPTION),
    ],
}

const webpack_config = webpack_merge.smart(webpack_base_config, webpack_production_config);
module.exports = webpack_config;
