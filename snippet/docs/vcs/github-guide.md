
## 查看差别

#### 查看分支间的差别
```
https://github.com/rails/rails/compare/4-0-stable...3-2-stable
```

#### 查看与几天前的差别
```
https://github.com/rails/rails/compare/master@{7.day.ago}...master
```
注：指定期间可以使用四个时间单位：`day`、`week`、`month`、`year`。

#### 查看与指定日期之间的差别
```
https://github.com/rails/rails/compare/master@{2013-01-01}...master
```
注：如果指定日期与现在的差别过大，或者指定日期过于久远，则无法显示。

**说明：**
在显示前后改变差别时（即diff），默认情况下系统会将空格的不同也高亮显示，所以在空格有改动的情况下会难以阅读。这时只要在URL的末尾添加 `?w=1` 就可以不显示空格的差别。


## 获取 diff 格式与 patch 格式的文件
只需要在 `commit` 对象或 `Pull Request` 的URL的末尾添加 `.diff` 或 `.patch` 即可，如：
```
https://github.com/用户名/仓库名/commit/HASH值.diff
https://github.com/用户名/仓库名/pull/PULL号码.diff
```

## 评论
### 在 Pull Request 的 Conversation 中引用评论
选中想引用的评论然后按 `R` 键，被选择的部分就会自动以评论语法写入评论文本框。

注：这个快捷键在 `Issue` 中同样有效。

### 在评论中应用表情
在评论中输入 `:` (冒号)便会启动表情自动补全功能。只要输入几个与该表情相关的字母，系统就会为您筛选自动补全的对象。选择想要的表情，其相应代码（前后都有冒号的字符串）便会插入到文本框中。

注：可以在 http://www.emoji-cheat-sheet.com/ 查找可使用的表情。


## 在 Wiki 中显示侧边栏
所有 Wiki 页面都可以显示侧边栏。做法很很简单，只要创建名为 `_siderba` 的页面即可。`_siderbar` 页不会显示在 Pages 的页面一览中。在编辑各页面时页面下部会附加 `Siderbar` 段。用户可以在这里编辑侧边栏的内容。


## Pull Request
只要在想发起讨论时发送 Pull Request 即可，不必等代码最终完成。即便某个功能尚在开发之中，只要在 Pull Request 中附带一段简单代码让大家有个大体印象。

向发送过 Pull Request 的分支添加提交时，该提交会自动添加至已发送的 Pull Request 中。

为了防止开发到一半的 Pull Request 被误合并，一般都会在标题前加上 `[WIP]` 字样。`WIP` 是 `Work In Progress` 的简写，表示仍在开发过程中。等所有功能都完成之后，再消去这个前缀。


## 使用Github的开发流程
### 不 Fork 仓库的方法
1. 在 Github 上进行 Fork
2. 将 1 的仓库 Clone 到本地开发环境
3. 在本地环境中创建特性分支
4. 对特性分支进行代码修改并进行提交
5. 将特性分支 Push 到 1 的仓库中
6. 在 Github 上对 Fork 来源仓库发送 Pull Request

### Github Flow的流程——其实就是不 Fork仓库的方法。
1. 令 Master 分支时常保持可以部署的状态
2. 进行新的作业时要从 Master 分支创建新分支，新分支名要具有描述性
3. 在 2 新建的本地仓库分支中进行提交
4. 在 Github 端仓库创建同名分支、定期 Push
5. 需要帮助或反馈时创建 Pull Request，以 Pull Request 进行交流
6. 让其他开发者进行查看，确认作业完成后与 Master 分支合并
7. 与Master分支合并后立刻部署

See http://scottchacon.com/2011/08/31/github-flow.html

在 Pull Request 中，审查之后如果认为可以与 Master 分支合并，则需要明确地告知对方。按照 Github 的文化，这里会用到 `:+1:` 或 `:shipit:` 等表情。偶尔也会见到 `LGTM` 的字样，这是 `Looks Good To Me` 的简写。


### Git Flow——以`发布`为中心的开发模式
1. 从开发版的分支（Develop）创建工作分支（Feature Branches），进行功能的实现或修正。
2. 工作分支（Feature Branches）的修改结束后，与开发版的分支（Develop）进行合并。
3. 重复上述 1 和 2，不断实现功能直至可以发布。
4. 创建用于发布的分支（Release Branches），处理发布的各项工作。
5. 发布工作完成后与 Master 分支合并，并打上版本标签（Tag）进行发布。
6. 如果发布的软件出现 Bug，以打了标签的版本为基础进行修正（Hotfixes）。

See http://nvie.com/posts/a-successful-git-branching-model/

#### 主分支
在中央代码库和从中央代码库克隆的各开发人员的代码库中一直存在的主要分支。

#### Master
为发布而建的分支。每次发布时都打上标签。

#### Develop
开发用的分支。发布之前的最新版本。

#### 辅助分支
原则上只存在于各开发人员的代码库中，是发挥相应的功能后就被删除的临时分支。

#### Feature
从 Develop 分离出来的被用于开发特定功能的分支。功能开发结束后被合并到 Develop 中。

#### Release
从 Develop 分离出来的为发布准备的分支。在发布的准备工作期间，为了避免多余的 Feature 混杂到发布中而建立的分支。发布结束后被合并到 Master 和 Develop 中。

#### Hotfix
主要是在发布后的产品发生故障时紧急建立的分支。直接从 Master 分离，Bug 修正后再合并到 Master 并打上标签。为了避免将来遗漏这个 Bug 的修正，还要合并到 Develop。如果此时有正在发布作业中的 Release 分支，还要向 Release 进行合并。


## 版本号的分配规则
用 `x.y.z` 格式进行版本管理时的规则如下：
- `x` 在重大功能变更或新版本不向下兼容时加 `1`，此时 `y` 与 `z` 的数字为 `0`。
- `y` 在添加新功能或者删除已有功能时加 `1`，此时 `z` 的数字归 `0`。
- `z` 只在进行内部修改后加 `1`。
