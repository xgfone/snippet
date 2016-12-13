# Atom Packages

## Customized Packages

### Commont
```shell
#activate-power-mode
atom-beautify
color-picker
linter
merge-conflicts
minimap
open-path
pigments
project-viewer
repl
script
platformio-atom-ide-terminal  # Replace terminal-plus
#terminal-plus
vim-mode-plus
```

### Git
```shell
git-log
#git-plus
#git-time-machine
#git-control
```

------

### C/C++
```shell
switch-header-source
autocomplete-clang
clang-format
gpp-compiler
linter-gcc
#language-cpp14
#linter-clang
#linter-cpplint
```

### Go
```
autocomplete-go
builder-go
go-config
go-debug
go-get
go-outline
go-plus
godoc
gofmt
gometalinter-linter
gorename
navigator-go
tester-go
```

### JS
```shell
linter-eslint
language-javascript-jsx
#linter-js-standard
#linter-js-standard-jsx
```

**Configure**
```shell
$ npm i -g eslint
```

### Python
```shell
autocomplete-python
#python-tools
#linter-python-pep257
linter-python-pep8
#linter-python-pyflakes
```

**Configuration**
```shell
pip install pep8 pep257 pylint
```

### Markdown
```shell
language-markdown
```

### SQL
```
qolor
```


## Core Packages
```
about
archive-view
autocomplete-atom-api
autocomplete-css
autocomplete-html
autocomplete-plus
autocomplete-snippets
autoflow
autosave
background-tips
bookmarks
bracket-matcher
command-palette
deprecation-cop
dev-live-reload
encoding-selector
exception-reporting
find-and-replace
fuzzy-finder
git-diff
go-to-line
grammer-selector
image-view
incompatible-packages
keybinding-resolver
language-c
language-clojure
language-coffee-script
language-csharp
language-css
language-gfm
language-git
language-go
language-html
language-hyperlink
language-java
language-javascript
language-json
language-less
language-make
language-mustache
language-objective-c
language-perl
language-php
language-property-list
language-python
language-ruby
language-ruby-on-rails
language-sass
language-shellscript
language-source
language-sql
language-text
language-todo
language-toml
language-xml
language-yaml
line-ending-selector
link
markdown-preview
metrics
notifications
open-on-github
package-generator
settings-view
snippets
spell-check
status-bar
styleguide
symbols-view
tabs
timecop
tree-view
update-package-dependencies
welcome
whitespace
wrap-guide
```

------

# Configuration

## `config.cson`
```cson
"*":
  #"autocomplete-go":
  #  snippetMode: "nameAndType"
  #"autocomplete-python":
  #  useKite: false
  #  useSnippets: "required"
  core:
    closeEmptyWindows: false
    disabledPackages: [
      "activate-power-mode"
    ]
    openEmptyEditorOnStart: false
    telemetryConsent: "limited"
  editor:
    showIndentGuide: true
    showInvisibles: true
    tabLength: 4
    zoomFontWhenCtrlScrolling: true
  "exception-reporting":
    userId: "9b9a29d3-8603-6a78-e2ca-83f27e7b8d16"
  #"go-config":
  #  gopath: "~/go"
  #gofmt:
  #  formatTool: "goreturns"
  linter: {}
  #"linter-python-pep257":
  #  ignoreCodes: "D100, D101, D102, D103, D104, D105, D209"
  #"linter-python-pep8":
  #  ignoreErrorCodes: "E125, E126, E127, E128, E129, E221, E265, E401"
  "markdown-preview":
    useGitHubStyle: true
  #"markdown-writer":
  #  fileExtension: ".md"
  minimap:
    plugins:
      cursorline: true
      cursorlineDecorationsZIndex: 0
  "project-viewer":
    autohide: true
    convertOldData: false
    hideHeader: true
    keepContext: true
    statusBarVisibility: true
  #qolor:
  #  fourBorders: true
  "platformio-ide-terminal":  # Replace terminal-plus
    toggles:
      autoClose: true
  #"terminal-plus":
  #  toggles:
  #    autoClose: true
  "vim-mode-plus":
    clearMultipleCursorsOnEscapeInsertMode: true
    highlightSearch: true
    incrementalSearch: true
    useClipboardAsDefaultRegister: true
  welcome:
    showOnStartup: false
```

## `keymap.cson`
```cson
'atom-text-editor':
  'ctrl-a': 'core:select-all'
  'ctrl-x': 'core:cut'
  'ctrl-c': 'core:copy'
  'ctrl-v': 'core:paste'

'atom-workspace':
  'ctrl-a': 'core:select-all'
  'ctrl-x': 'core:cut'
  'ctrl-c': 'core:copy'
  'ctrl-v': 'core:paste'
```
