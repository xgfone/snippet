
## VS Code User Setting

#### Setting.json
```json
{
    // "bookmarks.saveBookmarksBetweenSessions": true,
    // "bookmarks.navigateThroughAllFiles": true,

    "[c]": {
        "editor.insertSpaces": false
    },

    "[cpp]": {
        "editor.insertSpaces": false
    },

    "C_Cpp.intelliSenseEngine": "Default",

    "debug.allowBreakpointsEverywhere": true,
    "debug.openExplorerOnEnd": true,

    "diffEditor.ignoreTrimWhitespace": false,

    "editor.rulers": [
        80, 100, 120
    ],
    "editor.wordWrap": "on",
    "editor.mouseWheelZoom": true,
    "editor.minimap.enabled": true,
    "editor.minimap.maxColumn": 80,
    "editor.renderIndentGuides": true,
    "editor.useTabStops": true,
    "editor.detectIndentation": true,
    "editor.tabCompletion": true,
    "editor.renderWhitespace": "boundary",

    "emmet.useNewEmmet": true,

    "explorer.openEditors.visible": 0,
    "extensions.autoUpdate": true,

    "files.encoding": "utf8",
    "files.eol": "\n",
    "files.autoGuessEncoding": true,
    "files.trimTrailingWhitespace": true,

    "go.buildFlags": ["-race"],
    "go.formatOnSave": true,
    "go.formatTool": "goreturns",
    //"go.lintTool": "gometalinter",

    "html.format.indentInnerHtml": true,

    "projectManager.svn.baseFolders": [],
    "projectManager.git.baseFolders": [],
    "projectManager.git.maxDepthRecursion": 4,
    "projectManager.showProjectNameInStatusBar": true,

    "python.autoComplete.addBrackets": true,
    // "python.jediPath": "C:\\Users\\Administrator\\AppData\\Roaming\\Jedi",
    // "python.jediPath": "~/Library/Caches/Jedi",
    "python.linting.maxNumberOfProblems": 120,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--max-line-length=120",
        "-d C0103,C0111,C0411,C0413,E1123,W0603,W0613,W0621,W0622,W0703,W1202"
    ],
    "python.linting.pep8Enabled": true,
    "python.linting.pep8Args": [
        "--max-line-length=120",
        "--ignore=E125,E126,E127,E128,E129,E221,E265,E309,E401,E402,E731"
    ],
    "python.unitTest.nosetestsEnabled": false,
    "python.unitTest.nosetestArgs": [],

    "terminal.integrated.cursorStyle": "line",
    "terminal.integrated.cursorBlinking": true,
    "terminal.integrated.scrollback": 10000,
    "terminal.integrated.setLocaleVariables": true,

    "vim.leader": ";",
    "vim.useSystemClipboard": true,
    "vim.easymotion": true,
    "vim.hlsearch": true,

    "vsicons.presets.angular": false,
    "vsicons.dontShowNewVersionMessage": true,

    "window.openFoldersInNewWindow": "on",
    "window.title": "${rootPath}${separator}${activeEditorMedium}${dirty}",

    "workbench.editor.enablePreview": false,
    "workbench.editor.enablePreviewFromQuickOpen": false,
    "workbench.iconTheme": "vscode-icons",
    "workbench.colorTheme": "Quiet Light"
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
#JerryHong.autofilename
#IBM.output-colorizer
#seanmcbreen.Spell
#steve8708.Align                         # Align text
#humao.rest-client                       # Restful Client
#searKing.preview-vscode                 # Preview Markdown, HTML, CSS, Image, etc.
#vscodevim.vim                           # It will lead to 'editor.useTabStops' to be invalid.
#anseki.vscode-color                     # Helper with GUI to generate color codes.
#christian-kohler.path-intellisense
formulahendry.code-runner
robertohuertasm.vscode-icons
ybaumes.highlight-trailing-white-spaces
alefragnani.project-manager              # Project Manager
CoenraadS.bracket-pair-colorizer         # A customizable extension for colorizing matching brackets.


## Format
HookyQR.beautify                         # Format JS, JSON, CSS, HTML
DotJoshJohnson.xml                       # Format XML


## Git
#codezombiech.gitignore                  # Git ignore
donjayamanne.githistory                  # Git log
eamodio.gitlens                          # Supercharge Visual Studio Code's Git capabilities.
howardzuo.vscode-gitk                    # Show git commit log for selected source code information.
pprice.better-merge                      # Improved git merge conflict support.
lamartire.git-indicators                 # Atom like git counters.


## Python
donjayamanne.python                      # Python


## Go
lukehoban.Go                             # Golang


## C/C++
ms-vscode.cpptools                       # C/C++
#mitaki28.vscode-clang                   # C/C++ Completion and Diagnostic
#austin.code-gnu-global                  # C++ Intellisense


## JS/Node
christian-kohler.npm-intellisense        # npm
eg2.vscode-npm-script                    # Node NPM
dzannotti.vscode-babel-coloring          # Babel ES6/ES7/JSX
abierbaum.vscode-file-peek               # JS/TypeScript
#dbaeumer.vscode-eslint                  # JS Lint
#chenxsan.vscode-standardjs              # JS Standard Style

#donjayamanne.jquerysnippets             # Over 130 jQuery Code Snippets for JavaScript code.
#flowtype.flow-for-vscode                # FlowType
#vsmobile.vscode-react-native            # React Native


## HTML/CSS
ecmel.vscode-html-css                    # CSS support for HTML documents.
mkaufman.htmlhint                        # Integrates the HTMLHnt static analysis tool into VS Code.
pranaygp.vscode-css-peek                 # CSS
abusaidm.html-snippets                   # HTML 5
#formulahendry.auto-close-tag            # HTML/XML
#formulahendry.auto-rename-tag           # HTML/XML


## Browser
#akamud.vscode-caniuse                   # Can I Use
#msjsdiag.debugger-for-chrome            # JS Debuger


## Rust
#saviorisdead.RustyCode                  # Rust


## Java
#redhat.java                             # Java
#georgewfraser.vscode-javac              # Java
#donjayamanne.javadebugger               # Java Debugger


## SVG
#cssho.vscode-svgviewer                  # SVG Viewer


## YAML
#Togusa09.tmlanguage                     # YAML


## Others
#hcyang.ctags                            # CTags
```

#### For Windows
```shell
fantasytyx.tortoise-svn
ms-vscode.PowerShell
ms-mssql.mssql                           # Develop Microsoft SQL Server, Azure SQL Database.
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
