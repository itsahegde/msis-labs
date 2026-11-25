def binarysearch(arr, x):
    low, high = 0, len(arr)-1
    while low<=high:
        mid = low + (high-low)//2
        if arr[mid] == x:
            return mid+1
        elif arr[mid] <x :
            low = mid+1
        else:
            high = mid - 1
    return -1

arr = [8, 9, 10, 11]
print(binarysearch(arr, 10))