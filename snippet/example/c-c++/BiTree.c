//******************************************************************************
//******************************************************************************
//*程序：BiTree                                                               **
//*作者：谢高峰                                                               **
//*时间：2010年11月10号                                                       **
//*功能：完成二叉树的简单的操作                                               **
//*说明：                                                                     **
//*     (1)本程序使用C而非C++来实现（作者在学Linux，需要C的支持）             **
//*     (2)在添加结点时，本程序不是很好，如果要添加的结点的父结点有多个，那么 **
//*        以找到的第一个为准。                                               **
//*     (3)本程序的树元素类型在测试时被定义成char型，如若用其他的类型（比如   **
//*        int型），可以把typedef char DATA中的char改成所需要的类型（比如int）**
//*        即可，其他的不变。                                                 **
//*     (4)本程序的按层遍历参考其他的算法                                     **
//*     (5)本程序只是一个测试，有能力者可以改进                               **
//******************************************************************************
//******************************************************************************

#include <stdio.h>
#include <stdlib.h>
#define QUEUE_MAXSIZE 50
////////////////////////////////////////////////////////////////////////////////
typedef char DATA;       //定义元素类型
typedef struct ChainTree  //定义二叉树结点类型
{
    DATA data;	//元素数据
    struct ChainTree *left;	//左子树结点指针
    struct ChainTree *right;	//右子树结点指针
}ChainBinTree;
////////////////////////////////////////////////////////////////////////////////
//初始化二叉树根结点
ChainBinTree *BinTreeInit(ChainBinTree *node)
{
     if(node!=NULL) //若二叉树根结点不为空
         return node;
     else
         return NULL;
}
//添加数据到二叉树
//bt为父结点，node为子结点,n=1表示添加左子树，n=2表示添加右子树
int BinTreeAddNode(ChainBinTree *bt,ChainBinTree *node,int n)
{
    if(bt==NULL)
    {
        printf("父结点不存在，请先设置父结点!\n");
        return 0;
    }
    switch(n)
    {
        case 1: //添加到左结点
            if(bt->left) //左子树不为空
            {
                printf("左子树结点不为空!\n");
                return 0;
            }else
                bt->left=node;
            break;
        case 2://添加到右结点
            if( bt->right) //右子树不为空
            {
                printf("右子树结点不为空!\n");
                return 0;
            }else
                bt->right=node;
            break;
        default:
            printf("参数错误!\n");
            return 0;
    }
    return 1;
}
//返回左子结点
ChainBinTree *BinTreeLeft(ChainBinTree *bt)
{
    if(bt)
        return bt->left;
    else
        return NULL;
}
//返回右子结点
ChainBinTree *BinTreeRight(ChainBinTree *bt)
{
    if(bt)
        return bt->right;
    else
        return NULL;
}
//检查二叉树是否为空，为空则返回1,否则返回0
int BinTreeIsEmpty(ChainBinTree *bt)
{
    if(bt)
        return 0;
    else
        return 1;
}
//求二叉树深度
int BinTreeDepth(ChainBinTree *bt)
{
    int dep1,dep2;
    if(bt==NULL)
        return 0; //对于空树，深度为0
    else
    {
        //左子树深度 (递归调用)
        dep1 = BinTreeDepth(bt->left);
        //右子树深度 (递归调用)
        dep2 = BinTreeDepth(bt->right);
        if(dep1>dep2)
           return dep1 + 1;
        else
            return dep2 + 1;
    }
}
//在二叉树中查找值为data的结点
ChainBinTree *BinTreeFind(ChainBinTree *bt,DATA data)
{
    ChainBinTree *p;
    if(bt==NULL)
        return NULL;
    else
    {
        if(bt->data==data)
            return bt;
        else{ // 分别向左右子树递归查找
            if((p=BinTreeFind(bt->left,data)))
                return p;
            else if((p=BinTreeFind(bt->right, data)))
                return p;
            else
                return NULL;
        }
    }
}
// 清空二叉树，使之变为一棵空树
void BinTreeClear(ChainBinTree *bt)
{
     if(bt)
     {
         //清空左子树
         BinTreeClear(bt->left);
         //清空右子树
         BinTreeClear(bt->right);
         //释放当前结点所占内存
         free(bt);
         bt=NULL;
     }
     return;
}
//先序遍历
void BinTree_DLR(ChainBinTree *bt,void (*oper)(ChainBinTree *p))
{
     if(bt)//树不为空，则执行如下操作
     {
         //处理结点的数据
         oper(bt);
         BinTree_DLR(bt->left,oper);
         BinTree_DLR(bt->right,oper);
     }
     return;
}
//中序遍历
void BinTree_LDR(ChainBinTree *bt,void(*oper)(ChainBinTree *p))
{
     if(bt)//树不为空，则执行如下操作
     {
         //中序遍历左子树
         BinTree_LDR(bt->left,oper);
         //处理结点数据
         oper(bt);
         //中序遍历右子树
         BinTree_LDR(bt->right,oper);
     }
     return;
}
//后序遍历
void BinTree_LRD(ChainBinTree *bt,void (*oper)(ChainBinTree *p))
{
     if(bt)
     {
         //后序遍历左子树
         BinTree_LRD(bt->left,oper);
         //后序遍历右子树
         BinTree_LRD(bt->right,oper);
         //处理结点数据
         oper(bt);
     }
     return;
}
//操作二叉树结点数据
void oper(ChainBinTree *p)
{
     printf("%c ",p->data); //输出数据
     return;
}
//按层遍历
void BinTree_Level(ChainBinTree *bt,void (*oper)(ChainBinTree *p))
{
     ChainBinTree *p;
      //定义一个顺序栈
     ChainBinTree *q[QUEUE_MAXSIZE];
     int head=0,tail=0;//队首、队尾序号
     if(bt)//若队首指针不为空
     {
         //计算循环队列队尾序号
         tail=(tail+1)%QUEUE_MAXSIZE;
         //将二叉树根指针进队
         q[tail] = bt;
     }

     //队列不为空，进行循环
     while(head!=tail)
     {
         //计算循环队列的队首序号
         head=(head+1)%QUEUE_MAXSIZE;
         //获取队首元素
         p=q[head];
         //处理队首元素
         oper(p);
         //若结点存在左子树，则左子树指针进队
         if(p->left!=NULL)
         {
             //计算循环队列的队尾序号
             tail=(tail+1)%QUEUE_MAXSIZE;
             //将左子树指针进队
             q[tail]=p->left;
         }

         //若结点存在右孩子，则右孩子结点指针进队
         if(p->right!=NULL)
         {
             //计算循环队列的队尾序号
             tail=(tail+1)%QUEUE_MAXSIZE;
             //将右子树指针进队
             q[tail]=p->right;
         }
     }
     return;
}
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//初始化二叉树的根
ChainBinTree *InitRoot()
{
    ChainBinTree *node;
    if((node=(ChainBinTree *)malloc(sizeof(ChainBinTree)))) //分配内存
    {
        printf("\n输入根结点数据:");
        scanf("%s",&node->data);
        node->left=NULL;
        node->right=NULL;
        return BinTreeInit(node);
    }
    return NULL;
}
void AddNode(ChainBinTree *bt)
{
     ChainBinTree *node,*parent;
     DATA data;
     char select;
    if((node=(ChainBinTree *)malloc(sizeof(ChainBinTree)))) //分配内存
    {
        printf("\n输入二叉树结点数据:");
        //清空输入缓冲区
        fflush(stdin);
        scanf("%s",&node->data);
        //设置左右子树为空
        node->left=NULL;
        node->right=NULL;


        printf("输入父结点数据:");
        //清空输入缓冲区
        fflush(stdin);
        scanf("%s",&data);
        //查找指定数据的结点
        parent=BinTreeFind(bt,data);
        //若未找到指定数据的结点
        if(!parent)
        {
            printf("未找到父结点!\n");
            //释放创建的结点内存
            free(node);
            return;
         }
         printf("1.添加到左子树\n2.添加到右子树\n");
         do{
            select = getchar();
            select-='0';
            if(select==1 || select==2)
                BinTreeAddNode(parent,node,select); //添加结点到二叉树
         }while(select!=1 && select!=2);
    }
    return ;
}
int main()
{
    //root为指向二叉树根结点的指针
    ChainBinTree *root=NULL;
    char select;
     //指向函数的指针
    void (*oper1)();
    //指向具体操作的函数
    oper1=oper;
    do{
        printf("\n1.设置二叉树根元素    2.添加二叉树结点\n");
        printf("3.先序遍历            4.中序遍历\n");
        printf("5.后序遍历            6.按层遍历\n");
        printf("7.二叉树深度          0.退出\n");
        select = getchar();
        switch(select){
        case '1': //设置根元素
             root=InitRoot();
             break;
        case '2': //添加结点
             AddNode(root);
             break;
        case '3'://先序遍历
             printf("\n先序遍历的结果：");
             BinTree_DLR(root,oper1);
             printf("\n");
             break;
        case '4'://中序遍历
             printf("\n中序遍历的结果：");
             BinTree_LDR(root,oper1);
             printf("\n");
             break;
        case '5'://后序遍历
             printf("\n后序遍历的结果：");
             BinTree_LRD(root,oper1);
             printf("\n");
             break;
        case '6'://按层遍历
             printf("\n按层遍历的结果：");
             BinTree_Level(root,oper1);
             printf("\n");
             break;
        case '7'://二叉树的深度
            printf("\n二叉树深度为:%d\n",BinTreeDepth(root));
            break;
        case '0':
             break;
        }
    }while(select!='0');
    //清空二叉树
    BinTreeClear(root);
    root=NULL;
    getchar();
    return 0;
}
