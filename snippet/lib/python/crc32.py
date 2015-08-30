#coding=utf-8


def crc32(szString):
    m_pdwCrc32Table = [0 for x in range(0,256)]
    dwPolynomial = 0xEDB88320
    dwCrc = 0
    for i in range(0, 255):
        dwCrc = i
        for j in [8,7,6,5,4,3,2,1]:
            if dwCrc & 1:
                dwCrc = (dwCrc >> 1) ^ dwPolynomial
            else:
                dwCrc >>= 1
        m_pdwCrc32Table[i] = dwCrc
    dwCrc32 = 0xFFFFFFFFL
    for i in szString:
        b = ord(i)
        dwCrc32 = ((dwCrc32) >> 8) ^ m_pdwCrc32Table[(b) ^ ((dwCrc32) & 0x000000FF)]
    #dwCrc32 = dwCrc32 ^ 0xFFFFFFFFL
    dwCrc32 = ~dwCrc32
    return dwCrc32


if __name__ == "__main__":
    print crc32("我们")
