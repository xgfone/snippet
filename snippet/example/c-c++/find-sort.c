//******************************************************************************
//*程序：查找与排序                                                            *
//*作者：谢高峰                                                                *
//*功能：给定一个静态数据表，完成相关的排序与查找                              *
//*完成时间:2010年12月22日                                                     *
//*不足之处：1.各函数（模块）之间的耦合度太大，有待降低                        *
//*          2.所提供的功能不是很全面、强大，有待补充                          *
//******************************************************************************

#include<stdio.h>
#include<stdlib.h>

//数值型比较
#define EQ(a,b) ((a)==(b))
#define LT(a,b) ((a)< (b))
#define LQ(a,b) ((a)<=(b))
/*//字符串型
#define EQ(a,b) (!strcmp((a),(b)))
#define LT(a,b) (strcmp((a),(b))<0)
#define LQ(a,b) (strcmp((a),(b))<=0)
*/
//定义一些常量
#define OK        1
#define ERROR     0
#define ZERO      0
#define TRUE      1
#define FALSE     0
#define MAX_ARRAY 20

//定义一些类型，便于移值
typedef int Status;
typedef int int32;
typedef int BOOL;
typedef int KeyType;
//typedef double KeyType;
//typedef char * KeyType;
//typedef char * InfoType;

//定义一个类型，用来保存信息
typedef struct
{
    KeyType key;
    //InfoType info;
    char info[MAX_ARRAY];
}SElemType;

//定义一个静态表类型
typedef struct
{
    SElemType *elem;
    int32 length;
}SSTable;
typedef SSTable * QSSTable;

//创建一个空静态表，里面有n个元素
Status Create(QSSTable ST, int32 n)
{
    int32 i=1;
    int32 j=0;
    ST->elem=(SElemType*)malloc(sizeof(SElemType)*(n+1));
    if(!ST->elem)
    {
        printf("\nmemory error!");
        printf("\nPlease enter any key to continue! ");
        getchar();
        exit(1);
    }
    for(i=1; i<=ST->length; ++i)
    {
        for(j=0; j<MAX_ARRAY; ++j)
        {
            ST->elem[i].info[j]='\0';
        }
        ST->elem[i].key=-1;
    }
    ST->length=n;
    return OK;
}

//销毁一个静态表
Status Destroy(QSSTable ST)
{
    free(ST->elem);
    ST->length=0;
    return OK;
}

//打印数据
Status Print(QSSTable ST)
{
    int32 i=1;
    for(i=1; i<=ST->length; ++i)
    {
        printf("\nKEY:%2d ,INFOMATION: %s", ST->elem[i].key, ST->elem[i].info);
    }

    printf("\n");
    return OK;
}

//顺序查找，返回关键字的位置，如果返回0表明找不到
int32 Search_Seq(QSSTable ST, KeyType key)
{
    int32 i=1;
    ST->elem[0].key=key;
    for(i=ST->length; !EQ(ST->elem[i].key,key); --i)
    {}
    return i;
}

//折半查找，在折半查找之前要先进行排序(从小到大)或所要查找的表已是有序表(从小到大)
//返回关键字的位置，如果返回0表明找不到
int32 Search_Bin(QSSTable ST, KeyType key)
{
    int32 low=1;
    int32 high=ST->length;
    int32 mid=0;
    while(low<=high)
    {
        mid=(low+high)/2;
        if(EQ(key,ST->elem[mid].key))
        {
            return mid; //返回关键字的位置
        }
        else if(LT(key,ST->elem[mid].key))
        {
             high=mid-1;
        }
        else
        {
            low=mid+1;
        }
    }

    return ZERO;//返回0位置，表明找不到
}

//冒泡排序，从小到大排序
Status BubbleSort(QSSTable ST)
{
    int32 i=2;
    int32 j=2;
    BOOL change=TRUE;//设置一个标志，如果该标志为FALSE时，表明已按从小到大的顺序排好
    SElemType tmp;
    for(i=ST->length, change=TRUE; i>=1 && change; --i)
    {
        change=FALSE;
        for(j=0; j<i; ++j)
            if(ST->elem[j].key > ST->elem[j+1].key)
            {
                tmp=ST->elem[j];
                ST->elem[j]=ST->elem[j+1];
                ST->elem[j+1]=tmp;

                change=TRUE;
            }
    }
    return OK;
}

//直接插入排序
Status InsertSort(QSSTable ST)
{
    int32 i=2;
    int32 j=1;
    for(i=2; i<=ST->length; ++i)
        if(LT(ST->elem[i].key,ST->elem[i-1].key))
        {
            ST->elem[0]=ST->elem[i];
            ST->elem[i]=ST->elem[i-1];
            for(j=i-2; LT(ST->elem[0].key,ST->elem[j].key); --j)
            {
                ST->elem[j+1]=ST->elem[j];
            }
            ST->elem[j+1]=ST->elem[0];
        }

    return OK;
}

//快速排序的辅助函数
int32 Partition(QSSTable ST, int32 low, int32 high)
{
    KeyType pivotkey=ST->elem[low].key;
    ST->elem[0]=ST->elem[low];
    while(low<high)
    {
        while(low<high && ST->elem[high].key>=pivotkey)
        {
            --high;
        }
        ST->elem[low]=ST->elem[high];
        while(low<high && ST->elem[low].key<=pivotkey)
        {
            ++low;
        }
        ST->elem[high]=ST->elem[low];
    }
    ST->elem[low]=ST->elem[0];
    return low;
}

//快速排序的辅助函数，递归排序
void QSort(QSSTable ST, int32 low, int32 high)
{
     if(low<high)
     {
         int32 pivotloc=Partition(ST, low, high);
         QSort(ST, low, pivotloc-1);
         QSort(ST, pivotloc+1, high);
     }
}

//快速排序的主引擎
void QuickSort(QSSTable ST)
{
     QSort(ST, 1, ST->length);
}

//排序（从大到小）的主界面，要求挑选相应的排序算法
Status Sort(QSSTable ST)
{
    char choice='1';
    printf("\nSort(from small to large):");
    printf("\n1.Bubble Sort     2.Insert Sort");
    printf("\n3.Quick Sort      0.Exit");
    printf("\nPlease choose the choice(0-3): ");
    choice=getchar();
    choice=getchar();
    while(choice<'0' || choice>'3')
    {
        printf("The choice is between 0 and 3.");
        printf("\nPlease choose again!(0-3) ");
        choice=getchar();
        choice=getchar();
    }
    switch(choice)
    {
        case '1':
             BubbleSort(ST);
             break;
        case '2':
             InsertSort(ST);
             break;
        case '3':
             QuickSort(ST);
             break;
        case '0':
             exit(0);
    }
    return OK;
}

//查询的主界面，挑选相应的查询算法
Status Search(QSSTable ST)
{
    int32 position=0;   //保存查询到的关键字的位置
    char choice='1';    //挑选选项变量
    char SORT='y';     //询问是否排序变量
    KeyType key=1;    //要查询的关键字变量
    printf("\nPlease input the key(a integer): ");
    scanf("%d", &key);

    printf("\nSearch:");
    printf("\n1.Sequential Search");
    printf("\n2.Binary Search");
    printf("\n0.Exit");
    printf("\nPlease choose the choice(0-2): ");
    choice=getchar();
    choice=getchar();
    while(choice<'0' || choice>'2')
    {
        printf("The choice is between 0 and 2.");
        printf("\nPlease choose again!(0-2) ");
        choice=getchar();
        choice=getchar();
    }
    switch(choice)
    {
        case '1':
             position=Search_Seq(ST, key);
             break;
        case '2':     //在折半查询之前询问是否对数据排序
             printf("\nBefore searching binary, the key of the data must be sequential!");
             printf("\nWant to SORT?(y or n) ");
             SORT=getchar();
             SORT=getchar();
             while(SORT!='Y' && SORT!='y' && SORT!='N' && SORT!='n')
             {
                 printf("Please input again!(y or n) ");
                 SORT=getchar();
                 SORT=getchar();
             }
             if(SORT=='Y' || SORT=='y')
             {
                 Sort(ST);
             }

             position=Search_Bin(ST, key);
             break;
        case '0':
             exit(0);
    }
    //打印查询结果
    if(position)
    {
        printf("POSITION:%2d, KEY:%2d, INFOMATION: %s", position, key, ST->elem[position].info);
    }
    else
    {
        printf("NO DATA INCLUDING THE KEY(%d)", key);
    }
    printf("\n");
    return OK;
}

//主界面，挑选相应的操作（打印数据、排序、查询、退出）
void home(QSSTable ST)
{
    char choice='1';
    while(1)
    {
        printf("\nThe choice of the operation:");
        printf("\n1.Show the data          2.Sort");
        printf("\n3.Search by the key      0.Exit");
        printf("\nPlease choose the choice(0-3): ");

        choice=getchar();
        choice=getchar();
        while(choice<'0' || choice>'3')
        {
            printf("The choice is between 0 and 3.");
            printf("\nPlease choose again!(0-3) ");
            choice=getchar();
            choice=getchar();
        }//while
        switch(choice)
        {
            case '1':
                 Print(ST);
                 break;
            case '2':
                 Sort(ST);
                 break;
            case '3':
                 Search(ST);
                 break;
            case '0':
                 exit(0);
        }//switch
    }//while
}

int main()
{
    //创建一个静态表实例
    QSSTable test=(SSTable*)malloc(sizeof(SSTable));
    int32 i=1;
    char cont='Y';
    int32 num=10;

    //输入静态数据表中数据的总数（5-99）
    printf("Please input the number of the data(5-99): ");
    scanf("%d", &num);
    while(num<5 || num>99)
    {
        printf("\nPlease input again!(5-99) ");
        scanf("%d", &num);
    }

    Create(test, num);
    //输入静态表的数据
    printf("Please input the information:");
    for(i=1; i<=num; ++i)
    {
        printf("\nPlease input the main key(a integer) of the %dth element(total:%3d): ", i, num);
        scanf("%d", &test->elem[i].key);
        printf("Please input the information of the %dth element(total:%3d): ", i, num);
        scanf("%s", test->elem[i].info);
    }
    //进入操作主界面
    home(test);
    //销毁静态表中的元素
    Destroy(test);
    //销毁静态表实例
    free(test);

    printf("\nPlease enter any key to continue! ");
    getchar();
    return 0;
}
