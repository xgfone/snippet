
### ctags
ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .

### cscope
```shell
# -R: 在生成索引文件时，搜索子目录树中的代码
# -b: 只生成索引文件，不进入cscope的界面
# -k: 在生成索引文件时，不搜索/usr/include目录
# -q: 生成cscope.in.out和cscope.po.out文件，加快cscope的索引速度
$ cscope -Rbkq
```

```shell
#!/bin/sh

find . -name "*.h" -o -name "*.c"-o -name "*.cc" -o -name "*.cpp" -o -name "*.hpp" > cscope.files
cscope -bkq -i cscope.files
ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .
```
