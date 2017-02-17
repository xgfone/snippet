const webpack = require('webpack');
const webpack_merge = require('webpack-merge');
const config = require('./config');
const webpack_base_config = require('./webpack.base.config');

const webpack_dev_config = {
    // How Source Maps are generated.
    devtool: 'cheap-module-eval-source-map',

    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoErrorsPlugin(),
    ],

    devServer: {
        port: config.DEV_PORT,
        host: config.DEV_HOST,
        publicPath: config.OUTPUT_PUBLIC_PATH,
        contentBase: [config.DEV_BUILD_PATH],

        watchContentBase: true,
        watchOptions: {
            aggregateTimeout: 3000, // 1s
            ignored: /node_modules/,
            poll: 3000 // Check for changes every 3 seconds. Or true.
        },

        hot: true,
        colors: true,
        inline: true, // Livereload
        historyApiFallback: true,
    },
}

const webpack_config = webpack_merge.smart(webpack_base_config, webpack_dev_config);
module.exports = webpack_config;
