def partition(arr, low, high):
    pivot = arr[high]
    i = low-1
    for j in range(low, high):
        if arr[j]<=pivot:
            i+=1
            arr[j], arr[i] = arr[i], arr[j]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def sort(arr, low, high):
    if low<=high:
        pi = partition(arr, low, high)
        sort(arr, low, pi-1)
        sort(arr, pi+1, high)
    return arr

arr = [3,4,5,1,9,2,7,0,6]
sort(arr, 0, len(arr)-1)
for i in range(len(arr)):
    print(arr[i])