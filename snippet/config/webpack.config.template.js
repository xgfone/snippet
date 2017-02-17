import * as path from 'path';
import * as webpack from 'webpack';

const ROOT_DIR = __dirname;

const config = {
    cache: true,
    target: 'web', // or 'node', (compiler) => {...}

    // The home directory for webpack.
    // The entry and module.rules.loader option is resolved relative to this directory.
    context: ROOT_DIR,

    // The Entry Points
    entry: {},

    // The output
    output: {
        path: path.resolve(ROOT_DIR, 'dist'),
        publicPath: '/static/', // http://static.example.com/
        filename: '[name]-[chunkhash].js',
        // chunkFilename: '[name]-[chunkhash].js',

        // library: '[name]',
        // libraryTarget: 'var', // umd, umd2, commonjs, commonjs2, commonjs-module, amd, this, var, assign, window, global, jsonp

        // crossOriginLoading: false | "anonymous" | "use-credentials",
    },

    // Loaders
    // For example:
    //     module: {
    //         rules: [
    //             {
    //                 test: /\.(json)$/,
    //                 exclude: /node_modules/,
    //                 loader: 'json-loader',
    //             },
    //             {
    //                 test: /\.(js)$/,
    //                 exclude: /node_modules/,
    //                 use: [
    //                     {loader: 'babel-loader'},
    //                     {loader: 'eslint-loader'},
    //                 ]
    //             },
    //             {
    //                 test: /\.(?:png|jpe?g|git)$/,
    //                 use: [
    //                     {
    //                         loader: 'url-loader',
    //                         options: {
    //                             limit: 8192,
    //                         },
    //                     },
    //                 ]
    //             },
    //         ],
    //     },
    module: {
        rules: [
            {
                // The Shortcut Options.
                test: Condition,    // shortcut to Rule.resource.test.
                include: Condition, // shortcut to Rule.resource.include.
                exclude: Condition, // shortcut to Rule.resource.exclude.
                loader: string,     // shortcut to Rule.use: [ { loader } ].

                // Only the resources which match the conditions will are handled by the loaders.
                // The condition is one of a string, RegExp, function, array of conditions,
                // or object all whose properties must match.
                resource: {
                    test: Condition,
                    include: Condition,
                    exclude: Condition,
                    and: [Condition],
                    or: [Condition],
                    not: Condition,
                },

                use: [
                    {
                        loader: 'name-loader',
                        options: "string" | {}, // The option of the loader.
                    },
                    {
                        loader: 'name-loader',
                        options: "string" | {}, // The option of the loader.
                    },
                ],

                // issuer: {
                //     test: Condition,
                //     include: [Condition],
                //     exclude: [Condition],
                //     and: [Condition],
                //     or: [Condition],
                //     not: Condition,
                // },
                // oneof: [], // Only the first matching Rule is used when the Rule matches.
                // rules: [], // Use all of these nested rules when they match.
                // parser: {}, // See https://webpack.js.org/configuration/module/#rule-parser
                // enforce: 'pre' | 'post',
            },
        ],

        // Don't parse this module.
        // Ignored files should not have calls to import, require, define or any other importing mechanism.
        // noParse: RegExp | [RegExp], // Such as [/jquery|lodash/, /bootstrap/].
    },

    // list of additional plugins
    // For example:
    //     plugins: [
    //         new webpack.DefinePlugin({
    //             'process.env.NODE_ENV': JSON.stringify('production'),
    //         }),
    //         new webpack.optimize.UglifyJsPlugin(),
    //     ],
    plugins: [],

    // Configure how modules are resolved.
    // For example, when calling import "lodash" in ES2015, the resolve options
    // can change where webpack goes to look for "lodash" (see modules).
    resolve: {
        // alias: {}, // See https://webpack.js.org/configuration/resolve/#resolve-alias
        // modules: ['node_modules'], // The absolute or relative paths can both be used.
        // extensions: ['.js', '.json'],
        // plugins: [new DirectoryNamedWebpackPlugin()],
    },

    // Don't follow/bundle these modules, but request them at runtime from the environment.
    // Prevent bundling of certain imported packages and instead retrieve these external packages at runtime.
    externals: {
        // jquery: 'jQuery',
        // $: 'jQuery',
        // lodash: {
        //     amd: 'lodash',
        //     commonjs: 'lodash',
        //     commonjs2: 'lodash',
        //     root: '_', // indicates global variable, which is the default setting.
        // }
    },

    // How Source Maps are generated.
    // 'cheap-module-source-map' or 'source-map' for production.
    // 'cheap-module-eval-source-map' and 'eval-source-map' for development.
    devtool: 'cheap-module-source-map',

    // For development.
    devServer: {
        port: 8000,
        host: '0.0.0.0',
        publicPath: '/public/',
        contentBase: [path.join(ROOT_DIR, "public")],

        watchContentBase: true,
        watchOptions: {
            aggregateTimeout: 3000, // 1s
            ignored: RegExp | string, // Such as /node_modules/, "node_modules/**/*.js".
            poll: 3000 // Check for changes every 3 seconds. Or true.
        },

        hot: true,
        colors: true,
        inline: true, // Livereload
        historyApiFallback: true,

        // clientLogLevel: 'info',
        // compress: true,
        // headers: {'X-Custom-Foo': 'Foo'},
        // https: true, // See https://webpack.js.org/configuration/dev-server/#devserver-https
        // setup: (app) => {app.get('/some/path', (req, res) => {...});},
    },

    ///////////////////////////////////////////////////////////////////////////
    /// Other Settings

    /// lets you precisely control what bundle information gets displayed
    /// See https://webpack.js.org/configuration/stats
    // stats: 'normal',

    // performance: {
    //     maxAssetSize: 250000,
    //     maxAssetSize: 250000,
    //     assetFilter: function(assetFilename) {
    //         return assetFilename.endsWith('.css') || assetFilename.endsWith('.js');
    //     }
    // },

    /// Others
    // bail: false,
    // profile: true,
};

export default config;
