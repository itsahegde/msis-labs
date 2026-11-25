# insertion sort

def insertionsort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i-1
        while j>=0 and arr[j]>key:
            arr[j+1] = arr[j]
            j-=1
        arr[j+1] = key

arr = [9, 8, 7, 6]
insertionsort(arr)
print(arr)

        
