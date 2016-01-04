
用FPM快速制作RPM包
=================

#### 一、安装FPM
```shell
yum -y install ruby rubygems ruby-devel
gem sources --add https://ruby.taobao.org/ --remove https://rubygems.org/
gem install fpm
```

#### 二、把NodeJS打包成RPM包
```shell
# 下载并编译 NodeJS
wget http://nodejs.org/dist/v0.10.12/node-v0.10.12.tar.gz # 去nodejs官网下载最新源码包
tar zxvf node-v0.10.12.tar.gz -C /dev/shm/                # 解压
cd /dev/shm/node-v0.10.12/                                # 进入源码目录
./configure --prefix=/usr --dest-cpu=x64 --dest-os=linux  # 指定配置参数
make -j24                                                 # 使用多核编译
mkdir /dev/shm/node-root                                  # 创建安装目录
make -j24 install DESTDIR=/dev/shm/node-root              # 指定安装路径

# 使用 FPM 制作 RPM 包
fpm -f --verbose -s dir -t rpm --category 'Development/Languages' \
    --license 'BSD' -m 'higkoo'  --epoch 0 -v 0.10.12 \
    --url 'nodejs.org' --description 'Node.js real-time applications' \
    -n nodejs  -C /dev/shm/node-root -p ~/rpmbuild/RPMS/x86_64/ \
    --no-rpm-sign --iteration 1.el6 \
    -d 'openssl >= 0.9.8'  -d 'libstdc++ >= 4.4.3'  \
    usr/bin usr/lib usr/share

# 查看RPM包信息
rpm -qpi ~/rpmbuild/RPMS/x86_64/nodejs-0.10.12-1.x86_64.rpm
```

#### 三、其它
```
https://github.com/jordansissel/fpm/wiki
https://github.com/jordansissel/fpm/wiki/ConvertingPython
```
