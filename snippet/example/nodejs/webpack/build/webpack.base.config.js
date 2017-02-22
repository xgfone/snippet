const path = require('path');
const webpack = require('webpack');
const config = require('./config');

// const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const loaders = [];
if (config.ESLINT) {
    loaders.push({
        test: /\.(jsx?)$/,
        exclude: /node_modules/,
        enforce: 'pre',
        loader: 'eslint-loader',
        options: {
            configFile: config.resolve_path('.eslintrc.js'),
        },
    });
}

const webpack_base_config = {
    cache: true,
    target: config.TARGET,

    // The home directory for webpack.
    // The entry and module.rules.loader option is resolved relative to this directory.
    context: config.ROOT,

    // The Entry Points
    entry: config.ENTRY,

    // The output
    output: {
        path: config.OUTPUT_PATH,
        publicPath: config.OUTPUT_PUBLIC_PATH,
        filename: '[name]-[chunkhash].js',
        chunkFilename: '[name]-[chunkhash].js',
        //crossOriginLoading: false | "anonymous" | "use-credentials",
    },

    // The Loaders
    module: {
        rules: [
            ...loaders,
            {
                test: /\.(jsx?)$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            babelrc: true,
                            cacheDirectory: true,
                            presets: ['react', ['es2015', {'modules': false}], 'es2016', 'es2017'],
                            plugins: ['transform-runtime'],
                        }
                    }
                ]
            // }, {  // ExtractTextPlugin doesn't work under webpack 2. Wait 2.0.0 to be released.
            //     test: /\.(css|less)$/,
            //     loader: ExtractTextPlugin.extract({
            //         fallback: 'style-loader',
            //         use: [
            //             {
            //                 loader: 'css-loader',
            //                 options: {
            //                     modules: true,
            //                     minimize: true,
            //                     importLoaders: 1,
            //                     localIdentName: '[hash:base64:7]',
            //                 }
            //             },
            //             'less-loader',
            //         ]
            //     }),
            }, {
                test: /\.(png|jpe?g|git)$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                            // For file-loader
                            name: '[name]-[hash].[ext]',
                            outputPath: config.OUTPUT_PATH,
                            publicPath: config.OUTPUT_PUBLIC_PATH,
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
            names: ['common', 'manifest'],
            minChunks: 2,
        }),
        // new ExtractTextPlugin({
        //     filename: '[name]-[contenthash].css',
        //     options: {
        //         allChunks: true,
        //     }
        // }),
        // new CopyWebpackPlugin([{from: 'string', to: 'string'}]),
        new HtmlWebpackPlugin({
            template: config.path_join(config.HTML_TEMPLATE_PATH, 'index.html'),
        }),
    ]),

    resolve: {
        modules: ['node_modules', config.APP_ROOT],
        extensions: ['.js', '.json', '.jsx', '.css'],
        alias: {  // See https://webpack.js.org/configuration/resolve/#resolve-alias
        },
    },

    externals: {
    },
};

module.exports = webpack_base_config;
