const path = require('path');
const webpack = require('webpack');
const config = require('./config');

const HtmlWebpackPlugin = require('html-webpack-plugin');
// const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

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
            {
                test: /\.(json)$/,
                exclude: /node_modules/,
                loader: 'json-loader',
            }, {
                test: /\.(less|css)$/,
                loader: ExtractTextPlugin.extract('style', 'css?module&localIdentName=[hash:base64:7]!less'),
            }, {
                test: /\.(jsx?)$/,
                exclude: /node_modules/,
                include: config.resolve_path('src'),
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            cacheDirectory: true,
                            presets: ['es2015'],
                            plugins: ['transform-runtime'],
                        }
                    },
                    {loader: 'eslint-loader'},
                ]
            }, {
                test: /\.(?:png|jpe?g|git)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                        },
                    },
                ]
            },
        ],
    },

    plugins: config.DLL_NAMES.map((name) => {
        const manifest = config.resolve_dll(name + '-manifest.json');
        return new webpack.DllReferencePlugin({
            manifest: require(manifest),
            // context: config.DLL_OUTPUT_PATH,
        });
    }).concat([
        new webpack.optimize.CommonsChunkPlugin({
            name: 'common',
            minChunks: 3,
        }),
        new ExtractTextPlugin('[name]-[contenthash].css', {allChunks: true}),
        // new CopyWebpackPlugin([{from: 'string', to: 'string'}]),
        // new HtmlWebpackPlugin({
        //     template: config.path_join(config.HTML_TEMPLATE_PATH, 'index.html'),
        // }),
    ]),

    resolve: {
        root: config.resolve_path('src'),
        alias: {}, // See https://webpack.js.org/configuration/resolve/#resolve-alias
    },

    externals: {
        // Webpack can pack up lodash, but can't compress it, or throw an exception when using.
        lodash: 'lodash',
        _: 'lodash',
    },
};

module.exports = webpack_base_config;
