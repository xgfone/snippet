
## VS Code User Setting

#### Setting.json
```json
{
    "bookmarks.saveBookmarksBetweenSessions": true,
    "bookmarks.navigateThroughAllFiles": true,

    "editor.rulers": [
        80, 100, 120
    ],
    "editor.wordWrap": false,
    "editor.mouseWheelZoom": true,
    "editor.renderIndentGuides": true,
    "editor.wrappingColumn": 140,

    "extensions.autoUpdate": true,

    "files.eol": "\n",
    "files.trimTrailingWhitespace": true,

    "go.formatOnSave": true,
    "go.formatTool": "goreturns",

    "python.linting.maxNumberOfProblems": 120,
    "python.linting.pylintArgs": [
        "-d C0111,W0703"
    ],

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
gitignore
Go
html-snippets
vscode-javac
vscode-JS-CSS-HTML-formatter
markdown-pdf
prettify-json
project-manager
python
rest-client
RustyCode
Spell
vscode-svgviewer
vim
vscode-icons
xml
```

#### For Windows

```
tortoise-svn
PowerShell
```
