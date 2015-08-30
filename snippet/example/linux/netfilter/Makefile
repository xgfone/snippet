target = test_nf
obj-m := $(target).o
KERNELDIR = /lib/modules/`uname -r`/build
#KERNELDIR = /usr/src/kernels/`uname -r`
default:
	$(MAKE) -C $(KERNELDIR) M=`pwd` modules

install:
	insmod $(target).ko

uninstall:
	rmmod $(target)

clean:
	rm -rf *.o *.mod.c *.ko.*
	rm -rf Module.symvers .*cmd .tmp_versions modules.order

