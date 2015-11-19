
////////////////////////////////////
/// Include

#include <linux/types.h>
#include <linux/kernel.h>

#define TEST_DEBUG 1
#if TEST_DEBUG
#define test_info(fmt, ...)	printk(KERN_INFO pr_fmt(fmt), ##__VA_ARGS__)
#define test_emerg(fmt, ...)	printk(KERN_EMERG pr_fmt(fmt), ##__VA_ARGS__)
#define test_alert(fmt, ...)	printk(KERN_ALERT pr_fmt(fmt), ##__VA_ARGS__)
#define testr_crit(fmt, ...)	printk(KERN_CRIT pr_fmt(fmt), ##__VA_ARGS__)
#define test_err(fmt, ...)	printk(KERN_ERR pr_fmt(fmt), ##__VA_ARGS__)
#define test_warning(fmt, ...)	printk(KERN_WARNING pr_fmt(fmt), ##__VA_ARGS__)
#define test_notice(fmt, ...)	printk(KERN_NOTICE pr_fmt(fmt), ##__VA_ARGS__)
#define test_info(fmt, ...)	printk(KERN_INFO pr_fmt(fmt), ##__VA_ARGS__)
#define test_cont(fmt, ...)	printk(KERN_CONT fmt, ##__VA_ARGS__)
/* pr_devel() should produce zero code unless DEBUG is defined */
#ifdef DEBUG
#define pr_devel(fmt, ...)	printk(KERN_DEBUG pr_fmt(fmt), ##__VA_ARGS__)
#else
#define pr_devel(fmt, ...)	({ if (0) printk(KERN_DEBUG pr_fmt(fmt), ##__VA_ARGS__); 0; })
#endif
#else
#define test_info(fmt, ...)
#define test_info(fmt, ...)
#define test_emerg(fmt, ...)
#define test_alert(fmt, ...)
#define testr_crit(fmt, ...)
#define test_err(fmt, ...)
#define test_warning(fmt, ...)
#define test_notice(fmt, ...)
#define test_info(fmt, ...)
#define test_cont(fmt, ...)
#define test_devel(fmt, ...)
#endif

//// See in <linux/kernel.h>
#ifndef container_of
/**
 * container_of - cast a member of a structure out to the containing structure
 * @ptr:	the pointer to the member.
 * @type:	the type of the container struct this is embedded in.
 * @member:	the name of the member within the struct.
 */
#define container_of(ptr, type, member) ({			\
	const typeof(((type *)0)->member) * __mptr = (ptr);	\
	(type *)((char *)__mptr - offsetof(type, member)); })
#endif


// 打印信息
// 以十六进制打印每一个字节，共打印 n 个字节；其中，info是提供一个描述性信息
extern void test_print_hex(const char *info, void *data, size_t n);
// 以字符串的形式打印数据，直到空字符或第 n 个字符；其中，info是提供一个描述性信息
extern void test_print_char(const char *info, void *data, size_t n);

///////////////////////////////////////////////////////
// Implementation

void test_print_hex(const char *info, void *data, size_t n)
{
	size_t i;
	unsigned char *p = (unsigned char *)data;

	pr_info("%s ", info);
	for (i=0; i<n; ++i) {
		pr_info("%X ", *(p+i));
	}
	pr_info("\n");
}

void test_print_char(const char *info, void *data, size_t n)
{
	size_t i;
	unsigned char *p = (unsigned char *)data;

	pr_info("%s ", info);
	for (i=0; i<n; ++i) {
		if (*(p+i) == '\0')
			break;
		pr_info("%c ", (char)*(p+i));
	}
	pr_info("\n");
}
