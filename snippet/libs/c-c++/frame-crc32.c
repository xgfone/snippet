/* 以太网帧FCS校验码CRC32的三种实现方法

方法一：按位计算CRC32校验码。

方法二：使用非翻转的查找表进行快速计算，按字节计算CRC32校验码。但计算过程中有位翻转操作，计算速度慢。

方法三：使用翻转的查找表进行快速计算，按字节计算CRC校验码。速度极快。

*/

#include <stdio.h>
#include <stdlib.h>
#include <io.h>




#define alt_8    char
#define alt_u8   unsigned char
#define alt_32   int
#define alt_u32  unsigned int
#define alt_64   long long
#define alt_u64  unsigned long long


//位翻转函数
alt_u64 Reflect(alt_u64 ref,alt_u8 ch)
{
	int i;
	alt_u64 value = 0;
	for( i = 1; i < ( ch + 1 ); i++ )
	{
		if( ref & 1 )
			value |= 1 << ( ch - i );
		ref >>= 1;
	}
	return value;
}


//标准的CRC32多项式
#define poly  0x04C11DB7
//翻转的CRC32多项式
#define upoly 0xEDB88320



alt_u32 crc32_bit(alt_u8 *ptr, alt_u32 len, alt_u32 gx)
{
    alt_u8 i;
	alt_u32 crc = 0xffffffff;
    while( len-- )
    {
        for( i = 1; i != 0; i <<= 1 )
        {
            if( ( crc & 0x80000000 ) != 0 )
			{
				crc <<= 1;
				crc ^= gx;
			}
            else
				crc <<= 1;
            if( ( *ptr & i ) != 0 )
				crc ^= gx;
        }
        ptr++;
    }
    return ( Reflect(crc,32) ^ 0xffffffff );
}






alt_u32 Table1[256];
alt_u32 Table2[256];




 // 生成CRC32 普通表 , 第二项是04C11DB7
void gen_direct_table(alt_u32 *table)
{
	alt_u32 gx = 0x04c11db7;
	unsigned long i32, j32;
	unsigned long nData32;
	unsigned long nAccum32;
	for ( i32 = 0; i32 < 256; i32++ )
	{
		nData32 = ( unsigned long )( i32 << 24 );
		nAccum32 = 0;
		for ( j32 = 0; j32 < 8; j32++ )
		{
			if ( ( nData32 ^ nAccum32 ) & 0x80000000 )
				nAccum32 = ( nAccum32 << 1 ) ^ gx;
			else
				nAccum32 <<= 1;
			nData32 <<= 1;
		}
		table[i32] = nAccum32;
	}
}


// 生成CRC32 翻转表 第二项是77073096
void gen_normal_table(alt_u32 *table)
{
	alt_u32 gx = 0x04c11db7;
	alt_u32 temp,crc;
	for(int i = 0; i <= 0xFF; i++)
	{
		temp=Reflect(i, 8);
		table[i]= temp<< 24;
		for (int j = 0; j < 8; j++)
		{
			unsigned long int t1,t2;
			unsigned long int flag=table[i]&0x80000000;
			t1=(table[i] << 1);
			if(flag==0)
			t2=0;
			else
			t2=gx;
			table[i] =t1^t2 ;
		}
		crc=table[i];
		table[i] = Reflect(table[i], 32);
	}
}



alt_u32 DIRECT_TABLE_CRC(alt_u8 *ptr,int len, alt_u32 * table)
{
	alt_u32 crc = 0xffffffff;
	alt_u8 *p= ptr;
	int i;
	for ( i = 0; i < len; i++ )
		crc = ( crc << 8 ) ^ table[( crc >> 24 ) ^ (alt_u8)Reflect((*(p+i)), 8)];
	return ~(alt_u32)Reflect(crc, 32) ;
}




alt_u32 Reverse_Table_CRC(alt_u8 *data, alt_32 len, alt_u32 * table)
{
	alt_u32 crc = 0xffffffff;
	alt_u8 *p = data;
	int i;
	for(i=0; i <len; i++)
		crc =  table[( crc ^( *(p+i)) ) & 0xff] ^ (crc >> 8);
	return  ~crc ;
}



//这是一个完整的以太网帧。最后四个字节 8b 6b f5 13是其FCS字段，用于与后面生成的CRC32对照
alt_u8  tx_data[] = {
        0xff,   0xff,   0xff,   0xff,   0xff,   0xff,   0x00,   0x1f,   //8
        0x29,   0x00,   0xb5,   0xfa,   0x08,   0x06,   0x00,   0x01,   //15
        0x08,   0x00,   0x06,   0x04,   0x00,   0x01,   0x00,   0x1f,   //24
        0x29,   0x00,   0xb5,   0xfa,   0xac,   0x15,   0x0e,   0xd9,   //32
        0x00,   0x00,   0x00,   0x00,   0x00,   0x00,   0xac,   0x15,   //40
        0x0e,   0x8e,   0x00,   0x00,   0x00,   0x00,   0x00,   0x00,   //48
        0x00,   0x00 ,  0x00,   0x00,   0x00,   0x00,   0x00,   0x00,   //56
        0x00,   0x00,   0x00,   0x00,   0x8b,   0x6b,   0xf5,   0x13    //64
};




int main()
{
    alt_u8 *data = tx_data;
    alt_u8 dataLen = sizeof(tx_data) -4;

	int sum = 256;
	int i = 0;

	//生成普通表，用于直接计算的表
	gen_direct_table(Table1);
	printf("Table1 :\n");
	for( i = 0; i < sum; i++)
	{
		if(i<16)
			printf("%08x ",Table1[i]);
	}
	printf("\n\n");


	//生成翻转表，是官方推荐的，故称其为normal_table
	gen_normal_table(Table2);
	printf("Table2 :\n");
	for( i = 0; i < sum; i++)
	{
		if(i<16)
			printf("%08x ",Table2[i]);
	}
	printf("\n\n");



	printf("dataLen = %d\n",dataLen);//打印数据长度，应该是60字节。



	//计算并打印出CRC32校验码，应该是0x13f56b8b

	//按照bit进行校验，最慢
	printf("Slow CRC by bit          : %08x\n",crc32_bit( data, dataLen, 0x04c11db7 ));
	//使用普通表，非官方，很慢
	printf("Direct Table  ref + xor  : %08x\n",DIRECT_TABLE_CRC (data,dataLen,Table1));
	//使用翻转表，官方推荐的，很快
	printf("Reverse Table  ref + xor : %08x\n",Reverse_Table_CRC(data,dataLen,Table2));


    system("pause");
    return 0;
}
