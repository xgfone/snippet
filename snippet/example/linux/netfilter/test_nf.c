#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/skbuff.h>
#include <linux/ip.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <net/tcp.h>
#include <linux/if_ether.h>
//#include <if_packet.h>
//#include "nf_sockopte.h"

/*  NF初始化状态宏 */
#define NF_SUCCESS 0
#define NF_FAILURE 1

#ifndef NF_IP_PRE_ROUTING
#define NF_IP_PRE_ROUTING 0
#endif

#ifndef NF_IP_POST_ROUTING
#define NF_IP_POST_ROUTING 4
#endif

/*
//Judge whether the system is the big edian, or the little edian.

enum BLEdian {NONE=0, LITTLE_EDIAN=1, BIG_EDIAN=2, NETWORK_EDIAN=BIG_EDIAN};
static enum BLEdian bl_edian = NONE;

static int judge_bl_edian(void)
{
    if (bl_edian == NONE){
        __u32 tmp = 0x12345678;
        unsigned char *p = (unsigned char *)&tmp;
        if (*p == 0x12)
            bl_edian = BIG_EDIAN;
        else
            bl_edian = LITTLE_EDIAN;
    }
    return bl_edian;
}
*/

static void encrypt(unsigned char * data, size_t len)
{
    int i;
    for (i=0; i<len; ++i)
        data[i] ^= 0x1;
}


static void unencrypt(unsigned char *data, size_t len)
{
    encrypt(data, len);
}


static unsigned int nf_hook_pre_routing(unsigned int hooknum,
                                   struct sk_buff *skb,
                                   const struct net_device *in,
                                   const struct net_device *out,
                                   int (*okfn) (struct sk_buff*))
{
    // TODO:
    unsigned char *mac_h = skb_mac_header(skb);
    __u16 protocol_type;

    if (skb->mac_len == 0)
        return NF_ACCEPT;

    protocol_type = ((*(mac_h + 12)) << 8) + (*(mac_h + 13));

    if (protocol_type == 0x0800) {     // IP Protocol
        struct iphdr *iph = ip_hdr(skb);
        unsigned char *data = NULL;
        __u16 data_len;

        // ====================== encrypt IP including Header =====================
        // data = (unsigned char *)iph;
        // data_len = ntohs(iph->tot_len);
        // =============================== END ===================================

        // ======================= encrypt IP not Header ======================
        data = (unsigned char *)iph + (iph->ihl << 2);
        data_len = ntohs(iph->tot_len) - (iph->ihl << 2);
        // =============================== END ================================

        printk(KERN_ALERT "PRE -- Before Unencrypt: %X\n", data[0]);
        unencrypt(data, data_len);
        printk(KERN_ALERT "PRE -- After Unencrypt: %X\n", data[0]);
    } else {     // Not IP Protocol
        printk(KERN_ALERT "%X\n", protocol_type);
    }

    return NF_ACCEPT;
}


static unsigned int nf_hook_post_routing(unsigned int hooknum,
                                   struct sk_buff *skb,
                                   const struct net_device *in,
                                   const struct net_device *out,
                                   int (*okfn) (struct sk_buff*))
{
    // TODO:
    struct iphdr *iph = ip_hdr(skb);
    unsigned char *data = NULL;
    __u16 data_len;

    // ================== encrypt IP including header ====================
    // data = (unsigned char *)iph;
    // data_len = ntohs(iph->tot_len);
    // ============================== END ================================

    // ======================= encrypt IP not header =====================
    data = (unsigned char *)iph + (iph->ihl << 2);
    data_len = ntohs(iph->tot_len) - (iph->ihl << 2);
    // ============================== END ================================

    printk(KERN_ALERT "POST -- Before encrypt: %X\n", data[0]);
    encrypt(data, data_len);
    printk(KERN_ALERT "POST -- After encrypt: %X\n", data[0]);

    return NF_ACCEPT;
}

static struct nf_hook_ops nf_pre_routing = {
    .list = {NULL, NULL},
    .hook = nf_hook_pre_routing,
    .hooknum = NF_IP_PRE_ROUTING,
    .pf = PF_INET,
    .priority = NF_IP_PRI_FIRST,
};

static struct nf_hook_ops nf_post_routing = {
    .list = {NULL, NULL},
    .hook = nf_hook_post_routing,
    .hooknum = NF_IP_POST_ROUTING,
    .pf = PF_INET,
    .priority = NF_IP_PRI_LAST,
};

/* 初始化模块 */
static int __init daoli_nf_init(void)
{
    //judge_bl_edian();

    nf_register_hook(&nf_pre_routing);
    nf_register_hook(&nf_post_routing);

    //printk(KERN_INFO "netfilter init successfully!\n");
    printk(KERN_ALERT "netfilter init successfully!\n");
    return NF_SUCCESS;
}


/* 清理模块 */
static void __exit daoli_nf_exit(void)
{
    nf_unregister_hook(&nf_pre_routing);
    nf_unregister_hook(&nf_post_routing);

    //printk(KERN_INFO "netfilter clean successully!\n");
    printk(KERN_ALERT "netfilter clean successully!\n");
}

module_init(daoli_nf_init);
module_exit(daoli_nf_exit);

/* 作者、描述、版本、别名 */
MODULE_AUTHOR("xgfone <xgfone@126.com>");
MODULE_DESCRIPTION("netfilter encrypt");
MODULE_VERSION("0.1");
MODULE_ALIAS("xgfone");
MODULE_LICENSE("Dual BSD/GPL");

