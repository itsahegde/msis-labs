# quick sort using hoares partition

def partition(a, low, high):
    pivot = a[low]
    left, right = low-1, high+1
    while True:
        left+=1
        while a[left]<pivot:
            left+=1
        right-=1
        while a[right]>pivot:
            right-=1
        if left>=right:
            return right
        a[left], a[right] = a[right], a[left]

def quickort(a, low, high):
    if low<high:
        p = partition(a, low, high)
        quickort(a, low, p)
        quickort(a, p+1, high)

a = [9, 8, 7, 6, 5]
quickort(a, 0, len(a)-1)
print(a)