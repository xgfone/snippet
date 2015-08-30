
// The Kernel Timer

#include <linux/init.h>
#include <linux/module.h>
#include <linux/timer.h>
#include <linux/fs.h>

#define TIMER_MAJOR     234
#define DEVICE_NAME     "timer_test"

// 1. 定义timer结构
struct timer_list timer;

static void func_timer(unsigned long data)
{
    // 4. 修改定时器的超时参数并重启
    mod_timer(&timer, jiffies + HZ);
    printk("current jiffies is %ld\n", jiffies);
}

struct file_operations timer_ops = {
    .owner = THIS_MODULE,
};

static int __init timer_init(void)
{
    register_chrdev(TIMER_MAJOR, DEVICE_NAME, &timer_ops);

    // 2. 初始化定时器
    setup_timer(&timer, func_timer, 0);
    #if 0
    init_timer(&timer);
    timer.data = 0;
    timer.expires = jiffies + HZ;
    timer.function = func_timer;
    #endif

    // 3. 添加激活计时器
    add_timer(&timer);

    printk("timer_init\n");
    return 0;
}

static void __exit timer_exit(void)
{
    // 4. 删除定时器
    del_timer(&timer);
    unregister_chrdev(TIMER_MAJOR, DEVICE_NAME);
}

module_init(timer_init);
module_exit(timer_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("TEST Kernel Timer");
MODULE_AUTHOR("XXXX <XXX@XXX.com>");

/********************************************************/
// # insmod timer_test.ko
// timer_init
// timer_init
// current jiffies is 220614
// current jiffies is 220614
// current jiffies is 220714
// current jiffies is 220714
