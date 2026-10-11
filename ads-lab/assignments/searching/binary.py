def binarysearch(arr, x):
    low, high = 0, len(arr)-1
    while low<=high:
        mid = low + (high-low)//2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid+1
        else:
            high = mid-1
    return -1

arr = [3,4,5,1,9,2,7,0,6]
print(binarysearch(arr, 9))