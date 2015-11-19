//******************************************************************************
//******************************************************************************
//*    The header file of the Single List                                     **
//*    Copyright (C) 2012       Aaron                                         **
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

#ifndef _X_SLIST_H
#define _X_SLIST_H

#include "xtypes.h"

/*
 * define a structure type. And the variable the type defining will be the
 * elements of the single list. Before using it, you must define The Abstract
 * Data Type(ADT). The ADT is what you will store.
 * You don't need to known this structure and can ignore it completely;
 * You only define a specific type, that's "ADT", which is type which define
 * your data type.
 */
typedef struct _XSingleList{
  ADT data;
  struct _XSingleList *next;
} XSingleList;

/*
 * Define a structure type which is what data type you will use directly.
 * You think it for a container, in which your datas whose type is "ADT" is.
 */
typedef struct _XSList{
  XSingleList *head = NULL;
  XSingleList *tail = NULL;
  xuint length;

  /*
   * 0 represents "No Error", others represents "Error".
   * It is initialized with 0 when a single list be created;
   * from then on, its value will not be changed to 0 by the functions
   * operating the single list, unless you change it by hand.
   * SUGGEST: if you want to check whether a error appears, change its value
   * to 0, then invoke the functions and check its value.
   * Its usage is equal to "error" in standard library.
   * VALUE   MEANING
   *   0    no error.
   *   1    allocating memory failed.
   */
  xint error;
} XSList;


/*
 * Function: x_slist_create.
 * Description: Create a new single list.
 * @Args:  void.
 * Return: If success, return the pointer pointing to the XSList type;
 *         or, return NULL.
 * Others: None.
 */
XSList * x_slist_create();

/*
 * Function: x_slist_clear.
 * Description: Clear all elements of a single list, but not destroy "List".
 * @Args:  List -- a pointer whose type is XSList.
 * Return: void.
 * Others: If "List" is NULL, nothing does.
 */
void x_slist_clear(XSList *List);

/*
 * Function: x_slist_length.
 * Description: Get the number of all elements of a single list.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: Return the number of all elements of a single list.
 * Others: If "List" is NULL, return -1.
 */
xint x_slist_length(XSList *List);

/*
 * Function: x_slist_destroy.
 * Description: Destroy the whole single list, including its elements.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: void.
 * Others: If "List" is NULL, nothing does.
 *         In addition, after calling this function, you must guarantee yourself
 *         that the real parameter is NULL or it isn't used; or, maybe trouble.
 */
void x_slist_destroy(XSList *List);

/*
 * Function: x_slist_is_empty.
 * Description: Judge whether a single list is empty.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: If empty, return True; or, return False.
 *         If "List" is NULL, return True.
 * Others: None.
 */
xbool x_slist_is_empty(XSList *List);

/*
 * Function: x_slist_get_nth.
 * Description: Get the Nth element of a single list.
 * @Args:  List -- a pointer whose type is XSList
 *         n -- a unsigned integer.
 *         elem -- a pointer whose type is ADT to save the element accepted.
 * Return: If found, place it the memory which "elem" points return its pointer
 *         and return the pointer.
 *         If "List" is NULL or empty, or "elem" is NULL, or n is greater than
 *         the number of "List", return NULL and nothing does.
 * Others: None.
 */
ADT *x_slist_get_nth(XSList *List, const xuint n, ADT *elem);

/*
 * Function: x_slist_get_first.
 * Description: Get the first element of a single list.
 * @Args:  List -- a pointer whose type is XSList.
 *         elem -- a pointer whose type is ADT to save the element accepted.
 * Return: If found, place it the memory which "elem" points return its pointer
 *         and return the pointer.
 *         If "List" is NULL or empty, or "elem" is NULL, return NULL and
 *         nothing does.
 * Others: None.
 */
ADT *x_slist_get_first(XSList *List, ADT *elem);

/*
 * Function: x_slist_get_last.
 * Description: Get the last element of a single list.
 * @Args:  List -- a pointer whose type is XSList.
 *         elem -- a pointer whose type is ADT to save the element accepted.
 * Return: If found, place it the memory which "elem" points return its pointer
 *         and return the pointer.
 *         If "List" is NULL or empty, or "elem" is NULL, return NULL and
 *         nothing does.
 * Others: None.
 */
ADT *x_slist_get_last(XSList *List, ADT *elem);

/*
 * Function: x_slist_set_nth.
 * Description: Set the Nth element of a single list to the content which
 *              "elem" points to.
 * @Args:  List -- a pointer whose type is XSList
 *         n -- a unsigned integer.
 *         elem -- a pointer whose type is ADT to save the element setted.
 * Return: void.
 * Others: If "List" is NULL or empty, or "elem" is NULL, or n is greater than
 *         the number of "List", nothing does.
 */
void x_slist_set_nth(XSList *List, const xuint n, const ADT *elem);

/*
 * Function: x_slist_set_first.
 * Description: Set the first element of a single list to the content which
 *              "elem" points to.
 * @Args:  List -- a pointer whose type is XSList
 *         elem -- a pointer whose type is ADT to save the element setted.
 * Return: void.
 * Others: If "List" is NULL or empty, or "elem" is NULL, nothing does.
 */
void x_slist_set_first(XSList *List, const ADT *elem);

/*
 * Function: x_slist_set_last.
 * Description: Set the last element of a single list to the content which
 *              "elem" points to.
 * @Args:  List -- a pointer whose type is XSList
 *         elem -- a pointer whose type is ADT to save the element setted.
 * Return: void.
 * Others: If "List" is NULL or empty, or "elem" is NULL, nothing does.
 */
void x_slist_set_last(XSList *List, const ADT *elem);

/*
 * Function: x_slist_locate_elem.
 * Description: Locate the position of the first elements according to the big
 *              or small relation("relation").
 * @Args:  List -- a pointer whose type is XSList.
 *         elem -- a pointer whose type is ADT, which will be located.
 *         compare -- it is a pointer pointing a function. It is used to judge
 *                    the greater, equal, less relation between two variable
 *                    whose type is ADT. If adt1 is greater than adt2, it
 *                    returns a positive integer; if equal, 0; if less, a
 *                    negative integer.
 *         relation -- a integer, see the following.
 * Return: If "relation" is greater than 0, return the position of the first
 *         element which is greater than "elem".
 *         If "relation" is equal to 0, return the position of the first
 *         element which is equal to "elem".
 *         If "relation" is less than 0, return the position of the first
 *         element which is less than "elem".
 *         If not found, return 0;
 * Others: If "List" is NULL, or "List" is empty, or "elem" is NULL, or
 *         "compare" is NULL, return 0 and nothing does.
 */
xuint x_slist_locate_elem(XSList *List, const ADT *elem,
                          xint (*compare)(cosnt ADT *adt1,
                                          cosnt ADT *adt2),
                          const xint relation);

/*
 * Function: x_slist_insert_nth.
 * Description: Insert the element "elem" into the single list "List" before
 *              the Nth element.
 * @Args:  List -- a pointer whose type is XSList.
 *         n -- a unsigned integer, where "elem" is inserted.
 *         elem -- a pointer whose type is ADT and will be inserted into "List".
 * Return: If success, return True; or, return False.
 *         If "List" is NULL, or the number of the single list is less that n
 *         (but except when n is equal to 1), or "elem" is NULL, or n is equal
 *         to 0, return False and nothing does.
 * Others: If allocating the memory failed, also return False and set
 *         List->error to 1. In case, In case, please check List->error.
 */
xbool x_slist_insert_nth(XSList *List, const xuint n, const ADT *elem);

/*
 * Function: x_slist_insert_first.
 * Description: Insert the element "elem" into the single list("List") before
 *              the first element.
 * @Args:  List -- a pointer whose type is XSList.
 *         elem -- a pointer whose type is ADT and will be inserted into "List".
 * Return: If success, return True; or, return False.
 *         If "List" is NULL, or "elem" is NULL, return False and nothing does.
 * Others: If allocating the memory failed, also return False and set
 *         List->error to 1. In case, In case, please check List->error.
 */
xbool x_slist_insert_first(XSList *List, const ADT *elem);

/*
 * Function: x_slist_insert_last.
 * Description: Insert the element "elem" into the single list("List").
 * @Args:  List -- a pointer whose type is XSList.
 *         elem -- a pointer whose type is ADT and will be inserted into "List".
 * Return: If success, return True; or, return False.
 *         If "List" is NULL, or "elem" is NULL, return False and nothing does.
 * Others: If allocating the memory failed, also return False and set
 *         List->error to 1. In case, please check List->error.
 */
xbool x_slist_insert_last(XSList *List, const ADT *elem);

/*
 * Function: x_slist_remove_nth.
 * Description: Remove the Nth element of the single list and save the deleted
 *              element into the memory which "elem" pointing to.
 * @Args:  List -- a pointer whose type is XSList.
 *         n -- a unsigned integer.
 *         elem --  a pointer whose type is ADT to save the element removed.
 * Return: If success, return the pointer pointing to the element removed.
 *         If "List" is NULL, or the single list is empty, or n is 0, or n is
 *         greater than the number of the elements of "List", or "elem" is
 *         empty, return NULL and nothing does.
 * Others: None.
 */
ADT *x_slist_remove_nth(XSList *List, const xuint n, ADT *elem);

/*
 * Function: x_slist_remove_first.
 * Description: Delete the first element of the single list and save the removed
 *              element into the memory which "elem" pointing to.
 * @Args:  List -- a pointer whose type is XSList.
 *         elem --  a pointer whose type is ADT to save the element removed.
 * Return: If success, return the pointer pointing to the element removed.
 *         If "List" is NULL, or the single list is empty, or n is 0, or n is
 *         greater than the number of the elements of "List", or "elem" is
 *         empty, return NULL and nothing does.
 * Others: None.
 */
ADT *x_slist_remove_first(XSList *List, ADT *elem);

/*
 * Function: x_slist_remove_last.
 * Description: Delete the last element of the single list and save the removed
 *              element into the memory which "elem" pointing to.
 * @Args:  List -- a pointer whose type is XSList.
 *         elem --  a pointer whose type is ADT to save the element removed.
 * Return: If success, return the pointer pointing to the element removed.
 *         If "List" is NULL, or the single list is empty, or n is 0, or n is
 *         greater than the number of the elements of "List", or "elem" is
 *         empty, return NULL and nothing does.
 * Others: None.
 */
ADT *x_slist_remove_last(XSList *List, ADT *elem);

/*
 * Function: x_slist_traverse.
 * Description: Visit each element of the single list.
 * @Args:  List -- a pointer whose type is XSList.
 *         visit -- a function, functioning the each element of the single
 *                  list to visit them.
 * Return: void.
 * Others: If "List" is NULL, or "List" is empty, or "visit" is NULL,
 *         nothing does.
 */
void x_slist_traverse(XSList *List, void (*visit)(ADT *elem));

/*
 * Function: x_slist_reversal.
 * Description: Reverse the elements of the single list.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: void.
 * Others: If "List" is NULL, or the single list is empty, nothing does.
 */
void x_slist_reversal(XSList *List);

/*
 * Function: x_slist_sort_ascend.
 * Description: Sort the single list by ascendingly.
 * @Args:  List -- a pointer whose type is XSList.
 *         compare -- a function, representing the big and small relation of
 *                    two ADT's datas.
 *                    If "adt1" is greater than "adt2", it return a position
 *                    integer;
 *                    If "adt1" is equal to "adt2", it return 0;
 *                    If "adt1" is less than "adt2", it return a negative
 *                    integer.
 * Return: void.
 * Others: If "List" is NULL, or the single list is empty or has only one
 *         element, or "compare" is NULL, nothing does.
 */
void x_slist_sort_ascend(XSList *List,
                         xint (*compare)(const ADT *adt1, const ADT *adt2));

/*
 * Function: x_slist_sort_descend.
 * Description: Sort the single list by descendingly.
 * @Args:  List -- a pointer whose type is XSList.
 *         compare -- a function, representing the big and small relation of
 *                    two ADT's datas.
 *                    If "adt1" is greater than "adt2", it return a position
 *                    integer;
 *                    If "adt1" is equal to "adt2", it return 0;
 *                    If "adt1" is less than "adt2", it return a negative
 *                    integer.
 * Return: void.
 * Others: If "List" is NULL, or the single list is empty or has only one
 *         element, or "compare" is NULL, nothing does.
 */
void x_slist_sort_descend(XSList *List,
                          xint (*compare)(const ADT *adt1, const ADT *adt2));

#endif /*  _X_SLIST_H    */




















