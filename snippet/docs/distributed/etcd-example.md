
etcd集群实例
==========

## 一、创建一个静态（Static）etcd集群

##### Node1
```shell
$ etcd -name                    node1 \
-data-dir                       ./node1-data-dir \
-initial-advertise-peer-urls    http://10.0.0.101:2380 \
-listen-peer-urls               http://10.0.0.101:2380 \
-listen-client-urls             http://10.0.0.101:2379,127.0.0.1:2379 \
-advertise-client-urls          http://10.0.0.101:2379 \
-initial-cluster-token          etcd-cluster-1 \
-initial-cluster                node1=http://10.0.0.101:2380,\
                                node2=http://10.0.0.102:2380,\
                                node3=http://10.0.0.103:2380 \
-initial-cluster-state          new
```

##### Node2
```shell
$ etcd -name                    node2 \
-data-dir                       ./node2-data-dir \
-initial-advertise-peer-urls    http://10.0.0.102:2380 \
-listen-peer-urls               http://10.0.0.102:2380 \
-listen-client-urls             http://10.0.0.102:2379,http://127.0.0.1:2379 \
-advertise-client-urls          http://10.0.0.102:2379 \
-initial-cluster-token          etcd-cluster-1 \
-initial-cluster                node1=http://10.0.0.101:2380,\
                                node2=http://10.0.0.102:2380,\
                                node3=http://10.0.0.103:2380 \
-initial-cluster-state          new
```

##### Node3
```shell
$ etcd -name                    node3 \
-data-dir                       ./node3-data-dir \
-initial-advertise-peer-urls    http://10.0.0.103:2380 \
-listen-peer-urls               http://10.0.0.103:2380 \
-listen-client-urls             http://10.0.0.103:2379,http://127.0.0.1:2379 \
-advertise-client-urls          http://10.0.0.103:2379 \
-initial-cluster-token          etcd-cluster-1 \
-initial-cluster                node1=http://10.0.0.101:2380,\
                                node2=http://10.0.0.102:2380,\
                                node3=http://10.0.0.103:2380 \
-initial-cluster-state          new
```

**Notes:**

    If this cluster is a new cluster, the node, for instance, node3, must be
    be added to the list of initial cluster member. That is, the option,
    '-initial-cluster', contains the configuration of 'node3'.

**脚本样例**
```shell
#!/bin/sh
#
# This script starts a member of a new etcd v3 cluster.
#

# The value is "new" or "existing".
CLUSTER_STATUS=new
CURRENT_NODE=node1
CURRENT_HOST=10.0.0.101
ALL_HOSTS=node1=10.0.0.101,node2=10.0.0.102,node3=10.0.0.103

PROTOCOL=http
CLIENT_PORT=2379
ADVERTISE_PORT=2380
CLUSTER_NAME=etcd_cluster
DATA_DIR=/data/${CLUSTER_NAME}
WAL_DIR=

ETCD_CMD=`which etcd`
ENABLE_OLD_CLIENT_PORT=0

#######################################################################
CURRENT_DIR=${PWD}

if [[ "CMD_$1" == "CMD_add" ]]; then
    CLUSTER_STATUS=existing
fi

if [[ -z $CURRENT_NODE ]]; then
    CURRENT_NODE=`hostname`
fi

if [[ -z $DATA_DIR ]]; then
    DATA_DIR=${CURRENT_DIR}
fi

CLUSTER_HOST_URLS=
for node in `echo $ALL_HOSTS | sed "s/,/ /g"`
do
    key=`echo $node | awk -F'=' '{print $1}'`
    value=`echo $node | awk -F'=' '{print $2}'`
    if [[ -z $CLUSTER_HOST_URLS ]]; then
        CLUSTER_HOST_URLS=${key}=${PROTOCOL}://${value}:${ADVERTISE_PORT}
    else
        CLUSTER_HOST_URLS=${CLUSTER_HOST_URLS},${key}=${PROTOCOL}://${value}:${ADVERTISE_PORT}
    fi
done

CLUSTER_LISTEN_CLIENT_URLS_OLD=${PROTOCOL}://127.0.0.1:4001
CLUSTER_LISTEN_CLIENT_URLS=${PROTOCOL}://${CURRENT_HOST}:${CLIENT_PORT},${PROTOCOL}://127.0.0.1:${CLIENT_PORT}
# CLUSTER_LISTEN_CLIENT_URLS_OLD=${PROTOCOL}://0.0.0.0:4001
# CLUSTER_LISTEN_CLIENT_URLS=${PROTOCOL}://0.0.0.0:${CLIENT_PORT}

# if [[ ${CLIENT_PORT} -ne 4001 ]]; then
if [[ ENABLE_OLD_CLIENT_PORT -ne 0 ]]; then
    CLUSTER_LISTEN_CLIENT_URLS=${CLUSTER_LISTEN_CLIENT_URLS},${CLUSTER_LISTEN_CLIENT_URLS_OLD}
fi

# CLUSTER_LISTEN_PEER_URLS=${PROTOCOL}://0.0.0.0:${ADVERTISE_PORT}
CLUSTER_LISTEN_PEER_URLS=${PROTOCOL}://${CURRENT_HOST}:${ADVERTISE_PORT}

#######################################################################
### Member
export ETCD_NAME=${CURRENT_NODE}
export ETCD_DATA_DIR=${DATA_DIR}
export ETCD_WAL_DIR=${WAL_DIR}
export ETCD_LISTEN_PEER_URLS=${CLUSTER_LISTEN_PEER_URLS}
export ETCD_LISTEN_CLIENT_URLS=${CLUSTER_LISTEN_CLIENT_URLS}

### Cluster
# ETCD_ADVERTISE_CLIENT_URLS and ETCD_INITIAL_ADVERTISE_PEER_URLS can contain
# domain names, not 0.0.0.0 or 127.0.0.1.
#export ETCD_AUTO_COMPACTION_RETENTION=24
export ETCD_ADVERTISE_CLIENT_URLS=${PROTOCOL}://${CURRENT_HOST}:${CLIENT_PORT}
export ETCD_INITIAL_CLUSTER_STATE=${CLUSTER_STATUS}
export ETCD_INITIAL_CLUSTER_TOKEN=${CLUSTER_NAME}
export ETCD_INITIAL_ADVERTISE_PEER_URLS=${PROTOCOL}://${CURRENT_HOST}:${ADVERTISE_PORT}
export ETCD_INITIAL_CLUSTER=${CLUSTER_HOST_URLS}

### Logging
#export ETCD_DEBUG=false

# Start the ECTD cluster.
$ETCD_CMD

if [[ $? -ne 0 ]]; then {
    echo "Failed to start the member[${CURRENT_NODE}] in the cluster[${CLUSTER_NAME}]"
    exit 1
}
```


## 二、集群发现——Etcd Discovery

### 1、 Custom etcd Discovery Service
You must have an existing cluster, because discovery uses it to bootstrap itself.

#### (1) Create a discovery URL:
```shell
$ curl -X PUT http://myetcd.local/v2/keys/discovery/9295d70238b112a74ac40223c47cb843/_config/size -d value=3
==> The Discovery URL is "http://myetcd.local/v2/keys/discovery/9295d70238b112a74ac40223c47cb843"
```

**注意：**

    A. This URL will be deleted when the cluster has be built.
    B. If the number of the cluster is more than the size you given, such as above, 3,
       the nodes beyond the size are becoming proxies.

#### (2) Start the etcd cluster services
##### Node1
```shell
$ etcd -name                    node1 \
-initial-advertise-peer-urls    http://10.0.0.101:2380 \
-listen-peer-urls               http://10.0.0.101:2380 \
-listen-client-urls             http://10.0.0.101:2379,http://127.0.0.1:2379 \
-advertise-client-urls          http://10.0.0.101:2379 \
-discovery                      http://myetcd.local/v2/keys/discovery/9295d70238b112a74ac40223c47cb843
```

##### Node2
```shell
$ etcd -name                    node2 \
-initial-advertise-peer-urls    http://10.0.0.102:2380 \
-listen-peer-urls               http://10.0.0.102:2380 \
-listen-client-urls             http://10.0.0.102:2379,http://127.0.0.1:2379 \
-advertise-client-urls          http://10.0.0.102:2379 \
-discovery                      http://myetcd.local/v2/keys/discovery/9295d70238b112a74ac40223c47cb843
```

##### Node3
```shell
$ etcd -name                    node3 \
-initial-advertise-peer-urls    http://10.0.0.103:2380 \
-listen-peer-urls               http://10.0.0.103:2380 \
-listen-client-urls             http://10.0.0.103:2379,http://127.0.0.1:2379 \
-advertise-client-urls          http://10.0.0.103:2379 \
-discovery                      http://myetcd.local/v2/keys/discovery/9295d70238b112a74ac40223c47cb843
```

### 2、Public etcd Discovery Service
#### (1) Get a discovery url
```shell
$ curl https://discovery.etcd.io/new?size=3
==> https://discovery.etcd.io/9295d70238b112a74ac40223c47cb843
```

#### (2) Start the etcd cluster service
It's the same as Custom etcd Discovery Service, just only replace the discovery with:
https://discovery.etcd.io/9295d70238b112a74ac40223c47cb843


## 三、集群发现——DNS Discovery

OMIT ...


## 四、增加一个新节点
Adding a member is a two step process:

(1) Add the new member to the cluster via the members API or the "etcdctl member add" command.
```shell
$ etcdctl member add node4 http://10.0.0.104:2380
==> Added member named node4 with ID c4eb0bcf6cee9f81 to cluster
==> ETCD_NAME="node4"
==> ETCD_INITIAL_CLUSTER="node1=http://10.0.0.101:2380,node2=http://10.0.0.102:2380,node3=http://10.0.0.103:2380,node4=http://10.0.0.104:2380"
==> ETCD_INITIAL_CLUSTER_STATE="existing"
```

(2) Start the new member with the new cluster configuration, including a list of the updated members (existing members + the new member).
```shell
$ etcd -name                    node4 \
-data-dir                       ./node4-data-dir \
-initial-advertise-peer-urls    http://10.0.0.104:2380 \
-listen-peer-urls               http://10.0.0.104:2380 \
-listen-client-urls             http://10.0.0.104:2379,http://127.0.0.1:2379 \
-advertise-client-urls          http://10.0.0.104:2379 \
-initial-cluster                node1=http://10.0.0.101:2380,\
                                node2=http://10.0.0.102:2380,\
                                node3=http://10.0.0.103:2380,\
                                node4=http://10.0.0.104:2380 \
-initial-cluster-state          existing
```


## 五、删除一个节点
```shell
$ etcdctl member remove <NODE-ID>
```
or
```shell
$ curl http://10.0.0.101:2379/v2/members/<NODE-ID>; -XDELETE
```


## 六、代理模式

**The Proxy Mode in etcd is the same as the follower that don't participate in the leadership election.**

To start etcd in proxy mode, you need to provide three flags: "**`proxy`**", "**`listen-client-urls`**", and "**`initial-cluster`**" (or "**`discovery`**").
To start a readwrite proxy, set "**`-proxy on`**"; To start a readonly proxy, set "**`-proxy readonly`**".

The proxy will be listening on "**`listen-client-urls`**" and forward requests to the etcd cluster discovered from in "**`initial-cluster`**" or "**`discovery`**" url.

#### Start the proxy node
```shell
$ etcd \
-proxy                  on \
-listen-client-urls     http://10.0.0.104:2379,http://127.0.0.1:2379 \
-initial-cluster        node1=http://10.0.0.101:2380,\
                        node2=http://10.0.0.102:2380,\
                        node3=http://10.0.0.103:2380
```
