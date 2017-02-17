const path = require('path');
const webpack = require('webpack');
const config = require('./config');

const HtmlWebpackPlugin = require('html-webpack-plugin');
// const CopyWebpackPlugin = require('copy-webpack-plugin');
// const ExtractTextPlugin = require('extract-text-webpack-plugin');

const webpack_base_config = {
    cache: true,
    target: 'web',

    // The home directory for webpack.
    // The entry and module.rules.loader option is resolved relative to this directory.
    context: config.ROOT,

    // The Entry Points
    entry: config.entry,

    // The output
    output: {
        path: config.OUTPUT_PATH,
        publicPath: config.OUTPUT_PUBLIC_PATH,
        filename: '[name]-[chunkhash].js',
        //chunkFilename: '[name]-[chunkhash].js',
        //crossOriginLoading: false | "anonymous" | "use-credentials",
    },

    // The Loaders
    module: {
        rules: [
            // Handle JSON files
            {
                test: /\.(json)$/,
                exclude: /node_modules/,
                loader: 'json-loader',
            },
            // Handle JS files
            // {
            //     test: /\.(js)$/,
            //     exclude: /node_modules/,
            //     use: [
            //         {loader: 'babel-loader'},
            //         {loader: 'eslint-loader'},
            //     ]
            // },
            // Handle Image files
            // {
            //     test: /\.(?:png|jpe?g|git)$/,
            //     use: [
            //         {
            //             loader: 'url-loader',
            //             options: {
            //                 limit: 8192,
            //             },
            //         },
            //     ]
            // },
            // Handle CSS/LESS files
            // {
            //     test: /\.(less|css)$/,
            //     loader: ExtractTextPlugin.extract('style', 'css?module&localIdentName=[hash:base64:7]!less'),
            // },
        ],
    },

    plugins: config.DLL_NAMES.map((name) => {
        const manifest = config.resolve_dll(name + '-manifest.json');
        return new webpack.DllReferencePlugin({
            manifest: require(manifest),
            // context: config.DLL_OUTPUT_PATH,
        });
    }).concat([
        // new CopyWebpackPlugin([{from: 'string', to: 'string'}]),
        // new ExtractTextPlugin('[name]-[contenthash].css', {allChunks: true}),
        // new HtmlWebpackPlugin({
        //     template: config.path_join(config.HTML_TEMPLATE_PATH, 'index.html'),
        // }),
    ]),

    // resolve: {
    //     alias: {}, // See https://webpack.js.org/configuration/resolve/#resolve-alias
    // },

    externals: {
        // Webpack can pack up lodash, but can't compress it, or throw an exception when using.
        lodash: 'lodash',
        _: 'lodash',
    },
};

module.exports = webpack_base_config;
