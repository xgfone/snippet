
## Parser Generator

### Tools
##### ANTLR
    ANTLR (ANother Tool for Language Recognition) is a powerful parser generator for reading,
    processing, executing, or translating structured text or binary files.

- [GitHub Source](https://github.com/antlr/antlr4)
- [Official Website](http://www.antlr.org/)

##### Grako
    Grako (for "grammar compiler") takes a grammar in a variation of EBNF as input,
    and outputs a memoizing PEG/Packrat parser in Python.

- [Source](http://bitbucket.org/apalala/grako)

##### Ragel
    Ragel State Machine Compiler.

- [Github Source](https://github.com/colmnet/ragel)

##### Peg
    Peg, Parsing Expression Grammar, is an implementation of a Packrat parser generator.

- [Github Source](https://github.com/pointlander/peg)

##### Pigeon
    Command pigeon generates parsers in Go from a PEG grammar.

- [Github Source](https://github.com/PuerkitoBio/pigeon)
- [Introduction](http://0value.com/A-PEG-parser-generator-for-Go)

### Docs
- [Packrat & PEG](http://bford.info/packrat/)
- [PEG Wiki](https://en.wikipedia.org/wiki/Parsing_expression_grammar)

        PEG（Parsing Expression Grammar，解析表达式文法） 与 CFG（Context-Free Grammar，上下文无关文法）的基本
        区别就是：PEG 的选择符（choice operator）是顺序性的，即，对于 e1 | e2，如果 e1 成功匹配，e2 将会被忽略。
        这将不会产生二义性，也即是，PEG 通过顺序性避免了二义性（这在 CFG 中可能会产生二义性）。
