
## 1. Compile and Install `DPDK`

### 1.1 Install the dependencies:

```shell
$ yum install rpm-build \
    kernel-devel kernel-headers libpcap-devel \
    doxygen python-sphinx inkscape \
    texlive-collection-latex
```

### 1.2 By hand

1. 下载 DPDK 17.11.4(TLS 长期支持版)：
```shell
$ wget http://fast.dpdk.org/rel/dpdk-17.11.4.tar.gz
```
2. 解压并编译（这里我们以当前 64 位系统为例）：
```shell
$ cd dpdk-stable-17.11.4
$ make config T=x86_64-native-linuxapp-gcc
$ make && make install
```

上述编译并安装到默认位置。

另外，DPDK 默认编译成静态链接库，如果想编译成动态链接库（在性能上略于静态链接库），可以在编译前，`$DPDK_DIR/config/common_base` 文件中的 `CONFIG_RTE_BUILD_SHARED_LIB` 设置为 `y`（默认为 `n`）。

### 1.3 Build RPM Package
```bash
$ wget http://fast.dpdk.org/rel/dpdk-17.11.4.tar.gz
$ tar xf dpdk-17.11.4.tar.gz
$ mv dpdk-stable-17.11.4 dpdk-17.11.4
$ sed -i "s/all: api-html guides-html guides-pdf/all: api-html guides-html/g" \
      dpdk-17.11.4/mk/rte.sdkdoc.mk  # Optional
$ mkdir -p ~/rpmbuild/SOURCES/
$ tar czf ~/rpmbuild/SOURCES/dpdk-17.11.4.tar.gz dpdk-17.11.4
$ rpmbuild -ba dpdk-17.11.4/pkg/dpdk.spec
```

## 2. Compile OVS with DPDK

对于 `OVS + DPDK`，只须要编译用户空间的 `OVS` 即可，不须要内核空间的模块。


### 2.1 Install the dependencies:

```bash
$ yum install rpm-build autoconf automake libtool systemd-units \
    python2-devel python36-devel python2-six python2-sphinx \
    desktop-file-utils groff graphviz checkpolicy, selinux-policy-devel \
    python2-twisted-core python2-zope-interface \
    openssl openssl-devel \
    libcap-ng libcap-ng-devel \
    procps-ng procps-ng-devel \
    unbound unbound-devel \
    dpdk-devel libpcap-devel numactl-devel  # This three For DPDK
```

### 2.2 手工执行 `make` 编译 `OVS`

在执行 `.configure` 命令时，添加 `--with-dpdk` 选项即可，如：
```bash
$ ./configure --with-dpdk=$DPDK_DIR/x86_64-native-linuxapp-gcc
```

注意，如果 `DPDK` 是以静态编译，则 `OVS` 将会以静态方式进行链接；否则就以动态方式链接。另外，`DPDK` 目录的名字必须是 `DPDK` 的目标格式。`DPDK` 编译后的目录默认为 `build`，可以将其修改为目标格式名，如：`x86_64-native-linuxapp-gcc`。


### 2.3 通过 `RPM` 包编译 `OVS`

```bash
$ wget http://openvswitch.org/releases/openvswitch-2.9.2.tar.gz
$ tar xf openvswitch-2.9.2.tar.gz
$ cd openvswitch-2.9.2
$ ./configure  # for generating Makefile
$ chown -R root:root rhel  # Prevent the error "Bad owner/group" when building
$ make rpm-fedora RPMBUILD_OPT="--with dpdk --without check"
```

注意，此种方式默认只能使用 `DPDK` 的 RPM 包 `dpdk-devel`，不能使用手工编译的 `DPDK` 链接库。 而且，此时 `DPDK` 是以动态链接库的形式链接到 `OVS` 中的。

如果想要 `OVS` 以静态方式链接 `DPDK`，则须要修改 RPM 规范文件 `openvswitch-fedora.spec.in`：
1. 找到 `%global _hardened_build 1` 这一行，在其后添加如下一行代码：
```shell
%undefine _hardened_build
```
2. 注释掉以下几行，以防止检查 `DPDK` 动态链接库：
```bash
if %{with dpdk}
BuildRequires: libpcap-devel numactl-devel
BuildRequires: dpdk-devel >= 17.05.1
Provides: %{name}-dpdk = %{version}-%{release}
%endif
```
3. 找到 `--with-dpdk=` 这一行，将其后的值修改为 `DPDK` 静态链接库的位置（和手工编译 `OVS + DPDK` 的 `--with-dpdk=` 参数一样）。如：
```bash
--with-dpdk=$DPDK_DIR/x86_64-native-linuxapp-gcc
```


## 3. Setup OS

### 3.1 Setup `Hugepages`

Linux 内核在构建和启动时必须启用 `HUGETLBFS` 选项。另外，`PROC_PAGE_MONITOR` 也应当被支持。

#### 3.1.1 Reserve `Hugepages`

DPDK 须要使用 `Hugepages` 大页，因此，首先在系统启动时，要在启动参数中加入 `Hugepages`。

一般有两种页大小：`2M` 和 `1G`。对于 `2M`，须要 CPU 支持 `pse`；而 `1G` 的大页则须要 CPU 支持 `pdpe1gb`。可以通过以下命令来查看 CPU 是否支持 `pse` 或 `pdpe1gb`。

```shell
$ lscpu | grep pse
$ lscpu | grep pdpe1gb
```

注意，对于 64 位系统，如果 CPU 支持 `pdpe1gb`，尽量使用 `1G` 的大页，而不是 `2M` 的大页，这有助于性能的提升。

在系统启动参数中设置 `Hugepages` 的方式（假定总共设置 `4G` 的大页）如下：
```
default_hugepagesz=2M hugepagesz=2M hugepages=2048
```
或
```
default_hugepagesz=1G hugepagesz=1G hugepages=4
```

其中，`hugepagesz` 表示分配的每个页的大小，`default_hugepagesz` 表示默认的页大小，而 `hugepages` 表示要分配的内存页的数量；因此，要分配的总大小为 `hugepagesz * hugepages`。

注，上述参数可以在 `/etc/default/grub` 文件中的 `GRUB_CMDLINE_LINUX` 参数中添加，但要注意更新 `grub.cfg`。

之后，我们就可以在 `/sys/kernel/mm/hugepages` 目录下看到有一个目录 `hugepages-2048kB` 或 `hugepages-1g` 的子目录。

对于 CentOS 7，它默认启用了 `Hugepages`，且默认页大小为 `2M`，但是它的页数量（即 `hugepages` 为 `0`）。

注意，对于 `2M` 的页大小，在操作系统启动时可以不用设置 `hugepages`，在启动后再设置；但是对于 `1G` 的页大小，必须在操作系统启动时设置，不能在启动后设置。

对于 `NUMA` 构架，系统启动时保留的大页数量会平均地分配给每个 `NUMA` 节点。但对于 `NUMA` 构架，由于 `2M` 的大页可以在系统启动后再设置页数量，因此，我们可以显示地设置每个 `NUMA` 节点的大页数量：
```shell
$ echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
$ echo 1024 > /sys/devices/system/node/node1/hugepages/hugepages-2048kB/nr_hugepages
```

#### 3.1.2 Mount `Hugepages`

一旦 `Hugepages` 被保留，为了让保留的大页内存可见，我们须要将其挂载。

```shell
$ mount -t hugetlbfs nodev /dev/hugepages
```

为了让系统在每次启动时都自动挂载，我们可以将上面的命令放到 `/etc/rc.local` 文件中，也可以在 `/etc/fstab` 文件挂载大页。

```shell
nodev /dev/hugepages hugetlbfs defaults 0 0
```

与 `2M` 的大页不同，`1G` 的大页在挂载时，必须指定页大小。如：
```shell
nodev /dev/hugepages_1GB hugetlbfs pagesize=1GB 0 0
```

### 3.2 Enable `IOMMU` and Load `VFIO`driver

从 3.6.0 开始，Linux Kernel 官方已支持 `VFIO` 驱动，它的性能要优于 `UIO`，所以，有了 `VFIO`，我们就没必要再使用 `UIO` 了。

为了使用 `VFIO`，`BIOS` 和 Linux Kernel 都必须开启 `IO virtualization `（`IOMMU`，如 `Intel` 的 `VT-d`）。
1. 我们可以通过命令来查看 BIOS 是否开启了 `IOMMU`。
```shell
$ dmesg | grep -e DMAR -e IOMMU  # For Intel CPU
$ dmesg | grep AMD-Vi            # For AMD CPU
```
2. 我们可以通过下面的命令来确认 Linux Kernel 是否开启了 `IOMMU`。
```shell
$ cat /proc/cmdline | grep iommu=pt
$ cat /proc/cmdline | grep intel_iommu=on  # For Intel CPU
$ cat /proc/cmdline | grep amd_iommu=on    # For AMD CPU
```

一旦 `IOMMU` 被正确地配置，我们就可以加载相应的内核模块，并将 `NIC` 绑定到 `VFIO` 驱动。
```shell
$ modprobe vfio-pci
$ /usr/bin/chmod a+x /dev/vfio
$ /usr/bin/chmod 0666 /dev/vfio/*
$ $DPDK_DIR/usertools/dpdk-devbind.py --bind=vfio-pci eth1
$ $DPDK_DIR/usertools/dpdk-devbind.py --status
```
