
//******************************************************************************
//******************************************************************************
//*    The implemention file of the Single List                               **
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

#include "xslist.h"

/*
 * Function: x_slist_create.
 * Description: Create a new single list.
 * @Args:  void.
 * Return: If success, return the pointer pointing to the XSList type;
 *         or, return NULL.
 * Others: None.
 */
XSList * x_slist_create()
{
  XSList *List = (XSList *)malloc(sizeof(XSList));
  if (List == NULL){
    return NULL;
  }else{
    List->head = NULL;
    List->tail = NULL;
    List->length = 0;
    List->error = 0;
    return List;
  }
}

/*
 * Function: x_slist_clear.
 * Description: Clear all elements of a single list, but not destroy "List".
 * @Args:  List -- a pointer whose type is XSList.
 * Return: void.
 * Others: If "List" is NULL, nothing does.
 */
void x_slist_clear(XSList *List)
{
  XSingleList *p = NULL; // visit each element of "List"
  XSingleList *q = NULL; // point to the element be deleting
  if (List == NULL){
    return;
  }
  p = List->head;
  while (p != NULL){
    q = p;
    p = p->next;
    List->head = p; // In order to prevent some other actions from breaking it.
    free(q);
    --List->length; // In order to prevent some other actions from breaking it.
  }
  List->length = 0;
  List->tail = NULL;
  List->head = NULL;
}

/*
 * Function: x_slist_length.
 * Description: Get the number of all elements of a single list.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: Return the number of all elements of a single list.
 * Others: If "List" is NULL, return -1.
 */
xint x_slist_length(XSList *List)
{
  if (List == NULL){
    return -1;
  }
  else {
    return (xint)List->length;
  }
}

/*
 * Function: x_slist_destroy.
 * Description: Destroy the whole single list, including its elements.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: void.
 * Others: If "List" is NULL, nothing does.
 *         In addition, after calling this function, you must guarantee yourself
 *         that the real parameter is NULL or it isn't used; or, maybe trouble.
 */
void x_slist_destroy(XSList *List)
{
  if (List == NULL){
    return;
  }
  x_clear_slist(List);
  free(List);
}

/*
 * Function: x_slist_is_empty.
 * Description: Judge whether a single list is empty.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: If empty, return True; or, return False.
 *         If "List" is NULL, return True.
 * Others: None.
 */
xbool x_slist_is_empty(XSList *List)
{
  if (List == NULL || List->length == 0){
    return True;
  }
  return False;
}


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
ADT *x_slist_get_nth(XSList *List, const xuint n, ADT *elem)
{
  xint i;
  XSingleList *p;   // point to the element being getting.
  if (List == NULL || n == 0 || n > List->length || elem == NULL){
    return NULL;
  }

  if (n == List->length){
    *elem = List->tail->data;
    return elem;
  }

  if (n == 1){
    *elem = List->head->data;
    return elem;
  }

  p = List->head;
  for (i = 2; i <= n; ++i){
    p = p->next;
  }
  *elem = p->data;
  return elem;
}

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
ADT *x_slist_get_first(XSList *List, ADT *elem)
{
  return s_slist_get_nth(List, 1, elem);
}

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
ADT *x_slist_get_last(XSList *List, ADT *elem)
{
  if (List == NULL || List->length == 0 || elem == NULL){
    return NULL;
  }
  *elem = List->tail->data;
  return elem;
}

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
void x_slist_set_nth(XSList *List, const xuint n, const ADT *elem)
{
  XSingleList *p;
  xuint i;

  if (List == NULL || n == 0 || n > List->length || elem == NULL){
    return;
  }

  if (n == 1){  // set the first element.
    List->head->data = *elem;
    return;
  }
  if (n == List->length){ // set the last element.
    List->tail->data = *elem;
    return;
  }

  // find the Nth element and set.
  for (i = 1, p = List->head; i <= n; ++i){
    p = p->next;
  }
  p->data = *elem;
  return;
}

/*
 * Function: x_slist_set_first.
 * Description: Set the first element of a single list to the content which
 *              "elem" points to.
 * @Args:  List -- a pointer whose type is XSList
 *         elem -- a pointer whose type is ADT to save the element setted.
 * Return: void.
 * Others: If "List" is NULL or empty, or "elem" is NULL, nothing does.
 */
void x_slist_set_first(XSList *List, const ADT *elem)
{
  x_slist_set_nth(List, 1, elem);
}

/*
 * Function: x_slist_set_last.
 * Description: Set the last element of a single list to the content which
 *              "elem" points to.
 * @Args:  List -- a pointer whose type is XSList
 *         elem -- a pointer whose type is ADT to save the element setted.
 * Return: void.
 * Others: If "List" is NULL or empty, or "elem" is NULL, nothing does.
 */
void x_slist_set_last(XSList *List, const ADT *elem)
{
  x_slist_set_nth(List, List->length, elem);
}

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
                          const xint relation)
{
  XSingleList *p;
  xuint i;

  if (List == NULL || List->length == 0 || elem == NULL || compare == NULL){
    return 0;
  }

  for (i = 1, p = List->head; i <= List->length && p != NULL; ++i, p = p->next){
    if (ADT_comp(p->data, *elem)  0){
      return i;
    }
  }

  return 0;
}

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
xbool x_slist_insert_nth(XSList *List, const xuint n, const ADT *elem)
{
  XSingleList *p;  // point to the element being inserted.
  XSingleList *q;  // point to the (N-1)th element, that's the (N-1)th position
  xuint i;

  if (List == NULL || n <= 0 || elem == NULL){
    return False;
  }

  if (n == 1){  // Insert the element into the first position.
    p  = (XSingleList *)malloc(sizeof(XSingleList));
    if (p == NULL){
      List->error = 1;
      return False;
    }
    p->data = *elem;
    p->next = List->head;
    List->head = p;
    return True;
  }
  else {  // Insert the element into the other position except first.

    // n must not be greater than List->length.
    if (List->length < n){
      return False;
    }

    p  = (XSingleList *)malloc(sizeof(XSingleList));
    if (p == NULL){
      List->error = 1;
      return False;
    }
    p->data = *elem;

    // Find the Nth element, that's the Nth position, and insert element.
    q = List->head;
    if (n == 2){   // Insert the element into the second position.
      p->next = q->next;
      q->next = p;
      return True;
    }

    // Insert the element into the other position from the third position on.
    for (i = 2; i < n; ++i){
      q = q->next;
    }
    p->next = q->next;
    q->next = p;

    return True;
  }
}

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
xbool x_slist_insert_first(XSList *List, const ADT *elem)
{
  return x_slist_insert_elem(List, 1, elem);
}


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
xbool x_slist_insert_last(XSList *List, const ADT *elem)
{
  XSingleList *p;

  if (List == NULL || elem == NULL){
    return False;
  }

  p = (XSingleList *)malloc(sizeof(XSingleList));
  if (p == NULL){
    List->error = 1;
    return False;
  }
  p->data = *elem;
  p->next = NULL;

  if (List->length == 0){
    List->head = p;
  }
  else {
    List->tail->next = p;
  }
  List->tail = p;
  return True;
}


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
ADT *x_slist_remove_nth(XSList *List, const xuint n, ADT *elem)
{
  XSingleList *p; // point to the (N-1)th elelemt.
  XSingleList *q; // point to the Nth element, that's the element being reomved
  xuint i;

  if (List == NULL || n == 0 || List->length < n || elem == NULL){
    return NULL;;
  }

  p = List->head;
  q = List->head;
  // when the number of "List" is 1, remove the first element.
  if (List->length == 1){
    List->tail = NULL;
    List->head = NULL;
  }
  else { // when the number of "List" is greater than 1.
    if (n == 1){    // remove the first element.
      List->head = q->next;
    }
    else if (n == 2){ // remove the second element.
      q = p->next;
      p->next = q->next;
    }
    else { // remove the other element from the third element on.
      for (i = 2; i < n; ++i){
        p = p->next;
      }
      q = p->next;
      p->next = q->next;
    }
  }

  // remove element really.
  *elem = q->data;
  free(q);
  --List->length;
  return elem;
}


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
ADT *x_slist_remove_first(XSList *List, ADT *elem)
{
  return x_slsit_remove_nth(List, 1, elem);
}


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
ADT *x_slist_remove_last(XSList *List, ADT *elem)
{
  return x_slist_remove_elem(List, List->length, elem);
}


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
void x_slist_traverse(XSList *List, void (*visit)(ADT *elem))
{
  XSingleList *p;  // visit each element of "List".
  if (List == NULL || List->length == 0 || visit == NULL){
    return;
  }
  p = List->head;
  while (p == NULL){
    visit(&(p->data));
    p = p->next;
  }
}

/*
 * Function: x_slist_reversal.
 * Description: Reverse the elements of the single list.
 * @Args:  List -- a pointer whose type is XSList.
 * Return: void.
 * Others: If "List" is NULL, or the single list is empty, nothing does.
 */
void x_slist_reversal(XSList *List)
{
  XSingleList *p;  // point to the element being performed reversal on.
  XSingleList *q;  // point to the first element for ever.
  if (List == NULL || List->length == 0){
    return;
  }

  p = List->head->next;
  q = List->head;
  while (p == NULL){
    List->head->next = p->next;
    p->next = q;
    q = p;
    p = List->head->next;
  }

  /* Correct the head and tail. At the moment, List->tail points to the
   * first element, and List->head points to the last element.
   */
  List->tail = List->head;
  List->head = q;
}

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
                         xint (*compare)(const ADT *adt1, const ADT *adt2))
{
  XSingleList *p;
  XSingleList *q;
  XSingleList *min;
  ADT tmp;
  if (List == NULL || List->length == 0 ||
      List->length == 1 || compare == NULL){
    return;
  }

  // the choice sort.
  for (p = List->head; p != List->tail; p = p->next){
    min = p;
    for (q = p->next; q != NULL; q = q->next){
      if (compare(p->data, q->data) > 0){
        min = q;
      }
    }

    /*
     * I don't find a good way to exchange these datas,
     * so choose this way ----- Move Datas.
     */
    if (min != p){
      tmp = min->data;
      min->data = p->data;
      p->data = tmp;
    }
  }
}

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
                          xint (*compare)(const ADT *adt1, const ADT *adt2))
{
  XSingleList *p;
  XSingleList *q;
  XSingleList *max;
  ADT tmp;
  if (List == NULL || List->length == 0 ||
      List->length == 1 || compare == NULL){
    return;
  }

  for (p = List->head; p != List->tail; p = p->next){
    max = p;
    for (q = p->next; q != NULL; q = q->next){
      if (compare(p->data, q->data) < 0){
        max = q;
      }
    }

    /*
     * I don't find a good way to exchange these datas,
     * so choose this way ----- Move Datas.
     */
    if (max != p){
      tmp = max->data;
      max->data = p->data;
      p->data = tmp;
    }
  }
}
