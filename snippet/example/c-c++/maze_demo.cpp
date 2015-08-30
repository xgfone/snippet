
//******************************************************************************
//******************************************************************************
//*程序：maze                                                                 **
//*版本：v-1.4                                                                **
//*作者：Sangay                                                               **
//*功能：迷宫求解                                                             **
//*时间：2010年10月1日—2010年10月3日（编写代码）                             **
//*      2010年11月11日-2010年11月25日（调试并改进代码以及添加某些新功能）    **
//*      2011年11月8日（添加演示模式）                                        **
//*版权：GPL(参见以下声明，更具体的参见http://www.gnu.org/licenses/gpl.html)  **
//*说明：                                                                     **
//*      1、由于C++支持引用和重载以及严格的类型检查，所以本程序使用C++环境，  **
//*         而没有使用C。                                                     **
//*      2、本程序虽然使用C++，但由于本程序是为了模拟栈并利用栈来解决迷宫问   **
//*         题,所以本程序并没有使用C++标准程序库中已经完成的栈实现，而是自已  **
//*         重写了栈(C函数格式的栈)。                                         **
//*      3、本程序在Windows下经过DEV-C++编译并通过检测，但在Visual C++6.0下   **
//*         无法通过，原因是因为VC6.0在for循环的作用域上跟C++标准不一致，如   **
//*         果在Visual C++2003（或2005或2008）下应该能通过。本程序在Linux下   **
//*         也经过GNU C编译器的编译并检测，在该两种平台下运行应该没有问题。   **
//*      4、本程序没有以多文件形式使用工程。原因是：不同编译器使用的工程策略  **
//*         不同，这就导致了只能用特定的编译器；而用这个单个文件形式，不存在  **
//*         这样的问题，在标准的编译器都能编译运行。                          **
//*      5、本程序完全遵守C标准，可以跨平台编译运行。                         **
//*      6、本程序使用了栈，但没有使用栈的全部操作，但为了保持栈操作的全面性, **
//*         本程序保留了栈的所有操作，而不是把没有使用的操作删除。            **
//*      7、本程序使用简单的算法，简单明了。之所以没有采用更直观的可视化界面，**
//*         就是为了保持其简明性，这也使本程序可以用于教学演示当中。          **
//*      8、本程序中有部分代码是永远也不应该被执行的，如果执行的话，表明你运  **
//*         行本程序的环境有问题（比如内存不足等），请检查你的环境。本程序之  **
//*         所以保留它们，是因为为了在逻辑上保持完整性。另外，正如上条所介绍  **
//*         的，本程序可用于教学演示当中，为了使程序更加清楚，所以保留之。    **
//*      9、该程序仍有不足，需要解决的问题：                                  **
//*         (1)求最短(佳）可通路径（注：本迷宫求解求的是一种可能路径，不一定  **
//*            是最短路径）                                                   **
//*         (2)把可通的路径以坐标的形式直观地输出出来（注：本迷宫求解是直接   **
//*            打印迷宫地图来显示所走的路径）                                 **
//*         (3)优化界面，使界面更直观。                                       **
//*         (4)改进程序，如：在随机生成迷宫时，如果用户不满意，还能继续修改； **
//*            可以在运行时导入一个已经存在的伪迷宫模型来初始化迷宫。         **
//*         (5)优化演示模式，使其输出更加直观                                 **
//*         (6)优化程序的性能                                                 **
//******************************************************************************
//******************************************************************************

//******************************************************************************
//******************************************************************************
//*    The programm is maze to solve the maze.                                **
//*    Copyright (C) 2010-2011  Sangay                                        **
//*                                                                           **
//*    This program is free software: you can redistribute it and/or modify   **
//*    it under the terms of the GNU General Public License as published by   **
//*    the Free Software Foundation, either version 3 of the License, or      **
//*    (at your option) any later version.                                    **
//*                                                                           **
//*    This program is distributed in the hope that it will be useful,        **
//*    but WITHOUT ANY WARRANTY; without even the implied warranty of         **
//*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          **
//*    GNU General Public License for more details.                           **
//*                                                                           **
//*    You should have received a copy of the GNU General Public License      **
//*    along with this program.  If not, see <http://www.gnu.org/licenses/>.  **
//*                                                                           **
//*    if you have any questions, please send an Email to me(aaronxgf@126.com)**
//******************************************************************************
//******************************************************************************

//定义演示标志，默认值为FALSE
//如果该标志为真（TRUE），则打开演示模式，即显示求解迷宫时的每一个详细步骤；
//如果该标志为假（FALSE），则关闭演示模式，即正常求解迷宫。
#define DEMO 0

#include<iostream>
#include<cstdlib>
#include<ctime>
#include<iomanip>
#include<cstdio>
using namespace std;

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//                  程序所依赖的一些类型定义以及变量定义                      //
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//定义一些类型和常量，以增强本程序的可移植性
typedef char char_maze;
typedef int int32;
typedef short int16;
typedef unsigned int uint32;
typedef int16 Status;

const int16 OK=1;
const int16 ERROR=0;
const int16 OVERFLOW=-1;
const int16 TRUE=1;
const int16 FALSE=0;

//------------------------------------------------------------------------------
//设置迷宫时所用到的字符，你可以通过修改这些变量来自定义打印迷宫时所显示的样式
//注：为了使其通用性，在改变时请尽量选用标准的ASCII字符

const char_maze START_POS='&';      //迷宫的起始位置标识（&）
const char_maze END_POS='%';        //迷宫的结束位置标识（%）
const char_maze PERIMETER_WALL='#'; //迷宫的外围墙标识（#），在初始化迷宫时设置
const char_maze ROADBLOCK='$';      //迷宫的障碍物标识（$），在初始化迷宫时设置
const char_maze THOROUGHFARE=' ';   //迷宫的可通标识（空格），在初始化迷宫时设置

const char_maze PERVIOUS='*';    //迷宫的可通位置标识（*）
                                 //在求解时设置，表明这位置已经走过并且是可通的

const char_maze NOPERVIOUS='@'; //迷宫的不可通位置标识（@）
                                //在求解时设置，表明这位置已经走过并且不是可通的
//------------------------------------------------------------------------------

// 在演示模式中，每一步求解之后要暂停的时间（以秒为单位），默认值为2秒
// 该作用用在自动过程，但是目前本程序是在演示模式当中是手工进行的，故不需要
//const int16 PAUSE_TIME=2;

//############################################################################//

//定义一个迷宫位置类型，是一个二维的（行和列）
typedef struct
{
    uint32 row;             //迷宫中的行位置
    uint32 column;          //迷宫中的列位置
}PostType;

//定义一个类型，该类型是栈中的元素的类型
typedef struct
{
    PostType seat;             //迷宫中的位置（行和列）
    uint32 order;               //在迷宫中所走的步数
    uint32 nextdirection :3;  //走下一步的方向
}SElemType;

//定义一个栈类型
typedef struct
{
    SElemType *base;          //指向栈的基地址的指针
    SElemType *top;           //指向栈顶的指针
    uint32 StackSize;          //当前栈中已分配的存储空间，以元素为单位
}SqStack;

//定义一个迷宫类型MazeType
//注意：该类型MazeType中的行位置r和列位置c可以用PostType来表示
//但为了在迷宫中清晰，我们重新进行了定义，这没有多大的影响
const uint32 MAXROW=25;      //迷宫最大的行
const uint32 MAXCOL=25;      //迷宫最大的列
typedef struct
{
    uint32 r;               //迷宫中位置所在的行
    uint32 c;               //迷宫中位置所在的列

    //定义一个二维迷宫
    //其中的元素代表着不可通（有障碍物）、可通、已走过（是否可通）等等
    char_maze mazemap[MAXROW+1][MAXCOL+1];

}MazeType;

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//                           栈部分的开始                                     //
////////////////////////////////////////////////////////////////////////////////
//说明：本栈的存储与实现借鉴通用泛型算法思想，如果想使用本栈的相关操作，请    //
//      在本栈使用之前，先声明（或定义）本栈中的元素的类型（SElemType），之   //
//      后即可使用。本栈实现的操作有：初始化栈、销毁栈、清空栈、判断栈是否    //
//      为空、取栈顶的元素、把一个元素压入栈中、删除栈顶的元素（按是否返回    //
//      删除的元素分为两种）、计算栈中元素的个数等等等。                      //
//使用事项：在定义一个栈对象（变量）时，先要使用初始化函数初始化栈对象，然    //
//          后才能使用栈的各种操作。当栈对象不再使用时，要明确地调用销毁函    //
//          数来销毁栈，否则，将会出现"内存泄漏"，这由使用者自己保证。        //
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

//定义两个常量，用来初始化栈的大小以及增加栈大小时的速率
const uint32 STACK_INIT_SIZE=100;  //栈的初始化大小
const uint32 STACK_INCREMENT=10;    //栈大小增加时每次增加的大小

//############################################################################//
//对栈进行初始化为空，预分配STACK_INIT_SIZE个大小的空间
//栈顶标记的是没有元素的（就算是有，我们认为它们是无用值，认为它们为空、不存在）
Status InitSqStack(SqStack &q)
{
    q.base=new SElemType[STACK_INIT_SIZE];
    if(!q.base)
    {
        return ERROR;
    }

    q.top=q.base;
    q.StackSize=STACK_INIT_SIZE;
    return OK;
}
//############################################################################//
//销毁栈
Status DestroySqStack(SqStack &q)
{
    delete [] q.base;
    q.base=q.top=0;
    q.StackSize=0;
    return OK;
}
//############################################################################//
//把栈S设置为空
Status ClearStack(SqStack &q)
{
    q.top=q.base;
    q.StackSize=0;
    return OK;
}
//############################################################################//
//判断一个栈是否为空，若是则返回OK，否则返回ERROR
Status StackEmpty(const SqStack &q)
{
    if(q.top==q.base)
    {
        return TRUE;
    }
    else
    {
        return FALSE;
    }
}
//############################################################################//
//若栈不空，则用e返回栈q的栈顶元素，并返回OK；否则返回ERROR。
Status GetTop(SqStack &q, SElemType &e)
{
    if(StackEmpty(q))
    {
        return ERROR;
    }
    else
    {
        e=*--q.top;
        ++q.top;    //调回栈顶的指针，以不改变原栈中的元素的个数
        return OK;
    }
}
//############################################################################//
//把一个SElemType类型的元素e压入栈q中
//栈顶标记的是没有元素的（就算是有，我们认为它们是无用值，认为它们为空、不存在）
Status Push(SqStack &q, const SElemType &e)
{
  if(q.top-q.base >= static_cast<int32>(q.StackSize-1))
    {
        SElemType *p=new SElemType[q.StackSize+STACK_INCREMENT];
        if(!p)
        {
            return ERROR;
        }

        for(uint32 i=0; i<=q.StackSize-2; ++i)
        {
            p[i]=q.base[i]; //如果该行编译或运行时发生错误，
                            //可用下面来测试是否可行，但这是针对于本迷宫测试程序
                            /*  p[i].seat.row=q.base[i].seat.row;
                                p[i].seat.column=q.base[i].seat.column;
                                p[i].order=q.base[i].order;
                                p[i].StackSize=q.base[i].StackSize;
                            */
        }
        delete [] q.base;
        q.base=p;
        q.top=q.base+q.StackSize-1;
        q.StackSize+=STACK_INCREMENT;
    }

    *q.top++ = e;
    return OK;
}
//############################################################################//
//若栈不空，把一个栈顶中的元素删除，并用e来返回
//栈顶标记的是没有元素的（就算是有，我们认为它们是无用值，认为它们为空、不存在）
Status Pop(SqStack &q, SElemType &e)
{
    if(q.top==q.base)
    {
        return ERROR;
    }

    e=*--q.top;
    return OK;
}
//############################################################################//
//重载函数Pop，不用e来返回删除的元素
Status Pop(SqStack &q)
{
    if(q.top==q.base)
    {
        return ERROR;
    }
    --q.top;
    return OK;
}

//############################################################################//
//返回一个栈的元素个数，即栈的长度
uint32 StackLength(const SqStack &q)
{
    //if判断没必要，因为我们知道q.top-q.base肯定不小于0，
    //但为了把所有的结果范围考虑进去，我们这样做了，
    //这在性能上会有所影响，但在整体上无关紧要，所以我们可以这么做。
    if(q.top-q.base<0)
    {
        return ERROR;
    }
    else
    {
        return q.top-q.base;
    }
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//                             栈部分的结束                                   //
////////////////////////////////////////////////////////////////////////////////
void PrintMaze(const MazeType &maze);
////////////////////////////////////////////////////////////////////////////////
//                          迷宫规格部分的开始                                //
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

//随机设置障碍物
//本函数处于调试状态
Status RandSetRoadblock(MazeType &maze)
{
    //动态分配一个二维数组，用来随机设置迷宫障碍物，然后赋值给 maze
    int32 **judge=new int32*[maze.r-2];
    for(uint32 i=0; i<=maze.r-3; ++i)
    {
        judge[i]=new int32[maze.c-2];
    }

    //把迷宫地图二维数组里各元素的值随机设为0或1
    srand((unsigned)time(0));
    for(uint32 i=0; i<=maze.r-3; ++i)
        for(uint32 j=0; j<=maze.c-3; ++j)
        {
            judge[i][j]=rand()%2;
        }

    //如果judge[i][j]的值为0，就把maze.mazemap[++i][++j]的值设为THOROUGHFARE的值（可通）
    //如果judge[i][j]的值为1，就把maze.mazemap[++i][++j]的值设为ROADBLOCK的值（不通）
    for(uint32 i=0; i<=maze.r-3; ++i){
        for(uint32 j=0; j<=maze.c-3;++j)
            if(judge[i][j]==1)
            {
                ++i;  ++i;
                ++j;  ++j;
                maze.mazemap[i][j]=ROADBLOCK;
                --i;  --i;
                --j;  --j;
            }
            else if(judge[i][j]==0)
            {
              //
            }
            else   //理论上这段代码永远不应该被执行，如若执行，前面代码有问题
                   //之所以加入这一段代码，是为了与前面的if-else相对应，保持逻辑上的完整性。
            {
                //销毁动态分配的内存
                for(uint32 m=0; m<=maze.r-3; ++m)
                {
                    delete [] judge[m];
                }
                delete [] judge;

                return OVERFLOW;
            }

    }

    //销毁动态分配的内存
    for(uint32 m=0; m<=maze.r-3; ++m)
    {
        delete [] judge[m];
    }
    delete [] judge;

    return OK;
}
//############################################################################//
//手动设置障碍物
Status ManualSetRoadblock(MazeType &maze)
{
    int32 m=1;     //表示障碍物所在的行
    int32 n=1;     //表示障碍物所在的列
    bool flag=true;  //设置循环标志，如果为“真”则继承循环，否则结束循环
    do{
        PrintMaze(maze);
        cout<<"Please input the roadblock coordinate of the maze(end with(0,0)):";
        cin>>m>>n;
        while(m<0 || n<0)
	    {
	        cout<<"\nm or n can not be less than zero!\n"
	            <<"Please input m and n again! ";
	        cin>>m>>n;
	    }

        if(m==0  || n==0)
        {
            flag=false;
        }
        else if(m>=2 || m<=static_cast<int32>(maze.r)-1 ||
                n>=2 || n<=static_cast<int32>(maze.c)-1 )
        {
            maze.mazemap[m][n]=ROADBLOCK;
        }
        else
        {
            //如果不在可设置的范围内则返回OVERFLOW（溢出）
            return OVERFLOW;
        }
    }while(flag);

    return OK;
}
//############################################################################//
//默认设置障碍物，即行和列都是奇数的位置被设置成障碍物，其他的位置设置为"可通"
Status DefaultSetRoadblock(MazeType &maze)
{
    for(uint32 i=2; i<=maze.r-1; ++i)
        for(uint32 j=2; j<=maze.c-1; ++j)
            if(i%2==1 && j%2==1)
            {
                maze.mazemap[i][j]=ROADBLOCK;
            }
    return OK;
}
//############################################################################//
//初始化迷宫地图
Status InitMaze(MazeType &maze)
{
    //设定外围墻的行数
    do
    {
        cout<<"Please input the row(6-"<<MAXROW<<")of the maze:";
        cin>>maze.r;
    }while(maze.r>MAXROW || maze.r<6);
    //设定外围墻的列数
    do
    {
        cout<<"Please input the column(6-"<<MAXCOL<<")of the maze:";
        cin>>maze.c;
    }while(maze.c>MAXCOL || maze.c<6);

    //初始化行外围墻
    for(uint32 i=1; i<=maze.c; ++i)
    {
        maze.mazemap[1][i]=PERIMETER_WALL;
        maze.mazemap[maze.r][i]=PERIMETER_WALL;
    }
    //初始化列外围墻
    for(uint32 i=2; i<=maze.r-1; ++i)
    {
        maze.mazemap[i][1]=PERIMETER_WALL;
        maze.mazemap[i][maze.c]=PERIMETER_WALL;
    }

    //把除外围墙外其他位置均设置成空（即可通）
    for(uint32 i=2; i<=maze.r-1; ++i)
        for(uint32 j=2; j<=maze.c-1; ++j)
        {
            maze.mazemap[i][j]=THOROUGHFARE;
        }

  //  PrintMaze(maze);

    cout<<"\nPlease choose the options:\n"
        <<"1.Set acquiescently the roadblock\n"
        <<"2.Set random the roadblock\n"
        <<"3.Set manually the roadblock\n"
        <<"0.Exit\n\n\n"
        <<"The option which you choose(0-3): ";
    char choose_option='1';
    cin>>choose_option;
    while('3'<choose_option || choose_option<'0')
    {
        cout<<"Please choose(0-3): ";
        cin>>choose_option;
    }

    switch(choose_option)
    {
        case '1':
             DefaultSetRoadblock(maze);
             break;
        case '2':
             RandSetRoadblock(maze);
             break;
        case '3':
             ManualSetRoadblock(maze);
             break;
        case '0':
             exit(0);
        default: //理论上，这段代码永远不应该被执行；但为了保持完整性，加入了这段代码
             return ERROR;
    }
    return OK;
}
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//                             迷宫规格的结束                                 //
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
//                             迷宫求解的开始                                 //
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//打印迷宫地图，并显示一条可通的路径
void PrintMaze(const MazeType &maze)
{
    cout<<"\nShow the path of the maze:\n"
        <<"Instruction:\""<<PERIMETER_WALL<<"\" express the enclosure\n"
        <<"            \""<<ROADBLOCK<<"\" express the roadblock\n"
        <<"            \""<<THOROUGHFARE<<"\" express the access\n"
        <<"            \""<<PERVIOUS<<"\" express the access went across\n";
#if DEMO
    cout<<"            \""<<START_POS<<"\" express the starting position\n"
        <<"            \""<<END_POS<<"\" express the end position\n"
        <<"            \""<<NOPERVIOUS<<"\" express the access didn't go across\n"
        <<endl;
#endif

    //打印列名那一行中的第一个位置，其值应该是一个空格，
    //该位置所对应的这一列是用来打印行号的
    cout<<setw(3)<<" ";

    //打印列号
    for(uint32 i=1; i<=maze.c; ++i)
    {
        cout<<setw(3)<<i;
    }
    cout<<endl<<endl;

    //打印行号和迷宫内容
    for(uint32 i=1; i<=maze.r; ++i)
    {
        cout<<setw(3)<<i;
        for(uint32 j=1; j<=maze.c; ++j)
        {
            cout<<setw(3)<<maze.mazemap[i][j];
        }
        cout<<endl;
    }
}
//############################################################################//
//测试当前位置是否可通，如果可通则返回TRUE，否则返回FALSE
Status Pass(const MazeType &maze, const PostType &curpos)
{
    if(maze.mazemap[curpos.row][curpos.column]==THOROUGHFARE ||
       maze.mazemap[curpos.row][curpos.column]==START_POS ||
       maze.mazemap[curpos.row][curpos.column]==END_POS )
    {
        return TRUE;
    }
    else
    {
        return FALSE;
    }
}
//############################################################################//
//如果当前位置可通则把当前位置设为*
//当前位置是否可通，使用者必须自己保证，这里不做检查
Status FootPrint(MazeType &maze, const PostType &curpos)
{

    if(START_POS == maze.mazemap[curpos.row][curpos.column]  ||
       END_POS == maze.mazemap[curpos.row][curpos.column]) {
       //NOTHING
    }
    else{
        maze.mazemap[curpos.row][curpos.column]=PERVIOUS;
    }
    return OK;
}
//############################################################################//
//如果当前位置不可通则把当前位置设为@
//当前位置是否不可通，使用者必须自己保证，这里不做检查
Status BlockPrint(MazeType &maze, const PostType &curpos)
{
    maze.mazemap[curpos.row][curpos.column]=NOPERVIOUS;
    return OK;
}
//############################################################################//
//通过方向（1、2、3、4分别代表东、南、西、北）选取下一个位置
//如果返回的下一个位置是（0，0），则代表着返回一个错误值
PostType NextPost(PostType &curpos, const uint32 &direction)
{
    PostType nextpos=curpos;
    switch(direction)
    {
        case 1:
             nextpos.column++;
             break;
        case 2:
             nextpos.row++;
             break;
        case 3:
             nextpos.column--;
             break;
        case 4:
             nextpos.row--;
             break;
        default:
             PostType ErrorPost;
             ErrorPost.row=0;
             ErrorPost.column=0;
             return ErrorPost;
    }

    return nextpos;
}
//############################################################################//
//寻找从迷宫入口到迷宫出口的可通路径，如果找到了则返回OK，否则返回ERROR
Status MazePath(MazeType &maze, PostType start, PostType end)
{
    SqStack S;                //定义一个栈，用来保存可通的路径
    InitSqStack(S);           //初始化栈
    PostType curpos=start;    //定义一个变量，用来保存当前路径的位置
    uint32 curstep=1;         //保存当前可能路径坐标的个数
    SElemType e;              //定义一个栈元素，用来入栈出栈

    maze.mazemap[start.row][start.column]=START_POS;  //初始化迷宫的起始位置
    maze.mazemap[end.row][end.column]=END_POS;        //初始化迷宫的结束位置

    do
    {
#if DEMO
    while(getchar() != '\n');
    PrintMaze(maze);
    if(curstep==1){
        cout<<"The starting position (i.e. the entrance): ("<<curpos.row<<", "
            <<curpos.column<<")!\n";
    }
    else{
        cout<<"The position which will be tested is ("<<curpos.row<<", "
            <<curpos.column<<")!\n";
    }
    cout<<"Please press ENTER to continue! ";
#endif
        if(Pass(maze, curpos))
        {
            FootPrint(maze, curpos);
            //以下两行可以合并写成e.seat=curpos;
            e.seat.row=curpos.row;
            e.seat.column=curpos.column;
            e.order=curstep;
            e.nextdirection=1;

            Push(S, e);
            if(curpos.row==end.row && curpos.column==end.column)
            {
                DestroySqStack(S);
            #if !DEMO
                for(uint32 i=2; i<=maze.r-1; ++i)
                    for(uint32 j=2; j<=maze.c-1; ++j)
                        if(maze.mazemap[i][j]==NOPERVIOUS)
                        {
                            maze.mazemap[i][j]=THOROUGHFARE;
                        }
            #endif
                return OK;
            }

            curpos=NextPost(curpos, 1);
            ++curstep;
        }
        else
        {
            if(!StackEmpty(S))
            {
                Pop(S, e);
                while(e.nextdirection==4 && !StackEmpty(S))
                {
                    BlockPrint(maze, e.seat);
                    Pop(S,e);
                }
                if(e.nextdirection<4)
                {
                    ++e.nextdirection;
                    Push(S,e);
                    curpos=NextPost(e.seat, e.nextdirection);
                }
            }

        }
    }while(!StackEmpty(S));
    DestroySqStack(S);
    return ERROR;
}
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//                        迷宫求解部分的结束                                  //
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
//                        迷宫测试部分的开始                                  //
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

//版权说明
void Copyright()
{
    cout<<"\n"
        <<"The programm is maze to solve the maze.\n"
        <<"Copyright (C) 2010  Aaron xie\n\n"
        <<"This program is free software: you can redistribute it and/or modify\n"
        <<"it under the terms of the GNU General Public License as published by\n"
        <<"the Free Software Foundation, either version 3 of the License, or\n"
        <<"(at your option) any later version.\n\n"
        <<"This program is distributed in the hope that it will be useful,\n"
        <<"but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
        <<"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
        <<"GNU General Public License for more details.\n\n"
        <<"You should have received a copy of the GNU General Public License\n"
        <<"along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n"
        <<"if you have any questions, please send an e-mail to me(aaronxgf@163.com).\n\n\n";
}
//############################################################################//
//程序标题
void Headline()
{
    //输出标题
    cout<<setw(22)<<" ";
    for(int32 i=1; i<=6; ++i)
        cout<<static_cast<char>(i)<<" ";
    cout<<"MAZE SOLVING";
    for(int32 i=6; i>=1; --i)
        cout<<" "<<static_cast<char>(i);
    cout<<endl<<endl;

    return;
}
//############################################################################//
//测试迷宫
void MazeTest()
{
    Headline();
    //打印版权
    Copyright();
    cout<<setw(40)<<"LET'S GO!\n\n";
    //char pause='0';

    //定义一个迷宫实例对象
    MazeType maze_instance;
    if(!InitMaze(maze_instance))
    {
        cout<<"\nInitializatopn of the maze error!\n";
        char test=' ';
        cout<<"\nPlease enter any key to continue!\n";
        cin.get(test);
        exit(ERROR);
    }

    //打印迷宫地图
    PrintMaze(maze_instance);

    //定义迷宫的入口位置
    PostType start_post;
    //定义迷宫的出口位置
    PostType end_post;

    do
    {
        cout<<"Please input the entrance of the maze(Two-dimensional coordinate): ";
        cin>>start_post.row>>start_post.column;
        if(start_post.row<=1 || start_post.row>=maze_instance.r ||
           start_post.column<=1 || start_post.column>=maze_instance.c)
        {
            cout<<"\nBeyond the maze!\n";
            //超出迷宫的范围时继续输入
            continue;
        }

        if(!Pass(maze_instance, start_post))
        {
            cout<<"\nThe entrance is not transitable\n";
            continue;
        }

        //退出循环输入
        break;
    }while(true);

    do{
        cout<<"Please input the exit of the maze(Two-dimensional coordinate): ";
        cin>>end_post.row>>end_post.column;
        if(end_post.row<=1 || end_post.row>=maze_instance.r ||
           end_post.column<=1 || end_post.column>=maze_instance.c)
        {
            cout<<"\nBeyond the maze!\n";
            //超出迷宫的范围时继续输入
            continue;
        }

        if(!Pass(maze_instance, end_post))
        {
            cout<<"\nThe exit is not transitable\n";
            continue;
        }
        //退出循环输入
        break;
    }while(true);

//迷宫求解
#if DEMO
    if(!MazePath(maze_instance, start_post, end_post))
    {
        cout<<"\nNo path about the maze frome the entrance ("
            <<start_post.row<<", "<<start_post.column<<") to the exit ("
            <<end_post.row<<", "<<end_post.column<<")!\n";
    }
    else
    {
        PrintMaze(maze_instance);
        cout<<"\nYou can walk from the the entrance ("
            <<start_post.row<<", "<<start_post.column<<") to the exit ("
            <<end_post.row<<", "<<end_post.column<<")!\n";
    }
#else
    if(!MazePath(maze_instance, start_post, end_post))
    {
        cout<<"\n\nNo path about the maze frome the entrance ("
            <<start_post.row<<", "<<start_post.column<<") to the exit ("
            <<end_post.row<<", "<<end_post.column<<")!\n";
    }
    else
    {
        cout<<"\n\nYou can walk from the the entrance ("
            <<start_post.row<<", "<<start_post.column<<") to the exit ("
            <<end_post.row<<", "<<end_post.column<<")!\n";
        PrintMaze(maze_instance);
    }
#endif

    return;
}
//############################################################################//
//是否循环测试
void LoopTestMaze()
{
    char decide_continue='n';
    do{
        MazeTest();
        do
        {
            cout<<"\ncontinue(y or n)? ";
            cin>>decide_continue;
            if(decide_continue!='y' && decide_continue!='Y' &&
               decide_continue!='n' && decide_continue!='N' )
            {
                cout<<"Please input 'y' or 'n'!('y' or 'n') ";
                continue;
            }
            break;
        }while(true);
    }while(decide_continue=='Y' || decide_continue=='y');
    return;
}
void Test()
{
    LoopTestMaze();
}
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//                         迷宫测试部分的结束                                 //
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
//                              驱动程序                                      //
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
int main()
{
    Test();
    return 0;
}
//############################  程序结束  ####################################//
