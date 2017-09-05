# 使用 Go 工具链支持自定义仓库

当我们使用 `go get` 去下载一个 Go 代码仓库时，`go get` 默认支持 [Github](github.com)、[Bitbucket](bitbucket.org)、[IBM DevOps Services (JazzHub)](hub.jazz.net/git)、[Apache Git](git.apache.org)、[OpenStack Git](git.openstack.org) 以及任何以 `.git`、`.hg`、`.svn`、`.bzr` 结尾的通用仓库。

如果我们的仓库不是上述几种之一，将得不到 `go get` 命令的支持。

还有一种情况：如果在访问仓库时需要事先身份认证，那么也是无法得到 `go get` 支持的。

当 `go get` 不支持我们自定义的私有仓库时，我们可以简单地修改一下 `go get` 命令源码，使其得到支持。

以下我们以 `gitlab.example.com/username/project` 为例进行讲解，假设：通过 `HTTP` 或 `HTTPS` 访问时，用户须要事先进行认证，因此我们没法通过 `go get` 命令自动下载，但我们可以配置 SSH Key 以后通过 `SSH` 来访问。

因此，无论我们执行 `go get gitlab.example.com/username/project`，还是 `go get gitlab.example.com/username/project.git`，都将是失败的。

现在，我们将用下面的方法来解决它：

1. 用编辑器打开 `$GOROOT/src/cmd/go/vcs.go`，找到全局变量 `vcsPaths`（Go 1.9中在 855 行），我们会看到如下信息：
```go
var vcsPaths = []*vcsPath{
	// Github
	{
		prefix: "github.com/",
		re:     `^(?P<root>github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)(/[\p{L}0-9_.\-]+)*$`,
		vcs:   "git",
		repo:  "https://{root}",
		check: noVCSSuffix,
	},

	// Bitbucket
	{
		prefix: "bitbucket.org/",
		re:     `^(?P<root>bitbucket\.org/(?P<bitname>[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+))(/[A-Za-z0-9_.\-]+)*$`,
		repo:   "https://{root}",
		check:  bitbucketVCS,
	},

	// IBM DevOps Services (JazzHub)
	{
		prefix: "hub.jazz.net/git",
		re:     `^(?P<root>hub.jazz.net/git/[a-z0-9]+/[A-Za-z0-9_.\-]+)(/[A-Za-z0-9_.\-]+)*$`,
		vcs:    "git",
		repo:   "https://{root}",
		check:  noVCSSuffix,
	},

	// Git at Apache
	{
		prefix: "git.apache.org",
		re:     `^(?P<root>git.apache.org/[a-z0-9_.\-]+\.git)(/[A-Za-z0-9_.\-]+)*$`,
		vcs:    "git",
		repo:   "https://{root}",
	},

	// Git at OpenStack
	{
		prefix: "git.openstack.org",
		re:     `^(?P<root>git\.openstack\.org/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)(\.git)?(/[A-Za-z0-9_.\-]+)*$`,
		vcs:    "git",
		repo:   "https://{root}",
	},

	// General syntax for any server.
	// Must be last.
	{
		re:   `^(?P<root>(?P<repo>([a-z0-9.\-]+\.)+[a-z0-9.\-]+(:[0-9]+)?(/~?[A-Za-z0-9_.\-]+)+?)\.(?P<vcs>bzr|git|hg|svn))(/~?[A-Za-z0-9_.\-]+)*$`,
		ping: true,
	},
}
```
2. 复制一份 Github 的信息，然后修改如下：
```go
// gitlab.example.com
{
	prefix: "gitlab.example.com/",
	re:     `^(?P<root>gitlab\.example\.com/(?P<project>[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+))(/[\p{L}0-9_.\-]+)*$`,
	vcs:    "git",
	repo:   "ssh://git@gitlab.example.com/{project}",
	check:  noVCSSuffix,
}
```
3. 重新编译 `go` 命令。
    (1) 在 Linux/Mac 下，执行 `$GOROOT/src/make.bash`。
    (2) 在 Windows 下，执行 `cd %$GOROOT%\src\cmd\go && go install`。

**注意：**

1. 对于 `re`，我们只是在 `[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+` 的左右两边分别添加了 `(?P<project>` 和 `)`，这样我们就可以捕获 `gitlab.example.com/username/project` 中的 `username/project` 部分到变量 `project` 中，然后就能在 `repo` 中引用它。
2. 对于 `repo`，我们使用了 `ssh://git@gitlab.example.com/{project}`， 而不是 `git@gitlab.example.com/{project}`，因为后者会被实别为一个非法的 URL，从而导致失败；而多了 `ssh://` 之后，URL 格式就合法了，而且还会被 `go get` 命令认为是一个安全的 URL。
