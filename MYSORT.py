
import time

def myswap(Arr,leftmark,rightmark):
#    if isinstance(Arr[rightmark],int) and isinstance(Arr[leftmark],int) and 0:
#        Arr[rightmark] = Arr[rightmark] + Arr[leftmark]
#        Arr[leftmark]= Arr[rightmark] - Arr[leftmark]
#        Arr[rightmark]= Arr[rightmark] - Arr[leftmark]
#    else:
    temp=Arr[rightmark]
    Arr[rightmark]=Arr[leftmark]
    Arr[leftmark]=temp

def quicksortHelper(Arr,order,first,last):

    if first<last:
        splitpoint=partition(Arr,order,first,last)
        quicksortHelper(Arr,order,first, splitpoint-1)
        quicksortHelper(Arr,order,splitpoint+1, last)

def partition(Arr,order,first,last):

    pivot=Arr[first]
    leftmark=first+1
    rightmark=last

    flag=False
    while not flag:
        while leftmark<=rightmark and Arr[leftmark]<=pivot:
            leftmark=leftmark+1

        while rightmark>=leftmark and Arr[rightmark]>=pivot:
            rightmark=rightmark-1

        if leftmark > rightmark:
            flag=True
        else:
            myswap(Arr,leftmark,rightmark)  #swap the unbalance element
            myswap(order,leftmark,rightmark)

    myswap(Arr,rightmark,first)  #swap the pivot and the element smaller than it
    myswap(order,rightmark,first)

    return rightmark

def quicksort(Arr,order):
    quicksortHelper(Arr,order,first=0,last=len(Arr)-1 )


def bubbleSort(Arr,order):
    for passnum in range(len(Arr)-1,0,-1):
        for i in range(passnum):
            if Arr[i]>Arr[i+1]:
                myswap(Arr,i,i+1)
                myswap(order,i,i+1)
                state=False


def mysort(Arr,*attachArr):
    orderchange=[n for n in range(len( Arr) )]

    if(len(Arr)<1000):
        quicksort(Arr,orderchange)

    else:
        bubbleSort(Arr,orderchange)
    REattach=[]
    for each in attachArr:
        temp=[]
        for c in range( len(each)):
            Ind=orderchange[c]
            temp.append(each[Ind])

        REattach.append(temp)  #the change occurs in each would not change the arr outside the function
    return REattach

#def test():
#    a=[n for n in range(1002)]
#    b=[n for n in range(1002)]
#    c=[n for n in range(1000,1002+1000)]
#    a.reverse()
#    [b]=mysort(a,b)
#    print(b)
