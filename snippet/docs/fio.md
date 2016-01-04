
测试磁盘IO读写性能
================

#### 随机读
```shell
fio –bs=512 –ioengine=libaio –userspace_reap –time_based –runtime=60 \
    –group_reporting –buffered=0 –direct=1 –randrepeat=0 –norandommap \
    –ramp_time=6 –iodepth=16 –numjobs=16 –size=100G –name=randread –rw=randread \
    –directory=/md –filename=fio-test.file –output=/data/log/fio-r.txt
```

#### 随机写
```shell
fio –bs=512 –ioengine=libaio –userspace_reap –time_based –runtime=60 \
    –group_reporting –buffered=0 –direct=1 –randrepeat=0 –norandommap \
    –ramp_time=6 –iodepth=16 –numjobs=16 –size=100G –name=randwrite –rw=randwrite \
     –directory=/md –filename=fio-test.file –output=/data/log/fio-w.txt
```

#### 混合读写
```shell
fio –bs=512 –ioengine=libaio –userspace_reap –time_based –runtime=60 \
    –group_reporting –buffered=0 –direct=1 –randrepeat=0 –norandommap \
    –ramp_time=6 –iodepth=16 –numjobs=16 –size=100G –name=randmixed –rwmixwrite=20 –rw=randrw\
    –directory=/md –filename=fio-test.file –output=/data/log/fio-m.txt
```
