def sort(arr):
    for i in range(len(arr)-1):
        minidx = i
        for j in range(i+1, len(arr)):
            if arr[j]<arr[minidx]:
                minidx = j
        arr[i], arr[minidx] = arr[minidx], arr[i]
    for i in range(len(arr)):
        print(arr[i])

arr = [3,4,5,1,9,2,7,0,6]
sort(arr)