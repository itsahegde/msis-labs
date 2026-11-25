# selection sort

def selectionsort(arr):
    n = len(arr)
    for i in range(n-1):
        minidx = i
        for j in range(i+1, n):
            if arr[j]<arr[minidx]:
                minidx = j
        arr[i], arr[minidx] = arr[minidx], arr[i]

arr = [9, 8, 7, 6]
selectionsort(arr)
print(arr)
