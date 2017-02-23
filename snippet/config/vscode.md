
## VS Code User Setting

#### Setting.json
```json
{
    // "bookmarks.saveBookmarksBetweenSessions": true,
    // "bookmarks.navigateThroughAllFiles": true,

    "debug.allowBreakpointsEverywhere": true,
    "debug.openExplorerOnEnd": true,

    "diffEditor.ignoreTrimWhitespace": false,

    "editor.rulers": [
        80, 100, 120
    ],
    "editor.wordWrap": true,
    "editor.mouseWheelZoom": true,
    "editor.renderIndentGuides": true,
    "editor.wrappingColumn": 140,
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
    "go.lintTool": "gometalinter",

    "html.format.indentInnerHtml": true,

    "projectManager.openInNewWindow": true,
    "projectManager.git.baseFolders": [],
    "projectManager.svn.baseFolders": [],

    "python.autoComplete.addBrackets": true,
    "python.jediPath": "C:\\Users\\Administrator\\AppData\\Roaming\\Jedi", // For Windows
    //"python.jediPath": "/home/USER_NAME/.Jedi",  // For Unix/Linux/Mac
    "python.linting.maxNumberOfProblems": 120,
    "python.linting.pylintEnabled": false,
    "python.linting.pylintArgs": [
        "-d C0103,C0111,E1123,W0703,W1202"
    ],
    "python.linting.pep8Enabled": true,
    "python.linting.pep8Args": [
        "--max-line-length=140",
        "--ignore=E125,E126,E127,E128,E129,E221,E265,E309,E401,E402"
    ],
    "python.unitTest.nosetestsEnabled": true,
    "python.unitTest.nosetestArgs": [],

    "terminal.integrated.cursorBlinking": true,
    "terminal.integrated.scrollback": 10000,
    "terminal.integrated.setLocaleVariables": true,

    "vsicons.presets.angular": false,

    "window.openFoldersInNewWindow": "on",
    "window.showFullPath": true,

    "workbench.editor.enablePreview": false,
    "workbench.editor.enablePreviewFromQuickOpen": false,
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
    { "key": "shift+alt+e", "command": "projectManager.editProjects"},
    { "key": "shift+alt+s", "command": "projectManager.saveProject"},
    { "key": "shift+alt+o", "command": "projectManager.listProjectsNewWindow" },
    { "key": "ctrl+a", "command": "editor.action.selectAll" },
    { "key": "ctrl+f", "command": "actions.find" },
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
alefragnani.Bookmarks
formulahendry.code-runner
#anseki.vscode-color
robertohuertasm.vscode-icons
JerryHong.autofilename
christian-kohler.path-intellisense
IBM.output-colorizer
#seanmcbreen.Spell
#vscodevim.vim                          # It will lead to 'editor.useTabStops' to be invalid.
#steve8708.Align                        # Align text

akamud.vscode-caniuse                   # Can I Use
#christian-kohler.npm-intellisense      # npm
#vsmobile.vscode-react-native           # React Native

#dzannotti.vscode-babel-coloring        # Babel ES6/ES7/JSX
formulahendry.auto-close-tag            # HTML/XML
formulahendry.auto-rename-tag           # HTML/XML
HookyQR.beautify                        # Format JS, JSON, CSS, HTML
DotJoshJohnson.xml                      # Format XML
ms-vscode.cpptools                      # C/C++
pranaygp.vscode-css-peek                # CSS
abierbaum.vscode-file-peek              # JS/TypeScript
#msjsdiag.debugger-for-chrome           # JS Debuger
#dbaeumer.vscode-eslint                 # JS Lint
#chenxsan.vscode-standardjs             # JS Standard Style
#eg2.vscode-npm-script                  # Node NPM
donjayamanne.githistory                 # Git log
codezombiech.gitignore                  # Git ignore
lukehoban.Go                            # Golang
#abusaidm.html-snippets                 # HTML 5
#redhat.java                            # Java
#georgewfraser.vscode-javac             # Java
#donjayamanne.javadebugger              # Java Debugger
alefragnani.project-manager             # Project Manager
donjayamanne.python                     # Python
#humao.rest-client                      # Restful Client
#hcyang.ctags                           # CTags
#saviorisdead.RustyCode                 # Rust
#cssho.vscode-svgviewer                 # SVG Viewer
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

#### For RustyCode
```shell
$ cargo install racer
$ cargo install rustsym
$ cargo install rustfmt
```
