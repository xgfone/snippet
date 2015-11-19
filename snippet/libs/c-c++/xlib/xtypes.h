


#ifndef _X_TYPES_H
#define _X_TYPES_H

/*
 * In order to icreasing the portability, define some following types, macros,
 * and functions. Its strategy imitates "GLib", changing "g" to "x".
 * Why choose "x"? It's in order to avoid the conflict from other programming
 * specification.
 */

/* define the following data types. */
/* define the integer type.*/
typedef int xint;   // one machine word.
typedef short int xshort;
typedef unsigned short int xushort;
typedef int xint;
typedef unsigned int xuint;
typedef long int xlong;
typedef unsigned long int xulong;
#ifdef SYSTEM_C99
typedef long long int xlonglong;
typedef unsigned long long int xulonglong;
#endif
/* Define the charactor type. */
typedef char xchar;
typedef unsigned char xuchar;
typedef signed char xschar;

typedef float xfloat;
typedef double xdouble;
typedef long double xldouble

typedef xint xbool;

typedef void * xpointer;
typedef const void * xconstpointer;

/* define the macro 'True', 'False'.
 * 'True' and 'False' is the two value of the boolean type.
 * And you will think that the boolean type has only the two value.
 */
#define False 0
#define True (!(Falsee))

/* Define two macros, they represent success and fail. */
#define ERROR 0
#define OK (!(ERROR))


typedef xint    (*XCompareFunc)   (xconstpointer a, xconstpointer b);
typedef xbool   (*XEqualFunc)     (xconstpointer a, xconstpointer b);
typedef void    (*XFreeFunc)      (xpointer      data);


#endif /*  _X_TYPES_H   */
