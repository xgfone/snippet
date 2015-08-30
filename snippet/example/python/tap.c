
/**************************************************************
 * Compile:
 *     gcc -Wall -fpic -shared  -I/usr/include/python${version} tap.c -o tap.so
 * ${version} is the version number of python, such as 2.7.
 *
 * Use:
 * import tap
 * fd = tap.open(name, type='tap', block=True)
 * data = tap.read(fd, 8192)
 * count = tap.write(fd, data, data_size)
 * tap.close(fd)
 **************************************************************/

// #include <pcap.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <net/if.h>
#include <linux/if_tun.h>
#include <sys/ioctl.h>
#include <linux/ioctl.h>
// #include <linux/filter.h>
// #include <getopt.h>
#include <Python.h>


// <linux/if_tun.h>
// In the new version, the macros have changed, and the value changed, such as,
// IFF_TUN_DEV for tun, IFF_TAP_DEV for tap, and IFF_NO_PI is equal to 0x0040,
// not 0x1000.
// /* TUNSETIFF ifr flags */
// #define IFF_TUN     0x0001
// #define IFF_TAP     0x0002
// #define IFF_NO_PI   0x1000
// #define IFF_VNET_HDR    0x4000
// /* Ioctl defines */
// #define TUNSETNOCSUM  _IOW('T', 200, int)
// #define TUNSETDEBUG   _IOW('T', 201, int)
// #define TUNSETIFF     _IOW('T', 202, int)
// #define TUNSETPERSIST _IOW('T', 203, int)
// #define TUNSETOWNER   _IOW('T', 204, int)
// #define TUNSETLINK    _IOW('T', 205, int)
// #define TUNSETGROUP   _IOW('T', 206, int)
// #define TUNGETFEATURES _IOR('T', 207, unsigned int)
// #define TUNSETOFFLOAD  _IOW('T', 208, unsigned int)
// #define TUNSETTXFILTER _IOW('T', 209, unsigned int)
// #define TUNGETIFF      _IOR('T', 210, unsigned int)
// #define TUNGETSNDBUF   _IOR('T', 211, int)
// #define TUNSETSNDBUF   _IOW('T', 212, int)
// #define TUNATTACHFILTER _IOW('T', 213, struct sock_fprog)
// #define TUNDETACHFILTER _IOW('T', 214, struct sock_fprog)
// #define TUNGETVNETHDRSZ _IOR('T', 215, int)
// #define TUNSETVNETHDRSZ _IOW('T', 216, int)

#ifndef IFF_TUN_DEV
#define IFF_TUN_DEV  IFF_TUN
#endif

#ifndef IFF_TAP_DEV
#define IFF_TAP_DEV IFF_TAP
#endif


#ifdef PY3
#define BYTES_FORMAT "y#"
#else
#define BYTES_FORMAT "z#"
#endif

#define TAP_BUFSIZE  (1024 * 1024)
#define PATH_NET_TUN ("/dev/net/tun")


static PyObject* None()
{
    Py_INCREF(Py_None);
    return Py_None;
}

static int tap_tun_open(char *ifname, char *type, int block)
{
    struct ifreq ifr;
    int fd;
    size_t length;

    length = strlen(ifname);
    length = (length > IFNAMSIZ) ? IFNAMSIZ : length;
    memset(&ifr, 0, sizeof(ifr));
    if (ifname){
        memcpy(ifr.ifr_name, ifname, length);
    }else{
        fprintf(stderr, "ifname is invalid or empty!\n");
        return -1;
    }

    if (strncmp(type, "tap", 3) == 0){  // tap
        ifr.ifr_flags = IFF_TAP_DEV | IFF_NO_PI;
    } else {    // tun
        ifr.ifr_flags = IFF_TUN_DEV | IFF_NO_PI;
    }

    fd = open(PATH_NET_TUN, O_RDWR);
    if (fd < 0) {
        fprintf(stderr, "could not open %s\n", PATH_NET_TUN);
        return -1;
    }

    if (ioctl(fd, TUNSETIFF, (void *) &ifr) != 0) {
        if (ifname[0] != '\0') {
            fprintf(stderr, "could not configure %s (%s): %m\n", PATH_NET_TUN, ifr.ifr_name);
        } else {
            fprintf(stderr, "could not configure %s: %m\n", PATH_NET_TUN);
        }
        close(fd);
        return -1;
    }

    if (block && (fcntl(fd, F_SETFL, O_NONBLOCK) == -1)) {
        close(fd);
        return -1;
    }

    return fd;
}


// def open(name: str, type: str, block: bool) => int
// 如果成功，则返回一个整数，即文件描述符；如果失败，则返回-1。
static PyObject* tap_open(PyObject* self, PyObject *args, PyObject *keywds)
{
    int rtn = -1;
    char *name;
    char *type = "tap";
    int block = 1;
    static char *kwlist[] = {"name", "type", "block", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|si", kwlist, &name, &type, &block))
        return Py_BuildValue("i", -4);

    if (!name || !type) {
        return Py_BuildValue("i", -2);
    }

    if (strncmp(type, "tap", 3)!=0)
        if (strncmp(type, "tun", 3)!=0)
            return Py_BuildValue("i", -3);

    rtn = tap_tun_open(name, type, block);
    return Py_BuildValue("i", rtn);
}


// def read(fd: int, count: int) => str/None
// 如果count为负，则直接返回None；如果为0，则读取尽可能多的字符；如果大于0，则读取count个字符。
// 如果出现错误，则返回None；否则返回一个字符串，但可能是一个空字符串。
//static PyObject* tap_read(PyObject *self, int fd, int count)
static PyObject* tap_read(PyObject *self, PyObject *args)
{
    int fd;
    int count;
    int num = 0;
    //static char bufsize[TAP_BUFSIZE];
    char bufsize[TAP_BUFSIZE];

    if (!PyArg_ParseTuple(args, "ii", &fd, &count)) {
        return None();
    }

    if (count < 0) {
        return None();
    } else if (count == 0) {
        count = TAP_BUFSIZE;
    } else if (count > SSIZE_MAX) {
        count = (int)SSIZE_MAX;
    }

    memset(bufsize, 0, TAP_BUFSIZE);
    num = read(fd, bufsize, (size_t)count);
    if (num < 0){
        return None();
    } else if (num == 0) {
        return None();
    }
    return Py_BuildValue(BYTES_FORMAT, bufsize, num);
}


// def write(fd: int, data: str, count: int) => int
static PyObject* tap_write(PyObject *self, PyObject *args)
{
    int count = -1;
    int fd;
    char *data;
    int rtn = -1;

    if (!PyArg_ParseTuple(args, "iz#", &fd, &data, &count)){
        return Py_BuildValue("i", -1);
    }

    rtn = write(fd, data, count);
    return Py_BuildValue("i", rtn);
}


// def close(fd: int) => None
static PyObject* tap_close(PyObject *self, PyObject *args)
{
    int fd;
    if (!PyArg_ParseTuple(args, "i", &fd)){
        return None();
    }

    close(fd);
    return None();
}


static PyMethodDef TapMethods[] = {
    {"open",  (PyCFunction)tap_open,  METH_VARARGS | METH_KEYWORDS, "open the tap/tun interface."},
    {"close", tap_close, METH_VARARGS, "close the tap/tun interface."},
    {"read",  tap_read,  METH_VARARGS, "read the MAC frame from the tap, and the IP packet from the tun."},
    {"write", tap_write, METH_VARARGS, "write the MAC frame into the tap, and the IP packet into the tun."},
    {NULL,    NULL,      0,            NULL},
};


void inittap()
{
    (void)Py_InitModule("tap", TapMethods);
}
