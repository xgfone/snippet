
## VS Code User Setting

#### Setting.json
```json
{
    "bookmarks.saveBookmarksBetweenSessions": true,
    "bookmarks.navigateThroughAllFiles": true,

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
    "editor.detectIndentation": false,
    "editor.tabCompletion": true,

    "extensions.autoUpdate": true,

    "files.encoding": "utf8",
    "files.eol": "\n",
    "files.trimTrailingWhitespace": true,

    "go.formatOnSave": true,
    "go.formatTool": "goreturns",
    "go.goroot": null,
    "go.gopath": null,

    "html.format.indentInnerHtml": true,

    "python.autoComplete.addBrackets": true,
    "python.linting.maxNumberOfProblems": 120,
    "python.linting.pylintArgs": [
        "-d C0111,W0703"
    ],
    "python.linting.pep8Enabled": true,
    "python.linting.pep8Args": [],
    "python.unitTest.nosetestsEnabled": true,
    "python.unitTest.nosetestArgs": [],

    "terminal.integrated.cursorBlinking": true,

    "workbench.editor.enablePreview": false,
    "workbench.editor.enablePreviewFromQuickOpen": false
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

```
beautify
Bookmarks
cpptools
code-runner
vscode-color
debugger-for-chrome
vscode-eslint
githistory
gitignore
Go
html-snippets
#vscode-javac
#vscode-JS-CSS-HTML-formatter
project-manager
python
rest-client
#RustyCode
#Spell
vscode-svgviewer
#vim
vscode-icons
xml
```

#### For Windows

```
tortoise-svn
PowerShell
```
