# Atom Packages

## Customized Packages

### Commont
```
#activate-power-mode
atom-beautify
color-picker
linter
merge-conflicts
minimap
minimap-cursorline
pigments
script
vim-mode-plus
```

### C/C++
```
autocomplete-clang
clang-format
gpp-compiler
#language-cpp14
#linter-clang
#linter-cpplint
linter-gcc
switch-header-source
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
```
language-javascript-jsx
#linter-js-standard
#linter-js-standard-jsx
```

### Markdown
```
markdown-writer
language-markdown
```

### Python
```
autocomplete-python
python-tools
linter-python-pep257
linter-python-pep8
linter-python-pyflakes
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
  "autocomplete-python":
    useKite: false
    useSnippets: "required"
  core:
    closeEmptyWindows: false
    disabledPackages: [
      "activate-power-mode"
      "language-gfm"
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
  "go-config":
    gopath: "~/go"
  "go-plus":
    currentPanelHeight: "19.5364238410596vh"
  linter: {}
  "linter-python-pep257":
    ignoreCodes: "D100, D101, D102, D103, D104, D105, D209"
  "linter-python-pep8":
    ignoreErrorCodes: "E125, E126, E127, E128, E129, E221, E265, E401"
  "markdown-writer":
    fileExtension: ".md"
  minimap:
    plugins:
      cursorline: true
      cursorlineDecorationsZIndex: 0
  qolor:
    fourBorders: true
  "vim-mode-plus":
    clearMultipleCursorsOnEscapeInsertMode: true
    highlightSearch: true
    incrementalSearch: true
    useClipboardAsDefaultRegister: true
```