
## VS Code User Setting

#### Setting.json
```json
{
    // "bookmarks.saveBookmarksBetweenSessions": true,
    // "bookmarks.navigateThroughAllFiles": true,

    // "clang.completion.triggerChars": [
    //     ".", ":", ">",
    //     "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    //     "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    //     "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
    //     "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    // ],

    "[c]": {
        "editor.insertSpaces": false,
        "editor.quickSuggestions": true
    },

    "[cpp]": {
        "editor.insertSpaces": false,
        "editor.quickSuggestions": true
    },

    "debug.allowBreakpointsEverywhere": true,
    "debug.openExplorerOnEnd": true,

    "diffEditor.ignoreTrimWhitespace": false,

    "editor.rulers": [
        80, 100, 120
    ],
    "editor.wordWrap": "on",
    "editor.mouseWheelZoom": true,
    "editor.minimap.enabled": true,
    "editor.renderIndentGuides": true,
    "editor.useTabStops": true,
    "editor.detectIndentation": true,
    "editor.tabCompletion": true,
    "editor.renderWhitespace": "boundary",

    "explorer.openEditors.visible": 0,
    "extensions.autoUpdate": true,

    "files.encoding": "utf8",
    "files.eol": "\n",
    "files.trimTrailingWhitespace": true,

    "go.buildFlags": ["-race"],
    "go.formatOnSave": true,
    "go.formatTool": "goreturns",
    //"go.lintTool": "gometalinter",

    "html.format.indentInnerHtml": true,

    "projectManager.svn.baseFolders": [],
    "projectManager.git.baseFolders": [],
    "projectManager.git.maxDepthRecursion": 4,
    "projectManager.openInNewWindow": true,
    "projectManager.showProjectNameInStatusBar": true,

    "python.autoComplete.addBrackets": true,
    "python.jediPath": "C:\\Users\\Administrator\\AppData\\Roaming\\Jedi", // For Windows
    //"python.jediPath": "~/Library/Caches/Jedi",  // For Unix/Linux/Mac
    "python.linting.maxNumberOfProblems": 120,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--max-line-length=120",
        "-d C0103,C0111,C0411,C0413,E1123,W0613,W0621,W0622,W0703,W1202"
    ],
    "python.linting.pep8Enabled": true,
    "python.linting.pep8Args": [
        "--max-line-length=120",
        "--ignore=E125,E126,E127,E128,E129,E221,E265,E309,E401,E402,E731"
    ],
    "python.unitTest.nosetestsEnabled": false,
    "python.unitTest.nosetestArgs": [],

    "terminal.integrated.cursorBlinking": true,
    "terminal.integrated.scrollback": 10000,
    "terminal.integrated.setLocaleVariables": true,

    "vsicons.presets.angular": false,
    "vsicons.dontShowNewVersionMessage": true,

    "window.openFoldersInNewWindow": "on",
    "window.title": "${rootPath}${separator}${activeEditorMedium}${dirty}",

    "workbench.editor.enablePreview": false,
    "workbench.editor.enablePreviewFromQuickOpen": false,
    "workbench.iconTheme": "vscode-icons",
    "workbench.welcome.enabled": false
}
```

#### locale.json
```json
{
    "locale": "en"
}
```

#### keybindings.json
```json
[
    { "key": "ctrl+l", "command": "HookyQR.beautifyFile"},
    { "key": "shift+alt+e", "command": "projectManager.editProjects"},
    { "key": "shift+alt+s", "command": "projectManager.saveProject"},
    { "key": "shift+alt+o", "command": "projectManager.listProjectsNewWindow" },

    { "key": "ctrl+f", "command": "actions.find" },
    { "key": "ctrl+a", "command": "editor.action.selectAll" },
    { "key": "ctrl+x", "command": "editor.action.clipboardCutAction", "when": "editorTextFocus" },
    { "key": "ctrl+c", "command": "editor.action.clipboardCopyAction", "when": "editorTextFocus" },
    { "key": "ctrl+v", "command": "editor.action.clipboardPasteAction", "when": "editorTextFocus" }
]
```


## Installed Packages

Install a Package
1. `Ctrl + Alt + P` to open the command palette.
2. Type `ext install PACKAGE_NAME` and `Enter`.

#### Common Packages
```shell
#alefragnani.Bookmarks
formulahendry.code-runner
#anseki.vscode-color
robertohuertasm.vscode-icons
ybaumes.highlight-trailing-white-spaces
#JerryHong.autofilename
#christian-kohler.path-intellisense
#IBM.output-colorizer
#seanmcbreen.Spell
#vscodevim.vim                           # It will lead to 'editor.useTabStops' to be invalid.
#steve8708.Align                         # Align text

akamud.vscode-caniuse                    # Can I Use
christian-kohler.npm-intellisense        # npm
#searKing.preview-vscode                 # Preview　Markdown, HTML, CSS, Image, etc.
#flowtype.flow-for-vscode                # FlowType
#vsmobile.vscode-react-native            # React Native

#dzannotti.vscode-babel-coloring         # Babel ES6/ES7/JSX
#formulahendry.auto-close-tag            # HTML/XML
#formulahendry.auto-rename-tag           # HTML/XML
#HookyQR.beautify                        # Format JS, JSON, CSS, HTML
#DotJoshJohnson.xml                      # Format XML
#ms-vscode.cpptools                      # C/C++
#mitaki28.vscode-clang                   # C/C++ Completion and Diagnostic
#austin.code-gnu-global                  # C++ Intellisense
#pranaygp.vscode-css-peek                # CSS
abierbaum.vscode-file-peek               # JS/TypeScript
#msjsdiag.debugger-for-chrome            # JS Debuger
#dbaeumer.vscode-eslint                  # JS Lint
#chenxsan.vscode-standardjs              # JS Standard Style
#eg2.vscode-npm-script                   # Node NPM
donjayamanne.githistory                  # Git log
#codezombiech.gitignore                  # Git ignore
lukehoban.Go                             # Golang
#abusaidm.html-snippets                  # HTML 5
#redhat.java                             # Java
#georgewfraser.vscode-javac              # Java
#donjayamanne.javadebugger               # Java Debugger
alefragnani.project-manager              # Project Manager
#donjayamanne.python                     # Python
#humao.rest-client                       # Restful Client
#hcyang.ctags                            # CTags
#saviorisdead.RustyCode                  # Rust
#cssho.vscode-svgviewer                  # SVG Viewer
#Togusa09.tmlanguage                     # YAML
```

#### For Windows
```
fantasytyx.tortoise-svn
ms-vscode.PowerShell
```

### Install the commands depended on by the plugins above.

#### For ESLint
```
npm install -g eslint
```

#### For python
```
pip install pylint nose pep8 jedi
```

#### For Go
```
go get -v github.com/nsf/gocode
go get -v github.com/rogpeppe/godef
go get -v github.com/zmb3/gogetdoc
go get -v github.com/golang/lint/golint
go get -v github.com/lukehoban/go-outline
go get -v sourcegraph.com/sqs/goreturns
go get -v golang.org/x/tools/cmd/gorename
go get -v github.com/tpng/gopkgs
go get -v github.com/newhook/go-symbols
go get -v golang.org/x/tools/cmd/guru
go get -v github.com/cweill/gotests/...
```

#### For C/C++
```shell
$ sudo yum install clang
$ sudo apt-get install clang
```

#### For RustyCode
```shell
$ cargo install racer
$ cargo install rustsym
$ cargo install rustfmt
```
