
## VS Code User Setting

#### Setting.json
```json
{
    // "bookmarks.saveBookmarksBetweenSessions": true,
    // "bookmarks.navigateThroughAllFiles": true,

    "debug.allowBreakpointsEverywhere": true,
    "debug.openExplorerOnEnd": true,

    "diffEditor.ignoreTrimWhitespace": false,

    // "docker.attachShellCommand.linuxContainer": "//bin/bash", // For windows

    "editor.rulers": [80, 100, 120],
    "editor.wordWrap": "on",
    "editor.mouseWheelZoom": false,
    "editor.minimap.enabled": false,
    "editor.minimap.maxColumn": 80,
    "editor.renderIndentGuides": true,
    "editor.useTabStops": true,
    "editor.tabCompletion": "on",
    "editor.renderWhitespace": "boundary",
    "editor.quickSuggestionsDelay": 2,
    "editor.fontSize": 24,
    "editor.fontFamily": "'Courier New', Consolas, monospace",

    "explorer.openEditors.visible": 0,

    "files.defaultLanguage": "python",
    "files.encoding": "utf8",
    "files.eol": "\n",
    "files.enableTrash": false,
    "files.autoGuessEncoding": true,
    "files.insertFinalNewline": true,
    "files.trimFinalNewlines": true,
    "files.trimTrailingWhitespace": true,
    "files.useExperimentalFileWatcher": true,

    "gitlens.advanced.messages": {
        "suppressResultsExplorerNotice": true,
        "suppressShowKeyBindingsNotice": true
    },
    // "gitlens.codeLens.scopes": [],
    "gitlens.keymap": "chorded",
    "gitlens.defaultDateStyle": "absolute",
    "gitlens.hovers.currentLine.over": "line",
    "gitlens.historyExplorer.enabled": false,

    "go.inferGopath": true,
    "go.useLanguageServer": true,
    "go.autocompleteUnimportedPackages": true,
    "go.gotoSymbol.ignoreFolders": ["vendor"],

    "html.format.indentInnerHtml": true,

    "markdown.preview.fontSize": 22,

    // "projectManager.svn.baseFolders": [],
    // "projectManager.git.baseFolders": [],
    // "projectManager.git.maxDepthRecursion": 4,
    // "projectManager.showProjectNameInStatusBar": true,

    "python.pythonPath": "ipython",
    "python.autoComplete.addBrackets": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pep8Enabled": true,

    "rest-client.fontSize": 22,

    "svgviewer.enableautopreview": true,

    "terminal.integrated.fontSize": 22,
    "terminal.integrated.cursorStyle": "line",
    "terminal.integrated.cursorBlinking": true,
    "terminal.integrated.scrollback": 10000,
    "terminal.integrated.setLocaleVariables": true,

    // "vim.leader": ";",
    // "vim.useSystemClipboard": true,
    // "vim.easymotion": true,
    // "vim.hlsearch": true,

    "vsicons.presets.angular": false,
    "vsicons.dontShowNewVersionMessage": true,

    "window.restoreWindows": "all",
    "window.openFoldersInNewWindow": "on",
    "window.title": "${rootPath}${separator}${activeEditorMedium}${dirty}",

    "workbench.editor.enablePreview": false,
    "workbench.editor.enablePreviewFromQuickOpen": false,
    "workbench.iconTheme": "vscode-icons",
    "workbench.colorTheme": "Atom One Light"
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

    { "key": "ctrl+shift+up", "command": "editor.action.insertCursorAbove", "when": "editorTextFocus" },
    { "key": "ctrl+shift+down", "command": "editor.action.insertCursorBelow", "when": "editorTextFocus" },

    { "key": "ctrl+k m", "command": "workbench.action.editor.changeLanguageMode" },

    { "key": "ctrl+a", "command": "editor.action.selectAll" },
    // { "key": "ctrl+f", "command": "actions.find" },
    // { "key": "ctrl+x", "command": "editor.action.clipboardCutAction", "when": "editorTextFocus" },
    // { "key": "ctrl+c", "command": "editor.action.clipboardCopyAction", "when": "editorTextFocus" },
    // { "key": "ctrl+v", "command": "editor.action.clipboardPasteAction", "when": "editorTextFocus" },

    // On deepin linux, the notify system will use the shortcut `Ctrl+`, so we will override it.
    { "key": "alt+`", "command": "workbench.action.terminal.toggleTerminal" },
    { "key": "alt+1", "command": "workbench.action.terminal.focusAtIndex1" },
    { "key": "alt+2", "command": "workbench.action.terminal.focusAtIndex2" },
    { "key": "alt+3", "command": "workbench.action.terminal.focusAtIndex3" },

    // Focus Next Terminal.
    { "key": "ctrl+tab", "command": "workbench.action.terminal.focusNext" },

    { "key": "ctrl+n", "command": "workbench.action.files.newUntitledFile", "when": "editorTextFocus && vim.active && vim.use<C-n>" }
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
#anseki.vscode-color                     # Helper with GUI to generate color codes.
#slevesque.vscode-hexdump                # Display a specified file in hexadecimal
#christian-kohler.path-intellisense
jinsihou.diff-tool
vscodevim.vim
formulahendry.code-runner
robertohuertasm.vscode-icons
ybaumes.highlight-trailing-white-spaces
patrys.vscode-code-outline               # A code outline tree provider for VSCode
alefragnani.project-manager              # Project Manager
CoenraadS.bracket-pair-colorizer         # A customizable extension for colorizing matching brackets.


# Theme
LeCrunchic.mariana-nord                  # Hybrid theme between Nord and Sublime's Mariana.
arcticicestudio.nord-visual-studio-code  # An arctic, north-bluish clean and elegant VS Code theme.


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


## SQL
formulahendry.vscode-mysql            # MySQL Management Tool
mtxr.sqltools                         # SQL


## Python
ms-python.python                      # Python


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
#hdg.live-html-previewer                 # Edit and preview HTML


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


## TOML
#bungcip.better-toml                     # TOML


## Others
#hcyang.ctags                            # CTags
#fallenwood.viml                         # VimL
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
